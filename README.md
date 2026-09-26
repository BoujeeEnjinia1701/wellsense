# WellSense

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Water Security · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** $200 USD for WellSense parts, FieldNode core costed separately · **Difficulty:** 2 of 5

A well and borehole water level logger with a submersible pressure sensor and FieldNode telemetry, showing seasonal drawdown so communities can manage shared groundwater.

![WellSense concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement WLS-DWG-001 (PDF)](cad/drawings/WLS-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Measurement is the first step to shared management of an aquifer. A vented pressure transducer hung in a well gives a continuous water level record with millimetre resolution, and it is the same method groundwater agencies use ([USGS, 2011](https://pubs.usgs.gov/tm/1a1/)). WellSense puts that method in the wells people already draw from, on the lab's shared FieldNode core, so the only new parts are the probe, an access tube, a wellhead seal and a small interface board. A manual tape check each quarter keeps the record honest.

It is open and garage-buildable because the communities that share falling aquifers are rarely the ones that own monitoring equipment. Commercial loggers are closed and costly; a design built from plumbing parts, a stock industrial transducer and off-the-shelf modules can be made, checked and repaired locally, and its data belong to the community that hosts the well.

## Burning platform

Groundwater provides about half of the water withdrawn for domestic use worldwide, including drinking water for most rural people, and about 25 % of irrigation water ([UNESCO, WWDR 2022](https://www.unesco.org/reports/wwdr/2022/en)). Across 1,693 aquifer systems, rapid declines of more than 0.5 m a year are widespread in the twenty-first century, and declines have accelerated over four decades in 30 % of regional aquifers ([Jasechko et al., Nature, 2024](https://www.nature.com/articles/s41586-023-06879-8)).

When levels fall unmeasured, the response is to drill deeper: in the United States, typical wells are being built deeper 1.4 to 9.2 times more often than shallower, which the authors call an unsustainable stopgap ([Perrone and Jasechko, 2019](https://www.nature.com/articles/s41893-019-0325-z)). The same global study shows that levels recover where pumping is regulated, as in the Bangkok basin, so a shared record that people trust is worth having early.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Rural water supply and WASH programmes | Warn handpump and borehole committees before the static level nears the pump intake |
| Irrigated agriculture | Let farmer groups see seasonal drawdown in their own wells and agree pumping or cropping rules |
| Groundwater agencies and utilities | Densify official networks with low-cost community wells between observation boreholes |
| Drought early warning | Feed well levels into local drought indicators alongside rainfall |
| Mining, construction and dewatering | Track the effect of dewatering on neighbouring wells |
| Education and research | Teach aquifer response to pumping, recharge and air pressure with open data |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| India | The largest groundwater user in the world, over a quarter of the global total; groundwater serves more than 60 % of irrigated agriculture and 85 % of drinking water supplies ([World Bank](https://www.worldbank.org/en/news/feature/2012/03/06/india-groundwater-critical-diminishing)). |
| Sub-Saharan Africa | Groundwater storage is estimated at more than 100 times annual renewable freshwater, and boreholes can support handpumps ([MacDonald et al., 2012](https://iopscience.iop.org/article/10.1088/1748-9326/7/2/024009)), yet about one in four handpumps is out of service at any time ([Foster et al., 2019, via IRC](https://www.ircwash.org/resources/functionality-handpump-water-supplies-review-data-sub-saharan-africa-and-asia-pacific)). |
| Iran and the Arabian Peninsula | Named among regions of rapid decline in the global synthesis, which also reports slowing decline in the Saq aquifer after policy changes ([Jasechko et al., 2024](https://www.nature.com/articles/s41586-023-06879-8)). |
| United States (California) | The 2014 Sustainable Groundwater Management Act requires local agencies to reach sustainability within 20 years under monitored plans ([California DWR](https://water.ca.gov/programs/groundwater-management/sgma-groundwater-management)). |
| Southeastern Spain | Aquifer declines there are too small in area for satellite gravity to detect, so they must be measured in wells ([Jasechko et al., 2024](https://www.nature.com/articles/s41586-023-06879-8)). |
| Thailand (Bangkok) | Levels that fell in the late twentieth century recovered after regulation ([Jasechko et al., 2024](https://www.nature.com/articles/s41586-023-06879-8)), a case for measuring and managing early. |

## What sparked the idea

The starting point was the Andhra Pradesh Farmer Managed Groundwater Systems project, launched in 2003 in seven drought-prone districts of southern India ([FAO](https://www.fao.org/land-water/overview/projects/previous-projects/andhra-pradesh-farmer-managed-groundwater-systems/en/)). There, farmers took fortnightly measurements of static and pumping water levels in their own wells, kept rain gauges, and used the numbers to draw up a crop-water budget before each winter season; about half a million farmers in 661 habitations took part ([FAO, *Smallholders and Sustainable Wells*, 2013](https://www.fao.org/4/i3320e/i3320e.pdf)). The project showed that people who share an aquifer will manage it when they can see the water level themselves. WellSense asks what that practice looks like with a continuous, low-cost record in place of a hand reading every two weeks, so that the daily pumping cycle and the seasonal decline are visible between visits.

## Problem

Groundwater is falling in many regions, yet most wells have no measurement, so over-pumping is noticed only when wells run dry. Design with, not for: requirements must come from co-design with the communities that share the aquifer, through a local partner.

## Concept

A well and borehole water level logger with a submersible pressure sensor and FieldNode telemetry, showing seasonal drawdown so communities can manage shared groundwater. A vented 4 to 20 mA transducer hangs in its own access tube beside the pump, a sealed wellhead plate keeps the well clean, and the lab's FieldNode core reads it every 15 minutes and sends the level over LoRaWAN to an open dashboard.

TRL 3 calculations ([WLS-CAL-001](docs/04-calcs/01-sizing.md)): 0.52 mm resolution; 12.5 mm accuracy by root sum square after a two-point tape calibration with a 0.25 % class probe, 27.1 mm worst case, so the ±20 mm target is at risk; a 24 V boost on the interface board, because FieldNode's 12 V rail cannot drive the loop; 38.2 mWh a day of sensor energy, 1.6 % of FieldNode's allowance; a 22 mm probe with 2.3 mm radial clearance in the 1 in access tube; and $197.60 in WellSense parts at a 30 m probe depth including a galvanized conduit over the surface cable, within the $200 budget ($323.60 with the FieldNode core). Eight of sixteen requirements are met on paper, including cost (R12); drinking water evidence (R9) is not. See the [design precis](docs/02-concept.md), [requirements](docs/03-requirements.md) and decision records [WLS-DDR-001](docs/decisions/0001-trl2-review-decisions.md) and [WLS-DDR-002](docs/decisions/0002-recommendations-accepted.md).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Vented submersible pressure transducer, 4 to 20 mA, 0 to 10 m, 0.25 % class, 22 mm diameter or less
- Vented cable with desiccant breather
- 25 mm PVC access tube, tube cap and cable hanger
- Wellhead seal plate with glands
- Galvanized conduit over the surface cable from the tube cap to the junction box
- 4 to 20 mA interface board with 24 V boost, and barometric reference sensor
- FieldNode core (shared lab node) on a mounting post set in a concrete footing, with FieldNode's sun shield at hot sites
- Open community dashboard, plus a shared manual water level tape for checks

The priced bill of materials is in [bom/bom.csv](bom/bom.csv). The parametric model is `cad/src/model.py`, with STEP and STL exports in `cad/step/` and `cad/stl/`.

## Safety

> Keep the wellhead sealed to protect water quality and use materials suitable for drinking water contact for anything in the well. Disinfect everything lowered into a supply well.
>
> Isolate and lock off any mains-powered pump before working at the wellhead. Never leave an open well unattended; open wells are a fall and drowning hazard.
>
> The FieldNode core contains a lithium iron phosphate cell; follow its fusing and charging limits.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (WLS-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `WLS-PRC-001/v1.0`.

## Credits

Designed by Amish Chadha. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for roles. To cite this design, use [CITATION.cff](CITATION.cff) (GitHub shows it as "Cite this repository").

AI assistance (Claude) was used to accelerate concept renders, prototype documentation and first-pass sizing calculations. Design direction and all decisions are Amish Chadha's, recorded in this repository's decision records (`docs/decisions/`).

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
