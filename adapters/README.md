# Adapters — the roadmap, sprouting

Reference implementations of the "public adapters" roadmap item: **stdlib-only, no keys, runnable today**. Each emits the component contract (`raw` 0–100 + evidence note) that the scorer consumes.

| Adapter | Component | Source | Status |
|---|---|---|---|
| `polymarket_snapshot.py` | Prediction-market spike | Polymarket Gamma API (public) | **v1 — runs in the daily pipeline** |
| `polymarket_gamma.py` | Prediction-market spike | Polymarket Gamma API (public) | v0 — one-shot level snapshot |
| `futures_volume.py` | Futures volume anomaly | Yahoo public chart endpoint | v0 |

```bash
# v1: config-driven themes, dated snapshots, day-over-day spike scoring
python3 adapters/polymarket_snapshot.py
python3 adapters/polymarket_snapshot.py --config my_themes.json --out-dir snaps

# v0 one-shots
python3 adapters/polymarket_gamma.py --theme "hormuz,iran,strait"
python3 adapters/futures_volume.py --symbol CL=F
```

## How v1 works — and what it refuses to do

1. **Scan**: top 400 active markets by volume (Gamma caps pages at 100, so it paginates).
2. **Filter into themes** from [`themes.json`](themes.json) — a config file, because the hot theme changes faster than code should. Edit the JSON, the next run picks it up.
3. **Snapshot + diff**: writes `polymarket-YYYY-MM-DD.json` and compares against the previous snapshot. Per-market repricings → `suggested_raw` 0–100 (scale: |Δprice| 0.10 → 60).
4. **The refusal**: `suggested_raw` is **magnitude only**. The tool cannot know whether "Yes" on a given market means escalation or de-escalation — that judgment belongs to the research layer, which adjusts the number for direction *and must cite the repricing list when doing so*. First run = baseline only (`suggested_raw: null`), because a *spike* is a change between two snapshots, not a level.

Wire it with cron a few minutes before your scoring pass:

```cron
25 6 * * 1-5 cd /path/to/repo && python3 adapters/polymarket_snapshot.py
```

Design intent: where an API exists, the component becomes deterministic and nearly free — the AI research layer stays only where judgment is required (rhetoric, theme relevance, direction-vs-threat). Every adapter states its own limits in its output notes.
