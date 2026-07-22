#!/usr/bin/env python3
"""Polymarket adapter (v1) — daily snapshot + day-over-day spike, config-driven themes.

This is the pipeline-grade evolution of `polymarket_gamma.py` (v0), and the one
the daily pipeline actually runs (via cron, minutes before the scoring pass):

1. fetch the top-N active markets by volume from Polymarket's public Gamma API
   (no key, stdlib only);
2. filter them into THEMES read from a JSON config — edit the config, not the
   code, when the hot theme changes;
3. write a dated snapshot, and DIFF it against the most recent previous
   snapshot: per-market repricing -> a suggested raw 0-100 for the
   prediction-market-spike component.

The honesty contract, unchanged from v0 but now measurable:
- a *spike* is a change between two snapshots — the first run only lays the
  baseline (suggested_raw stays null);
- suggested_raw measures MAGNITUDE only (|delta| 0.10 -> 60). The tool cannot
  know which outcome means "escalation": direction is the analyst's call, and
  the per-market repricing list is there so the call can be cited.

Usage:
    python3 adapters/polymarket_snapshot.py
    python3 adapters/polymarket_snapshot.py --config my_themes.json --out-dir snaps
Cron example (daily, before the scoring pass):
    25 6 * * 1-5 cd /path/to/repo && python3 adapters/polymarket_snapshot.py
"""
import argparse
import json
import urllib.request
from datetime import date
from pathlib import Path

GAMMA = "https://gamma-api.polymarket.com/markets"
UA = {"User-Agent": "taco-score-adapter/1.0 (+https://github.com/HiroshigeG/taco-score)"}
DEFAULT_CONFIG = Path(__file__).resolve().parent / "themes.json"
DEFAULT_THEMES = {"iran_hormuz": ["hormuz", "iran", "strait"],
                  "tariffs_trade": ["tariff", "trade war", "trade deal"]}
TOP_N = 12          # markets kept per theme
SPIKE_SCALE = 600   # |price delta| 0.10 -> raw 60; 0.15+ -> ~90; capped at 100


def load_themes(config_path: Path):
    try:
        cfg = json.loads(config_path.read_text())
        themes = {k: [str(w).lower() for w in v] for k, v in cfg["themes"].items() if v}
        if themes:
            return themes, str(config_path)
    except (OSError, ValueError, KeyError, AttributeError):
        pass
    return DEFAULT_THEMES, "builtin-default"


def fetch_markets(pages: int = 4, page_size: int = 100) -> list:
    # The Gamma API caps `limit` at 100: paginate with offset (4 pages = top 400)
    out = []
    for i in range(pages):
        url = (f"{GAMMA}?closed=false&order=volumeNum&ascending=false"
               f"&limit={page_size}&offset={i * page_size}")
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            batch = json.loads(r.read().decode())
        if not batch:
            break
        out.extend(batch)
    return out


def parse_outcomes(m: dict) -> dict:
    try:
        prices = json.loads(m["outcomePrices"]) if isinstance(m.get("outcomePrices"), str) \
            else m.get("outcomePrices") or []
        outcomes = json.loads(m["outcomes"]) if isinstance(m.get("outcomes"), str) \
            else m.get("outcomes") or []
        return {o: round(float(p), 3) for o, p in zip(outcomes, prices)}
    except (KeyError, ValueError, TypeError):
        return {}


def matches(m: dict, words: list) -> bool:
    text = " ".join(str(m.get(k, "")) for k in ("question", "slug", "description")).lower()
    return any(w in text for w in words)


def previous_snapshot(out_dir: Path, today_name: str):
    older = sorted(p for p in out_dir.glob("polymarket-*.json") if p.name < today_name)
    for p in reversed(older):
        try:
            snap = json.loads(p.read_text())
            if not snap.get("error"):
                return snap
        except ValueError:
            continue
    return None


def build(config_path: Path, pages: int) -> dict:
    markets = fetch_markets(pages=pages)
    themes, themes_source = load_themes(config_path)
    themes_out = {}
    for theme, words in themes.items():
        hits = []
        for m in markets:
            if not matches(m, words):
                continue
            hits.append({
                "question": m.get("question"),
                "slug": m.get("slug"),
                "outcomes": parse_outcomes(m),
                "volume_usd": round(float(m.get("volumeNum") or 0)),
                "end_date": m.get("endDate"),
            })
        themes_out[theme] = hits[:TOP_N]
    return {"markets_scanned": len(markets), "themes_source": themes_source,
            "themes": themes_out}


def diff(today: dict, prev) -> dict:
    if not prev:
        return {"suggested_raw": None,
                "note": "First snapshot: nothing to compare against. "
                        "The spike becomes measurable from the next run."}
    prev_by_slug = {}
    for hits in prev.get("themes", {}).values():
        for h in hits:
            prev_by_slug[h.get("slug")] = h
    deltas, max_delta = [], 0.0
    for theme, hits in today.get("themes", {}).items():
        for h in hits:
            p = prev_by_slug.get(h.get("slug"))
            if not p or not h.get("outcomes") or not p.get("outcomes"):
                continue
            for outcome, price in h["outcomes"].items():
                if outcome not in p["outcomes"]:
                    continue
                d = round(price - p["outcomes"][outcome], 3)
                if abs(d) >= 0.01:
                    deltas.append({"theme": theme, "question": h["question"],
                                   "outcome": outcome, "prev": p["outcomes"][outcome],
                                   "now": price, "delta": d})
                max_delta = max(max_delta, abs(d))
    deltas.sort(key=lambda x: -abs(x["delta"]))
    return {
        "vs_snapshot": prev.get("date"),
        "repricings": deltas[:15],
        "max_abs_delta": round(max_delta, 3),
        "suggested_raw": min(100, round(max_delta * SPIKE_SCALE)),
        "note": ("suggested_raw measures MAGNITUDE only (|delta| 0.10 -> 60). "
                 "Direction (escalation vs de-escalation) is the analyst's call — "
                 "made citable by the per-market repricing list above."),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG,
                    help="themes JSON (default: themes.json next to this file)")
    ap.add_argument("--out-dir", type=Path, default=Path("polymarket-snapshots"),
                    help="where dated snapshots accumulate (default: ./polymarket-snapshots)")
    ap.add_argument("--pages", type=int, default=4,
                    help="Gamma pages of 100 markets to scan (default 4 = top 400)")
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    out_path = args.out_dir / f"polymarket-{today}.json"
    payload = {"date": today, "source": "Polymarket Gamma API (public, no key)",
               "component": "polymarket_spike", "error": None}
    try:
        data = build(args.config, args.pages)
        payload.update(data)
        payload["spike"] = diff(data, previous_snapshot(args.out_dir, out_path.name))
    except Exception as e:  # fail-soft: downstream consumers check `error`
        payload["error"] = f"{type(e).__name__}: {e}"
    out_path.write_text(json.dumps(payload, indent=1, ensure_ascii=False))
    matched = sum(len(v) for v in payload.get("themes", {}).values()) if not payload["error"] else 0
    print(f"polymarket-snapshot {today}: error={payload['error']} matched={matched} "
          f"raw={payload.get('spike', {}).get('suggested_raw')} -> {out_path}")


if __name__ == "__main__":
    main()
