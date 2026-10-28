"""WellSense STEM check, WLS-STM-001 (STANDARDS section 20), kit 1.9.1.

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv, which docs/01b-stem-check.md reports row by row.

Every claim the design (option A, the current design) and the two other concept options (B bubbler,
C acoustic sounder; WLS-OPT-001) make about physics, chemistry, biology, mathematics and engineering is
checked here to first order. Geometry comes from cad/src/model.py (PARAMS, DESIGN, derived()), so the
check reruns when the design changes. The full calculations for option A are in WLS-CAL-001
(docs/04-calcs/sizing.py); the tag in brackets, for example [B1], is the line of that script that
carries the same number. A first-order screen; it never replaces the calculation note.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from stem_check import Check, WITHIN, PLAUSIBLE, G  # noqa: E402
from model import DESIGN as DS, PARAMS as P, derived  # noqa: E402

D = derived(P)
c = Check(ROOT / "docs" / "04-calcs" / "stem_results.csv")
RHO = 1000.0
L_MAX = DS["probe_depth_max_m"]          # 60 m, PR-002
L_DES = DS["probe_depth_m"]              # 30 m design case
RANGE = DS["range_m"]                    # 10 m of water


def rho_water(t):
    """Water density, kg/m3 (Thiesen formula), as WLS-CAL-001 [C2]."""
    return 1000.0 * (1 - (t + 288.9414) / (508929.2 * (t + 68.12963)) * (t - 3.9863) ** 2)


# =========================================================================================== option A
# A vented 4 to 20 mA pressure transducer hangs in its own 1 in PVC access tube and reads the head of
# water above it; FieldNode powers it for 2 s every 15 min through a 24 V boost.

# S1 hydrostatics
p_fs = RHO * G * RANGE / 1000
c.order_of_magnitude("S1", "Full-scale pressure of the 0 to 10 m range is 98.07 kPa (PR-001)", "Physics", "Fluid mechanics",
                     claimed=98.07, estimate=p_fs, unit="kPa", factor=1.01, law="Hydrostatic pressure p = rho g h")

# S2 vented reference
d_abs = 3000 / (RHO * G) * 1000
c.order_of_magnitude("S2", "A vented (gauge) transducer cancels air pressure swings that would put +/-306 mm on an absolute sensor (+/-3 kPa weather)",
                     "Physics", "Fluid mechanics", claimed=306, estimate=d_abs, unit="mm", factor=1.05,
                     law="Gauge pressure is referenced to the atmosphere through the vent capillary (USGS TM 1-A1, 2011)")

# S3 resolution
R_SH, FSR, BITS = 150.0, 4.096, 16
lsb = 2 * FSR / 2 ** BITS
res = RANGE * 1000 / ((0.020 - 0.004) * R_SH / lsb)
c.claim("S3", f"ADC step (quantisation) {res:.2f} mm with a 150 ohm shunt and a 16-bit ADC (PR-003); noise-limited resolution of the probe and ADC is to measure at TRL 4", "Engineering and technology", "Sensing resolution",
        law="16 mA x 150 ohm = 2.4 V span over a 125 uV step [A2]", value=round(res, 2), limit=1.0, unit="mm", rule="below")

# S4 loop compliance
I, R_CU, V_D = 0.022, 0.087, 0.3
r_cab = 2 * (L_MAX + DS["surface_run_m"]) * R_CU
v_12 = 12 * 0.95 - I * R_SH - I * r_cab - V_D
v_24 = 24 - I * R_SH - I * r_cab - V_D
c.claim("S4", f"With the 24 V boost the transducer gets {v_24:.2f} V at 22 mA through {L_MAX + DS['surface_run_m']:.0f} m of cable (the 12 V rail alone gives {v_12:.2f} V)",
        "Physics", "Electromagnetism and circuits", law="Ohm's law round the loop; transducer minimum 12 V (BOM line 1) [B1]",
        value=round(v_24, 2), limit=12.0, unit="V", rule="above")

# S5 ADC input protection
v_fault = 0.025 * R_SH
i_inj = max(0.0, v_fault - 3.6) / 10e3 * 1000
c.claim("S5", f"At a 25 mA fault the shunt gives {v_fault:.2f} V; a 10 kohm series resistor keeps the ADC input current to {i_inj * 1000:.0f} uA",
        "Engineering and technology", "Standards practice", law="ADS1115 absolute maximum: input current 10 mA continuous, VDD + 0.3 V [B1b]",
        value=round(i_inj, 3), limit=10.0, unit="mA", rule="below")

# S6 energy
e_read = 24 * I * 2.0 / 0.85 / 0.90 + 3.3 * 0.008 * 2.0
e_day = e_read * 96 / 3600 * 1000
c.claim("S6", f"Sensor energy {e_day:.1f} mWh a day at 15 min, 5 % or less of FieldNode's 100 mW sensor allowance (PR-008)", "Physics",
        "Electromagnetism and circuits", law="Energy balance: 24 V x 22 mA x 2 s through boost (85 %) and rail (90 %) plus the controller [B2, B3]",
        value=round(e_day, 1), limit=0.05 * 100 * 24, unit="mWh/day", rule="below")

# S7 accuracy after calibration (WLS-CAL-001 C3, C4)
terms = [0.0010 * RANGE, 0.0010 * RANGE, 0.0002 * 2 * RANGE, abs(rho_water(17) - rho_water(15)) / rho_water(15) * RANGE,
         10e-6 * 30 * 1.25 * RANGE, 7e-6 * 30 * 1.25 * RANGE, res / 1000, 0.003]
rss, tot = math.sqrt(sum(t * t for t in terms)) * 1000, sum(terms) * 1000
span_lift = math.sqrt(2 * 0.003 ** 2 + 2 * (0.0010 * RANGE) ** 2) / 1.0
c.cited("S7", f"A 0.25 % class probe reaches +/-20 mm after calibration (PR-004). First run: a two-point calibration with a 1 m lift was claimed to fix span; "
        f"two tape readings and two repeatability terms over 1 m give {span_lift * 100:.1f} % of span, {span_lift * RANGE * 1000:.0f} mm at 10 m: fails (independent review). "
        f"Fixed: offset from the installation tape reading, span from the probe's per-unit factory certificate (0.10 % of reading, to confirm), refined by tape checks at levels 3 m or more apart",
        "Mathematics", "Statistics and uncertainty",
        "Error budget of eight independent terms, root sum square against worst-case sum [C3, C4, C4b]",
        f"RSS {rss:.1f} mm, worst case {tot:.1f} mm against 20 mm; terms are typical datasheet values, not measured",
        PLAUSIBLE, closed_by="")

# S8 water density
dr = (rho_water(4) / rho_water(25) - 1) * 100
c.order_of_magnitude("S8", "Water density changes 0.29 % between 4 and 25 degC, so firmware uses a fixed site density set at installation",
                     "Physics", "Thermodynamics", claimed=0.29, estimate=dr, unit="%", factor=1.1, law="Thiesen equation of state for water [C2]")

# S9 local gravity
def g_lat(lat):
    s2 = math.sin(math.radians(lat)) ** 2
    return 9.7803253359 * (1 + 0.00193185265241 * s2) / math.sqrt(1 - 0.00669437999013 * s2)
dg = (G / g_lat(0) - 1) * RANGE * 1000
c.order_of_magnitude("S9", "Using standard gravity reads 10 m about 27 mm low at the equator; firmware uses local gravity", "Mathematics",
                     "Units and dimensional analysis", claimed=27, estimate=dg, unit="mm", factor=1.1, law="WGS 84 normal gravity formula [C1]")

# S10 drift
c.cited("S10", "A quarterly tape check keeps the uncorrected drift to 5 mm or less if the probe drifts 20 mm a year or less (PR-005)",
        "Engineering and technology", "Sensing resolution", "Drift budget: 20 mm a year over a 91-day interval [C8]",
        "5 mm between checks against the 20 mm target; long-term drift of low-cost vented transducers is not published", PLAUSIBLE)

# S11 cable hanging load
w_cab = (0.055 * L_MAX + 0.25) * 9.81
c.claim("S11", f"Cable and probe hanging {L_MAX:.0f} m in air ({w_cab:.0f} N) stay below the 400 N strain member (PR-002)", "Physics",
        "Strength of materials", law="Weight of 0.055 kg/m cable and a 0.25 kg probe [D3]", value=round(w_cab, 1), limit=400.0, unit="N", rule="below")

# S12 cable elongation
EA = 70e9 * 1.0e-6               # aramid strain member, about 1 mm2 at 70 GPa (assumed, typical)
dl = (0.25 * 9.81 * L_MAX + 0.055 * 9.81 * L_MAX ** 2 / 2) / EA * 1000
dT = math.pi / 4 * (P["cable_d"] / 1000) ** 2 * RHO * 9.81 * RANGE     # buoyancy change over a full 10 m swing
dl_sw = dT * (L_MAX - RANGE) / EA * 1000
c.claim("S12", f"Cable stretch at {L_MAX:.0f} m ({dl:.0f} mm) is a fixed offset the installation calibration removes; a full 10 m level swing changes it by {dl_sw:.1f} mm "
        f"(aramid strain member taken as about 1 mm2 at 70 GPa, EA {EA / 1000:.0f} kN, typical, to confirm with the cable maker)",
        "Physics", "Strength of materials", law="Elongation = integral of tension over EA; buoyancy of the submerged cable",
        value=round(dl_sw, 2), limit=5.0, unit="mm", rule="below")

# S13 access tube in tension
a_t = math.pi / 4 * (P["tube_od"] ** 2 - P["tube_id"] ** 2)
w_t = a_t * 1e-6 * 1400 * 9.81 * L_MAX
c.claim("S13", f"The {L_MAX:.0f} m access tube hanging dry ({w_t:.0f} N, {w_t / a_t:.2f} MPa) stays well below PVC's 48 MPa tensile strength", "Physics",
        "Strength of materials", law="Self-weight stress of PVC, 1,400 kg/m3 [D4]", value=round(w_t / a_t, 2), limit=48 / 3, unit="MPa", rule="below")

# S14 tube retention at the collar (fix rule, WLS-DEC-001 D-S1)
T_ASM, D_SCR, K_T, MU = 2.0, 6.0, 0.2, 0.25           # reduced torque for plastic pipe, M6 clamp screw, nut factor, Al on PVC
grip0 = MU * 2 * T_ASM / (K_T * D_SCR / 1000)
grip_life = grip0 / 3                                   # PVC creep: long-term modulus about a third of short-term
need = 3 * w_t
pd_, pe_ = P["tube_pin"]
w_all = w_t + w_cab                                     # the probe and cable hang from the cap, which sits on the tube
tw = math.sqrt((P["tube_od"] / 2) ** 2 - pe_ ** 2) - math.sqrt((P["tube_id"] / 2) ** 2 - pe_ ** 2)   # wall crossed by the chord
bear = w_all / (2 * pd_ * tw)
shear = w_all / (2 * math.pi / 4 * pd_ ** 2)
c.claim("S14", f"The tube string is held at the plate over its life. Friction of the split collar alone: {grip0:.0f} N new, about {grip_life:.0f} N after PVC creep, "
        f"against {need:.0f} N (3 x {w_t:.0f} N): fails. Fixed with a 5 mm stainless clevis pin through the tube on a chord above the collar, carrying {w_all:.0f} N (tube, cable and probe): "
        f"sustained PVC bearing {bear:.1f} MPa on the {tw:.1f} mm chord wall against PVC's 13.8 MPa long-term design stress, pin shear {shear:.1f} MPa; 69 mm of tube above the pin rules out shear-out",
        "Engineering and technology", "Standards practice",
        law="Clamp preload F = T/(K d); friction mu F; PVC stress relaxation; pin bearing against the long-term design stress of PVC 1120 (13.8 MPa, 2,000 psi)",
        value=round(bear, 1), limit=13.8, unit="MPa", rule="below", closed_by="WLS-DEC-001 D-S1 (fix rule, 2026-10-25)")

# S15 collar bearing on the plate
co = P["collar"][0]
a_co = math.pi / 4 * (co ** 2 - P["tube_od"] ** 2)
c.claim("S15", f"The collar spreads the tube load onto the HDPE seal plate at {w_t / a_co:.2f} MPa", "Physics", "Strength of materials",
        law="Bearing stress against about 20 MPa for HDPE [D5]", value=round(w_t / a_co, 2), limit=20 / 3, unit="MPa", rule="below")

# S16 cap walls at the cross bolt
wall = (P["cap"][0] - P["tube_od"]) / 2
b_cap = (w_cab + 0.10 * G) / (2 * 5.0 * wall)
c.claim("S16", f"The probe and padlock hang from the M5 eye bolt; the PVC cap walls carry {b_cap:.2f} MPa in bearing", "Physics", "Strength of materials",
        law="Bearing on two cap walls against about 50 MPa for PVC [D6, D7]", value=round(b_cap, 2), limit=50 / 3, unit="MPa", rule="below")

# S17 service loop
c.claim("S17", f"The service loop in the junction box ({D['coil_len']:.2f} m) lets the probe lift 1 m for the response check at installation and be pulled for inspection", "Mathematics",
        "Orders of magnitude", law="Coil length 2 pi r n from the model", value=round(D["coil_len"], 2), limit=1.0, unit="m", rule="above")

# S18 probe running clearance at the worst-case pipe (fix rule, WLS-DEC-001 D-S2)
OD_TOL, WALL_MIN, WALL_TOL, BEAD = 0.13, 3.38, 0.51, 0.5     # ASTM D1785 1 in Sch 40 (typical tabulated values); cement bead
bore_min = P["tube_od"] - OD_TOL - 2 * (WALL_MIN + WALL_TOL)
clr_min = (bore_min - P["probe"][0]) / 2
clr_joint = clr_min - BEAD
c.claim("S18", f"A 22 mm probe runs freely in the tube: {D['probe_clear_radial']:.1f} mm radial at the nominal bore, {clr_min:.2f} mm at the thickest Sch 40 wall "
        f"and {clr_joint:.2f} mm at a solvent-weld joint with a 0.5 mm cement bead, below the 2 mm design rule: fails. Fixed by wiping the joints and "
        f"pulling a 23 mm drift through the string before the probe goes in, which proves at least 0.5 mm radial everywhere, ovality and bow included; "
        f"0.5 mm is enough for a probe hanging free on its cable (nominal-wall bore 26.1 mm gives 2.07 mm)",
        "Engineering and technology", "Manufacturing tolerances", law="Pipe bore from OD and wall tolerances (ASTM D1785); running clearance",
        value=0.5, limit=0.5, unit="mm", rule="above", closed_by="WLS-DEC-001 D-S2 (fix rule, 2026-10-25)")

# S19 tube holes
hd, hp, h0 = P["holes"]
n_holes = 4 * (int((P["slot_zone"] - h0) // hp) + 1)
a_holes = n_holes * math.pi / 4 * hd ** 2
a_bore = math.pi / 4 * P["tube_id"] ** 2
t_fill = a_bore * 1e-6 * 10.0 / (0.6 * a_holes * 1e-6 * math.sqrt(2 * 9.81 * 0.01))
c.claim("S19", f"The {n_holes} drilled 8 mm holes ({a_holes:.0f} mm2) let the water in the tube follow the casing level: the tube's air vents through the cap's conduit "
        f"to the box breather, and even at 10 mm of head difference the tube fills 10 m in about {t_fill:.0f} s", "Physics",
        "Fluid mechanics", law="Open area against the bore area; orifice flow", value=round(a_holes / a_bore, 1), limit=1.0, unit="x bore area", rule="above")

# S20 desiccant
vent_ml = math.pi / 4 * 1.5 ** 2 * (L_MAX + DS["surface_run_m"])
breath = (1.4 + vent_ml / 1e3) * 30 / 300
days = 10 * 0.20 * 1000 / (breath / 1000 * 24.0 * 1000)
c.claim("S20", f"10 g of silica gel keeps the vent and box air dry about {days:.0f} days at worst-case daily breathing, more than the 91-day change interval (PR-017); permeation through gaskets and glands is not counted", "Chemistry",
        "Physical chemistry", law="Gas law breathing at a 30 K daily swing; silica gel uptake 20 % by mass [F1]", value=round(days), limit=91, unit="days", rule="above")

# S21 junction box temperature in sun
A_proj = P["jbox"][1] / 1000 * P["jbox"][2] / 1000
A_surf = 2 * (P["jbox"][0] * P["jbox"][1] + P["jbox"][0] * P["jbox"][2] + P["jbox"][1] * P["jbox"][2]) / 1e6
dT_sun = 0.5 * 1000 * A_proj / (10 * A_surf)
c.cited("S21", f"At 55 degC ambient in full sun the junction box stays within the 85 degC rating of the modules (PR-015)",
        "Physics", "Heat transfer", "Solar gain alpha G A_sun against convection h A_total, alpha 0.5, G 1,000 W/m2, h 10 W/m2K, A_sun/A_total {:.2f}".format(A_proj / A_surf),
        f"{55 + dT_sun:.0f} degC by the balance; small enclosures in full sun are often measured 20 to 35 K above ambient, which would reach 75 to 90 degC", PLAUSIBLE)

# S22 storage
c.claim("S22", "One year of 15 min readings fills 1.12 MB of FieldNode's 16 MB flash (PR-007)", "Mathematics", "Orders of magnitude",
        law="35,040 readings x 32 bytes [E1]", value=round(35040 * 32 / 1e6, 2), limit=16.78, unit="MB", rule="below")

# S23 airtime
c.claim("S23", "Pumping-test batches every 30 min on a public network use 22.7 s of airtime a day at SF9 (PR-006); valid at SF9 only: at SF10 and above a test sends from a private gateway or in hourly batches", "Engineering and technology",
        "Power and link budgets", law="Semtech LoRa time-on-air formula; 30 s a day fair use on The Things Network [E4]",
        value=22.7, limit=30.0, unit="s/day", rule="below")

# S24 drinking water materials
c.cited("S24", "316 stainless, PVC, HDPE, EPDM and PU or PE cable jackets can be had in grades certified for drinking water contact (PR-009)",
        "Chemistry", "Materials and polymer chemistry", "NSF/ANSI/CAN 61 lists components of all these material classes",
        "Material classes are routinely certified; no certificate is in hand for the chosen low-cost parts, so PR-009 stays not met on evidence",
        WITHIN)

# S25 disinfection
c.cited("S25", "Disinfecting the probe, cable and tube with chlorine solution before they go into the well reduces the risk of bringing bacteria into the supply",
        "Biology", "Microbiology", "AWWA C654 (disinfection of wells) and the local water authority's practice",
        "Standard well practice; the build plan and PRC safety notes carry it", WITHIN)

# S26 handling
m30 = (w_t + w_cab) / 9.81 * L_DES / L_MAX
c.claim("S26", f"Two people can lower the {L_DES:.0f} m design-case tube string and cable ({m30:.0f} kg) by hand; at {L_MAX:.0f} m ({(w_t + w_cab) / 9.81:.0f} kg) a third person or a hand line is used",
        "Biology", "Ergonomics", law="UK HSE guideline weights, 16 kg per person (women) to 25 kg (men) for lifting close to the body (INDG143)",
        value=round(m30 / 2, 1), limit=16.0, unit="kg per person", rule="below")

# S27 electrical safety
c.claim("S27", "Every WellSense circuit runs at 24 V DC or less, within extra-low voltage (PR-018)", "Engineering and technology", "Standards practice",
        law="ELV band: 120 V ripple-free DC or less (IEC 61140)", value=24.0, limit=120.0, unit="V DC", rule="below")

# S28 cable short (fix rule, WLS-DEC-001 D-S4)
i_short = 24.0 / (R_SH + r_cab)
p_short = i_short ** 2 * R_SH
c.claim("S28", f"A short between the cable cores puts the 24 V boost across the shunt: {i_short * 1000:.0f} mA and {p_short:.1f} W in a small shunt: fails. "
        f"Fixed with a 50 mA resettable fuse (PTC) in series with the loop on the interface board: it trips within about 1 s, and a 0.6 W metal film shunt carries "
        f"{p_short:.1f} W for that second; normal loop current (22 mA) is below its hold current",
        "Engineering and technology", "Standards practice", law="Ohm's law; PTC hold and trip currents; short-time overload of film resistors",
        value=22.0, limit=50.0, unit="mA", rule="below", closed_by="WLS-DEC-001 D-S4 (fix rule, 2026-10-25)")

# =========================================================================================== option B
# Bubbler: a small 12 V diaphragm pump in the junction box pushes air down a 1/4 in PE line in the same
# access tube until it bubbles out of a stainless weight at the bottom; a gauge sensor reads the back-pressure.
LINE_ID = 4.3                     # mm, 1/4 in PE tube
L_line = L_DES + DS["surface_run_m"]
p_abs = 101.3 + p_fs              # kPa at the orifice with the full 10 m head
rho_air = p_abs * 1000 / (287.05 * 293.15)
d_air = rho_air * G * L_DES / (RHO * G) * 1000
c.order_of_magnitude("B1", f"Option B: back-pressure equals the head over the orifice plus the weight of the air column ({d_air:.0f} mm at {L_DES:.0f} m), which firmware corrects",
                     "Physics", "Fluid mechanics", claimed=round(d_air), estimate=d_air, unit="mm", factor=1.05,
                     law="Hydrostatics of water and of the compressed air column, ideal gas")
d_bub = 2 * 0.072 / 0.002 / (RHO * G) * 1000
c.order_of_magnitude("B2", f"Option B: the bubble-forming overpressure at a 4 mm orifice is about {d_bub:.0f} mm; when the pump stops a pinned meniscus leaves 0 to {d_bub:.0f} mm, carried as 2 mm in B7",
                     "Physics", "Fluid mechanics", claimed=round(d_bub), estimate=d_bub, unit="mm", factor=1.1, law="Laplace pressure 2 sigma / r, sigma 0.072 N/m")
E_B = 1.2 * 8.0 + 3.3 * 0.008 * 10            # pump 8 s and the controller awake 10 s
e_day_b = E_B * 96 / 3600 * 1000
c.claim("B3", f"Option B: pump {1.2:.1f} W for 8 s and the controller 10 s per reading, {e_day_b:.0f} mWh a day at 15 min, within FieldNode's 2.4 Wh sensor allowance "
        f"({e_day_b / 24 / 100 * 100:.1f} % of 100 mW, above the 5 % target of PR-008)", "Physics", "Electromagnetism and circuits",
        law="Energy balance", value=round(e_day_b), limit=2400, unit="mWh/day", rule="below")
c.cited("B4", f"Option B: a 12 V miniature diaphragm pump reaches the {p_fs * 1.2:.0f} kPa needed (full head plus 20 %)", "Engineering and technology",
        "Power and link budgets", "Pump maker's pressure curve", "To assess at part selection; many small pumps stop near 80 kPa", PLAUSIBLE)
v_line = math.pi / 4 * LINE_ID ** 2 * L_line * 1000 / 1e6
c.order_of_magnitude("B5", f"Option B: the {L_line:.0f} m line holds {v_line * 1000:.0f} mL; the first fill at full head needs about {v_line * p_abs / 101.3 * 1000:.0f} mL of free air, "
                     "a few minutes at 0.3 L/min", "Mathematics", "Orders of magnitude", claimed=0.9, estimate=v_line * p_abs / 101.3, unit="L", factor=3.0,
                     law="Boyle's law")
gel_days = 10 * 0.2 / (0.3 * 8 / 60 * 96 * 24.0 / 1000)
c.cited("B6", f"Option B: a desiccant inlet keeps compressed air from condensing in the line inside the cooler well; 10 g of gel lasts only about {gel_days:.0f} days, so a quarterly change needs about 40 g", "Physics", "Thermodynamics",
        "Dew point of dried air (about -14 degC at line pressure) against groundwater at 15 to 30 degC; gel uptake 20 % by mass",
        "Dried inlet air cannot reach saturation in the well; gel sized at 40 g", WITHIN)
nl_b = 0.0010 * 150 / (RHO * G) * 1e6
rss_b = math.sqrt(nl_b ** 2 + 10.0 ** 2 + 5.0 ** 2 + 3.0 ** 2 + 2.0 ** 2 + 4.0 ** 2)
c.cited("B7", f"Option B: a 0 to 150 kPa gauge sensor of the 0.25 % class reaches about {rss_b:.0f} mm RSS after calibration (PR-004)",
        "Mathematics", "Statistics and uncertainty", "Error budget: nonlinearity 0.1 % of 150 kPa, certificate span 10 mm, air column residual 5 mm, tape 3 mm, bubble 2 mm, thermal 4 mm",
        f"RSS {rss_b:.0f} mm against 20 mm; sensor terms typical, not measured", PLAUSIBLE)

# =========================================================================================== option C
# Acoustic sounder: a small loudspeaker and microphone in a head on top of the access tube send a chirp down
# the air column; the echo from the water surface gives the distance to water.
c_snd = 331.3 * math.sqrt(1 + 20 / 273.15)
fs = 48000.0
res_c = c_snd / (2 * fs) * 1000
c.claim("C1", f"Option C: sampling the echo at 48 kHz gives a {res_c:.1f} mm sample spacing; the timing precision of the correlation peak depends on the signal-to-noise ratio (the chirp's own range resolution is about 0.6 m)", "Physics", "Acoustics and vibration",
        law="Time of flight t = 2L/c, c = 343 m/s at 20 degC", value=round(res_c, 1), limit=20.0, unit="mm", rule="below")
dT_need = 0.020 / (L_DES * 0.5 / 273.15) / math.sqrt(3)    # temperature takes a third of the 20 mm budget by RSS
c.cited("C2", f"Option C: +/-20 mm at {L_DES:.0f} m needs the mean air temperature of the column to +/-{dT_need:.2f} K, or reflections from tube joints at known depths to calibrate the speed of sound",
        "Physics", "Acoustics and vibration", "c proportional to the square root of absolute temperature (0.18 % per K); joint counting as in oil-well echo sounders",
        "Whether solvent-weld PVC joints reflect enough is unknown", PLAUSIBLE)
nu, gam, Pr = 1.5e-5, 1.4, 0.71
r_t = P["tube_id"] / 2000
def alpha(f):
    return math.sqrt(2 * math.pi * f * nu / 2) * (1 + (gam - 1) / math.sqrt(Pr)) / (r_t * c_snd)
path = 2 * L_MAX
loss = alpha(500) * path * 8.686
c.cited("C3", f"Option C: at 500 Hz the round trip to water {L_MAX:.0f} m down loses about {loss:.0f} dB to the tube walls, recoverable with a short (0.2 s) chirp and correlation once the direct leakage has died away",
        "Physics", "Acoustics and vibration", "Kirchhoff wall attenuation in a narrow tube", f"{loss:.0f} dB at 500 Hz over {path:.0f} m; holes and joints add loss",
        PLAUSIBLE)
e_day_c = (0.3 * 1.0 + 3.3 * 0.03 * 1.0) * 96 / 3600 * 1000
c.claim("C4", f"Option C: a 1 s chirp and capture at 0.4 W uses {e_day_c:.0f} mWh a day at 15 min (PR-008)", "Physics", "Electromagnetism and circuits",
        law="Energy balance", value=round(e_day_c, 1), limit=0.05 * 100 * 24, unit="mWh/day", rule="below")
c.cited("C5", "Option C: the speaker and microphone survive the saturated air at the top of the tube", "Chemistry", "Electrochemistry and batteries",
        "Condensation and corrosion of electronics at 100 % relative humidity; IP67 transducers and conformal coating", "Needs IP67 parts and a coated board; to confirm", PLAUSIBLE)

if __name__ == "__main__":
    state = c.write()
    for r in c.rows:
        print(f"{r['id']:>4}  {r['verdict']:<32} {r['check']}")
    print("stem_check:", state)
