# Three-minute pitch

Timings are the target, not a script to read aloud. Say it in your own words.

## 0:00 — Open with one household, then the scale

There are children in London who have never had a bedroom that stayed theirs for a whole
school year.

As of December 2025, **100,930 children in London are living in temporary accommodation**. That
is the highest figure ever recorded, and it is higher than the number most people are quoting —
the select committee evidence everyone cites this year says 85,000. The official return says a
hundred thousand and rising. London crossed six figures and nobody announced it.

## 0:40 — The fiscal turn

This is not only a housing story, and we are not estimating this part. These are the figures
councils themselves reported to government.

In 2024-25 London boroughs spent **£740 million** net on temporary accommodation. Three years
earlier it was £243 million. It has **tripled**, and it now eats **71%** of everything London
spends on homelessness — squeezing the prevention budget that would stop the next family
arriving. Newham is the extreme: **88%** of its homelessness spending goes on temporary
accommodation, leaving barely £5 million for prevention.

That is the doom loop, and it is the chart to leave on screen.

## 1:10 — The counterpunch

Here is the part that makes it unforgivable.

Over the five years to 2023/24, London granted planning permission for **320,203 homes**. It
completed **184,169**. A **57% completion rate** — a gap of **136,034 homes**.

We are renting hotel rooms at scale, in the same boroughs that approved homes and did not build
them. Greenwich is the extreme: a **27% completion rate**, and a permission gap **nine times**
the number of households it currently has in temporary accommodation.

Put the two halves together. Since 2021-22 London has spent **£1.8 billion** of its own money on
temporary accommodation. At £300,000 a home that is roughly **6,000 homes** — and the city owns
none of it.

## 1:45 — Demo, live

*Ask the room to shout out a borough. Click it on the map.*

Every London borough. Households, children, how many are placed outside the borough entirely,
how it has moved since 2019, what it costs per day, and the homes approved but not delivered.
Postcode lookup, so anyone can find their own.

*Flip the map toggle to "homes approved but not built".*

Same city, second measure. The dark boroughs move.

*Drag the cost slider.*

And we are not asking you to take our cost estimate on trust. The nightly rate is a slider,
because the government does not publish it. Put in your own number and the page follows.

*Click the button.*

And a pre-written email to your councillor with your own borough's two numbers in it, asking the
one question a council has to answer in writing.

## 2:30 — Where we could be wrong

The honest bit. The approvals gap is **not** proof of land banking. Homes approved in 2023/24
could not have completed by 2023/24, so some of that gap is ordinary build-out time. We show the
two numbers side by side and we do not claim one causes the other. Splitting build-out lag from
genuine stalling needs site-level permission dates from the London Development Database — that is
the next build.

The spending is net, not gross, because housing benefit subsidy offsets most of the gross cost
and net is what actually lands on a council's budget. The only assumption left on the page is
what a home costs to build, and that is a slider.

## 2:50 — Close

Every number here is open data. No data use agreement, nothing embargoed, the whole pipeline is
four scripts in the repo and the site is one static page. Fork it, point it at next quarter's
release, and it updates itself.

The data to argue for fixing this already exists. We just made it typeable.

---

## Numbers to have on the tip of your tongue

| | |
|---|---|
| Children in TA, London, Dec 2025 | 100,930 |
| Households in TA, London | 75,600 |
| Growth since Dec 2019 | +28.9% |
| Worst borough | Newham — 1 in every 17 households |
| Net TA spend, London, 2024-25 | £740m |
| Same figure, 2021-22 | £243m (+204%) |
| Share of all homelessness spend | 71% (Newham 88%) |
| Cumulative since 2021-22 | £1.8bn — about 6,000 homes |
| Homes approved 2019/20–2023/24 | 320,203 |
| Homes completed | 184,169 |
| Completion rate | 57.5% |
| Biggest gap | Greenwich — 18,069 homes, 27% completion rate |

## Likely questions

**"Isn't the approvals gap just build-out time?"** Partly, and we say so on the page. But a 57%
five-year completion rate is low enough that build-out lag alone is a stretch, and the variance
between boroughs — 27% in Greenwich against boroughs delivering more than they approved — is not
explained by lag, because they all face the same construction timelines.

**"Why December snapshots?"** TA counts are seasonal. Comparing December to December keeps it
like-for-like.

**"Where does the cost figure come from?"** Not from us. It is form RO4 of MHCLG's local
authority revenue outturn — what each council reported it actually spent. We use net current
expenditure rather than gross, because housing benefit subsidy offsets most of the gross figure
and net is what genuinely lands on the borough's budget.

**"Why does the spending chart only start in 2021-22?"** Earlier releases exist, but most
boroughs leave the homelessness component lines blank before then. A longer chart would be
comparing against missing data rather than against smaller numbers.

**"Hackney is negative — is that a bug?"** No. A few boroughs completed more than they approved in
this window, working through older consents. The page says so in words rather than showing a
negative shortfall.
