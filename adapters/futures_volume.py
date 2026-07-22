#!/usr/bin/env python3
"""Futures volume adapter (v0) — the heaviest component from real market data.

Reference implementation of the roadmap item "public adapters": stdlib only,
no key. Pulls daily bars for a futures contract (default WTI, CL=F) from
Yahoo's public chart endpoint and scores the volume anomaly + price direction
into the component contract:

    {"component": "volume_anomaly_futures", "raw": <0-100>, "note": "...", "evidence": {...}}

Scoring (v0 heuristic, stated openly — calibration is the validation
protocol's job, not this script's):
    volume_ratio = last_volume / SMA20(volume)
    reactive     = |last_day_%| >= 1.0
    raw = base(volume_ratio) +15 if price is reactive, capped 0-100
    base: <0.8x -> 10 · 0.8-1.2x -> 25 · 1.2-2x -> 45 · 2-4x -> 65 · >4x -> 85

Usage:
    python3 adapters/futures_volume.py                # WTI (CL=F)
    python3 adapters/futures_volume.py --symbol ES=F  # S&P e-mini
"""
import argparse
import json
import urllib.request

CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=3mo&interval=1d"
UA = {"User-Agent": "Mozilla/5.0 (taco-score-adapter/0.1)"}


def fetch(sym: str) -> dict:
    req = urllib.request.Request(CHART.format(sym=sym), headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())["chart"]["result"][0]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="CL=F", help="futures symbol (default CL=F, WTI)")
    args = ap.parse_args()

    data = fetch(args.symbol)
    q = data["indicators"]["quote"][0]
    closes = [c for c in q["close"] if c is not None]
    vols = [v for v in q["volume"] if v]
    if len(vols) < 21 or len(closes) < 2:
        raise SystemExit(json.dumps({"error": "not enough bars"}))

    last_v, sma20 = vols[-1], sum(vols[-21:-1]) / 20
    ratio = last_v / sma20
    day_pct = (closes[-1] / closes[-2] - 1) * 100
    reactive = abs(day_pct) >= 1.0

    base = 10 if ratio < 0.8 else 25 if ratio < 1.2 else 45 if ratio < 2 else 65 if ratio < 4 else 85
    raw = min(100, base + (15 if reactive else 0))

    out = {
        "component": "volume_anomaly_futures",
        "source": f"Yahoo public chart endpoint ({args.symbol}, daily bars, no key)",
        "raw": raw,
        "note": (f"Volume {ratio:.2f}x the 20-day average "
                 f"({'above' if ratio >= 1 else 'below'} normal); last close "
                 f"{closes[-1]:.2f} ({day_pct:+.2f}% on the day, "
                 f"{'reactive' if reactive else 'muted'}). v0 heuristic scale — "
                 "direction-vs-threat judgment still needs the analysis layer: "
                 "this adapter measures the tape, not the story."),
        "evidence": {
            "last_volume": last_v,
            "sma20_volume": round(sma20),
            "volume_ratio": round(ratio, 2),
            "last_close": round(closes[-1], 2),
            "day_change_pct": round(day_pct, 2),
            "bars": len(vols),
        },
    }
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
