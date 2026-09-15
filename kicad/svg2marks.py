#!/usr/bin/env python3
"""Turn the brand SVGs into silkscreen-ready polygons: marks.json.

    source SVG --> flatten curves --> shapely --> holes cut away
               --> unit-width polygons, one JSON entry per mark

pcb_marks.py reads marks.json and scales the polygons onto a board. It
needs no SVG library and no shapely, so it runs where KiCad runs.

A silkscreen polygon cannot have holes, so every hole is cut through
with a horizontal line, which turns one ring-with-hole into two simple
polygons that meet on that line:

        +-------+           +-------+
        |  +-+  |    -->    |  +-+  |   upper piece
        |  | |  |           +--+ +--+
        |  +-+  |           +--+ +--+
        +-------+           |  +-+  |   lower piece
                            +-------+

Run in LXC 111 with the Ink/Stitch venv (svgelements + shapely):

    /home/user/inkstitch/.venv/bin/python kicad/svg2marks.py
"""
import json
import os
import re
from xml.etree import ElementTree as ET

from shapely.geometry import MultiPolygon, Polygon, box
from shapely.ops import unary_union
from svgelements import Close, Line, Move, Path

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_DIR = os.path.join(HERE, "..", "assets", "logo")
OUT = os.path.join(HERE, "marks.json")

CURVE_SAMPLES = 24              # points per Bezier segment
SLIVER_FRACTION = 1e-5          # of the mark's area: construction artefacts
SIMPLIFY = 0.0006               # in unit widths: 0.03 mm on a 50 mm mark
SEAM_OVERLAP = 0.001            # pieces overlap this much on the cut line
STROKE_AREA_KEEP = 0.5          # erosion that keeps half the ink = a typical stroke

# name -> (file, min width on a board in mm, why)
MARKS = {
    "riposte": ("riposte-ink.svg", 28.0, "docs/04-logo: print minimum; esh's checker turns to mud below"),
    "sfz": ("sfz-ink.svg", 0.0, "limited by the silkscreen line width only"),
}


def subpaths(d):
    """Yield closed polylines, one per subpath of d."""
    pts = []
    for seg in Path(d):
        if isinstance(seg, Move):
            if len(pts) > 2:
                yield pts
            pts = [(seg.end.x, seg.end.y)]
        elif isinstance(seg, (Line, Close)):
            pts.append((seg.end.x, seg.end.y))
        else:
            for i in range(1, CURVE_SAMPLES + 1):
                p = seg.point(i / CURVE_SAMPLES)
                pts.append((p.x, p.y))
    if len(pts) > 2:
        yield pts


def path_shape(d):
    """Nonzero-ish fill: a ring inside an accepted ring becomes a hole."""
    rings = sorted((Polygon(p).buffer(0) for p in subpaths(d)), key=lambda r: -r.area)
    shape = Polygon()
    for r in rings:
        if shape.contains(r.representative_point()):
            shape = shape.difference(r)
        else:
            shape = shape.union(r)
    return shape


def svg_shape(path):
    """All paths of the file, unioned: one ink colour on a silkscreen."""
    root = ET.parse(path).getroot()
    shapes = [path_shape(el.get("d")) for el in root.iter() if el.tag.endswith("path")]
    shape = unary_union(shapes)
    sliver = shape.area * SLIVER_FRACTION
    return unary_union([p for p in polygons(shape) if p.area > sliver])


def polygons(shape):
    if isinstance(shape, Polygon):
        return [shape] if not shape.is_empty else []
    if isinstance(shape, MultiPolygon):
        return list(shape.geoms)
    return [g for g in getattr(shape, "geoms", []) if isinstance(g, Polygon)]


def fracture(poly):
    """Simple polygons covering poly: each hole is cut through horizontally."""
    if not poly.interiors:
        return [poly]

    minx, miny, maxx, maxy = poly.bounds
    y = poly.interiors[0].centroid.y
    upper = poly.intersection(box(minx, y - SEAM_OVERLAP, maxx, maxy))
    lower = poly.intersection(box(minx, miny, maxx, y + SEAM_OVERLAP))

    out = []
    for piece in polygons(upper) + polygons(lower):
        out.extend(fracture(piece))
    return out


def stroke_ratio(shape, width):
    """Typical stroke width as a fraction of the mark's width.

    Erode until half the ink is gone; the stroke is twice that radius.
    """
    lo, hi = 0.0, width / 2
    for _ in range(40):
        mid = (lo + hi) / 2
        if shape.buffer(-mid).area > shape.area * STROKE_AREA_KEEP:
            lo = mid
        else:
            hi = mid
    return 2 * lo / width


def normalise(shape):
    """Scale to unit width, origin at the ink's centre, y down as in KiCad."""
    minx, miny, maxx, maxy = shape.bounds
    w = maxx - minx
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    pieces = []
    for poly in polygons(shape):
        for piece in fracture(poly):
            piece = piece.simplify(SIMPLIFY * w)
            pieces.append([[round((x - cx) / w, 5), round((y - cy) / w, 5)]
                           for x, y in piece.exterior.coords[:-1]])
    return pieces, (maxy - miny) / w


def main():
    marks = {}
    for name, (fname, min_mm, why) in MARKS.items():
        shape = svg_shape(os.path.join(LOGO_DIR, fname))
        width = shape.bounds[2] - shape.bounds[0]
        pieces, aspect = normalise(shape)
        marks[name] = {
            "source": fname,
            "aspect": round(aspect, 5),           # height / width
            "stroke": round(stroke_ratio(shape, width), 5),
            "min_width_mm": min_mm,
            "min_width_why": why,
            "polygons": pieces,
        }
        print(f"{name:8s} {fname:22s} h/w {aspect:.3f}  stroke {marks[name]['stroke']:.4f} w  "
              f"{len(pieces)} polygons  {sum(len(p) for p in pieces)} points")

    with open(OUT, "w") as f:
        json.dump(marks, f, separators=(",", ":"))
    print("wrote", os.path.relpath(OUT))


if __name__ == "__main__":
    main()
