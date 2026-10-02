---
doc_id: WLS-PRC-001
title: WellSense design precis
project: WellSense
doc_type: Design precis
version: "0.6"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update from WLS-CAL-001 and WLS-DDR-001 (24 V loop boost, 0.25 % class probe, two-point calibration, numbers checked, choices adopted for TRL 3 pending review)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish; parts within the $200 budget
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: Constructable design (WLS-DDR-004) and build plan WLS-BLD-001; cost against the value-engineering target
---

# WellSense design precis

## Summary

WellSense hangs a vented submersible pressure transducer in its own access tube inside an existing well and reads it every 15 minutes through the lab's shared FieldNode core, which sends the level over LoRaWAN to an open community dashboard. The TRL 3 calculations (WLS-CAL-001) give 0.52 mm resolution and a sensor load of 38.2 mWh a day, 1.6 % of FieldNode's 100 mW allowance. They also found that FieldNode's 12 V rail cannot drive the current loop, so the interface board carries a 24 V boost. After a two-point field calibration against a manual tape, a 0.25 % class probe reaches 12.5 mm by root sum square against the ±20 mm target, but 27.1 mm if every error adds, so accuracy is at risk. Amish accepted all recommendations on 2026-09-25 (WLS-DDR-002): the budget rises to $190 for the 30 m design well, the probe is limited to 22 mm so it runs freely in the 1 in access tube (2.3 mm radial clearance), a galvanized conduit protects the surface cable, FieldNode's sun shield is fitted at hot sites, and pumping tests on a public network send every 30 min. Writing the prototype build plan (WLS-BLD-001) made the design constructable (WLS-DDR-004): a split HDPE seal plate that closes round the riser and pump cable, a collar that carries the tube, a cross bolt and support grip that carry the probe, a flexible conduit tail so the cap can lift for calibration, and a junction box on a plate with V-blocks. Value-engineering target: USD 200. Estimated cost of the constructable design: USD 244.40 at a 30 m probe depth (USD 44.40 over the target), and $383.40 with the FieldNode core. The design choices below are decided by Amish (WLS-DDR-001 and WLS-DDR-002); the changes for construction are open for his review.

![Hero render](../media/hero.png)

Figure 1. Concept massing model in a borehole with a pump and riser, soil cut open, 1.75 m person for scale. The borehole is shortened for display. CONCEPT, NOT FOR FABRICATION.

## How it works

1. **Sense.** The transducer measures the pressure of the water column above it. Its cable carries a capillary vent tube to the surface, so the sensor reads gauge pressure and air pressure changes cancel out. Water above the probe is h = p / (ρg), about 102 mm per kPa.
2. **Keep clear of the pump.** The probe, 22 mm in diameter or less, hangs at a recorded depth inside a 25 mm PVC access tube, slotted at the bottom, so it cannot tangle with the pump cable or riser and can be pulled for checks without touching the pump.
3. **Seal the wellhead.** A split HDPE seal plate replaces or supplements the existing well cap: its two halves close round the riser, the pump cable and the access tube on EPDM wraps, a spigot ring locates it in the casing and a band round its rim holds it shut. A collar on the tube rests on the plate. The probe hangs from a cable support grip on a cross bolt in the tube cap; the cable leaves the cap through a short flexible tail and runs to the junction box inside a 1/2 in galvanized conduit.
4. **Read.** FieldNode switches its 12 V rail on sensor port 1 for about 2 s every 15 min. A boost on the interface board raises it to 24 V, because 12 V leaves the transducer 4.44 V short of its 12 V minimum through the shunt and 62 m of cable (WLS-CAL-001, section B). The 4 to 20 mA loop current develops 0.6 to 3.0 V across a 150 Ω precision shunt, read by a 16-bit ADC over I2C. A barometric sensor on the post logs air pressure.
5. **Convert and send.** Firmware converts current to water above the probe, then to depth to water below the measuring point: depth = probe depth below the measuring point minus water above the probe. FieldNode stores each reading and sends it in a short LoRaWAN uplink. During a pumping test at 1 min, readings are batched: every 15 min on a private TwinKit gateway, every 30 min on a public network to stay within fair use (22.7 s a day at SF9).
6. **Show.** An open dashboard plots level below ground, daily pumping drawdown and recovery, and the change against the same month last year. The community owns the data and can export CSV.
7. **Check.** At installation a caretaker measures depth to water with a manual electric tape, as in USGS procedures ([Cunningham and Schalk, 2011](https://pubs.usgs.gov/tm/1a1/)), then lifts the cap and probe a measured 1 m, the cable feeding from a service loop in the junction box, and reads again; the two points fix offset and span. Each quarter a tape reading checks and corrects drift.

![Data flow](../media/flow.png)

Figure 2. Data flow from probe to dashboard. Values are estimates from WLS-CAL-001.

## Main components

Table 1. Main components, numbered as in the BOM and the exploded view.

| # | Component | Adopted choice | Notes |
| --- | --- | --- | --- |
| 1 | Pressure transducer | Vented 4 to 20 mA, 0 to 10 m, 0.25 % full scale class, 316 stainless, 22 mm diameter or less, IP68 | Range and type per DDR-001, D2 and D3; diameter per DDR-002 |
| 2 | Vented cable | PU or PE jacket, two 0.2 mm² cores, 400 N strain member, vent capillary, about 7 mm | Probe depth plus 2.7 m, to 60 m |
| 3 | Access tube | 25 mm (1 in) Sch 40 PVC, 26.6 mm bore, drilled with 8 mm holes over the bottom 0.5 m, slip cap on the end | Where a pump or riser shares the casing (DDR-001, D4); 2.3 mm radial clearance for a 22 mm probe (DDR-002) |
| 4 | Wellhead seal plate | Two 20 mm HDPE halves, 200 mm diameter, with spigot rings, EPDM gasket and wraps, a rim band and a tube collar, for 150 mm casing | Fits round an installed riser and pump cable; keeps surface water and insects out |
| 5 | Tube cap and support grip | PVC slip cap with an M5 cross bolt; stainless cable support grip | Sets and records probe depth; lifts off for calibration |
| 6 | Junction box | IP66 box with lugs, two glands, a conduit hub and a silica gel breather in its floor | Desiccant changed every visit |
| 7 | Interface board | 150 Ω 0.1 % 10 ppm/K shunt, 16-bit ADC with series input resistor, 12 to 24 V boost, 3.3 V regulator, TVS surge protection | Off-the-shelf modules, no custom PCB |
| 8 | FieldNode core | Lab shared node: enclosure, 6 W panel, LiFePO4 cell, LoRaWAN radio; sun shield at hot sites | See the FieldNode repo (FND-DDR-002 for the shield) |
| 9 | Barometric sensor | BMP390 or BME280 class, in a vented housing on the post | Aquifer air pressure response; vent check |
| 10 | Mounting post | 48.3 mm galvanized pipe, 2.7 m, 2.1 m above ground, 0.75 m from the well; junction box plate with V-blocks and band clamps | FieldNode base at 1.75 m (FND-DDR-001, D11) |
| 13 | Post footing | 300 mm diameter, 0.6 m deep, one 25 kg bag of concrete | Added at TRL 3 |
| 14 | Surface cable conduit | 1/2 in (21.3 mm OD) galvanized rigid conduit, about 0.95 m with one bend, on two saddles; 0.3 m flexible tail to the tube cap | Added under DDR-002 for R16; tail and saddles under DDR-004 |
| 15 | FieldNode lead | Four-core lead with an M12 plug, junction box to FieldNode port A | Added under DDR-004 |

![Exploded view](../media/exploded.png)

Figure 3. Exploded view with BOM callouts. CONCEPT, NOT FOR FABRICATION.

![Cutaway](../media/cutaway.png)

Figure 4. Broken section: wellhead (left) and lower borehole with water level and probe (right).

## Numbers checked at TRL 3

All values come from WLS-CAL-001, where the assumptions are stated.

Table 2. Key numbers from WLS-CAL-001.

| Quantity | Value | Basis | Requirement |
| --- | --- | --- | --- |
| Full-scale pressure | 98.07 kPa | 10 m × 1,000 kg/m³ × 9.80665 m/s² | R1 met |
| Resolution | 0.52 mm | 16 mA × 150 Ω = 2.4 V; 125 µV ADC step; 19,200 steps over 10 m | R3 met |
| Loop voltage at the transducer | 7.56 V from 12 V; 20.16 V with the 24 V boost | 22 mA, 150 Ω shunt, 62 m of cable, diode | 12 V minimum; boost required |
| Accuracy, datasheet only | 50 mm (0.5 % class); 25 mm (0.25 % class) | Percentage of 10 m full scale | |
| Accuracy after two-point calibration | 12.5 mm RSS; 27.1 mm worst case | 0.25 % class probe; Table 2 of WLS-CAL-001 | R4 at risk |
| Density change, 4 to 25 °C | 0.29 %, 29 mm at 10 m | Fixed site density in firmware | |
| Absolute sensor without compensation | ±306 mm | ±3 kPa weather swing | Reason for the vented design |
| Energy per reading | 1.43 J | 24 V × 22 mA × 2 s through boost and rail, plus the controller | |
| Sensor energy per day | 38.2 mWh | 96 readings | R8 met: 1.6 % of 100 mW |
| Pumping test airtime, public network | 22.7 s/day | 30-reading batch every 30 min at SF9 | R6 met, within 30 s fair use |
| Energy at 1 min interval | 0.573 Wh/day | 1,440 readings | 24 % of the allowance during tests |
| Storage per year | 1.12 MB | 35,040 readings × 32 bytes | R7 met: 6.7 % of 16 MB |
| Probe clearance in the tube | 2.3 mm radial | 22 mm probe in 26.6 mm bore | R10 at risk (pump may need pulling) |
| Hanging loads at 60 m | 35 N cable (factor 11.5); 264 N tube (factor 58) | Dry, worst case | R2 met |
| WellSense parts per well | $244.40 | bom/bom.csv, 30 m probe depth, constructable design | R12: $44.40 over the $200 value-engineering target |
| With FieldNode core | $383.40 | Adds line 8 ($139.00, FND-CAL-001 v0.3); $392.40 with the hot-site shield | Counted in the FieldNode repo (DDR-001, D1) |
| Depth-dependent cost | $1.80 per metre | Cable plus access tube | |

## Key design choices

Decided by Amish, 2026-09-25: go with recommendation (WLS-DDR-001 and WLS-DDR-002).

- **Vented 4 to 20 mA transducer rather than an absolute-pressure sensor with barometric compensation (D2).** The current loop is robust over long cables and the reading needs no compensation. The costs are desiccant maintenance at the vent and a 24 V boost, since the loop needs more than FieldNode's 12 V rail. A sealed absolute sensor with RS-485 and a surface barometer is kept as a variant.
- **0 to 10 m range (D3),** with a 0 to 20 m variant for wells whose seasonal swing plus drawdown exceeds 9 m.
- **Own access tube where a pump is present (D4).** Standard practice to protect the probe and the pump; also the hardest part to fit in an existing well (R10 at risk). The tube ends above the pump.
- **FieldNode as the core (D8).** Reuses the lab's shared enclosure, solar charging, storage and radio, so WellSense designs only the well side. The interface board connects to sensor port 1 (switched 12 V rail and I2C); the pinout is still open in FieldNode (FND-DDR-001, O2). A battery-only node remains a question for the FieldNode project (DDR-001, O2).
- **Manual tape as the reference (D6).** A shared electric tape sets the datum and the two-point calibration at installation and checks drift each quarter.
- **Levels only (D7).** No camera, audio or pump data; the dashboard shows water level so that sharing the data carries little risk.
- **1 in access tube with a probe of 22 mm or less (DDR-002).** Keeps the tube small enough to pass a centered riser in 150 mm casing; a 1-1/4 in tube would fit only 200 mm casing.
- **Galvanized conduit over the surface cable (DDR-002).** Protects the cable from livestock, mowing and tampering between the tube cap and the junction box.
- **Hot sites (DDR-002).** R15 stays at 55 °C; where the design maximum air temperature exceeds 30 °C (FND-CAL-001 v0.2), the FieldNode core carries FieldNode's sun shield (FND-DDR-002).
- **Pumping-test uplinks (DDR-002).** Every 30 min on a public network, every 15 min on a private TwinKit gateway.

## Safety

> **Safety:** Drinking water. Anything lowered into a supply well can contaminate it. Disinfect the probe, cable and tube before installation (for example with a chlorine solution as local water authorities advise), use only materials suitable for drinking water contact, and keep the wellhead sealed so surface water, insects and animals cannot enter. Involve the well owner or water authority before opening a public supply well.

> **Safety:** Electrical and pump hazards. Many wells contain a submersible pump on mains power. Isolate and lock off the pump supply before working at the wellhead, and keep the logger wiring separate from the pump cable. WellSense itself runs at 24 V or less (extra-low voltage).

> **Safety:** Lithium cell. The FieldNode core contains a lithium iron phosphate cell of about 19 Wh; follow the FieldNode safety notes on fusing and charging temperature limits.

> **Safety:** Working at an open well. An open dug well or large borehole is a fall and drowning hazard, especially for children. Never leave a wellhead open, and cover large-diameter wells while working.

> **Safety:** Lifting and cable handling. A long cable with a probe and tube can be heavy; lower it slowly with two people so it does not run away into the well, and never let the cable carry more than the rated load of its strain member.

## Open questions

- [ ] Can an access tube be added beside an installed pump without pulling it? Only an installation trial can tell.
- [ ] Real long-term drift of low-cost vented transducers; is a quarterly tape check enough?
- [ ] Which drinking water material certifications can low-cost suppliers show for cable, seals and probe?
- [ ] How should the dashboard present drawdown so that non-specialists read it correctly? To be answered in co-design.
- [ ] Locking of the seal plate, tube cap and junction box (R16).
- [ ] First partner and region for co-design (DDR-001, O1).
- [x] Cost at the 30 m design depth with the conduit included ($197.60). Budget set to $200 to cover the priced BOM: decided by Amish, 2026-09-26 (WLS-DDR-002). Since 2026-10-01 the $200 is a value-engineering target; the constructable design is estimated at $244.40.

Open decisions are tracked in the [design decisions register](06-design-decisions.md).

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
