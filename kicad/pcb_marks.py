#!/usr/bin/env python3
"""Put the Riposte wordmark and the sfz mark on a board's silkscreen.

    python3 pcb_marks.py board.kicad_pcb [--side auto|F|B] [--max-width 36]

Reads marks.json (made by svg2marks.py) and places the marks as
board-only footprints LOGO1 (wordmark), LOGO2 (sfz) and LOGO3 (the rule
between them). Runs where pcbnew's Python is: LXC 130. Idempotent: a
second run replaces the marks it placed before.

The two marks go down as one lockup, the way docs/04-logo pairs the
wordmark with another mark: one clear-space unit, an ink rule, one
clear-space unit. The sfz mark takes the wordmark's height:

      ┌────────────────────────────────────────────────┐
      │                   clear (1 cap)                │
      │   ╔══════════════╗  cap │ cap  ╔══════╗        │
      │   ║   RIPOSTE    ║      │      ║ sfz  ║        │
      │   ╚══════════════╝      │      ╚══════╝        │
      │                                                │
      └────────────────────────────────────────────────┘

Where it goes is decided by a cost, not by the biggest hole:

    - on the board's vertical axis (a signature sits centred)
    - just above the board's own label text, which then reads as the
      lockup's sub-line (the sanctioned topbar exception); with no
      label, at the foot of the board
    - over as little copper as it can: silk over a trace is legal but
      shows through the mask as relief

    - centred in whatever frames it: as far from the part above as
      from the part below, and likewise left and right

A candidate is legal when its ink is a cap-height off the board edge and
off any other silk text, half a cap off every part and pad, and off any
untented via. Layouts are tried in order: the row lockup, then the
stacked one, then the two marks apart on the same axis. Each is tried
at the signature width first (SIGNATURE of the board's long side, 28 to
36 mm), shrinking only when nothing fits, and with the edge clearance
relaxed a rung at a time (the parts' clearance follows it down) before
the next layout is tried at all: a pair that sits tight beats a pair
that sits apart.
"""
import argparse
import json
import math
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
STEP_MM = GRID_MM             # candidate centres are tried on this pitch
SHRINK = 0.9                  # per retry when nothing fits at the current width
WORDMARK_CAP_HEIGHT = 0.8     # of the wordmark's height: its clear-space unit
WORDMARK_MAX_MM = 36.0        # a signature, not a billboard: just above the 28 mm floor
SIGNATURE = 0.28              # of the board's long side: the wordmark's target width
PART_CLEAR = 0.5              # of a cap height: room between the ink and a part
RULE_OF_WIDTH = 2 / 110       # docs/04-logo §6: a 2px rule beside the 110px topbar mark
LABEL_MIN_MM = 15.0           # a board text this wide is its label, not a pin name
LABEL_DROP = 0.4              # of a cap height: the label's top sits this far under the ink
CLEAR_LADDER = (1.0, 0.7, 0.5, 0.35)   # of a cap height, off the edge: the rule, then what a tight board affords
BAND_REACH = 2.0              # of a cap height: how far the eye looks for what frames the ink
AXIS_COST = 1.0               # per mm the lockup's centre is off the anchor, across
DEPTH_COST = 0.5              # per mm off the anchor, along
BAND_COST = 1.0               # per mm the ink sits nearer one neighbour than the other
COPPER_COST = 0.01            # per raster cell of track under the ink
LOGO_PREFIX = "LOGO"
LIB_NAME = "RiposteMarks"
NAMES = ("riposte", "sfz", "rule")      # LOGO1, LOGO2, LOGO3
LAYOUTS = ("row", "stack", "split")     # tried in this order

SIDES = {"F": (pcbnew.F_Cu, pcbnew.F_SilkS), "B": (pcbnew.B_Cu, pcbnew.B_SilkS)}


def bbox_mm(b):
    return (pcbnew.ToMM(b.GetLeft()), pcbnew.ToMM(b.GetTop()),
            pcbnew.ToMM(b.GetRight()), pcbnew.ToMM(b.GetBottom()))


def inflate(rect, m):
    x0, y0, x1, y1 = rect
    return (x0 - m, y0 - m, x1 + m, y1 + m)


def overlaps(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


class Grid:
    """Counts on the board's raster with a summed-area table, so asking
    "how much is under this rectangle" costs the same whatever its size."""

    def __init__(self, x0, y0, nx, ny):
        self.x0, self.y0, self.nx, self.ny = x0, y0, nx, ny
        self.cells = [[0] * nx for _ in range(ny)]
        self.sums = None

    def cell(self, x, y):
        return math.floor((x - self.x0) / GRID_MM), math.floor((y - self.y0) / GRID_MM)

    def mark(self, rect, margin=0.0):
        x0, y0, x1, y1 = inflate(rect, margin)
        i0, j0 = self.cell(x0, y0)
        i1, j1 = self.cell(x1, y1)
        for j in range(max(0, j0), min(self.ny - 1, j1) + 1):
            row = self.cells[j]
            for i in range(max(0, i0), min(self.nx - 1, i1) + 1):
                row[i] += 1
        self.sums = None

    def under(self, rect):
        """Sum of the cells whose centre is inside rect."""
        if self.sums is None:
            self.sums = [[0] * (self.nx + 1)]
            for row in self.cells:
                acc, line = 0, [0]
                for v in row:
                    acc += v
                    line.append(acc)
                self.sums.append([a + b for a, b in zip(self.sums[-1], line)])
        x0, y0, x1, y1 = rect
        i0, j0 = self.cell(x0 + GRID_MM / 2, y0 + GRID_MM / 2)
        i1, j1 = self.cell(x1 - GRID_MM / 2, y1 - GRID_MM / 2)
        i0, j0, i1, j1 = max(i0, 0), max(j0, 0), min(i1, self.nx - 1), min(j1, self.ny - 1)
        if i1 < i0 or j1 < j0:
            return 0
        s = self.sums
        return s[j1 + 1][i1 + 1] - s[j0][i1 + 1] - s[j1 + 1][i0] + s[j0][i0]


class Board:
    """One side of a board, seen from the silkscreen: what blocks the ink,
    what merely lies under it, and where the anchor is."""

    def __init__(self, board, side):
        self.side = side
        self.cu, self.silk = SIDES[side]
        self.outline = pcbnew.SHAPE_POLY_SET()
        try:
            board.GetBoardPolygonOutlines(self.outline)
        except TypeError:                                   # KiCad 10 wants aInferOutlineIfNecessary
            board.GetBoardPolygonOutlines(self.outline, True)
        self.box = bbox_mm(board.GetBoardEdgesBoundingBox())
        x0, y0, x1, y1 = self.box
        nx, ny = int((x1 - x0) / GRID_MM) + 1, int((y1 - y0) / GRID_MM) + 1
        self.parts = Grid(x0, y0, nx, ny)       # pads, bodies, holes: the ink keeps PART_CLEAR off
        self.text = Grid(x0, y0, nx, ny)        # other silk: a full clear-space unit off
        self.copper = Grid(x0, y0, nx, ny)      # tracks: a cost, not a wall
        self.label = self.find_label(board)
        self.occupy(board)
        self.via_list = self.vias(board)

    def find_label(self, board):
        """The widest board-level text on this silk: the label the lockup sits over."""
        texts = [d for d in board.GetDrawings()
                 if d.Type() == pcbnew.PCB_TEXT_T and d.GetLayer() == self.silk]
        boxes = [bbox_mm(t.GetBoundingBox()) for t in texts]
        boxes = [b for b in boxes if b[2] - b[0] >= LABEL_MIN_MM]
        return max(boxes, key=lambda b: b[2] - b[0]) if boxes else None

    def occupy(self, board):
        # a generated footprint sits at the origin with its pads offset, so its
        # own bounding box is useless: take the pads and the drawn body instead
        body_layers = {self.silk, pcbnew.F_Fab if self.side == "F" else pcbnew.B_Fab,
                       pcbnew.F_CrtYd if self.side == "F" else pcbnew.B_CrtYd}
        for fp in board.GetFootprints():
            if fp.GetReference().startswith(LOGO_PREFIX):
                continue
            for pad in fp.Pads():
                if pad.IsOnLayer(self.cu) or pad.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH):
                    self.parts.mark(bbox_mm(pad.GetBoundingBox()), PART_MARGIN_MM)
            for item in fp.GraphicalItems():
                if item.GetLayer() in body_layers:
                    self.parts.mark(bbox_mm(item.GetBoundingBox()), PART_MARGIN_MM)
            for text in (fp.Reference(), fp.Value()):
                if text.IsVisible() and text.GetLayer() == self.silk:
                    self.text.mark(bbox_mm(text.GetBoundingBox()))

        for d in board.GetDrawings():
            if d.GetLayer() != self.silk:
                continue
            box = bbox_mm(d.GetBoundingBox())
            if box == self.label:
                continue                        # the label may sit in the lower clear space
            self.text.mark(box)

        for t in board.GetTracks():
            if t.Type() != pcbnew.PCB_VIA_T and t.GetLayer() == self.cu:
                self.copper.mark(bbox_mm(t.GetBoundingBox()))

    def vias(self, board):
        """(x, y, r) in mm of every via the ink must avoid: too small to block
        a candidate, but ink over bare copper is clipped by the mask and looks
        cheap. A tented via is under the mask, so it does not count."""
        ds = board.GetDesignSettings()
        if ds.m_TentViasFront if self.side == "F" else ds.m_TentViasBack:
            return []
        out = []
        for t in board.GetTracks():
            if t.Type() == pcbnew.PCB_VIA_T:
                x0, y0, x1, y1 = bbox_mm(t.GetBoundingBox())
                out.append(((x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + VIA_MARGIN_MM))
        return out

    def clear_of_edge(self, rect, clear):
        """The ink rectangle keeps `clear` (never under EDGE_MARGIN_MM) from the outline."""
        clear = max(clear, EDGE_MARGIN_MM)
        x0, y0, x1, y1 = rect
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        d = 0.7 * clear                                   # the corners on a rounded clear zone
        for px, py in ((x0 - clear, cy), (x1 + clear, cy), (cx, y0 - clear), (cx, y1 + clear),
                       (x0 - d, y0 - d), (x1 + d, y0 - d), (x0 - d, y1 + d), (x1 + d, y1 + d)):
            if not self.outline.Contains(pcbnew.VECTOR2I(MM(px), MM(py))):
                return False
        return True

    def anchor(self, ink_h, cap):
        """Where the lockup wants its centre: on the axis, above the label or at the foot."""
        x0, y0, x1, y1 = self.box
        ax = (x0 + x1) / 2
        if self.label:
            return ax, self.label[1] - LABEL_DROP * cap - ink_h / 2
        return ax, y1

    def legal(self, ink, cap, edge, avoid=None):
        if self.parts.under(inflate(ink, min(PART_CLEAR * cap, edge))):
            return False
        if self.text.under(inflate(ink, cap)):
            return False
        if self.label and overlaps(inflate(ink, PART_MARGIN_MM), self.label):
            return False
        if avoid and overlaps(inflate(ink, cap), avoid):
            return False
        return self.clear_of_edge(ink, edge)

    def reach(self, ink, dx, dy, cap):
        """Free mm from the ink's edge outward in one direction, up to BAND_REACH caps."""
        x0, y0, x1, y1 = ink
        bx0, by0, bx1, by1 = self.box
        steps = int(BAND_REACH * cap / GRID_MM)
        for k in range(steps):
            d0, d1 = k * GRID_MM, (k + 1) * GRID_MM
            strip = ((x1 + d0, y0, x1 + d1, y1) if dx > 0 else (x0 - d1, y0, x0 - d0, y1) if dx < 0
                     else (x0, y1 + d0, x1, y1 + d1) if dy > 0 else (x0, y0 - d1, x1, y0 - d0))
            off_board = strip[0] < bx0 or strip[2] > bx1 or strip[1] < by0 or strip[3] > by1
            if off_board or self.parts.under(strip):
                return d0
        return steps * GRID_MM

    def lopsided(self, ink, cap):
        """How much nearer the ink sits to one neighbour than to the opposite one, in mm."""
        return (abs(self.reach(ink, -1, 0, cap) - self.reach(ink, 1, 0, cap))
                + abs(self.reach(ink, 0, -1, cap) - self.reach(ink, 0, 1, cap)))

    def cost(self, ink, cap, anchor):
        x0, y0, x1, y1 = ink
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        return (AXIS_COST * abs(cx - anchor[0]) + DEPTH_COST * abs(cy - anchor[1])
                + BAND_COST * self.lopsided(ink, cap) + COPPER_COST * self.copper.under(ink))


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


def rule_mark(aspect):
    """A plain bar, unit wide, `aspect` tall, in the shape marks.json uses."""
    return {"aspect": aspect, "source": "docs/04-logo ink rule",
            "polygons": [[(-0.5, -aspect / 2), (0.5, -aspect / 2), (0.5, aspect / 2), (-0.5, aspect / 2)]]}


def pieces(layout, marks, w):
    """The lockup at wordmark width w: [(name, mark, width, dx, dy)] about
    its centre, and its ink size. `split` yields one piece per call site."""
    h = w * marks["riposte"]["aspect"]
    cap = h * WORDMARK_CAP_HEIGHT
    sfz_w = h / marks["sfz"]["aspect"]
    t = w * RULE_OF_WIDTH
    if layout == "row":
        total = w + cap + t + cap + sfz_w
        left = -total / 2
        return ([("riposte", marks["riposte"], w, left + w / 2, 0),
                 ("rule", rule_mark(h / t), t, left + w + cap + t / 2, 0),
                 ("sfz", marks["sfz"], sfz_w, total / 2 - sfz_w / 2, 0)], (total, h))
    if layout == "stack":
        total = h + cap + t + cap + h
        top = -total / 2
        return ([("riposte", marks["riposte"], w, 0, top + h / 2),
                 ("rule", rule_mark(t / sfz_w), sfz_w, 0, top + h + cap + t / 2),
                 ("sfz", marks["sfz"], sfz_w, 0, total / 2 - h / 2)], (w, total))
    raise ValueError(layout)


def spread(lo, hi, origin):
    """origin and every STEP_MM either side of it, within lo..hi."""
    k = math.ceil((lo - origin) / STEP_MM)
    while origin + k * STEP_MM <= hi:
        yield origin + k * STEP_MM
        k += 1


def fit(board, group, size, cap, edge, anchor, avoid=None):
    """Cheapest legal centre for a group of pieces with this ink size, or None.
    Candidates sit on a grid through the anchor, so the anchor itself is one."""
    gw, gh = size
    bx0, by0, bx1, by1 = board.box
    best = None
    for cy in spread(by0 + gh / 2, by1 - gh / 2, anchor[1]):
        for cx in spread(bx0 + gw / 2, bx1 - gw / 2, anchor[0]):
            ink = (cx - gw / 2, cy - gh / 2, cx + gw / 2, cy + gh / 2)
            if not board.legal(ink, cap, edge, avoid):
                continue
            c = board.cost(ink, cap, anchor)
            if best is not None and c >= best[0]:
                continue
            if any(touches(m, pw, cx + dx, cy + dy, board.side, board.via_list) for _, m, pw, dx, dy in group):
                continue
            best = (c, cx, cy)
    return best


def widths(marks, target):
    """Wordmark widths to try, largest first, down to the brand floor."""
    floor = max(marks["riposte"]["min_width_mm"], MIN_SILK_LINE_MM / marks["riposte"]["stroke"])
    sfz_floor = MIN_SILK_LINE_MM / marks["sfz"]["stroke"] * marks["sfz"]["aspect"] / marks["riposte"]["aspect"]
    floor = max(floor, sfz_floor)               # the sfz mark's stroke must survive too
    w = max(target, floor)
    while w >= floor:
        yield w
        w *= SHRINK


def place_side(board, marks, target):
    """Plan for one side: (layout, [(name, mark, width, x, y)], wordmark width, cost) or None."""
    for layout in LAYOUTS:
        for rung in CLEAR_LADDER:
            for w in widths(marks, target):
                h = w * marks["riposte"]["aspect"]
                cap = h * WORDMARK_CAP_HEIGHT
                edge = rung * cap
                if layout == "split":
                    plan = place_split(board, marks, w, cap, edge)
                else:
                    plan = place_group(board, layout, marks, w, cap, edge)
                if plan:
                    return (layout, plan[0], w, plan[1])
    return None


def place_group(board, layout, marks, w, cap, edge):
    """The lockup as one piece."""
    group, size = pieces(layout, marks, w)
    best = fit(board, group, size, cap, edge, board.anchor(size[1], cap))
    if not best:
        return None
    c, cx, cy = best
    # seen from the back, board +x is the viewer's left
    mirror = -1 if board.side == "B" else 1
    return ([(n, m, pw, cx + mirror * dx, cy + dy) for n, m, pw, dx, dy in group], c)


def place_split(board, marks, w, cap, edge):
    """The two marks apart: the wordmark where the lockup would go, the sfz
    mark mirrored through the board's centre so the pair still reads as one."""
    h = w * marks["riposte"]["aspect"]
    word = [("riposte", marks["riposte"], w, 0, 0)]
    best = fit(board, word, (w, h), cap, edge, board.anchor(h, cap))
    if not best:
        return None
    c, wx, wy = best
    word_ink = (wx - w / 2, wy - h / 2, wx + w / 2, wy + h / 2)
    bx0, by0, bx1, by1 = board.box
    mirror = (bx0 + bx1 - wx, by0 + by1 - wy)
    sfz_w = h / marks["sfz"]["aspect"]
    sfz = [("sfz", marks["sfz"], sfz_w, 0, 0)]
    other = fit(board, sfz, (sfz_w, h), cap, edge, mirror, avoid=word_ink)
    if not other:
        return None
    c2, sx, sy = other
    return ([("riposte", marks["riposte"], w, wx, wy), ("sfz", marks["sfz"], sfz_w, sx, sy)], c + c2)


def make_footprint(board, name, mark, width, x, y, side):
    fp = pcbnew.FOOTPRINT(board)
    fp.SetFPID(pcbnew.LIB_ID(LIB_NAME, name))
    fp.SetReference(LOGO_PREFIX + str(NAMES.index(name) + 1))
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
    x0, y0, x1, y1 = bbox_mm(board.GetBoardEdgesBoundingBox())
    target = min(a.max_width, SIGNATURE * max(x1 - x0, y1 - y0))

    sides = ("B", "F") if a.side == "auto" else (a.side,)
    plans = {s: place_side(Board(board, s), marks, target) for s in sides}
    fitted = [s for s in sides if plans[s]]
    if not fitted:
        floor = next(widths(marks, 0))
        print(f"no room on {' or '.join(sides)}: the wordmark needs {floor:.0f} mm and its clear space")
        pcbnew.SaveBoard(a.board, board)
        return
    # the tighter layout wins, then the bigger wordmark, then the cheaper spot;
    # a tie goes to the back, where nothing competes with the parts' labels
    side = min(fitted, key=lambda s: (LAYOUTS.index(plans[s][0]), -plans[s][2], plans[s][3]))

    layout, placed, w, cost = plans[side]
    for name, mark, width, x, y in placed:
        make_footprint(board, name, mark, width, x, y, side)
        print(f"{name:8s} {side}.SilkS  {width:5.1f} mm wide at ({x:.1f}, {y:.1f})")
    print(f"{layout} lockup, wordmark {w:.1f} mm, cost {cost:.1f}")

    pcbnew.SaveBoard(a.board, board)
    print("wrote", a.board)


if __name__ == "__main__":
    main()
