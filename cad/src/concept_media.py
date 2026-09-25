"""WellSense concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; CONCEPT, NOT FOR FABRICATION.

Coordinates in mm. Ground surface at Z = 0, well axis at X = Y = 0. The existing well
(casing, apron, pump and riser) is grey and carries no BOM number; WellSense parts are colored.
The borehole is shortened for display: the model shows about 2.4 m of casing, while a real
probe may hang 10 to 60 m below the wellhead.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
import concept
from concept import Part, render_all, human_figure

# ---------------- well geometry (existing, grey) ----------------
CASING_OD, CASING_ID = 168.0, 150.0        # 6 in steel or PVC casing
CASING_TOP, CASING_BOT = 450.0, -2400.0    # 450 mm stick-up above ground
WATER_Z = -1200.0                          # static water level (display)
TUBE_X = 48.0                              # access tube offset from well axis
TUBE_OD, TUBE_ID = 33.4, 26.6              # 1 in PVC access (stilling) tube
TUBE_TOP, TUBE_BOT = 560.0, -2050.0
PROBE_R, PROBE_L = 12.0, 170.0             # 24 mm stainless transducer body
PROBE_BOT = -2010.0
PUMP_X = -24.0
POST_X = -750.0                            # 48 mm pole beside the apron

GREY = "#9CA3AF"
CONCRETE = "#C9C5BC"
WATER = "#60A5FA"


def cyl(r, z0, z1, x=0.0, y=0.0):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def box(cx, cy, cz, dx, dy, dz):
    return Pos(cx, cy, cz) * Box(dx, dy, dz)


casing = cyl(CASING_OD / 2, CASING_BOT, CASING_TOP) - cyl(CASING_ID / 2, CASING_BOT - 1, CASING_TOP + 1)
apron = cyl(600, 0, 100) - cyl(CASING_OD / 2 + 1, -1, 101)
pump = cyl(48, -2350, -1850, x=PUMP_X)
riser = cyl(21, -1850, 620, x=PUMP_X)
discharge = tube3((PUMP_X, 0, 600), (PUMP_X, 520, 600), 21) + cyl(21, 380, 620, x=PUMP_X, y=520)
existing_pump = pump + riser + discharge

# 3 Access (stilling) tube, slotted at the bottom, keeps the probe clear of the pump and riser
access_tube = cyl(TUBE_OD / 2, TUBE_BOT, TUBE_TOP, x=TUBE_X) - cyl(TUBE_ID / 2, TUBE_BOT - 1, TUBE_TOP + 1, x=TUBE_X)

# water inside the casing, with the pump, riser and tube taken out
water = (cyl(CASING_ID / 2 - 0.5, CASING_BOT + 5, WATER_Z) - cyl(49, -2360, -1840, x=PUMP_X)
         - cyl(22, -1850, WATER_Z + 5, x=PUMP_X) - cyl(TUBE_OD / 2 + 0.5, TUBE_BOT - 5, WATER_Z + 5, x=TUBE_X))

# 1 Submersible pressure transducer, hung inside the access tube
probe = cyl(PROBE_R, PROBE_BOT, PROBE_BOT + PROBE_L, x=TUBE_X)

# 2 Vented cable: up the access tube, over the hanger, across to the junction box on the post
JB_X, JB_Z = POST_X + 24 + 45, 1040.0
cable = (tube3((TUBE_X, 0, PROBE_BOT + PROBE_L), (TUBE_X, 0, 640), 3.5)
         + tube3((TUBE_X, 0, 640), (TUBE_X - 60, 0, 700), 3.5)
         + tube3((TUBE_X - 60, 0, 700), (JB_X + 20, 0, 700), 3.5)
         + tube3((JB_X + 20, 0, 700), (JB_X + 20, 0, JB_Z - 80), 3.5))

# 4 Wellhead seal plate with two cable and tube glands
seal_plate = (cyl(CASING_OD / 2 + 16, CASING_TOP, CASING_TOP + 25)
              - cyl(22, CASING_TOP - 1, CASING_TOP + 26, x=PUMP_X)
              - cyl(TUBE_OD / 2 + 0.5, CASING_TOP - 1, CASING_TOP + 26, x=TUBE_X))

# 5 Tube cap with cable grip hanger
hanger = cyl(24, TUBE_TOP, TUBE_TOP + 45, x=TUBE_X) + cyl(8, TUBE_TOP + 45, TUBE_TOP + 75, x=TUBE_X)

# 10 Mounting post (48 mm galvanized pole), set in the ground beside the apron, with two band clamps
post = (cyl(24, -500, 1850, x=POST_X)
        + cyl(30, 1000, 1030, x=POST_X) + cyl(30, 1480, 1510, x=POST_X))

# 6 Junction box with desiccant breather for the cable vent tube
jbox = box(JB_X, 0, JB_Z, 90, 120, 160) + cyl(20, JB_Z - 80 - 90, JB_Z - 80, x=JB_X - 20, y=35)

# 7 4 to 20 mA interface board (shunt, 16-bit ADC, surge protection), inside the junction box
board = box(JB_X, 0, JB_Z + 10, 10, 70, 90)

# 8 FieldNode core: IP65 enclosure, 6 W panel hood and antenna
NODE_X, NODE_Z = POST_X + 24 + 50, 1560.0
fieldnode = (box(NODE_X, 0, NODE_Z, 90, 150, 200)
             + cyl(6, NODE_Z + 100, NODE_Z + 260, x=NODE_X + 25, y=60)
             + Pos(POST_X + 30, -20, NODE_Z + 175) * Rot(-28, 0, 0) * Box(210, 290, 25))

# 9 Barometric reference sensor in a small vented housing under the node
baro = cyl(20, NODE_Z - 100 - 50, NODE_Z - 100, x=NODE_X + 10, y=-40)

parts = [
    Part("Existing casing, 150 mm (not in kit)", casing, GREY, None),
    Part("Existing concrete apron", apron, CONCRETE, None),
    Part("Existing pump and riser (not in kit)", existing_pump, "#6B7280", None),
    Part("Well water (static level shown)", water, WATER, None),
    Part("Pressure transducer, vented, 4 to 20 mA", probe, "#0F766E", 1, (-340, -212, 600)),
    Part("Vented cable with desiccant end", cable, "#111827", 2, (-187, -117, 0)),
    Part("Access tube, 25 mm PVC, slotted", access_tube, "#E5E7EB", 3, (255, 159, 0)),
    Part("Wellhead seal plate and glands", seal_plate, "#2563EB", 4, (0, 0, 350)),
    Part("Tube cap and cable hanger", hanger, "#D4A017", 5, (128, 80, 600)),
    Part("Junction box with desiccant breather", jbox, "#94A3B8", 6, (-383, -239, 0)),
    Part("4 to 20 mA interface board", board, "#16A34A", 7, (-213, -133, -250)),
    Part("FieldNode core (enclosure, panel, radio)", fieldnode, "#115E59", 8, (-255, -159, 250)),
    Part("Barometric reference sensor", baro, "#7C3AED", 9, (-298, -186, -120)),
    Part("Mounting post and clamps", post, "#A16207", 10, (0, 0, 0)),
]

person = human_figure(1750.0, x=350.0, y=700.0, z=0.0)

render_all(
    parts, project="WellSense", title="Well water level logger concept", dwg_no="WLS-DWG-010",
    key_figures=["Vented 4 to 20 mA transducer, 0 to 10 m range (proposed)",
                 "Resolution about 0.5 mm; accuracy about 50 mm before field check (estimate)",
                 "Probe to 60 m on vented cable; borehole shortened for display",
                 "15 min readings; sensor energy about 18 mWh/day (estimate)",
                 "Parts about $170, or about $296 with FieldNode (indicative)"],
    scale_figure=False, context=[person],
    cut=False,
    flow={"title": "data flow (estimated values)", "unit": "",
          "stages": [("Water over probe", "0 to 10 m head"),
                     ("Transducer", "4 to 20 mA, 2 s on"),
                     ("FieldNode ADC", "16 bit, 15 min"),
                     ("LoRaWAN uplink", "about 20 B each"),
                     ("Server", "96 readings/day"),
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
                     "borehole shortened for display (real probe depth 10 to 60 m).")

# Cutaway: broken section. Left, the wellhead (-0.9 to +0.8 m); right, the lower borehole around the
# water level and probe, moved up and across so both fit one image at a readable scale.
keep_names = {"Existing casing, 150 mm (not in kit)", "Existing concrete apron", "Existing pump and riser (not in kit)",
              "Well water (static level shown)", "Pressure transducer, vented, 4 to 20 mA",
              "Vented cable with desiccant end", "Access tube, 25 mm PVC, slotted",
              "Wellhead seal plate and glands", "Tube cap and cable hanger"}
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
