---
doc_id: WLS-PRC-001
title: WellSense design precis
project: WellSense
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update from WLS-CAL-001 and WLS-DDR-001 (24 V loop boost, 0.25 % class probe, two-point calibration, numbers checked, choices adopted for TRL 3 pending review)
---

# WellSense design precis

## Summary

WellSense hangs a vented submersible pressure transducer in its own access tube inside an existing well and reads it every 15 minutes through the lab's shared FieldNode core, which sends the level over LoRaWAN to an open community dashboard. The TRL 3 calculations (WLS-CAL-001) give 0.52 mm resolution and a sensor load of 38.2 mWh a day, 1.6 % of FieldNode's 100 mW allowance. They also found that FieldNode's 12 V rail cannot drive the current loop, so the interface board carries a 24 V boost. After a two-point field calibration against a manual tape, a 0.25 % class probe reaches 12.5 mm by root sum square against the ±20 mm target, but 27.1 mm if every error adds, so accuracy is at risk. The WellSense parts cost $187.60 at a 30 m probe depth, $7.60 over the $180 budget, and $313.60 with the FieldNode core. The design choices below are adopted for TRL 3 work under Amish's 2026-09-25 instruction, open for his review (WLS-DDR-001).

![Hero render](../media/hero.png)

Figure 1. Concept massing model in a borehole with a pump and riser, soil cut open, 1.75 m person for scale. The borehole is shortened for display. CONCEPT, NOT FOR FABRICATION.

## How it works

1. **Sense.** The transducer measures the pressure of the water column above it. Its cable carries a capillary vent tube to the surface, so the sensor reads gauge pressure and air pressure changes cancel out. Water above the probe is h = p / (ρg), about 102 mm per kPa.
2. **Keep clear of the pump.** The probe hangs at a recorded depth inside a 25 mm PVC access tube, slotted at the bottom, so it cannot tangle with the pump cable or riser and can be pulled for checks without touching the pump.
3. **Seal the wellhead.** A split seal plate replaces or supplements the existing well cap, with glands for the riser and access tube. The cable leaves the tube through a cap with a cable-grip hanger.
4. **Read.** FieldNode switches its 12 V rail on sensor port 1 for about 2 s every 15 min. A boost on the interface board raises it to 24 V, because 12 V leaves the transducer 4.44 V short of its 12 V minimum through the shunt and 62 m of cable (WLS-CAL-001, section B). The 4 to 20 mA loop current develops 0.6 to 3.0 V across a 150 Ω precision shunt, read by a 16-bit ADC over I2C. A barometric sensor on the post logs air pressure.
5. **Convert and send.** Firmware converts current to water above the probe, then to depth to water below the measuring point: depth = probe depth below the measuring point minus water above the probe. FieldNode stores each reading and sends it in a short LoRaWAN uplink.
6. **Show.** An open dashboard plots level below ground, daily pumping drawdown and recovery, and the change against the same month last year. The community owns the data and can export CSV.
7. **Check.** At installation a caretaker measures depth to water with a manual electric tape, as in USGS procedures ([Cunningham and Schalk, 2011](https://pubs.usgs.gov/tm/1a1/)), then lifts the probe a measured 1 m and reads again; the two points fix offset and span. Each quarter a tape reading checks and corrects drift.

![Data flow](../media/flow.png)

Figure 2. Data flow from probe to dashboard. Values are estimates from WLS-CAL-001.

## Main components

Table 1. Main components, numbered as in the BOM and the exploded view.

| # | Component | Adopted choice | Notes |
| --- | --- | --- | --- |
| 1 | Pressure transducer | Vented 4 to 20 mA, 0 to 10 m, 0.25 % full scale class, 316 stainless, 24 mm diameter or less, IP68 | Range and type per DDR-001, D2 and D3 |
| 2 | Vented cable | PU or PE jacket, two 0.2 mm² cores, 400 N strain member, vent capillary, about 7 mm | Probe depth plus 2 m, to 60 m |
| 3 | Access tube | 25 mm (1 in) Sch 40 PVC, 26.6 mm bore, slotted over the bottom 0.5 m | Where a pump or riser shares the casing (DDR-001, D4); bore tight for a 24 mm probe |
| 4 | Wellhead seal plate | Split plate, 200 mm diameter, EPDM gasket, two glands and a tube clamp, for 150 mm casing | Fits round an installed riser; keeps surface water and insects out |
| 5 | Tube cap and hanger | PVC cap with cable grip | Sets and records probe depth |
| 6 | Junction box | IP66 box with silica gel breather on the vent tube | Desiccant changed every visit |
| 7 | Interface board | 150 Ω 0.1 % 10 ppm/K shunt, 16-bit ADC with series input resistor, 12 to 24 V boost, 3.3 V regulator, TVS surge protection | Off-the-shelf modules, no custom PCB |
| 8 | FieldNode core | Lab shared node: enclosure, 6 W panel, LiFePO4 cell, LoRaWAN radio | See the FieldNode repo |
| 9 | Barometric sensor | BMP390 or BME280 class, in a vented housing on the post | Aquifer air pressure response; vent check |
| 10 | Mounting post | 48.3 mm galvanized pipe, 2.7 m, 2.1 m above ground, 0.75 m from the well | FieldNode base at 1.75 m (FND-DDR-001, D11) |
| 13 | Post footing | 300 mm diameter, 0.6 m deep, one 25 kg bag of concrete | Added at TRL 3 |

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
| Energy at 1 min interval | 0.573 Wh/day | 1,440 readings | 24 % of the allowance during tests |
| Storage per year | 1.12 MB | 35,040 readings × 32 bytes | R7 met: 6.7 % of 16 MB |
| Probe clearance in the tube | 1.3 mm radial | 24 mm probe in 26.6 mm bore | R10 at risk |
| Hanging loads at 60 m | 35 N cable (factor 11.5); 264 N tube (factor 58) | Dry, worst case | R2 met |
| WellSense parts per well | $187.60 | bom/bom.csv, 30 m probe depth | R12 not met ($180) |
| With FieldNode core | $313.60 | Adds line 8 ($126.00, FND-CAL-001) | Counted in the FieldNode repo (DDR-001, D1) |
| Depth-dependent cost | $1.80 per metre | Cable plus access tube | Budget holds to 25.8 m |

## Key design choices

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (WLS-DDR-001).

- **Vented 4 to 20 mA transducer rather than an absolute-pressure sensor with barometric compensation (D2).** The current loop is robust over long cables and the reading needs no compensation. The costs are desiccant maintenance at the vent and a 24 V boost, since the loop needs more than FieldNode's 12 V rail. A sealed absolute sensor with RS-485 and a surface barometer is kept as a variant.
- **0 to 10 m range (D3),** with a 0 to 20 m variant for wells whose seasonal swing plus drawdown exceeds 9 m.
- **Own access tube where a pump is present (D4).** Standard practice to protect the probe and the pump; also the hardest part to fit in an existing well (R10 at risk). The tube ends above the pump.
- **FieldNode as the core (D8).** Reuses the lab's shared enclosure, solar charging, storage and radio, so WellSense designs only the well side. The interface board connects to sensor port 1 (switched 12 V rail and I2C); the pinout is still open in FieldNode (FND-DDR-001, O2). A battery-only node remains a question for the FieldNode project (DDR-001, O2).
- **Manual tape as the reference (D6).** A shared electric tape sets the datum and the two-point calibration at installation and checks drift each quarter.
- **Levels only (D7).** No camera, audio or pump data; the dashboard shows water level so that sharing the data carries little risk.

## Safety

> **Safety:** Drinking water. Anything lowered into a supply well can contaminate it. Disinfect the probe, cable and tube before installation (for example with a chlorine solution as local water authorities advise), use only materials suitable for drinking water contact, and keep the wellhead sealed so surface water, insects and animals cannot enter. Involve the well owner or water authority before opening a public supply well.

> **Safety:** Electrical and pump hazards. Many wells contain a submersible pump on mains power. Isolate and lock off the pump supply before working at the wellhead, and keep the logger wiring separate from the pump cable. WellSense itself runs at 24 V or less (extra-low voltage).

> **Safety:** Lithium cell. The FieldNode core contains a lithium iron phosphate cell of about 19 Wh; follow the FieldNode safety notes on fusing and charging temperature limits.

> **Safety:** Working at an open well. An open dug well or large borehole is a fall and drowning hazard, especially for children. Never leave a wellhead open, and cover large-diameter wells while working.

> **Safety:** Lifting and cable handling. A long cable with a probe and tube can be heavy; lower it slowly with two people so it does not run away into the well, and never let the cable carry more than the rated load of its strain member.

## Open questions

- [ ] Access tube bore: keep 1 in and require a probe of 22 mm or less, or use 1-1/4 in where the casing allows? Proposed, awaiting Amish (see `docs/REVIEW.md`).
- [ ] Can an access tube be added beside an installed pump without pulling it? Only an installation trial can tell.
- [ ] Real long-term drift of low-cost vented transducers; is a quarterly tape check enough?
- [ ] Which drinking water material certifications can low-cost suppliers show for cable, seals and probe?
- [ ] How should the dashboard present drawdown so that non-specialists read it correctly? To be answered in co-design.
- [ ] Protection of the surface cable run against livestock, flooding and tampering (R16). Proposed, awaiting Amish.
- [ ] First partner and region for co-design (DDR-001, O1).

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
