"""Extract borough-level housing approvals, starts and completions from the
London Plan Annual Monitoring Report 21 (GLA, January 2026).

Each sheet holds a stack of tables; the by-planning-authority table is located by
its caption rather than a fixed row, since positions move between AMR editions.
"""

import re
from pathlib import Path

import pandas as pd

RAW = Path("data/raw/AMR21_Housing.xlsx")
OUT = Path("data/processed/pipeline_london.csv")

SHEETS = {
    "approvals": "housing approvals by planning authority",
    "starts": "housing starts by borough",
    "completions": "housing completions by planning authority",
}

NON_BOROUGH = {"total", "london", "location", "planning authority", "nan"}


def _find_table(df: pd.DataFrame, caption: str) -> int:
    for i, v in df[0].items():
        if caption in str(v).lower():
            return int(i)
    raise ValueError(f"caption not found: {caption}")


def _to_number(v):
    s = str(v).replace(",", "").strip()
    if s in {"", "nan", "-", ".."}:
        return pd.NA
    try:
        return float(s)
    except ValueError:
        return pd.NA


def extract(sheet: str, caption: str) -> pd.DataFrame:
    df = pd.read_excel(RAW, sheet_name=sheet.capitalize(), header=None)
    start = _find_table(df, caption)
    header = df.iloc[start + 1]
    years = {int(c): str(header[c]).strip() for c in df.columns[1:] if re.match(r"^\d{4}/\d{2}$", str(header[c]).strip())}

    rows = []
    for i in range(start + 2, len(df)):
        name = str(df.iloc[i, 0]).strip()
        if name.lower() in NON_BOROUGH or name.lower().startswith("table"):
            if name.lower() in {"nan", "total"} or name.lower().startswith("table"):
                break
            continue
        values = {years[c]: _to_number(df.iloc[i, c]) for c in years}
        if all(pd.isna(v) for v in values.values()):
            continue
        rows.append({"borough": name.replace(" & ", " and "), **values})

    out = pd.DataFrame(rows)
    out["metric"] = sheet
    return out


def main() -> None:
    frames = [extract(sheet, caption) for sheet, caption in SHEETS.items()]
    panel = pd.concat(frames, ignore_index=True)
    year_cols = [c for c in panel.columns if re.match(r"^\d{4}/\d{2}$", c)]
    panel["five_year_total"] = panel[year_cols].sum(axis=1, min_count=1)

    wide = panel.pivot_table(index="borough", columns="metric", values="five_year_total")
    wide["approved_not_completed"] = wide["approvals"] - wide["completions"]
    wide["approved_not_started"] = wide["approvals"] - wide["starts"]
    wide["completion_rate_pct"] = (wide["completions"] / wide["approvals"] * 100).round(1)
    wide = wide.sort_values("approved_not_completed", ascending=False)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    wide.reset_index().to_csv(OUT, index=False)

    print(f"wrote {OUT}  {wide.shape}  years: {', '.join(year_cols)}")
    print(wide.head(12).to_string(float_format=lambda v: f"{v:,.0f}"))
    total = wide.sum(numeric_only=True)
    print(
        f"\nLondon 5yr: {total.approvals:,.0f} approved, {total.completions:,.0f} completed "
        f"— gap {total.approvals - total.completions:,.0f} homes "
        f"({total.completions / total.approvals * 100:.0f}% completion rate)"
    )


if __name__ == "__main__":
    main()
