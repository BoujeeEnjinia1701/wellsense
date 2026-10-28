---
doc_id: WLS-URS-001
title: WellSense user requirements
project: WellSense
doc_type: User requirements
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First issue (kit 1.9.1 upgrade), drawn from the users and stakeholders of WLS-PRB-001 v0.7 (Tables 1 to 3) and the requirements of WLS-REQ-001 v0.8
---

# WellSense user requirements

What the people who share an aquifer, look after a well or run a monitoring programme need from a water level logger, written from their side. The product requirements that meet these needs are in WLS-PRS-001 (`03-requirements.md`) and the links are in the traceability matrix WLS-RTM-001 (`03b-traceability.md`). These needs are the author's reading of the users in WLS-PRB-001 and have not yet been checked in co-design; the first candidate partner, ACWADAM, has not been approached (WLS-DEC-001). Method: STANDARDS section 22.

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Performance | Trustworthy level record | We can see whether the water table is falling and by how much, with readings close enough to a manual tape that we trust them in a meeting | High | Village water committee or farmer group (PRB Table 2) |
| UR-002 | Performance | Our wells, not ideal ones | It works in the boreholes we have: 100 to 200 mm, 20 to 150 m deep, with water from a few metres to more than 50 m down | High | Farmer group, caretaker, ACWADAM (PRB Tables 1 and 3) |
| UR-003 | Performance | Pumping and recovery | We can watch how the level drops while the pump runs and how it recovers, including a pumping test | Medium | Farmer with an irrigation well (PRB Table 2) |
| UR-004 | Logistics | Nothing lost when the network drops | Readings are kept when the radio link fails and sent later | Medium | WASH NGO or agency (PRB Table 2) |
| UR-005 | Deployment and assembly | No extra power | It runs from the lab's shared FieldNode core and its small solar panel, with no grid supply and no extra battery | High | Caretaker (no grid power, PRB Table 2); FieldNode project (PRB Table 3) |
| UR-006 | Safety | Our drinking water stays safe | Nothing lowered into the well can contaminate it, and the wellhead stays sealed against surface water, insects and animals | High | Village water committee, well owner, water authority (PRB Tables 2 and 3) |
| UR-007 | Deployment and assembly | Leave the pump alone | It fits beside the existing pump, riser and cable without touching them, and without pulling the pump where possible | High | Well owner and pump installer (PRB Table 3) |
| UR-008 | Deployment and assembly | Quick to install | Two trained people with hand tools can install it in one visit | Medium | Caretaker, NGO field team (PRB Table 2) |
| UR-009 | Cost | Affordable for a community | The parts cost a small fraction of a commercial logger, so a group can afford one per shared well | High | Village water committee, WASH NGO (PRB Table 2) |
| UR-010 | Usability | Readable on a basic phone | We can read level below ground, daily drawdown and the change against last year on a basic phone, and export the data | Medium | Farmer group, NGO (PRB Table 2) |
| UR-011 | Regulatory | Our data | The community that hosts the well owns the data and decides what to share; only water levels are recorded | Medium | Gram panchayat water committee (PRB Table 3) |
| UR-012 | Environment and durability | Survives the wellhead | It survives sun, heat to 55 °C, monsoon rain and splash at the wellhead for years | High | Caretaker, farmer group (PRB Tables 1 and 2) |
| UR-013 | Safety | Hard to tamper with | The wellhead parts lock and no cable is exposed at a height people or livestock can reach | Medium | Caretaker (tampering and livestock, PRB Table 2) |
| UR-014 | Maintenance | Light upkeep | The caretaker can check and correct it with a tape and change the desiccant once a quarter, with nothing else to service between visits | Medium | Caretaker (PRB Table 2) |
| UR-015 | Safety | Safe to work on | The people installing and checking it are not exposed to dangerous voltages, even beside a mains-powered pump | High | Caretaker, pump installer (PRB Tables 2 and 3) |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.
