---
doc_id: WLS-REG-001
title: WellSense regulatory and standards register
project: WellSense
doc_type: Regulatory register
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First issue (kit 1.9.1 upgrade); drinking water rows reuse the Water Security focus-area research (StillStack, LumaFlow)
---

# WellSense regulatory and standards register

Which standards and regulations would apply to WellSense, where, and what is needed. Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. The first deployment region is India with a participatory groundwater partner (WLS-DEC-001), so Indian rows lead; international rows cover the open design wherever it is built. No certification is pursued while the portfolio is capped at TRL 3. Drinking water rows reuse the Water Security focus-area research cited in StillStack (SSK-REG-001) and LumaFlow (LMF-REG-001). Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | NSF/ANSI/CAN 61, drinking water system components, health effects | United States and Canada (often accepted as evidence elsewhere) | Contaminants that leach from materials in contact with drinking water | Every wetted part: probe body, vented cable jacket, PVC tube and end cap, HDPE seal plate, EPDM gasket and wraps (PR-009, STM S24) | Design lead with suppliers | To assess: no certificate in hand for the low-cost parts (PR-009 not met) |
| G2 | IS 10500:2012, drinking water specification (second revision), Bureau of Indian Standards | India | Acceptable and permissible limits for drinking water quality | Context: WellSense adds nothing to the water; its wetted parts must not move any parameter (G1); disinfection after installation (G5) | Partner and well owner | Applies as guidance |
| G3 | WHO Guidelines for Drinking-water Quality, 4th edition incorporating the first and second addenda (2022) | International (guidance) | Microbial and chemical guidance, including protection of groundwater sources and sanitary inspection of wells | Keeping the wellhead sealed (PR-009) and disinfecting anything lowered into a supply well | Design lead; partner | Applies as guidance |
| G4 | Directive (EU) 2020/2184, Article 11 (materials in contact with water for human consumption) | European Union | Hygiene requirements for materials and products in contact with drinking water | Only if WellSense is supplied for EU drinking water wells | Whoever places it on the market | Does not apply to the open design; certification needed later for any EU supply |
| G5 | AWWA C654-13, disinfection of wells | United States (practice reference) | Disinfecting wells and equipment put into them | Disinfection of the probe, cable, tube and seal before installation (STM S25, build plan safety stops) | Installer | Applies as practice reference; follow the local water authority where it differs |
| G6 | CGWA Guidelines to regulate and control ground water extraction in India, notification S.O. 3289(E), 24 September 2020 | India (pan-India where states do not regulate groundwater themselves) | No objection certificates for groundwater abstraction; piezometers for users drawing more than 10 m³/day, with a digital water level recorder from 51 m³/day and telemetry above 500 m³/day (Table 14.1) | Market context, not a requirement on community wells: shows the regulator already expects digital water level recorders; whether a WellSense unit could serve as a compliant recorder is to assess with CGWA | Project lead | To assess |
| G7 | ISO 4373:2022, hydrometry, water level measuring devices | International | Performance classes and test methods for water level measuring devices | A route to state WellSense's accuracy class at TRL 4 (PR-004, PR-005) | Design lead with a test laboratory | To assess (TRL 4 or later) |
| G8 | USGS Techniques and Methods 1-A1 (Cunningham and Schalk, 2011), groundwater technical procedures | United States (method reference) | Measuring well water levels with a steel tape, an electric tape and a submersible pressure transducer | The method WellSense follows: transducer for the record, tape for the datum and checks (PR-004, PR-005) | Design lead | Applies as method reference |
| G9 | IEC 60529, degrees of protection by enclosures (IP code) | International | Ingress protection ratings | Probe IP68, above-ground parts IP65 or better (PR-015); met on datasheets for bought parts | Design lead | Met by design (datasheets, to confirm at purchase) |
| G10 | IEC 61140, protection against electric shock | International | Extra-low voltage bands and protective measures | WellSense runs at 24 V DC or less (PR-018, STM S27); the pump's mains supply is separate and isolated before work (build plan safety stops) | Electronics lead | Met by design |
| G11 | Wireless Planning and Coordination Wing (WPC), Department of Telecommunications: licence-exempt use of 865 to 867 MHz and equipment type approval (ETA) for radio devices | India | Radio use and approval of the LoRaWAN radio in the FieldNode core | Carried by the FieldNode core on the IN865 band (WLS-DEC-001); WellSense adds no radio | FieldNode project | To assess (FieldNode repo) |
| G12 | Electromagnetic compatibility rules for the product's market (for example the EU EMC Directive 2014/30/EU or US FCC Part 15) | European Union; United States | Emissions and immunity of the boost converter and the logger | Only for a product placed on those markets | Electronics lead | To assess (product stage) |
| G13 | Local well construction and wellhead protection rules (state groundwater departments in India; state rules in the United States) | Local | Sealing, sanitary protection and who may open a well | Fitting the split seal plate and access tube to an existing well (PR-009, PR-010) | Partner and installer | To assess per site |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- Standards Council of Canada. "NSF/ANSI/CAN 61 - 2023." Standards database. https://scc-ccn.ca/standardsdb/standards/4032142 (checked 2026-10-24, StillStack SSK-REG-001).
- Bureau of Indian Standards. *IS 10500:2012, Drinking Water: Specification (Second Revision).* https://www.bis.gov.in/other/DrinWatIS10500.pdf (listed 2026-10-25).
- World Health Organization. *Guidelines for Drinking-Water Quality: Fourth Edition Incorporating the First and Second Addenda.* Geneva: WHO, 2022. https://www.who.int/publications/i/item/9789240045064 (checked 2026-10-24, StillStack SSK-REG-001).
- European Union. Directive (EU) 2020/2184 on the Quality of Water Intended for Human Consumption, Article 11. https://www.legislation.gov.uk/eudr/2020/2184/article/11 (checked 2026-10-24, StillStack SSK-REG-001).
- American Water Works Association. *AWWA C654-13, Disinfection of Wells.* https://store.awwa.org/AWWA-C654-13-Disinfection-of-Wells-PDF (listed 2026-10-25).
- Central Ground Water Authority, Ministry of Jal Shakti. *Guidelines to Regulate and Control Ground Water Extraction in India*, notification S.O. 3289(E), 24 September 2020, section 14 and Table 14.1. Copy hosted by the Maharashtra Pollution Control Board: https://www.mpcb.gov.in/sites/default/files/water-quality/standards-protocols/Ground_Water_NewGuidelinesNotifiedeng24092021102020.pdf (checked 2026-10-25).
- International Organization for Standardization. *ISO 4373:2022, Hydrometry: Water Level Measuring Devices.* AFNOR listing: https://www.boutique.afnor.org/en-gb/standard/iso-43732022/hydrometry-water-level-measuring-devices/xs139268/322212 (listed 2026-10-25).
- Cunningham, William L., and Charles W. Schalk. *Groundwater Technical Procedures of the U.S. Geological Survey.* Techniques and Methods 1-A1. Reston, VA: USGS, 2011. https://pubs.usgs.gov/tm/1a1/.
- Rows G9 to G13 are listed from the standards' and authorities' own titles; their detailed applicability is "to assess" and needs a test laboratory, the FieldNode project or a regulatory consultant. The LoRa band in India is described at https://www.everythingrf.com/community/lora-frequency-band-in-india (listed 2026-10-25); the WPC notification itself is to be cited by the FieldNode project.
