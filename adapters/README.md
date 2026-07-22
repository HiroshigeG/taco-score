# Adapters (v0) — the roadmap, sprouting

Reference implementations of the "public adapters" roadmap item: **stdlib-only, no keys, runnable today**. Each emits the component contract (`raw` 0–100 + evidence note) that the scorer consumes.

| Adapter | Component | Source |
|---|---|---|
| `polymarket_gamma.py` | Prediction-market spike | Polymarket Gamma API (public) |
| `futures_volume.py` | Futures volume anomaly | Yahoo public chart endpoint |

```bash
python3 adapters/polymarket_gamma.py --theme "hormuz,iran,strait"
python3 adapters/futures_volume.py --symbol CL=F
```

Design intent: where an API exists, the component becomes deterministic and nearly free — the AI research layer stays only where judgment is required (rhetoric, theme relevance, direction-vs-threat). Both adapters state their v0 limits in their own output notes.
