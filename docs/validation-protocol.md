# Validation protocol — frozen before the data grows

*Registered 2026-07-22. The point of freezing this now: when new readings arrive, the rules for judging them are already written — no moving the goalposts, no cherry-picking horizons after the fact.*

## What each level claims (and what would validate it)

| Level | The claim | Validated by | Falsified by |
|---|---|---|---|
| LOW <33 | no reversal setup | **quiet**: no completed backtrack event AND no sustained escalation break within the horizon | a major backtrack or escalation event the score didn't see building |
| MEDIUM 33–66 | pieces assembling, not actionable | no completed cycle event within the horizon (a fading flare counts as correct) | a full backtrack completing inside the horizon (the score should have been HIGH) |
| HIGH >66 | today resembles the days that preceded historical climb-downs | a **climb-down/backtrack event** on the active theme within the horizon | escalation holds *and intensifies* with no retreat component |
| EXTREME | maximum resemblance | as HIGH, with the event typically arriving in days | as HIGH |

## Rules

1. **Horizon**: 7 calendar days primary; days-to-event recorded exactly. A 48h sub-horizon is recorded when the reading itself stated one.
2. **Outcome labels** (closed set): `backtrack_completed` · `mixed_partial` (retreat on one axis, hold on another) · `escalation_held` · `quiet_continued` · `flare_faded` · `quiet_then_reescalation_dayN` (event outside horizon, day noted).
3. **Evidence dating**: outcomes are labeled only from sources dated *after* the reading. Later readings in this repo count as evidence for earlier ones (they documented what happened in between).
4. **Partial credit is declared, never averaged away**: a `mixed_partial` is reported as ~½, not rounded up.
5. **Metrics**: hit-rate by level now (n is tiny and says so); **Brier score and a calibration curve only when n ≥ 30** — with n=10 a calibration plot would be theater.
6. **Control theme** (open TODO): pick a noisy geopolitical theme with *no* threaten-retreat history; the instrument must stay LOW on it. Specificity needs its own test.
7. **No survivorship**: every produced reading is in [`../data/outcomes.json`](../data/outcomes.json), including gaps and failures (the 3-week credential gap is part of the record).

## Current scorecard (n=10 — promising, not proven)

- HIGH/EXTREME readings: 4 → **3 full backtracks within 7 days, 1 mixed_partial (day 1)**
- LOW readings: 4 → **4/4 quiet_continued**
- MEDIUM readings: 2 → **2/2 no completed event** (one flare faded; one re-escalated on day 9, outside horizon — and that reading's own note flagged the coming watch window)

Machine-readable: [`../data/outcomes.json`](../data/outcomes.json).
