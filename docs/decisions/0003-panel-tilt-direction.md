---
doc_id: WLS-DDR-003
title: WellSense FieldNode panel tilt direction
project: WellSense
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-27'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-27'
  author: Amish Chadha
  change: "Panel tilt sign corrected in model.py so the cells face -Y, as in FND-DWG-001: decided by Amish on 2026-09-27"
---

# 0003: FieldNode panel tilt direction

- **Date:** 2026-09-27
- **Status:** accepted. Decided by Amish on 2026-09-27.

## Context

The review of the product appearance model (`docs/REVIEW.md`, session 2026-09-26, render item 2) found that `cad/src/model.py` rotated the FieldNode solar panel by -40 deg about X. That turned the cells toward +Y, toward the post, with the high edge at the front. The FieldNode model (FND-DWG-001) tilts the panel toward -Y, the direction the node faces, and the product appearance model (`cad/src/product_model.py`) already drew it that way with its own rotation.

## Options considered

1. Correct the sign in `model.py` so the massing model, the drawing and the renders agree with FieldNode (recommended in the review).
2. Leave `model.py` as it was and keep the appearance model different.

## Decision

Option 1. On 2026-09-27 Amish wrote: "resolve the challenges for ConePro, BridgePulse, Grainguard and WellSense." Decided by Amish on 2026-09-27: go with the recommendation.

## Consequences

- `cad/src/model.py`: `derived()` now returns `panel_rot_x`, the X rotation of the panel (+40 deg, cells toward -Y, high edge at the back toward the post). `build_parts()` uses it, and the two panel legs now run from the back plate to the underside of the panel 60 mm behind its center line, so they still meet the panel. The 40 deg tilt, the 290 x 200 x 17 mm panel, its center, the enclosure and every interface are unchanged; the overall height stays 2,206 mm.
- `cad/src/product_model.py`: takes the panel rotation from `derived()["panel_rot_x"]` instead of applying its own opposite sign. Its geometry is unchanged.
- WLS-DWG-001 is reissued at Rev P3; the STEP and STL files and the concept media are regenerated from `model.py`.
- The BOM, the requirements and the calculations are unaffected. TRL stays 3.
