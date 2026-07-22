#!/usr/bin/env python3
"""Polymarket adapter (v0) — the prediction-market component from the REAL public API.

Reference implementation of the roadmap item "public adapters": stdlib only,
no key, no dependency. Fetches active markets from Polymarket's public Gamma
API, filters by theme keywords, and emits the component contract:

    {"component": "polymarket_spike", "raw": <0-100|null>, "note": "...", "markets": [...]}

Honesty note baked in: a *spike* needs two snapshots. A single run reports the
level and flags raw as provisional; run it twice (e.g. daily) and diff.

Usage:
    python3 adapters/polymarket_gamma.py --theme "hormuz,iran,strait"
    python3 adapters/polymarket_gamma.py --theme tariff --limit 200
"""
import argparse
import json
import urllib.request

GAMMA = "https://gamma-api.polymarket.com/markets"
UA = {"User-Agent": "taco-score-adapter/0.1 (+https://github.com/HiroshigeG/taco-score)"}


def fetch_markets(limit: int) -> list:
    url = f"{GAMMA}?closed=false&order=volumeNum&ascending=false&limit={limit}"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def matches(m: dict, words: list) -> bool:
    text = " ".join(str(m.get(k, "")) for k in ("question", "slug", "description")).lower()
    return any(w in text for w in words)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", required=True,
                    help="comma-separated keywords, e.g. 'hormuz,iran,strait'")
    ap.add_argument("--limit", type=int, default=300,
                    help="how many top-volume active markets to scan")
    args = ap.parse_args()
    words = [w.strip().lower() for w in args.theme.split(",") if w.strip()]

    markets = fetch_markets(args.limit)
    hits = []
    for m in markets:
        if not matches(m, words):
            continue
        try:
            prices = json.loads(m["outcomePrices"]) if isinstance(m.get("outcomePrices"), str) \
                else m.get("outcomePrices") or []
            outcomes = json.loads(m["outcomes"]) if isinstance(m.get("outcomes"), str) \
                else m.get("outcomes") or []
        except (KeyError, ValueError):
            prices, outcomes = [], []
        hits.append({
            "question": m.get("question"),
            "outcomes": dict(zip(outcomes, [round(float(p), 3) for p in prices])) if prices else None,
            "volume_usd": round(float(m.get("volumeNum") or 0)),
            "end_date": m.get("endDate"),
        })

    out = {
        "component": "polymarket_spike",
        "source": "Polymarket Gamma API (public, no key)",
        "theme": words,
        "markets_scanned": len(markets),
        "markets_matched": len(hits),
        "markets": hits[:15],
        "raw": None,
        "note": ("Level snapshot only: a SPIKE is a change between two snapshots. "
                 "Run daily and diff to score raw 0-100 per the methodology "
                 "(repricing magnitude + direction vs the active theme)."),
    }
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
