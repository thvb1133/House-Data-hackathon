"""Extract borough-level temporary accommodation metrics from MHCLG statutory
homelessness detailed local-authority tables.

The published spreadsheets use multi-row merged headers whose exact row/column
positions drift between quarters, so columns are located by matching the
concatenated header text rather than by fixed index.
"""

import re
from pathlib import Path

import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")

QUARTERS = {
    "2019-12": "TA_201912.ods",
    "2020-12": "TA_202012.ods",
    "2021-12": "TA_202112.ods",
    "2022-12": "TA_202212.ods",
    "2023-12": "TA_202312.ods",
    "2024-12": "TA_202412.ods",
    "2025-12": "TA_202512.ods",
}

# label -> (list of phrases that must all appear, list of phrases that must not)
TA1_COLUMNS = {
    "ta_households": (["total number of households in ta"], ["with children", "per ("]),
    "households_in_area_000s": (["number of households in area"], []),
    "ta_households_with_children": (["total number of households in ta with children"], []),
    "ta_children": (["total number of children in ta"], []),
    "bb_households": (["bed and breakfast", "total number of households"], ["children"]),
    "bb_with_children": (["bed and breakfast", "total with children"], ["6 weeks", "16/17"]),
    "bb_children_over_6_weeks": (["total with children and resident more than 6 weeks"], ["pending"]),
    "nightly_paid_households": (["nightly paid", "total number of households"], ["children"]),
    "la_ha_stock_households": (["(la/ha) stock", "total number of households"], ["children"]),
    "hostel_households": (["hostels (including", "total number of households"], ["children"]),
    "leased_households": (["private sector accommodation leased", "total number of households"], ["children"]),
    "other_ta_households": (["any other type of temporary accommodation", "total number of households"], ["children"]),
    "in_ta_another_district": (["in ta in another local authority district"], []),
}


def _norm(v) -> str:
    s = str(v)
    return "" if s == "nan" else s.strip().lower()


def _find_data_start(df: pd.DataFrame) -> int:
    codes = df[0].astype(str)
    hits = df.index[codes == "E92000001"]
    if len(hits) == 0:
        raise ValueError("could not locate ENGLAND row")
    return int(hits[0])


def _column_map(df: pd.DataFrame, start: int, spec: dict) -> dict:
    """Build {label: column index} by matching stacked header text."""
    header_text = {}
    for col in range(df.shape[1]):
        parts = [_norm(df.iloc[r, col]) for r in range(start)]
        header_text[col] = " :: ".join(p for p in parts if p)

    mapping = {}
    for label, (required, forbidden) in spec.items():
        matches = [
            col
            for col, text in header_text.items()
            if all(r in text for r in required) and not any(f in text for f in forbidden)
        ]
        if matches:
            mapping[label] = matches[0]
    return mapping


def _to_number(v):
    """Published tables use '-', '[z]', '..' etc. for suppressed/na values."""
    s = str(v).strip()
    if s in {"", "nan", "-", "..", ":", "[z]", "[c]", "[x]", "[w]", "[low]"}:
        return pd.NA
    s = s.replace(",", "").replace("%", "")
    try:
        return float(s)
    except ValueError:
        return pd.NA


def _clean_area(name: str) -> str:
    name = re.sub(r"\s+", " ", str(name)).strip()
    return name.replace(" & ", " and ")


def extract_ta1(path: Path, quarter: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="TA1", engine="odf", header=None)
    start = _find_data_start(df)
    cols = _column_map(df, start, TA1_COLUMNS)

    missing = set(TA1_COLUMNS) - set(cols)
    if "ta_households" in missing:
        raise ValueError(f"{path.name}: could not find TA household column")

    body = df.iloc[start:].copy()
    keep = body[body[0].astype(str).str.match(r"^(E09|E12000007|E92000001)")]

    out = pd.DataFrame(
        {
            "quarter": quarter,
            "area_code": keep[0].astype(str).str.strip(),
            "area_name": keep[1].map(_clean_area),
        }
    )
    for label, col in cols.items():
        out[label] = keep[col].map(_to_number)
    for label in missing:
        out[label] = pd.NA
    return out.reset_index(drop=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    frames = []
    for quarter, filename in QUARTERS.items():
        path = RAW / filename
        if not path.exists():
            print(f"skip {quarter}: {filename} not downloaded")
            continue
        frame = extract_ta1(path, quarter)
        boroughs = frame["area_code"].str.startswith("E09").sum()
        print(f"{quarter}: {len(frame)} rows ({boroughs} boroughs)")
        frames.append(frame)

    panel = pd.concat(frames, ignore_index=True)
    panel = panel.sort_values(["area_name", "quarter"]).reset_index(drop=True)
    panel.to_csv(OUT / "ta_panel_london.csv", index=False)
    print(f"\nwrote {OUT/'ta_panel_london.csv'}  {panel.shape}")

    latest = panel[panel["quarter"] == max(QUARTERS)]
    ldn = latest[latest["area_code"] == "E12000007"].iloc[0]
    print(
        f"\nLondon {max(QUARTERS)}: {ldn.ta_households:,.0f} households, "
        f"{ldn.ta_children:,.0f} children, "
        f"{ldn.ta_households/ldn.households_in_area_000s:.1f} per 1,000 households"
    )


if __name__ == "__main__":
    main()
