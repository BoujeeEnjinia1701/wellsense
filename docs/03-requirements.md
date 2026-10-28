---
doc_id: WLS-PRS-001
title: WellSense product requirements and specifications
project: WellSense
doc_type: Product requirements and specifications
version: "0.9"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold (as WLS-REQ-001)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from WLS-CAL-001; R1, R6 and R12 restated under WLS-DDR-001 (D1, D3, D5); assumptions updated
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish; R12 target $200, status Not met to Met
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: Constructable design (WLS-DDR-004); R12 reported against the $200 value-engineering target; R2 status names the tube collar
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: R15 and R16 notes record Amish's decisions of 2026-10-02 (WLS-DEC-001); no status changed
- version: "0.8"
  date: '2026-10-02'
  author: Amish Chadha
  change: Locks modelled and priced (BOM line 16); R16 now Met on design review; R12 restated at $262.40; R11 estimate 125 min
- version: "0.9"
  date: '2026-10-25'
  author: Amish Chadha
  change: Kit 1.8 migration from WLS-REQ-001 to WLS-PRS-001; each R becomes a PR with the same target and its old number in "Was", traced to WLS-URS-001; PR-017 (maintenance interval) and PR-018 (extra-low voltage) added; fixes D-S1 and D-S2 under the fix rule reflected in PR-002 and PR-010; cost restated at $263.90
---

# WellSense product requirements and specifications

What the design must do, each traced to a user need in WLS-URS-001. This document replaces WLS-REQ-001 (kit 1.8, STANDARDS section 22): requirement R1 to R16 became PR-001 to PR-016 with the same targets and the old number in the "Was" column; no target was changed. Two requirements were added, PR-017 (maintenance interval, from UR-014) and PR-018 (extra-low voltage, from UR-015), both already met by the design. Targets remain proposals for review with a co-design partner. Status is checked against the constructable design of WLS-DDR-004 by WLS-CAL-001 v0.6 and the STEM check WLS-STM-001.

On paper, 10 requirements are met (on paper or by design), 3 are at risk (PR-004 accuracy, PR-010 compatibility with the existing pump, PR-015 environment), 1 is not met (PR-009 water safety, for want of certificates), 3 can only be verified at TRL 4 (PR-005, PR-011, PR-013), and PR-012 is $64.40 over its value-engineering target.

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001, UR-002 | Performance | Measurement range | The transducer shall measure the water above it over the full range (WLS-DDR-001, D3), with a 0 to 20 m variant | 0 to 10 | min | m of water | Analysis (WLS-CAL-001 [A1], [A3]) and datasheet, TRL 3 | Met on paper: 98.07 kPa full scale; swings to 9 m fit with 1 m headroom | R1 |
| PR-002 | UR-002 | Physical architecture | Installation depth | The probe shall hang at any depth to the target below the wellhead, with the cable and tube carried safely | 60 | min | m | Analysis (WLS-CAL-001 [D3], [D4], [D5], [D8]; WLS-STM-001 S11, S13, S14), TRL 3 | Met on paper: cable factor 11.5 and tube stress 0.82 MPa at 60 m; the collar carries the tube on the seal plate (0.24 MPa) and a clevis pin above it holds the string if the collar's grip creeps (WLS-DEC-001 D-S1) | R2 |
| PR-003 | UR-001 | Performance | Resolution | The reading shall resolve a level change of the target or better | 1 | max | mm | Analysis (WLS-CAL-001 [A2]), TRL 3 | Met on paper: 0.52 mm (1.04 mm on the 20 m variant) | R3 |
| PR-004 | UR-001 | Performance | Accuracy after field calibration | After calibration (offset against a manual tape at installation, span from the probe's per-unit factory certificate; WLS-DEC-001 D-S3), the level shall be within the target over the range | 20 | ± | mm | Analysis (WLS-CAL-001 [C4], [C4b]), TRL 3; side-by-side with a manual tape at TRL 4 | At risk: 16.0 mm root sum square, 37.1 mm worst case, with a 0.25 % class probe (span from a 1 m lift would be about 148 mm at 10 m, so it is not used); a 0.5 % class probe does not meet it (WLS-STM-001 S7 open) | R4 |
| PR-005 | UR-001, UR-014 | Performance | Long-term drift | Drift shall not exceed the target, checked by a manual reading each quarter | 20 | max | mm per year | Field record, TRL 4 | To verify at TRL 4: drift of low-cost transducers is not published; a quarterly check leaves at most 5 mm uncorrected (WLS-STM-001 S10 open) | R5 |
| PR-006 | UR-003 | Software | Reading interval | Readings shall be taken every 15 min by default and every 1 min during a pumping test, logged and sent in batches: every 30 min on a public network, every 15 min on a private TwinKit gateway (DDR-001, D5; DDR-002) | 15 (1 in tests) | max | min | Analysis (WLS-CAL-001 [E3], [E4]) and firmware configuration, TRL 3 | Met by design: 30 min batches use 22.7 s a day at SF9, within 30 s fair use | R6 |
| PR-007 | UR-004 | Software | Local storage | The logger shall store at least the target of 15 min readings without a link | 1 | min | year | Analysis (WLS-CAL-001 [E1]), TRL 3 | Met on paper: 1.12 MB a year, 6.7 % of FieldNode flash | R7 |
| PR-008 | UR-005 | Electrical | Energy | The probe and interface shall use no more than the target share of the FieldNode sensor allowance (100 mW) at 15 min | 5 | max | % | Analysis (WLS-CAL-001 [B2], [B3]), TRL 3 | Met on paper: 38.2 mWh a day, 1.6 % of the allowance | R8 |
| PR-009 | UR-006 | Materials | Water safety | All wetted parts shall be 316 stainless steel or materials certified for drinking water contact, and the well shall be sealed against surface water | Certified (NSF/ANSI/CAN 61 or equal) | none | pass or fail | Inspection of material certificates, at purchase | Not met on evidence: no certificate in hand for the low-cost cable, seals or probe; the material classes can be certified (WLS-STM-001 S24) | R9 |
| PR-010 | UR-007 | Physical architecture | Compatibility with the existing pump | The probe shall be 22 mm or less and run in its own 1 in access tube (DDR-002), with no contact with the pump, riser or pump cable | 22 | max | mm (probe diameter) | Design review (WLS-CAL-001 [D1], [D9]), TRL 3; installation trial, TRL 4 | At risk: 2.3 mm radial clearance at the nominal bore and 1.24 mm at a cement bead in the thickest pipe, so joints are wiped and a 23 mm drift is pulled through before the probe goes in (WLS-DEC-001 D-S2); fitting a tube may still need the pump pulled | R10 |
| PR-011 | UR-008 | Usability | Installation | Two trained people with hand tools shall install the logger within the target where an access tube already exists | 120 | max | min | Installation trial, TRL 4 | To verify at TRL 4: 125 min estimate with the locks fitted (WLS-CAL-001 [G1]), 5 min over | R11 |
| PR-012 | UR-009 | Cost | Cost | WellSense parts at a 30 m probe depth shall cost no more than the value-engineering target (`budget_usd`, a hypothetical control target), plus $1.80 per metre beyond; the FieldNode core is costed in the FieldNode repo (DDR-001, D1) | 200 | max | USD | Priced BOM (WLS-CAL-001 [H2]), TRL 3 | Over target: $264.40 at 30 m for the constructable design with its locks and the clevis pin, $64.40 over; $403.40 with the FieldNode core | R12 |
| PR-013 | UR-010 | Software | Data use | The dashboard shall show level below ground, daily drawdown and the change against the same month last year on a basic phone, with CSV export | 3 views and CSV | none | pass or fail | Demonstration with sample data, TRL 4 | To verify at TRL 4: software not started | R13 |
| PR-014 | UR-011 | Software | Data ownership and privacy | Records shall hold water level, time and well ID only; the hosting community controls sharing | Levels only | none | pass or fail | Design review, TRL 3 | Met by design | R14 |
| PR-015 | UR-012 | Packaging and transport | Environment | The probe shall be IP68 at 1.5 times its range and the above-ground parts IP65 over the temperature range, with FieldNode's sun shield at hot sites (DDR-002) | -10 to 55 | range | °C | Datasheets (WLS-STM-001 S21), TRL 3; field test later | At risk: met on datasheets for WellSense parts; the junction box runs about 66 °C inside at 55 °C in sun by a first-order balance, but measured enclosures run 20 to 35 K above ambient, near the modules' 85 °C (STM S21 open); the FieldNode core is rated to 45 °C ambient, not 55 °C, so sites above 45 °C are not used until FieldNode confirms (WLS-DEC-001) | R15 |
| PR-016 | UR-013 | Safety | Tamper resistance | Wellhead parts shall be lockable and no cable exposed at reachable height | Lockable, no exposed cable | none | pass or fail | Design review, TRL 3 | Met by design: cable in galvanized conduit and a short flexible tail; security-head screw on the rim band, padlock on the cap's eye bolt and a hasp and padlock on the box (BOM line 16); the padlock does not stop the cap being lifted, which the steel cover does at exposed sites | R16 |
| PR-017 | UR-014 | Usability | Maintenance interval | The logger shall need no service between quarterly visits: the desiccant shall last at least the target | 91 | min | days | Analysis (WLS-STM-001 S20; WLS-CAL-001 [F1]), TRL 3 | Met on paper: 10 g of gel lasts about 552 days at worst-case daily breathing; permeation through gaskets and glands is not counted | |
| PR-018 | UR-015 | Electrical | Extra-low voltage | Every WellSense circuit shall run at the target or less, and a short of the cable shall not damage the interface | 24 | max | V DC | Design review (WLS-STM-001 S27, S28), TRL 3 | Met by design: 24 V boost output is the highest voltage, within extra-low voltage; a 50 mA resettable fuse protects the shunt (WLS-DEC-001 D-S4) | |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- The full list of assumptions is in WLS-CAL-001, Table 1. The main ones follow.
- Water density 1,000 kg/m³ nominal; 1 m of water is 9.81 kPa. Density changes by 0.29 % between 4 and 25 °C, so firmware uses a fixed site density set from the groundwater temperature at installation, and local gravity rather than standard gravity.
- A vented (gauge) transducer (DDR-001, D2), so the reading is already referenced to air pressure. The barometric sensor records the aquifer's response to air pressure and detects a blocked vent.
- Accuracy after field calibration: the tape reading at installation fixes the offset; span is taken from the probe's per-unit factory certificate (0.10 % of reading, typical, to confirm) and refined by tape checks at levels 3 m or more apart; the 1 m lift is kept as a response check (WLS-DEC-001 D-S3). Nonlinearity, hysteresis and repeatability of a 0.25 % class probe taken as 0.10 % of full scale (typical, not measured).
- Loop powered at 24 V from a boost on the interface board, fed by FieldNode's switched 12 V rail at 90 % efficiency; 22 mA for 2 s per reading.
- Design case: 150 mm casing, 4 in pump on a 1-1/4 in riser, probe 30 m below the top of the casing.
- 1 in Sch 40 PVC pipe bore from ASTM D1785 tolerances (typical tabulated values, to confirm): 26.6 mm at the minimum wall, 25.5 mm at the thickest wall and the low outside diameter.
