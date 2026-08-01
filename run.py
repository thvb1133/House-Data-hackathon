"""Homes vs Hotels — build everything and serve the site.

Works the same on Windows, macOS and Linux:

    python run.py

Stop it with Ctrl+C.
"""

import socket
import subprocess
import sys
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
PACKAGES = ["pandas", "odfpy", "openpyxl"]
STEPS = [
    ("Downloading official data (skips anything already downloaded)", "fetch_data.py"),
    ("Reading the homelessness spreadsheets (about a minute)", "extract_ta.py"),
    ("Reading the housing delivery spreadsheet", "extract_pipeline.py"),
    ("Building the map", "build_map.py"),
    ("Building the page", "build_site.py"),
]


def run_step(script: str) -> None:
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT)
    if result.returncode != 0:
        sys.exit(
            f"\nStep failed: {script}\n"
            "If it was a download problem, just run this again — finished downloads are kept."
        )


def ensure_packages() -> None:
    try:
        import odf  # noqa: F401
        import openpyxl  # noqa: F401
        import pandas  # noqa: F401
    except ImportError:
        print("    installing pandas, odfpy, openpyxl …")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", *PACKAGES], check=True
        )


def free_port(start: int = 8099) -> int:
    for port in range(start, start + 50):
        with socket.socket() as probe:
            if probe.connect_ex(("127.0.0.1", port)) != 0:
                return port
    sys.exit("No free port found between 8099 and 8148.")


def main() -> None:
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except AttributeError:
        pass

    total = len(STEPS) + 2
    print(f"==> 1/{total}  Checking Python packages")
    ensure_packages()

    for i, (label, script) in enumerate(STEPS, start=2):
        print(f"==> {i}/{total}  {label}")
        run_step(script)

    port = free_port()
    if port != 8099:
        print(f"    Port 8099 was busy, so this copy is on {port} instead.")

    url = f"http://localhost:{port}"
    print(f"\n==> {total}/{total}  Serving the site\n")
    print(f"    {url}")
    print("    Leave this window open. Press Ctrl+C to stop.\n")

    try:
        webbrowser.open(url)
    except Exception:
        pass

    handler = partial(SimpleHTTPRequestHandler, directory=str(SITE))
    with ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
