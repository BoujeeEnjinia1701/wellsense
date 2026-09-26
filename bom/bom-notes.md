# BOM notes

All costs are indicative estimates in USD at quantity 1 (September 2026), not quotes. Every line is priced, with a supplier or supplier type. The total is checked against `budget_usd` in `project.yaml` by `docs/04-calcs/sizing.py` (WLS-CAL-001, section H).

- Rows 1 to 10, 13 and 14 are numbered to match the callouts in `media/exploded.png` and the parts in `cad/src/model.py`. Rows 11 and 12 are not modeled.
- The design case is a probe 30 m below the top of the casing: 32 m of cable (30 m plus a 2 m surface run) and 31 m of access tube.
- WellSense parts per well (rows 1 to 7, 9, 10, 13 and 14): **$197.60**, $2.40 under the $200 `budget_usd` (approved by Amish on 2026-09-26 to cover the priced BOM, WLS-DDR-002; it was $190, and $180 before 2026-09-25). Without the $10.00 conduit the parts would be $187.60. The budget holds to a probe depth of 31.3 m. Without an access tube (no pump in the casing) the parts cost $166.60.
- Row 8, the FieldNode core ($126.00 in FND-CAL-001), is costed in the FieldNode repo under WLS-DDR-001, D1 (decided by Amish, 2026-09-25: go with recommendation). With it, a complete logger is $323.60, and $331.60 at a hot site with FieldNode's $8.00 sun shield (FND-DDR-002).
- Changes at TRL 3: row 1 specified in the 0.25 % class (+$5, to reach R4 after calibration); row 7 gains a 12 to 24 V boost and a 3.3 V regulator (+$2), because the FieldNode 12 V rail cannot drive the loop; rows 2 and 3 are priced per metre; row 10 is lengthened so the FieldNode core sits at 1.75 m (+$2); row 13, footing concrete, is new (+$6).
- Row 11, the manual water level meter, is shared by a community or partner and is not in the per-well cost.
- The LoRaWAN gateway (TwinKit or a public network) is not included.
- Changes under WLS-DDR-002: row 1 limited to a 22 mm body (price assumed unchanged, to be confirmed); row 14, galvanized surface conduit, added (+$10.00).
- Cable and access tube scale with probe depth: $1.80 per metre of depth together.
