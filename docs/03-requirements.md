---
doc_id: WLS-REQ-001
title: WellSense requirements
project: WellSense
doc_type: Requirements
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
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
---

# WellSense requirements

These requirements are checked by calculation in WLS-CAL-001 v0.4 against the constructable design of WLS-DDR-004 and WLS-PRC-001 v0.6. Targets remain proposals, to be revised after co-design. Under WLS-DDR-001 (decided by Amish, 2026-09-25: go with recommendation), R1 names the 0 to 10 m range (D3), R6 states how 1 min readings are sent (D5), and R12 costs the WellSense parts only, with the FieldNode core costed in the FieldNode repo (D1). Under WLS-DDR-002, R12 is restated at $190 for the 30 m design well (raised to $200 by Amish on 2026-09-26 to cover the priced BOM), R10 limits the probe to 22 mm in the 1 in tube, R6 adds the 30 min uplink rule for pumping tests on public networks, and R15 requires FieldNode's sun shield at hot sites. No target was relaxed. Under the 2026-10-01 portfolio rule, `budget_usd` is a value-engineering target, a hypothetical control target rather than a limit, so R12 is reported as over or under that target. On paper, 7 requirements are met, 4 are at risk, 1 is not met (R9), 3 cannot be verified at TRL 3, and R12 is $44.40 over its value-engineering target.

Table 1. Requirements and status at TRL 3 (WLS-CAL-001 v0.4, Table 3).

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R1 | Measurement range (water above the probe) | 0 to 10 m (DDR-001, D3), with a 0 to 20 m variant | Datasheet | Met: 98.07 kPa full scale; swings to 9 m fit with 1 m headroom |
| R2 | Installation depth below the wellhead | Probe to 60 m or more | Cable and tube length; hanger load | Met: cable factor 11.5 and tube factor 58 at 60 m; a split collar carries the tube on the seal plate (0.24 MPa bearing) |
| R3 | Resolution | 1 mm or better | ADC and shunt calculation | Met: 0.52 mm (1.04 mm on the 20 m variant) |
| R4 | Accuracy after field calibration against a manual tape | ±20 mm over the range | Calculation, then side-by-side with a manual tape | **At risk:** 12.5 mm root sum square, 27.1 mm worst case, with a 0.25 % class probe and two-point calibration; a 0.5 % class probe does not meet it |
| R5 | Long-term drift | 20 mm a year or less, checked by a manual reading each quarter | Field record | Not verifiable at TRL 3: drift of low-cost transducers is not published; a quarterly check leaves at most 5 mm uncorrected |
| R6 | Reading interval | 15 min default; 1 min during a pumping test, logged and sent in batches (DDR-001, D5); on a public network a test sends every 30 min, on a private TwinKit gateway every 15 min (DDR-002) | Firmware configuration | Met by design: 30 min batches use 22.7 s a day at SF9, within 30 s fair use |
| R7 | Local storage | 1 year of 15 min readings without a link | Storage calculation | Met: 1.12 MB a year, 6.7 % of FieldNode flash |
| R8 | Energy | Probe and interface use 5 % or less of the FieldNode sensor energy budget at 15 min | Power budget | Met: 38.2 mWh a day, 1.6 % of the 100 mW allowance |
| R9 | Water safety | All wetted parts 316 stainless steel or materials certified for drinking water contact; well sealed against surface water | Material certificates | **Not met on evidence:** no certificate in hand for low-cost cable, seals or probe |
| R10 | Compatibility with the existing pump | Probe of 22 mm or less in its own 1 in access tube (DDR-002); no contact with pump, riser or pump cable | Design review, installation trial | **At risk:** tube and probe fit the 150 mm design well with 2.3 mm radial clearance, but fitting a tube may need the pump pulled |
| R11 | Installation | Two trained people, hand tools, 2 h or less when an access tube already exists | Installation trial | Not verifiable at TRL 3: 120 min estimate, at the limit |
| R12 | Cost | Value-engineering target: WellSense parts $200 per well at a 30 m probe depth (`budget_usd`, a hypothetical control target), plus $1.80 per metre beyond; FieldNode core costed in the FieldNode repo (DDR-001, D1) | Priced BOM | **Over the target:** $244.40 at 30 m for the constructable design (WLS-DDR-004), $44.40 over; $383.40 with the FieldNode core |
| R13 | Data use | Dashboard shows level below ground, daily drawdown and change against the same month last year on a basic phone; CSV export | Demonstration with sample data | Not verifiable at TRL 3 (software not started) |
| R14 | Data ownership and privacy | Water level, time and well ID only; the hosting community controls sharing | Design review | Met by design |
| R15 | Environment | Probe IP68 at 1.5 times range; above-ground parts IP65, -10 to 55 °C; FieldNode sun shield fitted at hot sites (DDR-002) | Datasheets, later field test | **At risk:** met on datasheets for WellSense parts; with its shield the FieldNode core stays at 48.5 to 52.2 °C inside at 45 °C ambient (FND-CAL-001 v0.2), but it is rated to 45 °C ambient, not 55 °C |
| R16 | Tamper resistance | Wellhead parts lockable; no exposed cable at reachable height | Design review | **At risk:** the surface cable now runs in galvanized conduit and a short flexible tail from the tube cap to the junction box (DDR-002, DDR-004), but locking of the seal plate, tube cap and box is not yet specified |

## Assumptions

- The full list of assumptions is in WLS-CAL-001, Table 1. The main ones follow.
- Water density 1,000 kg/m³ nominal; 1 m of water is 9.81 kPa. Density changes by 0.29 % between 4 and 25 °C, so firmware uses a fixed site density set from the groundwater temperature at installation, and local gravity rather than standard gravity.
- A vented (gauge) transducer (DDR-001, D2), so the reading is already referenced to air pressure. The barometric sensor records the aquifer's response to air pressure and detects a blocked vent.
- Accuracy after a two-point field calibration: the tape reading at installation and again after lifting the probe a measured 1 m. Nonlinearity, hysteresis and repeatability of a 0.25 % class probe taken as 0.10 % of full scale (typical, not measured).
- Loop powered at 24 V from a boost on the interface board, fed by FieldNode's switched 12 V rail at 90 % efficiency; 22 mA for 2 s per reading.
- Design case: 150 mm casing, 4 in pump on a 1-1/4 in riser, probe 30 m below the top of the casing.
