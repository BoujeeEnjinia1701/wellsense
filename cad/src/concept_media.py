"""WellSense concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes the parts from cad/src/model.py (PARAMS), colors and numbers them to match bom/bom.csv,
adds the existing well (grey, no BOM number) as context and renders the media set with
.kit/concept.py. Figures on the sheet and in the flow diagram come from
docs/04-calcs/sizing.py (WLS-CAL-001). CONCEPT, NOT FOR FABRICATION.

Coordinates in mm. Ground surface at Z = 0, well axis at X = Y = 0. The borehole is shortened
for display: the model shows about 2.6 m of casing, while the design probe hangs 30 m (to 60 m)
below the wellhead.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Box, Pos  # noqa: E402
import concept  # noqa: E402
from concept import Part, render_all, human_figure  # noqa: E402
from model import BOM, CONTEXT, build_parts  # noqa: E402


def box(cx, cy, cz, dx, dy, dz):
    return Pos(cx, cy, cz) * Box(dx, dy, dz)


S = build_parts()
EXPLODE = {"probe": (-340, -212, 500), "cable": (-187, -117, 0), "tube": (255, 159, 0), "seal": (0, 0, 350),
           "cap": (128, 80, 300), "jbox": (300, -250, -150), "board": (380, -330, 0), "fieldnode": (-255, -159, 250),
           "baro": (-298, -186, -120), "post": (0, 0, 0), "footing": (0, 0, -300),
           "conduit": (60, -420, -320)}
parts = [Part(CONTEXT[k][0], S[k], CONTEXT[k][1], None) for k in ("casing", "apron", "pump", "water")]
for k, (n, name, color) in BOM.items():
    parts.append(Part(name, S[k], color, n, EXPLODE[k]))

person = human_figure(1750.0, x=350.0, y=700.0, z=0.0)

render_all(
    parts, project="WellSense", title="Well water level logger concept", dwg_no="WLS-DWG-010",
    key_figures=["Vented 4 to 20 mA transducer, 22 mm, 0 to 10 m, 24 V loop (WLS-CAL-001)",
                 "Resolution 0.52 mm; 12.5 mm RSS after two-point tape calibration",
                 "Probe 30 m design case, to 60 m; borehole shortened for display",
                 "15 min readings; 38 mWh/day, 1.6 % of the FieldNode allowance",
                 "Parts $197.60 at 30 m (budget $190); $323.60 with FieldNode"],
    scale_figure=False, context=[person],
    cut=False,
    flow={"title": "data flow (estimated values, WLS-CAL-001)", "unit": "",
          "stages": [("Water over probe", "0 to 10 m head"),
                     ("Transducer", "4 to 20 mA, 24 V"),
                     ("Interface board", "16 bit, 0.52 mm"),
                     ("FieldNode", "1.43 J per reading"),
                     ("LoRaWAN uplink", "20 B, 0.25 s at SF9"),
                     ("Dashboard", "level and trend")]},
)

# Hero: re-render with a soil block cut open on the viewer's side, so the well shows in section.
notch = box(900, -900, -1300, 1800, 1800, 3000)
soil_dry = box(0, 0, -600, 2000, 2000, 1200) - notch
soil_wet = box(0, 0, -1900, 2000, 2000, 1400) - notch
hero_parts = [Part("Unsaturated soil", soil_dry, "#C8A97E", None),
              Part("Saturated aquifer", soil_wet, "#8C7B68", None)]
for p in parts:
    try:
        s = p.shape - notch
        if s.volume > 1e-6:
            hero_parts.append(Part(p.name, s, p.color, p.bom))
    except Exception:
        hero_parts.append(p)
hero_parts.append(person)
concept._render(hero_parts, concept.ROOT / "media" / "hero.png", title="WellSense",
                note="Grey figure: 1.75 m person for scale. Soil cut open to show the well; "
                     "borehole shortened for display (design probe depth 30 m, to 60 m).")

# Cutaway: broken section. Left, the wellhead (-0.9 to +0.8 m); right, the lower borehole around the
# water level and probe, moved up and across so both fit one image at a readable scale.
keep_names = {"Existing casing, 150 mm (not in kit)", "Existing concrete apron", "Existing pump and riser (not in kit)",
              "Well water (static level shown)", "Pressure transducer, vented, 4 to 20 mA",
              "Vented cable with desiccant end", "Access tube, 25 mm PVC, slotted",
              "Wellhead seal plate and glands", "Tube cap and cable hanger", "Surface cable conduit, galvanized"}
half = box(0, 2500, 0, 6000, 5000, 8000)          # keep y >= 0; the viewer looks from -Y
halves = []
for p in parts:
    if p.name in keep_names:
        cut_shape = p.shape & half
        if cut_shape is not None and cut_shape.volume > 1e-6:
            halves.append(Part(p.name, cut_shape, p.color, p.bom))
upper_win = box(0, 0, -50, 640, 2000, 1700)       # x -320..320, z -900..800
lower_win = box(0, 0, -1760, 640, 2000, 1420)     # z -2470..-1050
SHIFT = Pos(780, 0, 1450)
cut_parts = []
for p in halves:
    for win, move, lower in ((upper_win, None, False), (lower_win, SHIFT, True)):
        try:
            s = p.shape & win
        except Exception:
            continue
        if s is None or s.volume < 1e-6:
            continue
        if move is not None:
            s = move * s
        bom = p.bom if (p.bom == 1) == lower else None
        cut_parts.append(Part(p.name, s, p.color, bom))
concept._render(cut_parts, concept.ROOT / "media" / "cutaway.png", elev=12, azim=-90, labels=True,
                title="WellSense: cutaway (broken section)",
                note="Left: wellhead. Right: lower borehole with water level and probe, moved up for display.\n"
                     "Grey: existing well, pump and riser (not in kit).")

# remove temporary view folders left by the renderer
import shutil
for d in (concept.ROOT / "media").glob("_views*"):
    shutil.rmtree(d, ignore_errors=True)
