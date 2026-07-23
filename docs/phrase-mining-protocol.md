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

---

## Run 1 — first results (2026-07-23)

As promised above: results get published, **including the negative ones**. First
execution on the full public archive (34,842 posts, CC0 mirror, `created_at` in UTC
verified from the scraper source).

**Descriptives (full corpus, maximum power):**
- Volume: mean 22.6 posts/active-day (median 18, max 138); 2025 total = 6,229 posts —
  matching the independent Roll Call count to within their published range.
- Hourly distribution: the evening peak is REAL — 18:00 ET is the top hour of 2025
  with 493 posts (Roll Call independently reports 494 — a single-count match,
  strong evidence both measure the same underlying corpus). The 17-18 ET block holds
  14.3% of 2025 posts vs 8.3% uniform. Nuance: over the whole corpus the absolute
  max is 11:00 ET; the evening peak strengthens year over year. Two frontier-model
  adversarial reviews reached OPPOSITE verdicts on this claim before the corpus
  settled it — a good illustration of why we run the data instead of trusting reviews.

**Pre-registered hypotheses vs. labeled events (~20-30 cycles, theme-level labels —
low power, declared):**
- **H1 (sign-off → HOLD): REFUTED in direction.** The "attention to this matter"
  sign-off is MORE frequent on the retreat-prone Iran theme (79.5%) than on
  tariff-HOLD themes (23.7%) — the opposite of the prediction. The signature has
  migrated from pasted formal letters to ordinary posts (287 vs 173 occurrences) and
  now co-occurs with THREAT language (lift 9.4). H1 as originally stated does not
  survive; the sign-off is a variable of its own, not a tell of resolve.
- **H2 (night/weekend timing): INCONCLUSIVE**, weakly favorable — 47% of pre-retreat
  windows are night-or-weekend vs a corpus base-rate of 33.3% (n=17). Side product:
  the corrected hourly base-rate that published studies skip.
- **H3 (CAPS ↔ magnitude): INCONCLUSIVE**, right sign — Spearman ρ +0.60 on n=5
  (zero-move days had CAPS_max 0.11-0.15; max-move days had CAPS_max 1.0).
- Top co-occurrence lifts: tariffs×Canada 32.8 · tariffs×threat 27.3 · tariffs×EU 25.5.

**Honest limits:** event labels are theme-level (not post-level), n is small, no test
reaches significance after Holm. Run 2 needs: post-level outcome labels, a placebo
lexicon control, daily market data joins, and the Section 122 expiry (Jul 24) as a
fresh out-of-sample event.
