---
doc_id: WLS-MKT-001
title: WellSense market and viability
project: WellSense
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First issue (kit 1.9.1 upgrade), with cited benchmark prices checked on 2026-10-25
---

# WellSense market and viability

WellSense is for the people who share an aquifer and have no measurement of it: village water committees, farmer groups, handpump caretakers and the NGOs and agencies that work with them, first in India with a participatory groundwater partner. A commercial level logger without telemetry lists at USD 425 to 750 and an Indian telemetered recorder at INR 47,500, while WellSense's parts cost USD 264.40 at a 30 m depth (USD 403.40 with the lab's FieldNode telemetry core), and it is open, so a community or a school can build, check and repair it. Prices and benchmarks are cited with the date they were checked. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Participatory groundwater management | Farmer groups and village water committees sharing an aquifer; India first (ACWADAM, Pune, first candidate partner, not yet approached) | CGWA-style digital water level recorders from an Indian maker: INR 34,000 to 38,000 without telemetry and INR 47,500 with telemetry (Acorn Controls listings, checked 2026-10-25) | 264.40 parts at 30 m; 403.40 with the FieldNode core and LoRaWAN | Continuous, community-owned record at a fraction of a commercial recorder; open data; repairable locally |
| WASH programmes and handpump networks | NGOs and utilities in sub-Saharan Africa and South Asia monitoring community water points | Onset HOBO U20L-04 water level logger, 0 to 4 m: USD 425.00 (Instrumart, checked 2026-10-25), no telemetry and a separate barometric logger needed | 264.40 (233.40 where no pump shares the casing and no tube is needed) | Telemetry included through FieldNode; early warning when the level nears the pump intake |
| Network densification for agencies | Groundwater departments and researchers adding wells between official monitoring stations | Solinst Levelogger 6: USD 749.55; Levelogger 6 Junior: USD 535.80 (Fondriest, checked 2026-10-25), no telemetry | 264.40 parts (403.40 with telemetry) | More wells for the same budget; open hardware and data formats |
| Teaching and research | Universities and schools teaching hydrogeology and instrumentation | Same commercial loggers as above | 264.40 parts | Inspectable, buildable instrument for teaching; a lab exercise in calibration against a tape |

The benchmarks are list prices for one unit from distributors, not quotes; they buy a sealed, calibrated, supported instrument with years of field record, which WellSense does not yet have (PR-004 at risk, PR-005 to verify at TRL 4). WellSense's figures are indicative estimates from `bom/bom.csv` (September 2026, quantity 1), not quotes. The USD 200 value-engineering target is a control target, not a price.

## Open route

- **Who builds it.** A partner's field team, a district workshop or a university lab, from the build plan (WLS-BLD-001) with plumbing, electrical and online parts and hand tools; the FieldNode core comes from the lab's shared design.
- **How it spreads.** Through participatory groundwater programmes (the first candidate partner works with farmer groups on shared aquifers), WASH NGOs, the Helpful Engineering volunteer network and hydrogeology courses; build reports and design suggestions come back through the repo's issue templates.
- **What keeps it open.** CERN-OHL-S-2.0 for the hardware and MIT for the software (REUSE.toml), data owned by the hosting community (PR-014), and a design that avoids proprietary parts: any vented 4 to 20 mA transducer of the right size and class will do.
- **What it is not.** It is not a certified instrument for regulatory compliance (WLS-REG-001 G6, G7); a regulated user would need a certified recorder until WellSense has a test record and, if pursued, a certification route.

## Sources

- Instrumart. "HOBO U20L Series Water Level Loggers." https://www.instrumart.com/products/40734/hobo-u20l-series-water-level-loggers (U20L-04 at USD 425.00; checked 2026-10-25).
- Fondriest Environmental. "Solinst Levelogger 6 Water Level Loggers." https://fondriest.com/solinst-levelogger-5-water-level-loggers.htm (Levelogger 6 at USD 749.55, Levelogger 6 Junior at USD 535.80; checked 2026-10-25).
- Acorn Controls Private Limited, IndiaMART listings. "Digital Piezometer." https://m.indiamart.com/acorn-controls/digital-piezometer.html (DWLR and piezometer sets INR 34,000 to 47,500; telemetry piezometer DWLR INR 47,500; checked 2026-10-25).
- Central Ground Water Authority. Notification S.O. 3289(E), 24 September 2020, Table 14.1 (see WLS-REG-001 G6).
- WellSense cost: `bom/bom.csv` and WLS-CAL-001 [H2], [H3].
