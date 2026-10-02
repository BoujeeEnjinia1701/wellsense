---
doc_id: WLS-DEC-001
title: WellSense design decisions register
project: WellSense
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-02'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
---

# WellSense design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Review the design-for-construction changes P1 to P11 (split seal plate, collar, drilled tube, tube cap with cross bolt and grip, flexible tail, bent conduit on saddles, junction box plate with V-blocks, box entries and internal plate, barometric housing, FieldNode lead, post cap) | Accept as made; or ask for changes | Accept | The whole build plan | WLS-DDR-004, made under Amish's 2026-09-30 instruction; open for his review |
| 2 | Locking of the wellhead and junction box (R16) | (a) security-head screw on the rim band, padlock through the cross bolt's head, padlockable hasp kit on the box; (b) lockable steel cover over the wellhead | (a), decided after the first site visit | Seal plate, tube cap, junction box | WLS-DDR-004, A1; WLS-PRC-001 open questions |
| 3 | First partner and region for co-design | An Indian farmer group, an African handpump programme or a US groundwater agency | None yet | Design well (casing, riser and pump cable sizes); LoRaWAN band of the FieldNode core | WLS-DDR-001, O1 |
| 4 | Battery-only FieldNode variant without the panel | Keep the standard core; or a battery-only core | None (for the FieldNode project) | FieldNode core | WLS-DDR-001, O2 |
| 5 | FieldNode sensor port pin assignment | Pinout of port A agreed with the FieldNode project; WellSense assumes 12 V rail, ground and I2C | None yet (FieldNode decision) | FieldNode lead wiring (build plan section 3.5.1) | FND-DDR-001, O2 |
| 6 | FieldNode core above 45 °C ambient (R15 asks for 55 °C) | FieldNode confirms the shielded core at 55 °C; or R15 restated to FieldNode's range | None yet (FieldNode decision) | FieldNode sun shield at hot sites | REVIEW.md, cross-repo actions |
| 7 | How the FieldNode geometry in `cad/vendor/` is kept up to date | (a) re-export it whenever FieldNode's general arrangement is revised; (b) a shared library repo | (a) | Model, drawings and pictures of the FieldNode core | WLS-DDR-004, A2 |
| 8 | Photoreal render layout: post drawn 330 mm from the well and 350 mm lower than installed | Accept for renders only; or render the installed layout | Accept for renders only | Renders only; not the build | REVIEW.md, 2026-09-26, render item 1 |
| 9 | Render grouping of the post, tube and cable for the exploded render | Accept; or group as the BOM | Accept | Renders only | REVIEW.md, 2026-09-26, render item 5 |

Render items 3 (conduit route at the tube cap) and 4 (seal plate gasket) of the 2026-09-26 review are overtaken by WLS-DDR-004: the conduit now ends in a flexible tail and the gasket is a separate ring under the plate. The renders need redoing on Amish's Mac in any case.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Drinking-water certificates for the probe, the vented cable, the HDPE sheet and the EPDM (gasket and wraps) | R9 is not met without them | WLS-REQ-001, R9; WLS-DDR-004 |
| 2 | The riser and pump cable diameters at the well | They set the seal plate's split holes (designed for a 42.2 mm riser and a 12 mm cable) | WLS-DDR-004, P6 |
| 3 | The junction box model, its boss spacing (80 x 110 mm assumed) and its lug kit | They set the internal plate holes and the lug holes in the plate | WLS-DDR-004, P3 |
| 4 | The shaft collar's rated axial grip on PVC pipe, at least 264 N | It carries the tube at 60 m | WLS-CAL-001, [D5] |
| 5 | The cable support grip suits 6 to 8 mm cable and carries at least 35 N | It carries the probe and cable at 60 m | WLS-CAL-001, [D6] |
| 6 | The probe body is 22 mm or less, and its supplier's price | 2.3 mm radial clearance in the tube; the BOM assumes the 26 to 28 mm class price | WLS-DDR-002; BOM line 1 |
| 7 | The flexible tail's connector fits a 22.5 mm hole in a 1 in PVC cap, with its locknut inside | The cap is the connector's only support | WLS-DDR-004, P5 and P8 |

## Value engineering

Value-engineering target: USD 200 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 244.40 for the WellSense parts at the 30 m design depth (USD 44.40 over the target); USD 383.40 with the FieldNode core, which is costed in the FieldNode repo. Main cost drivers and savings worth trying:

- The largest lines are the transducer (USD 50), the access tube (USD 31 at 30 m), the post with its plate, V-blocks and bands (USD 32), the vented cable (USD 26.40 at 30 m), the seal plate set (USD 23) and the conduit set (USD 20). Cable and tube scale with depth at USD 1.80 a metre.
- Making the design constructable added USD 46.80: the seal plate set (+8), tube cap and grip (+4), junction box lugs, glands and internal plate (+6), terminal strip (+1), junction box plate and V-blocks (+10), flexible tail, saddles and hub (+10), the FieldNode lead (+7) and 1 m more cable (+0.80).
- Savings worth trying: fit the conduit set only where livestock or tampering is likely (USD 20); leave the access tube out where no pump shares the casing (USD 31 at 30 m, already the rule); mount the barometric module inside the junction box, which breathes through its desiccant, instead of in its own housing (about USD 4); buy the junction box with a pole-mount kit if one is offered at less than the plate, V-blocks and bands (up to USD 10); cut the seal plate from offcuts shared across several wells.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 items D1 to D8: FieldNode core costed in its own repo; vented 4 to 20 mA transducer; 0 to 10 m range; own access tube where a pump shares the casing; 15 min readings, 1 min in pumping tests; quarterly manual tape check; levels only, community controls sharing; FieldNode as the core | Amish: "i accept all your recommendations, go with them across all repos." | WLS-DDR-001, WLS-DDR-002 |
| 2026-09-25 | TRL 3 items A9 to A13: design depth 30 m; 1 in tube with a probe of 22 mm or less; galvanized conduit over the surface cable; FieldNode sun shield at hot sites; pumping tests send every 30 min on a public network | Amish, same instruction | WLS-DDR-002 |
| 2026-09-26 | `budget_usd` set to $200 | Amish: "i approve all the budget items." | WLS-DDR-002, N1 |
| 2026-09-27 | FieldNode panel tilt corrected to face the way the node faces | Amish: "resolve the challenges for ConePro, BridgePulse, Grainguard and WellSense." | WLS-DDR-003 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." Changes made under this instruction; open for his review (open decision 1) | WLS-DDR-004 |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | STANDARDS section 18; this register |
