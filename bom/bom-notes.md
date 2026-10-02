# BOM notes

All costs are indicative estimates in USD at quantity 1 (September 2026), not quotes. Every line is priced, with a supplier or supplier type. The total is compared with the value-engineering target, `budget_usd` in `project.yaml`, by `docs/04-calcs/sizing.py` (WLS-CAL-001, section H). `budget_usd` is a hypothetical control target that keeps the design on a value-engineering lens, not a spending limit (Amish, 2026-10-01).

- Rows 1 to 10 and 13 to 15 are numbered to match the parts in `cad/src/model.py` and the callouts in `media/exploded.png`. Rows 11 and 12 are not modeled.
- The design case is a probe 30 m below the top of the casing: 33 m of cable (30 m plus a 2.7 m surface run that includes a 1.1 m service loop in the junction box) and 31 m of access tube.
- Value-engineering target: USD 200. Estimated cost of the constructable design (rows 1 to 7, 9, 10 and 13 to 15): **USD 244.40** (USD 44.40 over the target). The concept, before the design was made constructable, was $197.60.
- Changes for construction (WLS-DDR-004): row 4 becomes a split HDPE seal plate with spigot rings, EPDM gasket and wraps, a rim band and a tube collar (+$8.00); row 5 a drilled slip cap with a cross bolt and cable support grip (+$4.00); row 6 gains lugs and glands (+$6.00); row 7 a terminal strip and printed internal plate (+$1.00); row 10 a junction box plate, two V-blocks and a post cap (+$10.00); row 14 a flexible tail, spacer saddles and a hub (+$10.00); row 15, the FieldNode lead, is new (+$7.00); row 2 is 1 m longer (+$0.80).
- Row 8, the FieldNode core, is now FieldNode's constructable base node ($139.00 in FND-CAL-001 v0.3, was $126.00) and is costed in the FieldNode repo under WLS-DDR-001, D1. With it a complete logger is $383.40, and $392.40 at a hot site with FieldNode's $9.00 sun shield (FND-DDR-002).
- Changes at TRL 3: row 1 specified in the 0.25 % class (+$5, to reach R4 after calibration); row 7 gains a 12 to 24 V boost and a 3.3 V regulator (+$2), because the FieldNode 12 V rail cannot drive the loop; rows 2 and 3 are priced per metre; row 10 is lengthened so the FieldNode core sits at 1.75 m (+$2); row 13, footing concrete, is new (+$6).
- Changes under WLS-DDR-002: row 1 limited to a 22 mm body (price assumed unchanged, to be confirmed); row 14, galvanized surface conduit, added (+$10.00).
- Row 11, the manual water level meter, is shared by a community or partner and is not in the per-well cost.
- The LoRaWAN gateway (TwinKit or a public network) is not included.
- Cable and access tube scale with probe depth: $1.80 per metre of depth together. Savings worth trying are listed in the design decisions register (`docs/06-design-decisions.md`).
