#!/usr/bin/env bash
# Homes vs Hotels — build everything from scratch and open the site.
# Usage:  ./run.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "==> 1/5  Checking Python packages"
if ! python3 -c "import pandas, odf, openpyxl" 2>/dev/null; then
  python3 -m pip install --quiet pandas odfpy openpyxl
fi

echo "==> 2/5  Downloading official data (skips anything already downloaded)"
python3 scripts/fetch_data.py

echo "==> 3/5  Reading the government spreadsheets (this takes about a minute)"
python3 scripts/extract_ta.py
python3 scripts/extract_pipeline.py

echo "==> 4/5  Building the site"
python3 scripts/build_map.py
python3 scripts/build_site.py

echo "==> 5/5  Starting the site"

# If a previous run is still serving, step along to the next free port rather
# than dying with "Address already in use".
START_PORT="${PORT:-8099}"
PORT="$(START_PORT="$START_PORT" python3 - <<'PY'
import os, socket, sys

start = int(os.environ["START_PORT"])
for port in range(start, start + 50):
    with socket.socket() as probe:
        if probe.connect_ex(("127.0.0.1", port)) != 0:
            print(port)
            sys.exit(0)
sys.exit("no free port found")
PY
)"

if [ "$PORT" != "$START_PORT" ]; then
  echo "    Port ${START_PORT} was busy (the site is probably already open there)."
  echo "    Using port ${PORT} instead."
fi

echo
echo "    Open this in your browser:  http://localhost:${PORT}"
echo "    Press Ctrl+C here to stop."
echo
python3 -m http.server "$PORT" --directory site
