---
doc_id: WLS-STM-001
title: WellSense STEM check
project: WellSense
doc_type: STEM check
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First STEM check (kit 1.9.1 upgrade) of the current design (option A) and options B and C; four detail failures fixed under Amish's standing instruction of 2026-10-23 (WLS-DEC-001 D-S1 to D-S4, two of them found by the independent review); independent review recorded
---

# WellSense STEM check

Verdict: every claim the current design (option A) makes sits within known science once four detail failures are fixed; 25 of its 28 rows are within known science and 3 are plausible and can only be closed by data at TRL 4 (calibrated accuracy, S7; long-term drift, S10; junction box temperature in full sun, S21), so `stem_check` is **open**. The author's first run found two failures, both engineering details: the split collar that carries the access tube relies on friction on PVC, which creeps (S14), and the 22 mm probe has less than the 2 mm design clearance at the thickest Sch 40 wall and at a cement bead (S18). The independent review found two more: a 1 m lift cannot calibrate the probe's span (S7), and a short of the cable cores would burn the shunt (S28). All four were fixed in this session under Amish's standing instruction of 2026-10-23 (WLS-DEC-001 D-S1 to D-S4) and the check was rerun; none changes the working principle. Options B (bubbler) and C (acoustic sounder) have no failing row; B has 2 and C has 3 plausible rows that their own development would have to close. Method and rules: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py` (results in `docs/04-calcs/stem_results.csv`); option A's full calculations are in WLS-CAL-001, whose tags appear in brackets.

> **Safety:** These are first-principles screens for a paper proof of concept. They do not show that anything lowered into a supply well is safe for drinking water or that work at a well with a mains-powered pump is safe. See WLS-PRC-001, Safety.

## Claims checked

### Option A: vented transducer in an access tube (current design)

Table 1. Claims of option A, governing science and verdicts.

| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | Full-scale pressure of the 0 to 10 m range is 98.07 kPa (PR-001) | Physics | Fluid mechanics | Hydrostatic pressure p = rho g h | claimed 98.07 kPa, estimate 98.1 kPa (ratio 1.00) | Within known science |  |
| S2 | A vented (gauge) transducer cancels air pressure swings that would put +/-306 mm on an absolute sensor (+/-3 kPa weather) | Physics | Fluid mechanics | Gauge pressure is referenced to the atmosphere through the vent capillary (USGS TM 1-A1, 2011) | claimed 306 mm, estimate 306 mm (ratio 1.00) | Within known science |  |
| S3 | ADC step (quantisation) 0.52 mm with a 150 ohm shunt and a 16-bit ADC (PR-003); noise-limited resolution of the probe and ADC is to measure at TRL 4 | Engineering and technology | Sensing resolution | 16 mA x 150 ohm = 2.4 V span over a 125 uV step [A2] | 0.52 mm <= 1 mm | Within known science |  |
| S4 | With the 24 V boost the transducer gets 20.16 V at 22 mA through 63 m of cable (the 12 V rail alone gives 7.56 V) | Physics | Electromagnetism and circuits | Ohm's law round the loop; transducer minimum 12 V (BOM line 1) [B1] | 20.16 V >= 12 V | Within known science |  |
| S5 | At a 25 mA fault the shunt gives 3.75 V; a 10 kohm series resistor keeps the ADC input current to 15 uA | Engineering and technology | Standards practice | ADS1115 absolute maximum: input current 10 mA continuous, VDD + 0.3 V [B1b] | 0.015 mA <= 10 mA | Within known science |  |
| S6 | Sensor energy 38.2 mWh a day at 15 min, 5 % or less of FieldNode's 100 mW sensor allowance (PR-008) | Physics | Electromagnetism and circuits | Energy balance: 24 V x 22 mA x 2 s through boost (85 %) and rail (90 %) plus the controller [B2, B3] | 38.2 mWh/day <= 120 mWh/day | Within known science |  |
| S7 | A 0.25 % class probe reaches +/-20 mm after calibration (PR-004). First run: a two-point calibration with a 1 m lift was claimed to fix span; two tape readings and two repeatability terms over 1 m give 1.5 % of span, 148 mm at 10 m: fails (independent review). Fixed: offset from the installation tape reading, span from the probe's per-unit factory certificate (0.10 % of reading, to confirm), refined by tape checks at levels 3 m or more apart | Mathematics | Statistics and uncertainty | Error budget of eight independent terms, root sum square against worst-case sum [C3, C4, C4b] | RSS 16.0 mm, worst case 37.1 mm against 20 mm; terms are typical datasheet values, not measured | Plausible, to confirm at TRL 3 | Method fixed by WLS-DEC-001 D-S3; open: PR-004 side-by-side tape test, TRL 4 |
| S8 | Water density changes 0.29 % between 4 and 25 degC, so firmware uses a fixed site density set at installation | Physics | Thermodynamics | Thiesen equation of state for water [C2] | claimed 0.29 %, estimate 0.293 % (ratio 0.99) | Within known science |  |
| S9 | Using standard gravity reads 10 m about 27 mm low at the equator; firmware uses local gravity | Mathematics | Units and dimensional analysis | WGS 84 normal gravity formula [C1] | claimed 27 mm, estimate 26.9 mm (ratio 1.00) | Within known science |  |
| S10 | A quarterly tape check keeps the uncorrected drift to 5 mm or less if the probe drifts 20 mm a year or less (PR-005) | Engineering and technology | Sensing resolution | Drift budget: 20 mm a year over a 91-day interval [C8] | 5 mm between checks against the 20 mm target; long-term drift of low-cost vented transducers is not published | Plausible, to confirm at TRL 3 | Open: PR-005 field record, TRL 4 |
| S11 | Cable and probe hanging 60 m in air (35 N) stay below the 400 N strain member (PR-002) | Physics | Strength of materials | Weight of 0.055 kg/m cable and a 0.25 kg probe [D3] | 34.8 N <= 400 N | Within known science |  |
| S12 | Cable stretch at 60 m (16 mm) is a fixed offset the installation calibration removes; a full 10 m level swing changes it by 2.7 mm (aramid strain member taken as about 1 mm2 at 70 GPa, EA 70 kN, typical, to confirm with the cable maker) | Physics | Strength of materials | Elongation = integral of tension over EA; buoyancy of the submerged cable | 2.7 mm <= 5 mm | Within known science |  |
| S13 | The 60 m access tube hanging dry (264 N, 0.82 MPa) stays well below PVC's 48 MPa tensile strength | Physics | Strength of materials | Self-weight stress of PVC, 1,400 kg/m3 [D4] | 0.82 MPa <= 16 MPa | Within known science |  |
| S14 | The tube string is held at the plate over its life. Friction of the split collar alone: 833 N new, about 278 N after PVC creep, against 792 N (3 x 264 N): fails. Fixed with a 5 mm stainless clevis pin through the tube on a chord above the collar, carrying 299 N (tube, cable and probe): sustained PVC bearing 7.0 MPa on the 4.3 mm chord wall against PVC's 13.8 MPa long-term design stress, pin shear 7.6 MPa; 69 mm of tube above the pin rules out shear-out | Engineering and technology | Standards practice | Clamp preload F = T/(K d); friction mu F; PVC stress relaxation; pin bearing against the long-term design stress of PVC 1120 (13.8 MPa, 2,000 psi) | 7 MPa <= 13.8 MPa | Within known science | WLS-DEC-001 D-S1 (fix rule, 2026-10-25) |
| S15 | The collar spreads the tube load onto the HDPE seal plate at 0.24 MPa | Physics | Strength of materials | Bearing stress against about 20 MPa for HDPE [D5] | 0.24 MPa <= 6.667 MPa | Within known science |  |
| S16 | The probe and padlock hang from the M5 eye bolt; the PVC cap walls carry 0.81 MPa in bearing | Physics | Strength of materials | Bearing on two cap walls against about 50 MPa for PVC [D6, D7] | 0.81 MPa <= 16.67 MPa | Within known science |  |
| S17 | The service loop in the junction box (1.13 m) lets the probe lift 1 m for the response check at installation and be pulled for inspection | Mathematics | Orders of magnitude | Coil length 2 pi r n from the model | 1.13 m >= 1 m | Within known science |  |
| S18 | A 22 mm probe runs freely in the tube: 2.3 mm radial at the nominal bore, 1.74 mm at the thickest Sch 40 wall and 1.24 mm at a solvent-weld joint with a 0.5 mm cement bead, below the 2 mm design rule: fails. Fixed by wiping the joints and pulling a 23 mm drift through the string before the probe goes in, which proves at least 0.5 mm radial everywhere, ovality and bow included; 0.5 mm is enough for a probe hanging free on its cable (nominal-wall bore 26.1 mm gives 2.07 mm) | Engineering and technology | Manufacturing tolerances | Pipe bore from OD and wall tolerances (ASTM D1785); running clearance | 0.5 mm >= 0.5 mm | Within known science | WLS-DEC-001 D-S2 (fix rule, 2026-10-25) |
| S19 | The 40 drilled 8 mm holes (2011 mm2) let the water in the tube follow the casing level: the tube's air vents through the cap's conduit to the box breather, and even at 10 mm of head difference the tube fills 10 m in about 10 s | Physics | Fluid mechanics | Open area against the bore area; orifice flow | 3.6 x bore area >= 1 x bore area | Within known science |  |
| S20 | 10 g of silica gel keeps the vent and box air dry about 552 days at worst-case daily breathing, more than the 91-day change interval (PR-017); permeation through gaskets and glands is not counted | Chemistry | Physical chemistry | Gas law breathing at a 30 K daily swing; silica gel uptake 20 % by mass [F1] | 552 days >= 91 days | Within known science |  |
| S21 | At 55 degC ambient in full sun the junction box stays within the 85 degC rating of the modules (PR-015) | Physics | Heat transfer | Solar gain alpha G A_sun against convection h A_total, alpha 0.5, G 1,000 W/m2, h 10 W/m2K, A_sun/A_total 0.22 | 66 degC by the balance; small enclosures in full sun are often measured 20 to 35 K above ambient, which would reach 75 to 90 degC | Plausible, to confirm at TRL 3 | Open: PR-015 box temperature log, TRL 4 |
| S22 | One year of 15 min readings fills 1.12 MB of FieldNode's 16 MB flash (PR-007) | Mathematics | Orders of magnitude | 35,040 readings x 32 bytes [E1] | 1.12 MB <= 16.78 MB | Within known science |  |
| S23 | Pumping-test batches every 30 min on a public network use 22.7 s of airtime a day at SF9 (PR-006); valid at SF9 only: at SF10 and above a test sends from a private gateway or in hourly batches | Engineering and technology | Power and link budgets | Semtech LoRa time-on-air formula; 30 s a day fair use on The Things Network [E4] | 22.7 s/day <= 30 s/day | Within known science |  |
| S24 | 316 stainless, PVC, HDPE, EPDM and PU or PE cable jackets can be had in grades certified for drinking water contact (PR-009) | Chemistry | Materials and polymer chemistry | NSF/ANSI/CAN 61 lists components of all these material classes | Material classes are routinely certified; no certificate is in hand for the chosen low-cost parts, so PR-009 stays not met on evidence | Within known science |  |
| S25 | Disinfecting the probe, cable and tube with chlorine solution before they go into the well reduces the risk of bringing bacteria into the supply | Biology | Microbiology | AWWA C654 (disinfection of wells) and the local water authority's practice | Standard well practice; the build plan and PRC safety notes carry it | Within known science |  |
| S26 | Two people can lower the 30 m design-case tube string and cable (15 kg) by hand; at 60 m (30 kg) a third person or a hand line is used | Biology | Ergonomics | UK HSE guideline weights, 16 kg per person (women) to 25 kg (men) for lifting close to the body (INDG143) | 7.6 kg per person <= 16 kg per person | Within known science |  |
| S27 | Every WellSense circuit runs at 24 V DC or less, within extra-low voltage (PR-018) | Engineering and technology | Standards practice | ELV band: 120 V ripple-free DC or less (IEC 61140) | 24 V DC <= 120 V DC | Within known science |  |
| S28 | A short between the cable cores puts the 24 V boost across the shunt: 149 mA and 3.3 W in a small shunt: fails. Fixed with a 50 mA resettable fuse (PTC) in series with the loop on the interface board: it trips within about 1 s, and a 0.6 W metal film shunt carries 3.3 W for that second; normal loop current (22 mA) is below its hold current | Engineering and technology | Standards practice | Ohm's law; PTC hold and trip currents; short-time overload of film resistors | 22 mA <= 50 mA | Within known science | WLS-DEC-001 D-S4 (fix rule, 2026-10-25) |

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails, fix proposed**, **Fails**. Rows S14 and S18 failed on the first run, and S7 and S28 failed in the independent review; each is shown with its fix and the first figures are kept in the claim. S7 stays plausible after its fix, because the remaining budget (16.0 mm RSS, 37.1 mm worst case) rests on typical, unmeasured datasheet terms.

### Fixes made under the fix rule

- **S14, tube retention (WLS-DEC-001 D-S1).** The split aluminium shaft collar was the only thing holding the access tube string (264 N at 60 m). A collar holds by the clamp preload of its screw, about 833 N of friction on new PVC at the reduced torque plastic pipe takes, but PVC relaxes under a constant clamp to about a third of its short-term stiffness over years, leaving about 278 N against the 792 N a factor of 3 needs. If the grip went, the tube, probe and cable would drop into the well and could foul the pump. Options weighed: (a) a stainless clevis pin through the tube on a chord just above the collar, so the collar keeps the grip and the pin takes the load only if it slips (about USD 1.50; PVC bearing 7.8 MPa and pin shear 6.7 MPa); (b) a solvent-welded coupling as a shoulder on the plate (needs the string cut at the plate on site, and the shoulder must pass the split plate's hole); (c) a second collar (same creep). Chosen: (a), the cheapest, needs only a drill, and leaves the cable path clear because the chord sits 9 mm off the axis. Implemented in `cad/src/model.py` (tube hole, pin and split pin), BOM line 4, the build plan (WLS-BLD-001 section 3.8 and step 14), WLS-CAL-001 [D5] note and PR-002.
- **S18, probe running clearance (WLS-DEC-001 D-S2).** At the nominal bore the 22 mm probe has 2.3 mm radial clearance, but a 1 in Sch 40 pipe at its thickest wall (ASTM D1785 tolerances, typical tabulated values) leaves 1.74 mm and a 0.5 mm cement bead inside a solvent-weld joint leaves 1.24 mm, under the 2 mm rule of WLS-CAL-001. Options weighed: (a) wipe every joint inside while the cement is wet and pull a 23 mm drift, 300 mm long, through the whole string before the probe goes in (no cost beyond a dowel); (b) specify a 19 mm probe (narrows the supplier list; price unknown); (c) a larger tube (does not pass a centered riser in 150 mm casing, WLS-DDR-002). Chosen: (a); a 19 mm probe stays acceptable under the existing "22 mm or less" specification. Implemented in the build plan (section 3.8 and step 12) and PR-010.

- **S7, span calibration (WLS-DEC-001 D-S3, found by the independent review).** The design took offset and span from a tape reading and a measured 1 m lift. Two tape readings (±3 mm) and two probe repeatability terms (±10 mm) over 1 m fix span only to about 1.5 %, 148 mm at 10 m, far worse than the probe's own 0.25 % class. Options weighed: (a) offset from the tape, span from the probe's per-unit factory calibration certificate, refined by quarterly tape checks once two are 3 m or more apart (no added part; the certificate's cost is to confirm); (b) a longer lift (a 5 m service loop does not fit the box and still leaves about 0.3 %); (c) datasheet span alone (25 mm at full head). Chosen: (a). The 1 m lift is kept as a response check. The budget becomes 16.0 mm RSS and 37.1 mm worst case, so PR-004 stays at risk. Implemented in WLS-CAL-001 [C3] to [C4b], BOM line 1, PRC step 7, PR-004 and the build plan's first checks.
- **S28, cable short (WLS-DEC-001 D-S4, found by the independent review).** A short between the cable cores would put the 24 V boost across the 150 Ω shunt: 149 mA and 3.3 W. Options weighed: (a) a 50 mA resettable fuse (PTC) in series with the loop (about USD 0.50; normal 22 mA is below its hold current); (b) a series current-limit resistor (eats the loop's compliance margin); (c) the boost module's own current limit (not specified for low-cost modules). Chosen: (a). Implemented in BOM line 7, WLS-CAL-001 [B1c] and PR-018.

### Option B: bubbler with a surface sensor

Table 2. Claims of option B.

| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B1 | Option B: back-pressure equals the head over the orifice plus the weight of the air column (71 mm at 30 m), which firmware corrects | Physics | Fluid mechanics | Hydrostatics of water and of the compressed air column, ideal gas | claimed 71 mm, estimate 71.1 mm (ratio 1.00) | Within known science |  |
| B2 | Option B: the bubble-forming overpressure at a 4 mm orifice is about 7 mm; when the pump stops a pinned meniscus leaves 0 to 7 mm, carried as 2 mm in B7 | Physics | Fluid mechanics | Laplace pressure 2 sigma / r, sigma 0.072 N/m | claimed 7 mm, estimate 7.34 mm (ratio 0.95) | Within known science |  |
| B3 | Option B: pump 1.2 W for 8 s and the controller 10 s per reading, 263 mWh a day at 15 min, within FieldNode's 2.4 Wh sensor allowance (11.0 % of 100 mW, above the 5 % target of PR-008) | Physics | Electromagnetism and circuits | Energy balance | 263 mWh/day <= 2400 mWh/day | Within known science |  |
| B4 | Option B: a 12 V miniature diaphragm pump reaches the 118 kPa needed (full head plus 20 %) | Engineering and technology | Power and link budgets | Pump maker's pressure curve | To assess at part selection; many small pumps stop near 80 kPa | Plausible, to confirm at TRL 3 | Open (option B): pump curve at selection |
| B5 | Option B: the 33 m line holds 475 mL; the first fill at full head needs about 935 mL of free air, a few minutes at 0.3 L/min | Mathematics | Orders of magnitude | Boyle's law | claimed 0.9 L, estimate 0.935 L (ratio 0.96) | Within known science |  |
| B6 | Option B: a desiccant inlet keeps compressed air from condensing in the line inside the cooler well; 10 g of gel lasts only about 22 days, so a quarterly change needs about 40 g | Physics | Thermodynamics | Dew point of dried air (about -14 degC at line pressure) against groundwater at 15 to 30 degC; gel uptake 20 % by mass | Dried inlet air cannot reach saturation in the well; gel sized at 40 g | Within known science |  |
| B7 | Option B: a 0 to 150 kPa gauge sensor of the 0.25 % class reaches about 20 mm RSS after calibration (PR-004) | Mathematics | Statistics and uncertainty | Error budget: nonlinearity 0.1 % of 150 kPa, certificate span 10 mm, air column residual 5 mm, tape 3 mm, bubble 2 mm, thermal 4 mm | RSS 20 mm against 20 mm; sensor terms typical, not measured | Plausible, to confirm at TRL 3 | Open (option B): sensor data at selection |

### Option C: acoustic echo sounder

Table 3. Claims of option C.

| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | Option C: sampling the echo at 48 kHz gives a 3.6 mm sample spacing; the timing precision of the correlation peak depends on the signal-to-noise ratio (the chirp's own range resolution is about 0.6 m) | Physics | Acoustics and vibration | Time of flight t = 2L/c, c = 343 m/s at 20 degC | 3.6 mm <= 20 mm | Within known science |  |
| C2 | Option C: +/-20 mm at 30 m needs the mean air temperature of the column to +/-0.21 K, or reflections from tube joints at known depths to calibrate the speed of sound | Physics | Acoustics and vibration | c proportional to the square root of absolute temperature (0.18 % per K); joint counting as in oil-well echo sounders | Whether solvent-weld PVC joints reflect enough is unknown | Plausible, to confirm at TRL 3 | Open (option C): joint echo test, TRL 4 |
| C3 | Option C: at 500 Hz the round trip to water 60 m down loses about 52 dB to the tube walls, recoverable with a short (0.2 s) chirp and correlation once the direct leakage has died away | Physics | Acoustics and vibration | Kirchhoff wall attenuation in a narrow tube | 52 dB at 500 Hz over 120 m; holes and joints add loss | Plausible, to confirm at TRL 3 | Open (option C): echo test, TRL 4 |
| C4 | Option C: a 1 s chirp and capture at 0.4 W uses 11 mWh a day at 15 min (PR-008) | Physics | Electromagnetism and circuits | Energy balance | 10.6 mWh/day <= 120 mWh/day | Within known science |  |
| C5 | Option C: the speaker and microphone survive the saturated air at the top of the tube | Chemistry | Electrochemistry and batteries | Condensation and corrosion of electronics at 100 % relative humidity; IP67 transducers and conformal coating | Needs IP67 parts and a coated board; to confirm | Plausible, to confirm at TRL 3 | Open (option C): part selection |

## Fields not relevant

- Physics, nuclear and ionising radiation: no radioactive material or ionising source.
- Physics, optics and radiation: no optical sensing; solar gain on the box is covered by S21 under heat transfer.
- Chemistry, organic and environmental chemistry beyond S24 and S25: no reagents, emissions or discharges; WellSense measures level only and puts nothing into the water except disinfected wetted parts.
- Biology, ecology, agronomy, plant and animal biology, epidemiology and toxicology beyond S24 to S26: the device does not touch crops, animals or people, and wetted-material toxicology is carried by the drinking water certificates of PR-009.

## Concept options

- **Option A (current design):** within known science after the fixes D-S1 to D-S4; open on S7 (calibrated accuracy, 16.0 mm RSS but 37.1 mm worst case against 20 mm), S10 (drift) and S21 (box temperature in sun), which only TRL 4 records can close.
- **Option B (bubbler):** no failing row. Plausible on B4 (a small 12 V pump must reach about 118 kPa) and B7 (20 mm RSS after calibration, at the limit). Its energy (B3, 11 % of FieldNode's 100 mW allowance) is within physics but misses the 5 % target of PR-008.
- **Option C (acoustic sounder):** no failing row. Plausible on C2 (the speed of sound needs the column temperature to about 0.2 K or joint echoes to calibrate it), C3 (52 dB of wall loss at 500 Hz to water 60 m down) and C5 (electronics in saturated air).

## Independent review

A second agent (a headless `claude -p` session, because this rollout agent had no subagent tool) was given only this document, WLS-CAL-001, WLS-PRS-001 and `docs/04-calcs/sizing.py`, none of the author's reasoning, and asked to refute the headline results and every "Within known science" verdict, recomputing the numbers itself. It reproduced S1, S2, S4, S6, S8, S10, S11, S13, S15, S16, S22, S24, S27, B1, B5 and the 43 dB of C3, and raised 20 findings. What changed:

Table 4. Independent review findings and responses.

| Row | Finding | Response |
| --- | --- | --- |
| S7 | A 1 m lift cannot fix span: about 1.5 %, 148 mm at 10 m; the budget omitted the term | Accepted; fix D-S3 (span from the probe's factory certificate, offset from the tape); budget now 16.0 mm RSS, 37.1 mm worst case; PR-004 stays at risk |
| S5 | A short of the cable cores puts 24 V across the shunt (about 150 mA, 3.3 W); ADS1115 rating is 10 mA continuous | Accepted; fix D-S4 (50 mA resettable fuse), new row S28; S5 wording corrected |
| S21 | The balance hides an area ratio of 0.22; enclosures in sun run 20 to 35 K above ambient | Accepted; ratio stated and the row downgraded to plausible (open, TRL 4 temperature log) |
| S14 | Load omitted the 35 N probe and cable; the pin hole's own sustained bearing was not checked | Accepted; 299 N on the 4.3 mm chord wall, 7.0 MPa against PVC's 13.8 MPa long-term design stress; 69 mm of tube above the pin |
| S18 | The rule was relaxed to 0 mm; the drift proves only 0.5 mm; 26.6 mm is the minimum-wall bore | Accepted; row restated as 0.5 mm proved by the drift, nominal-wall clearance 2.07 mm given |
| S9 | Sign: standard gravity reads low at the equator | Corrected |
| S3 | 0.52 mm is the ADC step, not resolution | Reworded as quantisation; noise-limited resolution to measure at TRL 4 |
| S12 | EA not stated | Stated (about 70 kN, typical, to confirm) |
| S19 | Area only; is the cap vented? | The cap vents through the conduit to the box breather; fill-time estimate added |
| S20 | Breathing only; permeation not counted | Stated in S20 and PR-017 |
| S23 | Valid at SF9 only | Stated, with the fallback |
| S25 | Overstated wording | Reworded: reduces the risk |
| S26 | Cable omitted; 16 kg guideline for women; 60 m case | Recomputed at the 30 m design case (7.6 kg each against 16 kg); a third person or a hand line beyond that |
| B2, B3, B6, B7 | Residual meniscus; controller energy unexplained; inlet gel lasts about 22 days; span term missing | Reworded; controller time stated; gel sized at 40 g; span term added (B7 now 20 mm RSS) |
| C1, C2, C3 | Sample spacing is not resolution; temperature must take a share of the budget (about 0.2 K); chirp overlap; 60 m case 52 dB | Reworded and recomputed |
| C4 | 10.67 against 10.6 mWh | Rounding; unchanged |

The option scores in WLS-OPT-001 did not change: A's accuracy score (4) still reflects a budget inside 20 mm by RSS, and B's and C's corrections lower rows that already scored them below A.

## Sources

- Cunningham, William L., and Charles W. Schalk. *Groundwater Technical Procedures of the U.S. Geological Survey.* Techniques and Methods 1-A1. Reston, VA: USGS, 2011. https://pubs.usgs.gov/tm/1a1/ (cited in WLS-PRB-001).
- Texas Instruments. *ADS111x Ultra-Small, Low-Power, I2C-Compatible, 16-Bit ADCs* (ADS1115 datasheet), absolute maximum ratings (input current, analog input voltage). Typical figures used in WLS-CAL-001.
- Tanaka, M., G. Girard, R. Davis, A. Peuto, and N. Bignell. "Recommended Table for the Density of Water between 0 °C and 40 °C Based on Recent Experimental Reports." *Metrologia* 38 (2001): 301 to 309 (the Thiesen form used in [C2] is the classical equivalent).
- National Geospatial-Intelligence Agency. *World Geodetic System 1984*, normal gravity formula (Somigliana form) used in [C1].
- ASTM International. ASTM D1785, *Standard Specification for Poly(Vinyl Chloride) (PVC) Plastic Pipe, Schedules 40, 80, and 120*: outside diameter and wall tolerances; the values used in S18 are the typical tabulated ones and are to confirm against the standard's current edition.
- NSF International. NSF/ANSI/CAN 61, *Drinking Water System Components, Health Effects*. Standards Council of Canada listing, https://scc-ccn.ca/standardsdb/standards/4032142 (checked 2026-10-24 for the Water Security focus area, StillStack SSK-REG-001).
- American Water Works Association. AWWA C654-13, *Disinfection of Wells*. https://store.awwa.org/AWWA-C654-13-Disinfection-of-Wells-PDF (checked 2026-10-25).
- Health and Safety Executive. *Manual Handling at Work: A Brief Guide* (INDG143), guideline weights.
- International Electrotechnical Commission. IEC 61140, *Protection against Electric Shock: Common Aspects for Installation and Equipment*, extra-low voltage band.
- Semtech. *SX1272/3/6/7/8: LoRa Modem Designer's Guide* (AN1200.13), time-on-air formula; The Things Network fair use policy of 30 s of uplink airtime a day, as used in FND-CAL-001.
- Kinsler, Lawrence E., Austin R. Frey, Alan B. Coppens, and James V. Sanders. *Fundamentals of Acoustics.* 4th ed. New York: Wiley, 2000: speed of sound in air and Kirchhoff wall attenuation in tubes (C1 to C3).
- Echo sounding of liquid levels in wells by counting tubing-collar reflections: McCoy, J. N., A. L. Podio, and K. L. Huddleston. "Acoustic Determination of Producing Bottomhole Pressure." *SPE Formation Evaluation* 3, no. 3 (1988) (C2; method reference, not checked against a PVC tube).
- Plastics creep and stress relaxation of PVC under sustained load: long-term modulus about a third of short-term over 10 years at 23 °C is a typical design value from pipe makers' data; to confirm with the collar's maker (S14).
