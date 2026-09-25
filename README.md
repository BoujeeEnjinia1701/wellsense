# WellSense

**Area:** Water Security · **Status:** Concept · **Prototype budget:** about $180 USD · **Difficulty:** 2 of 5

A well and borehole water level logger with a submersible pressure sensor and FieldNode telemetry, showing seasonal drawdown so communities can manage shared groundwater.

## Concept rationale

Measurement is the first step to shared management of an aquifer.

## Burning platform

Groundwater depletion threatens farming and drinking water in many of the world's most populous regions.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. It extends the lab's water security work.

## Problem

Groundwater is falling in many regions, yet most wells have no measurement, so over-pumping is noticed only when wells run dry.

## Concept

A well and borehole water level logger with a submersible pressure sensor and FieldNode telemetry, showing seasonal drawdown so communities can manage shared groundwater.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Submersible pressure transducer and vented cable
- Barometric reference sensor
- FieldNode core
- Wellhead cap mount
- Dashboard

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Keep the wellhead sealed to protect water quality and use food-grade materials for anything in the well.

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Extending strong areas set.
