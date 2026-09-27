"""WellSense product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders. Surface logger: the FieldNode core with a filleted
light grey enclosure, side ribs, a lid parting line, lid screws, a clear lid window over the
controller board with a lit green status light, a lid label, M12 sensor ports (port 1 with the
lead plugged in, port 2 capped), the whip antenna, the 6 W panel with its frame and cell grid on
flat-bar legs, and the back plate with V-blocks and band clamps; the junction box with a clear lid
window over the 4 to 20 mA interface board (shunt, ADC, 24 V boost, terminal block, lit power
light), lid screws, a WellSense label, a top cable gland, the conduit hub and the clear desiccant
breather with orange silica gel; the louvered barometric sensor housing. Wellhead: the teal split
seal plate with its gasket line, bolts and EPDM glands; the PVC tube cap with its stainless cable
grip hanger; the galvanized conduit with swept bends and a compression gland. In the well: the
slotted PVC access tube with its end plug and the 22 mm stainless vented transducer with a black
nose guard and a teal band, on its vented cable. Context is a compact block of ground cut open on
the viewer's side: dry soil over the saturated aquifer, a small concrete apron, the steel casing
in section with the existing pump riser and the well water (clear).
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every part size, the wellhead, the tube and probe positions in plan, the post, junction box,
barometric sensor and FieldNode offsets relative to the post, and the conduit route come from
PARAMS, derived() and build_parts() in model.py, with the same axes: the well axis is the Z axis,
Z is up with the ground at z = 0, the post stands on -X and the FieldNode core faces -Y.
Render layout (not the installed layout), see the constants below and docs/REVIEW.md, session
2026-09-26: the post is drawn 330 mm from the well instead of 750 mm and everything on it 350 mm
lower (FieldNode base 1.40 m instead of 1.75 m, junction box center 0.90 m instead of 1.25 m);
the borehole is shortened further, with the probe tip 0.58 m below the ground and the water 0.15 m
below the ground. The panel tilt comes from derived()["panel_rot_x"] in model.py (cells toward -Y).
The post, the access tube and the vented cable are each drawn in two parts: the lower post and
footing, the upper access tube and the upper cable are in the "context" group, so the exploded view
shows the logger on the upper post, the wellhead parts and the probe on the slotted tube section
side by side.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Align, Axis, Box, Circle, Cone, Cylinder, FilletPolyline, Plane, Pos,
                       RegularPolygon, Rot, Solid, Sphere, Text, Vector, extrude, fillet, sweep)
from model import PARAMS, derived, build_parts

_FONT = Path(__file__).resolve().parents[2] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf"

TITLE = "WellSense: well and borehole water level logger"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); ground cut open to show "
             "the casing, access tube and submersible probe below the water line, teal wellhead seal and "
             "conduit to the junction box and FieldNode logger on the post. Post drawn closer and lower "
             "than installed; borehole shortened (design probe depth 30 m)"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): FieldNode panel, lid, "
             "controller board and ports, barometric sensor, junction box lid, interface board and breather on "
             "the upper post (left); seal plate, gasket, glands, tube cap, hanger and conduit (center); slotted "
             "access tube, end plug and the pressure transducer on its vented cable (right)"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 14, "az": -35,
     "note": "Detail from the front right, slightly above (about 14 deg elevation), without the well and "
             "ground: FieldNode core with its panel, lit status light and M12 ports; junction box with the "
             "interface board behind its clear window, desiccant breather and conduit hub; barometric "
             "sensor on the post"},
]

# ---------------------------------------------------------------- render layout (not installed)
RENDER_POST_X = -330.0      # post axis X (installed: PARAMS["post_x"], -750 mm)
RENDER_DZ = -350.0          # everything on the post drawn this much lower than installed
DISP_BOT = -650.0           # bottom of the ground block and of the casing section shown
DISP_WATER = -150.0         # water level shown (model.py display: -1100 mm)
DISP_TUBE_BOT = -630.0      # bottom of the access tube shown (model.py display: -1950 mm)
BLOCK = (-560.0, 460.0, -400.0, 400.0)   # ground block x0, x1, y0, y1
APRON_D = 640.0             # concrete apron drawn smaller than the existing 1.2 m apron
POST_SPLIT_Z = 760.0        # post drawn in two parts: upper (logger detail) and lower
TUBE_SPLIT_Z = -100.0       # access tube drawn in two parts: slotted bottom (exploded view) and upper
E_LOGGER = (-300.0, 0.0, -300.0)   # exploded view: logger group offset, added to its parts' own offsets
CABLE_STUB = 180.0          # length of vented cable drawn with the probe in the exploded view

# Colors (restrained product palette; kit accent; FieldNode colors as in its product model)
C_SHELL = "#DADDE1"
C_LID = "#E6E8EB"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_ACCENT = "#0F766E"
C_WINDOW = "#DCEBF5"
C_STEEL = "#A7AEB6"
C_GALV = "#9EA6AE"
C_ALU = "#C3C8CE"
C_ALU2 = "#AEB4BB"
C_CELLS = "#1B2735"
C_GRID = "#C9CED4"
C_LABEL = "#F4F4F2"
C_PCB = "#166534"
C_PCB_DARK = "#1A1D21"
C_CHIP = "#111827"
C_MODULE = "#1E3A5F"
C_TERM = "#2E7D5B"
C_LED_G = "#22C55E"
C_GEL = "#E08A2E"
C_PVC = "#E4E6E3"
C_PVC_CAP = "#CDD1D4"
C_CABLE = "#1F2328"
C_WHITE = "#EEF0F2"
C_SOIL = "#CBBDA6"
C_AQUIFER = "#A3947F"
C_CONCRETE = "#C9C5BC"
C_CASING = "#7E858D"
C_RISER = "#6B7280"
C_WATER = "#7FB3E0"


# ---------------------------------------------------------------- helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _bx(x0, x1, y0, y1, z0, z1):
    return _box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, x1 - x0, y1 - y0, z1 - z0)


def _zc(x, y, z0, z1, r):
    """Vertical cylinder from z0 to z1."""
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _rod(a, c, r):
    a, c = Vector(*a), Vector(*c)
    d = c - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _hex_x(x, y, z, af, h):
    return Pos(x - h / 2, y, z) * extrude(Plane.YZ * RegularPolygon(af / 1.732, 6), amount=h)


def _fmin(s, axis):
    return s.faces().sort_by(axis)[0].edges()


def _fmax(s, axis):
    return s.faces().sort_by(axis)[-1].edges()


def _union(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def _swept(points, r, bend):
    """Round tube or cable along `points` with filleted bends; spheres at the joints as a fallback."""
    try:
        path = FilletPolyline(*points, radius=bend)
        a, b = Vector(*points[0]), Vector(*points[1])
        prof = Plane(origin=a, z_dir=(b - a).normalized()) * Circle(r)
        s = sweep(prof, path=path)
        if s.is_valid and s.volume > 0:
            return s
    except Exception:
        pass
    out = None
    for a, c in zip(points, points[1:]):
        seg = _rod(a, c, r)
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _text(txt, size, origin, x_dir, z_dir, h=0.3):
    """Raised text on a face whose outward normal is z_dir, centerd on origin."""
    t = extrude(Text(txt, font_size=size, font_path=str(_FONT), align=(Align.CENTER, Align.CENTER)), amount=h)
    return Plane(origin=origin, x_dir=x_dir, z_dir=z_dir) * t


def _text_ny(txt, size, x, y, z, h=0.3):
    return _text(txt, size, (x, y, z), (1, 0, 0), (0, -1, 0), h)


def _text_px(txt, size, x, y, z, h=0.3):
    return _text(txt, size, (x, y, z), (0, 1, 0), (1, 0, 0), h)


def _notch(z_top=0.0):
    """The ground and well are cut open on the viewer's side (y < 0) below z_top: a half section."""
    return _bx(-2000.0, 2000.0, -2000.0, 0.0, -3000.0, z_top)


# ---------------------------------------------------------------- parts
def product_parts(P=PARAMS):
    D = derived(P)
    M = build_parts(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    dz = RENDER_DZ
    px, po = RENDER_POST_X, P["post_od"] / 2
    tx, to, ti = P["tube_x"], P["tube_od"] / 2, P["tube_id"] / 2
    rx, rr = P["riser_x"], P["riser_od"] / 2
    st = P["stickup"]
    seal_top = D["seal_top"]
    cap_top = D["cap_top"]
    jx, jy, jz = P["jbox"]
    jcx = px + po + jx / 2
    jcz = P["jbox_z"] + dz
    jb0, jb1 = jcz - jz / 2, jcz + jz / 2
    z0 = P["fnd_z0"] + dz
    notch = _notch(0.0)

    # exploded offsets (hero coordinates)
    E_FND = (0, 0, 130)
    E_JB = (0, 0, 60)

    def e(base, d=(0, 0, 0)):
        return tuple(base[i] + d[i] for i in range(3))

    # ============================================================ FieldNode core (BOM 8)
    ew, ed, eh = P["fnd_enc"]
    y_back = D["enc_back"]                      # -45, on the back plate
    y_front = D["enc_front"]                    # -135, lid face
    lid_d, wt = 12.0, 3.0
    ys = y_front + lid_d                        # parting line
    zc = z0 + eh / 2
    outer = _bx(px - ew / 2, px + ew / 2, y_front, y_back, z0, z0 + eh)
    outer = _fillet_try(outer, outer.edges().filter_by(Axis.Y), [9.0, 7.0, 5.0])
    outer = _fillet_try(outer, _fmin(outer, Axis.Y), [3.0, 2.0, 1.0])
    body = outer & _bx(px - 200, px + 200, ys + 0.4, y_back + 1, z0 - 10, z0 + eh + 10)
    body -= _bx(px - ew / 2 + wt, px + ew / 2 - wt, ys, y_back - wt, z0 + wt, z0 + eh - wt)
    for sx in (-1, 1):                                  # side ribs
        for k in range(5):
            body -= _box(px + sx * ew / 2, ys + 14 + 11 * k, zc, 1.6, 3.0, eh - 50)
    add("FieldNode enclosure base", body, C_SHELL, "plastic", 8, "shell", E_FND)

    lid = outer & _bx(px - 200, px + 200, y_front - 1, ys - 0.4, z0 - 10, z0 + eh + 10)
    lid -= _bx(px - ew / 2 + wt, px + ew / 2 - wt, y_front + wt, ys, z0 + wt, z0 + eh - wt)
    wx0, wx1, wz0, wz1 = px - 48, px + 48, z0 + 118, z0 + 176
    win = _bx(wx0, wx1, y_front - 1, y_front + wt + 1, wz0, wz1)
    win = _fillet_try(win, win.edges().filter_by(Axis.Y), [6.0, 4.0])
    lid -= win
    lid -= _ycyl(px + 56, y_front + wt / 2, z0 + 14, 2.6, wt + 2)
    E_FLID = e(E_FND, (0, -170, 0))
    add("FieldNode lid", lid, C_LID, "plastic", 8, "shell", E_FLID)
    pane = _bx(wx0 - 3, wx1 + 3, y_front + wt, y_front + wt + 1.5, wz0 - 3, wz1 + 3)
    pane = _fillet_try(pane, pane.edges().filter_by(Axis.Y), [8.0, 6.0])
    add("FieldNode lid window (clear polycarbonate)", pane, C_WINDOW, "clear", 8, "shell", E_FLID)
    bez = _bx(wx0 - 4, wx1 + 4, y_front - 0.8, y_front, wz0 - 4, wz1 + 4)
    bez = _fillet_try(bez, bez.edges().filter_by(Axis.Y), [9.0, 7.0])
    bez -= _bx(wx0, wx1, y_front - 3, y_front + 1, wz0, wz1)
    add("FieldNode window trim", bez, C_DARK, "plastic", 8, "shell", E_FLID)
    gasket = (_bx(px - ew / 2 + 1, px + ew / 2 - 1, ys - 0.4, ys + 0.4, z0 + 1, z0 + eh - 1)
              - _bx(px - ew / 2 + wt, px + ew / 2 - wt, ys - 1, ys + 1, z0 + wt, z0 + eh - wt))
    add("FieldNode lid gasket", gasket, C_BLACK, "rubber", 8, "shell", e(E_FND, (0, -85, 0)))
    scr = []
    for sx in (-1, 1):
        for sz in (-1, 1):
            x, z = px + sx * (ew / 2 - 11), zc + sz * (eh / 2 - 11)
            s = _ycyl(x, y_front - 0.6, z, 3.4, 1.2)
            s -= _box(x, y_front - 1.2, z, 4.0, 1.0, 0.8)
            s -= _box(x, y_front - 1.2, z, 0.8, 1.0, 4.0)
            scr.append(s)
    add("FieldNode lid screws", _union(scr), C_STEEL, "metal", 8, "shell", e(E_FND, (0, -200, 0)))
    ly, lz = y_front - 0.2, z0 + 66
    add("FieldNode lid label", _box(px, ly, lz, 112, 0.4, 70), C_LABEL, "paper", 8, "shell", E_FLID)
    add("FieldNode label accent band", _box(px, ly - 0.3, lz + 27, 112, 0.3, 12), C_ACCENT, "painted", 8,
        "shell", E_FLID)
    ink = _text_ny("FieldNode", 13.0, px, ly - 0.2, lz + 5)
    ink += _text_ny("SOLAR LORAWAN SENSOR NODE", 5.2, px, ly - 0.2, lz - 11)
    ink += _box(px, ly - 0.35, lz - 22, 90, 0.3, 1.0)
    add("FieldNode label print", ink, C_DARK, "paper", 8, "shell", E_FLID)
    add("FieldNode label band text", _text_ny("OPEN HARDWARE CORE", 6.0, px, ly - 0.4, lz + 27, h=0.2),
        C_LABEL, "paper", 8, "shell", E_FLID)
    marks = []
    for dxp, t in zip(P["fnd_port_x"], ("1", "2")):
        marks.append(_text_ny(t, 8.0, px + dxp, y_front - 0.1, z0 + 14, h=0.4))
    add("FieldNode port markings", _union(marks), C_ACCENT, "painted", 8, "shell", E_FLID)
    lbez = _ycyl(px + 56, y_front - 0.8, z0 + 14, 4.5, 1.6) - _ycyl(px + 56, y_front - 0.8, z0 + 14, 2.6, 3.0)
    add("FieldNode status light bezel", lbez, C_DARK, "plastic", 8, "shell", E_FLID)
    dome = Pos(px + 56, y_front + 0.4, z0 + 14) * Sphere(3.0) & _bx(px + 50, px + 62, y_front - 2.6, y_front + wt,
                                                                      z0 + 8, z0 + 20)
    add("FieldNode status light, green (lit)", dome, C_LED_G, "emissive", 8, "shell", E_FLID)

    # controller board behind the lid window (illustrative)
    E_CTRL = e(E_FND, (0, -110, 0))
    yb = ys + 18
    cpcb = _bx(px - 60, px + 60, yb, yb + 1.6, z0 + 60, z0 + 188)
    add("FieldNode controller board", cpcb, C_PCB_DARK, "plastic", 8, "internal", E_CTRL)
    comp = _bx(px - 30, px + 2, yb - 3.0, yb, z0 + 132, z0 + 164)                 # LoRa module can
    comp += _bx(px + 12, px + 34, yb - 2.0, yb, z0 + 140, z0 + 162)
    comp += _bx(px - 44, px - 36, yb - 1.4, yb, z0 + 124, z0 + 170)
    comp += _bx(px + 12, px + 44, yb - 6.0, yb, z0 + 72, z0 + 84)                  # connector
    add("FieldNode controller components", comp, C_CHIP, "plastic", 8, "internal", E_CTRL)
    can = _bx(px - 28, px, yb - 3.6, yb - 3.0, z0 + 134, z0 + 162)
    add("FieldNode radio shield can", can, C_ALU, "metal", 8, "internal", E_CTRL)
    led = _bx(px + 52, px + 60, yb - 1.4, yb, z0 + 70, z0 + 76)
    add("FieldNode board light (lit)", led, C_LED_G, "emissive", 8, "internal", E_CTRL)

    # ports underneath: M12 port 1 with the WellSense lead plug, port 2 capped; whip antenna
    E_DOWN = e(E_FND, (0, 0, -70))
    yp = D["enc_yc"]
    socks, ins = [], []
    for dxp in P["fnd_port_x"]:
        x = px + dxp
        s = _hex_z(x, yp, z0 - 2.0, 18.0, 4.0) + _zc(x, yp, z0 - 20, z0 - 4, 8.0)
        socks.append(s)
    add("FieldNode M12 sensor sockets", _union(socks), C_STEEL, "metal", 8, "shell", E_DOWN)
    x2 = px + P["fnd_port_x"][1]
    cap = _zc(x2, yp, z0 - 34, z0 - 18, 9.5)
    cap = _fillet_try(cap, _fmin(cap, Axis.Z), [2.0, 1.0])
    for k in range(12):
        a = 2 * math.pi * k / 12
        cap -= _box(x2 + 9.5 * math.cos(a), yp + 9.5 * math.sin(a), z0 - 24, 1.2, 1.2, 12.0)
    add("FieldNode port 2 sealing cap", cap, C_DARK, "rubber", 8, "shell", e(E_DOWN, (0, 0, -40)))
    ax_, whl = px + P["fnd_ant_x"], P["fnd_whip"][1]
    base = _hex_z(ax_, yp, z0 - 2.5, 16.0, 5.0) + _zc(ax_, yp, z0 - 20, z0 - 5, 7.5)
    base = _fillet_try(base, _fmin(base, Axis.Z), [1.5, 1.0])
    add("FieldNode antenna base", base, C_STEEL, "metal", 8, "shell", E_DOWN)
    whip = _zc(ax_, yp, z0 - 20 - whl, z0 - 20, P["fnd_whip"][0] / 2)
    whip = _fillet_try(whip, _fmin(whip, Axis.Z), [4.0, 2.5])
    add("FieldNode whip antenna", whip, C_BLACK, "rubber", 8, "shell", e(E_DOWN, (0, 0, -60)))

    # back plate, V-blocks and band clamps on the post
    E_MNT = e(E_FND, (0, 120, 0))
    pw_, ph_, pt_ = P["fnd_plate"]
    plate = _bx(px - pw_ / 2, px + pw_ / 2, P["fnd_plate_y0"] - pt_, P["fnd_plate_y0"], z0 - 40, z0 - 40 + ph_)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Y), [8.0, 5.0])
    for sx in (-1, 1):
        for zz in (z0 - 22, z0 + 262):
            plate -= _ycyl(px + sx * 70, P["fnd_plate_y0"] - 1.5, zz, 3.5, 5.0)
    add("FieldNode back plate (aluminum)", plate, C_ALU, "metal", 8, "shell", E_MNT)
    vbs, bands = [], []
    for zz in (z0 + 10, z0 + 230):
        vb = _bx(px - 22, px + 22, P["fnd_plate_y0"] + 0.01, -po + 6, zz - 15, zz + 15)
        vb -= _zc(px, 0, zz - 20, zz + 20, po + 0.5)
        vbs.append(vb)
        band = _zc(px, 0, zz - 7, zz + 7, po + 1.5) - _zc(px, 0, zz - 8, zz + 8, po)
        band += _bx(px - 8, px + 8, po - 2, po + 10, zz - 8, zz + 8)                 # worm housing
        bands.append(band)
    add("FieldNode V-blocks", _union(vbs), C_ALU2, "metal", 8, "shell", E_MNT)
    add("FieldNode band clamps", _union(bands), C_STEEL, "metal", 8, "shell", E_MNT)

    # 6 W panel on flat-bar legs, tilted as in model.py (cells toward -Y, see derived()["panel_rot_x"])
    E_PAN = e(E_FND, (0, 0, 180))
    pnw, pnl, pnt = P["fnd_panel"]
    tilt = D["panel_rot_x"]
    pcy, pcz = P["fnd_panel_c"][0], z0 + P["fnd_panel_c"][1]
    pan = Pos(px, pcy, pcz) * Rot(tilt, 0, 0)
    frame = Box(pnw, pnl, pnt)
    frame = _fillet_try(frame, frame.edges().filter_by(Axis.Z), [5.0, 3.0])
    frame -= Pos(0, 0, pnt / 2 - 2) * Box(pnw - 14, pnl - 14, 5)
    frame -= Pos(0, 0, -pnt / 2 + 6) * Box(pnw - 8, pnl - 8, 12.02)
    add("Solar panel frame (anodized aluminum)", pan * frame, C_ALU, "metal", 8, "shell", E_PAN)
    lam = Pos(0, 0, pnt / 2 - 3.2) * Box(pnw - 14, pnl - 14, 2.4)
    lam += Pos(0, 0, -pnt / 2 + 11.5) * Box(pnw - 8, pnl - 8, 1.0)
    add("Solar cells (6 W)", pan * lam, C_CELLS, "screen", 8, "shell", E_PAN)
    grid = []
    zt = pnt / 2 - 1.85
    for k in range(1, 6):
        grid.append(Pos(-(pnw - 14) / 2 + k * (pnw - 14) / 6, 0, zt) * Box(0.9, pnl - 16, 0.3))
    for k in range(1, 4):
        grid.append(Pos(0, -(pnl - 14) / 2 + k * (pnl - 14) / 4, zt) * Box(pnw - 16, 0.9, 0.3))
    add("Solar cell grid lines", pan * _union(grid), C_GRID, "metal", 8, "shell", E_PAN)
    jbp = Pos(90, 30, -pnt / 2 + 5.0 - 6.0) * Box(40, 40, 10)
    add("Panel junction box", pan * jbp, C_BLACK, "plastic", 8, "shell", E_PAN)

    t = math.radians(tilt)

    def under(lyp):
        lzp = -pnt / 2 - 1.0
        return (pcy + lyp * math.cos(t) - lzp * math.sin(t), pcz + lyp * math.sin(t) + lzp * math.cos(t))

    legs = []
    yf = P["fnd_plate_y0"] - pt_ - 2.0
    for sx in (-1, 1):
        x = px + sx * 80
        for lyp, zf in ((60.0, z0 + 262), (-55.0, z0 + 200)):
            hy, hz = under(lyp)
            legs.append(_rod((x, yf, zf), (x, hy, hz), 5.0))
            legs.append(_ycyl(x, yf + 1.0, zf, 7.0, 4.0))
    add("Panel legs (aluminum)", _union(legs), C_ALU2, "metal", 8, "shell", E_PAN)

    # ============================================================ post (BOM 10) and footing (BOM 13)
    ptop = P["post_h"] + dz
    pwall = P["post_wall"]
    upper = _zc(px, 0, POST_SPLIT_Z, ptop, po) - _zc(px, 0, POST_SPLIT_Z - 1, ptop + 1, po - pwall)
    add("Mounting post, upper (galvanized)", upper, C_GALV, "metal", 10, "shell", (0, 0, 0))
    pcap = _zc(px, 0, ptop - 8, ptop + 6, po + 1.5)
    pcap = _fillet_try(pcap, _fmax(pcap, Axis.Z), [4.0, 2.0])
    add("Post cap", pcap, C_BLACK, "plastic", 10, "shell", (0, 0, 60))
    lower = (_zc(px, 0, -P["embed"], POST_SPLIT_Z, po)
             - _zc(px, 0, -P["embed"] + 10, POST_SPLIT_Z + 1, po - pwall))
    add("Mounting post, lower (galvanized)", lower, C_GALV, "metal", 10, "context", (0, 0, 0))
    footing = _zc(px, 0, -P["embed"], -50, P["footing_d"] / 2) - _zc(px, 0, -P["embed"] - 1, -49, po)
    footing = _fillet_try(footing, _fmax(footing, Axis.Z), [20.0, 10.0])
    footing -= notch
    add("Post footing (concrete), cut away", footing, C_CONCRETE, "plastic", 13, "context", (0, 0, 0))

    # ============================================================ junction box (BOM 6) and board (BOM 7)
    xb = px + po                     # back face on the post
    xl = xb + jx                     # lid face (+X)
    lid_t = 14.0
    xs = xl - lid_t                  # parting line
    jouter = _bx(xb, xl, -jy / 2, jy / 2, jb0, jb1)
    jouter = _fillet_try(jouter, jouter.edges().filter_by(Axis.X), [8.0, 6.0, 4.0])
    jouter = _fillet_try(jouter, _fmax(jouter, Axis.X), [2.5, 1.5])
    jbody = jouter & _bx(xb - 1, xs - 0.4, -200, 200, jb0 - 10, jb1 + 10)
    jbody -= _bx(xb + wt, xs + 1, -jy / 2 + wt, jy / 2 - wt, jb0 + wt, jb1 - wt)
    for sy in (-1, 1):                                  # side ribs
        for k in range(4):
            jbody -= _box(xb + 16 + 12 * k, sy * jy / 2, jcz, 3.0, 1.6, jz - 44)
    jbody -= _zc(jcx + 20, 0, jb0 - 1, jb0 + wt + 1, P["conduit_od"] / 2)
    jbody -= _zc(jcx, -20, jb1 - wt - 1, jb1 + 1, 6.5)
    jbody -= _zc(jcx - 20, 35, jb0 - 1, jb0 + wt + 1, 6.0)
    add("Junction box body (IP66)", jbody, C_SHELL, "plastic", 6, "shell", E_JB)

    E_JLID = e(E_JB, (170, 0, 0))
    jlid = jouter & _bx(xs + 0.4, xl + 1, -200, 200, jb0 - 10, jb1 + 10)
    jlid -= _bx(xs, xl - wt, -jy / 2 + wt, jy / 2 - wt, jb0 + wt, jb1 - wt)
    jwz0, jwz1, jwy = jcz - 12, jcz + 62, 30.0
    jwin = _bx(xl - wt - 1, xl + 1, -jwy, jwy, jwz0, jwz1)
    jwin = _fillet_try(jwin, jwin.edges().filter_by(Axis.X), [6.0, 4.0])
    jlid -= jwin
    add("Junction box lid", jlid, C_LID, "plastic", 6, "shell", E_JLID)
    jpane = _bx(xl - wt - 1.5, xl - wt, -jwy - 3, jwy + 3, jwz0 - 3, jwz1 + 3)
    jpane = _fillet_try(jpane, jpane.edges().filter_by(Axis.X), [8.0, 6.0])
    add("Junction box lid window (clear polycarbonate)", jpane, C_WINDOW, "clear", 6, "shell", E_JLID)
    jbez = _bx(xl, xl + 0.8, -jwy - 4, jwy + 4, jwz0 - 4, jwz1 + 4)
    jbez = _fillet_try(jbez, jbez.edges().filter_by(Axis.X), [9.0, 7.0])
    jbez -= _bx(xl - 1, xl + 3, -jwy, jwy, jwz0, jwz1)
    add("Junction box window trim", jbez, C_DARK, "plastic", 6, "shell", E_JLID)
    jg = (_bx(xs - 0.4, xs + 0.4, -jy / 2 + 1, jy / 2 - 1, jb0 + 1, jb1 - 1)
          - _bx(xs - 1, xs + 1, -jy / 2 + wt, jy / 2 - wt, jb0 + wt, jb1 - wt))
    add("Junction box lid gasket", jg, C_BLACK, "rubber", 6, "shell", e(E_JB, (90, 0, 0)))
    jscr = []
    for sy in (-1, 1):
        for sz in (-1, 1):
            y, z = sy * (jy / 2 - 10), jcz + sz * (jz / 2 - 10)
            s = _xcyl(xl + 0.6, y, z, 3.4, 1.2)
            s -= _box(xl + 1.2, y, z, 1.0, 4.0, 0.8)
            s -= _box(xl + 1.2, y, z, 1.0, 0.8, 4.0)
            jscr.append(s)
    add("Junction box lid screws", _union(jscr), C_STEEL, "metal", 6, "shell", e(E_JB, (200, 0, 0)))
    jlz = jb0 + 30
    add("WellSense label", _bx(xl, xl + 0.4, -46, 46, jlz - 18, jlz + 18), C_LABEL, "paper", 6, "shell", E_JLID)
    add("WellSense label accent band", _bx(xl + 0.4, xl + 0.7, -46, 46, jlz + 10, jlz + 18), C_ACCENT,
        "painted", 6, "shell", E_JLID)
    jink = _text_px("WellSense", 10.0, xl + 0.4, 0, jlz - 1)
    jink += _text_px("WELL LEVEL  ·  4 TO 20 mA  ·  24 V LOOP", 3.6, xl + 0.4, 0, jlz - 12)
    add("WellSense label print", jink, C_DARK, "paper", 6, "shell", E_JLID)

    # interface board behind the window (off-the-shelf modules, illustrative)
    E_BRD = e(E_JB, (110, 0, 0))
    bx_, by_, bz_ = P["board"]
    bzc = jcz + 10
    xcar0, xpcb = jcx - bx_ / 2, jcx + bx_ / 2 - 1.6
    carrier = _bx(xcar0, xpcb, -by_ / 2 - 4, by_ / 2 + 4, bzc - bz_ / 2 - 4, bzc + bz_ / 2 + 4)
    add("Interface board carrier plate", carrier, C_DARK, "plastic", 7, "internal", E_BRD)
    pcb = _bx(xpcb, xpcb + 1.6, -by_ / 2, by_ / 2, bzc - bz_ / 2, bzc + bz_ / 2)
    add("Interface board PCB", pcb, C_PCB, "plastic", 7, "internal", E_BRD)
    xf = xpcb + 1.6
    boost = _bx(xf, xf + 1.2, -30, -2, bzc + 8, bzc + 40)                      # boost module board
    adc = _bx(xf, xf + 1.2, 4, 30, bzc + 14, bzc + 38)                         # ADC module board
    add("Boost and ADC module boards", boost + adc, C_MODULE, "plastic", 7, "internal", E_BRD)
    parts_ = _xcyl(xf + 1.2 + 3.0, -16, bzc + 24, 5.5, 6.0)                    # boost inductor
    parts_ += _bx(xf + 1.2, xf + 3.2, 10, 22, bzc + 22, bzc + 30)              # ADC chip
    parts_ += _bx(xf, xf + 2.0, -26, -18, bzc - 8, bzc - 2)                    # TVS
    parts_ += _bx(xf, xf + 2.0, -4, 4, bzc - 10, bzc + 2)                      # regulator
    add("Interface board components", parts_, C_CHIP, "plastic", 7, "internal", E_BRD)
    shunt = _bx(xf, xf + 2.5, 8, 24, bzc - 12, bzc - 6)
    add("150 ohm precision shunt", shunt, "#2F5D8A", "painted", 7, "internal", E_BRD)
    term = _bx(xf, xf + 9, -28, 28, bzc - 36, bzc - 24)
    for k in range(6):
        term -= _xcyl(xf + 9, -23 + 9.2 * k, bzc - 30, 2.0, 3.0)
    add("Interface board terminal block", term, C_TERM, "plastic", 7, "internal", E_BRD)
    add("Interface board power light (lit)", _bx(xf, xf + 1.4, 26, 30, bzc + 30, bzc + 34), C_LED_G,
        "emissive", 7, "internal", E_BRD)

    # glands, conduit hub and desiccant breather
    tg = _hex_z(jcx, -20, jb1 + 3.0, 19.0, 6.0) + _zc(jcx, -20, jb1 + 6, jb1 + 16, 8.5)
    tg = _fillet_try(tg, _fmax(tg, Axis.Z), [2.5, 1.5])
    add("Junction box cable gland", tg, C_BLACK, "plastic", 6, "shell", e(E_JB, (0, 0, 70)))
    hub = _hex_z(jcx + 20, 0, jb0 - 5.0, 30.0, 10.0) - _zc(jcx + 20, 0, jb0 - 12, jb0 + 1, P["conduit_od"] / 2)
    add("Conduit hub (galvanized)", hub, C_GALV, "metal", 14, "shell", e(E_JB, (0, 0, -60)))
    br, bl = P["breather"]
    bxx, byy = jcx - 20, 35.0
    E_BR = e(E_JB, (0, 0, -110))
    bfit = _hex_z(bxx, byy, jb0 - 4, 16.0, 8.0) + _zc(bxx, byy, jb0 - 12, jb0 - 8, br)
    add("Breather fitting", bfit, C_BLACK, "plastic", 6, "shell", E_BR)
    bclr = _zc(bxx, byy, jb0 - bl + 8, jb0 - 12, br) - _zc(bxx, byy, jb0 - bl + 9, jb0 - 13, br - 1.5)
    add("Breather body (clear)", bclr, C_WINDOW, "clear", 6, "shell", E_BR)
    gel = _zc(bxx, byy, jb0 - bl + 9, jb0 - 22, br - 1.6)
    add("Silica gel (orange, indicating)", gel, C_GEL, "plastic", 6, "shell", E_BR)
    bend = _zc(bxx, byy, jb0 - bl, jb0 - bl + 8, br)
    bend = _fillet_try(bend, _fmin(bend, Axis.Z), [3.0, 2.0])
    for k in range(6):
        a = 2 * math.pi * k / 6
        bend -= _box(bxx + (br - 1) * math.cos(a), byy + (br - 1) * math.sin(a), jb0 - bl + 5, 2.5, 2.5, 4.0)
    add("Breather end cap", bend, C_BLACK, "plastic", 6, "shell", E_BR)

    # junction box band clamp and barometric sensor clamp (model.py clamp heights, render layout)
    cl = []
    for zc_ in P["clamp_z"]:
        z = zc_ + dz
        band = _zc(px, 0, z - 6, z + 6, po + 3) - _zc(px, 0, z - 7, z + 7, po)
        band += _bx(px - 8, px + 8, -po - 10, -po + 2, z - 7, z + 7)
        cl.append(band)
    add("Stainless band clamps", _union(cl), C_STEEL, "metal", 10, "shell", (0, 0, 0))

    # ============================================================ barometric sensor (BOM 9)
    brr, bll, bzz = P["baro"]
    bzz += dz
    bxc = px - po - brr - 4
    E_BARO = (-120, 0, 0)
    stack = []
    n = 4
    pitch = (bll - 12) / n
    for k in range(n):
        zk = bzz - bll / 2 + 4 + k * pitch
        stack.append(_zc(bxc, 0, zk, zk + 2.6, brr))
    core = _zc(bxc, 0, bzz - bll / 2, bzz + bll / 2 - 8, brr - 7)
    top = _zc(bxc, 0, bzz + bll / 2 - 8, bzz + bll / 2, brr)
    top = _fillet_try(top, _fmax(top, Axis.Z), [3.0, 2.0])
    add("Barometric sensor housing (louvered)", _union(stack + [core, top]), C_WHITE, "plastic", 9, "shell",
        E_BARO)
    arm = _bx(bxc + brr - 2, px - po + 1, -6, 6, bzz + bll / 2 - 8, bzz + bll / 2 - 2)
    arm += _bx(px - po - 3, px - po + 1, -10, 10, bzz + 4, bzz + bll / 2 - 2)
    add("Barometric sensor bracket", arm, C_ALU2, "metal", 9, "shell", E_BARO)
    add("Barometric sensor accent ring", _zc(bxc, 0, bzz - bll / 2 + 0.8, bzz - bll / 2 + 2.2, brr + 0.3)
        - _zc(bxc, 0, bzz - bll / 2, bzz - bll / 2 + 3, brr - 1), C_ACCENT, "painted", 9, "shell", E_BARO)

    # ============================================================ lead: junction box to FieldNode port 1
    x1 = px + P["fnd_port_x"][0]
    lead = _swept([(jcx, -20, jb1 + 14), (jcx, -20, jb1 + 60), (jcx, -45, z0 - 150),
                   (x1, yp, z0 - 90), (x1, yp, z0 - 56)], 3.0, 18.0)
    add("Sensor lead to FieldNode port 1", lead, C_CABLE, "rubber", 2, "shell", (0, -40, 150))
    plug = _zc(x1, yp, z0 - 58, z0 - 22, 8.0)
    plug = _fillet_try(plug, _fmin(plug, Axis.Z), [3.0, 2.0])
    for k in range(10):
        a = 2 * math.pi * k / 10
        plug -= _box(x1 + 8 * math.cos(a), yp + 8 * math.sin(a), z0 - 30, 1.2, 1.2, 12.0)
    add("M12 plug, port 1", plug, C_BLACK, "plastic", 2, "shell", e(E_DOWN, (0, 0, -40)))

    # ============================================================ wellhead: seal plate (BOM 4)
    sr = D["seal_d"] / 2
    E_SEAL = (0, 0, 160)
    halves = []
    plate_ = _zc(0, 0, st + 2.5, seal_top, sr)
    plate_ = _fillet_try(plate_, _fmax(plate_, Axis.Z), [4.0, 2.5])
    plate_ -= _zc(rx, 0, st, seal_top + 1, rr + 1)
    plate_ -= _zc(tx, 0, st, seal_top + 1, to + 0.5)
    plate_ -= _box(0, 0, (st + seal_top) / 2, 2 * sr + 4, 1.2, 60)             # split line
    for k in range(4):
        a = math.radians(45 + 90 * k)
        plate_ -= _zc(sr * 0.78 * math.cos(a), sr * 0.78 * math.sin(a), seal_top - 1.5, seal_top + 1, 6.5)
    add("Wellhead seal plate (split)", plate_, C_ACCENT, "painted", 4, "accessory", E_SEAL)
    sgk = _zc(0, 0, st, st + 2.5, sr - 1.5) - _zc(0, 0, st - 1, st + 3.5, P["casing_id"] / 2 - 2)
    sgk -= _zc(rx, 0, st - 1, st + 4, rr + 1)
    sgk -= _zc(tx, 0, st - 1, st + 4, to + 0.5)
    add("Seal plate gasket (EPDM)", sgk, C_BLACK, "rubber", 4, "accessory", e(E_SEAL, (0, 0, -60)))
    bolts = []
    for k in range(4):
        a = math.radians(45 + 90 * k)
        x, y = sr * 0.78 * math.cos(a), sr * 0.78 * math.sin(a)
        b = _hex_z(x, y, seal_top + 1.5, 10.0, 5.0) + _zc(x, y, seal_top - 1.5, seal_top - 0.5, 8.0)
        bolts.append(b)
    add("Seal plate bolts (stainless)", _union(bolts), C_STEEL, "metal", 4, "accessory", e(E_SEAL, (0, 0, 90)))
    gl = []
    for (gx, r_in, r_out) in ((rx, rr + 1, rr + 8), (tx, to + 0.5, to + 7)):
        g = _zc(gx, 0, seal_top, seal_top + 12, r_out) - _zc(gx, 0, seal_top - 1, seal_top + 13, r_in)
        g = _fillet_try(g, _fmax(g, Axis.Z), [1.5, 1.0])
        nut = (_hex_z(gx, 0, seal_top + 16, 2 * r_out + 2, 8.0)
               - _zc(gx, 0, seal_top + 10, seal_top + 22, r_in))
        gl.append(g)
        gl.append(nut)
    add("Seal plate glands", _union(gl), C_BLACK, "rubber", 4, "accessory", e(E_SEAL, (0, 0, 60)))

    # ============================================================ tube cap and cable-grip hanger (BOM 5)
    cod, ch, god, gh = P["cap"]
    E_CAP = (0, 0, 250)
    tcap = _zc(tx, 0, P["tube_top"], P["tube_top"] + ch, cod / 2)
    tcap = _fillet_try(tcap, _fmax(tcap, Axis.Z), [4.0, 2.5])
    tcap -= _zc(tx, 0, P["tube_top"] - 1, P["tube_top"] + ch - 6, to)
    tcap -= _zc(tx, 0, P["tube_top"] + ch - 8, P["tube_top"] + ch + 1, god / 2 - 2)
    for k in range(12):
        a = 2 * math.pi * k / 12
        tcap -= _box(tx + cod / 2 * math.cos(a), cod / 2 * math.sin(a), P["tube_top"] + 18, 1.4, 1.4, 22)
    add("Tube cap (PVC)", tcap, C_PVC_CAP, "plastic", 5, "accessory", E_CAP)
    zg = P["tube_top"] + ch
    hang = _hex_z(tx, 0, zg + 5, 19.0, 10.0) + _zc(tx, 0, zg + 10, cap_top, god / 2)
    hang = _fillet_try(hang, _fmax(hang, Axis.Z), [2.0, 1.2])
    add("Cable-grip hanger (stainless)", hang, C_STEEL, "metal", 5, "accessory", e(E_CAP, (0, 0, 60)))

    # ============================================================ galvanized conduit (BOM 14)
    E_CON = (0, -180, 230)
    cr_ = P["conduit_od"] / 2
    cz = P["cable_z"]
    conduit = _swept([(tx, 0, cap_top + 16), (tx, 0, cz), (jcx + 20, 0, cz), (jcx + 20, 0, jb0 - 10)],
                     cr_, 42.0)
    add("Surface cable conduit (galvanized)", conduit, C_GALV, "metal", 14, "accessory", E_CON)
    cgl = _hex_z(tx, 0, cap_top + 6, 26.0, 12.0) - _zc(tx, 0, cap_top - 1, cap_top + 13, god / 2 - 1)
    cgl += _zc(tx, 0, cap_top + 12, cap_top + 20, cr_ + 2.5) - _zc(tx, 0, cap_top + 11, cap_top + 21, cr_ - 0.5)
    add("Conduit compression gland", cgl, C_GALV, "metal", 14, "accessory", e(E_CON, (0, 0, -60)))

    # ============================================================ access tube (BOM 3), end plug, probe (BOM 1)
    tb = DISP_TUBE_BOT
    tube = _zc(tx, 0, tb, P["tube_top"], to) - _zc(tx, 0, tb + 10, P["tube_top"] + 1, ti)
    sw, sl = P["slot"]
    nrow = P["slot_rows"]
    pitch = (P["slot_zone"] - 40) / nrow
    for k in range(nrow):
        zc_ = tb + 40 + pitch * (k + 0.5)
        for ang in (0, 90):
            tube -= Pos(tx, 0, zc_) * Rot(0, 0, ang + 45 * (k % 2)) * Box(2 * to + 4, sw, sl)
    tube -= notch
    E_TUBE = (230, 0, 1330)
    add("Access tube (PVC), slotted bottom section, cut away", tube & _bx(-2000, 2000, -2000, 2000, tb - 1, TUBE_SPLIT_Z),
        C_PVC, "plastic", 3, "accessory", E_TUBE)
    add("Access tube (PVC), upper section, cut away", tube & _bx(-2000, 2000, -2000, 2000, TUBE_SPLIT_Z, 2000),
        C_PVC, "plastic", 3, "context", (0, 0, 0))
    plug_ = _zc(tx, 0, tb - 12, tb + 26, to + 2.5) - _zc(tx, 0, tb, tb + 27, to)
    plug_ = _fillet_try(plug_, _fmin(plug_, Axis.Z), [4.0, 2.0])
    plug_ -= notch
    add("Access tube end plug", plug_, C_PVC_CAP, "plastic", 3, "accessory", (230, 0, 1180))

    pr, pl = P["probe"][0] / 2, P["probe"][1]
    pb = tb + P["probe_gap"]
    ptp = pb + pl
    E_PRB = (320, -40, 1350)
    nose = _zc(tx, 0, pb, pb + 8, pr - 4) + _zc(tx, 0, pb + 8, pb + 34, pr)
    nose = _fillet_try(nose, _fmin(nose, Axis.Z), [2.5, 1.5])
    for k in range(6):
        a = 2 * math.pi * k / 6
        nose -= _box(tx + pr * math.cos(a), pr * math.sin(a), pb + 21, 3.0, 3.0, 12.0)
    add("Transducer nose guard (acetal)", nose, C_BLACK, "plastic", 1, "accessory", E_PRB)
    pbody = _zc(tx, 0, pb + 34, ptp - 22, pr)
    add("Pressure transducer body (316 stainless)", pbody, C_STEEL, "metal", 1, "accessory", E_PRB)
    band = _zc(tx, 0, ptp - 50, ptp - 38, pr + 0.3)
    add("Transducer band", band, C_ACCENT, "painted", 1, "accessory", E_PRB)
    relief = Pos(tx, 0, ptp - 11) * Cone(pr, P["cable_d"] / 2 + 1.2, 22)
    add("Transducer cable strain relief", relief, C_DARK, "rubber", 1, "accessory", E_PRB)
    add("Vented cable (in the access tube), lower", _zc(tx, 0, ptp - 1, ptp + CABLE_STUB, P["cable_d"] / 2),
        C_CABLE, "rubber", 2, "accessory", E_PRB)
    add("Vented cable (in the access tube), upper", _zc(tx, 0, ptp + CABLE_STUB, P["tube_top"] + ch - 6, P["cable_d"] / 2),
        C_CABLE, "rubber", 2, "context", (0, 0, 0))

    # ============================================================ context: ground, apron, casing, riser, water
    x0, x1, y0, y1 = BLOCK
    holes = _zc(0, 0, DISP_BOT - 10, 10, P["casing_od"] / 2) + _zc(px, 0, -P["embed"] - 10, 10, P["footing_d"] / 2)
    dry = _bx(x0, x1, y0, y1, DISP_WATER, 0) - holes - notch
    wet = _bx(x0, x1, y0, y1, DISP_BOT, DISP_WATER) - holes - notch
    add("Ground, unsaturated soil (section)", dry, C_SOIL, "rubber", None, "context", (0, 0, 0))
    add("Ground, saturated aquifer (section)", wet, C_AQUIFER, "rubber", None, "context", (0, 0, 0))
    apron = _zc(0, 0, 0, P["apron"][1], APRON_D / 2) - _zc(0, 0, -1, 200, P["casing_od"] / 2 + 1)
    apron = _fillet_try(apron, _fmax(apron, Axis.Z), [8.0, 4.0])
    apron -= _notch(P["apron"][1] + 1)
    add("Existing concrete apron (section)", apron, C_CONCRETE, "rubber", None, "context", (0, 0, 0))
    casing = _zc(0, 0, DISP_BOT, st, P["casing_od"] / 2) - _zc(0, 0, DISP_BOT - 1, st + 1, P["casing_id"] / 2)
    casing -= _notch(P["apron"][1] + 1)
    add("Existing steel casing, 150 mm (section)", casing, C_CASING, "painted", None, "context", (0, 0, 0))
    riser = _swept([(rx, 0, DISP_BOT), (rx, 0, st + 150), (rx, 240, st + 150), (rx, 240, P["apron"][1] - 5)], rr, 45.0)
    riser += _zc(rx, 240, st + 52, st + 70, rr + 5)
    add("Existing pump riser (not in kit)", riser, C_RISER, "metal", None, "context", (0, 0, 0))
    water = (_zc(0, 0, DISP_BOT + 2, DISP_WATER, P["casing_id"] / 2 - 0.5)
             - _zc(rx, 0, DISP_BOT, DISP_WATER + 5, rr + 0.5)
             - _zc(tx, 0, DISP_BOT, DISP_WATER + 5, to + 0.5))
    water += _zc(tx, 0, tb + 11, DISP_WATER, ti - 0.5) - _zc(tx, 0, pb - 1, DISP_WATER + 5, pr + 0.5)
    water -= notch
    add("Well water (static level shown)", water, C_WATER, "clear", None, "context", (0, 0, 0))

    # exploded view: the logger on its upper post section moves as a group beside the wellhead
    for p in out:
        if p["group"] in ("shell", "internal"):
            p["explode"] = tuple(a + b for a, b in zip(p["explode"], E_LOGGER))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:48s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
