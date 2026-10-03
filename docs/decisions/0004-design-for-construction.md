---
doc_id: WLS-DDR-004
title: WellSense design for construction
project: WellSense
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-02'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Accepted by Amish on 2026-10-02, with A1 (locking fitted from the start) and A2 (vendor copy re-exported) decided
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: A1 carried into the design, with the locks modelled, priced and drawn; cost and document versions updated
---

# 0004: Design for construction

- **Date:** 2026-10-02
- **Status:** draft; accepted. Amish, 2026-10-02: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." This approves the recommendation written for each open decision in the design decisions register (WLS-DEC-001 v0.1): every change in Tables 1 and 2 is accepted as made, and A1 and A2 in Table 3 are decided as recorded there.

## Context

On 2026-09-30 Amish asked for every repo to have a prototype build plan that shows how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of WLS-DDR-002 and WLS-DDR-003 was a massing model: it showed what WellSense does, but several parts could not be made or fixed as drawn. Checking it with build123d found, among others, that the junction box overlapped the post by 602 mm³, the interface board sat inside a solid box (63,000 mm³ of overlap), the conduit was a solid rod round the cable (46,400 mm³ of overlap), the barometric housing floated 1 mm off the post with no fixing, and the FieldNode core floated 17.9 mm off the post with nothing holding it.

The changes keep what WellSense does: the same vented 4 to 20 mA probe hung in its own 1 in access tube, the same seal at the wellhead, the same galvanized conduit over the surface cable, the same junction box, interface board, barometric sensor and FieldNode core on a 2.1 m post 0.75 m from the well, the same 15 min readings and the same calibration method. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 99 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must not touch are apart by at least the stated clearance. All 99 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The FieldNode core was a massing block on two legs, 17.9 mm off the post with no V-blocks or bands, and its panel bracket was not FieldNode's. | The FieldNode core is now FieldNode's constructable design (FND-DDR-003), built to FND-BLD-001 and drawn from geometry exported from the FieldNode model (`cad/vendor/`). Its V-blocks sit on the WellSense post and its two bands clamp it, base 1,750 mm up. WellSense uses sensor port A. | The post is FieldNode's 48.3 mm design pole, so FieldNode fits it unchanged; one design, one build plan. |
| P2 | The junction box was drawn flat against the round post, overlapping it by 602 mm³, and "held" by two band rings round the post, one of them at 1,450 mm, above the box. A band cannot hold a flat box on a round post. | A 140 x 530 x 3 mm aluminium junction box plate, 42 mm in front of the post axis, held by two V-blocks (the same 60 x 33 x 20 mm part as FieldNode's) and two 12 mm band clamps through slots in the plate. The box sits flat on the plate on its maker's four lugs, one M5 screw each, and faces the well. | The same mounting method as FieldNode, with the same V-block, so one jig and one making sketch serve both. The plate also carries the conduit saddles and the barometric housing. |
| P3 | The junction box was a solid block with the interface board inside it, and it had no cable entries. | The box is a bought IP66 box with four moulded bosses inside its back wall. A printed internal plate on the bosses carries the boost module, the ADC and shunt module, the regulator and surge module and a terminal strip on standoffs. Four entries in the floor, in two rows 22 and 62 mm from the back face: conduit hub, M16 gland for the FieldNode lead, desiccant breather and M12 gland for the barometric lead; outside flanges at least 10 mm apart. | Entries in the floor keep water out; the internal plate lifts out as one piece; the plate clears the entry nuts by 6 mm. |
| P4 | The barometric housing floated 1 mm off the post on the side away from the well, with no fixing and no cable. | A flanged louvred housing screwed to the junction box plate below the box with two M4 screws; its 0.3 m lead enters the box through the M12 gland. | It reads air pressure anywhere near the box; a short lead and a flat fixing. |
| P5 | The conduit was drawn as a solid rod round the cable, with sharp mitred corners a rigid conduit cannot take. It was joined rigidly to the tube cap, so the cap could not come off to lift the probe for the two-point calibration, and nothing held it at the post. | A rigid 1/2 in conduit with one 90° bend of 100 mm radius runs level at 720 mm from the well to the post and up into a hub in the junction box floor; two spacer saddles hold its upright leg to the plate. A 0.3 m liquid-tight flexible tail joins its well end to a connector in the tube cap. The cable carries a 1.1 m service loop coiled in the box, so the probe can be lifted 1 m. | A hand bender makes the bend; the flexible tail lets the cap lift off after one connector is undone; the cable feeds out of the box for the lift. The cable's surface run is now 2.7 m, not 2 m. |
| P6 | The seal plate was one 200 mm disc with two gland bosses. It could not be fitted round an installed riser, which the concept requires, had nothing to locate or hold it on the casing, and had no way through for the pump's power cable. | Two half plates of 20 mm drinking-water HDPE, split on the line through the three holes; a 10 mm HDPE spigot half ring screwed under each half locates it inside the casing; a 3 mm EPDM gasket on the casing rim; one turn of 2 mm EPDM wrap round the riser, the pump cable and the tube, squeezed in the split holes; a worm-drive band round the rim pulls the halves together. | Every part is cut with a jigsaw and drilled; it goes round the riser and pump cable without pulling the pump; the band gives an even squeeze on the wraps. |
| P7 | The calculations said a tube clamp was needed to carry 264 N of tube at 60 m, but none was modelled. | A split aluminium shaft collar on the tube rests on the seal plate. Bearing on the HDPE is 0.24 MPa [D5]. | A bought part; set the tube height by sliding the collar. |
| P8 | The tube cap had a "cable-grip hanger" boss on top, but nothing carried the probe's weight, and the cap could not take the conduit. | A 1 in slip cap, not glued, drilled for the conduit connector in its top and for an M5 cross bolt through its sides. A stainless cable support grip on the cable hangs by its eye from the cross bolt. The cap sits on the tube end. Bearing on the cap walls is 0.79 MPa at 60 m [D6]. | The grip sets and holds the recorded probe depth; the cap, grip and probe lift off together for calibration. |
| P9 | The access tube's slots were 3 x 60 mm, cut lengthwise through both walls, which needs a router; its end plug was drawn as part of the tube. | Ten rings of 8 mm holes over the bottom 0.5 m, two holes drilled straight through at right angles in each ring, alternate rings turned 45°. A bought 1 in slip cap is solvent-welded on the bottom end, with an 8 mm drain hole. | A hand drill and a V-block do it; the 40 holes give about three and a half times the bore's area. |
| P10 | The lead from the junction box to the FieldNode core entered the box through its top, which lets water in, and had no plug or BOM line. | A 1.5 m four-core lead with an M12 plug, BOM line 15: through the M16 gland in the box floor with a drip loop, up the post outside the bands, cable-tied, into FieldNode sensor port A. | Every entry is in a floor; the lead clears the plate, bands and V-blocks by at least 3.5 mm. |
| P11 | The post's top was open. | A push-in plastic cap. | Keeps rain out of the pipe. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Cost | Lines 4, 5, 6, 7, 10 and 14 repriced and line 15 added. Value-engineering target: USD 200. Estimated cost of the constructable design: USD 244.40 (USD 44.40 over the target) before the locks of A1; with them USD 262.40 (USD 62.40 over the target); the concept was USD 197.60 [H2], [H2c], [H2d]. Line 8, the FieldNode core, is now FieldNode's constructable base node, $139.00 (was $126.00), outside the target. | Parts added for construction. `budget_usd` is unchanged. |
| Cable | 33 m at the 30 m design depth (was 32 m); surface run 2.7 m including the 1.1 m service loop; loop supply at 60 m still leaves 8.16 V of margin [B1]. | P5. |
| Drawing | WLS-DWG-001 Rev P6 (locks added); WLS-DWG-109 Rev P2; making sketches WLS-DWG-101 to 109 added. | Follows the model. |
| Documents | WLS-CAL-001 v0.5, WLS-REQ-001 v0.8, WLS-PRC-001 v0.8, `bom/bom.csv`, `bom/bom-notes.md`. R12 is now reported against the value-engineering target. No other requirement changed status. | Follows the model. |
| Media | Concept media regenerated from the model. The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` need re-rendering on Amish's Mac. The appearance model `cad/src/product_model.py` was brought into line with the constructable design on 2026-10-02 and the render scenes exported. | They are made with Blender. |

*Table 3. Decided by Amish, 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Locking (R16). The rim band, tube cap and junction box lid can now be undone with a screwdriver or by hand, which the concept did not address either. | (a) a security-head screw on the rim band, a padlock through the cross bolt's head, and a padlockable hasp kit on the box; (b) a lockable steel cover over the whole wellhead. | (a): small, cheap parts that fit the present design; decide after the first site visit. **Decided by Amish, 2026-10-02:** (a) is fitted on the prototype from the start; (b) at sites where the first site visit shows open access or livestock. The locking parts are now in the model, the BOM (line 16, and an eye bolt in line 5) and the drawings; the padlock on the cap is hung through the eye of an M5 eye bolt, which stops the bolt being unscrewed but not the cap being lifted (the steel cover does that). |
| A2 | The FieldNode core's geometry is copied from the FieldNode model into `cad/vendor/`, so a FieldNode change does not reach WellSense until it is exported again. | (a) keep the copy and re-export it whenever FieldNode's general arrangement is revised; (b) share it through a common library repo. | (a), noted in the review checklist. **Decided by Amish, 2026-10-02: (a).** |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan WLS-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: 1 not met (R9), 4 at risk (R4, R10, R15, R16), 3 not verifiable at TRL 3 (R5, R11, R13), 7 met, and R12 over its value-engineering target (WLS-CAL-001 v0.4).
- The seal plate hole sizes follow the design well's riser and pump cable; at a real well they are set from the measured riser and cable. The enclosure's boss spacing and lug kit, the collar's grip rating and the drinking-water certificates of the HDPE and EPDM are confirmed when parts are bought (WLS-DEC-001).
- TRL stays 3. Nothing in this record authorizes building or testing.
