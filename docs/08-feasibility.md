---
doc_id: WLS-FEA-001
title: WellSense feasibility assessment
project: WellSense
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First issue (kit 1.9.1 upgrade), for the current design (option A)
---

# WellSense feasibility assessment

WellSense (option A, the current design) is feasible on paper: the physics is standard groundwater practice, every part is bought or made with hand tools, and the energy and data budgets have wide margins; the open points are evidence, not principle (drinking-water certificates, a low-cost probe's real accuracy and drift, and fitting a tube beside an installed pump), and the cost is USD 64.40 over its value-engineering target. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Hydrostatic level measurement with a vented transducer, the USGS method; every claim within known science after four detail fixes (D-S1 clevis pin, D-S2 drift test, D-S3 span from the probe's certificate, D-S4 loop fuse) | High | Calibrated accuracy 16.0 mm RSS but 37.1 mm worst case against ±20 mm (PR-004 at risk); drift unknown (PR-005) | WLS-STM-001 (S1 to S28), WLS-CAL-001 [A] to [D] |
| Materials | 316 stainless, PVC, drinking-water HDPE, EPDM, aluminium, galvanized steel, polycarbonate; all common | Medium | No drinking-water certificates in hand for the low-cost probe, cable, HDPE and EPDM (PR-009 not met); PVC creep under the collar handled by the pin (D-S1) | WLS-STM-001 S14, S24; WLS-REG-001 G1 |
| Manufacturing and assembly | Hand tools only: drilling, sawing, tapping; the seal plate is cut from one HDPE disc; 18 assembly steps for two people | High | Installation estimate 125 min against 120 (PR-011); cement beads in tube joints (D-S2 drift test); fitting the tube past an installed pump untested (PR-010) | WLS-BLD-001, WLS-CAL-001 [G1], [D9] |
| Power and controls | 24 V boost from FieldNode's switched 12 V rail; 38.2 mWh a day, 1.6 % of the allowance; firmware is a FieldNode sensor driver plus conversion | High | Rail current limit and boost start-up on FieldNode to confirm (FieldNode repo); FieldNode core rated 45 °C ambient against 55 °C (PR-015) | WLS-CAL-001 [B1] to [B5], STM S4 to S6 |
| Supply of parts | Plumbing, electrical and online suppliers; vented 4 to 20 mA transducers are sold widely; 22 mm bodies are narrower than the common class | Medium | Price of a 22 mm, 0.25 % class probe assumed, not quoted; drinking-water certified versions may cost more | BOM lines 1 to 16, bom-notes.md, WLS-MKT-001 |
| Data and software | Storage 1.12 MB a year; airtime 22.7 s a day in pumping tests on a public network | Medium | Dashboard not started (PR-013); data ownership rules to agree with the partner | WLS-CAL-001 [E1] to [E4] |
| Cost | USD 264.40 for the WellSense parts at 30 m against the USD 200 target; USD 403.40 with the FieldNode core | Medium | Cheaper than the commercial benchmarks in WLS-MKT-001 even with the core, but over the target; option C (acoustic) would be about USD 205 if proven (WLS-OPT-001) | WLS-CAL-001 [H2], [H3] |

Ratings: High, Medium, Low.
