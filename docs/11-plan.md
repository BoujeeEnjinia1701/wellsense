---
doc_id: WLS-PLN-001
title: WellSense project plan
project: WellSense
doc_type: Project plan
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First issue (kit 1.9.1 upgrade) at stage P3
---

# WellSense project plan

WellSense is at stage P3 (design outputs, TRL 3): the design is constructable, drawn, priced and planned for a prototype build, and every concept option is modelled at detail level D3. The next gate is Amish's concept decision between options A and C (WLS-DDR-005), with P4 (verification, TRL 4) on hold while the portfolio cap is P3. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Problem and users | Project lead | WLS-PRB-001 with users and stakeholder tables | Done (v0.7); co-design not started |
| STEM check | Design lead | WLS-STM-001 and `docs/04-calcs/stem_check.py` | Open: S7, S10 and S21 need TRL 4 data; fixes D-S1 to D-S4 made |
| Concept options | Design lead | WLS-OPT-001, `cad/src/model.py` options A to C at D3 | Done; choice awaiting Amish (WLS-DDR-005) |
| Requirements and traceability | Design lead | WLS-URS-001, WLS-PRS-001, WLS-RTM-001 | Done; targets to revise in co-design |
| Calculations | Design lead | WLS-CAL-001 v0.6 | Done for TRL 3 |
| CAD and drawings | Design lead | `cad/src/model.py`, `cad/fidelity.json` (D3), STEP, WLS-DWG-001 | Done |
| Build plan | Design lead | WLS-BLD-001 | Done (plan only; no build at TRL 3) |
| Regulatory, feasibility, risk, market | Project lead | WLS-REG-001, WLS-FEA-001, WLS-RSK-001, WLS-MKT-001 | Done (first issue); certificates to assess |
| Electronics interface | Electronics lead | Interface board from bought modules; FieldNode pinout signed off (WLS-DEC-001) | Designed on paper; no PCB at TRL 3 |
| Firmware and dashboard | Software lead | FieldNode sensor driver, conversion, dashboard (PR-013) | Not started (TRL 4 and later; firmware only as a labelled sketch before then) |
| Partner and co-design | Project lead | Approach ACWADAM; co-design sessions | Not started |
| Renders and storefront | Coordinator (studio machine) | `media/options.png` (Cycles), product renders from `cad/src/product_model.py`, cards | Awaiting the coordinator's render run |

## Resources needed

Table 2. Resources (estimates; no money is committed while the portfolio is capped at TRL 3).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Co-design partner time (field team) | Well sizes, site access, co-design sessions, dashboard language | 3 to 5 days | To agree with the partner |
| Prototype parts, one logger | Build to WLS-BLD-001 (TRL 4, on hold) | Parts only | 264.40 at 30 m plus 139.00 for the FieldNode core (BOM) |
| Shared electric tape meter | Datum, calibration and checks (BOM line 11) | One per partner | 80.00 (BOM estimate) |
| Workshop time | Build and bench check (TRL 4, on hold) | About 2 days for two people | Volunteer or partner |
| Drinking-water certificates | Supplier documents for probe, cable, HDPE, EPDM (PR-009) | Supplier enquiries | To assess |
| Test laboratory or university | Side-by-side accuracy and drift record (PR-004, PR-005) | 3 to 12 months of field record | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB with users and stakeholders, STM, OPT, REG, FEA, PLN | Met |
| P1 Definition | URS, PRS draft, RSK with hazard analysis, MKT | Met |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR, STEM check closed | Met except the STEM check, which stays open on S7, S10 and S21 (TRL 4 data) and the concept choice (awaiting Amish) |
| P3 Design outputs | Model, STEP, DWG, priced BOM, BLD, DEC, design FMEA, traceability complete | Met (2026-10-25, kit 1.9.1) |
| P4 Verification | Bench and field tests (TST), verification report | On hold (TRL cap 3) |
| P5 Validation | Field trial with the partner, certification status | On hold |
| P6 Commercialization | Launch with a named deployment partner | On hold |

## Next steps and decision requested

1. **Decision requested of Amish (O-1):** choose the concept to carry forward, option A (current design) or option C (acoustic sounder), which scored within 10 % (173 against 164; WLS-OPT-001, WLS-DDR-005). Recommendation: none, as the rule asks; the repo stays on A meanwhile.
2. Review the four fixes made under the standing instruction (WLS-DEC-001 D-S1 clevis pin, D-S2 drift test, D-S3 span from the probe's certificate, D-S4 loop fuse); any can be reversed.
3. Approach ACWADAM (decided 2026-10-02) and ask for well sizes and a site with a pump.
4. Ask suppliers for drinking-water certificates (PR-009) and a quote for a 22 mm, 0.25 % class vented probe.
5. When the cap rises: TRL 4 bench build and a side-by-side tape record (PR-004, PR-005), and an installation trial beside a pump (PR-010, PR-011).

## References

Every source cited in this repo's documents, Chicago style.

- Beddows, Patricia A., and Edward K. Mallon. "Cave Pearl Data Logger: A Flexible Arduino-Based Logging Platform for Long-Term Monitoring in Harsh Environments." *Sensors* 18, no. 2 (2018): 530. https://www.mdpi.com/1424-8220/18/2/530.
- Bureau of Indian Standards. *IS 10500:2012, Drinking Water: Specification (Second Revision).* https://www.bis.gov.in/other/DrinWatIS10500.pdf.
- Central Ground Water Authority. *Guidelines to Regulate and Control Ground Water Extraction in India.* Notification S.O. 3289(E), 24 September 2020. https://www.mpcb.gov.in/sites/default/files/water-quality/standards-protocols/Ground_Water_NewGuidelinesNotifiedeng24092021102020.pdf.
- Cunningham, William L., and Charles W. Schalk. *Groundwater Technical Procedures of the U.S. Geological Survey.* Techniques and Methods 1-A1. Reston, VA: U.S. Geological Survey, 2011. https://pubs.usgs.gov/tm/1a1/.
- European Union. Directive (EU) 2020/2184 on the Quality of Water Intended for Human Consumption. https://www.legislation.gov.uk/eudr/2020/2184/article/11.
- Food and Agriculture Organization of the United Nations. *Smallholders and Sustainable Wells: A Retrospect: Participatory Groundwater Management in Andhra Pradesh (India).* Rome: FAO, 2013. https://www.fao.org/4/i3320e/i3320e.pdf.
- Jasechko, Scott, Hansjörg Seybold, Debra Perrone, Ying Fan, Mohammad Shamsudduha, Richard G. Taylor, Othman Fallatah, and James W. Kirchner. "Rapid Groundwater Decline and Some Cases of Recovery in Aquifers Globally." *Nature* 625 (2024). https://www.nature.com/articles/s41586-023-06879-8.
- Kinsler, Lawrence E., Austin R. Frey, Alan B. Coppens, and James V. Sanders. *Fundamentals of Acoustics.* 4th ed. New York: Wiley, 2000.
- McCoy, J. N., A. L. Podio, and K. L. Huddleston. "Acoustic Determination of Producing Bottomhole Pressure." *SPE Formation Evaluation* 3, no. 3 (1988).
- Perrone, Debra, and Scott Jasechko. "Deeper Well Drilling an Unsustainable Stopgap to Groundwater Depletion." *Nature Sustainability* 2 (2019). https://www.nature.com/articles/s41893-019-0325-z.
- Standards Council of Canada. "NSF/ANSI/CAN 61 - 2023." https://scc-ccn.ca/standardsdb/standards/4032142.
- UNESCO. *The United Nations World Water Development Report 2022: Groundwater: Making the Invisible Visible.* Paris: UNESCO, 2022. https://www.unesco.org/reports/wwdr/2022/en.
- World Health Organization. *Guidelines for Drinking-Water Quality: Fourth Edition Incorporating the First and Second Addenda.* Geneva: WHO, 2022. https://www.who.int/publications/i/item/9789240045064.
- Standards and practice references named in WLS-STM-001 and WLS-REG-001: AWWA C654-13 (disinfection of wells), ASTM D1785 (PVC pipe), IEC 60529 (IP code), IEC 61140 (protection against electric shock), ISO 4373:2022 (hydrometry, water level measuring devices), HSE INDG143 (manual handling), Texas Instruments ADS1115 datasheet, Semtech AN1200.13 (LoRa time on air).
- Market benchmarks in WLS-MKT-001: Instrumart (HOBO U20L), Fondriest (Solinst Levelogger 6), Acorn Controls on IndiaMART (DWLR), all checked 2026-10-25.
