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

### Proposed, awaiting Amish (status updated 2026-09-25: items 1 to 7 decided; 8 and 9 still open)

1. **Budget treatment of FieldNode.** Options: (a) count the FieldNode core in the FieldNode repo and hold WellSense to $180 for its own parts (about $170 now); (b) raise `budget_usd` to about $300 for a complete logger; (c) cut cost with a battery-only node or cheaper transducer. Recommendation: (a), with the complete cost stated in the README as done here. `budget_usd` is unchanged. **Decided by Amish, 2026-09-25: go with recommendation** (WLS-DDR-002).
2. **Sensor type.** Option A: vented 4 to 20 mA gauge transducer (proposed; simple, no compensation, needs desiccant care). Option B: sealed absolute sensor with RS-485 and surface barometric compensation (no vent; adds error and a digital probe). Recommendation: A for the first build, with B kept as a variant. **Decided by Amish, 2026-09-25: go with recommendation** (WLS-DDR-002).
3. **Range.** 0 to 10 m (recommended; better resolution and accuracy) or 0 to 20 m for wells with large pumping drawdown. **Decided by Amish, 2026-09-25: go with recommendation** (WLS-DDR-002).
4. **Access tube** fitted wherever a pump shares the casing (recommended), versus hanging the probe freely where there is no pump. **Decided by Amish, 2026-09-25: go with recommendation** (WLS-DDR-002).
5. **Default interval** of 15 min, with 1 min during pumping tests. **Decided by Amish, 2026-09-25: go with recommendation** (WLS-DDR-002).
6. **Manual tape check** each quarter as part of the method, with one shared tape per community or partner. **Decided by Amish, 2026-09-25: go with recommendation** (WLS-DDR-002).
7. **Data ownership:** levels only, community controls sharing, CSV export. **Decided by Amish, 2026-09-25: go with recommendation** (WLS-DDR-002).
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

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to go through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item that carried a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (WLS-DDR-001 v0.1, status proposed): eight items adopted as recommended for TRL 3, open for Amish's review (D1 to D8), and two left open (O1, O2).
- `docs/04-calcs/01-sizing.md` (WLS-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: range and resolution, loop supply and energy, accuracy error budget and drift, fit in the casing and hanging loads, storage and airtime, vent desiccant, installation time and cost, with a status for every requirement. The script imports the model, reads the BOM and `project.yaml`, prints every number the note quotes and writes `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d model (existing casing, pump and riser as grey context; access tube with slots and plug, probe, seal plate with glands, tube cap and hanger, vented cable, post and footing, junction box, interface board, barometric sensor, and a FieldNode core massing with dimensions copied from the FieldNode model). The borehole is shortened for display; the 30 m design case lives in `DESIGN`. Exports `cad/step/` and `cad/stl/` for `wellsense-assembly`, `wellsense-wellhead`, `wellsense-probe` and `wellsense-post`.
- `cad/src/sheets.py` and `cad/drawings/WLS-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:25 above z = -700 mm, with a 1:5 detail of the probe zone, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". WLS-DWG-001 was free because the concept blueprint is WLS-DWG-010.
- `bom/bom.csv` (13 lines, all priced with a supplier or supplier type) and `bom/bom-notes.md`: $187.60 for WellSense parts against the $180 budget.
- `cad/src/concept_media.py` now builds from the model; all of `media/` was re-rendered and every image checked; temporary `_views` folders are deleted by the script.
- WLS-PRB-001, WLS-PRC-001 and WLS-REQ-001 revised to v0.3; `README.md` (badge, TRL line, links, concept figures, key components) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. The pitch and problem lines are unchanged, since no rewording was recommended. PDFs rebuilt in `docs/pdf/`.

### Requirement status (WLS-CAL-001, Table 3)

2 not met, 4 at risk, 3 not verifiable at TRL 3, 7 met.

| ID | Status | Key number |
| --- | --- | --- |
| R9 Water safety | **Not met** (no evidence) | No drinking water certificate in hand for low-cost cable, seals or probe |
| R12 Cost | **Not met** | $187.60 at 30 m against $180; met to 25.8 m; $313.60 with the FieldNode core |
| R4 Accuracy | At risk | 12.5 mm RSS, 27.1 mm worst case after two-point calibration (0.25 % class); 0.5 % class misses |
| R10 Pump compatibility | At risk | 1.3 mm radial clearance for a 24 mm probe in a 1 in tube; fitting may need the pump pulled |
| R15 Environment | At risk | FieldNode rated to 45 °C ambient against WellSense's 55 °C |
| R16 Tamper resistance | At risk | Cable exposed from the wellhead to the post |
| R5, R11, R13 | Not verifiable at TRL 3 | Drift unknown; install 120 min estimate at the limit; dashboard not started |
| R1, R2, R3, R6, R7, R8, R14 | Met | 98.07 kPa; factors 11.5 and 58 at 60 m; 0.52 mm; 1.12 MB a year; 38.2 mWh/day (1.6 %) |

Key numbers and changes from TRL 2: the FieldNode 12 V rail leaves the transducer 7.56 V against its 12 V minimum, so the interface board gains a 24 V boost (20.16 V at the probe); energy per reading rises from 0.66 J to 1.43 J and daily energy from 18 to 38.2 mWh; storage uses FieldNode's 32-byte record (1.12 MB a year, not 0.3 MB); parts rise from about $170 to $187.60.

### Decisions recorded (WLS-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction (now decided by Amish, 2026-09-25: go with recommendation; see WLS-DDR-002): D1 budget covers WellSense parts, FieldNode core costed in its own repo, `budget_usd` unchanged (R12 restated); D2 vented 4 to 20 mA transducer, absolute RS-485 sensor as a variant; D3 0 to 10 m range, 0 to 20 m variant; D4 access tube wherever a pump shares the casing; D5 15 min default, 1 min in pumping tests; D6 quarterly manual tape check with a shared tape; D7 levels only, community controls sharing, CSV export; D8 FieldNode as the core. Detail choices within D2 and D8 that Amish should see: 24 V boost and 3.3 V regulator on the interface board, 0.25 % class probe, two-point calibration by lifting the probe 1 m, a longer post for FieldNode's 1.75 m mounting height, and a footing concrete line.

### Still awaiting Amish (status updated 2026-09-25: items 3 to 7 decided; O1 and O2 still open)

1. **O1, first partner and region for co-design.** No preference stated.
2. **O2, battery-only FieldNode variant.** For discussion with the FieldNode project; no recommendation to adopt.
3. **New, cost at the design depth (R12).** Options: (a) keep $180 and state R12 at a 25 m design depth; (b) raise `budget_usd` to $190 to cover a 30 m design well, with $1.80 per metre beyond; (c) cost down, for example a cheaper probe (fails R4) or no access tube where there is no pump. Recommendation: (b), $190. Not applied; `budget_usd` stays at $180. **Decided by Amish, 2026-09-25: go with recommendation** (WLS-DDR-002).
4. **New, access tube bore (R10).** Options: (a) keep the 1 in tube and require a probe of 22 mm or less; (b) 1-1/4 in tube, which takes 24 to 28 mm probes but fits beside a centered riser only in 200 mm casing. Recommendation: (a). Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (WLS-DDR-002).
5. **New, surface cable protection (R16).** Options: (a) galvanized conduit from the seal plate to the junction box, about $10 (estimate); (b) a buried conduit; (c) accept the exposed run. Recommendation: (a). Not applied and not in the BOM total. **Decided by Amish, 2026-09-25: go with recommendation** (WLS-DDR-002).
6. **New, hot-site rating (R15).** FieldNode is rated -20 to +45 °C ambient, and its own review recommends a sun shield for hot-climate sites. Options: (a) keep R15 at 55 °C and require the FieldNode shield at hot sites; (b) restate R15 to FieldNode's range. Recommendation: (a), following FieldNode's item 4. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (WLS-DDR-002).
7. **New, pumping-test uplinks.** A 1 min test batch uses 31.6 s a day at SF9, over public fair use. Recommendation: on a public network send every 30 min during a test; use a TwinKit gateway where possible. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (WLS-DDR-002).

### Cross-repo consistency

- FieldNode (read-only): cost $126.00, 12 V switched rail, M12 port with the candidate pinout (pin 1 rail, 2 and 4 data, 3 ground, 5 analog), 32-byte records in 16 MB flash, 90 % rail efficiency and the 100 mW allowance (115 mW ceiling) are all used as FieldNode states them. WellSense fits either allowance (1.6 % or 1.4 %).
- Conflict 1: WellSense R15 asks for 55 °C above-ground parts; FieldNode is rated to 45 °C ambient and misses its interior temperature target in hot sun (FND-CAL-001). Recorded here as item 6; FieldNode not edited.
- Conflict 2: the WellSense loop needs 24 V, which a FieldNode port does not offer; the boost sits on the WellSense interface board, so FieldNode needs no change. The FieldNode port pinout is still open (FND-DDR-001, O2); WellSense assumes I2C on port 1.
- TwinKit is assumed as the private gateway, as FieldNode does. No other shared component is used. No other repo was edited.

### Safety concerns

- Drinking water contamination by the probe, cable, tube, seal plate or an unsealed wellhead; R9 has no evidence yet. Disinfection and certified materials remain conditions of any installation.
- Mains-powered submersible pumps at the wellhead: isolate and lock off before work; keep logger wiring apart from the pump cable. WellSense itself is extra-low voltage (24 V boost).
- A tube lowered past an installed riser may snag the pump cable and damage its insulation; this is part of the R10 risk.
- Open wells as fall and drowning hazards; heavy cable and tube (up to 264 N of tube at 60 m) running away into the well during installation; the seal plate needs a tube clamp.
- Lithium iron phosphate cell and heat in the FieldNode core, as in the FieldNode review.

### Gaps and notes

- Citations: the TRL 2 note flagged no unchecked citations. It left out figures for Atal Bhujal Yojana and Mexico; one WebFetch attempt (World Bank press page 404; the scheme's site timed out) did not verify them, so they stay out.
- Transducer, cable, tube and board prices are estimates, not quotes. The accuracy budget's largest term (nonlinearity, 0.10 % of full scale) is a typical value.
- The kit's cutaway was not used (`cut=False`, as at TRL 2); `concept_media.py` renders its own broken section of the wellhead and the probe zone. The exploded view still shows the small wellhead parts (callouts 4, 5, 6 and 7) small at full-installation scale; the cutaway and drawing detail A show them clearly.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. No test, build or firmware material exists.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on items 3 to 7 above, on O1 and O2, and on the adopted items D1 to D8. For the record only, TRL 4 would need: a bench build of the interface board with a chosen transducer; a lab test report (TST, `environment: lab`) covering calibration and linearity against a water column, loop supply at the far end of 60 m of cable, temperature drift of the shunt and ADC, and probe fit in the chosen access tube; supplier drinking water certificates for wetted parts; and build log entries. None of this has been started.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item in this note and in WLS-DDR-001 that carried a recommendation is now decided by Amish, 2026-09-25: go with recommendation. The decisions and their effects are recorded in `docs/decisions/0002-recommendations-accepted.md` (WLS-DDR-002 v0.1).

### Decisions applied and what changed

| Decision | Before | After |
| --- | --- | --- |
| D1 to D8 (WLS-DDR-001) | Adopted for TRL 3, open for review | Decided; no design change beyond the items below |
| Cost at the design depth, option (b) | `budget_usd` $180; R12 at $180 | `budget_usd` $190 for a 30 m design well, $1.80 per metre beyond; R12 restated |
| Access tube bore, option (a) | 24 mm probe, 1.3 mm radial clearance in the 1 in tube | Probe 22 mm or less, 2.3 mm radial clearance; model, BOM line 1, R10 updated |
| Surface cable protection, option (a) | Cable exposed from the tube cap to the junction box; not in the BOM | Galvanized 1/2 in conduit, BOM line 14, $10.00; modeled and on the drawing |
| Hot-site rating, option (a) | R15 at risk on the FieldNode 45 °C rating | R15 kept at 55 °C with FieldNode's sun shield required at hot sites (48.5 to 52.2 °C inside at 45 °C, FND-CAL-001 v0.2); still at risk above 45 °C ambient |
| Pumping-test uplinks | 15 min batches, 31.6 s a day at SF9, over public fair use | Every 30 min on a public network: 22.7 s a day; 15 min on a TwinKit gateway; R6 text updated. Firmware on hold (TRL 4) |
| WellSense parts at 30 m | $187.60 ($7.60 over $180); $313.60 with FieldNode | $197.60 ($7.60 over $190); $323.60 with FieldNode; $331.60 with the hot-site shield |

Files changed: `project.yaml` (`budget_usd`, evidence list); `bom/bom.csv` (line 1 respecified, line 14 added) and `bom/bom-notes.md`; `cad/src/model.py` (probe 22 mm, `conduit` part) and re-exported STEP and STL; `cad/src/sheets.py` and WLS-DWG-001 at Rev P2; `cad/src/concept_media.py` and all of `media/` re-rendered (hero, blueprint, exploded and cutaway checked; `_views` folders deleted); `docs/04-calcs/sizing.py`, `results.csv` and WLS-CAL-001 v0.2; WLS-PRB-001 v0.4, WLS-PRC-001 v0.4, WLS-REQ-001 v0.4, WLS-DDR-001 v0.2, new WLS-DDR-002 v0.1; `README.md` (budget, concept figures, components, and a rewritten "What sparked the idea" citing the Andhra Pradesh Farmer Managed Groundwater Systems project). All PDFs rebuilt, and all generated files now carry designmolecule.com.

### Requirement status (WLS-CAL-001 v0.2, Table 3)

2 not met, 4 at risk, 3 not verifiable at TRL 3, 7 met.

| ID | Status | Key number |
| --- | --- | --- |
| R9 Water safety | **Not met** (no evidence) | No drinking water certificate in hand for low-cost cable, seals or probe |
| R12 Cost | **Not met** | $197.60 at 30 m against $190 ($187.60 without the conduit); met to 25.8 m |
| R4 Accuracy | At risk | 12.5 mm RSS, 27.1 mm worst case |
| R10 Pump compatibility | At risk | 2.3 mm radial clearance with a 22 mm probe; fitting a tube may need the pump pulled |
| R15 Environment | At risk | Shielded FieldNode core rated to 45 °C ambient against 55 °C |
| R16 Tamper resistance | At risk | Cable now in conduit; locking of the seal plate, tube cap and box not specified |
| R5, R11, R13 | Not verifiable at TRL 3 | Drift unknown; install 120 min estimate; dashboard not started |
| R1, R2, R3, R6, R7, R8, R14 | Met | R6 now with the 30 min public-network rule (22.7 s a day) |

### Still awaiting Amish

1. **O1, first partner and region for co-design.** No preference stated.
2. **O2, battery-only FieldNode variant.** No recommendation to adopt.
3. **New, N1, cost with the conduit.** The $190 budget and the $10.00 conduit together give $197.60 at 30 m. Options: (a) raise `budget_usd` to $200; (b) keep $190 and state R12 at a 25 m design depth; (c) keep $190 and fit the conduit only where livestock or tampering is likely. No option applied. **Decided by Amish, 2026-09-26: budget set to $200** (WLS-DDR-002).

### Cross-repo actions (other repos not edited)

- **FieldNode:** confirm how the shielded core behaves at 55 °C ambient, or state the limit, since WellSense R15 asks for 55 °C and FieldNode is rated to 45 °C ambient.
- **FieldNode:** WellSense now cites only the published 100 mW sensor allowance (no longer 115 mW), and uses the sun shield (BOM line 14, $8.00) at hot sites.
- **FieldNode:** the sensor port pinout (FND-DDR-001, O2) is still open; WellSense assumes I2C on port 1.

### TRL 4

TRL 4 remains on hold by Amish's instruction. `trl` and `trl_target` stay at 3. The firmware uplink rule, the interface board build, the probe fit test, supplier drinking water certificates and any purchasing are decided in principle where recommended but have not been started.

## Session 2026-09-26: budget approved

Amish wrote on 2026-09-26: "i approve all the budget items." Budget set to $200 to cover the priced BOM: decided by Amish, 2026-09-26. This closes N1.

- `project.yaml` `budget_usd` $190 to **$200**. The priced WellSense parts are unchanged at $197.60 at a 30 m probe depth (lines 1 to 7, 9, 10, 13 and 14; the FieldNode core and the shared tape stay outside the budget).
- R12 (cost): target $190 to $200; status **Not met to Met**, $2.40 under, and the budget now holds to a 31.3 m probe depth (was 25.8 m). Requirement status is now 1 not met (R9), 4 at risk (R4, R10, R15, R16), 3 not verifiable at TRL 3 (R5, R11, R13), 8 met.
- Files changed: `project.yaml`, `README.md`, WLS-PRB-001 v0.5, WLS-PRC-001 v0.5, WLS-REQ-001 v0.5, WLS-CAL-001 v0.3 (`sizing.py` and `results.csv` rerun; R12 status now computed from the budget), WLS-DDR-002 v0.2, `bom/bom-notes.md`, `cad/src/concept_media.py` (blueprint key figure); media and PDFs regenerated, temporary `media/_views*` folders deleted.
- Still awaiting Amish: O1 (co-design partner and region) and O2 (battery-only FieldNode variant). `trl: 3` and `trl_target: 3` are unchanged; TRL 4 remains on hold.
