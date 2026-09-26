---
doc_id: WLS-PRB-001
title: WellSense problem statement
project: WellSense
doc_type: Problem statement
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (problem, users, context, constraints, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Reflect WLS-DDR-001 (budget covers WellSense parts only) and the TRL 3 cost and access findings of WLS-CAL-001
---

# WellSense problem statement

Groundwater is falling in many regions, yet most wells have no measurement, so over-pumping is noticed only when wells run dry. The people who share an aquifer need a cheap, trustworthy record of how the water level in their own wells moves through the day, the season and the years, in a form they can read and discuss.

## The problem

Groundwater supplies about half of the water withdrawn for domestic use worldwide, including drinking water for most rural people, and about 25 % of irrigation water ([UNESCO, World Water Development Report 2022](https://www.unesco.org/reports/wwdr/2022/en)). A synthesis of in situ records from about 170,000 monitoring wells in 1,693 aquifer systems found rapid declines of more than 0.5 m a year widespread in the twenty-first century, and accelerating declines in 30 % of regional aquifers ([Jasechko et al., Nature, 2024](https://www.nature.com/articles/s41586-023-06879-8)). The same study shows recoveries where pumping was regulated or recharge increased, as in the Bangkok basin, so measured decline can be reversed when people act on it.

Most wells that people actually draw from are not monitored. Official networks use a small number of dedicated observation wells, and data reach village councils, farmer groups and handpump committees late or not at all. Owners learn that the aquifer is falling when the pump starts to suck air or the handpump runs dry, and the usual response is to drill deeper. In the United States, new wells are being built deeper 1.4 to 9.2 times more often than shallower ([Perrone and Jasechko, Nature Sustainability, 2019](https://www.nature.com/articles/s41893-019-0325-z)), a stopgap that the authors call unsustainable.

Commercial water level loggers exist and work well, but they cost several hundred dollars each before telemetry, need vendor software, and are usually owned by an agency rather than the community. There is no open, low-cost reference design that a community group, a WASH organization or a school can build, check and repair.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Village water committee or farmer group sharing an aquifer | See whether the water table is falling, how fast, and how it responds to pumping and rain; set local rules | Rural India, sub-Saharan Africa, Mexico, Middle East; shared tube wells and boreholes |
| Handpump or borehole caretaker | Know when static level approaches the pump intake before the supply fails | Community water points, often no grid power |
| Farmer with a private irrigation well | Plan pumping hours and crop choice; avoid dry wells | Seasonal peaks in the dry season |
| WASH NGO, utility or groundwater agency | Low-cost network densification between official monitoring wells | Programme monitoring, drought early warning |
| Hydrogeology student or researcher | Open, inspectable data and hardware for teaching and small studies | Universities, schools |

Typical wells are 100 to 200 mm (4 to 8 in) boreholes 20 to 150 m deep with a submersible pump or handpump riser inside, or large-diameter dug wells. Static water levels lie from a few metres to more than 50 m below ground, with seasonal swings of several metres in intensively pumped areas. The wellhead may be exposed to sun, flooding, livestock and tampering. Mobile coverage is patchy; the lab's shared node, FieldNode, reports over LoRaWAN to a TwinKit gateway or a public network.

## Constraints

- Garage-buildable prototype, $180 USD in WellSense parts per well, with the FieldNode core costed in the FieldNode repo (WLS-DDR-001, D1, adopted for TRL 3 pending Amish's review). At TRL 3 the parts cost $187.60 at a 30 m probe depth, so the budget holds only to about 25.8 m (WLS-CAL-001).
- Built on the lab's shared FieldNode core for power, radio and enclosure; WellSense adds only the probe, wellhead parts and interface.
- No change to the water supply: nothing in the well may contaminate the water, and the well must stay sealed.
- Must work beside an existing pump and riser without pulling them where possible.
- Data belongs to the community that hosts the well. Readings are water levels only; the owner decides what to share.
- Hand tools only for installation; parts available from plumbing, electrical and online suppliers.

## Prior work

- **Commercial loggers.** Absolute-pressure loggers with barometric compensation and vented 4 to 20 mA transducers are the standard tools in groundwater monitoring. They are accurate and robust but closed and costly for community use.
- **Standard methods.** The U.S. Geological Survey publishes procedures for measuring well water levels with a steel tape, an electric tape and a submersible pressure transducer ([Cunningham and Schalk, USGS Techniques and Methods 1-A1, 2011](https://pubs.usgs.gov/tm/1a1/)). WellSense follows the same logic: a transducer for the continuous record and a manual tape for the datum and periodic checks.
- **Open loggers.** The Cave Pearl Project showed that an Arduino-class logger built from breakout boards can run for more than a year on three AA cells for $25 to $50 before sensors ([Beddows and Mallon, Sensors, 2018](https://www.mdpi.com/1424-8220/18/2/530)).
- **Community groundwater management.** Farmer-led monitoring programmes in India have trained villagers to record well levels and rainfall and use them to plan crops. WellSense aims to make that record continuous and cheap. The specific programme data were not verified in this session and are left out.

## Out of scope

- Water quality (conductivity, nitrate, arsenic). A conductivity probe could share the port later.
- Pump control or metering of abstraction.
- Aquifer modelling beyond simple trend and drawdown charts.

## Open questions

- First partner and region for co-design: an Indian farmer group, an African handpump programme or a US groundwater agency? Proposed, awaiting Amish (WLS-DDR-001, O1).
- How much access to the wellhead can a community give: can an access tube be added without pulling the pump? WLS-CAL-001 shows a 1 in tube fits beside the riser of a 150 mm well in plan, but only an installation trial can show whether it can be lowered past an installed pump's riser and cable.
- Who holds and publishes the data, and in what language and form do users want the dashboard?

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
