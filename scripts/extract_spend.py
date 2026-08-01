"""Extract borough homelessness spending from MHCLG revenue outturn RO4 tables.

This replaces the guessed cost-per-night with what councils actually reported, and
separates the two halves of the argument: money spent housing people in temporary
accommodation, against money spent preventing them from needing it.

Net current expenditure is used throughout — gross spend on temporary accommodation
is largely offset by housing benefit subsidy, so net is what a council genuinely
carries on its own budget.
"""

import re
from pathlib import Path

import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed/spend_london.csv")

# Earlier releases exist, but the homelessness breakdown only becomes consistently
# reported from 2021-22 — before that most boroughs leave the component lines blank.
YEARS = ["2021-22", "2022-23", "2023-24", "2024-25"]

# Category name -> output column. Matched on the part of the header before " - ".
CATEGORIES = {
    "nightly paid, privately managed accommodation": "nightly_paid",
    "bed and breakfast hotels": "bed_and_breakfast",
    "hostels (including reception centres": "hostels",
    "private sector accommodation leased": "leased",
    "local authority or housing association stock": "la_ha_stock",
    "any other type of temporary accommodation": "other_ta",
    "temporary accommodation administration": "ta_admin",
    "homeless reduction act: administration, prevention": "prevention",
    "total homelessness": "total_homelessness",
}

TA_COLUMNS = ["nightly_paid", "bed_and_breakfast", "hostels", "leased", "la_ha_stock", "other_ta"]


def _to_number(v):
    s = str(v).replace(",", "").strip()
    if s in {"", "nan", "-", "..", ":", "[c]", "[z]", "[x]"}:
        return pd.NA
    try:
        return float(s)
    except ValueError:
        return pd.NA


def _header_row(df: pd.DataFrame) -> int:
    for i in range(min(20, len(df))):
        if str(df.iloc[i, 0]).strip().lower() in {"e-code", "ecode"}:
            return i
    raise ValueError("header row not found")


def extract(year: str) -> pd.DataFrame:
    path = RAW / f"RO4_{year}.ods"
    book = pd.ExcelFile(path, engine="odf")
    sheet = next(s for s in book.sheet_names if s.upper().startswith("RO4"))
    df = book.parse(sheet, header=None)

    head = _header_row(df)
    headers = df.iloc[head].astype(str)

    # Locate the ONS code column by content, since its position shifts between years.
    code_col = next(
        c for c in df.columns if str(headers[c]).strip().lower() in {"ons code", "ons_code"}
    )

    # Recent releases put "Category - Sub-column" in one header cell; older ones put
    # the category in a merged row above, so forward-fill those rows across columns.
    banner = df.iloc[:head].ffill(axis=1) if head else pd.DataFrame()

    def full_header(col) -> str:
        parts = []
        for r in range(len(banner)):
            value = str(banner.iloc[r, col]).strip()
            if len(value) > 8 and not re.fullmatch(r"[\d.,\-]+", value) and value != "nan":
                parts.append(value)
        parts.append(str(headers[col]).strip())
        return " - ".join(parts).lower()

    wanted = {}
    for col in df.columns:
        text = full_header(col)
        if "net current expenditure" not in text:
            continue
        for needle, label in CATEGORIES.items():
            if needle in text and label not in wanted:
                wanted[label] = col
                break

    body = df.iloc[head + 1 :]
    london = body[body[code_col].astype(str).str.match(r"^E09\d{6}$", na=False)]

    out = pd.DataFrame(
        {
            "year": year,
            "area_code": london[code_col].astype(str).str.strip(),
            "borough": london.iloc[:, 2].astype(str).str.strip().str.replace(" & ", " and "),
        }
    )
    for label, col in wanted.items():
        out[label] = london[col].map(_to_number)
    for label in set(CATEGORIES.values()) - set(wanted):
        out[label] = pd.NA

    # RO4 is published in £ thousands.
    money = [c for c in out.columns if c not in {"year", "area_code", "borough"}]
    out[money] = out[money].astype("Float64") * 1000
    out["ta_total"] = out[TA_COLUMNS].sum(axis=1, min_count=1)
    return out.reset_index(drop=True)


def main() -> None:
    frames = []
    for year in YEARS:
        if not (RAW / f"RO4_{year}.ods").exists():
            print(f"skip {year}: file not downloaded")
            continue
        frame = extract(year)
        print(f"{year}: {len(frame)} boroughs, TA spend £{frame.ta_total.sum()/1e6:,.0f}m, "
              f"prevention £{frame.prevention.sum()/1e6:,.0f}m")
        frames.append(frame)

    panel = pd.concat(frames, ignore_index=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(OUT, index=False)
    print(f"\nwrote {OUT}  {panel.shape}")

    totals = panel.groupby("year")[["ta_total", "prevention"]].sum()
    first, last = totals.index[0], totals.index[-1]
    print(
        f"\nLondon net TA spend {first} -> {last}: "
        f"£{totals.ta_total[first]/1e6:,.0f}m -> £{totals.ta_total[last]/1e6:,.0f}m "
        f"({totals.ta_total[last]/totals.ta_total[first]-1:+.0%})"
    )
    print(
        f"London net prevention spend {first} -> {last}: "
        f"£{totals.prevention[first]/1e6:,.0f}m -> £{totals.prevention[last]/1e6:,.0f}m "
        f"({totals.prevention[last]/totals.prevention[first]-1:+.0%})"
    )


if __name__ == "__main__":
    main()
