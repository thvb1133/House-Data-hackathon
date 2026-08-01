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

## Just look at it

No install, no terminal, nothing to run:

**https://raw.githack.com/thvb1133/Data-hackathon-/cursor/homes-vs-hotels-f5eb/dist/homes-vs-hotels.html**

`dist/homes-vs-hotels.html` is the whole tool — page, data, map and all — bundled into one
87 KB file. Download it and double-click it and it works offline, on any laptop, with no web
server. Useful when the venue wifi dies five minutes before a demo.

## Run it

You need no data files of your own. Every dataset is downloaded automatically from
gov.uk, the London Datastore and ONS. One command does everything, on any operating system:

```bash
python run.py
```

On macOS and Linux you may need `python3 run.py`. There is also `./run.sh` if you prefer bash.

It opens your browser at **http://localhost:8099** by itself. If it doesn't, type that address in
manually — or whatever address the script prints, since it moves to the next free port if 8099 is
taken. Press `Ctrl+C` in the terminal window to stop it.

The script installs the Python packages, downloads the official spreadsheets, parses them,
builds the map and the page payload, and starts a local web server. It takes a couple of
minutes the first time and a few seconds after that, because downloads are cached in
`data/raw/`. Safe to re-run any time.

**The site is only up while that terminal window is running.** Close the window, or press
`Ctrl+C`, and the page stops loading. That is normal — start it again with the same command.

### If something goes wrong

**"This site can't be reached" / `ERR_CONNECTION_REFUSED`** — nothing is serving the page. Either
the script was never started, or its terminal window was closed. Run `python run.py` again and
leave the window open.

**`OSError: [Errno 98] Address already in use`** — the opposite problem: it is already running,
so nothing is broken. `run.py` now steps to the next free port and prints which one it chose.

**`./run.sh` is not recognised** — you are on Windows, where that bash script does not apply.
Use `python run.py` instead.

**`permission denied: ./run.sh`** — macOS or Linux only. Run `chmod +x run.sh` once, then try again.

**A download fails** — re-run `./run.sh`. It keeps whatever it already fetched and only
retries the missing files.

If you would rather run the steps yourself:

```bash
python3 -m pip install pandas odfpy openpyxl
python3 scripts/fetch_data.py        # download the official source files (no login needed)
python3 scripts/extract_ta.py        # MHCLG homelessness tables -> TA panel
python3 scripts/extract_pipeline.py  # GLA AMR 21 -> approvals/starts/completions
python3 scripts/build_map.py         # boundaries -> site/boroughs.json
python3 scripts/build_site.py        # -> site/data.json
python3 -m http.server 8099 --directory site
```

`data/raw/` is gitignored, so a fresh clone re-downloads it. `site/` is a static page with no
build step and no runtime dependencies, so it can be published to GitHub Pages as-is.

## What's in the tool

- **Borough lookup** by dropdown or postcode, resolved through postcodes.io.
- **A clickable choropleth of all 33 boroughs**, switchable between temporary accommodation
  pressure and the homes approved but not built. Boundaries are projected and simplified into
  SVG paths at build time, so the map needs no mapping library and adds 35 KB.
- **An adjustable cost assumption.** The nightly rate is a slider, not a fixed number, because
  MHCLG does not publish borough TA spend. Every cost on the page follows it.
- **A trend chart** per borough, December to December.
- **A pre-written email to your councillor** carrying that borough's own figures and three
  questions a council has to answer in writing.

## Sources

- [MHCLG live tables on homelessness](https://www.gov.uk/government/statistical-data-sets/live-tables-on-homelessness) —
  detailed local authority data, table TA1, December quarters 2019–2025. Official statutory returns.
- [GLA London Plan Annual Monitoring Report 21](https://data.london.gov.uk/dataset/london-plan-amr-21-data-tables)
  (January 2026), chapter 2 housing tables — approvals, starts and completions by planning authority,
  2019/20 to 2023/24.
- [ONS Open Geography](https://geoportal.statistics.gov.uk) — local authority district boundaries,
  December 2025, super-generalised and clipped, carrying the same E09 codes as the statistics.
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
  daily figure applies one flat nightly rate, exposed as a slider rather than buried. Order of
  magnitude only.
- **Two development corporations** (Old Oak and Park Royal, London Legacy) are the planning
  authority for parts of several boroughs, so their consents are missing from those boroughs' rows.
- **Two boroughs did not return usable TA data in December 2019**, so their change figure runs from
  the first year they did, labelled per borough.
- **Out-of-borough placements are counted by the placing borough**, so exporting boroughs look worse
  and receiving boroughs do not appear at all.
