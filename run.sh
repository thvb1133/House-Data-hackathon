#!/usr/bin/env bash
# Homes vs Hotels — build everything from scratch and open the site.
# Usage:  ./run.sh
set -euo pipefail
cd "$(dirname "$0")"

PORT="${PORT:-8099}"

echo "==> 1/5  Installing Python packages"
python3 -m pip install --quiet --upgrade pandas odfpy openpyxl

echo "==> 2/5  Downloading official data (skips anything already downloaded)"
python3 scripts/fetch_data.py

echo "==> 3/5  Reading the government spreadsheets (this takes about a minute)"
python3 scripts/extract_ta.py
python3 scripts/extract_pipeline.py

echo "==> 4/5  Building the site"
python3 scripts/build_map.py
python3 scripts/build_site.py

echo "==> 5/5  Starting the site"
echo
echo "    Open this in your browser:  http://localhost:${PORT}"
echo "    Press Ctrl+C here to stop."
echo
python3 -m http.server "$PORT" --directory site
