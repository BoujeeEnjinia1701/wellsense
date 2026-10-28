---
doc_id: WLS-RSK-001
title: WellSense risk register and hazard analysis
project: WellSense
doc_type: Risk register
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First issue (kit 1.9.1 upgrade) with the project risk register, preliminary hazard analysis and first-pass design FMEA of the current design (option A)
---

# WellSense risk register and hazard analysis

The top project risks are evidence for drinking-water safety (no material certificates for the low-cost wetted parts) and whether a low-cost vented probe holds ±20 mm and 20 mm a year in a real well; the top hazards are contaminating a supply well and electric shock from the existing pump's mains supply while the wellhead is open. The design FMEA's highest RPN items are vent blockage (F-1) and transducer drift (F-4), both 36, then a gap in the seal plate (F-9, 30); the tube string dropping into the well (F-2) scored 60 before the clevis pin of WLS-DEC-001 D-S1 and 20 after it. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be found) to 5 (unlikely to be found).

> **Safety:** Drinking water, mains-powered pumps, open wells, a lithium iron phosphate cell in the FieldNode core and heavy cable runs. See WLS-PRC-001, Safety, and the safety stops in WLS-BLD-001.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-1 | No drinking-water certificates for wetted parts | Low-cost suppliers rarely hold NSF/ANSI/CAN 61 or equal for probes, cable and seal materials | PR-009 stays not met; partner or authority will not allow the probe in a supply well | 4 | 5 | Design lead | Ask suppliers at purchase (DEC to confirm item 1); fall back to certified grades and accept the cost; option C reduces wetted parts to the tube (WLS-OPT-001) |
| R-2 | Low-cost probe misses ±20 mm or drifts more than 20 mm a year | Unmeasured nonlinearity, thermal effect and drift of low-cost transducers | PR-004 and PR-005 not met; data not trusted by the community | 3 | 4 | Design lead | Side-by-side tape record at TRL 4; quarterly tape checks correct drift; choose the 0.25 % class |
| R-3 | Access tube cannot pass an installed pump's riser and cable | Tight casing, couplings and cable clamps on the riser | Tube only fits when the pump is pulled, which owners avoid | 3 | 4 | Partner field lead | Installation trial with the partner; fit the tube when a pump is next pulled; a 19 mm probe gives more room |
| R-4 | Cost stays over the USD 200 target | Locks, conduit, constructable wellhead parts | PR-012 over target (USD 64.40 now) | 4 | 2 | Project lead | Value-engineering savings in WLS-DEC-001; option C if proven; budget is a control target, not a limit |
| R-5 | Partner not engaged | ACWADAM not yet approached | Requirements stay the author's reading; no field trial | 3 | 4 | Project lead | Approach the first candidate partner (WLS-DEC-001); Helpful Engineering network as fallback |
| R-6 | FieldNode core not confirmed at 55 °C ambient | FieldNode rated to 45 °C with its shield | Hot sites excluded (PR-015 at risk) | 3 | 3 | FieldNode project | Sites above 45 °C not used until FieldNode confirms (WLS-DEC-001) |
| R-7 | Dashboard not built | Software not started | PR-013 not met; data not used in meetings | 3 | 3 | Software lead | Plan it in co-design (WLS-PLN-001); CSV export first |
| R-8 | Data misuse or conflict over shared groundwater | Level data could be used against a community or a farmer | Loss of trust, removal of loggers | 2 | 4 | Partner | Levels only; community controls sharing (PR-014); agree rules before installing |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H-1 | Contamination of a drinking water supply | Undisinfected probe, cable or tube; wetted materials that leach; wellhead left open | Illness of everyone drinking from the well | 5 | 2 | Disinfect everything lowered in (AWWA C654 practice, STM S25); certified materials (PR-009); split seal plate with gasket and wraps; install with the owner or authority | Medium until certificates are in hand |
| H-2 | Electric shock from the pump's mains supply | Working at an open wellhead beside a live pump cable | Electric shock, death | 5 | 2 | Isolate and lock off the pump supply before opening the wellhead (build plan safety stops); WellSense itself is 24 V or less (PR-018); logger wiring kept apart from the pump cable | Low |
| H-3 | Fall or drowning at an open well | Large-diameter or open well left uncovered during work | Injury or death, especially of children | 5 | 1 | Never leave a wellhead open; cover large wells while working (PRC Safety) | Low |
| H-4 | Tube string, probe or cable dropping into the well | Collar grip creeps on PVC; cable runs away while lowering | Lost probe, pump fouled, well out of use | 3 | 2 | Clevis pin on the collar (D-S1, STM S14); two people lower the string slowly (STM S26); cable strain member factor 11.5 | Low |
| H-5 | Lithium iron phosphate cell fault in the FieldNode core | Charging out of temperature, damage | Fire, burns | 4 | 1 | FieldNode's fusing and charge limits; hot-site rule (WLS-DEC-001) | Low |
| H-6 | Manual handling strain | Lifting the post, footing concrete, a 60 m tube string | Back injury | 2 | 2 | Two people; loads under 25 kg each (STM S26) | Low |
| H-7 | Cuts and swarf | Drilling PVC, HDPE and aluminium; sawing the post | Cuts, eye injury | 2 | 3 | Eye protection, deburring (WLS-BLD-001 section 7) | Low |
| H-8 | Tampering or theft at the wellhead | Exposed parts at a public water point | Contamination path, lost logger | 3 | 3 | Locks on the seal plate, cap and box; cable in conduit (PR-016); steel cover at exposed sites | Low to medium |

## Design FMEA (first pass, P3)

Table 3. Failure modes of the chosen design (option A). RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-1 | Vent capillary and breather (BOM 2, 6) | Keep the transducer referenced to air | Water or condensate blocks the vent | Reading drifts with air pressure by up to ±306 mm | Desiccant spent; condensation in the cable in a cool well | 4 | 3 | 3 | 36 | Quarterly desiccant change (PR-017, 552 days of capacity); barometric sensor flags a blocked vent by correlation |
| F-2 | Collar, clevis pin and seal plate (BOM 4) | Carry the access tube string | Tube slips through the collar | String drops into the well, probe lost | PVC creep under the collar clamp | 5 | 1 | 4 | 20 | Closed by D-S1: clevis pin takes the load if the grip slips (was O 3, RPN 60 before the fix) |
| F-3 | Access tube joints (BOM 3) | Let the probe run freely | Probe snags on a cement bead | Probe cannot be lowered or lifted for calibration | Excess solvent cement; thick-walled pipe | 3 | 2 | 2 | 12 | Closed by D-S2: wipe joints, pull a 23 mm drift through before the probe |
| F-4 | Transducer (BOM 1) | Read the head of water | Offset or span drift | Level error beyond ±20 mm | Low-cost sensor ageing, temperature | 4 | 3 | 3 | 36 | Quarterly tape check and correction (PR-005); 0.25 % class probe with a factory calibration certificate for span (D-S3); side-by-side record at TRL 4 |
| F-5 | Interface board, boost (BOM 7) | Power the loop at 24 V | Boost fails or rail sags | No reading | Component failure, surge | 3 | 2 | 1 | 6 | FieldNode reports a missing reading at once; TVS surge protection; spare module costs a few dollars |
| F-6 | Shunt and ADC (BOM 7) | Convert current to a number | Gain drift with box temperature | Level error up to a few millimetres | 10 ppm/K shunt, ADC drift over 30 K | 2 | 3 | 4 | 24 | 0.1 % 10 ppm/K shunt; drift in the error budget (WLS-CAL-001 [C3]) |
| F-7 | Vented cable (BOM 2) | Carry signal and vent; hold the probe | Jacket cut or crushed | Water ingress, lost reading, vent blocked | Livestock, mowing, tampering at the surface | 4 | 2 | 2 | 16 | Galvanized conduit and flexible tail (PR-016) |
| F-8 | Cable support grip and eye bolt (BOM 5) | Set and hold the probe depth | Grip slips | Probe depth changes, offset error | Grip not suited to the cable diameter | 3 | 2 | 3 | 18 | Grip for 6 to 8 mm cable, 35 N (DEC to confirm item 5); the tape check finds an offset |
| F-9 | Seal plate, gasket and wraps (BOM 4) | Keep surface water and insects out | Gap at the riser or pump cable | Contamination path into the well | Riser or cable diameter differs from design | 5 | 2 | 3 | 30 | Measure the riser and cable at the well before cutting the plate (DEC to confirm item 2); EPDM wraps take up a few millimetres |
| F-10 | Junction box and glands (BOM 6) | Keep the electronics dry | Water ingress | Corrosion, lost reading | Gland not tightened; lid seal aged | 3 | 2 | 3 | 18 | IP66 box; glands checked each quarter |
| F-11 | FieldNode lead and M12 plug (BOM 15) | Carry power and I2C | Plug loosened or corroded | No reading | Vibration, moisture | 3 | 2 | 1 | 6 | IP67 plug; missing readings show at once |
| F-13 | Interface board, shunt (BOM 7) | Convert loop current | Shunt burns out | No reading; board replaced | Short between the cable cores puts 24 V across the shunt (149 mA, 3.3 W) | 3 | 2 | 2 | 12 | Closed by D-S4: 50 mA resettable fuse in the loop (was O 2 with no protection, RPN 12 with a board lost) |
| F-12 | Post and footing (BOM 10, 13) | Hold the logger | Post leans or is knocked over | Conduit strained, logger damaged | Livestock, soft ground | 3 | 2 | 1 | 6 | 0.6 m concrete footing; visible at each visit |

## Option notes

Options B and C (WLS-OPT-001) would change F-1, F-4 and F-7: B replaces the vent with a pump and valve (new failure modes: pump diaphragm wear, line leak, water entering the line during an outage), and C removes every wetted electronic part (new failure modes: condensation on the head's speaker and microphone, insects in the tube, lost echo at depth). These are not scored until Amish chooses (WLS-DDR-005).
