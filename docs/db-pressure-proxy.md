# Rebuilding Deutsche Bank's Pressure Index from public data

Deutsche Bank's Pressure Index — the institutional "TACO index" — was built by **Maximilian Uleer**'s cross-asset strategy team (~May 2025, after Liberation Day). It measures the politico-economic pressure on the US president to reverse course:

> *"If the index rises, the likelihood of a strategic adjustment by the U.S. administration increases. If all four pain points are hit, the incentive to adjust is very high."* — M. Uleer, Deutsche Bank

**Four equal-weight components, all as 4-week changes:** the S&P 500 (falling = pressure), the 10-year Treasury yield (rising = pressure), 1-year inflation expectations (rising = pressure), presidential approval (falling = pressure).

**The catch: DB never published the formula or a single numeric value.** Everything known about it is qualitative, via press coverage (Sam Ro's notes citing Robert Armstrong / FT Alphaville, Axios, Yahoo Finance). Which makes it a perfect candidate for open replication.

## The public recipe

| DB component | Public proxy | Source | Series |
|---|---|---|---|
| S&P 500, 4w change | S&P 500 index | FRED / market data | `SP500` |
| 10Y Treasury, 4w change | US 10Y constant-maturity yield | FRED | `DGS10` |
| 1Y inflation expectations, 4w change | U. Michigan 1Y expectations (monthly) or breakeven rates (daily) | FRED | `MICH`, `T5YIFR`/`T10YIE` |
| Approval rating, 4w change | polling averages | aggregators | scraped |

Sketch: invert the signs so that "pain" is always positive, z-score each component on a rolling window, average the four.

## Open problems (declared, not hidden)

1. **Inflation expectations**: the Michigan series is monthly; daily replication needs bond-market breakevens as a stand-in.
2. **Approval**: no official series; polling aggregators must be scraped.
3. **Normalization**: unknown whether DB uses z-scores, min-max, or something else.
4. **Window**: "4-week changes" could be 20 trading days or 28 calendar days.
5. **Oil/gas**: recent coverage mentions gasoline and crude as amplifiers — unclear whether they're formally in the index or qualitative color.

Any replication is therefore a *proxy with stated error bars*, and the readings in this repo mark it as such.

## Documented behavior (from press coverage)

Every documented peak of the index was followed by a backtrack within days to weeks (Liberation Day → 90-day pause in 7 days; the July 2025 EU-deadline peak → postponement in 1 day). Reported reliability is strong on tariffs and domestic policy, and explicitly uncertain on military geopolitics — *"the Strait of Hormuz cannot be reopened by executive fiat alone"* (Irish Times). That caveat is inherited by this instrument's own honesty notes.

## Sources

- Sam Ro, [Substack note](https://substack.com/@samro/note/c-233553540) (Mar 26, 2026)
- Axios — [Pressure on Trump? Wall Street's got an index for that](https://www.axios.com/2026/03/25/trump-stocks-gas-index)
- Yahoo Finance — [Wall Street Actually Came Up With an Index…](https://finance.yahoo.com/economy/policy/articles/wall-street-actually-came-index-221355598.html)
- CNBC — [Deutsche Bank raises S&P 500 forecast on TACO theory](https://www.cnbc.com/2025/06/03/deutsche-bank-raises-sp-500-forecast-on-taco-theory-we-will-get-further-relents.html) (Jun 3, 2025)
- Irish Times — [Trump under pressure, but it takes two to Taco on Iran](https://www.irishtimes.com/your-money/2026/03/29/trump-under-pressure-but-it-takes-two-to-taco-on-iran/)
- FT Alphaville, Robert Armstrong — "The heat is on" (Mar 26, 2026)
- Wikipedia — [Trump Always Chickens Out](https://en.wikipedia.org/wiki/Trump_Always_Chickens_Out)
