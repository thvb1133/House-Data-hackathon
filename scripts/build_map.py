"""Turn borough boundaries into ready-to-draw SVG paths.

Projecting and simplifying here rather than in the browser keeps the page free of
mapping libraries and cuts the payload from ~1.3 MB of raw coordinates to a few
tens of kilobytes.
"""

import json
import math
from pathlib import Path

SRC = Path("data/raw/london_boroughs.geojson")
OUT = Path("site/boroughs.json")

WIDTH, HEIGHT = 720.0, 480.0
PADDING = 8.0
TOLERANCE = 0.35  # in output pixels; below this, detail is invisible anyway


def _perp_distance(p, a, b):
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def simplify(points, tol):
    """Ramer-Douglas-Peucker, iterative to avoid recursion limits on big rings."""
    if len(points) < 3:
        return points
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        lo, hi = stack.pop()
        worst, index = tol, -1
        for i in range(lo + 1, hi):
            d = _perp_distance(points[i], points[lo], points[hi])
            if d > worst:
                worst, index = d, i
        if index != -1:
            keep[index] = True
            stack.append((lo, index))
            stack.append((index, hi))
    return [p for p, k in zip(points, keep) if k]


def rings(geometry):
    if geometry["type"] == "Polygon":
        return geometry["coordinates"]
    if geometry["type"] == "MultiPolygon":
        return [ring for poly in geometry["coordinates"] for ring in poly]
    raise ValueError(geometry["type"])


def main() -> None:
    geo = json.loads(SRC.read_text())
    features = geo["features"]

    lons = [c[0] for f in features for r in rings(f["geometry"]) for c in r]
    lats = [c[1] for f in features for r in rings(f["geometry"]) for c in r]
    lat0 = math.radians(sum(lats) / len(lats))
    kx = math.cos(lat0)

    xs = [lon * kx for lon in lons]
    minx, maxx, miny, maxy = min(xs), max(xs), min(lats), max(lats)
    scale = min((WIDTH - 2 * PADDING) / (maxx - minx), (HEIGHT - 2 * PADDING) / (maxy - miny))
    offx = (WIDTH - (maxx - minx) * scale) / 2
    offy = (HEIGHT - (maxy - miny) * scale) / 2

    def project(lon, lat):
        return (
            round((lon * kx - minx) * scale + offx, 1),
            round((maxy - lat) * scale + offy, 1),
        )

    paths, kept, total = {}, 0, 0
    for feature in features:
        props = feature["properties"]
        # ONS Open Geography names the columns per release year; earlier extracts
        # of the same boundaries just use "name".
        name = next(
            props[k] for k in props if k.lower().endswith(("nm", "name")) or k == "name"
        )
        code = next((props[k] for k in props if k.lower().endswith("cd")), None)
        d = []
        for ring in rings(feature["geometry"]):
            pts = [project(c[0], c[1]) for c in ring]
            total += len(pts)
            pts = simplify(pts, TOLERANCE)
            kept += len(pts)
            if len(pts) < 3:
                continue
            d.append("M" + "L".join(f"{x},{y}" for x, y in pts) + "Z")
        path = "".join(d)
        paths[name] = path
        if code:
            paths[code] = path

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"width": WIDTH, "height": HEIGHT, "paths": paths}))
    print(f"wrote {OUT} — {len(paths)} boroughs, {kept:,} of {total:,} points kept "
          f"({OUT.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
