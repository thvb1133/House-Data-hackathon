"""Bundle the site into one self-contained HTML file.

The result opens by double-clicking, with no web server, no Python and no internet
connection — which is what you want on a strange laptop five minutes before a demo.
"""

import json
from pathlib import Path

SITE = Path("site")
OUT = Path("dist/homes-vs-hotels.html")
PAYLOADS = ["data.json", "boroughs.json"]


def main() -> None:
    html = (SITE / "index.html").read_text()
    embedded = {name: json.loads((SITE / name).read_text()) for name in PAYLOADS}

    inline = (
        "<script>window.__EMBEDDED__ = "
        + json.dumps(embedded, separators=(",", ":"))
        + ";</script>\n<script>"
    )
    if "<script>" not in html:
        raise ValueError("no script tag to anchor the payload to")
    html = html.replace("<script>", inline, 1)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html)
    print(f"wrote {OUT} — {OUT.stat().st_size / 1024:.0f} KB, opens with no server")


if __name__ == "__main__":
    main()
