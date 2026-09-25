---
doc_id: WLS-REQ-001
title: WellSense requirements
project: WellSense
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# WellSense requirements

These are first-pass requirements for the concept. Targets are proposals for review, to be revised after co-design and checked by calculation at TRL 3. The status column states whether the concept in WLS-PRC-001 meets each target on first-order estimates.

Table 1. Requirements and status at TRL 2.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Measurement range (water above the probe) | 0 to 10 m, with a 0 to 20 m option | Datasheet | Met by the proposed transducer |
| R2 | Installation depth below the wellhead | Probe to 60 m or more | Cable and tube length; hanger load | Met by design (cable sized per well) |
| R3 | Resolution | 1 mm or better | ADC and shunt calculation | Met: about 0.5 mm (estimate) |
| R4 | Accuracy after field calibration against a manual tape | ±20 mm over the range | Calculation, then side-by-side with a manual tape | **Not met on datasheet:** about ±50 mm at 0.5 % of full scale; may be met with a 0.25 % sensor or two-point field calibration, unverified |
| R5 | Long-term drift | 20 mm a year or less, checked by a manual reading each quarter | Field record | **Unverified, at risk:** drift of low-cost transducers is not published |
| R6 | Reading interval | 15 min default; 1 min during a pumping test | Firmware configuration | Met by design |
| R7 | Local storage | 1 year of 15 min readings without a link | Storage calculation | Met: about 0.3 MB a year against FieldNode flash (estimate) |
| R8 | Energy | Probe and interface use 5 % or less of the FieldNode sensor energy budget at 15 min | Power budget | Met: about 18 mWh a day, about 0.6 % (estimate) |
| R9 | Water safety | All wetted parts 316 stainless steel or materials certified for drinking water contact; well sealed against surface water | Material certificates | **Not met on evidence:** cable jacket and sensor seal certification for low-cost transducers unknown |
| R10 | Compatibility with the existing pump | Probe in its own access tube; no contact with pump, riser or pump cable | Design review, installation trial | **At risk:** fitting a tube may need the pump pulled; no room in narrow casings |
| R11 | Installation | Two trained people, hand tools, 2 h or less when an access tube already exists | Installation trial | Unverified |
| R12 | Cost | WellSense parts $180 or less per well (FieldNode core counted separately) | Priced BOM | Met: about $170; **not met** if FieldNode is included (about $296) |
| R13 | Data use | Dashboard shows level below ground, daily drawdown and change against the same month last year on a basic phone; CSV export | Demonstration with sample data | Unverified (software not started) |
| R14 | Data ownership and privacy | Water level, time and well ID only; the hosting community controls sharing | Design review | Met by design |
| R15 | Environment | Probe IP68 at 1.5 times range; above-ground parts IP65, -10 to 55 °C | Datasheets, later field test | Met on datasheets; unverified in the field |
| R16 | Tamper resistance | Wellhead parts lockable; no exposed cable at reachable height | Design review | **At risk:** cable run from the wellhead to the post is exposed in the concept |

## Assumptions

- Water density 1,000 kg/m³; 1 m of water is 9.81 kPa. Temperature changes density by about 0.3 % between 4 and 25 °C, which firmware corrects using the probe temperature where available.
- A vented (gauge) transducer is assumed, so the reading is already referenced to air pressure. The barometric sensor is kept to record the aquifer's response to air pressure and to detect a blocked vent.
- Accuracy stated as a percentage of full scale applies over the whole 10 m range; ±0.5 % of 10 m is ±50 mm.
- Sensor supply 12 V, current up to about 22 mA, powered for about 2 s per reading, from FieldNode's switched 12 V rail at about 80 % boost efficiency.
