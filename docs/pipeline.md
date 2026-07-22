# How a reading is made — the pipeline

Two AI agents with separated jobs, a strict JSON contract, and deterministic arithmetic on top. The human designs the instrument and the contract; the pipeline does the daily legwork; nothing about the final number is vibes.

```
06:00 ET  ┌────────────────┐   signals JSON   ┌─────────────────┐   reading JSON
scheduled │ signal-scanner │ ───────────────► │ pattern-analyzer │ ─────────────► logs/taco-score-YYYY-MM-DD.json
          └────────────────┘                  └─────────────────┘                       │
          collects, never scores              scores, never collects                    ▼
                                                                                 gauge / dashboard
```

**Separation of concerns:** the scanner *collects* (posts, futures, prediction markets, news, central-bank calendar) and is forbidden from judging; the analyzer *scores* against the methodology and historical patterns and is forbidden from collecting. Each reading records its `score_source` (scheduled vs manual run) and a `confidence`.

**The contract is the honesty mechanism.** Every component must ship `raw`, `weight`, and a written evidence `note`; the backtrack flag requires a quote; proxied fields must say they're proxied; anything not cleanly fetched is marked *to re-validate*. When two runs disagreed (Apr 7), the resolution was written into the reading as a reconciliation note instead of silently overwriting. The demo page recomputes the weighted sum in front of you — including the one day it doesn't match.

---

## Reference prompt 1 — morning scan

*Translated from the Italian original. Position-monitoring sections removed for publication — the score itself is market-wide by construction and never needed them.*

> **@signal-scanner**
>
> Scan all relevant signals from the last 12 hours:
>
> 1. **Truth Social**: latest posts — tone, theme, timing, ALL-CAPS usage
> 2. **Premarket**: anomalous volume on oil futures (WTI, Brent), S&P e-Mini, defense stocks
> 3. **Prediction markets**: moves correlated to the active themes (conflict, tariffs, trade)
> 4. **News**: official statements, leaks, rumors, foreign-government reactions
> 5. **🏦 CENTRAL BANKS TODAY (mandatory, never skip)**: check whether a rate decision from ECB, Fed (FOMC), BoE or BoJ lands today or tomorrow. If yes: date/time, consensus expectation, what's priced in. If one landed in the last 24h: the actual outcome. Add to the JSON: `"central_banks": [{"bank":"…","event":"rate decision","when":"…","expected":"…","actual":"…"}]`, else `[]`.
>    *(Added after a scheduled scan missed a fully-priced ECB hike — the calendar check became mandatory the next day. Instruments improve by writing their misses into the procedure.)*
>
> Output structured JSON. Save to `logs/scan-YYYY-MM-DD.json`.
> If there are no relevant signals, write `{"signals": [], "note": "no signal"}` and stop.

## Reference prompt 2 — TACO analysis

*Translated from the Italian original; internal paths generalized.*

> **@pattern-analyzer**
>
> Analyze the signals collected by today's morning scan (`logs/scan-YYYY-MM-DD.json`).
>
> 1. Compute the current TACO Score (0–100) per the methodology
> 2. Compare against the historical TACO patterns (Liberation Day, China, Iran)
> 3. What is the backtrack probability?
> 4. On what timeline (hours, 1–2 days, 3–5 days)?
> 5. Which historical TACO does today resemble most?
>
> MANDATORY — EXECUTE, don't describe: at the end of the analysis you MUST write
> `logs/taco-score-YYYY-MM-DD.json` (today's date) using the Write tool. If the
> file already exists, OVERWRITE it with your richer version: include
> `taco_score`, `level`, the components with raw/weighted values, the pattern
> match and the backtrack probability. Set `"score_source"` accordingly. Do not
> ask for confirmation, do not close with questions: the run is non-interactive
> and the written file is the only output that counts.
>
> **Backtrack detection** — if the analyzed signals contain de-escalation
> keywords (ceasefire, deal, backs down, pause, extension, rollback, withdraw,
> suspend), add to the JSON output:
>
> ```json
> "backtrack_detected": true,
> "backtrack_evidence": "specific headline or quote"
> ```
>
> If there are no backtrack signals, omit these fields entirely (never write `false`).

---

## Design notes worth stealing

- **"EXECUTE, don't describe"** — non-interactive agent runs need the output contract stated as an obligation, or you get essays instead of artifacts.
- **Omit-when-absent beats `false`** — a `backtrack_detected: false` invites dashboards to render a reassuring "no backtrack" out of silence; omission forces consumers to treat absence as absence.
- **Write the miss into the procedure** — the central-bank block exists because a scan missed one. The prompt is the changelog.
