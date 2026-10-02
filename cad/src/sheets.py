"""WellSense general arrangement sheet WLS-DWG-001, Rev P5 (TRL 3; P2 applies WLS-DDR-002; P3 applies WLS-DDR-003;
P5 shows the constructable design of WLS-DDR-004).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/WLS-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions come from PARAMS and derived(), so they
follow any parameter change. The main views show the installation above z = -700 mm (post
footing, wellhead and top of the casing); a detail shows the probe zone at the bottom of the
access tube. The borehole between them is not drawn. The concept blueprint in media/ is
WLS-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import DESIGN as DS, PARAMS as P, box, build_parts, derived  # noqa: E402

DATE = "2026-09-25"
DATE_P3 = "2026-09-27"
DATE_P5 = "2026-10-02"
Z_CUT = -700.0


def safe_project_views(part, workdir, names=("front", "top", "right", "iso"), line_weight=0.35):
    """Same views as drawing.project_views, but edge by edge, so a degenerate edge from the
    hidden-line projection is skipped instead of stopping the export."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name in names:
        origin, up = setups[name]
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected {len(names)} views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab, dl = 14, 12, 11
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab + dl)) / 2 + dl
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    from build123d import Compound
    D = derived(P)
    s_parts = build_parts(P)
    work = ROOT / "cad" / "drawings" / "_views"
    clip = box(0, -125, (Z_CUT + 3000) / 2, 6000, 550, 3000 - Z_CUT)     # y -400..150: leaves out the pump discharge
    keep = [k for k in s_parts if k not in ("water", "apron")]
    surf = Compound(children=[sh for sh in ((s_parts[k] & clip) for k in keep) if sh is not None and sh.volume > 1e-6])
    views = safe_project_views(surf, work)
    lo = box(P["tube_x"], 0, P["tube_bot"] + 300, 120, 120, 600)
    probe = Compound(children=[s_parts[k] & lo for k in ("tube", "probe")])
    pviews = safe_project_views(probe, work / "probe", names=("front",))
    bb = surf.bounding_box()
    s = Sheet(project="WellSense", title="General arrangement", dwg_no="WLS-DWG-001", rev="P5",
              author="Amish Chadha", date=DATE_P5, scale=None, theme="technical",
              material="Bought-in parts per bom/bom.csv; borehole not drawn below -700. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "22 mm probe; conduit 14 added (WLS-DDR-002)", DATE, "AC"),
                         ("P3", "FieldNode panel tilt corrected to face -Y (WLS-DDR-003)", DATE_P3, "AC"),
                         ("P4", "Layout and labels tidied", DATE_P3, "AC"),
                         ("P5", "Constructable design (WLS-DDR-004)", DATE_P5, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    px, tx = P["post_x"], P["tube_x"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zg = Z(0)
    L.append(f'<line x1="{x - 4:.2f}" y1="{zg:.2f}" x2="{x + w + 4:.2f}" y2="{zg:.2f}" stroke="{INK}" stroke-width="0.35"/>')
    L.append(_t(X(-560), zg - 1, "GROUND", 2.0, 600, MUTED, "start"))
    for zz, txt in ((-260, "EXISTING WELL"), (-330, "(NOT IN BOM)"), (-560, "BOREHOLE CONTINUES"), (-630, "PROBE 30 m (DESIGN)")):
        L.append(_t(X(-110), Z(zz), txt, 1.7, 600, MUTED, "end"))
    xl = X(bb.min.X) - 12
    for i, (zz, label) in enumerate(((D["enc_bot"], f"{D['enc_bot']:.0f} FieldNode base"),
                                     (P["post_h"], f"{P['post_h']:.0f} post top"),
                                     (D["overall_h"], f"{D['overall_h']:,.0f} overall"))):
        xd = xl - 6 * i
        L += [ext(X(px), Z(zz), xd - 1, Z(zz))]
        L += dim_v(xd, Z(zz), zg, label)
    L += dim_v(X(px) - 14, zg, Z(-P["embed"]), f"{P['embed']:.0f}")
    xr = X(bb.max.X) + 5
    L += [ext(X(tx), Z(D["cap_top"]), xr + 1, Z(D["cap_top"])), ext(X(0), Z(P["stickup"]), xr + 1, Z(P["stickup"]))]
    L += dim_v(xr, Z(D["cap_top"]), zg, f"{D['cap_top']:.0f} cap", side=3.2)
    L += dim_v(xr + 6, Z(P["stickup"]), zg, f"{P['stickup']:.0f} casing", side=3.2)
    zt = -430
    L += dim_h(X(px), X(0), Z(zt), f"{D['well_to_post']:.0f}")
    L += leader(X(D["jbox_x"]), Z(P["jbox_z"]), X(D["jbox_x"]) + 18, Z(P["jbox_z"] + 60), "6 JUNCTION BOX, 7 BOARD")
    L += leader(X(tx), Z(P["tube_top"] + 20), X(tx) + 9, Z(P["tube_top"] + 380), "5 CAP")
    L.append(_t(X(tx) + 10, Z(P["tube_top"] + 380) + 4.6, "AND GRIP", 2.1, 400, INK, "start"))
    L += leader(X(-D["seal_d"] / 2 + 10), Z(D["seal_top"] - 10), X(-D["seal_d"] / 2) - 8, Z(D["seal_top"] + 110), "4 SEAL PLATE", "end")
    L += leader(X(px + 40), Z(D["enc_bot"] + 100), X(px) + 30, Z(D["enc_bot"] + 560), "8 FIELDNODE CORE (FND-BLD-001)")
    L += leader(X(-300), Z(P["cable_z"]), X(-300) + 6, Z(P["cable_z"] + 330), "14 CONDUIT AND TAIL")

    # top view (from +Z)
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k

    # right view: seal plate diameter
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    L += dim_h(Yr(-D["seal_d"] / 2), Yr(D["seal_d"] / 2), Zr(D["seal_top"] + 330), "")
    L.append(_t(Yr(D["seal_d"] / 2) + 1.5, Zr(D["seal_top"] + 330) + 0.8, f"{D['seal_d']:.0f}", 2.3, 400, INK, "start", mono=True))
    L += [ext(Yr(-D["seal_d"] / 2), Zr(D["seal_top"]), Yr(-D["seal_d"] / 2), Zr(D["seal_top"] + 340)),
          ext(Yr(D["seal_d"] / 2), Zr(D["seal_top"]), Yr(D["seal_d"] / 2), Zr(D["seal_top"] + 340))]

    s._layers += L
    s.add_svg(views["iso"], 276, 47, 66, 90, label="Isometric view", sublabel="Not to scale")
    # probe detail at 1:6
    pk = 1 / 6
    pb = probe.bounding_box()
    dx, dy = 368, 44
    s.add_svg(pviews["front"], dx, dy, scale=pk, label=None)
    pw_, ph_ = _viewbox(pviews["front"].read_text())[2:]
    Zp = lambda mz: dy + ph_ * pk - (mz - pb.min.Z) * pk
    Xp = lambda mx: dx + (mx - pb.min.X) * pk
    s._layers += dim_v(Xp(pb.min.X) - 4, Zp(D["probe_top"]), Zp(D["probe_bot"]), f"{P['probe'][1]:.0f}")
    s._layers += dim_v(Xp(pb.min.X) - 10, Zp(P["tube_bot"] + P["slot_zone"]), Zp(P["tube_bot"]), f"{P['slot_zone']:.0f} drilled")
    s._layers.append(_t(dx + pw_ * pk / 2, dy + ph_ * pk + 6, "DETAIL A: PROBE ZONE", 2.8, 600, INK, "middle"))
    s._layers.append(_t(dx + pw_ * pk / 2, dy + ph_ * pk + 10, "Scale 1:6; bottom of tube", 2.2, 400, MUTED, "middle"))
    s._layers += leader(Xp(pb.max.X) - 2, Zp(D["probe_top"] - 60), Xp(pb.max.X) + 5, Zp(D["probe_top"] - 60), "1 PROBE")
    s._layers += leader(Xp(pb.max.X) - 1, Zp(D["probe_top"] + 120), Xp(pb.max.X) + 5, Zp(D["probe_top"] + 120), "3 TUBE")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Casing {P['casing_id']:.0f} bore (existing), stick-up {P['stickup']:.0f}. Seal plate: split {D['seal_d']:.0f} x {P['seal_t']:.0f} HDPE, rim band",
        f"Access tube 1 in Sch 40 PVC {P['tube_od']} x {P['tube_id']}; {D['tube_to_riser']:.0f} clear of riser",
        f"Probe {P['probe'][0]:.0f} max x {P['probe'][1]:.0f}, {D['probe_clear_radial']:.1f} radial clearance; {DS['probe_depth_m']:.0f} m below casing top (to {DS['probe_depth_max_m']:.0f} m)",
        f"Post 48.3 x 3.2 galv., {P['post_h']:.0f} above ground, {P['embed']:.0f} in {P['footing_d']:.0f} footing",
        f"Junction box {P['jbox'][0]:.0f} x {P['jbox'][1]:.0f} x {P['jbox'][2]:.0f}, center {P['jbox_z']:.0f}, on a plate with V-blocks",
        f"FieldNode core per FND-DWG-001; base {D['enc_bot']:.0f}; sensor port A (I2C, 12 V rail)",
        "Loop 4 to 20 mA from a 24 V boost; 150 ohm shunt (WLS-CAL-001)",
        f"Cable in 1/2 in galv. conduit ({P['conduit_od']} OD) and a flexible tail to the cap",
        "Third-angle; front view from -Y, FieldNode and panel face the equator; well on the Z axis",
    ], x=276, y=161, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "WLS-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
