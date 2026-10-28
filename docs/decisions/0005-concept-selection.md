---
doc_id: WLS-DDR-005
title: WellSense concept selection
project: WellSense
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: Concept selection between options A, B and C of WLS-OPT-001 argued; A and C within 10 %, both put to Amish without a pick; proposed, awaiting Amish
---

# 0005: Concept selection

- **Date:** 2026-10-25
- **Status:** proposed, awaiting Amish. Nothing here is decided; the repo stays on option A, the current design, until Amish decides (STANDARDS section 21, existing designs).

## Context

Kit 1.8 asks every repo for at least two concept options with different working principles, scored against the same user requirements (STANDARDS section 21), and kit 1.9 asks for every option to be modelled to the repo's detail level (D3 at P3; Amish, 2026-10-24: "Detail every option"). WellSense was designed before kit 1.8, so its current design is option A. Two other ways of turning a water level into a number fit the same wellhead, tube, post, junction box and FieldNode core: a bubbler (B) and an acoustic echo sounder (C). All three are in `cad/src/model.py` (`OPTIONS`, `components(option)`) and pass the D3 fidelity check (`cad/fidelity.json`); their STEM rows are in WLS-STM-001 and their scoring in WLS-OPT-001.

## Options

Table 1. The options and their weighted scores (WLS-OPT-001, Table 2; of 215).

| Option | Working principle | Score | Cost at 30 m (USD) | Sensor energy | Main open point |
| --- | --- | --- | --- | --- | --- |
| A, vented transducer in an access tube (current design) | Hydrostatic head on a vented 4 to 20 mA probe hung in the tube | 173 | 264.40 (priced) | 38.2 mWh/day | Calibrated accuracy 37.1 mm worst case (STM S7); drift (S10); certificates for the probe and cable (PR-009) |
| B, bubbler with a surface sensor | Back-pressure of air purged down a PE line, read at the surface | 147 | about 233 (estimate) | 263 mWh/day | Energy 11 % of FieldNode's allowance against 5 % (PR-008); pump and valve wear; pump pressure (B4) |
| C, acoustic echo sounder | Time of flight of a chirp down the tube's air column to the water surface | 164 | about 205 (estimate) | 10.6 mWh/day | Speed-of-sound calibration from joint echoes unproven in PVC (C2); signal at depth (C3); condensation on the head (C5) |

## Recommendation

Options A and C score within 10 % of each other (164 is 5.2 % below 173), so both go to Amish without a pick, as STANDARDS section 21 requires. For his choice:

- **Choose A** to keep the proven, fully drawn and priced design; its open points are evidence (a side-by-side tape record and supplier certificates), not principle.
- **Choose C** to pursue a cheaper logger with nothing new in the water and a quarter of A's energy, accepting that its accuracy depends on an echo calibration that needs a TRL 4 echo test in a real PVC tube before any redesign of the drawing, BOM or build plan.

Option B is not put forward: its pump energy misses PR-008 and it adds wear parts, for an accuracy no better than A's.

Graft for either choice: record the depth of every tube joint on the build sheet (C's idea), so a later acoustic check head or a tape can confirm the probe depth without pulling it.

## Consequences

- If Amish chooses A: `project.yaml` `concept_chosen: A`; no design change.
- If Amish chooses C: `CHOSEN` in `cad/src/model.py` stays A until the TRL 4 echo test is planned and approved; the C head, ranging board and firmware get their own STEM closure, BOM lines, drawing and build plan in a later session.
- Either way the decision is recorded in WLS-DEC-001 and WLS-PRC-001 is updated to describe the chosen option.
