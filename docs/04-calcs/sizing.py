"""WellSense sizing calculations, WLS-CAL-001 v0.2 (TRL 3, WLS-DDR-002 applied).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md. Each line carries a tag such as
[B2] that the note cites, and the results are also written to docs/04-calcs/results.csv.
Geometry comes from cad/src/model.py (PARAMS, DESIGN and derived), the parts cost from
bom/bom.csv and the budget from project.yaml. First-principles estimates for a paper proof
of concept; not a substitute for tests.
"""
import csv
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import DESIGN as DS, PARAMS as P, derived  # noqa: E402

D = derived(P)
ROWS = []


def tag(t, text):
    print(f"[{t}] {text}")
    ROWS.append((t, text))


# ------------------------------------------------------------------ assumptions
G0 = 9.80665               # m/s2, standard gravity (sensor calibration in kPa)
RANGE_M = DS["range_m"]    # m of water, full scale (DDR-001 D3)
R_SHUNT = 150.0            # ohm
ADC_FSR = 4.096            # V, ADS1115 programmable gain setting (+/-)
ADC_BITS = 16
I_MAX = 0.022              # A, loop ceiling (over-range and fault)
T_ON = 2.0                 # s rail on per reading (warm-up, 16 samples, margin)
V_RAIL = 12.0              # V, FieldNode switched rail
RAIL_TOL = 0.05            # rail low by 5 %
ETA_RAIL = 0.90            # FieldNode rail converter (FND-CAL-001)
V_BOOST = 24.0             # V, interface board boost output
ETA_BOOST = 0.85
V_MIN_TX = 12.0            # V, transducer minimum supply (BOM line 1: 12 to 30 V)
R_CU = 0.087               # ohm/m for a 0.2 mm2 copper core at 20 degC
V_DIODE = 0.3              # V, Schottky reverse-polarity diode
CTRL = (3.3, 0.008)        # V, A controller awake during the warm-up (FND-CAL-001 figure)
ALLOW_W = (0.100, 0.115)   # W, FieldNode sensor allowance: design value and ceiling (FND-CAL-001 [A3], [A5])
READ_DAY = 96              # 15 min default (D5)
READ_TEST = 1440           # 1 min during a pumping test
BYTES_STORED = 32          # FieldNode record size (FND-CAL-001)
FLASH = 16 * 1024 * 1024   # bytes, FieldNode SPI flash
# accuracy budget (0.25 % class, after two-point field calibration)
NL = {"0.25 % class": 0.0010, "0.5 % class": 0.0020}  # nonlinearity, hysteresis, repeatability, fraction of FS
TC_PROBE = 0.0002          # fraction of FS per K, compensated thermal effect
DT_GW = 2.0                # K, groundwater temperature change after calibration
TC_SHUNT = 10e-6           # per K
TC_ADC = 7e-6              # per K, ADS1115 typical gain drift
DT_BOX = 30.0              # K, junction box temperature away from calibration
TAPE = 0.003               # m, electric tape reading uncertainty (0.01 ft)
# mechanical
CABLE_KG_M = 0.055         # kg/m vented cable
PROBE_KG = 0.25
STRAIN_N = 400.0           # N, strain member rating (BOM line 2)
PVC = (1400.0, 48e6)       # kg/m3, tensile strength Pa
# desiccant
BOX_AIR_L = 1.4            # L of air in the junction box
VENT_ID = 1.5              # mm capillary bore
ABS_HUM = 24.0             # g/m3, 30 degC at 80 % RH
DT_DAY = 30.0              # K daily swing inside the box in sun
GEL = (10.0, 0.20)         # g silica gel, usable uptake fraction
# fit in the casing
CLEAR = 3.0                # mm minimum running clearance
RISER_C = {100: 40.0, 125: 52.0, 150: 52.0, 200: 73.0}   # riser coupling OD per casing bore (1, 1-1/4, 1-1/4, 2 in)
TUBES = {"1 in (DN25)": (33.4, 26.6, 40.0), "1-1/4 in (DN32)": (42.2, 35.1, 50.0)}  # OD, bore, coupling OD
PROBES = (22.0, 24.0, 26.0, 28.0)


def rho_water(t):
    """Water density, kg/m3 (Thiesen formula)."""
    return 1000.0 * (1 - (t + 288.9414) / (508929.2 * (t + 68.12963)) * (t - 3.9863) ** 2)


def g_lat(lat):
    s2 = math.sin(math.radians(lat)) ** 2
    return 9.7803253359 * (1 + 0.00193185265241 * s2) / math.sqrt(1 - 0.00669437999013 * s2)


def airtime(pl, sf=9, bw=125e3, cr=1, npre=8, header=True, crc=True):
    de = 1 if sf >= 11 else 0
    ts = 2 ** sf / bw
    h = 0 if header else 1
    n = 8 + max(math.ceil((8 * pl - 4 * sf + 28 + 16 * crc - 20 * h) / (4 * (sf - 2 * de))) * (cr + 4), 0)
    return (npre + 4.25) * ts + n * ts


print("WellSense sizing, WLS-CAL-001 v0.2")
print(f"Model: casing {P['casing_id']:.0f} mm bore, tube {P['tube_od']} x {P['tube_id']} mm, probe {P['probe'][0]:.0f} x {P['probe'][1]:.0f} mm; "
      f"design probe depth {DS['probe_depth_m']:.0f} m (to {DS['probe_depth_max_m']:.0f} m)")

# ------------------------------------------------------------------ A. Range and resolution (R1, R3)
print("\nA. Range and resolution")
p_fs = 1000 * G0 * RANGE_M / 1000
tag("A1", f"Full scale {RANGE_M:.0f} m of water = {p_fs:.2f} kPa; 1 kPa = {1000 / (1000 * G0) * 1000:.1f} mm of water")
v_lo, v_hi = 0.004 * R_SHUNT, 0.020 * R_SHUNT
lsb = 2 * ADC_FSR / 2 ** ADC_BITS
steps = (v_hi - v_lo) / lsb
res = RANGE_M * 1000 / steps
tag("A2", f"Shunt {R_SHUNT:.0f} ohm gives {v_lo:.2f} to {v_hi:.2f} V; ADC step {lsb * 1e6:.0f} uV; {steps:,.0f} steps; resolution {res:.2f} mm (0 to 10 m), {2 * res:.2f} mm (0 to 20 m variant)")
tag("A3", f"Placement rule: probe at least 1 m below the lowest pumping level; seasonal swing plus pumping drawdown up to "
    f"{RANGE_M - 1:.0f} m then stays in range with 1 m of headroom; larger swings need the 0 to 20 m variant")

# ------------------------------------------------------------------ B. Loop supply and energy (R8)
print("\nB. Loop supply and energy")
L_loop = DS["probe_depth_max_m"] + DS["surface_run_m"]
r_cable = 2 * L_loop * R_CU
v_low = V_RAIL * (1 - RAIL_TOL)
v_tx_direct = v_low - I_MAX * R_SHUNT - I_MAX * r_cable - V_DIODE
v_tx_boost = V_BOOST - I_MAX * R_SHUNT - I_MAX * r_cable - V_DIODE
tag("B1", f"Loop at {I_MAX * 1000:.0f} mA, {L_loop:.0f} m cable ({r_cable:.1f} ohm): from the 12 V rail (low {v_low:.1f} V) the transducer gets {v_tx_direct:.2f} V "
    f"against {V_MIN_TX:.0f} V minimum (short by {V_MIN_TX - v_tx_direct:.2f} V); with a {V_BOOST:.0f} V boost it gets {v_tx_boost:.2f} V (margin {v_tx_boost - V_MIN_TX:.2f} V)")
v_adc_max = 0.025 * R_SHUNT
tag("B1b", f"Shunt voltage at a 25 mA fault is {v_adc_max:.2f} V, above the ADC's 3.6 V limit at 3.3 V supply; a series input resistor is needed")
e_loop = V_BOOST * I_MAX * T_ON / ETA_BOOST / ETA_RAIL
e_ctrl = CTRL[0] * CTRL[1] * T_ON
e_read = e_loop + e_ctrl
e_day = e_read * READ_DAY / 3600
e_test = e_read * READ_TEST / 3600
tag("B2", f"Per reading: loop {e_loop:.2f} J (24 V x 22 mA x 2 s, boost 85 %, rail 90 %) + controller {e_ctrl:.3f} J = {e_read:.2f} J")
tag("B3", f"At 15 min: {e_day * 1000:.1f} mWh/day, {e_day / 24 * 1000:.2f} mW average; {e_day / (ALLOW_W[0] * 24) * 100:.1f} % of FieldNode's published 100 mW allowance")
tag("B4", f"At 1 min (pumping test): {e_test:.3f} Wh/day, {e_test / 24 * 1000:.1f} mW average; {e_test / (ALLOW_W[0] * 24) * 100:.0f} % of the 100 mW allowance")
e_trl2 = 12 * I_MAX * T_ON / 0.80
tag("B5", f"TRL 2 figure for comparison: {e_trl2:.2f} J per reading, {e_trl2 * READ_DAY / 3600 * 1000:.0f} mWh/day (12 V direct, 80 %)")

# ------------------------------------------------------------------ C. Accuracy (R4, R5)
print("\nC. Accuracy after two-point field calibration")
lat_g = (g_lat(0), g_lat(45), g_lat(60))
tag("C1", f"Gravity {lat_g[0]:.4f} m/s2 at the equator, {lat_g[1]:.4f} at 45 deg, {lat_g[2]:.4f} at 60 deg: "
    f"using standard g misreads 10 m by {(G0 / lat_g[0] - 1) * RANGE_M * 1000:+.0f} mm at the equator; firmware uses local g, and calibration absorbs the rest")
r4, r15, r25 = rho_water(4), rho_water(15), rho_water(25)
tag("C2", f"Density {r4:.2f} kg/m3 at 4 degC, {r15:.2f} at 15 degC, {r25:.2f} at 25 degC: {(r4 / r25 - 1) * 100:.2f} % or {(r4 / r25 - 1) * RANGE_M * 1000:.0f} mm at 10 m across 4 to 25 degC")
d_rho = abs(rho_water(15 + DT_GW) - r15) / r15 * RANGE_M
k_i = 20 / 16  # head error per unit gain error at 20 mA, relative to the 10 m span
budget = {}
for cls, nl in NL.items():
    terms = {
        "nonlinearity, hysteresis, repeatability": nl * RANGE_M,
        f"probe thermal effect, {DT_GW:.0f} K": TC_PROBE * DT_GW * RANGE_M,
        f"density at a fixed site value, {DT_GW:.0f} K": d_rho,
        f"shunt drift, {DT_BOX:.0f} K": TC_SHUNT * DT_BOX * k_i * RANGE_M,
        f"ADC gain drift, {DT_BOX:.0f} K": TC_ADC * DT_BOX * k_i * RANGE_M,
        "ADC resolution": res / 1000,
        "manual tape reference": TAPE,
    }
    rss = math.sqrt(sum(v ** 2 for v in terms.values()))
    budget[cls] = (terms, rss, sum(terms.values()))
terms, rss, tot = budget["0.25 % class"]
for i, (k, v) in enumerate(terms.items(), 1):
    tag(f"C3.{i}", f"{k}: {v * 1000:.1f} mm")
tag("C4", f"0.25 % class after two-point calibration: RSS {rss * 1000:.1f} mm, worst-case sum {tot * 1000:.1f} mm (target 20 mm)")
_, rss5, tot5 = budget["0.5 % class"]
tag("C5", f"0.5 % class after two-point calibration: RSS {rss5 * 1000:.1f} mm, worst-case sum {tot5 * 1000:.1f} mm")
tag("C6", f"Datasheet only, no field calibration: {0.0050 * RANGE_M * 1000:.0f} mm (0.5 % class), {0.0025 * RANGE_M * 1000:.0f} mm (0.25 % class)")
tag("C7", f"Absolute sensor without compensation, +/-3 kPa weather: +/-{3000 / (1000 * G0) * 1000:.0f} mm")
tag("C8", f"Drift: with a tape check every quarter, a transducer drifting 20 mm a year leaves at most {20 / 4:.0f} mm uncorrected between checks, "
    f"close to the {TAPE * 1000:.0f} mm tape uncertainty; real drift of low-cost probes is unknown")

# ------------------------------------------------------------------ D. Fit in the well (R10, R2)
print("\nD. Fit in the well and hanging loads")
tag("D1", f"Model: probe {P['probe'][0]:.0f} mm in a {P['tube_id']} mm bore: {D['probe_clear_radial']:.1f} mm radial clearance; "
    f"tube {D['tube_to_riser']:.1f} mm from the riser and {D['tube_to_casing']:.1f} mm from the casing wall in the 150 mm design well")
fit = []
for name, (od, bore, cpl) in TUBES.items():
    probes_ok = [pd for pd in PROBES if (bore - pd) / 2 >= 2.0]
    for cid, rc in RISER_C.items():
        centered = (cid - rc) / 2 >= cpl + CLEAR
        wall = cid - rc >= cpl + CLEAR
        fit.append((name, cid, rc, centered, wall))
    tag(f"D2 {name}", f"bore {bore} mm takes probes up to {max(probes_ok) if probes_ok else 0:.0f} mm with 2 mm radial clearance; fits beside a centered riser in casings of "
        + ", ".join(f"{c}" for (n, c, _, ce, _) in fit if n == name and ce) + " mm; beside a riser against the wall in "
        + ", ".join(f"{c}" for (n, c, _, _, w) in fit if n == name and w) + " mm")
w_cable = (CABLE_KG_M * DS["probe_depth_max_m"] + PROBE_KG) * 9.81
tag("D3", f"Cable and probe hanging in air at {DS['probe_depth_max_m']:.0f} m: {w_cable:.0f} N against a {STRAIN_N:.0f} N strain member (factor {STRAIN_N / w_cable:.1f})")
a_tube = math.pi / 4 * (P["tube_od"] ** 2 - P["tube_id"] ** 2) / 1e6
w_tube = a_tube * PVC[0] * 9.81 * DS["probe_depth_max_m"]
tag("D4", f"Access tube {a_tube * 1e6:.0f} mm2, {a_tube * PVC[0]:.2f} kg/m; {DS['probe_depth_max_m']:.0f} m hanging dry: {w_tube:.0f} N, stress {w_tube / a_tube / 1e6:.2f} MPa "
    f"against {PVC[1] / 1e6:.0f} MPa (factor {PVC[1] / (w_tube / a_tube):.0f}); the seal plate gland needs a tube clamp for {w_tube:.0f} N")

# ------------------------------------------------------------------ E. Storage and airtime (R6, R7)
print("\nE. Storage and airtime")
yr = READ_DAY * 365
tag("E1", f"One year at 15 min: {yr:,} readings x {BYTES_STORED} B = {yr * BYTES_STORED / 1e6:.2f} MB, {yr * BYTES_STORED / FLASH * 100:.1f} % of the 16 MB flash")
tag("E2", f"A 7-day pumping test at 1 min adds {7 * READ_TEST:,} readings, {7 * READ_TEST * BYTES_STORED / 1e6:.2f} MB")
a20, a38 = airtime(20 + 13), airtime(38 + 13)
tag("E3", f"Airtime at SF9: 20-byte uplink {a20 * 1000:.1f} ms, {a20 * 96:.1f} s/day at 15 min (FieldNode figure); pumping test batch of 15 readings "
    f"(38 bytes) {a38 * 1000:.1f} ms, {a38 * 96:.1f} s/day, over the 30 s/day fair use on a public network; fits a private TwinKit gateway")
a68 = airtime(68 + 13)
tag("E4", f"Rule (WLS-DDR-002): on a public network a pumping test sends every 30 min, a batch of 30 readings (68 bytes) "
    f"{a68 * 1000:.1f} ms, {a68 * 48:.1f} s/day, within 30 s/day; on a private TwinKit gateway the 15 min batch is kept")

# ------------------------------------------------------------------ F. Desiccant (R15, maintenance)
print("\nF. Vent desiccant")
vent_ml = math.pi / 4 * VENT_ID ** 2 * (DS["probe_depth_max_m"] + DS["surface_run_m"]) * 1000 / 1000
breath_l = (BOX_AIR_L + vent_ml / 1000) * DT_DAY / 300
water_mg = breath_l / 1000 * ABS_HUM * 1000
days = GEL[0] * GEL[1] * 1000 / water_mg
tag("F1", f"Vent capillary {vent_ml:.0f} mL at 62 m; box and vent breathe {breath_l:.2f} L/day at a {DT_DAY:.0f} K swing, carrying {water_mg:.1f} mg of water at worst; "
    f"{GEL[0]:.0f} g of gel lasts about {days:.0f} days if the whole box breathes through it (quarterly change: factor {days / 91:.1f})")

# ------------------------------------------------------------------ G. Installation (R11)
print("\nG. Installation time with an access tube already in place")
steps_min = [("Isolate and lock off the pump, open the wellhead", 10), ("Disinfect probe and cable", 15),
             ("Fit the split seal plate round the riser", 20), ("Lower the probe, set the hanger", 10),
             ("Tape datum at the measuring point", 10), ("Fit junction box and FieldNode on a set post", 20),
             ("Wire, seal glands, fit desiccant", 15), ("Two-point calibration (probe lifted 1 m)", 15),
             ("Confirm an uplink", 5)]
t_inst = sum(m for _, m in steps_min)
tag("G1", f"Estimated {t_inst} min for two people ({len(steps_min)} steps) against 120 min; post footing set and cured on an earlier visit")

# ------------------------------------------------------------------ H. Cost (R12)
print("\nH. Cost")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
budget_usd = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
def line(r):
    return float(r["qty"]) * float(r["unit_cost_usd"])
num = lambda r: int(r["item"].split()[0])
own = [r for r in rows if num(r) not in (8, 11, 12)]
c_own = sum(line(r) for r in own)
c_node = sum(line(r) for r in rows if num(r) == 8)
unpriced = [r["item"] for r in rows if not r["unit_cost_usd"].strip()]
per_m = sum(float(r["unit_cost_usd"]) for r in rows if num(r) in (2, 3))
tube_len = DS["probe_depth_m"] + DS["tube_extra_m"] + (P["tube_top"] - P["stickup"]) / 1000
cable_len = DS["probe_depth_m"] + DS["surface_run_m"]
fixed = c_own - per_m * DS["probe_depth_m"]
breakeven = (budget_usd - fixed) / per_m
no_tube = c_own - sum(line(r) for r in rows if num(r) == 3)
tag("H1", f"BOM {len(rows)} lines, {len(rows) - len(unpriced)} priced; cable {cable_len:.0f} m and tube {tube_len:.2f} m (BOM {math.ceil(tube_len)} m) at {DS['probe_depth_m']:.0f} m probe depth")
tag("H2", f"WellSense parts (lines 1 to 7, 9, 10, 13, 14): ${c_own:.2f} against budget_usd ${budget_usd:.0f} ({'over' if c_own > budget_usd else 'within'} by ${abs(c_own - budget_usd):.2f}; set to $200 by Amish on 2026-09-26, WLS-DDR-002); "
    f"with the FieldNode core ${c_own + c_node:.2f}; with FieldNode's hot-site shield (+$8.00, FND-DDR-002) ${c_own + c_node + 8:.2f}")
c_conduit = sum(line(r) for r in rows if num(r) == 14)
tag("H2b", f"Without the conduit (line 14, ${c_conduit:.2f}) the parts would be ${c_own - c_conduit:.2f}, within the ${budget_usd:.0f} budget")
tag("H3", f"Depth-dependent ${per_m:.2f}/m; budget met to a probe depth of {breakeven:.1f} m; at 60 m ${c_own + per_m * 30:.2f}; "
    f"without an access tube (no pump in the casing) ${no_tube:.2f}")

# ------------------------------------------------------------------ results table
results = [
    ("R9", "Not met", "No drinking water certificate in hand for low-cost cable, seal or probe"),
    ("R4", "At risk", f"RSS {rss * 1000:.1f} mm, sum {tot * 1000:.1f} mm (0.25 % class, calibrated)"),
    ("R10", "At risk", f"{D['probe_clear_radial']:.1f} mm radial clearance with a 22 mm probe; tube may need the pump pulled"),
    ("R15", "At risk", "FieldNode shield at hot sites (48.5 to 52.2 degC inside at 45 degC); FieldNode rated to 45 degC ambient against 55 degC"),
    ("R16", "At risk", "Cable in conduit from the tube cap to the box; locking of the wellhead parts not specified"),
    ("R5", "Not verifiable at TRL 3", "Drift unknown; quarterly check leaves 5 mm"),
    ("R11", "Not verifiable at TRL 3", f"{t_inst} min estimate"),
    ("R13", "Not verifiable at TRL 3", "Dashboard not started"),
    ("R1", "Met", f"0 to 10 m, {p_fs:.2f} kPa"),
    ("R2", "Met", f"Cable factor {STRAIN_N / w_cable:.1f}, tube factor {PVC[1] / (w_tube / a_tube):.0f} at 60 m"),
    ("R3", "Met", f"{res:.2f} mm"),
    ("R6", "Met", f"15 min; 1 min logged, sent every 30 min on a public network ({a68 * 48:.1f} s/day)"),
    ("R7", "Met", f"{yr * BYTES_STORED / 1e6:.2f} MB a year"),
    ("R8", "Met", f"{e_day * 1000:.1f} mWh/day, {e_day / (ALLOW_W[0] * 24) * 100:.1f} % of 100 mW"),
    ("R12", "Met" if c_own <= budget_usd else "Not met", f"${c_own:.2f} at 30 m against ${budget_usd:.0f}; met to {breakeven:.1f} m"),
    ("R14", "Met", "Levels, time and well ID only"),
]
print("\nL. Requirement status")
for rid, st, val in results:
    tag(f"L {rid}", f"{st}: {val}")
counts = {}
for _, st, _ in results:
    counts[st] = counts.get(st, 0) + 1
tag("L", ", ".join(f"{v} {k[0].lower() + k[1:]}" for k, v in counts.items()))

with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["tag", "result"])
    w.writerows(ROWS)
