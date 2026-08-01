# What every word in this project means

Read this once before you pitch. If someone asks "what's TA?" you must not hesitate.

---

## The two words you will say most

**TA — Temporary Accommodation.**
When a council has a legal duty to house a homeless family but has no permanent home for them,
it puts them in "temporary accommodation": a hotel, a B&B, a hostel, or a flat the council rents
from a private landlord. Families can stay for years. It is the most expensive and least secure
way to house someone. **This is the core subject of the whole project.**

**Never started.**
A council granted planning permission for homes, and construction never began. Not "slow", not
"half-built" — never begun. London has 112,104 of these.

---

## The brief codes (from the hackathon pack)

The organisers wrote a list of suggested project briefs, each with a code letter.

| Code | What it was | Did I use it? |
|---|---|---|
| **PD** | Policy brief D — *"Is temporary accommodation bankrupting London's boroughs?"* | **Yes — my main brief** |
| **DE** | Data brief E — *"Who's sitting on land that could be homes?"* (permitted but unbuilt) | **Yes — combined with PD** |
| **PG** | Policy brief G — a property tax calculator | **No — this was my backup** |

**What "backup brief" means:** the organisers told everyone to pick a main idea *and* a spare one,
in case your main idea's data turned out to be broken or missing. If the temporary accommodation
data had failed at the midday checkpoint, I would have switched to PG. It didn't fail, so I never
needed the backup.

**If asked "which brief did you do?"** say: *"PD crossed with DE. The pack says you can modify
the briefs, so I combined the demand side and the supply side into one thing."*

---

## The organisations

| Short | Full name | What they gave me |
|---|---|---|
| **MHCLG** | Ministry of Housing, Communities and Local Government | The homelessness figures and the council spending figures |
| **GLA** | Greater London Authority (the Mayor of London's body) | The homes approved, started and completed |
| **ONS** | Office for National Statistics | The borough map boundaries |

---

## The datasets, in plain words

**Table TA1** — MHCLG's official homelessness return. Every council in England must file it every
three months. It says how many households and children are in temporary accommodation. This is
where 100,930 children comes from. *Nothing here is estimated by me.*

**AMR 21** — the GLA's *Annual Monitoring Report*, number 21, published January 2026. It reports,
for each borough, how many homes were **approved**, how many were **started**, and how many were
**completed**. The gap between approved and started is my 112,104.

**RO4** — a form councils fill in every year saying what they actually spent, broken down by
category. RO4 is the housing one. This is where £740 million comes from. *Again, their number,
not mine.*

**RS** — the matching form for reserves: how much money a council has saved up. Used for the
"287% of spendable reserves" figure for Hillingdon.

---

## The money words

**Net current expenditure.**
Spending **minus** income. Councils get housing benefit subsidy and rent back, which cancels out a
lot of the raw cost. **Net** is what the council genuinely pays from its own budget. I use net
everywhere, because that is the number that actually squeezes a council.

> If asked why: *"Gross is a bigger, scarier number, but net is the honest one — it's what lands
> on the borough's budget."*

**Why some boroughs show a minus number.**
On council-owned or leased stock, the subsidy and rent recovered can be more than the spend, so
net goes negative. Tower Hamlets does this. It is real, not an error. Where it happens, the page
hides the percentage instead of printing nonsense.

**Spendable reserves.**
A council's savings that it is actually allowed to spend on anything. It excludes money ring-fenced
for schools and public health. My definition, not an official one — and I say so on the page.

> If asked "is Hillingdon bankrupt at 287%?": *"No. It pays from revenue, not reserves. It just
> shows how big the bill has got next to the money it could reach for in an emergency."*

**Prevention (and relief).**
Money spent stopping someone becoming homeless in the first place — advice, help with rent
arrears, mediation. Cheaper than temporary accommodation. It is the green line on my chart, and
it is barely moving while the red line triples. That is the trap.

---

## The statistics words

**Correlation.**
Do two things move together? I asked: do the boroughs with the worst temporary accommodation also
have the most unbuilt homes? Answer: no.

**Spearman rank correlation (ρ = −0.21).**
A correlation measured on rankings rather than raw numbers, so one extreme borough can't distort
it. It runs from −1 to +1. **0 means no relationship.** −0.21 is close to zero.

**p-value (p = 0.25).**
The chance of seeing a pattern this strong purely by luck. Below 0.05 means "probably real".
Mine is 0.25 — five times higher — so **this is indistinguishable from coincidence.**

**Permutation test.**
How I got the p-value: shuffle the data thousands of times at random and see how often chance
produces a pattern as strong as the real one. It assumes nothing about the shape of the data,
which matters when you only have 31 boroughs.

**Null result.**
A test that finds nothing. Mine found no link between need and failure to build.

> If someone says "a null result isn't a finding": *"It is, when the whole room assumes the
> opposite. And it changes what you'd do about it."*

---

## The technical words

**Static site.** A web page that is just a file. No server, no database. It cannot break in a demo.

**Standalone / offline build.** `dist/homes-vs-hotels.html` — the entire tool squeezed into one
file, data and map included. Double-click it and it works with no internet.

**Pipeline.** The five scripts that download the government spreadsheets, read them, and rebuild
the page. One command: `python run.py`.

**Reproducible.** Anyone can run my command and get exactly my numbers. Nothing is hand-typed.

---

## The 30-second version, if someone asks at the bar

> "I looked at temporary accommodation — families councils put in hotels because they have
> nowhere else. London has a hundred thousand children in it, and boroughs now spend seven
> hundred and forty million a year on it. Then I looked at homes that got planning permission
> and were never built — a hundred and twelve thousand of them. I assumed the worst-hit boroughs
> would be the ones not building. They're not. There's no link at all. So the homes aren't
> going where the need is — and I can name six boroughs where they should."
