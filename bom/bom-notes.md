# BOM notes

All costs are indicative estimates in USD at quantity 1 (September 2026), not quotes. Every line is priced, with a supplier or supplier type. The total is checked against `budget_usd` in `project.yaml` by `docs/04-calcs/sizing.py` (WLS-CAL-001, section H).

- Rows 1 to 10 and 13 are numbered to match the callouts in `media/exploded.png` and the parts in `cad/src/model.py`. Rows 11 and 12 are not modeled.
- The design case is a probe 30 m below the top of the casing: 32 m of cable (30 m plus a 2 m surface run) and 31 m of access tube.
- WellSense parts per well (rows 1 to 7, 9, 10 and 13): **$187.60**, $7.60 over the $180 `budget_usd`. The budget holds to a probe depth of 25.8 m. Without an access tube (no pump in the casing) the parts cost $156.60.
- Row 8, the FieldNode core ($126.00 in FND-CAL-001), is costed in the FieldNode repo under WLS-DDR-001, D1 (adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review). With it, a complete logger is $313.60.
- Changes at TRL 3: row 1 specified in the 0.25 % class (+$5, to reach R4 after calibration); row 7 gains a 12 to 24 V boost and a 3.3 V regulator (+$2), because the FieldNode 12 V rail cannot drive the loop; rows 2 and 3 are priced per metre; row 10 is lengthened so the FieldNode core sits at 1.75 m (+$2); row 13, footing concrete, is new (+$6).
- Row 11, the manual water level meter, is shared by a community or partner and is not in the per-well cost.
- The LoRaWAN gateway (TwinKit or a public network) is not included. A surface cable guard for R16 is proposed, awaiting Amish, and is not in the total.
- Cable and access tube scale with probe depth: $1.80 per metre of depth together.
