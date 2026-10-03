---
doc_id: WLS-DDR-001
title: WellSense TRL 2 review decisions
project: WellSense
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review recommendations adopted for TRL 3 work under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: O1 and O2 recorded as decided by Amish on 2026-10-02
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for D1 to D8. On 2026-09-25 Amish accepted all recommendations, so items D1 to D8 are "Decided by Amish, 2026-09-25: go with recommendation" (see WLS-DDR-002). Items O1 and O2 carried no recommendation on 2026-09-25; Amish decided both on 2026-10-02 (WLS-DEC-001).

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", and the design precis WLS-PRC-001 v0.2 listed five key design choices, all marked proposed. On 2026-09-25 Amish asked for this batch of Design Molecule repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carried a recommendation is therefore adopted as recommended for TRL 3 work, open for his review. Items without a recommendation stay open. At v0.1 nothing here was recorded as decided by Amish; he accepted the recommendations later the same day (WLS-DDR-002).

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in WLS-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items decided (adopted for TRL 3 work, then accepted by Amish on 2026-09-25).*

| # | Item | Adopted recommendation | Status |
| --- | --- | --- | --- |
| D1 | Budget treatment of FieldNode (review item 1) | Option (a): the FieldNode core is costed in the FieldNode repo, and `budget_usd` covers the WellSense parts only; the complete logger cost is stated alongside. The figure itself was raised from $180 to $190 under WLS-DDR-002. | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Sensor type (review item 2; precis choice 1) | Option A: vented (gauge) 4 to 20 mA transducer for the first build; option B, a sealed absolute sensor with RS-485 and surface barometric compensation, kept as a variant | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Range (review item 3) | 0 to 10 m of water; 0 to 20 m kept as a variant for wells with large pumping drawdown | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Access tube (review item 4; precis choice 2) | Own access tube wherever a pump or riser shares the casing; probe hung freely where there is no pump | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | Default interval (review item 5) | 15 min, with 1 min during pumping tests | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | Manual tape check (review item 6; precis choice 4) | Tape datum at installation and a tape check each quarter as part of the method, with one shared tape per community or partner | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | Data ownership (review item 7; precis choice 5) | Levels, time and well ID only; the hosting community controls sharing; CSV export | Decided by Amish, 2026-09-25: go with recommendation |
| D8 | FieldNode as the core (precis choice 3) | Reuse the lab's shared FieldNode core for enclosure, power, radio and storage; WellSense designs only the well side and the interface | Decided by Amish, 2026-09-25: go with recommendation |

No rewording of the pitch or problem line was recommended at TRL 2, so both stay as they are in `project.yaml` and `README.md`.

*Table 2. Items left open on 2026-09-25, decided by Amish on 2026-10-02 (WLS-DEC-001).*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner and region for co-design (an Indian farmer group, an African handpump programme or a US groundwater agency). No preference stated and no recommendation made on 2026-09-25. | Decided by Amish, 2026-10-02: a participatory groundwater management group in India that works with farmer groups on shared aquifers; the first candidate to approach is ACWADAM in Pune, with its well sizes setting the design well and the FieldNode core at its sites on the IN865 band |
| O2 | Battery-only FieldNode variant without the panel (review item 9). Raised for discussion with the FieldNode project, with no recommendation to adopt; the baseline keeps the standard FieldNode core. | Decided by Amish, 2026-10-02: the standard FieldNode core with its panel is kept; no battery-only variant is asked of FieldNode until a site shows the panel cannot be placed |

## Consequences

- `project.yaml`: only the TRL fields and the evidence list change. `budget_usd` stays at $180, and the pitch and problem are unchanged.
- WLS-PRB-001, WLS-PRC-001 and WLS-REQ-001 are revised to v0.3. The design choices in the precis are no longer described as "proposed"; they are adopted for TRL 3 work pending Amish's review.
- Requirement R12 is restated under D1 as the WellSense parts per well at the 30 m design case, with the FieldNode core costed in the FieldNode repo (FND-CAL-001, $126.00). R1 names the 0 to 10 m range (D3) with the 0 to 20 m variant, and R6 states that 1 min readings are logged and sent in batches (D5). No other target changes.
- The TRL 3 calculations (WLS-CAL-001) made detail choices within D2 that Amish should see: the FieldNode 12 V rail cannot drive the current loop through a 150 Ω shunt to the transducer's 12 V minimum, so the interface board gains a 12 to 24 V boost and a 3.3 V regulator; the transducer is specified in the 0.25 % class, since the 0.5 % class cannot reach R4 even after calibration; and calibration is two-point, by lifting the probe a measured 1 m in its tube. Within D8, the post is lengthened so the FieldNode core sits at its 1.75 m mounting height (FND-DDR-001, D11), and a footing concrete line is added to the BOM.
- The calculations also raise new items that need Amish's decision (cost over $180 at 30 m, access tube bore, surface cable protection, hot-site temperature rating, pumping-test airtime). They are listed in `docs/REVIEW.md` as proposed and are not decided by this record.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
