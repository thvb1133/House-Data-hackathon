"""Join the TA panel and the delivery pipeline into the JSON payload the page reads."""

import json
from pathlib import Path

import pandas as pd

PANEL = Path("data/processed/ta_panel_london.csv")
PIPELINE = Path("data/processed/pipeline_london.csv")
SPEND = Path("data/processed/spend_london.csv")
RESERVES = Path("data/processed/reserves_london.csv")
OUT = Path("site/data.json")

# The AMR names two boroughs in short form and adds two development corporations,
# whose consents sit inside host-borough boundaries and are left unmatched.
PIPELINE_ALIASES = {"Kingston": "Kingston upon Thames", "Richmond": "Richmond upon Thames"}

# MHCLG does not publish TA spend, so the per-night cost is applied as an
# explicit, user-visible assumption rather than presented as measured data.
NIGHTLY_COST_ASSUMPTION = 60.0

# Likewise the build cost. Both are exposed as sliders on the page so the
# comparison can be re-run against the reader's own numbers.
BUILD_COST_ASSUMPTION = 300_000.0


def _num(v):
    return None if pd.isna(v) else float(v)


def _spearman(x, y, trials=20000, seed=0):
    """Rank correlation with a permutation p-value.

    A permutation test avoids a scipy dependency and makes no distributional
    assumption, which matters at n=31 boroughs.
    """
    import numpy as np

    a, b = pd.Series(x).rank().to_numpy(), pd.Series(y).rank().to_numpy()
    a, b = a - a.mean(), b - b.mean()
    observed = float((a * b).sum() / (np.sqrt((a**2).sum()) * np.sqrt((b**2).sum())))

    rng = np.random.default_rng(seed)
    shuffled = np.array([b[rng.permutation(len(b))] for _ in range(trials)])
    null = (shuffled * a).sum(axis=1) / (
        np.sqrt((a**2).sum()) * np.sqrt((shuffled**2).sum(axis=1))
    )
    p = float((np.abs(null) >= abs(observed)).mean())
    return round(observed, 2), round(p, 3)




def main() -> None:
    panel = pd.read_csv(PANEL).drop_duplicates(subset=["quarter", "area_code"])
    quarters = sorted(panel["quarter"].unique())
    latest = quarters[-1]

    spend = pd.read_csv(SPEND)
    spend_years = sorted(spend["year"].unique())
    latest_spend_year = spend_years[-1]
    by_area = {code: g.sort_values("year") for code, g in spend.groupby("area_code")}
    london_spend = spend.groupby("year")[["ta_total", "prevention", "total_homelessness"]].sum()

    reserves = pd.read_csv(RESERVES).set_index("area_code")["spendable_reserves"]
    london_reserves = float(reserves.sum())

    def spend_block(code):
        if code == "E12000007":
            rows = [
                {"year": y, "ta": float(london_spend.ta_total[y]),
                 "prevention": float(london_spend.prevention[y]),
                 "total": float(london_spend.total_homelessness[y])}
                for y in spend_years
            ]
        elif code in by_area:
            g = by_area[code]
            rows = [
                {"year": r.year, "ta": _num(r.ta_total),
                 "prevention": _num(r.prevention), "total": _num(r.total_homelessness)}
                for r in g.itertuples()
            ]
        else:
            return None
        latest = rows[-1]
        first = rows[0]
        pot = london_reserves if code == "E12000007" else reserves.get(code)
        return {
            "reserves": _num(pot) if pot is not None else None,
            "ta_vs_reserves_pct": (
                round(latest["ta"] / pot * 100) if pot and latest["ta"] else None
            ),
            "series": rows,
            "ta": latest["ta"],
            "prevention": latest["prevention"],
            "total": latest["total"],
            "ta_share_pct": round(latest["ta"] / latest["total"] * 100, 1) if latest["total"] else None,
            "ta_change_pct": (
                round((latest["ta"] / first["ta"] - 1) * 100) if first["ta"] else None
            ),
        }

    pipe = pd.read_csv(PIPELINE)
    pipe["borough"] = pipe["borough"].replace(PIPELINE_ALIASES)
    pipeline = pipe.set_index("borough").to_dict("index")
    london_pipeline = {
        "approvals": float(pipe["approvals"].sum()),
        "completions": float(pipe["completions"].sum()),
        "approved_not_completed": float(pipe["approved_not_completed"].sum()),
        "approved_not_started": float(pipe["approved_not_started"].sum()),
        "starts": float(pipe["starts"].sum()),
    }
    london_pipeline["completion_rate_pct"] = round(
        london_pipeline["completions"] / london_pipeline["approvals"] * 100, 1
    )

    areas = []
    for code, group in panel.groupby("area_code"):
        group = group.sort_values("quarter")
        current = group[group["quarter"] == latest]
        if current.empty:
            continue
        current = current.iloc[0]

        series = [
            {"quarter": r.quarter, "households": _num(r.ta_households), "children": _num(r.ta_children)}
            for r in group.itertuples()
        ]
        observed = [p for p in series if p["households"] is not None]
        first = observed[0] if observed else None

        households = _num(current.ta_households)
        stock = _num(current.households_in_area_000s)
        pl = london_pipeline if code == "E12000007" else pipeline.get(current.area_name)

        areas.append(
            {
                "code": code,
                "name": current.area_name,
                "is_borough": code.startswith("E09"),
                "households": households,
                "children": _num(current.ta_children),
                "households_with_children": _num(current.ta_households_with_children),
                "per_1000_households": round(households / stock, 1) if households and stock else None,
                "one_in": round(stock * 1000 / households) if households and stock else None,
                "bb_households": _num(current.bb_households),
                "nightly_paid_households": _num(current.nightly_paid_households),
                "placed_out_of_borough": _num(current.in_ta_another_district),
                "baseline_quarter": first["quarter"] if first else None,
                "baseline_households": first["households"] if first else None,
                "change_pct": (
                    round((households / first["households"] - 1) * 100, 1)
                    if first and first["households"] and households
                    else None
                ),
                "series": series,
                "spend": spend_block(code),
                "approvals": _num(pl["approvals"]) if pl else None,
                "completions": _num(pl["completions"]) if pl else None,
                "approved_not_completed": _num(pl["approved_not_completed"]) if pl else None,
                "approved_not_started": _num(pl["approved_not_started"]) if pl else None,
                "starts": _num(pl["starts"]) if pl else None,
                "completion_rate_pct": _num(pl["completion_rate_pct"]) if pl else None,
            }
        )

    # Set demand pressure against supply failure on a common per-1,000-households
    # basis, so the two halves of the argument can be tested against each other.
    for a in areas:
        stock = (
            a["households"] / a["per_1000_households"] * 1000
            if a["households"] and a["per_1000_households"]
            else None
        )
        # Boroughs that started more than they approved keep their negative value:
        # they sit at the delivering end of the scale, and dropping them would bias
        # the test toward the boroughs with the worst backlogs.
        a["unstarted_per_1000"] = (
            round(a["approved_not_started"] / stock * 1000, 1)
            if stock and a.get("approved_not_started") is not None
            else None
        )

    tested = [
        a for a in areas
        if a["is_borough"] and a["unstarted_per_1000"] is not None and a["per_1000_households"]
    ]
    rho, p = _spearman(
        [a["per_1000_households"] for a in tested],
        [a["unstarted_per_1000"] for a in tested],
    )
    mismatch = {
        "n": len(tested),
        "rho": rho,
        "p": p,
        "median_ta": round(pd.Series([a["per_1000_households"] for a in tested]).median(), 1),
        "median_unstarted": round(pd.Series([a["unstarted_per_1000"] for a in tested]).median(), 1),
    }

    # Boroughs above the median on both measures: the need is already acute and the
    # permissions already exist, so delivery there relieves the most pressure soonest.
    priority = sorted(
        (
            a for a in tested
            if a["per_1000_households"] > mismatch["median_ta"]
            and a["unstarted_per_1000"] > mismatch["median_unstarted"]
        ),
        key=lambda a: -a["approved_not_started"],
    )
    mismatch["priority"] = [
        {
            "name": a["name"],
            "code": a["code"],
            "households": a["households"],
            "children": a["children"],
            "unstarted": a["approved_not_started"],
        }
        for a in priority
    ]
    # The sharpest illustration of the null result: worst need yet delivering, against
    # least need yet sitting on the most unstarted consent.
    delivering = min(tested, key=lambda a: (a["unstarted_per_1000"], -a["per_1000_households"]))
    idle = max(tested, key=lambda a: (a["unstarted_per_1000"], -a["per_1000_households"]))
    mismatch["contrast"] = {
        "delivering": {
            "name": delivering["name"],
            "ta_rate": delivering["per_1000_households"],
            "unstarted_per_1000": delivering["unstarted_per_1000"],
            "households": delivering["households"],
        },
        "idle": {
            "name": idle["name"],
            "ta_rate": idle["per_1000_households"],
            "unstarted_per_1000": idle["unstarted_per_1000"],
            "unstarted": idle["approved_not_started"],
        },
    }
    mismatch["priority_totals"] = {
        "unstarted": sum(a["approved_not_started"] for a in priority),
        "households": sum(a["households"] for a in priority),
        "children": sum(a["children"] for a in priority),
    }

    areas.sort(key=lambda a: (not a["is_borough"], a["name"]))
    payload = {
        "latest_quarter": latest,
        "quarters": quarters,
        "nightly_cost_assumption": NIGHTLY_COST_ASSUMPTION,
        "build_cost_assumption": BUILD_COST_ASSUMPTION,
        "pipeline_years": "2019/20 to 2023/24",
        "mismatch": mismatch,
        "spend_years": spend_years,
        "latest_spend_year": latest_spend_year,
        "sources": [
            "MHCLG statutory homelessness detailed local authority tables, table TA1",
            "GLA London Plan Annual Monitoring Report 21 (January 2026), chapter 2 housing tables",
            "MHCLG local authority revenue outturn RO4 (housing services), net current expenditure",
        ],
        "areas": areas,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=1))
    london = next(a for a in areas if a["code"] == "E12000007")
    print(f"wrote {OUT} — {len(areas)} areas, latest {latest}")
    print(f"London: {london['households']:,.0f} households, {london['children']:,.0f} children")


if __name__ == "__main__":
    main()
