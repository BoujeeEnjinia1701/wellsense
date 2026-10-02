"""WellSense prototype build plan pictures (WLS-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
A single step, joint or sheet can be drawn on its own, for example `steps:3` or `sheets:105`.
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/WLS-DWG-101 to 109        making sketches for the made and drilled components
    docs/05-build-plan/*-holes.png         full-size hole layouts (matplotlib)
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
The borehole is shortened: the access tube, cable and casing are drawn with their middle left out.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, bx  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
REPO = "github.com/BoujeeEnjinia1701/wellsense"
D = derived(P)
C = build_components(P)

COL = {"post": "#A16207", "footing": "#C9C5BC", "jplate": "#A8A29E", "vblock": "#57534E", "band": "#9CA3AF",
       "jbody": "#D1D5DB", "jlid": "#E5E7EB", "lugs": "#374151", "entries": "#1F2937", "breather": "#C2410C",
       "iplate": "#94A3B8", "boost": "#16A34A", "adc": "#0F766E", "reg": "#15803D", "strip": "#7C3AED",
       "baro": "#7C3AED", "fieldnode": "#115E59", "lead": "#374151", "conduit": "#64748B", "saddle": "#1D4ED8",
       "tube": "#E5E7EB", "endcap": "#CBD5E1", "gasket": "#111827", "seal": "#2563EB", "spigot": "#1E40AF",
       "wraps": "#0F172A", "rim": "#9CA3AF", "collar": "#B45309", "cable": "#111827", "probe": "#0F766E",
       "cap": "#D4A017", "bolt": "#111827", "grip": "#6B7280", "flex": "#475569", "conn": "#1F2937",
       "casing": "#9CA3AF", "pump": "#6B7280"}

# borehole break: keep z above Z_HI and below Z_LO, move the lower piece up by LIFT
Z_HI, Z_LO = 0.0, -1650.0
LIFT = (Z_HI - Z_LO) - 350.0


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def S(*ks):
    return _fuse([C[k].shape for k in ks])


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def short(shape):
    """The shape with the middle of the borehole left out (z between Z_LO and Z_HI)."""
    import build123d as b
    big = 4000
    hi = shape & b.Pos(0, 0, Z_HI + big / 2) * b.Box(big * 2, big * 2, big)
    lo = shape & b.Pos(0, 0, Z_LO - big / 2) * b.Box(big * 2, big * 2, big)
    pieces = []
    for s, dz in ((hi, 0.0), (lo, LIFT)):
        try:
            if s is not None and s.volume > 1e-6:
                pieces.append(b.Pos(0, 0, dz) * s)
        except Exception:
            pass
    return _fuse(pieces)


def post_stub(z0=760.0, z1=1500.0):
    return part("Post (part)", S("post", "post_cap") & bx(-1000, 0, -100, 100, z0, z1), COL["post"])


def well_ctx(half=True, zmin=-500.0):
    """Grey context: the top of the casing (cut open on the viewer's side) and the riser and pump cable."""
    import build123d as b
    keep = b.Pos(0, 0, (zmin + 2000) / 2) * b.Box(600, 600, 2000 - zmin)
    cas = C["casing"].shape & keep
    if half:
        cas = cas & b.Pos(0, 200, 0) * b.Box(600, 400, 6000)
    pump = C["pump"].shape & keep
    return [part("Casing (cut open)", cas, COL["casing"], alpha=1.0), part("Riser and pump cable", pump, COL["pump"])]


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "post": part("Post with top cap", S("post", "post_cap"), COL["post"]),
        "footing": part("Concrete footing", C["footing"].shape, COL["footing"]),
        "jplate": part("Junction box plate", C["jplate"].shape, COL["jplate"]),
        "vblocks": part("V-blocks (2)", S("vblock_low", "vblock_up"), COL["vblock"]),
        "jbody": part("Junction box body, drilled", C["jbody"].shape, COL["jbody"]),
        "entries": part("Hub, glands and breather", S("hub", "glands", "breather"), COL["entries"]),
        "lugs": part("Box lugs (4) and M5 screws", S("jlugs", "jlug_screws"), COL["lugs"]),
        "iboard": part("Internal plate with the interface modules", S("iplate", "mod_boost", "mod_adc", "mod_reg", "mod_strip"), "#16A34A"),
        "jlid": part("Junction box lid", C["jlid"].shape, COL["jlid"]),
        "baro": part("Barometric sensor housing and lead", C["baro"].shape, COL["baro"]),
        "jbands": part("Band clamps (2)", C["jbands"].shape, COL["band"]),
        "fieldnode": part("FieldNode core with its bands", S("fieldnode", "fnd_bands"), COL["fieldnode"]),
        "lead": part("FieldNode lead with M12 plug", C["lead"].shape, COL["lead"]),
        "conduit": part("Rigid conduit and saddles", S("conduit", "saddles"), COL["conduit"]),
        "tube": part("Access tube with end cap (shortened)", short(S("tube", "endcap")), COL["tube"]),
        "gasket": part("EPDM gasket ring", C["gasket"].shape, COL["gasket"]),
        "seal": part("Seal plate halves with spigot rings", S("seal_a", "seal_b", "spigot_a", "spigot_b"), COL["seal"]),
        "wraps": part("EPDM wraps", C["wraps"].shape, COL["wraps"]),
        "rim": part("Rim band clamp", C["rim_band"].shape, COL["rim"]),
        "collar": part("Tube collar", C["collar"].shape, COL["collar"]),
        "cable": part("Vented cable (shortened)", short(C["cable"].shape), COL["cable"]),
        "probe": part("Pressure transducer", short(C["probe"].shape), COL["probe"]),
        "cap": part("Tube cap, cross bolt and support grip", S("cap", "cross_bolt", "grip"), COL["cap"]),
        "flex": part("Flexible tail and connectors", S("connector", "flex", "coupling"), COL["flex"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    import build123d as b
    M = made()
    PB = 650.0      # post break: the post between 50 and 700 mm above ground is left out
    big = 5000
    post = S("post", "post_cap")
    lo = post & b.Pos(0, 0, 50 - big / 2) * b.Box(big, big, big)
    hi = b.Pos(0, 0, -PB) * (post & b.Pos(0, 0, 700 + big / 2) * b.Box(big, big, big))
    M["post"] = part("Post with top cap (middle left out)", lo + hi, COL["post"])
    up = -PB        # everything on the post moves down with the break
    off = {"post": (0, 0, 0), "footing": (0, 0, -150), "jplate": (230, 0, up), "vblocks": (-110, 0, up),
           "jbody": (420, 0, up), "entries": (420, 0, up - 170), "lugs": (330, 0, up + 150), "iboard": (580, 0, up + 40),
           "jlid": (740, 0, up), "baro": (330, 0, up - 230), "jbands": (-260, 0, up), "fieldnode": (0, 0, up + 450),
           "lead": (-200, 220, up), "conduit": (380, 0, up - 330),
           "tube": (500, 0, -150), "gasket": (500, 0, 450), "seal": (500, 0, 570), "wraps": (700, 0, 690),
           "rim": (500, 0, 790), "collar": (700, 0, 890), "cable": (900, 0, -150), "probe": (1050, 0, -150),
           "cap": (500, 0, 990), "flex": (700, 0, 1090)}
    parts = []
    for k, p in M.items():
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "WellSense prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Left: the post, junction box and FieldNode core. Right: the wellhead kit. Post, tube and cable drawn with their middles left out",
                       elev=12, azim=-75, size=(12, 9.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    M = made()
    base = dict(project="WellSense", date=DATE)
    out = []
    px = P["post_x"]
    want = lambda n: only is None or n in only  # noqa: E731
    jx0, jf = D["jplate_x0"], D["jplate_front"]
    jw, jh, jt = P["jplate"]

    if want(101):
        out.append(bv.component_sheet(
            Part("Post", S("post", "post_cap"), COL["post"]), [M["footing"], M["jplate"], M["fieldnode"], M["jbands"]],
            dwg_no="WLS-DWG-101", title="WellSense post: making sketch", material="Galvanized steel pipe 48.3 x 3.2 mm (1-1/2 in), 2.7 m",
            view_shape=b.Pos(-px, 0, 0) * S("post", "post_cap"), inset_view=(18, -40),
            notes=["Cut the pipe to 2,700 mm, square; file the ends; paint each cut end",
                   "  with zinc-rich paint so the galvanizing is made good.",
                   "Push the plastic cap into the top end.",
                   "Mark with tape, measured up from the bottom end: 600 (ground level),",
                   "  1,480 and 1,970 (junction box bands), 2,330 and 2,580 (FieldNode",
                   "  bands). These are guides only; the parts are set by eye on site.",
                   "No holes are drilled in the post: everything clamps to it.",
                   "Fit: 600 mm stands in a 300 mm concrete footing, 2,100 mm above",
                   "  ground, plumb in both directions, 750 mm from the well centre.",
                   "Check: straight within 5 mm over its length; the cap is a push fit."],
            **base))

    if want(102):
        jpv = b.Rot(0, 0, -90) * b.Pos(-(jx0 + jt / 2), 0, -(P["jplate_z0"] + jh / 2)) * C["jplate"].shape
        out.append(bv.component_sheet(
            Part("Junction box plate", C["jplate"].shape, COL["jplate"]), [post_stub(), M["vblocks"], M["jbody"], M["jlid"], M["baro"], M["jbands"]],
            dwg_no="WLS-DWG-102", title="WellSense junction box plate: making sketch", material="Aluminium sheet 3 mm, 5052 or 6061 class",
            view_shape=jpv, inset_view=(18, 25),
            notes=["Blank 140 x 530 mm. Front view is the face the box sits on.",
                   "Heights up from the bottom edge; sideways from the centre line.",
                   "Band slots 3 x 15 at 51 each side, centred 20 and 510 up:",
                   "  chain drill 3 mm and file square. The bands go through these.",
                   "V-block screws 4.5, countersunk from the front, at 18 each side,",
                   "  20 and 510 up.",
                   "Lug screws 5.5 at 44 each side, 302 and 478 up.",
                   "Saddle screws 5.5 at 17.4 each side, 100 and 230 up.",
                   "Barometric housing 4.5 at 45 to the left (seen from the front),",
                   "  158 and 202 up.",
                   "Deburr every hole and edge; round the corners about 2 mm.",
                   "Check: lay the V-blocks, lugs and saddles on it and look through",
                   "  each hole; the holes must line up without forcing a screw."],
            **base))

    if want(103):
        vb = C["vblock_low"].shape
        out.append(bv.component_sheet(
            Part("V-block", vb, COL["vblock"]), [part("Plate", C["jplate"].shape & bx(-800, 0, -100, 100, 845, 925), COL["jplate"]),
                                                 part("Band", C["jbands"].shape & bx(-800, 0, -100, 100, 845, 925), COL["band"]),
                                                 post_stub(840, 930)],
            dwg_no="WLS-DWG-103", title="WellSense V-block (make 2): making sketch", material="Aluminium flat bar 60 x 40 mm, 6082 or 6061",
            view_shape=b.Rot(0, 0, -90) * b.Pos(-(jx0 - 16.5), 0, -D["jband_z"][0]) * vb, inset_view=(45, 210),
            notes=["Make two, the same as FieldNode's V-blocks. Saw a 20 mm slice off",
                   "  60 x 40 bar; saw and file it to 60 wide x 33 deep x 20 tall.",
                   "  The flat back goes on the junction box plate.",
                   "Scribe a 90 degree V on both 60 x 33 faces with a 45 degree square:",
                   f"  {2 * (D['vpoint'] - (jx0 - 33)):.1f} wide at the front face, point {jx0 - D['vpoint']:.1f} from the back face.",
                   "Saw just inside both lines, file to the lines, keep the faces flat.",
                   "Break the V's front edges 0.5 mm so they cannot scratch the post.",
                   "Drill 3.3, 14 deep, and tap M4 12 deep in the back face, 18 each",
                   "  side of centre, half way up (10).",
                   "Fit: two M4 countersunk screws from the front of the plate.",
                   "The 48.3 post touches both V faces; it never touches the bottom.",
                   "Check: on the post the block must not rock; light shows at the",
                   "  bottom of the V, not along its faces."],
            **base))

    if want(104):
        jb = C["jbody"].shape
        flip = b.Rot(180, 0, 0) * b.Rot(0, 0, -90) * b.Pos(-D["jbox_x"], 0, -P["jbox_z"]) * jb
        out.append(bv.component_sheet(
            Part("Junction box body", jb, COL["jbody"]), [M["jplate"], M["entries"], M["lugs"], post_stub()],
            dwg_no="WLS-DWG-104", title="WellSense junction box body: drilling sketch",
            material="Bought IP66 polycarbonate box 160 x 120 x 90 mm with bosses and lug kit",
            view_shape=flip, inset_view=(-30, 30),
            notes=["Drawn upside down: stand the box on its top, back face toward you;",
                   "  the top view then shows the bottom face as it lies on the bench.",
                   "Measure forward from the back face and sideways from the centre line",
                   "  (left and right as seen from the front, the lid side).",
                   "Back row, 22 from the back face: conduit hub 22 hole on the centre",
                   "  line; M16 gland 16 hole at 38 right.",
                   "Front row, 62 from the back face: breather 20 hole at 30 right;",
                   "  M12 gland 12 hole at 30 left.",
                   "Tape the face, pilot drill 3 slowly with wood behind, open out with",
                   "  a step drill. No solvents: polycarbonate crazes. Deburr.",
                   "Check each size against the part's datasheet before the last step.",
                   "Fit the four lugs to the back corners as the lug kit's maker says.",
                   "Check: no crack runs out of any hole under a bright lamp."],
            **base))

    if want(105):
        ib = S("iplate")
        xi = D["jbox_back"] + P["jwall"] + P["iboss"][2]
        ivs = b.Rot(0, 0, -90) * b.Pos(-(xi + 1.5), 0, -P["jbox_z"]) * ib
        out.append(bv.component_sheet(
            Part("Internal plate", ib, COL["iplate"]), [M["jbody"]],
            dwg_no="WLS-DWG-105", title="WellSense internal plate: making sketch", material="ASA, 3D printed, 100 % infill",
            view_shape=ivs, inset_view=(22, 25),
            notes=["Print flat, 100 x 130 x 3 mm, in ASA in an enclosed printer.",
                   "Four 4.5 holes, 80 apart across and 110 apart up and down, 10 in",
                   "  from the top and bottom edges: they meet the box's four moulded",
                   "  bosses. Measure your box's bosses first and move the holes to suit.",
                   "Lay out on the front: boost module upper left, ADC and shunt upper",
                   "  right, regulator and surge board below it, terminal strip along",
                   "  the bottom (left and right as seen from the lid side).",
                   "Mark each module's holes through the module; drill 3.2 for M3",
                   "  screws on 6 mm nylon standoffs.",
                   "Fit: four M4 screws into the bosses; the plate stands 6 mm off the",
                   "  back wall and 12 mm above the floor, clear of the entry nuts.",
                   "Check: flat within 0.5 mm; drops in and lifts out without force."],
            **base))

    if want(106):
        cv = b.Pos(-D["hub_x"], 0, -P["cable_z"]) * C["conduit"].shape
        out.append(bv.component_sheet(
            Part("Rigid conduit", C["conduit"].shape, COL["conduit"]), [M["post"], M["jplate"], M["jbody"], M["flex"], M["seal"]],
            dwg_no="WLS-DWG-106", title="WellSense rigid conduit: making sketch", material="1/2 in galvanized rigid conduit, 21.3 mm OD",
            view_shape=cv, inset_view=(15, -60),
            notes=[f"One length with one 90 degree bend, {P['bend_r']:.0f} mm centre-line radius,",
                   "  made with a 1/2 in hand conduit bender.",
                   f"Long leg (horizontal, toward the well): {P['rigid_x0'] - D['hub_x']:.0f} to the bend's",
                   f"  corner; short leg (vertical, into the box): {D['jbox_bot'] - P['jentries']['hub'][4] - P['cable_z']:.0f}",
                   "  to the corner. Developed length about 0.95 m.",
                   "Mark the bend from the corner back along each leg; bend, then",
                   "  check the angle with a square and trim the ends to length.",
                   "Cut with a hacksaw or tube cutter, ream the ends so the bore",
                   "  cannot cut the cable, and paint each cut end with zinc-rich paint.",
                   "Fit: the short end screws into the hub under the box; two spacer",
                   "  saddles hold it to the plate; the long end takes the connector",
                   "  of the flexible tail over the well.",
                   "Check: both legs square; the ends are smooth inside."],
            **base))

    if want(107):
        sp = S("seal_a", "seal_b", "spigot_a", "spigot_b")
        spv = b.Pos(0, 0, -D["seal_bot"]) * sp
        hr, hc, ht = P["seal_holes"]
        out.append(bv.component_sheet(
            Part("Seal plate", sp, COL["seal"]), [M["tube"], M["collar"], M["rim"], M["wraps"], M["gasket"]] + well_ctx(),
            dwg_no="WLS-DWG-107", title="WellSense split seal plate with spigot rings: making sketch",
            material="HDPE sheet 20 mm and 10 mm, drinking-water grade; EPDM 3 mm and 2 mm",
            view_shape=spv, inset_view=(28, -60),
            notes=["Plate: a 200 mm disc of 20 mm HDPE. Spigot: a ring of 10 mm HDPE,",
                   "  148 outside, 128 inside. Cut both with a jigsaw and a circle jig;",
                   "  file to the line. Check the spigot slides into your casing.",
                   f"Holes on one diameter: riser {hr:.0f} at {abs(P['riser_x']):.0f} left of centre,",
                   f"  pump cable {hc:.0f} at {P['pump_cable'][0]:.0f} right, tube {ht:.1f} at {P['tube_x']:.0f} right.",
                   "  Change them to suit your well: measure the riser and cable first.",
                   "Saw the disc and the ring in half along that diameter.",
                   "Screw each half ring under its plate half with three stainless",
                   "  4 x 16 screws, pilot drilled 3 mm.",
                   "Gasket: 3 mm EPDM, 184 outside, 150 inside, cut once to fit.",
                   "Wraps: 2 mm EPDM strips, 20 wide, one turn round the riser, the",
                   "  pump cable and the tube.",
                   "Fit: the halves meet round the wraps; a band clamp round the rim",
                   "  pulls them together. Check: halves meet with no daylight."],
            **base))

    if want(108):
        tb = S("tube", "endcap")
        zb = P["tube_bot"]
        bot = tb & b.Pos(P["tube_x"], 0, zb + 300) * b.Box(80, 80, 620)
        out.append(bv.component_sheet(
            Part("Access tube bottom", short(tb), COL["tube"]), [M["probe"]] + well_ctx(),
            dwg_no="WLS-DWG-108", title="WellSense access tube, drilled end: making sketch",
            material="1 in Sch 40 PVC pressure pipe 33.4 x 26.6 mm and a 1 in slip cap",
            view_shape=b.Pos(-P["tube_x"], 0, -zb) * bot, inset_view=(15, -60),
            notes=["Length: probe depth plus 0.5 m below it and 0.11 m above the casing",
                   "  top; in 3 m lengths joined with solvent-weld couplings. Joints",
                   "  must be smooth inside so the probe cannot catch.",
                   f"Bottom 0.5 m: {int(((P['slot_zone'] - P['holes'][2]) // P['holes'][1]) + 1)} rings of 8 mm holes, rings 50 apart, the first",
                   "  40 up from the end. Each ring is two holes drilled straight through",
                   "  at right angles (four holes); turn the next ring 45 degrees.",
                   "  Drill in a V-block; deburr inside with a round file.",
                   "Solvent-weld the slip cap on the bottom end; drill one 8 mm",
                   "  drain hole in the cap so water can leave when the tube is lifted.",
                   "Top end: cut square 110 mm above the casing top; deburr.",
                   "The probe hangs 50 mm above the end, inside the drilled zone.",
                   "Check: a 22 mm rod drops through the whole tube freely."],
            **base))

    if want(109):
        cp = S("cap", "cross_bolt")
        out.append(bv.component_sheet(
            Part("Tube cap", cp, COL["cap"]), [part("Tube top", C["tube"].shape & bx(0, 80, -40, 40, 470, 600), COL["tube"]),
                                               part("Tail", S("connector", "flex") & bx(-30, 80, -40, 40, 560, 800), COL["flex"]), M["collar"]],
            dwg_no="WLS-DWG-109", title="WellSense tube cap: making sketch", material="1 in Sch 40 PVC slip cap; stainless M5 x 50 bolt",
            view_shape=b.Pos(-P["tube_x"], 0, -D["cap_bot"]) * cp, inset_view=(20, -50),
            notes=["Do not glue the cap: it lifts off with the probe for calibration.",
                   "Top: drill 22.5 mm in the centre for the 1/2 in conduit connector.",
                   f"Side: drill 5 mm straight across, {P['cross_bolt'][1]:.0f} above the tube end (the cap's",
                   f"  shoulder) and {P['cross_bolt'][0]:.0f} off the centre line, for the M5 cross bolt.",
                   "The bolt passes beside the cable, never through it.",
                   "Fit: the conduit connector goes through the top with its locknut",
                   "  inside. The cable support grip's eye goes over the cross bolt,",
                   "  which then carries the probe and cable; nyloc nut outside.",
                   "The cap sits on the tube end by its own weight and the load.",
                   "Check: with the bolt in, the cap still slides on and off the tube."],
            **base))
    return out


# ----------------------------------------------------------------- joints
def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & bx(x0, x1, y0, y1, z0, z1)


def joints(only=None):
    out = []
    want = lambda n: only is None or n in only  # noqa: E731
    px = P["post_x"]
    jx0, jf = D["jplate_x0"], D["jplate_front"]
    z1 = D["jband_z"][1]
    if want(1):
        box_ = (px - 40, jf + 60, -75, 75, z1 - 10, z1 + 6)
        out.append(bv.joint([
            part("Post", win(C["post"].shape, *box_), COL["post"]),
            part("Junction box plate", win(C["jplate"].shape, *box_), COL["jplate"]),
            part("V-block", win(C["vblock_up"].shape, *box_), COL["vblock"]),
            part("Band clamp, through the plate slots", win(C["jbands"].shape, *box_), COL["band"]),
            part("Junction box lug", win(C["jlugs"].shape, *box_), COL["lugs"])],
            OUT / "joint-01.png", "Joint 1: V-block, post and band clamp",
            subtitle="Cut level with the upper band, seen from above. The post bears on both V faces; the band pulls it in",
            elev=80, azim=-90, size=(8, 6)))
    if want(2):
        jt = D["jbox_top"]
        box_ = (jx0 - 6, jf + 30, 25, 60, jt - 25, jt + 30)
        out.append(bv.joint([
            part("Junction box plate", win(C["jplate"].shape, *box_), COL["jplate"]),
            part("Junction box body", win(C["jbody"].shape, *box_), COL["jbody"]),
            part("Lug (maker's kit)", win(C["jlugs"].shape, *box_), "#2563EB"),
            part("M5 screw from behind, nyloc nut in front", win(C["jlug_screws"].shape, *box_), COL["bolt"])],
            OUT / "joint-02.png", "Joint 2: junction box lug on the plate (top right corner)",
            subtitle="Seen from the right and above. The lug lies flat on the plate on top of the box; one M5 screw holds it",
            elev=25, azim=70, size=(8, 6)))
    if want(3):
        jb = D["jbox_bot"]
        box_ = (jf - 2, D["jbox_front"] + 2, -65, 65, jb - 32, jb + 12)
        g = C["glands"].shape
        out.append(bv.joint([
            part("Junction box floor", win(C["jbody"].shape, *box_), COL["jbody"]),
            part("1 Conduit hub, with the conduit", win(S("hub", "conduit"), *box_), COL["conduit"]),
            part("2 M16 gland (FieldNode lead)", win(g, jf - 2, D["jbox_front"], 10, 65, jb - 32, jb + 12), "#2563EB"),
            part("3 Desiccant breather", win(C["breather"].shape, *box_), COL["breather"]),
            part("4 M12 gland (barometric lead)", win(g, jf - 2, D["jbox_front"], -65, -10, jb - 32, jb + 12), "#7C3AED")],
            OUT / "joint-03.png", "Joint 3: the junction box floor, seen from below",
            subtitle="Numbers as the drilling layout. Back row (near the plate): hub and M16 gland; front row: breather and M12 gland",
            elev=-65, azim=-150, size=(8, 6)))
    if want(4):
        zc = P["jbox_z"]
        box_ = (jf - 1, D["jbox_front"] + 1, -40, 65, zc - 100, zc + 90)
        out.append(bv.joint([
            part("Junction box body (cut open)", win(C["jbody"].shape, *box_), COL["jbody"]),
            part("Internal plate", win(C["iplate"].shape, *box_), COL["iplate"]),
            part("Boost module", win(C["mod_boost"].shape, *box_), COL["boost"]),
            part("Terminal strip", win(C["mod_strip"].shape, *box_), COL["strip"]),
            part("Lid", win(C["jlid"].shape, *box_), COL["jlid"]),
            part("Hub nut on the floor", win(C["hub"].shape, *box_), COL["entries"])],
            OUT / "joint-04.png", "Joint 4: internal plate on its bosses (box cut through the left bosses)",
            subtitle="Seen from the left. The plate sits on the moulded bosses, 6 mm off the back wall and 6 mm above the hub nut",
            elev=12, azim=-110, size=(8, 6)))
    if want(5):
        hx = D["hub_x"]
        zs = P["saddle_z"][1]
        box_ = (jx0 - 3, hx + 30, -40, 40, zs - 45, D["jbox_bot"] - 0.01)
        out.append(bv.joint([
            part("Junction box plate", win(C["jplate"].shape, *box_), COL["jplate"]),
            part("Spacer saddle (two M5 screws)", win(C["saddles"].shape, *box_), COL["saddle"]),
            part("Rigid conduit", win(C["conduit"].shape, *box_), COL["conduit"]),
            part("Conduit hub, screwed into the box floor above", win(C["hub"].shape, *box_), COL["entries"])],
            OUT / "joint-05.png", "Joint 5: conduit on its saddle and into the hub",
            subtitle="Seen from the front right; the box above is left out. The saddle holds the conduit 11 mm off the plate, square under the hub",
            elev=12, azim=-35, size=(8, 6)))
    if want(6) and False:
        import build123d as b
        st = P["stickup"]
        cut = b.Pos(0, 150, 0) * b.Box(600, 300, 3000)
        box_ = (-110, 110, -110, 110, st - 60, st + 60)
        ws = lambda k: win(C[k].shape, *box_) & cut  # noqa: E731
        out.append(bv.joint([
            part("Casing", ws("casing"), COL["casing"]),
            part("EPDM gasket", ws("gasket"), COL["gasket"]),
            part("Seal plate half A", ws("seal_a"), COL["seal"]),
            part("Spigot half ring", ws("spigot_a"), COL["spigot"]),
            part("Rim band clamp", ws("rim_band"), COL["rim"]),
            part("EPDM wraps", ws("wraps"), COL["wraps"]),
            part("Riser and pump cable", ws("pump"), COL["pump"]),
            part("Access tube", ws("tube"), COL["tube"]),
            part("Tube collar", ws("collar"), COL["collar"])],
            OUT / "joint-06.png", "Joint 6: seal plate on the casing, cut on the split line",
            subtitle="Seen from the front. Spigot inside the casing, gasket on its rim, collar on the plate carrying the tube",
            elev=12, azim=-90, size=(9, 6)))
    if want(7) and False:
        st = P["stickup"]
        box_ = (-110, 110, -110, 110, st - 5, D["collar_top"] + 5)
        out.append(bv.joint([
            part("Seal plate half A (back)", win(C["seal_a"].shape, *box_), COL["seal"]),
            part("Seal plate half B (front)", win(C["seal_b"].shape, *box_), "#60A5FA"),
            part("EPDM wraps round the riser, pump cable and tube", win(C["wraps"].shape, *box_), COL["wraps"]),
            part("Riser and pump cable", win(C["pump"].shape, *box_), COL["pump"]),
            part("Access tube", win(C["tube"].shape, *box_), COL["tube"]),
            part("Tube collar", win(C["collar"].shape, *box_), COL["collar"]),
            part("Rim band clamp", win(C["rim_band"].shape, *box_), COL["rim"])],
            OUT / "joint-07.png", "Joint 7: the split, seen from above",
            subtitle="Both halves close round the wrapped riser, pump cable and tube; the rim band pulls them together",
            elev=70, azim=-90, size=(8, 6)))
    if want(8) and False:
        import build123d as b
        tx = P["tube_x"]
        cut = b.Pos(0, 150, 0) * b.Box(600, 300, 3000)
        box_ = (tx - 40, tx + 40, -40, 40, P["tube_top"] - 80, D["conn_top"] + 30)
        ws = lambda k: win(C[k].shape, *box_) & cut  # noqa: E731
        out.append(bv.joint([
            part("Access tube", ws("tube"), COL["tube"]),
            part("Tube cap", ws("cap"), COL["cap"]),
            part("M5 cross bolt", win(C["cross_bolt"].shape, *box_), COL["bolt"]),
            part("Support grip on the cable", ws("grip"), COL["grip"]),
            part("Vented cable", ws("cable"), COL["cable"]),
            part("Conduit connector", ws("connector"), COL["conn"]),
            part("Flexible tail", ws("flex"), COL["flex"])],
            OUT / "joint-08.png", "Joint 8: tube cap, cut open",
            subtitle="Seen from the front. The grip's eye hangs on the cross bolt; the cap rests on the tube end",
            elev=8, azim=-90, size=(8, 6.5)))
    out += sections({n for n in (6, 7, 8) if want(n)})
    if want(9):
        import build123d as b
        tx = P["tube_x"]
        cut = b.Pos(0, 150, 0) * b.Box(600, 300, 6000)
        zb = P["tube_bot"]
        box_ = (tx - 40, tx + 40, -40, 40, zb - 10, zb + 320)
        ws = lambda k: win(C[k].shape, *box_) & cut  # noqa: E731
        out.append(bv.joint([
            part("Access tube (drilled)", ws("tube"), COL["tube"]),
            part("End cap", ws("endcap"), COL["endcap"]),
            part("Pressure transducer", win(C["probe"].shape, *box_), COL["probe"]),
            part("Vented cable", win(C["cable"].shape, *box_), COL["cable"])],
            OUT / "joint-09.png", "Joint 9: probe in the drilled bottom of the tube, cut open",
            subtitle="2.3 mm clear all round; 50 mm above the end cap; water reaches it through the 8 mm holes",
            elev=8, azim=-90, size=(7, 7)))
    return out


# ----------------------------------------------------------------- 2D sections (joints 6, 7 and 8)
def _sec_fig(title, sub):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(12, 6.5), dpi=150)
    fig.text(0.02, 0.97, title, fontsize=13, fontweight="bold", color="#111827", va="top")
    fig.text(0.02, 0.925, sub, fontsize=9, color="#374151", va="top")
    fig.text(0.02, 0.015, bv.BANNER, fontsize=7, color="#B45309")
    fig.text(0.98, 0.015, REPO, fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax = fig.add_axes([0.27, 0.06, 0.46, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    return fig, ax


def _lab(ax, fig, xy, text, side, ty):
    """Leader from a point on a part (data coords) to a label at the left or right edge (axes y fraction ty)."""
    import matplotlib.transforms as mt
    tx = -0.04 if side == "left" else 1.04
    ax.annotate(text, xy=xy, xytext=(tx, ty), textcoords=ax.transAxes, fontsize=8, color="#111827",
                ha="right" if side == "left" else "left", va="center",
                arrowprops=dict(arrowstyle="-", color="#6B7280", lw=0.6, shrinkA=2, shrinkB=0),
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#6B7280", lw=0.5))
    ax.plot(*xy, "o", ms=2.2, color="#111827", zorder=9)


def sections(only):
    from matplotlib.patches import Rectangle, Circle, Wedge, Polygon
    out = []
    st = P["stickup"]
    sb, stp = D["seal_bot"], D["seal_top"]
    rx, rr = P["riser_x"], P["riser_od"] / 2
    cx_, cd_ = P["pump_cable"]
    tx, to, ti = P["tube_x"], P["tube_od"] / 2, P["tube_id"] / 2
    hr, hc, ht = (h / 2 for h in P["seal_holes"])
    cr, cod = P["casing_id"] / 2, P["casing_od"] / 2
    sr = P["seal_d"] / 2
    spo, spi, spd = P["spigot"]
    gt, god = P["gasket"]
    co, cw = P["collar"]
    rbw, rbt = P["rim_band"]
    GREY, HDPE, HDPE2, RUB, PVC, ORG = "#9CA3AF", "#2563EB", "#60A5FA", "#111827", "#D1D5DB", "#B45309"

    def R(ax, x0, x1, z0, z1, c, **k):
        ax.add_patch(Rectangle((x0, z0), x1 - x0, z1 - z0, fc=c, ec="#111827", lw=0.6, **k))

    if 6 in only:
        fig, ax = _sec_fig("Joint 6: seal plate on the casing, cut along the split line",
                           "Section through the riser, pump cable and tube. Sizes in mm. The spigot locates the plate; the collar carries the tube")
        z0, z1 = st - 60, stp + 55
        for sgn in (-1, 1):
            R(ax, sgn * cr, sgn * cod, z0, st, GREY)                       # casing wall
            R(ax, sgn * cr, sgn * (god / 2), st, st + gt, RUB)             # gasket
            R(ax, sgn * (spi / 2), sgn * (spo / 2), sb - spd, sb, "#1E40AF")  # spigot
            R(ax, sgn * sr, sgn * (sr + rbt + 0.8), sb + (P["seal_t"] - rbw) / 2, sb + (P["seal_t"] + rbw) / 2, "#6B7280")  # rim band
        # plate pieces between the holes
        edges = [-sr, rx - hr, rx + hr, cx_ - hc, cx_ + hc, tx - ht, tx + ht, sr]
        for a, b_ in zip(edges[0::2], edges[1::2]):
            R(ax, a, b_, sb, stp, HDPE)
        for c_, r_in, r_out in ((rx, rr, hr), (cx_, cd_ / 2, hc), (tx, to, ht)):
            R(ax, c_ - r_out, c_ - r_in, sb, stp, RUB); R(ax, c_ + r_in, c_ + r_out, sb, stp, RUB)
        R(ax, rx - rr, rx + rr, z0, z1, "#6B7280")                         # riser
        R(ax, cx_ - cd_ / 2, cx_ + cd_ / 2, z0, z1, "#4B5563")              # pump cable
        R(ax, tx - to, tx - ti, z0, z1, PVC); R(ax, tx + ti, tx + to, z0, z1, PVC)  # tube walls
        R(ax, tx - co / 2, tx - to, stp, stp + cw, ORG); R(ax, tx + to, tx + co / 2, stp, stp + cw, ORG)  # collar
        ax.set_xlim(-sr - 12, sr + 12); ax.set_ylim(z0 - 5, z1 + 5)
        L = [((-cod + 4, st - 30), "Existing casing (150 mm bore)", "left", 0.12),
             ((-(god / 2) + 3, st + gt / 2), "EPDM gasket, 3 mm, on the rim", "left", 0.36),
             ((-(spo / 2) + 4, sb - spd / 2), "HDPE spigot half ring, 1 mm inside the bore", "left", 0.24),
             ((-sr + 15, stp - 4), "Seal plate, 20 mm HDPE", "left", 0.62),
             ((-sr - rbt - 0.4, sb + P["seal_t"] / 2), "Rim band clamp", "left", 0.48),
             ((rx, z1 - 10), "Riser (existing)", "left", 0.88),
             ((rx - hr + 1, stp - 3), "EPDM wrap, 2 mm, squeezed", "left", 0.75),
             ((cx_, z1 - 10), "Pump cable (existing)", "right", 0.88),
             ((tx + ti + 1.5, z1 - 15), "Access tube", "right", 0.75),
             ((tx + co / 2 - 3, stp + cw / 2), "Tube collar on the plate", "right", 0.6),
             ((tx + to + 1, sb + 4), "EPDM wrap round the tube", "right", 0.42),
             ((cod - 4, st - 30), "Casing wall", "right", 0.12)]
        for xy, t, sd, ty in L:
            _lab(ax, fig, xy, t, sd, ty)
        fig.savefig(OUT / "joint-06.png", facecolor="white"); out.append(OUT / "joint-06.png")
        import matplotlib.pyplot as plt; plt.close(fig)

    if 7 in only:
        fig, ax = _sec_fig("Joint 7: the split, seen from above",
                           "Both halves close round the wrapped riser, pump cable and tube; the band round the rim pulls them together")
        ax.add_patch(Wedge((0, 0), sr, 0, 180, fc=HDPE, ec="#111827", lw=0.8))
        ax.add_patch(Wedge((0, 0), sr, 180, 360, fc=HDPE2, ec="#111827", lw=0.8))
        ax.add_patch(Circle((0, 0), sr + rbt + 0.8, fc="none", ec="#6B7280", lw=2.2))
        ax.add_patch(Rectangle((-9, -sr - 11), 18, 10, fc="#6B7280", ec="#111827", lw=0.6))
        for c_, r_in, r_out, col in ((rx, rr, hr, "#6B7280"), (cx_, cd_ / 2, hc, "#4B5563")):
            ax.add_patch(Circle((c_, 0), r_out, fc=RUB, ec="none"))
            ax.add_patch(Circle((c_, 0), r_in, fc=col, ec="#111827", lw=0.6))
        ax.add_patch(Circle((tx, 0), ht, fc=RUB, ec="none"))
        ax.add_patch(Circle((tx, 0), co / 2, fc=ORG, ec="#111827", lw=0.6))
        ax.add_patch(Circle((tx, 0), to, fc=PVC, ec="#111827", lw=0.6))
        ax.add_patch(Circle((tx, 0), ti, fc="white", ec="#111827", lw=0.6))
        ax.plot([-sr - 4, sr + 4], [0, 0], color="#B91C1C", lw=0.8, ls=(0, (5, 3)))
        ax.set_xlim(-sr - 8, sr + 8); ax.set_ylim(-sr - 14, sr + 8)
        L = [((-60, 55), "Plate half A (back)", "left", 0.82),
             ((-60, -55), "Plate half B (front)", "left", 0.18),
             ((rx, 0), "Riser (existing)", "left", 0.6),
             ((rx - hr + 0.8, 4), "EPDM wrap", "left", 0.45),
             ((-sr * 0.71, -sr * 0.71), "Rim band clamp", "left", 0.06),
             ((cx_, hc - 0.5), "Pump cable (existing) in its wrap", "right", 0.94),
             ((tx + co / 2 - 3, 6), "Tube collar (on the plate)", "right", 0.64),
             ((tx + ti + 1, -2), "Access tube", "right", 0.5),
             ((sr - 2, 0), "Split line", "right", 0.36),
             ((0, -sr - 6), "Band's worm drive", "right", 0.06)]
        for xy, t, sd, ty in L:
            _lab(ax, fig, xy, t, sd, ty)
        fig.savefig(OUT / "joint-07.png", facecolor="white"); out.append(OUT / "joint-07.png")
        import matplotlib.pyplot as plt; plt.close(fig)

    if 8 in only:
        fig, ax = _sec_fig("Joint 8: tube cap, cut open on the tube's centre line",
                           "The grip's eye hangs on the cross bolt; the cap rests on the tube end; the connector's locknut is inside the cap")
        tt = P["tube_top"]
        cbot, ctop = D["cap_bot"], D["cap_top"]
        cpo = P["cap"][0] / 2
        ctk = P["cap"][3]
        ch = P["cap_hole"] / 2
        bxo, bz = P["cross_bolt"]
        crr = P["cable_d"] / 2
        fo, fi = P["flex"]
        z0, z1 = tt - 110, ctop + 70
        R(ax, tx - to, tx - ti, z0, tt, PVC); R(ax, tx + ti, tx + to, z0, tt, PVC)            # tube
        CAP = "#D4A017"
        R(ax, tx - cpo, tx - to, cbot, ctop, CAP); R(ax, tx + to, tx + cpo, cbot, ctop, CAP)  # cap skirt
        R(ax, tx - to, tx - ti - 0.4, tt, ctop - ctk, CAP); R(ax, tx + ti + 0.4, tx + to, tt, ctop - ctk, CAP)  # shoulder
        R(ax, tx - to, tx - ch, ctop - ctk, ctop, CAP); R(ax, tx + ch, tx + to, ctop - ctk, ctop, CAP)  # top
        CON = "#1F2937"
        R(ax, tx - ch, tx - 8, ctop - ctk, ctop, CON); R(ax, tx + 8, tx + ch, ctop - ctk, ctop, CON)
        R(ax, tx - 13, tx - 8, ctop, ctop + 20, CON); R(ax, tx + 8, tx + 13, ctop, ctop + 20, CON)
        R(ax, tx - 13, tx - 8, ctop - ctk - 3, ctop - ctk, CON); R(ax, tx + 8, tx + 13, ctop - ctk - 3, ctop - ctk, CON)
        R(ax, tx - fo / 2, tx - fi / 2, ctop + 20, z1, "#475569"); R(ax, tx + fi / 2, tx + fo / 2, ctop + 20, z1, "#475569")
        R(ax, tx - crr, tx + crr, z0, z1, "#111827")                                          # cable
        R(ax, tx - crr - 1.5, tx - crr, tt - 70, tt - 10, "#6B7280"); R(ax, tx + crr, tx + crr + 1.5, tt - 70, tt - 10, "#6B7280")  # grip
        ax.add_patch(Polygon([(tx + crr + 1.5, tt - 12), (tx + bxo, tt - 2), (tx + bxo, tt + bz - 2.5)], closed=False,
                             fill=False, ec="#6B7280", lw=2.2))
        ax.add_patch(Circle((tx + bxo, tt + bz), 2.5, fc="#111827", ec="none"))                   # cross bolt
        ax.set_xlim(tx - 45, tx + 45); ax.set_ylim(z0 - 3, z1 + 3)
        L = [((tx - fo / 2 + 1, z1 - 12), "Flexible conduit tail", "left", 0.9),
             ((tx - 12, ctop + 10), "Conduit connector, locknut inside", "left", 0.74),
             ((tx - cpo + 1, cbot + 15), "Tube cap (1 in slip cap, not glued)", "left", 0.5),
             ((tx - ti - 1.7, tt - 40), "Access tube", "left", 0.3),
             ((tx - crr - 0.8, tt - 50), "Cable support grip", "left", 0.14),
             ((tx, z1 - 30), "Vented cable", "right", 0.86),
             ((tx + bxo + 2, tt + bz + 1), "M5 cross bolt (seen end on)", "right", 0.62),
             ((tx + bxo, tt - 4), "Grip's eye over the bolt", "right", 0.48),
             ((tx + to - 1, tt + 3), "Tube end against the cap's shoulder", "right", 0.34)]
        for xy, t, sd, ty in L:
            _lab(ax, fig, xy, t, sd, ty)
        fig.savefig(OUT / "joint-08.png", facecolor="white"); out.append(OUT / "joint-08.png")
        import matplotlib.pyplot as plt; plt.close(fig)
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    import build123d as b
    M = made()
    out = []
    want = lambda n: only is None or n in only  # noqa: E731

    def st(n, done, new, title, sub, **kw):
        if want(n):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    px = P["post_x"]
    ground = part("Ground", bx(px - 300, px + 300, -300, 300, -2, 0), "#E7E5E4")
    hole = part("Footing hole", b.Pos(px, 0, -300) * b.Cylinder(150, 600), "#D6D3D1", alpha=1.0)
    st(1, [], [mv(M["post"], (0, 0, 700)), mv(M["footing"], (0, 0, 0))], "post into its footing",
       "Hole 300 mm across and 650 deep; post on 50 mm of gravel, plumbed and braced; one 25 kg bag of concrete",
       context=[ground], elev=12, azim=-50)
    st(2, [M["jplate"]], [mv(part("Upper V-block", C["vblock_up"].shape, COL["vblock"]), (-110, 0, 0)),
                          mv(part("Lower V-block", C["vblock_low"].shape, COL["vblock"]), (-110, 0, 0))],
       "V-blocks onto the junction box plate", "Two M4 countersunk screws each, from the front of the plate, threadlocker. Seen from behind",
       elev=20, azim=140, label_done=False)
    gl = C["glands"].shape
    st(3, [part("Junction box body", C["jbody"].shape, COL["jbody"])],
       [mv(part("1 Conduit hub", C["hub"].shape, COL["entries"]), (0, 0, -90)),
        mv(part("2 M16 gland", gl & bx(-800, 0, 10, 80, 1000, 1300), "#2563EB"), (0, 0, -90)),
        mv(part("3 Desiccant breather", C["breather"].shape, COL["breather"]), (0, 0, -90)),
        mv(part("4 M12 gland", gl & bx(-800, 0, -80, -10, 1000, 1300), "#7C3AED"), (0, 0, -90))],
       "hub, glands and breather into the box", "Each goes in from below with its seal outside and its nut inside. Seen from the front, below",
       elev=-22, azim=25, label_done=False)
    st(4, [part("Internal plate", C["iplate"].shape, COL["iplate"])],
       [mv(part("Boost module", C["mod_boost"].shape, COL["boost"]), (80, 0, 0)),
        mv(part("ADC and shunt module", C["mod_adc"].shape, COL["adc"]), (80, 0, 0)),
        mv(part("Regulator and surge module", C["mod_reg"].shape, COL["reg"]), (80, 0, 0)),
        mv(part("Terminal strip", C["mod_strip"].shape, COL["strip"]), (80, 0, 0))],
       "build the internal plate", "Each module on M3 screws and 6 mm nylon standoffs; then wire them as the wiring diagram shows",
       elev=15, azim=40, label_done=True)
    jdone = [M["jplate"], M["vblocks"]]
    st(5, jdone, [mv(part("Junction box body with entries", S("jbody", "hub", "glands", "breather"), COL["jbody"]), (140, 0, 0)),
                  mv(M["lugs"], (60, 0, 0))],
       "junction box onto the plate", "Lugs on the box corners; box back flat on the plate; four M5 screws from behind, nyloc nuts in front",
       elev=18, azim=40)
    box_done = jdone + [part("Junction box", S("jbody", "hub", "glands", "breather"), COL["jbody"]), M["lugs"]]
    st(6, box_done, [mv(M["iboard"], (160, 0, 0))], "internal plate into the box",
       "Four M4 screws into the moulded bosses. Leave the lid off until step 17", elev=18, azim=40, label_done=False)
    box_done = box_done + [M["iboard"]]
    st(7, box_done, [mv(M["baro"], (90, 0, 0))], "barometric housing onto the plate",
       "Two M4 screws through its flange; its lead up through the M12 gland, tightened on the lead",
       elev=18, azim=40, label_done=False)
    box_done = box_done + [M["baro"]]
    st(8, [post_stub(780, 1480)], [mv(part("Junction box plate assembly", _fuse([p.shape for p in box_done]), "#0F766E"), (220, 0, 0)),
                                   mv(part("Band clamps (2)", C["jbands"].shape, COL["band"]), (0, 0, 0))],
       "junction box onto the post", "V-blocks on the post, box facing the well, plate 860 mm above the ground; bands round the post, through the slots, tightened",
       elev=18, azim=-35)
    surf = [post_stub(700, 2120), part("Junction box on its plate", _fuse([p.shape for p in box_done] + [C["jbands"].shape]), COL["jplate"])]
    st(9, surf, [mv(M["fieldnode"], (0, -250, 0))], "FieldNode core onto the post",
       "Built to the FieldNode build plan. Its V-blocks on the post, base 1,750 mm up, facing the equator; its two bands tightened",
       elev=12, azim=-40, label_done=False)
    surf = surf + [M["fieldnode"]]
    clip10 = bx(-1000, 0, -300, 300, 1060, 1800)
    st(10, _clip_parts(surf, clip10), [mv(part("FieldNode lead with M12 plug", C["lead"].shape, "#DC2626"), (0, 0, 0))],
       "FieldNode lead from the box to port A",
       "Through the M16 gland with a drip loop below the box; up the post outside the bands, cable-tied; M12 plug into port A",
       elev=12, azim=-30, label_done=False)
    surf = surf + [M["lead"]]
    clip11 = bx(-1000, 0, -300, 300, 650, 1420)
    st(11, _clip_parts(surf, clip11), [mv(M["conduit"], (0, 0, -160))], "rigid conduit into the hub and saddles",
       "Short leg up into the hub, hand tight plus a quarter turn; saddles screwed to the plate; long leg level toward the well",
       elev=12, azim=-35, label_done=False)
    wctx = well_ctx(zmin=200.0)
    top = bx(-3000, 3000, -3000, 3000, 200, 4000)
    st(12, [], [mv(part("Access tube (top end shown)", S("tube") & top, "#0F766E"), (0, 0, 450))], "access tube down the casing",
       "Pump isolated and locked off first. Lower it slowly beside the riser and pump cable, two people; it hangs from the hands until step 14",
       context=wctx, elev=14, azim=-60)
    tube_in = part("Access tube", S("tube") & top, COL["tube"])
    st(13, [tube_in], [mv(M["gasket"], (0, 0, 90)), mv(part("EPDM wraps", C["wraps"].shape, "#DC2626"), (0, 0, 200)),
                       mv(part("Seal plate half A", S("seal_a", "spigot_a"), COL["seal"]), (0, 180, 40)),
                       mv(part("Seal plate half B", S("seal_b", "spigot_b"), "#60A5FA"), (0, -180, 40))],
       "gasket, wraps and the two seal plate halves", "Gasket on the casing rim; one turn of EPDM round the riser, pump cable and tube; the halves close round them",
       context=wctx, elev=25, azim=-60)
    seal_done = [tube_in, M["gasket"], M["wraps"], M["seal"]]
    st(14, seal_done, [mv(M["rim"], (0, 0, 120)), mv(M["collar"], (0, 0, 160))], "rim band and tube collar",
       "Rim band tightened until the halves meet; tube top 110 mm above the casing; collar clamped on it, on the plate",
       context=wctx, elev=25, azim=-60, label_done=False)
    seal_done = seal_done + [M["rim"], M["collar"]]
    head = surf + [M["conduit"]] + seal_done
    clip15 = bx(-800, 200, -300, 600, 380, 1400)
    head15 = _clip_parts(head, clip15)
    st(15, head15, [mv(part("Tube cap with connector, and flexible tail", S("cap", "connector", "flex", "coupling"), "#0F766E"), (0, 0, 140)),
                    mv(part("Vented cable end, pushed up into the box", S("cable") & bx(-800, -600, -100, 100, D["jbox_bot"] - 25, 1400), "#DC2626"), (0, 0, 0))],
       "thread the cable", "Cable end up through the cap, the tail and the rigid conduit into the box; tail connector onto the rigid end",
       context=wctx, elev=16, azim=-50, label_done=False)
    import build123d as b
    pr_shape = S("probe") + (C["cable"].shape & bx(0, 80, -40, 40, D["probe_top"], D["probe_top"] + 250))
    lift = (P["tube_top"] - 150) - D["probe_top"]
    probe_up = b.Pos(0, 0, lift) * pr_shape
    st(16, seal_done, [mv(part("Pressure transducer on its cable (lowered down the tube)", probe_up, COL["probe"]), (0, 0, 480)),
                       mv(part("Support grip and cross bolt", S("grip", "cross_bolt"), "#DC2626"), (0, 0, 200))],
       "lower the probe and hang it", "Disinfected first. Lower it hand over hand to the recorded depth; grip on the cable at the mark, its eye on the cross bolt",
       context=wctx, elev=16, azim=-60, label_done=False)
    clip17 = bx(-800, -550, -300, 300, 820, 1420)
    full17 = _clip_parts(head, clip17)
    coil = C["cable"].shape & bx(D["jbox_back"], D["jbox_front"], -70, 70, D["jbox_bot"] + 3, D["jbox_top"])
    st(17, full17, [mv(part("Service loop, 1.1 m coiled", coil, "#DC2626"), (0, 0, 0)),
                    mv(part("Junction box lid", C["jlid"].shape, "#0F766E"), (140, 0, 0))], "service loop, terminals and lid",
       "Coil 1.1 m of cable in the box; vent tube end left open inside; cores to the terminal strip; lid gasket clean, screws in a cross pattern",
       elev=16, azim=-30, label_done=False)
    return out


def _clip_parts(parts, box_):
    out = []
    for q in parts:
        try:
            sh = q.shape & box_
        except Exception:
            continue
        if bv._has_volume(sh):
            out.append(part(q.name, sh, q.color))
    return out


def _above(z):
    return bx(-3000, 3000, -3000, 3000, z, 4000)


def _below(z):
    return bx(-3000, 3000, -3000, 3000, -6000, z)


# ----------------------------------------------------------------- hole layouts
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle, Wedge
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    res = []

    def foot(fig):
        fig.text(0.04, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
        fig.text(0.96, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")

    # junction box plate, seen from the front (the face the box sits on); y to the right
    jw, jh, jt = P["jplate"]
    z0 = P["jplate_z0"]
    holes = []
    for zb in D["jband_z"]:
        for s in (+1, -1):
            holes.append(("slot", s * P["band_slot_y"], zb - z0, 3, 15))
            holes.append(("csk", s * 18.0, zb - z0, 4.5, 0))
    for zl in (D["jbox_top"] + P["jlug"][3] / 2, D["jbox_bot"] - P["jlug"][3] / 2):
        for s in (+1, -1):
            holes.append(("hole", s * P["jlug"][0], zl - z0, 5.5, 0))
    ro = P["conduit_od"] / 2
    for zs in P["saddle_z"]:
        for s in (+1, -1):
            holes.append(("hole", s * (ro + 6.75), zs - z0, 5.5, 0))
    by, bz = P["baro"][2], P["baro"][3]
    for zz in (bz - 22, bz + 22):
        holes.append(("hole", by, zz - z0, 4.5, 0))
    fig = plt.figure(figsize=(9, 12), dpi=150)
    ax = fig.add_axes([0.1, 0.06, 0.5, 0.86]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((-jw / 2, 0), jw, jh, fc="#F5F5F4", ec=INK, lw=1.2))
    ax.plot([0, 0], [-4, jh + 6], color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    # where the box and its lugs sit (dashed)
    ax.add_patch(Rectangle((-P["jbox"][1] / 2, D["jbox_bot"] - z0), P["jbox"][1], P["jbox"][2], fc="none", ec=MUT, lw=0.7, ls="--"))
    ax.text(0, P["jbox_z"] - z0 + 20, "junction box\nsits here", ha="center", va="center", fontsize=8, color=MUT)
    xs, zs_ = set(), set()
    for kind, x, z, d, h in holes:
        if kind == "slot":
            ax.add_patch(Rectangle((x - d / 2, z - h / 2), d, h, fc="white", ec=INK, lw=1))
        else:
            ax.add_patch(Circle((x, z), d / 2, fc="white", ec=INK, lw=1))
            if kind == "csk":
                ax.add_patch(Circle((x, z), d / 2 + 2, fc="none", ec=INK, lw=0.5))
        if x > 0.5 or kind == "hole" and x < 0 and abs(x - by) < 0.1:
            xs.add(round(abs(x), 1) * (1 if x > 0 else -1))
        zs_.add(round(z, 1))
    for i, x in enumerate(sorted(xs)):
        yl = -14 - 11 * (i % 2)
        ax.plot([x, x], [0, yl + 4], color=AC, lw=0.4, ls=":")
        ax.text(x, yl, f"{abs(x):g}" + (" L" if x < 0 else ""), ha="center", va="top", fontsize=7.5, color=AC)
    ax.text(0, -44, "sideways from the centre line, mm (same each side unless marked L)", ha="center", fontsize=8, color=MUT)
    for i, z in enumerate(sorted(zs_)):
        xl = -jw / 2 - 6 - 22 * (i % 2)
        ax.plot([xl + 2, -jw / 2], [z, z], color=AC, lw=0.4, ls=":")
        ax.text(xl, z, f"{z:g}", ha="right", va="center", fontsize=7.5, color=AC)
    ax.text(-jw / 2 - 52, jh / 2, "up from the bottom edge, mm", rotation=90, ha="center", va="center", fontsize=8, color=MUT)
    ax.set_xlim(-jw / 2 - 60, jw / 2 + 10); ax.set_ylim(-50, jh + 8)
    fig.text(0.04, 0.975, "Junction box plate: hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.955, "Seen from the front (the face the box sits on). Full-size figures in mm, taken from the model. L: left as seen from the front.",
             fontsize=8.5, color=MUT, va="top")
    key = ["Band slots 3 x 15 at 51;", "  20 and 510 up", "V-block screws 4.5,", "  countersunk from the front,", "  at 18; 20 and 510 up",
           "Lug screws 5.5 at 44;", "  302 and 478 up", "Saddle screws 5.5 at 17.4;", "  100 and 230 up",
           "Barometric housing 4.5", "  at 45 L; 158 and 202 up", "", "Blank 140 x 530 x 3 mm"]
    fig.text(0.66, 0.88, "What each opening is (mm)", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, t in enumerate(key):
        fig.text(0.66, 0.855 - i * 0.02, t, fontsize=8.2, color=INK, va="top")
    foot(fig)
    fig.savefig(OUT / "plate-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "plate-holes.png")

    # junction box floor, seen from below with the back face at the top, left and right as seen from the front
    jd, jwb, _ = P["jbox"]
    jl = P["jlid"]
    names = {"hub": "Conduit hub", "lead_gland": "M16 gland, FieldNode lead", "breather": "Breather", "baro_gland": "M12 gland, barometric lead"}
    fig = plt.figure(figsize=(10, 7.5), dpi=150)
    ax = fig.add_axes([0.03, 0.08, 0.62, 0.78]); ax.set_aspect("equal"); ax.set_axis_off()
    # looking up at the floor, standing in front of the box (at the lid): +y (right as seen from the front) appears on the right
    ax.add_patch(Rectangle((-jwb / 2, 0), jwb, jd - jl, fc="#F3F4F6", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((-jwb / 2, jd - jl), jwb, jl, fc="white", ec=MUT, lw=0.8, ls="--"))
    ax.text(0, jd - jl / 2, "lid (do not drill)", ha="center", va="center", fontsize=7.5, color=MUT)
    ax.text(-jwb / 2, -3, "back face (against the plate)", ha="left", va="top", fontsize=8, color=MUT)
    ax.plot([0, 0], [-4, jd - jl], color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    keyl = []
    for i, (k, (u, v, hd, od, ln)) in enumerate(P["jentries"].items(), 1):
        ax.add_patch(Circle((v, u), od / 2, fc="none", ec=MUT, lw=0.6, ls="--"))
        ax.add_patch(Circle((v, u), hd / 2, fc="white", ec=INK, lw=1.1))
        ax.text(v, u, str(i), ha="center", va="center", fontsize=9, fontweight="bold", color="white",
                bbox=dict(boxstyle="circle,pad=0.25", fc=AC, ec="none"))
        side = "on the centre line" if abs(v) < 0.1 else f"{abs(v):g} {'right' if v > 0 else 'left'}"
        keyl.append((i, names[k], f"{hd:g} mm hole", f"{u:g} from the back face, {side}"))
    for j, (i, nm, t1, t2) in enumerate(keyl):
        fig.text(0.68, 0.80 - j * 0.11, f"{i}  {nm}", fontsize=9, fontweight="bold", color=INK, va="top")
        fig.text(0.68, 0.80 - j * 0.11 - 0.03, f"    {t1}", fontsize=8, color=INK, va="top")
        fig.text(0.68, 0.80 - j * 0.11 - 0.055, f"    {t2}", fontsize=8, color=INK, va="top")
    for r in sorted({e[0] for e in P["jentries"].values()}):
        ax.plot([-jwb / 2 - 8, -jwb / 2], [r, r], color=AC, lw=0.5, ls=":")
        ax.text(-jwb / 2 - 9, r, f"{r:g}", va="center", ha="right", fontsize=8, color=AC)
    ax.text(-jwb / 2 - 20, (jd - jl) / 2, "from the back face, mm", rotation=90, va="center", ha="center", fontsize=8, color=MUT)
    ax.set_xlim(-jwb / 2 - 26, jwb / 2 + 4); ax.set_ylim(jd + 3, -14)
    fig.text(0.03, 0.97, "Junction box floor: drilling layout", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.93, "Looking up at the floor from in front of the box. Sideways positions from the centre line, right and left as seen from the front.\n"
             "Solid circle: the hole to drill. Dashed circle: the outside of the part that goes in it.", fontsize=8.2, color=MUT, va="top")
    foot(fig)
    fig.savefig(OUT / "box-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "box-holes.png")

    # seal plate, seen from above
    sr = P["seal_d"] / 2
    spo, spi, _ = P["spigot"]
    hr, hc, ht = P["seal_holes"]
    fig = plt.figure(figsize=(10, 7.5), dpi=150)
    ax = fig.add_axes([0.05, 0.08, 0.66, 0.8]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Wedge((0, 0), sr, 0, 180, fc="#BFDBFE", ec=INK, lw=1.2))
    ax.add_patch(Wedge((0, 0), sr, 180, 360, fc="#DBEAFE", ec=INK, lw=1.2))
    ax.add_patch(Circle((0, 0), spo / 2, fc="none", ec=MUT, lw=0.7, ls="--"))
    ax.add_patch(Circle((0, 0), spi / 2, fc="none", ec=MUT, lw=0.7, ls="--"))
    ax.add_patch(Circle((0, 0), P["casing_od"] / 2, fc="none", ec="#9CA3AF", lw=0.6, ls=":"))
    ax.plot([-sr - 6, sr + 6], [0, 0], color="#B91C1C", lw=1.0, ls=(0, (6, 3)))
    ax.text(sr + 8, 0, "split line\n(saw here)", va="center", fontsize=8, color="#B91C1C")
    for x, d, nm in ((P["riser_x"], hr, "riser"), (P["pump_cable"][0], hc, "pump cable"), (P["tube_x"], ht, "access tube")):
        ax.add_patch(Circle((x, 0), d / 2, fc="white", ec=INK, lw=1.1))
    lab = [(P["riser_x"], hr, "Riser hole", -1), (P["pump_cable"][0], hc, "Pump cable hole", 1), (P["tube_x"], ht, "Access tube hole", -1)]
    for i, (x, d, nm, sgn) in enumerate(lab):
        yy = sgn * (62 + 14 * (i == 2))
        ax.annotate(f"{nm}: {d:g}, {abs(x):g} {'left' if x < 0 else 'right'} of centre", xy=(x, sgn * d / 2), xytext=(x, yy), ha="center",
                    va="center", fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.6),
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
    ax.text(0, sr - 18, "half A (back)", ha="center", fontsize=8, color=INK)
    ax.text(0, -sr + 14, "half B (front)", ha="center", fontsize=8, color=INK)
    ax.set_xlim(-sr - 10, sr + 45); ax.set_ylim(-sr - 8, sr + 8)
    fig.text(0.03, 0.97, "Seal plate: holes and split line, seen from above", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.93, "200 mm disc of 20 mm HDPE. Dashed: the 148 mm spigot ring screwed underneath (inside 128 mm). Dotted: the casing outside (168 mm).\n"
             "All three holes are on the split line; measure your riser and pump cable and change the holes to suit.", fontsize=8.2, color=MUT, va="top")
    key = ["Hole = part + 2 mm of", "EPDM wrap each side", "", f"Riser 42.2 > hole {hr:g}", f"Pump cable 12 > hole {hc:g}",
           f"Tube 33.4 > hole {ht:g}", "", "Spigot half rings: three", "4 x 16 stainless screws each"]
    fig.text(0.74, 0.8, "Sizes (mm)", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, t in enumerate(key):
        fig.text(0.74, 0.77 - i * 0.03, t, fontsize=8.2, color=INK, va="top")
    foot(fig)
    fig.savefig(OUT / "seal-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "seal-holes.png")
    return res


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "WellSense prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules wired at block level; no circuit board is laid out. Stranded copper; ferrules on every screw terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, REPO, fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((30, 11), 66, 50, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(31.5, 59.8, "In the junction box, on the internal plate", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, GRN = "#B91C1C", "#1D4ED8", "#6B7280", "#15803D"
    blk(3, 42, 20, 15, "FieldNode core", "port A (M12, 5 pin):\n12 V switched rail,\nground, I2C", "#115E59")
    blk(3, 14, 20, 14, "Transducer", "4 to 20 mA, two wire,\n12 to 30 V; vent tube\nin the cable", "#0F766E")
    blk(36, 44, 18, 12, "Surge and reverse", "TVS on the 12 V in,\nSchottky diode", "#15803D")
    blk(60, 44, 16, 12, "Boost module", "12 V to 24 V,\nloop supply", "#16A34A")
    blk(80, 44, 14, 12, "3.3 V regulator", "for the ADC and\nbarometric sensor", "#15803D")
    blk(60, 24, 16, 12, "Shunt 150 ohm", "0.1 %, 10 ppm/K,\nin the loop return", "#0F766E")
    blk(80, 24, 14, 12, "ADC", "16 bit, ADS1115\nclass, series\ninput resistor", "#0F766E")
    blk(100, 24, 17, 12, "Barometric sensor", "in its housing on\nthe plate, 0.3 m lead", "#7C3AED")
    blk(36, 14, 18, 7, "Terminal strip", "", "#7C3AED")
    # 12 V in from FieldNode through the M12 lead
    wire([(23, 50), (36, 50)], RED); lab(24, 52.5, "12 V and ground,\nFieldNode lead 0.2 mm²", RED)
    wire([(54, 50), (60, 50)], RED); lab(57, 52.5, "0.5 mm²", RED, "center")
    wire([(76, 50), (80, 50)], RED)
    wire([(68, 44), (68, 40), (45, 40), (45, 21)], RED); lab(46, 38.5, "24 V loop +, 0.5 mm²", RED)
    wire([(23, 21), (36, 21)], RED); lab(24, 23.3, "loop + and -,\nvented cable cores", RED)
    wire([(45, 14), (45, 11.5), (68, 11.5), (68, 24)], RED); lab(50, 13.2, "loop - to the shunt", RED)
    wire([(76, 30), (80, 30)], BLU); lab(78, 32.5, "shunt volts", BLU, "center")
    wire([(87, 44), (87, 36)], GRN); lab(87.6, 40, "3.3 V", GRN)
    wire([(94, 50), (108, 50), (108, 36)], GRN); lab(100, 52.5, "3.3 V", GRN)
    wire([(87, 24), (87, 9), (1.3, 9), (1.3, 46), (3, 46)], BLU); lab(40, 7.2, "I2C (SDA, SCL), 0.25 mm², back up the FieldNode lead", BLU)
    wire([(108, 24), (108, 9), (87, 9)], BLU)
    ax.text(2, 64, "Safety: extra-low voltage only (24 V highest). The pump's mains wiring stays outside this box.", fontsize=7.6,
            color="#B45309", fontweight="bold", ha="left", va="top")
    ax.text(30, 4.2, "Red: power and loop. Blue: signal. Green: 3.3 V. The vent tube in the cable ends open inside the box, which breathes through the desiccant.",
            fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        name, _, sel = w.partition(":")
        if sel:
            r = fns[name]({int(x) for x in sel.split(",")})
        else:
            r = fns[name]()
        print(w, "->", r)
