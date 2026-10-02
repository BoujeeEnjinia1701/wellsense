"""WellSense parametric model (build123d), TRL 3, constructable design (WLS-DDR-004).

WLS-DDR-002 (2026-09-25): probe body 22 mm or less for the 1 in access tube, and a galvanized
conduit (BOM line 14) over the surface cable from the tube cap to the junction box.
WLS-DDR-004 (2026-10-02): design for construction. Every part can be made by its stated process
and fits and fastens to the parts next to it: split HDPE seal plate with a spigot ring, EPDM
wraps and a rim band; tube collar; drilled access tube with an end cap; drilled tube cap with a
cross bolt and a cable support grip; flexible conduit tail; bent rigid conduit on saddles;
junction box plate with V-blocks and band clamps; lugs, entries and an internal plate in the
junction box; barometric housing on the plate; FieldNode lead with an M12 plug; the FieldNode
core as built to FND-BLD-001 (geometry vendored from the FieldNode model).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks
Exports:
    wellsense-assembly.step / .stl   the whole installation on the mock-up well (borehole shortened)
    wellsense-wellhead.step / .stl   seal plate, collar, tube cap, flexible tail, top of the tube
    wellsense-probe.step / .stl      transducer, drilled bottom of the access tube, end cap
    wellsense-post.step / .stl       post and footing, junction box on its plate, barometric
                                      sensor, conduit, FieldNode lead and the FieldNode core

Axes: the well axis is the Z axis (x = y = 0), Z is up with the ground at z = 0. The existing
riser is off center toward -X and the access tube toward +X. The post stands on -X; the FieldNode
core on it faces -Y, as in the FieldNode model, and the junction box faces +X, toward the well.

The borehole is shortened for display: the model shows the wellhead, a short length of casing
and the probe zone. The real design case (probe 30 m below the wellhead, to 60 m) is carried by
the DESIGN parameters, which docs/04-calcs/sizing.py (WLS-CAL-001) uses for loads, cable and cost.
The same PARAMS feed the drawing WLS-DWG-001 (cad/src/sheets.py), the build plan pictures
(cad/src/build_plan_media.py) and the concept media (cad/src/concept_media.py).
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDOR = HERE.parents[0] / "vendor"

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # existing well (context, not in the BOM): 150 mm casing (6 in), 450 mm stick-up, apron
    "casing_id": 150.0, "casing_od": 168.0, "stickup": 450.0, "casing_bot": -2600.0,
    "apron": (1200.0, 100.0),                  # diameter, thickness
    "riser_x": -30.0, "riser_od": 42.2,        # 1-1/4 in drop pipe, off center
    "pump": (98.0, 500.0), "pump_top": -2100.0,  # 4 in submersible pump, diameter and length
    "pump_cable": (7.0, 12.0),                 # pump power cable: x on the split line, diameter
    "water_z": -1100.0,                        # static water level (display)
    # 3 access tube: 1 in Sch 40 PVC (33.4 x 26.6 mm), drilled over the bottom 500 mm, end cap
    "tube_x": 40.0, "tube_od": 33.4, "tube_id": 26.6, "tube_top": 560.0, "tube_bot": -1950.0,
    "slot_zone": 500.0,
    "holes": (8.0, 50.0, 40.0),                # drilled hole dia, ring pitch, first ring above the tube end
    "endcap": (42.2, 22.0, 5.0),               # 1 in slip cap: OD, socket depth, end thickness
    # 1 transducer body (diameter, length); gap between the probe tip and the tube end
    "probe": (22.0, 170.0), "probe_gap": 50.0,   # 22 mm maximum body (WLS-DDR-002)
    # 2 vented cable diameter; route height of the conduit above the ground
    "cable_d": 7.0, "cable_z": 720.0,
    # service loop coiled in the junction box (coil radius, bundle radius, turns), for the 1 m lift
    "coil": (45.0, 9.0, 4),
    # 14 surface conduit: 1/2 in galvanized rigid conduit OD and bore, bend radius; flexible tail
    #   OD and bore; rigid end above the well (x); saddle heights
    "conduit_od": 21.3, "conduit_id": 15.8, "bend_r": 100.0, "flex": (21.5, 16.0), "rigid_x0": -140.0,
    "saddle_z": (960.0, 1090.0),
    # 4 split seal plate: HDPE thickness, diameter; spigot ring OD, ID and depth; EPDM gasket
    #   thickness and OD; EPDM wrap thickness (squeezed); hole diameters for riser, pump cable, tube
    "seal_t": 20.0, "seal_d": 200.0, "spigot": (148.0, 128.0, 10.0), "gasket": (3.0, 184.0),
    "wrap": 2.0, "seal_holes": (46.2, 16.0, 37.4),
    "rim_band": (12.0, 0.8),                   # worm-drive band round the plate rim: width, thickness
    "collar": (50.0, 14.0),                    # split shaft collar on the tube above the plate: OD, width
    # 5 tube cap (1 in slip cap OD, socket depth, head space, top thickness); conduit connector hole;
    #   cross bolt offset from the tube axis and height above the tube end
    "cap": (42.2, 22.0, 18.0, 5.0), "cap_hole": 22.5, "cross_bolt": (9.0, 9.0),
    # 10 post: 1-1/2 in galvanized pipe 48.3 x 3.2, height above ground, embedment, footing diameter
    "post_x": -750.0, "post_od": 48.3, "post_wall": 3.2, "post_h": 2100.0, "embed": 600.0,
    "footing_d": 300.0,
    # 10 junction box plate: width (Y) x height (Z) x thickness; rear face in front of the post axis;
    #   bottom and top heights; V-block size (W x depth x H), band, slot offset
    "jplate": (140.0, 530.0, 3.0), "jplate_x0": 42.0, "jplate_z0": 860.0,
    "vblock": (60.0, 33.0, 20.0), "band": (12.0, 0.8), "band_slot_y": 51.0,
    # 6 junction box: depth (X) x width (Y) x height (Z), lid depth, wall; centre height
    "jbox": (90.0, 120.0, 160.0), "jlid": 12.0, "jwall": 3.0, "jbox_z": 1250.0,
    "jlug": (44.0, 16.0, 4.0, 16.0),           # lug y centre, width, thickness, reach past the box
    # bottom-face entries: name: (distance forward of the box back face, y, hole dia, outside dia, length below)
    "jentries": {"hub": (22.0, 0.0, 22.0, 32.0, 20.0), "lead_gland": (22.0, 38.0, 16.0, 24.0, 22.0),
                 "breather": (62.0, 30.0, 20.0, 30.0, 45.0), "baro_gland": (62.0, -30.0, 12.0, 18.0, 18.0)},
    # 7 interface board: internal plate (Y x Z x t) on bosses 6 mm off the back wall
    "iplate": (100.0, 130.0, 3.0), "iboss": (40.0, 55.0, 6.0),
    "board": (10.0, 70.0, 90.0),
    # 9 barometric sensor housing on the plate: radius, length, y, centre height
    "baro": (18.0, 50.0, -45.0, 1040.0),
    # 8 FieldNode core (vendored from the FieldNode model, FND-DWG-001 Rev P3); key figures
    "fnd_enc": (150.0, 90.0, 200.0), "fnd_z0": 1750.0, "fnd_plate": (180.0, 320.0, 3.0),
    "fnd_plate_y0": -42.0, "fnd_panel": (290.0, 200.0, 17.0), "fnd_tilt": 40.0,
    "fnd_panel_c": (-115.0, 385.0), "fnd_port_x": (-54.0, -22.0), "fnd_port_y": -100.0,
    "fnd_port_bot": 1728.0, "fnd_ant_x": 30.0, "fnd_whip": (10.0, 190.0),
    # 15 FieldNode lead: cable diameter, M12 plug (dia, length)
    "lead": (6.0, (20.0, 45.0)),
    # kept for cad/src/product_model.py (appearance model, stale until re-rendered)
    "slot": (3.0, 60.0), "slot_rows": 4, "clamp_z": (880.0, 1370.0), "breather": (15.0, 45.0),
}

# Design case for the calculations (the real well, not the display model)
DESIGN = {
    "probe_depth_m": 30.0,        # probe below the measuring point (top of casing), design case
    "probe_depth_max_m": 60.0,    # R2
    "range_m": 10.0,              # D3: 0 to 10 m of water
    "surface_run_m": 2.7,         # cable from the tube top to its terminals, service loop included (derived()["surface_run"], 2.70 m)
    "tube_extra_m": 0.5,          # access tube below the probe (drilled zone and end cap)
}

BOM = {  # model key: (BOM line, name, color)
    "probe": (1, "Pressure transducer, vented, 4 to 20 mA", "#0F766E"),
    "cable": (2, "Vented cable with service loop", "#111827"),
    "tube": (3, "Access tube, 25 mm PVC, drilled, end cap", "#E5E7EB"),
    "seal": (4, "Split seal plate, gasket, wraps, rim band, collar", "#2563EB"),
    "cap": (5, "Tube cap, cross bolt, support grip", "#D4A017"),
    "jbox": (6, "Junction box, lugs, entries, breather", "#94A3B8"),
    "board": (7, "Interface board on its internal plate", "#16A34A"),
    "fieldnode": (8, "FieldNode core (built to FND-BLD-001)", "#115E59"),
    "baro": (9, "Barometric reference sensor and housing", "#7C3AED"),
    "post": (10, "Post, junction box plate, V-blocks, bands", "#A16207"),
    "footing": (13, "Post footing, concrete", "#C9C5BC"),
    "conduit": (14, "Conduit, flexible tail, saddles, hub", "#64748B"),
    "lead": (15, "FieldNode lead with M12 plug", "#374151"),
}
CONTEXT = {  # existing well, grey, no BOM number
    "casing": ("Existing casing, 150 mm (not in kit)", "#9CA3AF"),
    "apron": ("Existing concrete apron", "#C9C5BC"),
    "pump": ("Existing pump, riser and cable (not in kit)", "#6B7280"),
    "water": ("Well water (static level shown)", "#60A5FA"),
}


@dataclass
class Comp:
    """One component: a single made or bought piece (or a matched set of fixings)."""
    name: str
    shape: object
    bom: int | None
    kind: str          # "made", "bought", "fixing" or "context"
    group: str | None  # key in BOM or CONTEXT (build_parts groups components by it)


def derived(p=PARAMS):
    """Dimensions the calc note, the drawings and the build plan quote, computed from PARAMS."""
    pl, pbody = p["probe"]
    probe_bot = p["tube_bot"] + p["probe_gap"]
    ew, ed, eh = p["fnd_enc"]
    t = math.radians(p["fnd_tilt"])
    pcy, pcz = p["fnd_panel_c"][0], p["fnd_z0"] + p["fnd_panel_c"][1]
    half = p["fnd_panel"][1] / 2
    enc_back = p["fnd_plate_y0"] - p["fnd_plate"][2]
    riser_edge = p["riser_x"] + p["riser_od"] / 2
    tube_in = p["tube_x"] - p["tube_od"] / 2
    st = p["stickup"]
    g = p["gasket"][0]
    seal_bot = st + g
    seal_top = seal_bot + p["seal_t"]
    cod, csock, chead, ctop = p["cap"]
    cap_bot = p["tube_top"] - csock
    cap_top = p["tube_top"] + chead + ctop
    px = p["post_x"]
    jx0 = px + p["jplate_x0"]                    # rear face of the junction box plate
    jfront = jx0 + p["jplate"][2]                # front face (the box sits on it)
    jd, jw, jh = p["jbox"]
    jz = p["jbox_z"]
    out = {
        "casing_top": st, "seal_bot": seal_bot, "seal_top": seal_top, "seal_d": p["seal_d"],
        "probe_bot": probe_bot, "probe_top": probe_bot + pbody,
        "probe_clear_radial": (p["tube_id"] - pl) / 2,
        "tube_to_riser": tube_in - riser_edge,
        "tube_to_casing": p["casing_id"] / 2 - (p["tube_x"] + p["tube_od"] / 2),
        "head_display": p["water_z"] - probe_bot,
        "enc_back": enc_back, "enc_front": enc_back - ed, "enc_yc": enc_back - ed / 2,
        "enc_bot": p["fnd_z0"], "enc_top": p["fnd_z0"] + eh,
        "panel_rot_x": p["fnd_tilt"],
        "panel_high_z": pcz + half * math.sin(t) + p["fnd_panel"][2] / 2 * math.cos(t),
        "overall_h": pcz + half * math.sin(t) + p["fnd_panel"][2] / 2 * math.cos(t),
        "cap_bot": cap_bot, "cap_top": cap_top, "conn_top": cap_top + 20.0,
        "collar_bot": seal_top, "collar_top": seal_top + p["collar"][1],
        "post_len": p["post_h"] + p["embed"],
        "jplate_x0": jx0, "jplate_front": jfront,
        "jplate_z1": p["jplate_z0"] + p["jplate"][1],
        "jbox_back": jfront, "jbox_front": jfront + jd, "jbox_x": jfront + jd / 2,
        "jbox_bot": jz - jh / 2, "jbox_top": jz + jh / 2,
        "jband_z": (p["jplate_z0"] + 20.0, p["jplate_z0"] + p["jplate"][1] - 20.0),
        "vpoint": px + p["post_od"] / 2 * math.sqrt(2),     # x of the V's point (pole touches both faces)
        "well_to_post": -px,
    }
    out["hub_x"] = jfront + p["jentries"]["hub"][0]
    # cable and conduit route lengths (m), for the calc note
    r = p["bend_r"]
    hx = out["hub_x"]
    h_run = (p["rigid_x0"] - hx) - r
    v_run = (out["jbox_bot"] - p["jentries"]["hub"][4]) - p["cable_z"] - r
    out["rigid_len"] = (h_run + v_run + math.pi * r / 2) / 1000
    out["flex_len"] = 0.30
    coil_r, _, turns = p["coil"]
    out["coil_len"] = 2 * math.pi * coil_r * turns / 1000
    out["surface_run"] = ((cap_top - p["tube_top"]) / 1000 + 0.02 + out["flex_len"] + out["rigid_len"]
                          + 0.05 + out["coil_len"] + 0.25)
    return out


# ------------------------------------------------------------------ geometry helpers
def cyl(r, z0, z1, x=0.0, y=0.0):
    from build123d import Cylinder, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def xcyl(r, x0, x1, y, z):
    from build123d import Cylinder, Pos, Rot
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def ycyl(r, y0, y1, x, z):
    from build123d import Cylinder, Pos, Rot
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def box(cx, cy, cz, dx, dy, dz):
    from build123d import Box, Pos
    return Pos(cx, cy, cz) * Box(dx, dy, dz)


def bx(x0, x1, y0, y1, z0, z1):
    return box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, x1 - x0, y1 - y0, z1 - z0)


def ring(ro, ri, z0, z1, x=0.0, y=0.0):
    return cyl(ro, z0, z1, x, y) - cyl(ri, z0 - 1, z1 + 1, x, y)


def tube(a, b, r):
    from build123d import Plane, Solid, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def polyline_tube(points, r):
    """A flexible cable along points: straight runs with a ball at each bend."""
    from build123d import Pos, Sphere
    shape = None
    for a, b in zip(points, points[1:]):
        seg = tube(a, b, r)
        shape = seg if shape is None else shape + seg
    for q in points[1:-1]:
        shape = shape + Pos(*q) * Sphere(r)
    return shape


def swept_pipe(points, ro, ri=0.0, bend=0.0):
    """A pipe of outer radius ro (bore ri) along a polyline with bends of radius bend."""
    from build123d import Circle, FilletPolyline, Plane, Polyline, sweep
    path = FilletPolyline(*points, radius=bend) if bend > 0 and len(points) > 2 else Polyline(*points)
    e0 = path.edges()[0]
    pl = Plane(origin=e0.position_at(0), z_dir=e0.tangent_at(0))
    prof = pl * Circle(ro)
    if ri > 0:
        prof = prof - pl * Circle(ri)
    return sweep(prof, path)


def seg_box(a, b, w, h, z0):
    """A flat strip w wide (in plan) and h tall from point a to point b (x, y), starting at z0."""
    from build123d import Box, Pos, Rot
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    ang = math.degrees(math.atan2(dy, dx))
    return Pos((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, z0 + h / 2) * Rot(0, 0, ang) * Box(L, w, h)


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def vendored(name, dx=0.0):
    """FieldNode geometry exported from the FieldNode model (FND-DWG-001 Rev P3), moved to the post."""
    from build123d import Pos, import_step
    return Pos(dx, 0, 0) * import_step(str(VENDOR / f"fieldnode-{name}.step"))


# ------------------------------------------------------------------ the band clamp round the post
def band_clamp(p, zc, side=+1):
    """Band round the back of the post, through two slots in the junction box plate and across its
    front face. side=+1: the plate is on +X of the post."""
    px = p["post_x"]
    bw, bt = p["band"]
    D = derived(p)
    r = p["post_od"] / 2 + bt / 2                # band mid-line radius
    xf = D["jplate_front"] + bt / 2              # mid-line across the plate front
    xr = D["jplate_x0"]
    ys = p["band_slot_y"]
    parts = []
    z0 = zc - bw / 2
    for s in (+1, -1):
        S = (xr, s * ys)
        dx, dy = S[0] - px, S[1]
        d = math.hypot(dx, dy)
        a_s = math.atan2(dy, dx)
        a_t = a_s + s * math.acos(r / d)          # tangent point on the far side of the line to the slot
        T = (px + r * math.cos(a_t), r * math.sin(a_t))
        parts.append(seg_box(T, S, bt, bw, z0))
        parts.append(seg_box((xr - bt / 2, s * ys), (xf, s * ys), bt, bw, z0))
        if s > 0:
            a_top = a_t
        else:
            a_bot = a_t
    parts.append(seg_box((xf, -ys - bt / 2), (xf, ys + bt / 2), bt, bw, z0))
    # the arc round the back of the post, from the +y tangent point the long way to the -y one
    from build123d import Pos, Rot, Box
    arc = ring(p["post_od"] / 2 + bt, p["post_od"] / 2, z0, z0 + bw, x=px)
    span = 2 * math.pi - (a_top - a_bot)
    keep = None
    n = 24
    for i in range(n):
        a = a_top + span * (i + 0.5) / n
        w = Pos(px + 30 * math.cos(a), 30 * math.sin(a), zc) * Rot(0, 0, math.degrees(a)) * Box(60, 2 * 30 * math.tan(span / n / 2) + 0.6, bw + 2)
        keep = w if keep is None else keep + w
    parts.append(arc & keep)
    return fuse(parts)


def vblock(p, zc):
    """V-block behind the junction box plate: flat back on the plate, true 90 deg V on the post."""
    from build123d import Polygon, Plane, extrude
    D = derived(p)
    w, dep, h = p["vblock"]
    xr = D["jplate_x0"]
    xf = xr - dep
    xp = D["vpoint"]
    hw = xp - xf                                   # V half width at the front face (90 deg V)
    pts = [(xr, -w / 2), (xr, w / 2), (xf, w / 2), (xf, hw), (xp, 0.0), (xf, -hw), (xf, -w / 2)]
    face = Plane.XY.offset(zc - h / 2) * Polygon(*pts, align=None)
    blk = extrude(face, h)
    for s in (+1, -1):                             # tapped M4 holes from the plate side
        blk = blk - xcyl(1.65, xr - 14, xr + 1, s * 18.0, zc)
    return blk


# ------------------------------------------------------------------ components
def build_components(p=PARAMS):
    """Return {key: Comp} for every made, bought and fixing component, plus the grey context."""
    from build123d import Pos, Rot, Box, Sphere, Torus
    D = derived(p)
    C = {}

    def add(key, name, shape, bom, kind, group):
        C[key] = Comp(name, shape, bom, kind, group)

    # ---------------- existing well (context)
    cr = p["casing_id"] / 2
    st = p["stickup"]
    add("casing", "Existing casing", cyl(p["casing_od"] / 2, p["casing_bot"], st) - cyl(cr, p["casing_bot"] - 1, st + 1),
        None, "context", "casing")
    ad, at = p["apron"]
    add("apron", "Existing apron", cyl(ad / 2, 0, at) - cyl(p["casing_od"] / 2 + 1, -1, at + 1), None, "context", "apron")
    pd, plen = p["pump"]
    rx, rr = p["riser_x"], p["riser_od"] / 2
    pump = cyl(pd / 2, p["pump_top"] - plen, p["pump_top"], x=rx + 5)
    riser = cyl(rr, p["pump_top"], st + 170, x=rx)
    disch = tube((rx, 0, st + 150), (rx, 520, st + 150), rr) + cyl(rr, st - 70, st + 170, x=rx, y=520)
    cx_, cd_ = p["pump_cable"]
    pcable = cyl(cd_ / 2, p["pump_top"], st + 160, x=cx_) + tube((cx_, 0, st + 160), (cx_, 300, st + 160), cd_ / 2)
    add("pump", "Existing pump, riser and pump cable", pump + riser + disch + pcable, None, "context", "pump")
    tx, to, ti = p["tube_x"], p["tube_od"] / 2, p["tube_id"] / 2
    add("water", "Well water", cyl(cr - 0.5, p["casing_bot"] + 5, p["water_z"])
        - cyl(pd / 2 + 1, p["pump_top"] - plen - 5, p["pump_top"] + 1, x=rx + 5)
        - cyl(rr + 1, p["pump_top"], p["water_z"] + 5, x=rx)
        - cyl(cd_ / 2 + 1, p["pump_top"], p["water_z"] + 5, x=cx_)
        - cyl(p["endcap"][0] / 2 + 0.5, p["tube_bot"] - 10, p["water_z"] + 5, x=tx), None, "context", "water")

    # ---------------- 3 access tube, drilled at the bottom, with a slip end cap
    t = cyl(to, p["tube_bot"], p["tube_top"], x=tx) - cyl(ti, p["tube_bot"] - 1, p["tube_top"] + 1, x=tx)
    hd, hp, h0 = p["holes"]
    nring = int((p["slot_zone"] - h0) // hp) + 1
    for k in range(nring):
        zc = p["tube_bot"] + h0 + hp * k
        for ang in (0, 90):
            a = ang + 45 * (k % 2)
            t = t - Pos(tx, 0, zc) * Rot(0, 0, a) * Rot(0, 90, 0) * cyl(hd / 2, -to - 2, to + 2)
    add("tube", "Access tube, drilled", t, 3, "made", "tube")
    eod, esock, eend = p["endcap"]
    ec = cyl(eod / 2, p["tube_bot"] - eend, p["tube_bot"] + esock, x=tx) - cyl(to, p["tube_bot"], p["tube_bot"] + esock + 1, x=tx)
    ec = ec - cyl(hd / 2, p["tube_bot"] - eend - 1, p["tube_bot"] + 1, x=tx)        # drain hole
    add("endcap", "Tube end cap", ec, 3, "bought", "tube")

    # ---------------- 1 transducer
    pr, pl = p["probe"][0] / 2, p["probe"][1]
    add("probe", "Pressure transducer", cyl(pr, D["probe_bot"] + 8, D["probe_top"], x=tx)
        + cyl(pr - 4, D["probe_bot"], D["probe_bot"] + 8, x=tx), 1, "bought", "probe")

    # ---------------- 4 split seal plate on the casing
    g_t, g_od = p["gasket"]
    add("gasket", "EPDM gasket ring (cut once)", ring(g_od / 2, cr, st, st + g_t), 4, "made", "seal")
    sb, stp = D["seal_bot"], D["seal_top"]
    sr = p["seal_d"] / 2
    hr, hc, ht = p["seal_holes"]
    disc = cyl(sr, sb, stp) - cyl(hr / 2, sb - 1, stp + 1, x=rx) - cyl(hc / 2, sb - 1, stp + 1, x=cx_) - cyl(ht / 2, sb - 1, stp + 1, x=tx)
    spo, spi, spd = p["spigot"]
    sp = ring(spo / 2, spi / 2, sb - spd, sb)
    for s, key, nm in ((+1, "seal_a", "Seal plate half A (back, +Y)"), (-1, "seal_b", "Seal plate half B (front, -Y)")):
        half = bx(-sr - 1, sr + 1, 0 if s > 0 else -sr - 1, sr + 1 if s > 0 else 0, sb - spd - 1, stp + 1)
        add(key, nm, disc & half, 4, "made", "seal")
        add(f"spigot_{key[-1]}", f"Spigot half ring {key[-1].upper()}", sp & half, 4, "made", "seal")
    w = p["wrap"]
    wraps = (ring(hr / 2, rr, sb, stp, x=rx) + ring(hc / 2, cd_ / 2, sb, stp, x=cx_) + ring(ht / 2, to, sb, stp, x=tx))
    add("wraps", "EPDM wraps (riser, pump cable, tube)", wraps, 4, "made", "seal")
    rbw, rbt = p["rim_band"]
    zb = (sb + stp) / 2
    rim = ring(sr + rbt, sr, zb - rbw / 2, zb + rbw / 2) + bx(-9, 9, -sr - rbt - 9, -sr - rbt + 0.01, zb - rbw / 2 - 2, zb + rbw / 2 + 2)
    add("rim_band", "Rim band clamp", rim, 4, "bought", "seal")
    co, cw = p["collar"]
    add("collar", "Tube collar (split shaft collar)", ring(co / 2, to, stp, stp + cw, x=tx), 4, "bought", "seal")

    # ---------------- 5 tube cap with cross bolt and support grip
    cod, csock, chead, ctop = p["cap"]
    cap = (cyl(cod / 2, D["cap_bot"], D["cap_top"], x=tx) - cyl(to, D["cap_bot"] - 1, p["tube_top"], x=tx)
           - cyl(ti + 0.4, p["tube_top"] - 0.01, D["cap_top"] - ctop, x=tx) - cyl(p["cap_hole"] / 2, D["cap_top"] - ctop - 1, D["cap_top"] + 1, x=tx))
    bxo, bz = p["cross_bolt"]
    zcb = p["tube_top"] + bz
    cap = cap - ycyl(2.5, -cod, cod, tx + bxo, zcb)
    add("cap", "Tube cap, drilled", cap, 5, "made", "cap")
    bolt = ycyl(2.5, -cod / 2 - 4, cod / 2 + 4, tx + bxo, zcb)
    # the bolt's flats where it meets the cap wall stand for the head and nut, outside the cap
    bolt = bolt + ycyl(4.5, cod / 2 + 0.1, cod / 2 + 4, tx + bxo, zcb) + ycyl(4.5, -cod / 2 - 4, -cod / 2 - 0.1, tx + bxo, zcb)
    add("cross_bolt", "M5 cross bolt", bolt, 5, "fixing", "cap")
    cr_ = p["cable_d"] / 2
    grip = ring(cr_ + 1.5, cr_, p["tube_top"] - 70, p["tube_top"] - 10, x=tx)
    bail = (tube((tx + cr_ + 1.5, 0, p["tube_top"] - 12), (tx + bxo, 0, p["tube_top"] - 2), 1.2)
            + Pos(tx + bxo, 0, p["tube_top"] - 2) * Sphere(1.2) + tube((tx + bxo, 0, p["tube_top"] - 2), (tx + bxo, 0, zcb - 2.53), 1.2))
    add("grip", "Cable support grip", grip + bail, 5, "bought", "cap")

    # ---------------- 14 conduit: connector on the cap, flexible tail, rigid conduit, saddles, hub
    ct = D["cap_top"]
    conn = cyl(p["cap_hole"] / 2, ct - ctop, ct, x=tx) + cyl(13.0, ct, ct + 20, x=tx) + cyl(13.0, ct - ctop - 3, ct - ctop, x=tx)
    conn = conn - cyl(8.0, ct - ctop - 4, ct + 21, x=tx)
    add("connector", "Flexible conduit connector on the cap", conn, 14, "bought", "conduit")
    cz = p["cable_z"]
    x0 = p["rigid_x0"]
    fo, fi = p["flex"]
    flex_pts = [(tx, 0, ct + 20), (tx, 0, cz), (x0 + 30, 0, cz)]
    add("flex", "Flexible conduit tail", swept_pipe(flex_pts, fo / 2, fi / 2, bend=60.0), 14, "bought", "conduit")
    coup = ring(13.5, 8.0, 0, 30)
    add("coupling", "Flex-to-rigid connector", Pos(x0 + 15, 0, cz) * Rot(0, 90, 0) * Pos(0, 0, -15) * coup, 14, "bought", "conduit")
    hx = D["hub_x"]
    hub_e = p["jentries"]["hub"]
    zhub = D["jbox_bot"] - hub_e[4]
    rigid_pts = [(x0, 0, cz), (hx, 0, cz), (hx, 0, zhub)]
    add("conduit", "Rigid conduit, bent", swept_pipe(rigid_pts, p["conduit_od"] / 2, p["conduit_id"] / 2, bend=p["bend_r"]),
        14, "made", "conduit")
    jf = D["jplate_front"]
    sad = []
    ro = p["conduit_od"] / 2
    for zs in p["saddle_z"]:
        strap = ring(ro + 1.5, ro, zs - 10, zs + 10, x=hx) & bx(hx, hx + ro + 2, -ro - 2, ro + 2, zs - 11, zs + 11)
        spacer = bx(jf, hx - ro, -ro - 12, ro + 12, zs - 10, zs + 10)
        # the strap's feet sit on the spacer, which sits on the plate; the conduit sits in the spacer's face
        feet = bx(hx - ro, hx, -ro - 12, -ro - 1.5, zs - 10, zs + 10) + bx(hx - ro, hx, ro + 1.5, ro + 12, zs - 10, zs + 10)
        sad.append(strap + spacer + feet - cyl(ro, zs - 12, zs + 12, x=hx))
    add("saddles", "Conduit spacer saddles (2)", fuse(sad), 14, "bought", "conduit")

    # ---------------- 10 post, cap, footing, junction box plate, V-blocks, band clamps
    px, po = p["post_x"], p["post_od"] / 2
    post = cyl(po, -p["embed"], p["post_h"], x=px) - cyl(po - p["post_wall"], -p["embed"] + 10, p["post_h"] + 1, x=px)
    add("post", "Post, galvanized pipe", post, 10, "made", "post")
    add("post_cap", "Post top cap", cyl(po + 1.5, p["post_h"], p["post_h"] + 8, x=px) + cyl(po - p["post_wall"], p["post_h"] - 15, p["post_h"], x=px),
        10, "bought", "post")
    add("footing", "Post footing", cyl(p["footing_d"] / 2, -p["embed"], -50, x=px) - cyl(po, -p["embed"] - 1, -49, x=px), 13, "made", "footing")
    jw_, jh_, jt = p["jplate"]
    jx0 = D["jplate_x0"]
    z0j, z1j = p["jplate_z0"], D["jplate_z1"]
    jp = bx(jx0, jx0 + jt, -jw_ / 2, jw_ / 2, z0j, z1j)
    for zb_ in D["jband_z"]:
        for s in (+1, -1):
            jp = jp - bx(jx0 - 1, jx0 + jt + 1, s * p["band_slot_y"] - 1.5, s * p["band_slot_y"] + 1.5, zb_ - 7.5, zb_ + 7.5)
            jp = jp - xcyl(2.25, jx0 - 1, jx0 + jt + 1, s * 18.0, zb_)
    jd, jw, jh = p["jbox"]
    for zl in (D["jbox_top"] + p["jlug"][3] / 2, D["jbox_bot"] - p["jlug"][3] / 2):
        for s in (+1, -1):
            jp = jp - xcyl(2.75, jx0 - 1, jx0 + jt + 1, s * p["jlug"][0], zl)
    for zs in p["saddle_z"]:
        for s in (+1, -1):
            jp = jp - xcyl(2.75, jx0 - 1, jx0 + jt + 1, s * (ro + 6.75), zs)
    br, bl, by, bz_ = p["baro"]
    for zz in (bz_ - 22, bz_ + 22):
        jp = jp - xcyl(2.25, jx0 - 1, jx0 + jt + 1, by, zz)
    add("jplate", "Junction box plate", jp, 10, "made", "post")
    add("vblock_low", "Lower V-block", vblock(p, D["jband_z"][0]), 10, "made", "post")
    add("vblock_up", "Upper V-block", vblock(p, D["jband_z"][1]), 10, "made", "post")
    add("jbands", "Band clamps (2)", band_clamp(p, D["jband_z"][0]) + band_clamp(p, D["jband_z"][1]), 10, "bought", "post")

    # ---------------- 6 junction box: body, lid, lugs, bottom entries; 7 internal plate and modules
    jl, jwall = p["jlid"], p["jwall"]
    jb, jtop = D["jbox_bot"], D["jbox_top"]
    xb, xfr = D["jbox_back"], D["jbox_front"]
    body = bx(xb, xfr - jl, -jw / 2, jw / 2, jb, jtop) - bx(xb + jwall, xfr - jl + 1, -jw / 2 + jwall, jw / 2 - jwall, jb + jwall, jtop - jwall)
    ib = p["iboss"]
    jzc = p["jbox_z"]
    for sy in (+1, -1):
        for sz in (+1, -1):
            body = body + xcyl(4.0, xb + jwall - 0.01, xb + jwall + ib[2], sy * ib[0], jzc + sz * ib[1])
    ent = p["jentries"]
    for k, (u, v, hd_, od_, ln) in ent.items():
        body = body - cyl(hd_ / 2, jb - 1, jb + jwall + 1, x=xb + u, y=v)
    add("jbody", "Junction box body, drilled", body, 6, "made", "jbox")
    add("jlid", "Junction box lid", bx(xfr - jl, xfr, -jw / 2, jw / 2, jb, jtop), 6, "bought", "jbox")
    lw = p["jlug"]
    lugs = []
    for zl0, zl1 in ((jtop, jtop + lw[3]), (jb - lw[3], jb)):
        for s in (+1, -1):
            lg = bx(xb, xb + lw[2], s * lw[0] - lw[1] / 2, s * lw[0] + lw[1] / 2, zl0, zl1)
            lg = lg - xcyl(2.75, xb - 1, xb + lw[2] + 1, s * lw[0], (zl0 + zl1) / 2)
            lugs.append(lg)
    add("jlugs", "Junction box lugs (4)", fuse(lugs), 6, "bought", "jbox")
    lsc = []
    for zl in (jtop + lw[3] / 2, jb - lw[3] / 2):
        for s in (+1, -1):
            lsc.append(xcyl(2.5, jx0 - 0.01, xb + lw[2] + 5, s * lw[0], zl) + xcyl(4.5, jx0 - 3, jx0, s * lw[0], zl)
                       + xcyl(4.5, xb + lw[2], xb + lw[2] + 5, s * lw[0], zl))
    add("jlug_screws", "M5 lug screws and nyloc nuts", fuse(lsc), 6, "fixing", "jbox")
    ents = {}
    for k, (u, v, hd_, od_, ln) in ent.items():
        xx = xb + u
        outside = cyl(od_ / 2, jb - ln, jb, x=xx, y=v)
        thread = cyl(hd_ / 2, jb, jb + jwall, x=xx, y=v)
        nut = cyl(od_ / 2, jb + jwall, jb + jwall + 6, x=xx, y=v)
        shp = outside + thread + nut
        if k != "breather":
            bore = 8.0 if k == "hub" else (p["lead"][0] / 2 if k == "lead_gland" else 2.5)
            shp = shp - cyl(bore, jb - ln - 1, jb + jwall + 7, x=xx, y=v)
        ents[k] = shp
    add("hub", "Conduit hub", ents["hub"], 14, "bought", "conduit")
    add("glands", "Cable glands, M16 and M12", ents["lead_gland"] + ents["baro_gland"], 6, "bought", "jbox")
    add("breather", "Desiccant breather", ents["breather"], 6, "bought", "jbox")
    iw, ih, itk = p["iplate"]
    xi = xb + jwall + ib[2]
    ipl = bx(xi, xi + itk, -iw / 2, iw / 2, jzc - ih / 2, jzc + ih / 2)
    for sy in (+1, -1):
        for sz in (+1, -1):
            ipl = ipl - xcyl(2.25, xi - 1, xi + itk + 1, sy * ib[0], jzc + sz * ib[1])
    add("iplate", "Internal plate", ipl, 7, "made", "board")
    xm = xi + itk
    mods = {"boost": (-25.0, 1290.0, 21.0, 43.0, 20.0), "adc": (25.0, 1295.0, 18.0, 28.0, 14.0),
            "reg": (25.0, 1255.0, 20.0, 30.0, 16.0), "strip": (0.0, 1215.0, 70.0, 12.0, 20.0)}
    for k, (yc, zc, wy, hz, dx) in mods.items():
        add(f"mod_{k}", {"boost": "12 to 24 V boost module", "adc": "ADC and shunt module",
                         "reg": "3.3 V regulator and surge module", "strip": "Terminal strip"}[k],
            bx(xm, xm + dx, yc - wy / 2, yc + wy / 2, zc - hz / 2, zc + hz / 2), 7, "bought", "board")

    # ---------------- 9 barometric housing on the plate, its lead into the box
    flange = bx(jf, jf + 3, by - 20, by + 20, bz_ - 30, bz_ + 30)
    for zz in (bz_ - 22, bz_ + 22):
        flange = flange - xcyl(2.25, jf - 1, jf + 4, by, zz)
    hx_c = jf + 3 + br
    housing = cyl(br, bz_ - bl / 2, bz_ + bl / 2, x=hx_c, y=by)
    for k in range(4):
        housing = housing - cyl(br + 1, bz_ - bl / 2 + 8 + 9 * k, bz_ - bl / 2 + 11 + 9 * k, x=hx_c, y=by) + cyl(br - 3, bz_ - bl / 2 + 8 + 9 * k - 0.1, bz_ - bl / 2 + 11 + 9 * k + 0.1, x=hx_c, y=by)
    bg = ent["baro_gland"]
    blead = polyline_tube([(hx_c, by, bz_ + bl / 2), (hx_c, by, bz_ + bl / 2 + 30), (xb + bg[0], bg[1], jb - bg[4] - 25),
                           (xb + bg[0], bg[1], jb + jwall + 6)], 2.5)
    add("baro", "Barometric sensor housing and lead", flange + housing + blead, 9, "bought", "baro")

    # ---------------- 2 vented cable: probe, tube, cap, flexible tail, conduit, hub, service loop
    run = (swept_pipe([(tx, 0, D["probe_top"]), (tx, 0, cz), (x0, 0, cz)], cr_, bend=60.0)
           + swept_pipe([(x0, 0, cz), (hx, 0, cz), (hx, 0, jb + 10)], cr_, bend=p["bend_r"]))
    coil_r, coil_b, _ = p["coil"]
    xcoil = xfr - jl - coil_b - 4
    zcoil = jtop - jwall - coil_b - coil_r - 2
    coil = Pos(xcoil, 0, zcoil) * Rot(0, 90, 0) * Torus(coil_r, coil_b)
    tie = tube((hx, 0, jb + 10), (xcoil, 0, zcoil - coil_r), cr_) + Pos(hx, 0, jb + 10) * Sphere(cr_)
    add("cable", "Vented cable", run + tie + coil, 2, "bought", "cable")

    # ---------------- 8 FieldNode core (vendored) and 15 its lead
    add("fieldnode", "FieldNode core", vendored("node", px), 8, "made", "fieldnode")
    add("fnd_bands", "FieldNode band clamps", vendored("bands", px), 8, "bought", "fieldnode")
    ld, (pgd, pgl) = p["lead"]
    lg = ent["lead_gland"]
    xa, ya = px + p["fnd_port_x"][0], p["fnd_port_y"]
    pb = p["fnd_port_bot"]
    plug = cyl(pgd / 2, pb - pgl, pb, x=xa, y=ya)
    lead_pts = [(xb + lg[0], lg[1], jb + jwall + 6), (xb + lg[0], lg[1], jb - 70), (jx0 + 8, 85.0, jb - 75),
                (px + 22, 62.0, jb - 60), (px + 22, 62.0, pb - 100), (px - 20, 40.0, pb - 85), (px - 50, 10.0, pb - 80),
                (xa, ya, pb - 80), (xa, ya, pb - pgl)]
    add("lead", "FieldNode lead with M12 plug", polyline_tube(lead_pts, ld / 2) + plug, 15, "bought", "lead")
    return C


def build_parts(p=PARAMS):
    """Return {BOM or CONTEXT key: solid}, grouping components by BOM line."""
    C = build_components(p)
    out = {}
    for c in C.values():
        if c.group:
            out[c.group] = c.shape if c.group not in out else out[c.group] + c.shape
    return out


def assembly(p=PARAMS, context=True):
    from build123d import Compound
    C = build_components(p)
    keys = [k for k, c in C.items() if (context or c.kind != "context") and k != "water"]
    return Compound(children=[C[k].shape for k in keys])


def subset(keys, p=PARAMS, clip=None):
    from build123d import Compound
    C = build_components(p)
    shapes = []
    for k in keys:
        sh = C[k].shape
        if clip is not None:
            sh = sh & clip
        if sh is not None and sh.volume > 1e-6:
            shapes.append(sh)
    return Compound(children=shapes)


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch, and pairs that must stay apart by a clearance (mm). Returns a list of
    (description, overlap volume mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    S = lambda *ks: fuse([C[k].shape for k in ks])  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    # wellhead
    chk("Gasket on the casing top", S("gasket"), S("casing"), "touch")
    for h in ("a", "b"):
        chk(f"Seal plate half {h.upper()} on the gasket", S(f"seal_{h}"), S("gasket"), "touch")
        chk(f"Spigot half ring {h.upper()} under its plate half", S(f"spigot_{h}"), S(f"seal_{h}"), "touch")
        chk(f"Spigot half ring {h.upper()} inside the casing bore", S(f"spigot_{h}"), S("casing"), 0.5)
        chk(f"Spigot half ring {h.upper()} clear of the riser and pump cable", S(f"spigot_{h}"), S("pump"), 2.0)
        chk(f"Spigot half ring {h.upper()} clear of the access tube", S(f"spigot_{h}"), S("tube"), 2.0)
        chk(f"Rim band on plate half {h.upper()}", S("rim_band"), S(f"seal_{h}"), "touch")
        chk(f"Wraps squeezed by plate half {h.upper()}", S("wraps"), S(f"seal_{h}"), "touch")
    chk("Seal plate halves meet at the split", S("seal_a"), S("seal_b"), "touch")
    chk("Wraps on the riser and pump cable", S("wraps"), S("pump"), "touch")
    chk("Wrap on the access tube", S("wraps"), S("tube"), "touch")
    chk("Collar on the seal plate", S("collar"), S("seal_a", "seal_b"), "touch")
    chk("Collar on the access tube", S("collar"), S("tube"), "touch")
    chk("Collar clear of the pump cable", S("collar"), S("pump"), 1.0)
    chk("Access tube clear of the riser and pump cable", S("tube", "endcap"), S("pump"), 3.0)
    chk("Access tube clear of the casing wall", S("tube", "endcap"), S("casing"), 3.0)
    chk("End cap on the tube", S("endcap"), S("tube"), "touch")
    chk("Probe clear of the tube bore", S("probe"), S("tube"), 2.0)
    chk("Probe clear of the end cap", S("probe"), S("endcap"), 20.0)
    chk("Cap on the tube end", S("cap"), S("tube"), "touch")
    chk("Cap clear of the collar", S("cap"), S("collar"), 20.0)
    chk("Cross bolt through the cap", S("cross_bolt"), S("cap"), "touch")
    chk("Support grip on the cable", S("grip"), S("cable"), "touch")
    chk("Support grip bail on the cross bolt", S("grip"), S("cross_bolt"), "touch")
    chk("Support grip clear of the tube wall", S("grip"), S("tube"), 1.0)
    chk("Cable clear of the cross bolt", S("cable"), S("cross_bolt"), 1.0)
    chk("Connector in the cap", S("connector"), S("cap"), "touch")
    chk("Connector clear of the cross bolt", S("connector"), S("cross_bolt"), 1.0)
    chk("Flexible tail on the connector", S("flex"), S("connector"), "touch")
    chk("Flexible tail on the rigid connector", S("flex"), S("coupling"), "touch")
    chk("Rigid conduit in its connector", S("conduit"), S("coupling"), "touch")
    chk("Flexible tail clear of the riser and discharge", S("flex", "coupling"), S("pump"), 10.0)
    chk("Flexible tail clear of the seal plate and collar", S("flex"), S("seal_a", "seal_b", "collar"), 50.0)
    chk("Cable inside the conduit, tail and connector (no contact)", S("cable"), S("conduit", "flex", "connector", "coupling"), 0.5)
    chk("Cable clear of the tube bore", S("cable"), S("tube"), 5.0)
    # post and junction box plate
    pole = S("post")
    chk("Post in its footing", S("footing"), pole, "touch")
    chk("Post cap on the post", S("post_cap"), pole, "touch")
    for k in ("vblock_low", "vblock_up"):
        chk(f"{C[k].name} on the junction box plate", S(k), S("jplate"), "touch")
        chk(f"{C[k].name} on the post (both V faces)", S(k), pole, "touch")
        chk(f"{C[k].name} clear of the band", S(k), S("jbands"), 1.0)
    chk("Bands round the post", S("jbands"), pole, "touch")
    chk("Bands through the slots and across the plate front", S("jbands"), S("jplate"), "touch")
    chk("Plate clear of the post", S("jplate"), pole, 10.0)
    chk("Junction box body on the plate", S("jbody"), S("jplate"), "touch")
    chk("Lugs on the plate", S("jlugs"), S("jplate"), "touch")
    chk("Lugs against the box", S("jlugs"), S("jbody"), "touch")
    chk("Lid on the body", S("jlid"), S("jbody"), "touch")
    chk("Bands clear of the box and lugs", S("jbands"), S("jbody", "jlugs"), 5.0)
    chk("Internal plate on the bosses", S("iplate"), S("jbody"), "touch")
    for k in ("mod_boost", "mod_adc", "mod_reg", "mod_strip"):
        chk(f"{C[k].name} on the internal plate", S(k), S("iplate"), "touch")
        chk(f"{C[k].name} clear of the lid", S(k), S("jlid"), 5.0)
        chk(f"{C[k].name} clear of the service loop", S(k), S("cable"), 2.0)
    chk("Internal plate clear of the entry nuts", S("iplate"), S("hub", "glands", "breather"), 2.0)
    for k in ("hub", "glands", "breather"):
        chk(f"{C[k].name} in the box floor", S(k), S("jbody"), "touch")
    ents = ("hub", "glands", "breather")
    for i, a in enumerate(ents):
        for b_ in ents[i + 1:]:
            chk(f"{C[a].name} apart from {C[b_].name}", S(a), S(b_), 4.0)
    chk("Service loop clear of the lid", S("cable"), S("jlid"), 1.0)
    # conduit on the plate
    chk("Rigid conduit in the hub", S("conduit"), S("hub"), "touch")
    chk("Rigid conduit in the saddles", S("conduit"), S("saddles"), "touch")
    chk("Saddles on the plate", S("saddles"), S("jplate"), "touch")
    chk("Rigid conduit clear of the plate", S("conduit"), S("jplate"), 5.0)
    chk("Rigid conduit clear of the bands", S("conduit"), S("jbands"), 5.0)
    chk("Rigid conduit clear of the post", S("conduit"), pole, 20.0)
    chk("Barometric housing on the plate", S("baro"), S("jplate"), "touch")
    chk("Barometric lead into its gland", S("baro"), S("glands"), "touch")
    chk("Barometric housing clear of the conduit and saddles", S("baro"), S("conduit", "saddles"), 3.0)
    chk("Barometric housing clear of the bands", S("baro"), S("jbands"), 5.0)
    # FieldNode and its lead
    chk("FieldNode bands round the post", S("fnd_bands"), pole, "touch")
    chk("FieldNode V-blocks on the post", S("fieldnode"), pole, "touch")
    chk("FieldNode core clear of the junction box parts", S("fieldnode"), S("jplate", "jbody", "jlid", "jbands", "conduit"), 100.0)
    chk("Lead plug on FieldNode port A", S("lead"), S("fieldnode"), "touch")
    chk("Lead into its gland", S("lead"), S("glands"), "touch")
    chk("Lead clear of the post", S("lead"), pole, 2.0)
    chk("Lead clear of the plate, V-blocks and bands", S("lead"), S("jplate", "vblock_low", "vblock_up", "jbands"), 2.0)
    chk("Lead clear of the box and barometric parts", S("lead"), S("jbody", "jlid", "jlugs", "baro", "breather", "hub", "conduit"), 2.0)
    chk("Lead clear of the FieldNode bands", S("lead"), S("fnd_bands"), 2.0)
    chk("Post top cap clear of the FieldNode core", S("post_cap"), S("fieldnode"), 1.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:62s} overlap {v:9.3f} mm3  gap {gp:8.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import Compound, export_step, export_stl
    P, D = PARAMS, derived()
    out = HERE.parents[0]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    C = build_components()
    head = ["seal_a", "seal_b", "spigot_a", "spigot_b", "gasket", "wraps", "rim_band", "collar", "cap", "cross_bolt",
            "grip", "connector", "flex", "coupling"]
    head_clip = box(P["tube_x"] / 2, 0, (P["stickup"] - 300 + D["conn_top"]) / 2 + 10, 300, 300, D["conn_top"] - P["stickup"] + 340)
    probe_clip = box(P["tube_x"], 0, P["tube_bot"] + 350, 80, 80, 720)
    post_keys = ["post", "post_cap", "footing", "jplate", "vblock_low", "vblock_up", "jbands", "jbody", "jlid", "jlugs",
                 "jlug_screws", "hub", "glands", "breather", "iplate", "mod_boost", "mod_adc", "mod_reg", "mod_strip", "baro",
                 "conduit", "saddles", "lead", "fieldnode", "fnd_bands"]
    sets = {
        "wellsense-assembly": assembly(),
        "wellsense-wellhead": Compound(children=[s for s in (C[k].shape & head_clip for k in head + ["tube"]) if s is not None and s.volume > 1e-6]),
        "wellsense-probe": Compound(children=[s for s in (C[k].shape & probe_clip for k in ("probe", "tube", "endcap", "cable")) if s is not None and s.volume > 1e-6]),
        "wellsense-post": Compound(children=[C[k].shape for k in post_keys]),
    }
    for name, shape in sets.items():
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm, volume {shape.volume / 1e6:.3f} L")
    print(f"probe radial clearance in tube {D['probe_clear_radial']:.1f} mm; tube to riser {D['tube_to_riser']:.1f} mm; "
          f"tube to casing {D['tube_to_casing']:.1f} mm; overall height {D['overall_h']:.0f} mm; "
          f"rigid conduit {D['rigid_len']:.2f} m; surface cable run {D['surface_run']:.2f} m")
