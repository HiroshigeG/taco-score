# TACO Score — Methodology

The score is a weighted sum of **seven components**, each rated 0–100 from public signals, then rounded:

```
weighted_i = raw_i × weight_i / 100
score      = round(Σ weighted_i)
```

**Levels:** `LOW` < 33 · `MEDIUM` 33–66 · `HIGH` > 66 · `EXTREME` is reserved for peak readings (used once, Apr 7 2026, score 78 in a maximally stretched setup).

Reference reading with every field populated: [`examples/2026-07-20-high.json`](../examples/2026-07-20-high.json) (72/HIGH, Iran/Hormuz kinetic re-escalation).

---

## The seven components

### 1. Rhetoric intensity — weight 20
How aggressive and extreme the day's posts are: intensity keywords ("obliterate", "immediately"), ALL-CAPS, named attacks, ultimatums. **Crucially: a violent post *on the market-moving theme* scores high; an aggressive post on an unrelated theme scores lower.**
Scale anchors: 0 = no relevant posts · ~55 = aggressive but not extreme · 85+ = peak rhetoric ("attacking them tonight"). Jul 20 reading: **85**.

### 2. Timing urgency — weight 15
The posting pattern (night / pre-market / **weekend** posts carry a structural reversal bonus — historical backtracks often start there) plus proximity of macro events (central-bank decisions within 48h amplify).
Jul 20 reading: **68** (continuous escalation with a hard deadline, but missing the classic isolated pre-reversal night post).

### 3. Pressure index — weight 15
An aggregate threat/pressure level. **In this public version it is a declared proxy** (the original private feed is not shipped); candidate public sources: GDELT tone, news-sentiment/escalation-count composites. Readings that used the proxy say so in their notes.
Jul 20 reading: **72** (proxied, declared).

### 4. Futures volume anomaly — weight 20 (often the decisive tell)
Volume/price anomalies in oil (`CL=F`) and S&P (`ES=F`) futures consistent with smart-money front-running around the posts. **The contrarian case matters most:** when price *doesn't* react to an escalation ("boy who cried wolf"), the score should stay low no matter how loud the rhetoric — this is exactly what kept the Jul 1 reading at 47 while threats were at full volume (oil was falling).
Scale anchors: 15 = no anomaly / price moving against the threat · 58+ = oil genuinely reactive. Jul 20 reading: **58**.

### 5. Prediction-market spike — weight 10
Repricing in event-market odds (peace deal / diplomatic meeting / conflict contracts). A spike of deal-making optimism is consistent with a reversal forming; a collapse toward conflict is escalation.
Jul 20 reading: **62** (large, recent repricing).

### 6. Historical precedent — weight 10
How strong and recent the precedent is *on the same theme*. A theme with a completed recent TACO cycle scores high.
Jul 20 reading: **93** (same-theme backtrack six days earlier).

### 7. Approval pressure — weight 10
Domestic political pressure pushing toward a climb-down: approval ratings when fresh, visible proxies otherwise (declared).
Jul 20 reading: **68** (fresh polling near lows, unpopular war).

---

## Backtrack detection

If de-escalation language appears in the day's signals — *ceasefire, deal, backs down, pause, extension, rollback, withdraw, suspend* — the reading sets:

```json
"backtrack_detected": true,
"backtrack_evidence": "quoted headline or post"
```

The flag is evidence-carrying by contract: no quote, no flag.

## Pattern comparison

Each reading compares the current setup against the canonical historical TACO cycles (Liberation-Day tariffs, China rollback, Iran/Hormuz) and records `best_match`, a `similarity` estimate, `key_differences`, and the `historical_outcome` — which is where context gets to overrule the number (see below).

## Schema generations

The instrument evolved while running. The data declares it instead of hiding it:

- **gen-1** (Mar 31, Apr 5): prototype — raw component values only, no recorded weights, levels predate the standardized thresholds (shown as recorded, with a footnote).
- **gen-2** (Apr 7, Apr 9): weights appear (as fractions), two experimental components (`budget_signaling`, `defense_down_signal`) were tried and later dropped. The Apr 7 reading carries a written **reconciliation note**: two runs disagreed (68 vs 84) and the recorded 78 integrates both — the component sum (79.8) intentionally doesn't round to it.
- **gen-3** (Jun–Jul): the full contract — 7 canonical components with notes, lifecycle tracking, market snapshot, confidence, analyst note.

## Calibration notes from the real cases

1. **Component 4 is the discriminant.** When the market ignores the threat, the TACO-as-market-mover thesis deflates even with rhetoric at maximum. Jul 1 vs Jul 20 differ almost entirely on this component (15 → 58).
2. **Context beats the number.** A 72/HIGH during a real kinetic war is HIGH for tension and pattern-similarity, but the *chickens-out* base rate is weakened when there are real casualties — the escalation may hold. The reading's own `analyst_note` and `historical_outcome` are where this is written down.
3. **Proxy honesty.** Anything not cleanly fetchable (pressure feed, some snapshot prices) is marked *proxied* or *to re-validate* in the data itself. The demo page surfaces those flags rather than smoothing them over.
