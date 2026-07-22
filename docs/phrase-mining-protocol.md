# Phrase-mining protocol — pre-registered

*Registered 2026-07-22, before any mining. The hypotheses below are frozen now so the eventual analysis can't cherry-pick: whatever the archives say — including "no effect" — gets published.*

## Why pre-register

The rhetoric and timing components currently encode folk hypotheses (night/weekend posts precede reversals; certain phrasings are tells). The event-study literature validated that presidential posts move markets — but nobody has validated the *reversal-timing* folklore. Mining archives *after* forming beliefs invites confirmation bias; registering the tests first is the only honest order.

## Data

- **Trump Twitter Archive** (complete through Jan 2021) — timestamps, full text
- **Truth Social trackers/archives** (2022→) — timestamps, full text
- Event labels: the completed threaten→retreat cycles (this repo's readings + press-documented backtracks with dates)

## Frozen hypotheses

**H1 — the sign-off tell.** Posts ending in the signature *"Thank you for your attention to this matter!"* are disproportionately followed (≤72h) by escalation-HOLD rather than retreat, versus threat-posts without the sign-off.
*Rationale to test, not assume: the formal sign-off may mark performative/settled positions rather than negotiating ones.*

**H2 — night/weekend timing.** Threat-posts published 22:00–06:00 ET or on weekends are followed by a retreat within 72h at a higher rate than weekday/daytime threat-posts. *(This is the current `timing_urgency` bonus — it has never been measured.)*

**H3 — ALL-CAPS intensity.** The CAPS-density percentile of a threat-post correlates with the magnitude of the same-day market move (oil for supply themes, index futures otherwise) — but **not** with the probability of eventual retreat.
*If true: CAPS measures market-moving power, not resolve — which would justify keeping rhetoric and volume as separate components.*

**H4 — repetition decay.** The Nth threat on the same theme within 30 days moves markets less than the (N−1)th ("boy who cried wolf" — observed qualitatively on Jul 1, never measured).

## Method (frozen)

1. Define threat-posts by a fixed keyword lexicon (published with the analysis, versioned).
2. Label each threat-post's 72h window: `retreat` / `hold` / `escalate` from dated press.
3. Tests: two-proportion comparisons for H1/H2, rank correlation for H3, per-theme regression for H4. Report **effect sizes with confidence intervals**, not just p-values.
4. Multiple-comparison correction across the four hypotheses (Holm).
5. Negative results are published with the same prominence as positive ones.

## What this feeds

- H2 outcome → recalibrate (or delete) the timing bonus in `timing_urgency`
- H3 outcome → validate the rhetoric/volume separation
- H1/H4 outcomes → candidate new sub-signals, only if effect sizes survive

*Status: protocol registered, mining not started.*
