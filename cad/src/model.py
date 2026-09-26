"""WellSense parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    wellsense-assembly.step / .stl   wellhead, access tube and probe in the existing well, post,
                                      junction box and the FieldNode core (borehole shortened)
    wellsense-wellhead.step / .stl   seal plate, tube cap and hanger, top of the access tube
    wellsense-probe.step / .stl      transducer, slotted bottom of the access tube, end plug
    wellsense-post.step / .stl       post and footing, junction box, interface board, barometric
                                      sensor and the FieldNode core massing

Axes: the well axis is the Z axis (x = y = 0), Z is up with the ground at z = 0. The existing
riser is off center toward -X and the access tube toward +X. The post stands on -X; the FieldNode
core on it faces -Y, as in the FieldNode model. Main dimensions and interfaces only; not
fabrication detail; not for fabrication.

The borehole is shortened for display: the model shows the wellhead, a short length of casing
and the probe zone. The real design case (probe 30 m below the wellhead, to 60 m) is carried
by the DESIGN parameters, which docs/04-calcs/sizing.py (WLS-CAL-001) uses for loads, cable and
cost. The same PARAMS feed the drawing WLS-DWG-001 (cad/src/sheets.py) and the concept media
(cad/src/concept_media.py).
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # existing well (context, not in the BOM): 150 mm casing (6 in), 450 mm stick-up, apron
    "casing_id": 150.0, "casing_od": 168.0, "stickup": 450.0, "casing_bot": -2600.0,
    "apron": (1200.0, 100.0),                  # diameter, thickness
    "riser_x": -30.0, "riser_od": 42.2,        # 1-1/4 in drop pipe, off center
    "pump": (98.0, 500.0), "pump_top": -2100.0,  # 4 in submersible pump, diameter and length
    "water_z": -1100.0,                        # static water level (display)
    # 3 access tube: 1 in Sch 40 PVC (33.4 x 26.6 mm), slotted over the bottom 500 mm, end plug
    "tube_x": 40.0, "tube_od": 33.4, "tube_id": 26.6, "tube_top": 560.0, "tube_bot": -1950.0,
    "slot": (3.0, 60.0), "slot_rows": 4, "slot_zone": 500.0,
    # 1 transducer body (diameter, length); gap between the probe tip and the end plug
    "probe": (24.0, 170.0), "probe_gap": 50.0,
    # 2 vented cable diameter; route height above the wellhead
    "cable_d": 7.0, "cable_z": 720.0,
    # 4 split seal plate (thickness, overhang past the casing OD)
    "seal_t": 25.0, "seal_over": 16.0,
    # 5 tube cap and cable-grip hanger (cap OD, cap height, grip OD, grip height)
    "cap": (44.0, 45.0, 16.0, 30.0),
    # 10 post: 1-1/2 in galvanized pipe 48.3 x 3.2, height above ground, embedment, footing diameter
    "post_x": -750.0, "post_od": 48.3, "post_wall": 3.2, "post_h": 2100.0, "embed": 600.0,
    "footing_d": 300.0, "clamp_z": (1300.0, 1450.0),
    # 6 junction box (X x Y x Z) on the +X face of the post, center height; 7 interface board inside
    "jbox": (90.0, 120.0, 160.0), "jbox_z": 1250.0, "board": (10.0, 70.0, 90.0),
    "breather": (20.0, 60.0),                  # desiccant breather under the box (radius, length)
    # 9 barometric sensor housing on the -X face of the post (radius, length, center height)
    "baro": (20.0, 50.0, 1450.0),
    # 8 FieldNode core, key dimensions copied from the FieldNode model (FND-DWG-001)
    "fnd_enc": (150.0, 90.0, 200.0), "fnd_z0": 1750.0, "fnd_plate": (180.0, 320.0, 3.0),
    "fnd_plate_y0": -42.0, "fnd_panel": (290.0, 200.0, 17.0), "fnd_tilt": 40.0,
    "fnd_panel_c": (-115.0, 385.0), "fnd_port_x": (-52.0, -22.0), "fnd_ant_x": 58.0,
    "fnd_whip": (10.0, 190.0),
}

# Design case for the calculations (the real well, not the display model)
DESIGN = {
    "probe_depth_m": 30.0,        # probe below the measuring point (top of casing), design case
    "probe_depth_max_m": 60.0,    # R2
    "range_m": 10.0,              # D3: 0 to 10 m of water
    "surface_run_m": 2.0,         # cable from the tube cap to the junction box
    "tube_extra_m": 0.5,          # access tube below the probe (slotted zone and plug)
}

BOM = {  # model key: (BOM line, name, color)
    "probe": (1, "Pressure transducer, vented, 4 to 20 mA", "#0F766E"),
    "cable": (2, "Vented cable with desiccant end", "#111827"),
    "tube": (3, "Access tube, 25 mm PVC, slotted", "#E5E7EB"),
    "seal": (4, "Wellhead seal plate and glands", "#2563EB"),
    "cap": (5, "Tube cap and cable hanger", "#D4A017"),
    "jbox": (6, "Junction box with desiccant breather", "#94A3B8"),
    "board": (7, "4 to 20 mA interface board with 24 V boost", "#16A34A"),
    "fieldnode": (8, "FieldNode core (enclosure, panel, radio)", "#115E59"),
    "baro": (9, "Barometric reference sensor", "#7C3AED"),
    "post": (10, "Mounting post and clamps", "#A16207"),
    "footing": (13, "Post footing, concrete", "#C9C5BC"),
}
CONTEXT = {  # existing well, grey, no BOM number
    "casing": ("Existing casing, 150 mm (not in kit)", "#9CA3AF"),
    "apron": ("Existing concrete apron", "#C9C5BC"),
    "pump": ("Existing pump and riser (not in kit)", "#6B7280"),
    "water": ("Well water (static level shown)", "#60A5FA"),
}


def derived(p=PARAMS):
    """Dimensions the calc note and the drawing quote, computed from PARAMS."""
    pl, pbody = p["probe"]
    probe_bot = p["tube_bot"] + p["probe_gap"]
    ew, ed, eh = p["fnd_enc"]
    t = math.radians(p["fnd_tilt"])
    pcy, pcz = p["fnd_panel_c"][0], p["fnd_z0"] + p["fnd_panel_c"][1]
    half = p["fnd_panel"][1] / 2
    enc_back = p["fnd_plate_y0"] - p["fnd_plate"][2]
    riser_edge = p["riser_x"] + p["riser_od"] / 2
    tube_in = p["tube_x"] - p["tube_od"] / 2
    return {
        "casing_top": p["stickup"], "seal_top": p["stickup"] + p["seal_t"],
        "seal_d": p["casing_od"] + 2 * p["seal_over"],
        "probe_bot": probe_bot, "probe_top": probe_bot + pbody,
        "probe_clear_radial": (p["tube_id"] - pl) / 2,
        "tube_to_riser": tube_in - riser_edge,
        "tube_to_casing": p["casing_id"] / 2 - (p["tube_x"] + p["tube_od"] / 2),
        "head_display": p["water_z"] - probe_bot,
        "enc_back": enc_back, "enc_front": enc_back - ed, "enc_yc": enc_back - ed / 2,
        "enc_bot": p["fnd_z0"], "enc_top": p["fnd_z0"] + eh,
        "panel_high_z": pcz + half * math.sin(t) + p["fnd_panel"][2] / 2 * math.cos(t),
        "overall_h": pcz + half * math.sin(t) + p["fnd_panel"][2] / 2 * math.cos(t),
        "cap_top": p["tube_top"] + p["cap"][1] + p["cap"][3],
        "post_len": p["post_h"] + p["embed"],
        "jbox_x": p["post_x"] + p["post_od"] / 2 + p["jbox"][0] / 2,
        "well_to_post": -p["post_x"],
    }


# ------------------------------------------------------------------ geometry helpers
def cyl(r, z0, z1, x=0.0, y=0.0):
    from build123d import Cylinder, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def box(cx, cy, cz, dx, dy, dz):
    from build123d import Box, Pos
    return Pos(cx, cy, cz) * Box(dx, dy, dz)


def tube(a, b, r):
    from build123d import Plane, Solid, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def polyline_tube(points, r):
    shape = None
    for a, b in zip(points, points[1:]):
        seg = tube(a, b, r)
        shape = seg if shape is None else shape + seg
    return shape


# ------------------------------------------------------------------ parts
def build_parts(p=PARAMS):
    """Return {key: shape} for the WellSense parts and the grey context parts."""
    from build123d import Pos, Rot, Box
    D = derived(p)
    s = {}
    cr = p["casing_id"] / 2
    # existing well (context)
    s["casing"] = cyl(p["casing_od"] / 2, p["casing_bot"], p["stickup"]) - cyl(cr, p["casing_bot"] - 1, p["stickup"] + 1)
    ad, at = p["apron"]
    s["apron"] = cyl(ad / 2, 0, at) - cyl(p["casing_od"] / 2 + 1, -1, at + 1)
    pd, plen = p["pump"]
    rx, rr = p["riser_x"], p["riser_od"] / 2
    pump = cyl(pd / 2, p["pump_top"] - plen, p["pump_top"], x=rx + 5)
    riser = cyl(rr, p["pump_top"], p["stickup"] + 170, x=rx)
    disch = tube((rx, 0, p["stickup"] + 150), (rx, 520, p["stickup"] + 150), rr) + cyl(rr, p["stickup"] - 70, p["stickup"] + 170, x=rx, y=520)
    s["pump"] = pump + riser + disch
    tx, to, ti = p["tube_x"], p["tube_od"] / 2, p["tube_id"] / 2
    s["water"] = (cyl(cr - 0.5, p["casing_bot"] + 5, p["water_z"])
                  - cyl(pd / 2 + 1, p["pump_top"] - plen - 5, p["pump_top"] + 1, x=rx + 5)
                  - cyl(rr + 1, p["pump_top"], p["water_z"] + 5, x=rx)
                  - cyl(to + 0.5, p["tube_bot"] - 5, p["water_z"] + 5, x=tx))

    # 3 access tube with slots over the bottom zone and an end plug
    t = cyl(to, p["tube_bot"], p["tube_top"], x=tx) - cyl(ti, p["tube_bot"] + 10, p["tube_top"] + 1, x=tx)
    sw, sl = p["slot"]
    n = p["slot_rows"]
    pitch = (p["slot_zone"] - 40) / n
    for k in range(n):
        zc = p["tube_bot"] + 40 + pitch * (k + 0.5)
        for ang in (0, 90):
            t = t - Pos(tx, 0, zc) * Rot(0, 0, ang + 45 * (k % 2)) * Box(2 * to + 4, sw, sl)
    s["tube"] = t

    # 1 transducer
    pr, pl = p["probe"][0] / 2, p["probe"][1]
    s["probe"] = cyl(pr, D["probe_bot"] + 8, D["probe_top"], x=tx) + cyl(pr - 4, D["probe_bot"], D["probe_bot"] + 8, x=tx)

    # 4 seal plate with glands for the riser and the tube
    sr = D["seal_d"] / 2
    s["seal"] = (cyl(sr, p["stickup"], D["seal_top"]) - cyl(rr + 1, p["stickup"] - 1, D["seal_top"] + 1, x=rx)
                 - cyl(to + 0.5, p["stickup"] - 1, D["seal_top"] + 1, x=tx)
                 + (cyl(rr + 8, D["seal_top"], D["seal_top"] + 20, x=rx) - cyl(rr + 1, D["seal_top"] - 1, D["seal_top"] + 21, x=rx))
                 + (cyl(to + 7, D["seal_top"], D["seal_top"] + 20, x=tx) - cyl(to + 0.5, D["seal_top"] - 1, D["seal_top"] + 21, x=tx)))

    # 5 tube cap and cable-grip hanger
    cod, ch, god, gh = p["cap"]
    s["cap"] = cyl(cod / 2, p["tube_top"], p["tube_top"] + ch, x=tx) + cyl(god / 2, p["tube_top"] + ch, D["cap_top"], x=tx)

    # 10 post with two band clamps, 13 footing
    px, po = p["post_x"], p["post_od"] / 2
    post = cyl(po, -p["embed"], p["post_h"], x=px) - cyl(po - p["post_wall"], -p["embed"] + 10, p["post_h"] + 1, x=px)
    for zc in p["clamp_z"]:
        post = post + (cyl(po + 3, zc - 6, zc + 6, x=px) - cyl(po, zc - 7, zc + 7, x=px))
    s["post"] = post
    s["footing"] = cyl(p["footing_d"] / 2, -p["embed"], -50, x=px) - cyl(po, -p["embed"] - 1, -49, x=px)

    # 6 junction box and breather, 7 board inside
    jx, jy, jz = p["jbox"]
    jcx, jcz = D["jbox_x"], p["jbox_z"]
    br, bl = p["breather"]
    s["jbox"] = box(jcx, 0, jcz, jx, jy, jz) + cyl(br, jcz - jz / 2 - bl, jcz - jz / 2, x=jcx - 20, y=35)
    bx, by, bz = p["board"]
    s["board"] = box(jcx, 0, jcz + 10, bx, by, bz)

    # 9 barometric sensor housing, -X face of the post
    brr, bll, bz0 = p["baro"]
    s["baro"] = cyl(brr, bz0 - bll / 2, bz0 + bll / 2, x=px - po - brr - 4)

    # 8 FieldNode core massing: back plate, enclosure, ports, whip, tilted panel as a hood
    ew, ed, eh = p["fnd_enc"]
    z0 = p["fnd_z0"]
    pw, ph, pt = p["fnd_plate"]
    plate = box(px, p["fnd_plate_y0"] - pt / 2, z0 - 40 + ph / 2, pw, pt, ph)
    enc = box(px, D["enc_yc"], z0 + eh / 2, ew, ed, eh)
    ports = None
    for dx in p["fnd_port_x"]:
        c = cyl(11, z0 - 20, z0, x=px + dx, y=D["enc_yc"])
        ports = c if ports is None else ports + c
    wd, wl = p["fnd_whip"]
    whip = cyl(wd / 2, z0 - 20 - wl, z0, x=px + p["fnd_ant_x"], y=D["enc_yc"])
    pnw, pnl, pnt = p["fnd_panel"]
    pcy, pcz = p["fnd_panel_c"][0], z0 + p["fnd_panel_c"][1]
    panel = Pos(px, pcy, pcz) * Rot(-p["fnd_tilt"], 0, 0) * Box(pnw, pnl, pnt)
    legs = (tube((px - 80, enc_back_y(p), z0 + 260), (px - 80, pcy + 60, pcz - 40), 6)
            + tube((px + 80, enc_back_y(p), z0 + 260), (px + 80, pcy + 60, pcz - 40), 6))
    s["fieldnode"] = plate + enc + ports + whip + panel + legs

    # 2 vented cable: probe up the tube, out of the hanger, across to the box, box to FieldNode port 1
    cz = p["cable_z"]
    run = [(tx, 0, D["probe_top"]), (tx, 0, D["cap_top"] + 30), (tx - 40, 0, cz),
           (jcx + 20, 0, cz), (jcx + 20, 0, jcz - jz / 2)]
    lead = [(jcx, -20, jcz + jz / 2), (jcx, -45, z0 - 150),
            (px + p["fnd_port_x"][0], D["enc_yc"], z0 - 45), (px + p["fnd_port_x"][0], D["enc_yc"], z0 - 20)]
    s["cable"] = polyline_tube(run, p["cable_d"] / 2) + polyline_tube(lead, 3.0)
    return s


def enc_back_y(p):
    return p["fnd_plate_y0"] - p["fnd_plate"][2] - 1


def assembly(p=PARAMS, context=True):
    from build123d import Compound
    s = build_parts(p)
    keys = [k for k in s if context or k not in CONTEXT]
    return Compound(children=[s[k] for k in keys if k != "water"])


def subset(keys, p=PARAMS, clip=None):
    from build123d import Compound
    s = build_parts(p)
    shapes = []
    for k in keys:
        sh = s[k]
        if clip is not None:
            sh = sh & clip
        if sh is not None and sh.volume > 1e-6:
            shapes.append(sh)
    return Compound(children=shapes)


if __name__ == "__main__":
    from build123d import export_step, export_stl
    P, D = PARAMS, derived()
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    head_clip = box(P["tube_x"] / 2, 0, (P["stickup"] - 300 + D["cap_top"]) / 2 + 10, 260, 260, D["cap_top"] - P["stickup"] + 320)
    probe_clip = box(P["tube_x"], 0, P["tube_bot"] + 350, 80, 80, 700)
    sets = {
        "wellsense-assembly": assembly(),
        "wellsense-wellhead": subset(["seal", "cap", "tube"], clip=head_clip),
        "wellsense-probe": subset(["probe", "tube"], clip=probe_clip),
        "wellsense-post": subset(["post", "footing", "jbox", "board", "baro", "fieldnode"]),
    }
    for name, shape in sets.items():
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm, volume {shape.volume / 1e6:.3f} L")
    print(f"probe radial clearance in tube {D['probe_clear_radial']:.1f} mm; tube to riser {D['tube_to_riser']:.1f} mm; "
          f"tube to casing {D['tube_to_casing']:.1f} mm; overall height {D['overall_h']:.0f} mm")
