"""Download every raw file the pipeline needs into data/raw/.

Safe to re-run: files already present are skipped, so an interrupted download
session can be resumed without re-fetching gigabytes.
"""

import sys
import time
import urllib.request
from pathlib import Path

RAW = Path("data/raw")

GOV = "https://assets.publishing.service.gov.uk/media"

FILES = {
    # MHCLG statutory homelessness, detailed local authority tables (table TA1),
    # December quarter each year.
    "TA_201912.ods": f"{GOV}/5f749aaad3bf7f2868b3ffa2/DetailedLA_201912_revised.ods",
    "TA_202012.ods": f"{GOV}/60fae728d3bf7f04599e2170/DetailedLA_202012_Revised_updated.ods",
    "TA_202112.ods": f"{GOV}/62e14c208fa8f564a21dcd8a/Detailed_LA_202112_revised.ods",
    "TA_202212.ods": f"{GOV}/64be88f41e10bf000e17cd3a/Detailed_LA_202212_revised.ods",
    "TA_202312.ods": f"{GOV}/66b331c5a3c2a28abb50ddfd/Detailed_LA_202312_Revised_No_Dropdowns.ods",
    "TA_202412.ods": f"{GOV}/699d956edb2401de164d6c1c/Statutory_Homelessness_Detailed_Local_Authority_Data_202412_revised.ods",
    "TA_202512.ods": f"{GOV}/69f08a8108ecdb5c6f34b065/Statutory_Homelessness_Detailed_Local_Authority_Data_202512.ods",
    # GLA London Plan Annual Monitoring Report 21 (January 2026), chapter 2.
    "AMR21_Housing.xlsx": "https://data.london.gov.uk/download/2rjko/0yx/AMR%2021%20Chapter%202%20Housing%20Tables.xlsx",
    # Borough boundaries, generalised, WGS84.
    # MHCLG local authority revenue outturn, RO4 (housing services) — carries the
    # actual homelessness and temporary accommodation spend each council reported.
    "RO4_2018-19.ods": f"{GOV}/66573b9e0c8f88e868d33335/RO4_2018-19_data_by_LA.ods",
    "RO4_2019-20.ods": f"{GOV}/6656f573dc15efdddf1a84bd/RO4_2019-20_data_by_LA.ods",
    "RO4_2020-21.ods": f"{GOV}/67dc26a2cb8c6838d74b4fd5/RO4_2020-21_data_by_LA_March_2025.ods",
    "RO4_2021-22.ods": f"{GOV}/6825a5e47293a87b6c75ec90/RO4_2021-22_data_by_LA_Live.ods",
    "RO4_2022-23.ods": f"{GOV}/686be46a81dd8f70f5de3c19/RO4_2022-23_data_by_LA.ods",
    "RO4_2023-24.ods": f"{GOV}/6a29120f3b15d05a7ce31ff7/RO4_2023-24_data_by_LA.ods",
    "RO4_2024-25.ods": f"{GOV}/6a291b65e371d9d2c0052b83/RO4_LA_Data_2024-25_data_by_LA.ods",
    # Borough boundaries — ONS Open Geography, super-generalised and clipped,
    # carrying the same E09 codes the statistical tables use.
    "london_boroughs.geojson": (
        "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"
        "Local_Authority_Districts_DEC_2025_Boundaries_UK_BSC/FeatureServer/0/query"
        "?where=LAD25CD+LIKE+%27E09%25%27&outFields=LAD25CD,LAD25NM&outSR=4326&f=geojson"
    ),
}

RETRIES = 4


def fetch(name: str, url: str) -> bool:
    target = RAW / name
    if target.exists() and target.stat().st_size > 0:
        print(f"  have  {name}")
        return True

    for attempt in range(1, RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "house-london-hackathon"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            target.write_bytes(data)
            print(f"  got   {name}  ({len(data)/1e6:.1f} MB)")
            return True
        except Exception as exc:
            wait = 2**attempt
            if attempt == RETRIES:
                print(f"  FAILED {name}: {exc}")
                return False
            print(f"  retry {name} in {wait}s ({exc})")
            time.sleep(wait)
    return False


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {len(FILES)} files into {RAW}/")
    failed = [name for name, url in FILES.items() if not fetch(name, url)]
    if failed:
        print(f"\n{len(failed)} file(s) failed: {', '.join(failed)}")
        sys.exit(1)
    print("\nAll raw data present.")


if __name__ == "__main__":
    main()
