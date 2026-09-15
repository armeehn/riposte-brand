#!/usr/bin/env python3
"""Put the Riposte wordmark and the sfz mark on a board's silkscreen.

    python3 pcb_marks.py board.kicad_pcb [--side auto|F|B] [--max-width 60]

Reads marks.json (made by svg2marks.py) and places each mark as a
board-only footprint LOGO1 / LOGO2 in the largest free patch of the
chosen side. Runs where pcbnew's Python is: LXC 130. Idempotent: a
second run replaces the marks it placed before.

Free space is found on a grid of the board:

    . . . . . . . . . . . .      . free (inside the outline, nothing there)
    . # # # . . . . . . # .      # blocked: a part, a pad, a hole, silk text,
    . # # # . . . . . . # .        plus a margin round each and round the edge
    . . . . . [ mark ] . . .
    . . . . . . . . . . . .

Rules honoured (riposte-brand docs/04-logo): the wordmark goes no
smaller than 28 mm and keeps one cap-height clear on every side. The
sfz mark's floor is the fab's silkscreen line width against its
thinnest stroke.
"""
import argparse
import json
import os
import subprocess
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
MARKS_JSON = os.path.join(HERE, "marks.json")
MM = pcbnew.FromMM

GRID_MM = 0.5                 # occupancy raster
EDGE_MARGIN_MM = 1.0          # silk this close to the edge gets clipped by the fab
PART_MARGIN_MM = 0.5          # silk against a courtyard is read as part of it
MIN_SILK_LINE_MM = 0.15       # common fab floor for silkscreen
VIA_MARGIN_MM = 0.15          # ink stays this far off a via's ring
NUDGE_MM = 1.0                # placement search step inside a free rectangle
SHRINK = 0.9                  # per retry when every spot hits a via
WORDMARK_CAP_HEIGHT = 0.8     # of the wordmark's height: its clear-space unit
WORDMARK_MAX_MM = 36.0        # a signature, not a billboard: just above the 28 mm floor
SFZ_CLEAR = 0.25              # of the mark's height: room round the monogram
LOGO_PREFIX = "LOGO"
LIB_NAME = "RiposteMarks"
ORDER = ("riposte", "sfz")    # the wordmark is the harder fit, so it goes first

SIDES = {"F": (pcbnew.F_Cu, pcbnew.F_SilkS), "B": (pcbnew.B_Cu, pcbnew.B_SilkS)}


def bbox_mm(b):
    return (pcbnew.ToMM(b.GetLeft()), pcbnew.ToMM(b.GetTop()),
            pcbnew.ToMM(b.GetRight()), pcbnew.ToMM(b.GetBottom()))


class Raster:
    """Boolean grid over the board's bounding box; True is free."""

    def __init__(self, board):
        self.outline = pcbnew.SHAPE_POLY_SET()
        try:
            board.GetBoardPolygonOutlines(self.outline)
        except TypeError:                                   # KiCad 10 wants aInferOutlineIfNecessary
            board.GetBoardPolygonOutlines(self.outline, True)
        x0, y0, x1, y1 = bbox_mm(board.GetBoardEdgesBoundingBox())
        self.x0, self.y0 = x0, y0
        self.nx = int((x1 - x0) / GRID_MM) + 1
        self.ny = int((y1 - y0) / GRID_MM) + 1
        self.cells = [[self.inside(i, j) for i in range(self.nx)] for j in range(self.ny)]

    def inside(self, i, j):
        """Free of the edge: the point and its margin ring are within the outline."""
        cx, cy = self.x0 + i * GRID_MM, self.y0 + j * GRID_MM
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7), (-0.7, -0.7)):
            p = pcbnew.VECTOR2I(MM(cx + dx * EDGE_MARGIN_MM), MM(cy + dy * EDGE_MARGIN_MM))
            if not self.outline.Contains(p):
                return False
        return True

    def block(self, box, margin=PART_MARGIN_MM):
        x0, y0, x1, y1 = box
        i0 = max(0, int((x0 - margin - self.x0) / GRID_MM))
        i1 = min(self.nx - 1, int((x1 + margin - self.x0) / GRID_MM) + 1)
        j0 = max(0, int((y0 - margin - self.y0) / GRID_MM))
        j1 = min(self.ny - 1, int((y1 + margin - self.y0) / GRID_MM) + 1)
        for j in range(j0, j1 + 1):
            row = self.cells[j]
            for i in range(i0, i1 + 1):
                row[i] = False

    def rectangles(self):
        """Every maximal free rectangle as (x0, y0, w, h) in mm."""
        found = []
        heights = [0] * self.nx
        for j in range(self.ny):
            row = self.cells[j]
            heights = [heights[i] + 1 if row[i] else 0 for i in range(self.nx)]
            stack = []
            for i in range(self.nx + 1):
                h = heights[i] if i < self.nx else 0
                start = i
                while stack and stack[-1][1] >= h:
                    s, sh = stack.pop()
                    found.append((self.x0 + s * GRID_MM, self.y0 + (j - sh + 1) * GRID_MM,
                                  (i - s) * GRID_MM, sh * GRID_MM))
                    start = s
                stack.append((start, h))
        return found


def occupy(raster, board, side):
    """Block whatever a silk mark must not sit on, seen from this side."""
    cu, silk = SIDES[side]

    # a generated footprint sits at the origin with its pads offset, so its
    # own bounding box is useless: take the pads and the drawn body instead
    body_layers = {silk, pcbnew.F_Fab if side == "F" else pcbnew.B_Fab,
                   pcbnew.F_CrtYd if side == "F" else pcbnew.B_CrtYd}
    for fp in board.GetFootprints():
        if fp.GetReference().startswith(LOGO_PREFIX):
            continue
        for pad in fp.Pads():
            if pad.IsOnLayer(cu) or pad.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH):
                raster.block(bbox_mm(pad.GetBoundingBox()))
        for item in fp.GraphicalItems():
            if item.GetLayer() in body_layers:
                raster.block(bbox_mm(item.GetBoundingBox()))
        for text in (fp.Reference(), fp.Value()):
            if text.IsVisible() and text.GetLayer() == silk:
                raster.block(bbox_mm(text.GetBoundingBox()))

    for d in board.GetDrawings():
        if d.GetLayer() == silk:
            raster.block(bbox_mm(d.GetBoundingBox()))


def vias(board):
    """(x, y, r) in mm of every via: too small to block a rectangle, but
    ink over one looks cheap, so the mark is tested against them."""
    out = []
    for t in board.GetTracks():
        if t.Type() == pcbnew.PCB_VIA_T:
            x0, y0, x1, y1 = bbox_mm(t.GetBoundingBox())
            out.append(((x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + VIA_MARGIN_MM))
    return out


def inked(poly, x, y):
    """Ray-casting point-in-polygon."""
    inside = False
    n = len(poly)
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            inside = not inside
    return inside


def touches(mark, width, cx, cy, side, via_list):
    """Does any via sit under the ink of the mark placed here?"""
    half_h = width * mark["aspect"] / 2
    mirror = -1 if side == "B" else 1
    for vx, vy, r in via_list:
        if abs(vx - cx) > width / 2 + r or abs(vy - cy) > half_h + r:
            continue
        for dx, dy in ((0, 0), (r, 0), (-r, 0), (0, r), (0, -r)):
            ux, uy = mirror * (vx + dx - cx) / width, (vy + dy - cy) / width
            if any(inked(poly, ux, uy) for poly in mark["polygons"]):
                return True
    return False


def centre_out(lo, hi, step):
    """lo..hi in steps, nearest the middle first."""
    mid = (lo + hi) / 2
    n = int((hi - lo) / step / 2)
    yield mid
    for k in range(1, n + 1):
        yield mid - k * step
        yield mid + k * step


def best_fit(rects, mark, min_w, max_w, side, via_list):
    """Largest width the mark can take clear of vias, and where."""
    aspect = mark["aspect"]
    rects = sorted(rects, key=lambda r: -min(r[2], r[3] / aspect))
    best = None
    for x, y, w, h in rects:
        width = min(w, h / aspect, max_w)
        while width >= min_w and (best is None or width > best[0]):
            hgt = width * aspect
            spots = ((cx, cy) for cy in centre_out(y + hgt / 2, y + h - hgt / 2, NUDGE_MM)
                     for cx in centre_out(x + width / 2, x + w - width / 2, NUDGE_MM))
            spot = next((s for s in spots if not touches(mark, width, s[0], s[1], side, via_list)), None)
            if spot:
                best = (width, spot[0], spot[1])
                break
            width *= SHRINK
    return best


def make_footprint(board, name, mark, width, x, y, side):
    fp = pcbnew.FOOTPRINT(board)
    fp.SetFPID(pcbnew.LIB_ID(LIB_NAME, name))
    fp.SetReference(LOGO_PREFIX + str(ORDER.index(name) + 1))
    fp.SetValue(name)
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    fp.SetAttributes(pcbnew.FP_BOARD_ONLY | pcbnew.FP_EXCLUDE_FROM_POS_FILES | pcbnew.FP_EXCLUDE_FROM_BOM)
    fp.SetLibDescription(f"{mark['source']} at {width:.1f} mm, riposte-brand/kicad/pcb_marks.py")

    for poly in mark["polygons"]:
        s = pcbnew.PCB_SHAPE(fp)
        s.SetShape(pcbnew.SHAPE_T_POLY)
        s.SetPolyPoints([pcbnew.VECTOR2I(MM(px * width), MM(py * width)) for px, py in poly])
        s.SetFilled(True)
        s.SetWidth(0)
        s.SetLayer(pcbnew.F_SilkS)
        fp.Add(s)

    board.Add(fp)
    fp.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
    if side == "B":
        fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
    return fp


def place_side(board, marks, side, max_w):
    """Plan (name, width, x, y) for each mark on one side; None where it fails."""
    raster = Raster(board)
    occupy(raster, board, side)
    via_list = vias(board)
    plan = []
    height = max_w * marks[ORDER[0]]["aspect"]      # the sfz mark matches the wordmark's height
    for name in ORDER:
        mark = marks[name]
        min_w = max(mark["min_width_mm"], MIN_SILK_LINE_MM / mark["stroke"])
        fit = best_fit(raster.rectangles(), mark, min_w, height / mark["aspect"], side, via_list)
        plan.append((name,) + fit if fit else None)
        if not fit:
            continue
        w, cx, cy = fit
        h = height = w * mark["aspect"]
        clear = h * (WORDMARK_CAP_HEIGHT if name == "riposte" else SFZ_CLEAR)
        raster.block((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), margin=clear)
    return plan


def strip(path):
    """Drop earlier LOGO footprints in a process of their own.

    pcbnew misbehaves after Remove() (later calls hand back bare SWIG
    objects), so this never shares a process with the placement.
    """
    board = pcbnew.LoadBoard(path)
    old = [fp for fp in board.GetFootprints() if fp.GetReference().startswith(LOGO_PREFIX)]
    if not old:
        return
    for fp in old:
        board.Remove(fp)
    pcbnew.SaveBoard(path, board)
    print("stripped", ", ".join(fp.GetReference() for fp in old))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("board")
    ap.add_argument("--side", choices=("auto", "F", "B"), default="auto")
    ap.add_argument("--max-width", type=float, default=WORDMARK_MAX_MM, help="mm, the wordmark's ceiling")
    ap.add_argument("--strip", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args()

    if a.strip:
        strip(a.board)
        return
    subprocess.run([sys.executable, __file__, "--strip", a.board], check=True)

    with open(MARKS_JSON) as f:
        marks = json.load(f)
    board = pcbnew.LoadBoard(a.board)

    sides = ("B", "F") if a.side == "auto" else (a.side,)
    plans = {s: place_side(board, marks, s, a.max_width) for s in sides}
    # the side that fits more marks, then the one that fits them bigger;
    # a tie goes to the back, where nothing competes with the parts' labels
    side = max(sides, key=lambda s: (sum(p is not None for p in plans[s]),
                                     sum(p[1] for p in plans[s] if p)))

    for p in plans[side]:
        if p is None:
            continue
        name, w, x, y = p
        make_footprint(board, name, marks[name], w, x, y, side)
        print(f"{name:8s} {side}.SilkS  {w:5.1f} mm wide at ({x:.1f}, {y:.1f})")
    for name, p in zip(ORDER, plans[side]):
        if p is None:
            print(f"{name:8s} no room on {side}: needs {max(marks[name]['min_width_mm'], MIN_SILK_LINE_MM / marks[name]['stroke']):.0f} mm")

    pcbnew.SaveBoard(a.board, board)
    print("wrote", a.board)


if __name__ == "__main__":
    main()
