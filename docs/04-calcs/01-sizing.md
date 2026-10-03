---
doc_id: WLS-CAL-001
title: WellSense sizing calculations
project: WellSense
doc_type: Calculation
version: "0.5"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (range and resolution, loop supply and energy, accuracy and drift, fit in the well and hanging loads, storage and airtime, vent desiccant, installation, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish; budget $200 covers the priced BOM, so R12 is met and holds to 31.3 m (WLS-DDR-002 v0.2)
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: Constructable design (WLS-DDR-004); surface cable run, wellhead load paths and cost recomputed; budget treated as a value-engineering target
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: Locks added under WLS-DEC-001 decision 2; cost, R16 status and installation time recomputed; new check [D7]
---

# WellSense sizing calculations

On paper, WellSense meets eight of its sixteen requirements, has three at risk, misses one, leaves three that only field work can settle and is over its value-engineering target on cost. The miss is water safety. With the decisions of WLS-DDR-002 applied (a 22 mm probe in the 1 in tube, a galvanized conduit over the surface cable and a 30 min uplink rule for pumping tests on public networks) and the design made constructable under WLS-DDR-004, the WellSense parts cost $262.40 at the 30 m design depth, locks included. Value-engineering target: USD 200 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 262.40 (USD 62.40 over the target). No drinking water certificate is in hand for the low-cost cable, seal or probe (R9). The calculations changed the interface: the FieldNode 12 V rail cannot drive a 4 to 20 mA loop through a 150 Ω shunt and 62 m of cable to the transducer's 12 V minimum (it delivers 7.56 V), so the interface board gains a 24 V boost. That doubles the sensor energy of the TRL 2 estimate to 38.2 mWh a day, still only 1.6 % of the FieldNode allowance. Accuracy (R4) is at risk rather than not met: a 0.25 % class probe after a two-point field calibration against a manual tape gives 12.5 mm by root sum square against the ±20 mm target, but 27.1 mm if every term adds. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that anything lowered into a well is safe for drinking water, that the wellhead is sealed, or that work at a well with a mains-powered pump is safe. See WLS-PRC-001, Safety.

## Scope and method

The note checks every requirement in WLS-REQ-001 v0.4 against the design in WLS-PRC-001 v0.4 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `DESIGN` and `derived()`, so the tube, probe, casing, post and seal plate used here are the ones in the STEP files and in drawing WLS-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes `docs/04-calcs/results.csv`.

The design case is a 150 mm (6 in) borehole with a 4 in submersible pump on a 1-1/4 in riser, the probe hung 30 m below the top of the casing (up to 60 m for R2) in a 1 in PVC access tube, and a FieldNode core on a post 0.75 m from the well, reading every 15 min (DDR-001, D5).

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Pressure | Water 1,000 kg/m³ nominal; standard gravity 9.80665 m/s² in the sensor's kPa calibration; local gravity from the WGS 84 formula | Physical constants |
| Loop | 150 Ω shunt; ADS1115 class 16-bit ADC at ±4.096 V; loop ceiling 22 mA; rail on 2 s per reading; FieldNode 12 V rail 5 % low, 90 % efficient; boost to 24 V at 85 %; transducer minimum supply 12 V; two 0.2 mm² copper cores at 0.087 Ω/m; 0.3 V reverse-polarity diode | BOM lines 1, 2 and 7; FND-CAL-001 for the rail |
| Node | Controller awake 2 s at 8 mA, 3.3 V, per reading; published sensor allowance 100 mW; 32-byte stored record; 16 MB flash; 20-byte uplink | FND-CAL-001 v0.2 |
| Accuracy | After a two-point calibration: nonlinearity, hysteresis and repeatability 0.10 % of full scale (0.25 % class) or 0.20 % (0.5 % class); probe thermal effect 0.02 % of full scale per K over 2 K of groundwater change; shunt 10 ppm/K and ADC gain 7 ppm/K over 30 K in the junction box; tape reading ±3 mm (0.01 ft) | Typical datasheet ranges and USGS tape practice; not measured |
| Mechanical | Vented cable 0.055 kg/m, probe 0.25 kg, strain member 400 N; PVC 1,400 kg/m³ and 48 MPa tensile | Typical catalogue values |
| Fit | 3 mm running clearance; 2 mm radial clearance for a probe in its tube; riser coupling OD 40 mm (1 in riser in 100 mm casing), 52 mm (1-1/4 in, in 125 and 150 mm casing), 73 mm (2 in, in 200 mm casing); tube coupling OD 40 mm (1 in) and 50 mm (1-1/4 in) | Common pipe sizes |
| Desiccant | 1.4 L of air in the junction box, 1.5 mm vent capillary, 30 K daily swing, 24 g/m³ humid air, 10 g of silica gel with 20 % usable uptake | Screening values |

## A. Range and resolution (R1, R3)

- **Range.** Full scale is 10 m of water, 98.07 kPa; 1 kPa is 102.0 mm of water [A1]. R1 is met by the 0 to 10 m transducer (DDR-001, D3).
- **Resolution.** The 150 Ω shunt turns 4 to 20 mA into 0.60 to 3.00 V. At 125 µV per ADC step that is 19,200 steps, or 0.52 mm per step over 10 m, and 1.04 mm on the 0 to 20 m variant [A2]. R3 is met; the 20 m variant just misses 1 mm.
- **Placement.** With the probe at least 1 m below the lowest pumping level, seasonal swing plus pumping drawdown of up to 9 m stays in range with 1 m of headroom; larger swings need the 0 to 20 m variant [A3].

## B. Loop supply and energy (R8)

- **The 12 V rail cannot drive the loop.** At 22 mA through 63 m of cable (10.9 Ω; 60 m down the well plus the 2.7 m surface run of WLS-DDR-004) and the shunt, the transducer gets 7.56 V from a rail 5 % low, 4.44 V short of its 12 V minimum. A 24 V boost on the interface board gives it 20.16 V, a margin of 8.16 V [B1]. The boost and a 3.3 V regulator for the ADC and barometric sensor are added to BOM line 7 (+$2).
- **ADC protection.** A 25 mA fault puts 3.75 V on the shunt, above the ADC's 3.6 V limit at a 3.3 V supply, so the ADC input needs a series resistor [B1b].
- **Energy.** Each reading takes 1.38 J in the loop (24 V at 22 mA for 2 s, through the boost and the FieldNode rail) plus 0.053 J for the controller, 1.43 J in all [B2]. At 15 min that is 38.2 mWh a day, 1.59 mW on average: 1.6 % of FieldNode's published 100 mW allowance [B3]. **R8 is met.** During a pumping test at 1 min the load is 0.573 Wh a day, 23.9 mW, or 24 % of the allowance [B4]. The TRL 2 estimate, 0.66 J and 18 mWh a day, assumed the loop ran straight from the 12 V rail [B5].

## C. Accuracy and drift (R4, R5)

- **Gravity and density.** Converting kPa to head with standard gravity misreads 10 m by +27 mm at the equator, so firmware uses local gravity and the calibration absorbs the rest [C1]. Water density falls 0.29 % from 4 to 25 °C, 29 mm at 10 m [C2]; groundwater temperature at one well changes little, so firmware uses a fixed site density set at installation.
- **Calibration method.** At installation the caretaker reads depth to water with the tape, then lifts the probe a measured 1 m in its tube and reads again. The two points fix offset and span, removing the datasheet offset and span error, the gravity error and the cable length error. What remains is in Table 2.

*Table 2. Error budget at full scale after a two-point calibration, 0.25 % class probe [C3.1] to [C4].*

| Term | Error |
| --- | --- |
| Nonlinearity, hysteresis and repeatability | 10.0 mm |
| Probe thermal effect, 2 K | 4.0 mm |
| Density at a fixed site value, 2 K | 3.2 mm |
| Shunt drift, 30 K | 3.8 mm |
| ADC gain drift, 30 K | 2.6 mm |
| ADC resolution | 0.5 mm |
| Manual tape reference | 3.0 mm |
| Root sum square | 12.5 mm |
| Worst-case sum | 27.1 mm |

- **R4 is at risk.** The root sum square meets ±20 mm; the worst-case sum does not, and the nonlinearity figure, the largest term, is a typical value rather than a measured one [C4]. A 0.5 % class probe gives 21.4 mm root sum square and 37.1 mm worst case, so it does not meet R4 even after calibration [C5]; BOM line 1 is therefore specified in the 0.25 % class. Without field calibration the datasheet figures are 50 mm and 25 mm [C6]. An absolute sensor without barometric compensation would read weather as water level, ±306 mm for ±3 kPa [C7], which is why the vented design was adopted (DDR-001, D2).
- **R5 cannot be verified at TRL 3.** A quarterly tape check leaves at most 5 mm of a 20 mm-a-year drift uncorrected between checks, close to the 3 mm tape uncertainty [C8]. The real drift of low-cost probes is unknown.

## D. Fit in the well and hanging loads (R2, R10)

- **Model.** In the 150 mm design well the tube sits 32.2 mm clear of the riser and 18.3 mm from the casing wall. Under WLS-DDR-002 the 1 in tube is kept and the probe body is limited to 22 mm, which gives 2.3 mm radial clearance in the 26.6 mm bore of 1 in Sch 40 PVC [D1], against 1.3 mm for the 24 mm probe of v0.1. Joints must be flush inside so a solvent bead does not catch the probe.
- **Tube size.** The 1 in tube takes probes up to 22 mm with 2 mm of radial clearance and fits beside a centered riser in 150 and 200 mm casings, and beside a riser against the wall in all four sizes checked. A 1-1/4 in tube takes probes up to 28 mm but fits beside a centered riser only in 200 mm casing [D2]. The tube ends above the pump, so the pump body does not limit the fit.
- **R10 is at risk.** The tube and a 22 mm probe fit the design well, but lowering a tube past the riser, cable ties and pump cable of an installed pump may snag them or need the pump pulled. Only an installation trial can settle it.
- **Loads.** Cable and probe hanging 60 m in air weigh 35 N against a 400 N strain member, a factor of 11.5 [D3]. Sixty metres of tube hanging dry weigh 264 N, a stress of 0.82 MPa against 48 MPa, a factor of 58; a split collar on the tube carries the 264 N onto the seal plate [D4]. **R2 is met.**
- **Load paths of the constructable wellhead (WLS-DDR-004).** The collar bears on the 20 mm HDPE seal plate at 0.24 MPa, about a factor of 82 under HDPE's compressive strength; the collar's grip on the tube is its maker's rating, to be confirmed at purchase [D5]. The probe and cable (35 N at 60 m) hang from a cable support grip on an M5 eye bolt (the cross bolt) through the tube cap; the bolt bears on the two 4.4 mm cap walls at 0.79 MPa against about 50 MPa for PVC, and the cap sits on the tube end, so the load reaches the collar through the tube [D6]. The padlock hung on the eye adds 1.0 N (0.81 MPa on the cap walls); it stops the eye bolt being unscrewed but not the cap being lifted off the tube, so exposed sites need the lockable steel wellhead cover [D7].

## E. Storage and airtime (R6, R7)

- **R7 is met.** A year of 15 min readings is 35,040 records of 32 bytes, 1.12 MB, 6.7 % of the FieldNode's 16 MB flash [E1]. A 7-day pumping test at 1 min adds 0.32 MB [E2].
- **R6 is met.** The 15 min default and the 1 min test rate are firmware settings. At 1 min the readings are logged and sent 15 at a time in the normal 15 min uplink. That 38-byte batch takes 328.7 ms at SF9, 31.6 s a day, slightly over the 30 s a day fair use of a public network; on a private TwinKit gateway only the regional duty cycle applies [E3]. Under WLS-DDR-002, a test on a public network sends every 30 min instead: a 30-reading batch of 68 bytes takes 472.1 ms, 22.7 s a day, within fair use [E4]. On a private TwinKit gateway the 15 min batch is kept.

## F. Vent desiccant (maintenance)

The vent capillary holds 111 mL at 62.7 m. With the box and vent breathing 0.15 L a day at a 30 K swing, humid air carries at most 3.6 mg of water a day; 10 g of gel would last about 552 days even if the whole box breathed through it, a factor of 6.1 over the quarterly change [F1]. The quarterly desiccant change has ample margin, provided the box gaskets are intact.

## G. Installation (R11)

With an access tube already in place, ten steps from isolating the pump to fitting the padlocks are estimated at 125 min for two people, 5 min over the R11 limit once the locks are fitted, with the post footing set and cured on an earlier visit [G1]. **R11 cannot be verified at TRL 3**; only a timed installation can.

## H. Cost (R12)

- **BOM.** All 16 lines are priced. The design case uses 33 m of cable (30 m down the well and a 2.7 m surface run that includes a 1.1 m service loop in the junction box for the 1 m calibration lift) and 30.61 m of tube (31 m in the BOM) [H1].
- **R12, over the value-engineering target.** Value-engineering target: USD 200 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 262.40 for lines 1 to 7, 9, 10 and 13 to 16 (USD 62.40 over the target); with the $139.00 FieldNode core (FND-CAL-001 v0.3) the complete logger is $401.40, and $410.40 at a hot site with FieldNode's $9.00 sun shield [H2]. Making the design constructable (WLS-DDR-004) repriced lines 4, 5, 6, 7, 10 and 14 and added line 15, the FieldNode lead; the concept total was $197.60 [H2c]. The locks decided on 2026-10-02 add $18.00: line 16 at $16.50 and $1.50 for the eye bolt in line 5 [H2d]. Without the $20.00 conduit set (line 14) the parts would be $242.40 [H2b]. The fixed parts alone are $208.40, so the target is not met at any depth. Cable and tube add $1.80 per metre of depth; at 60 m the parts cost $316.40, and without an access tube (no pump in the casing) $231.40 [H3]. Savings worth trying are listed in the design decisions register (WLS-DEC-001).

## L. Results against every requirement

*Table 3. Requirement status from this note [L].*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R9 | Water safety | No drinking water certificate in hand for low-cost cable, seal or probe | Wetted parts 316 stainless or certified for drinking water; well sealed | **Not met** (no evidence) |
| R4 | Accuracy after field calibration | 12.5 mm RSS, 27.1 mm worst case (0.25 % class) | ±20 mm | **At risk** |
| R10 | Pump compatibility | 2.3 mm radial clearance with a 22 mm probe; tube may need the pump pulled | Own tube, no contact with pump, riser or cable | **At risk** |
| R15 | Environment | Probe IP68 on datasheet; FieldNode shield at hot sites gives 48.5 to 52.2 °C inside at 45 °C; FieldNode rated to 45 °C ambient | Above-ground parts IP65, -10 to 55 °C; FieldNode shield at hot sites | **At risk** |
| R16 | Tamper resistance | Cable in galvanized conduit from the tube cap to the box; by design review the seal plate (security-head screw), cross bolt (padlock on its eye) and junction box (hasp and padlock) are each lockable; lifting the cap at exposed sites needs the steel cover [D7] | Lockable; no exposed cable at reachable height | **Met** (design review) |
| R5 | Long-term drift | Unknown; a quarterly check leaves at most 5 mm | 20 mm a year or less | Not verifiable at TRL 3 |
| R11 | Installation | 125 min estimate with the locks fitted [G1] | 2 h or less with a tube in place | Not verifiable at TRL 3 |
| R13 | Data use | Dashboard not started | Level, drawdown, year-on-year, CSV | Not verifiable at TRL 3 |
| R1 | Range | 0 to 10 m, 98.07 kPa | 0 to 10 m; 0 to 20 m option | Met |
| R2 | Installation depth | Cable factor 11.5, tube factor 58 at 60 m | 60 m or more | Met |
| R3 | Resolution | 0.52 mm | 1 mm or better | Met |
| R6 | Reading interval | 15 min; 1 min logged, sent every 30 min on a public network (22.7 s/day) | 15 min; 1 min in tests | Met |
| R7 | Local storage | 1.12 MB a year, 6.7 % of flash | 1 year | Met |
| R8 | Energy | 38.2 mWh/day, 1.6 % of 100 mW | 5 % or less | Met |
| R12 | Cost | $262.40 at 30 m; $401.40 with FieldNode | Value-engineering target $200 for WellSense parts at 30 m | Over the target by $62.40 |
| R14 | Data ownership | Levels, time and well ID only | Community controls sharing | Met (by design) |

Counts: 1 not met, 3 at risk, 3 not verifiable at TRL 3, 8 met, and R12 over the value-engineering target.

## Checks against the TRL 2 figures

| TRL 2 claim (WLS-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| Resolution about 0.5 mm | 0.52 mm | Stands |
| Datasheet accuracy about ±50 mm | 50 mm (0.5 %), 25 mm (0.25 %); 12.5 mm RSS after calibration | Precis and REQ updated; R4 now at risk |
| Energy about 0.66 J per reading, 18 mWh/day | 1.43 J and 38.2 mWh/day with the 24 V boost | Precis updated |
| About 0.6 % of a 2.8 Wh/day allowance | 1.6 % of 100 mW (2.4 Wh/day) | Precis updated |
| Storage about 0.3 MB a year at 8 bytes | 1.12 MB at FieldNode's 32-byte record | Precis and REQ updated |
| Parts about $170; about $296 with FieldNode | $187.60 and $313.60 in v0.1; $197.60 and $323.60 in v0.2 | Precis, README and REQ updated |
| Depth-dependent about $1.80 per metre | $1.80 per metre | Stands |
| 12 V rail powers the loop directly | Short by 4.44 V; 24 V boost needed | Precis and BOM updated |

## Changes in v0.2 (WLS-DDR-002)

| Item | v0.1 | v0.2 |
| --- | --- | --- |
| `budget_usd` | $180 | $190; $200 in v0.3 (approved by Amish, 2026-09-26) [H2] |
| Probe body and clearance | 24 mm, 1.3 mm radial | 22 mm maximum, 2.3 mm radial [D1] |
| Surface cable | Exposed from the tube cap to the box | Galvanized conduit, BOM line 14, $10.00 |
| WellSense parts at 30 m | $187.60 ($7.60 over $180) | $197.60 ($7.60 over $190; $2.40 under the $200 budget of v0.3) [H2] |
| Pumping test uplinks, public network | 15 min batches, 31.6 s/day | 30 min batches, 22.7 s/day [E4] |
| R15 hot sites | FieldNode 45 °C rating only | FieldNode shield required at hot sites (FND-DDR-002) |

## Changes in v0.4 (WLS-DDR-004, design for construction)

| Item | v0.3 | v0.4 |
| --- | --- | --- |
| Surface cable run | 2 m | 2.7 m, including a 1.1 m service loop for the calibration lift; 63 m loop at 60 m depth [B1], [F1] |
| Tube load path | "A tube clamp is needed" | Split collar on the tube bearing on the HDPE seal plate, 0.24 MPa [D5] |
| Probe load path | Cable-grip hanger, not specified | Support grip on an M5 cross bolt through the cap, 0.79 MPa on the cap walls [D6] |
| BOM | 14 lines, $197.60 | 15 lines, $244.40; lines 4, 5, 6, 7, 10 and 14 repriced, line 15 added [H2], [H2c] |
| FieldNode core | $126.00, shield $8.00 | $139.00 and $9.00 (FND-CAL-001 v0.3) [H2] |
| R12 | Met against the $200 budget | Over the $200 value-engineering target by $44.40 |

## Changes in v0.5 (locking, WLS-DEC-001)

| Item | v0.4 | v0.5 |
| --- | --- | --- |
| Locks | Not specified | Security-head screw on the rim band, padlock on the eye of the cross bolt, hasp and padlock on the box; BOM line 16 [H2d], load check [D7] |
| BOM | 15 lines, $244.40 | 16 lines, $262.40; line 16 added and line 5 repriced to $11.50 for the eye bolt |
| R16 | At risk | Met on design review; the cap itself can still be lifted, so exposed sites use the steel cover |
| R11 estimate | 120 min | 125 min, 5 min over the limit, with the locks fitted [G1] |
| R12 | Over the target by $44.40 | Over the target by $62.40 |
