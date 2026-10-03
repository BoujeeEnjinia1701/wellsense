---
doc_id: WLS-DEC-001
title: WellSense design decisions register
project: WellSense
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-02'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: Amish approved the recommendations for open items 1 to 9 on 2026-10-02 (WLS-DDR-004 accepted with A1 and A2, ACWADAM as first candidate partner, standard FieldNode core and pinout, R15 kept with hot sites held, render items); moved to decisions made
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: Locks modelled and priced (BOM line 16); value-engineering cost restated at USD 262.40
---

# WellSense design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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

Value-engineering target: USD 200 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 262.40 for the WellSense parts at the 30 m design depth (USD 62.40 over the target); USD 401.40 with the FieldNode core, which is costed in the FieldNode repo. Main cost drivers and savings worth trying:

- The largest lines are the transducer (USD 50), the access tube (USD 31 at 30 m), the post with its plate, V-blocks and bands (USD 32), the vented cable (USD 26.40 at 30 m), the seal plate set (USD 23) and the conduit set (USD 20). Cable and tube scale with depth at USD 1.80 a metre.
- Making the design constructable added USD 46.80: the seal plate set (+8), tube cap and grip (+4), junction box lugs, glands and internal plate (+6), terminal strip (+1), junction box plate and V-blocks (+10), flexible tail, saddles and hub (+10), the FieldNode lead (+7) and 1 m more cable (+0.80).
- The locks decided on 2026-10-02 added USD 18.00: line 16 (security-head screw and bit USD 3.50, two padlocks USD 9.00, hasp kit USD 4.00) and USD 1.50 for the eye bolt in line 5. The lockable steel wellhead cover is priced only when a site visit calls for it.
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
| 2026-10-02 | Design for construction accepted: the changes P1 to P11 of WLS-DDR-004, as made | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WLS-DDR-004 |
| 2026-10-02 | Locking (R16): option (a) is fitted on the prototype from the start: a security-head screw on the rim band, a padlock through the cross bolt's head and a padlockable hasp kit on the junction box; the lockable steel wellhead cover is used at sites where the first site visit shows open access or livestock | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WLS-DDR-004, A1; WLS-PRC-001 open questions |
| 2026-10-02 | First partner and region: a participatory groundwater management group in India that works with farmer groups on shared aquifers; the first candidate to approach is ACWADAM in Pune, with its well sizes setting the design well and the FieldNode core at its sites on the IN865 band | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WLS-DDR-001, O1 |
| 2026-10-02 | Battery-only FieldNode variant: the standard FieldNode core with its panel is kept; no battery-only variant is asked of FieldNode until a site shows the panel cannot be placed | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WLS-DDR-001, O2 |
| 2026-10-02 | FieldNode sensor port pinout: FieldNode's proposed standard pinout is signed off for port A (pin 1 switched rail, pin 2 data A, pin 3 ground, pin 4 data B, pin 5 analog), with data A and B carrying I2C; the switched rail voltage is confirmed against the boost module input | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | FND-DDR-001, O2; FND-DEC-001 |
| 2026-10-02 | FieldNode core above 45 °C: R15 stays at 55 °C, as decided on 2026-09-25 (WLS-DDR-002, A12); the FieldNode project is asked to confirm the shielded core at 55 °C ambient, and until it does WellSense is not sited where the design maximum exceeds 45 °C | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | REVIEW.md, cross-repo actions; WLS-DDR-002, A12 |
| 2026-10-02 | FieldNode geometry in `cad/vendor/`: kept as a copy and re-exported whenever FieldNode's general arrangement is revised, as a line in the review checklist | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | WLS-DDR-004, A2 |
| 2026-10-02 | Photoreal render layout: the post drawn closer to the well and lower than installed is accepted, for renders only | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | REVIEW.md, 2026-09-26, render item 1 |
| 2026-10-02 | Exploded render: grouping the post, tube and cable together is accepted | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | REVIEW.md, 2026-09-26, render item 5 |
