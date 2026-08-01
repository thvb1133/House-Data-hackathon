# House London #0 — submission

**Team name:** _fill this in before you submit_
**Brief:** PD (temporary accommodation) crossed with DE (permitted but unbuilt)
**Track:** Data, Policy and Software — the entry is deliberately legible to all three

**Live tool (no install):**
https://raw.githack.com/thvb1133/Data-hackathon-/cursor/homes-vs-hotels-f5eb/dist/homes-vs-hotels.html

**Code:** https://github.com/thvb1133/Data-hackathon-/pull/1
**Offline copy:** `dist/homes-vs-hotels.html` — one file, double-click, works with no wifi

## One-paragraph description

London has 100,930 children in temporary accommodation, the highest figure ever recorded and well
above the 85,000 still being quoted. Boroughs now spend £740m a year of their own money on it,
triple the 2021-22 figure and 71% of all homelessness spending. We set that against what London
approved and never built — 320,203 homes consented, 184,169 completed, 112,104 never started —
and then tested the obvious explanation. The boroughs with the worst temporary accommodation
crises are **not** the boroughs failing to build: across 31 boroughs the two are statistically
unrelated. London's unbuilt permissions are simply in the wrong places. From that we name six
boroughs where acute need and unstarted consent already coincide, holding 37,312 approved homes
that never broke ground against 24,585 households in temporary accommodation — the permission to
house every one of those families 1.5 times over already exists.

## Headline numbers

| | |
|---|---|
| Children in temporary accommodation, London, Dec 2025 | 100,930 |
| Households | 75,600 (+28.9% since 2019) |
| Net TA spend 2024-25 | £740m, up 204% in three years |
| Share of homelessness budget | 71% |
| Worst reserves exposure | Hillingdon, 287% of spendable reserves |
| Homes approved but never started | 112,104 |
| Need vs failure-to-build | ρ = −0.21, p = 0.25, n = 31 — no relationship |

## Data sources

All open. No data use agreement, nothing embargoed, fully reproducible from a clean clone.

- MHCLG statutory homelessness detailed local authority tables (TA1), Dec 2019–Dec 2025
- GLA London Plan Annual Monitoring Report 21, chapter 2 housing tables
- MHCLG local authority revenue outturn RO4 (spending) and RS (reserves)
- ONS Open Geography borough boundaries; postcodes.io for postcode lookup

WhereToBuild was deliberately not used: its agreement bars publishing results online before
contacting the authors, and this needed to be publicly shareable tonight.

## Reproduce it

```bash
python run.py
```

Downloads all seventeen source files, parses them, rebuilds the map, page and offline bundle,
and serves it. No credentials, no manual downloads.

## Checklist before 17:00

- [ ] Team name filled in above
- [ ] Repo link posted to GitHub or the House London Drive
- [ ] Community judging form submitted (one per team)
- [ ] `PITCH.md` rehearsed out loud, twice, against a timer
- [ ] Offline copy downloaded to the presenting laptop in case the wifi dies
