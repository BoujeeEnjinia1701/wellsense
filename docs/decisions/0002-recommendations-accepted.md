---
doc_id: WLS-DDR-002
title: WellSense recommendations accepted
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
  change: Record Amish's acceptance of all recommendations (2026-09-25), what changed in the repo, and the items still open
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: "Budget set to $200 to cover the priced BOM: decided by Amish, 2026-09-26 (N1 closed)"
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: O1 and O2 recorded as decided by Amish on 2026-10-02
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below is "Decided by Amish, 2026-09-25: go with recommendation". Items without a recommendation were decided later: N1 (cost with the conduit) by Amish on 2026-09-26, and O1 and O2 by Amish on 2026-10-02 (WLS-DEC-001).

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." This record lists every WellSense item that carried a recommendation in `docs/REVIEW.md` (TRL 2 and TRL 3 sessions) and in WLS-DDR-001, and what changed in the repo because of it. Where a recommendation offered several options, the recommended option is the decision. Work that belongs to TRL 4 is recorded as decided but on hold, since TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (sessions 2026-09-25, /populate and TRL 3) and in WLS-DDR-001.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| A1 | D1, budget treatment of FieldNode (TRL 2 item 1) | Option (a): `budget_usd` covers WellSense parts only; FieldNode core costed in its own repo | Status wording in WLS-DDR-001, WLS-PRC-001 and REVIEW.md; no design change |
| A2 | D2, sensor type (TRL 2 item 2) | Vented 4 to 20 mA transducer; absolute RS-485 sensor kept as a variant | Status wording only; the TRL 3 detail choices (24 V boost, 0.25 % class, two-point calibration) stand |
| A3 | D3, range (TRL 2 item 3) | 0 to 10 m, 0 to 20 m variant | Status wording only |
| A4 | D4, access tube (TRL 2 item 4) | Own tube wherever a pump shares the casing | Status wording only |
| A5 | D5, default interval (TRL 2 item 5) | 15 min, 1 min in pumping tests | Status wording only |
| A6 | D6, manual tape check (TRL 2 item 6) | Quarterly tape check with one shared tape | Status wording only |
| A7 | D7, data ownership (TRL 2 item 7) | Levels only, community controls sharing, CSV export | Status wording only |
| A8 | D8, FieldNode as the core | Reuse FieldNode for enclosure, power, radio and storage | Status wording only |
| A9 | Cost at the design depth (TRL 3 item 3) | Option (b): raise `budget_usd` to $190 for a 30 m design well, $1.80 per metre beyond | `project.yaml` `budget_usd` $180 to $190; R12 restated in WLS-REQ-001 v0.4; README, precis and CAL updated |
| A10 | Access tube bore (TRL 3 item 4) | Option (a): keep the 1 in tube and require a probe of 22 mm or less | `cad/src/model.py` probe 24 mm to 22 mm (radial clearance 1.3 mm to 2.3 mm); BOM line 1 respecified; R10 restated; STEP, STL, WLS-DWG-001 (Rev P2) and media regenerated |
| A11 | Surface cable protection (TRL 3 item 5) | Option (a): galvanized conduit from the seal plate to the junction box, about $10 (estimate) | BOM line 14 added ($10.00); conduit modeled (`conduit` part); drawing note and callout; parts cost $187.60 to $197.60 |
| A12 | Hot-site rating (TRL 3 item 6) | Option (a): keep R15 at 55 °C and require FieldNode's sun shield at hot sites | R15 text in WLS-REQ-001 v0.4; precis; complete hot-site cost $331.60 with FieldNode's $8.00 shield (FND-DDR-002). FieldNode itself not edited |
| A13 | Pumping-test uplinks (TRL 3 item 7) | On a public network send every 30 min during a test; use a TwinKit gateway where possible | R6 text; CAL-001 v0.2 [E4]: 30-reading batch every 30 min, 22.7 s a day at SF9, within 30 s fair use. Firmware is TRL 4 work and is on hold |

No rewording of the pitch or problem line was recommended, so both are unchanged.

*Table 2. Items open on 2026-09-25 (no recommendation); O1 and O2 decided by Amish on 2026-10-02 (WLS-DEC-001).*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner and region for co-design (WLS-DDR-001, O1). No preference stated. | Decided 2026-10-02: ACWADAM in Pune, India, as the first candidate to approach |
| O2 | Battery-only FieldNode variant (WLS-DDR-001, O2). No recommendation to adopt. | Decided 2026-10-02: keep the standard core with its panel |
| N1 | New: cost with the conduit. A9 and A11 together give $197.60 at 30 m against $190. Options: (a) raise `budget_usd` to $200; (b) keep $190 and state R12 at a 25 m design depth; (c) keep $190 and fit the conduit only where livestock or tampering is likely. | Decided by Amish, 2026-09-26: budget set to $200 (see below) |

### Budget approved, 2026-09-26

On 2026-09-26 Amish wrote: "i approve all the budget items."

- Budget set to $200 to cover the priced BOM: decided by Amish, 2026-09-26. This closes N1. `project.yaml` `budget_usd` 190 to 200; WLS-REQ-001 R12 target $200, status Not met to Met (budget holds to a 31.3 m probe depth, was 25.8 m); WLS-CAL-001 v0.3 (`sizing.py` and `results.csv` rerun); WLS-PRB-001, WLS-PRC-001, README, `bom/bom-notes.md` and the blueprint key figures updated. The BOM and geometry are unchanged.

## Consequences

- `project.yaml`: `budget_usd` $190. `trl: 3` and `trl_target: 3` unchanged.
- Documents revised: WLS-PRB-001 v0.4, WLS-PRC-001 v0.4, WLS-REQ-001 v0.4, WLS-CAL-001 v0.2, WLS-DDR-001 v0.2; drawing WLS-DWG-001 Rev P2.
- Requirement status: 2 not met (R9 water safety, R12 cost at $197.60 against $190), 4 at risk (R4, R10, R15, R16), 3 not verifiable at TRL 3 (R5, R11, R13), 7 met.
- After the 2026-09-26 budget approval (WLS-CAL-001 v0.3): 1 not met (R9), 4 at risk, 3 not verifiable at TRL 3, 8 met.
- Cross-repo action (FieldNode, not edited here): confirm the shielded core's behaviour at 55 °C ambient, since WellSense R15 asks for 55 °C and FieldNode is rated to 45 °C ambient.
- TRL 4 remains on hold by Amish's instruction. The firmware uplink rule, the interface board build, supplier certificates and any purchasing are decided in principle but not started.
