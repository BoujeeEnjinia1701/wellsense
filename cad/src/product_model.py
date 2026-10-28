"""WellSense product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3, kit 1.9.

Every product part is components(CHOSEN) from cad/src/model.py as it is, at its installed position: the split
seal plate with its spigot rings, gasket, wraps, rim band, collar and clevis pin; the drilled PVC tube cap with the
eye bolt, support grip and padlock; the flexible tail, bent rigid conduit, saddles and their bolts; the post with
its cap; the junction box plate, V-blocks, band clamps and their screws; the junction box body, clear lid, lugs,
glands, breather, hasp and padlock; the internal plate with the boost, ADC and regulator boards on standoffs and
the terminal strip; the barometric housing; the FieldNode core with its bands; the FieldNode lead. Parts that go
below ground (access tube, vented cable, post) are cut 150 mm below ground, so the camera frames the wellhead
and the logger; the probe and the drilled foot of the tube are underground and not drawn. Only the site is added,
as context parts: the existing steel casing and its concrete apron, the pump's riser and discharge pipe, and a
1.75 m mannequin standing on the ground beside the well. Ground level is model z = 0 (photoreal --ground-z=0);
every site part reaches below it.
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (the logger as installed), "context" (site and mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402

TITLE = "WellSense: well and borehole water level logger"
Z_CUT = -150.0

_SITE = ["--scene=outdoor", "--ground=soil", "--ground-z=0", "--sun=42,-75", "--lens=50"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "context"], "explode": False, "el": 14, "az": -40, "args": _SITE,
     "note": "Site render at a village borehole from the front right, a little above (about 14 deg elevation): the split "
             "seal plate on the existing casing and apron, padlocked tube cap, conduit to the junction box on the post and "
             "the FieldNode core with its panel at the top; 1.75 m person standing beside the well for scale"},
    {"name": "studio", "groups": ["shell"], "explode": False, "el": 20, "az": -40,
     "note": "Studio render from the front right and above (about 20 deg elevation): wellhead, conduit, junction box with "
             "the boards behind its clear lid, barometric housing and the FieldNode core on the post"},
    {"name": "exploded", "groups": ["shell"], "explode": True, "el": 22, "az": -55,
     "note": "Exploded view from the front right and above (about 22 deg elevation): wellhead parts lifted off the "
             "casing, tube cap and padlock above them, junction box lid and boards pulled toward the well, FieldNode "
             "core lifted off the post"},
]

EXPLODE = {"seal": (0, 0, 220), "cap": (0, 0, 420), "conduit": (120, -200, 0), "jbox": (160, 0, 0), "board": (300, 0, 0),
           "baro": (120, -150, 0), "fieldnode": (0, -250, 250), "lead": (0, -120, 0)}


def _clip(shape):
    keep = M.bx(-5000, 5000, -5000, 5000, Z_CUT, 6000)
    bb = shape.bounding_box()
    if bb.min.Z >= Z_CUT:
        return shape
    if bb.max.Z < Z_CUT:
        return None
    s = shape & keep
    return s if s is not None and s.volume > 1e-3 else None


def site():
    """Site context: the existing casing and its apron, the pump riser and discharge pipe, and a mannequin. Every
    site part reaches below ground (z = 0)."""
    P = M.PARAMS
    out = []
    ctx = lambda n, sh, mat: out.append(part(f"{n} (site)", sh, mat, kind="context", group="context"))  # noqa: E731
    ctx("Existing steel casing", M.ring(P["casing_od"] / 2, P["casing_id"] / 2, -600.0, P["stickup"]), "mild_steel")
    ad, at = P["apron"]
    ctx("Existing concrete apron", break_edges(M.ring(ad / 2, P["casing_od"] / 2 + 1, -100.0, at), 6), "concrete")
    rx, rr, st = P["riser_x"], P["riser_od"] / 2, P["stickup"]
    riser = M.cyl(rr, -600.0, st + 170, x=rx) + M.tube((rx, 0, st + 150), (rx, 520, st + 150), rr) + M.cyl(rr, -600.0, st + 170, x=rx, y=520)
    ctx("Existing pump riser and discharge", riser, "galvanised")
    cx_, cd_ = P["pump_cable"]
    ctx("Existing pump cable", M.cyl(cd_ / 2, -600.0, st + 160, x=cx_) + M.tube((cx_, 0, st + 160), (cx_, 300, st + 160), cd_ / 2), "epdm")
    try:
        import context_parts
        man = Pos(650, -900, 0) * Rot(0, 0, 150) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        if p["kind"] == "context":
            continue
        s = _clip(p["shape"])
        if s is None:
            continue
        q = dict(p)
        q["shape"], q["explode"] = s, EXPLODE.get(p["group"], (0, 0, 0))
        q["src_group"], q["group"] = p["group"], "shell"
        out.append(q)
    return out + site()


if __name__ == "__main__":
    ps = product_parts()
    print(len(ps), "parts;", sum(p["group"] == "shell" for p in ps), "shell,", sum(p["group"] == "context" for p in ps), "context")
