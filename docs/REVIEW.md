# Review note: WellSense

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (WLS-PRB-001 v0.2): problem with cited figures, users and context, constraints, prior work, out of scope, open questions; co-design checklist kept.
- `docs/03-requirements.md` (WLS-REQ-001 v0.2): 16 measurable requirements (R1 to R16) with targets, verification and a status column that marks what is not met.
- `docs/02-concept.md` (WLS-PRC-001 v0.2): how it works, numbered components, first-order numbers with assumptions, design choices, safety section, open questions.
- `cad/src/concept_media.py`: massing model of a 150 mm borehole with an existing pump and riser (grey, not in kit), the WellSense parts in color with BOM numbers, and the FieldNode core on a post. The hero is re-rendered with the soil cut open; the cutaway is a broken section (wellhead and lower borehole side by side) so the 24 mm probe is readable. The borehole is shortened for display and captions say so.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` (callouts 1 to 10), `cutaway.png`, `flow.png` (data flow, estimated values), `model.glb` and `viewer.html`. Temporary `_views*` folders are removed by the script.
- `bom/bom.csv`: 12 rows with indicative prices, rows 1 to 10 matching the exploded view; `bom/bom-notes.md` explains what is and is not in the per-well cost.
- `README.md`: hero and links line, concept rationale, burning platform, where it could be used (by industry and by country or region), what sparked the idea, and updated concept, components and safety.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch and problem remain accurate.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Range | 0 to 10 m of water (98 kPa) | R1 met |
| Resolution | about 0.5 mm | R3 met |
| Datasheet accuracy | about ±50 mm (0.5 % of full scale) | **R4 (±20 mm) not met** |
| Sensor energy | about 18 mWh a day at 15 min, about 0.6 % of FieldNode's sensor budget | R8 met |
| Storage | about 0.3 MB a year | R7 met |
| WellSense parts per well (30 m) | about $170 | R12 met with FieldNode counted separately |
| Complete logger with FieldNode core | about $296 | **Over the $180 budget** |
| Depth-dependent cost | about $1.80 per metre | |

Requirements not met or at risk:

- **R4 accuracy not met:** about ±50 mm on datasheet against ±20 mm; needs a 0.25 % sensor plus two-point field calibration, unverified.
- **R5 drift unverified and at risk:** long-term drift of low-cost transducers is not published.
- **R9 water safety not met on evidence:** drinking water certification of low-cost cable and seals is unknown.
- **R10 pump compatibility at risk:** fitting an access tube may require pulling the pump.
- **R12 not met if the FieldNode core is counted** in the WellSense budget.
- **R16 tamper resistance at risk:** the cable run from wellhead to post is exposed in the concept.
- R11 and R13 are unverified (installation trial and dashboard not started).

### Proposed, awaiting Amish

1. **Budget treatment of FieldNode.** Options: (a) count the FieldNode core in the FieldNode repo and hold WellSense to $180 for its own parts (about $170 now); (b) raise `budget_usd` to about $300 for a complete logger; (c) cut cost with a battery-only node or cheaper transducer. Recommendation: (a), with the complete cost stated in the README as done here. `budget_usd` is unchanged.
2. **Sensor type.** Option A: vented 4 to 20 mA gauge transducer (proposed; simple, no compensation, needs desiccant care). Option B: sealed absolute sensor with RS-485 and surface barometric compensation (no vent; adds error and a digital probe). Recommendation: A for the first build, with B kept as a variant.
3. **Range.** 0 to 10 m (recommended; better resolution and accuracy) or 0 to 20 m for wells with large pumping drawdown.
4. **Access tube** fitted wherever a pump shares the casing (recommended), versus hanging the probe freely where there is no pump.
5. **Default interval** of 15 min, with 1 min during pumping tests.
6. **Manual tape check** each quarter as part of the method, with one shared tape per community or partner.
7. **Data ownership:** levels only, community controls sharing, CSV export.
8. **First partner and region** for co-design (an Indian farmer group, an African handpump programme, or a US groundwater agency).
9. **Battery-only FieldNode variant** without the panel, given the very small load; to be discussed with the FieldNode project, not changed here.

### Safety concerns

- Contamination of a drinking water well by the probe, cable, tube or an unsealed wellhead.
- Mains-powered submersible pumps at the wellhead; isolation and lock-off before work.
- Open wells as fall and drowning hazards, especially for children.
- Lithium iron phosphate cell in the FieldNode core.
- Heavy cable and probe running away into the well during installation.

### Problems and notes

- The web search budget for this session ran out before searching; all citations were checked by fetching the source pages directly. Figures for community groundwater programmes in India (for example Atal Bhujal Yojana) and for Mexico could not be verified, so they were left out.
- The transducer and cable prices are estimates from general market knowledge, not quotes.
- The exploded view shows the tube cap (item 5) and probe (item 1) small at full-well scale; the cutaway shows both clearly.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 to 3. If approved, run `/advance-trl3` to check accuracy, drift allowance, energy and cable load by calculation and produce the parametric model and drawing sheet.
