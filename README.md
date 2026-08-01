# Homes vs Hotels

**London has 100,930 children living in temporary accommodation — the highest figure on record.
Over the same period, the city granted permission for 320,203 homes and completed 184,169.**

A borough-by-borough lookup built at House London #0, Newspeak House, 1 August 2026.
Type in a postcode, see what your borough is spending on accommodation it does not own, see the
homes it approved and did not build, and send the two numbers to your councillor.

Briefs: **PD** (is temporary accommodation bankrupting London's boroughs?) crossed with **DE**
(the gap between permitted and built).

## The finding

| | London, latest published |
|---|---|
| Households in temporary accommodation | 75,600 |
| Children in temporary accommodation | 100,930 |
| Change since December 2019 | +28.9% |
| Homes approved, 2019/20–2023/24 | 320,203 |
| Homes completed, same period | 184,169 |
| Completion rate | 57.5% |

Two numbers worth sitting with. The select committee evidence widely quoted this year put
85,000+ children in temporary accommodation in London; the December 2025 return puts it at
**100,930**. The figure dipped through the pandemic years and has risen every quarter since 2022.

Newham is the sharpest case: **one in every 17 households** in the borough is in temporary
accommodation.

## Run it

```bash
pip install pandas odfpy openpyxl
python3 scripts/extract_ta.py         # MHCLG statutory homelessness tables -> TA panel
python3 scripts/extract_pipeline.py   # GLA AMR 21 -> approvals/starts/completions by borough
python3 scripts/build_site.py         # -> site/data.json
python3 -m http.server 8099 -d site
```

`data/raw/` is gitignored. Download links are listed in `scripts/download_notes.md`.
The site is a single static page with no build step and no dependencies, so it can be served
from GitHub Pages as-is.

## Sources

- [MHCLG live tables on homelessness](https://www.gov.uk/government/statistical-data-sets/live-tables-on-homelessness) —
  detailed local authority data, table TA1, December quarters 2019–2025. Official statutory returns.
- [GLA London Plan Annual Monitoring Report 21](https://data.london.gov.uk/dataset/london-plan-amr-21-data-tables)
  (January 2026), chapter 2 housing tables — approvals, starts and completions by planning authority,
  2019/20 to 2023/24.
- [postcodes.io](https://postcodes.io) — postcode to borough lookup, client-side.

All open data. No data use agreement, nothing under embargo, everything reproducible from the
scripts in this repo.

## What we're less sure about

The page says this in full, but the short version:

- **The approvals gap is not proof of land banking.** Homes approved in 2023/24 could not have
  completed by 2023/24, so part of the gap is ordinary build-out time. It measures consent running
  ahead of delivery over a fixed window — not sites deliberately sat on. Separating the two needs
  site-level permission dates from the London Development Database.
- **Cost is an assumption.** MHCLG does not publish TA spend by borough in this release, so the
  daily figure applies one flat nightly rate, shown on the face of the page. Order of magnitude only.
- **Two development corporations** (Old Oak and Park Royal, London Legacy) are the planning
  authority for parts of several boroughs, so their consents are missing from those boroughs' rows.
- **Two boroughs did not return usable TA data in December 2019**, so their change figure runs from
  the first year they did, labelled per borough.
- **Out-of-borough placements are counted by the placing borough**, so exporting boroughs look worse
  and receiving boroughs do not appear at all.
