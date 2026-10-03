---
doc_id: WLS-BLD-001
title: WellSense prototype build plan
project: WellSense
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-02'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (WLS-DDR-004)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: Locks added as decided on 2026-10-02 (security-head screw, eye bolt and padlock, hasp and padlock, Figures 9a and 23a, step 18); wiring redrawn to FieldNode's standard port pinout
---

# WellSense prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. The decisions behind the design are recorded in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)).

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order. The access tube, cable and probe are drawn with the middle of the borehole left out.*

The prototype is one complete WellSense on a mock-up well: a short length of 150 mm casing standing in for the well, with a stand-in 1-1/4 in riser and pump cable, and the post set in the ground beside it. At a real well the steps are the same; only the access tube and cable are made to the well's depth. A vented pressure probe hangs on its cable inside a 1 in plastic access tube beside the riser. A split plastic seal plate closes the top of the casing round the riser, the pump cable and the tube. The cable leaves the tube through a cap, runs in a short flexible tail and a bent steel conduit to a junction box on the post, and the junction box feeds a FieldNode core higher up the same post. Figure 1 shows the 26 components in the order you make or fit them. Nine are made or worked in a small workshop: the post, the junction box plate, two V-blocks, the drilled junction box, the printed internal plate, the bent conduit, the seal plate with its spigot rings, the drilled access tube and the drilled tube cap. Everything else is bought and fitted, and the FieldNode core is built to its own plan. The work is sawing, drilling and filing aluminium, plastic and steel pipe, bending one length of conduit, one 3D print, cutting rubber sheet, and wiring bought modules with screw terminals. The WellSense parts cost about $262 at a 30 m probe depth, from the bill of materials.

> **Safety:** A real well is drinking water and often has a mains-powered pump. Before any work at a real well, isolate and lock off the pump supply, disinfect everything that goes into the well, and never leave the wellhead open. WellSense itself runs at 24 V or less. The FieldNode core holds a lithium iron phosphate cell of about 19 Wh: follow its build plan's safety stops. Cut aluminium and steel edges are sharp; printing ASA gives off fumes; concrete is caustic on skin.

## 2. What changed to make it buildable

The concept showed what WellSense does; some of its parts could not be made or fixed as drawn. Each change below keeps what WellSense does, and all of them are recorded in decision record WLS-DDR-004.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| FieldNode core | A block on two legs, floating 18 mm off the post | FieldNode's own constructable design, on its V-blocks and band clamps (step 9) | It is built to the FieldNode build plan and fits the same post |
| Junction box mounting | A flat box drawn into the round post, "held" by two bands, one of them above the box | A plate with two V-blocks and two band clamps; the box on the plate by four lugs (Figures 3, 5 and 9) | A band cannot hold a flat box on a round post |
| Junction box inside | A solid block with the board inside it; no cable entries | A hollow bought box; a printed internal plate on its bosses; four entries in the floor (Figures 6 to 12) | Entries in the floor keep water out; the electronics lift out as one piece |
| Barometric sensor | A housing floating beside the post, no fixing, no cable | A flanged housing screwed to the plate below the box, its lead in a gland (step 7) | A flat fixing and a short lead |
| Conduit | A solid rod round the cable with sharp corners, fixed hard to the tube cap | One bend of 100 mm radius, a hub under the box, two saddles, and a flexible tail to the cap (Figures 14, 15 and 23) | A hand bender makes it; the cap lifts off for calibration |
| Seal plate | One solid disc with two gland bosses; no way round an installed riser, no fixing, no hole for the pump cable | Two HDPE halves with spigot rings, an EPDM gasket and wraps, and a band round the rim (Figures 16 to 19) | It fits round the riser and pump cable without pulling the pump |
| Tube support | Not drawn, although 264 N of tube hangs from it at 60 m | A split collar on the tube resting on the seal plate (Figure 18) | A bought part that sets the tube height |
| Tube cap | A cap with a "hanger" boss, nothing carrying the probe | A slip cap with an eye bolt as the cross bolt; a cable support grip hangs from the bolt (Figure 23) | It holds the recorded probe depth and lifts off with the probe |
| Access tube bottom | 3 x 60 mm lengthwise slots and a plug made as part of the tube | Rings of 8 mm drilled holes and a bought end cap (Figures 20 and 21) | A hand drill does it |
| FieldNode lead | A cable into the top of the box with no plug | A lead with an M12 plug through a gland in the box floor, with a drip loop (step 10) | No entry on the top of a box outdoors |
| Locks | Nothing locked; the lockable parts were not specified | A security-head screw on the rim band, an eye bolt on the tube cap with a padlock, and a padlock hasp on the junction box, all fitted from the start (Figures 9a and 23a, step 18) | Keeps passers-by and livestock from opening the wellhead or the box |
| Surface cable | 2 m, no slack | 2.7 m with a 1.1 m service loop in the box (step 17) | The probe is lifted 1 m to calibrate it |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Front" is the side facing the well for the junction box and the side facing the equator for the FieldNode core; "left" and "right" are as seen standing in front. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Post and footing

![Figure 2. Making sketch of the post](../cad/drawings/WLS-DWG-101.png)

*Figure 2. Post making sketch (WLS-DWG-101).*

**What it is and what it is made from.** The upright that carries the junction box and the FieldNode core, 750 mm from the well's centre. Galvanized steel pipe 48.3 mm outside, 3.2 mm wall (1-1/2 in), 2.7 m long, with a push-in plastic cap; set in one 25 kg bag of premixed concrete.

**How to make it.**

1. Cut the pipe to 2,700 mm, square. File the ends and paint each cut end with zinc-rich paint.
2. Push the cap into the top end.
3. Mark with tape, measured up from the bottom end: 600 (ground level), 1,480 and 1,970 (junction box bands), 2,330 and 2,580 (FieldNode bands). The marks are guides; the parts are set on site.
4. No holes are drilled in the post: everything clamps to it.

**How it fits the parts next to it.** The bottom 600 mm stands in a concrete footing 300 mm across, on 50 mm of gravel, plumb both ways (step 1). The junction box plate's V-blocks and the FieldNode core's V-blocks sit on it, each pair held by two band clamps.

**Check before moving on.** Straight within 5 mm over its length; the cap is a firm push fit.

### 3.2 Junction box plate

![Figure 3. Making sketch of the junction box plate](../cad/drawings/WLS-DWG-102.png)

*Figure 3. Junction box plate making sketch (WLS-DWG-102).*

![Figure 3a. Hole positions on the junction box plate](05-build-plan/plate-holes.png)

*Figure 3a. Every hole and slot, measured up from the bottom edge and sideways from the centre line.*

**What it is and what it is made from.** The flat plate the junction box, the conduit saddles and the barometric housing are fixed to; it clamps to the post on two V-blocks. Aluminium sheet 3 mm, 5052 or 6061 class, cut to 140 x 530 mm.

**How to make it.**

1. Cut the blank to 140 x 530 mm, square. File the edges and round the corners to about 2 mm.
2. Scribe a centre line down the long side. Choose one face as the front (the box side) and mark it.
3. Mark every hole from Figure 3a: heights up from the bottom edge, sideways from the centre line.
4. Band slots: four slots 3 wide and 15 tall, 51 each side of centre, centred 20 and 510 up. Chain drill with a 3 mm drill and file the slots square.
5. V-block screw holes: four 4.5 mm holes, 18 each side of centre, 20 and 510 up. Countersink them from the front so M4 countersunk screws sit flush.
6. Lug holes: four 5.5 mm holes, 44 each side of centre, 302 and 478 up.
7. Saddle holes: four 5.5 mm holes, 17.4 each side of centre, 100 and 230 up.
8. Barometric housing holes: two 4.5 mm holes, 45 left of centre, 158 and 202 up.
9. Deburr every hole on both faces.

**How it fits the parts next to it.** The V-blocks sit flat on its back face at the top and bottom (Figure 5). The box's back sits flat on its front face between 310 and 470 up, held by four lugs (Figure 9). The saddles and the barometric housing sit flat on its front face below the box.

**Check before moving on.** Lay the V-blocks, lugs and saddles on the plate and look through each hole: the holes must line up without forcing a screw.

### 3.3 V-blocks (make 2)

![Figure 4. Making sketch of the V-block](../cad/drawings/WLS-DWG-103.png)

*Figure 4. V-block making sketch (WLS-DWG-103). The same part as FieldNode's V-block.*

**What it is and what it is made from.** A block with a 90° V cut in it that the post sits in, one at each band clamp. Aluminium flat bar 60 x 40 mm, 6082 or 6061 class.

**How to make it.**

1. Saw two slices 20 mm thick off the bar. Saw and file each to 60 wide, 33 deep and 20 tall. The 60 x 20 face that will sit on the plate is the back face; file it flat.
2. On each 60 x 33 face, scribe the V with a 45° square: two lines from the front face, 50.3 apart where they start, meeting at a point 7.8 from the back face, centred on the width.
3. Saw just inside both lines, then file to the lines. Keep the two V faces flat and square to the block's faces.
4. Break the sharp front edges of the V by 0.5 mm.
5. On the back face, 18 each side of centre and half way up, drill 3.3 mm 14 deep and tap M4 12 deep.

**How it fits the parts next to it.**

![Figure 5. Joint 1: V-block, post and band clamp, seen from above](05-build-plan/joint-01.png)

*Figure 5. The post sits in the V and touches both faces; the band clamp goes round the post and pulls it into the V.*

The back face sits flat on the back of the plate, held by two M4 countersunk screws put in from the front of the plate with a drop of medium threadlocker. The 48.3 mm post touches both faces of the V; it never touches the bottom of the V. The band passes 2 mm clear of the block's outer corners.

**Check before moving on.** Hold the block against the post: it must not rock, and you should see light at the bottom of the V but not along its faces.

### 3.4 Junction box body, drilled, with its entries and lugs

![Figure 6. Drilling sketch of the junction box body](../cad/drawings/WLS-DWG-104.png)

*Figure 6. Junction box drilling sketch (WLS-DWG-104), drawn upside down so the top view shows the floor.*

![Figure 7. Junction box floor drilling layout](05-build-plan/box-holes.png)

*Figure 7. Drilling layout of the floor.*

**What it is and what it is made from.** A bought grey polycarbonate box, 160 tall, 120 wide and 90 deep, rated IP66, with a gasketed lid on the front, four moulded bosses inside the back wall and the maker's kit of four external mounting lugs. Four holes are drilled in its floor.

**How to make it.**

1. Stand the box upside down on its top on a soft cloth, back face toward you. Cover the floor with masking tape.
2. Mark the holes from Figure 7. Back row, 22 from the back face: the conduit hub on the centre line and the M16 gland 38 right. Front row, 62 from the back face: the breather 30 right and the M12 gland 30 left.
3. Put a block of wood inside under the floor. Pilot drill every hole 3 mm at low speed.
4. Open each hole with a step drill, light pressure, low speed: 22 for the hub, 20 for the breather, 16 and 12 for the glands. Check each size against the part's datasheet before the last step.
5. Deburr inside and out, peel the tape, and clean with water and mild soap only; solvents craze polycarbonate.
6. Fit the four lugs to the box's back corners as the lug kit's maker describes.
7. Fit the hasp kit on the right-hand side wall, as you face the lid, at the middle of the box's height. One stainless tab goes on the body just behind the split between body and lid and one on the lid just in front of it, each on two M3 screws with the kit's sealing washers through 3.2 mm holes. The tabs stand out from the wall 22 mm, 4 mm apart across the split, and each has a 7 mm hole for the padlock.

**How it fits the parts next to it.**

![Figure 8. Joint 3: the junction box floor, seen from below](05-build-plan/joint-03.png)

*Figure 8. Hub and M16 gland in the back row, breather and M12 gland in the front row; the conduit comes up into the hub.*

Each entry goes in from below with its seal outside and its nut inside (step 3). The outside bodies are at least 10 mm apart, so a spanner fits each. The box's back sits flat on the plate, held by the lugs:

![Figure 9. Joint 2: junction box lug on the plate](05-build-plan/joint-02.png)

*Figure 9. Each lug lies flat on the plate beside the box and is held by one M5 button-head screw from behind the plate, nyloc nut in front.*

![Figure 9a. Joint 11: hasp kit and padlock across the split of the junction box](05-build-plan/joint-11.png)

*Figure 9a. The two tabs line up across the split between the body and the lid; one padlock shackle goes through both holes, so the lid cannot be opened while the padlock is shut.*

**Check before moving on.** No crack runs out from any hole under a bright lamp; the box sits flat on the plate with all four lug holes lined up; the two hasp tab holes line up with the lid shut and a 4 mm rod passes through both.

### 3.5 Internal plate and the interface modules on it

![Figure 10. Making sketch of the internal plate](../cad/drawings/WLS-DWG-105.png)

*Figure 10. Internal plate making sketch (WLS-DWG-105).*

**What it is and what it is made from.** A printed plate that carries the interface modules and the terminal strip and lifts out of the box as one unit. ASA plastic, 100 x 130 x 3 mm, printed flat at 100 % infill in an enclosed printer.

**How to make it.**

1. Measure the four bosses inside your box. The model assumes they are 80 apart across and 110 apart up and down; move the plate's holes to match your box.
2. Print the plate with four 4.5 mm holes at the bosses, 10 in from the top and bottom edges. Let it cool on the bed so it does not warp.
3. Lay out the parts on the front face as Figure 11 shows: boost module upper left, ADC and shunt module upper right, regulator and surge module below it, terminal strip along the bottom.
4. Mark each module's mounting holes through the module, drill 3.2 mm, and fit the modules on M3 screws with 6 mm nylon standoffs.
5. Wire the modules as Figure 13 shows (section 3.5.1).

![Figure 11. Step 4 picture: parts on the internal plate](05-build-plan/step-04.png)

*Figure 11. Where each part goes on the internal plate.*

**How it fits the parts next to it.**

![Figure 12. Joint 4: internal plate on its bosses](05-build-plan/joint-04.png)

*Figure 12. The plate sits on the four moulded bosses, 6 mm off the back wall and 12 mm above the floor, clear of the entry nuts, held by four M4 screws.*

**Check before moving on.** The plate is flat within 0.5 mm and drops in and lifts out without force.

#### 3.5.1 Wiring

![Figure 13. Block-level wiring](05-build-plan/wiring.png)

*Figure 13. Block-level wiring with wire sizes, with the pins of FieldNode sensor port A named. No circuit board is laid out at this stage; bought modules make up the interface board.*

Buy modules that meet this specification:

*Table 2. Modules that make up the interface board.*

| Module | What to buy |
| --- | --- |
| Surge and reverse protection | A TVS diode across the 12 V input and a Schottky diode in series, on a small board |
| Boost module | 12 V in, 24 V out, at least 50 mA, adjustable, about 43 x 21 mm |
| Shunt | 150 Ω, 0.1 %, 10 ppm/K, 0.25 W or more |
| ADC module | 16-bit, ADS1115 class, I2C, with a 1 kΩ to 10 kΩ series resistor added on its input |
| 3.3 V regulator | Low-dropout, 3.3 V, 100 mA or more, feeding the ADC and the barometric sensor |
| Terminal strip | Pluggable, 5.08 mm pitch, about 10 ways |

Wire it like this, with stranded copper and a ferrule on every screw terminal:

1. FieldNode lead to the terminal strip: pin 1 (the switched 12 V rail) and pin 3 (ground), then on to the surge and reverse board: 0.2 mm² in the lead, 0.5 mm² on the plate. This is FieldNode's standard sensor port pinout.
2. Surge board to the boost module input: 0.5 mm².
3. Boost module output (24 V) to the loop + terminal: 0.5 mm².
4. Vented cable cores to the loop + and loop - terminals.
5. Loop - terminal through the 150 Ω shunt to ground: 0.5 mm².
6. Shunt to the ADC input through the series resistor: 0.25 mm², twisted.
7. 12 V to the 3.3 V regulator; regulator to the ADC and to the barometric lead: 0.25 mm².
8. ADC and barometric sensor I2C lines to the terminal strip and back up the FieldNode lead: data A (pin 2) carries SDA and data B (pin 4) carries SCL, 0.25 mm². Pin 5 (analog) is not used and is left unconnected.
9. Leave the vent tube in the vented cable open inside the box; do not crimp or seal it.

**Check before moving on.** Every wire continues end to end; with no supply, the 24 V output and the 12 V input read open to ground; every wire is labelled.

### 3.6 Rigid conduit

![Figure 14. Making sketch of the rigid conduit](../cad/drawings/WLS-DWG-106.png)

*Figure 14. Rigid conduit making sketch (WLS-DWG-106).*

**What it is and what it is made from.** The steel pipe that protects the cable from the well to the junction box. 1/2 in galvanized rigid conduit, 21.3 mm outside.

**How to make it.**

1. Cut a length of about 1 m. Ream both ends so the bore is smooth.
2. Bend one 90° bend of 100 mm centre-line radius with a 1/2 in hand conduit bender, so that the long leg runs 543 mm from the bend's corner and the short leg 430 mm.
3. Check the bend with a square and trim both legs to length.
4. Paint each cut end with zinc-rich paint.

**How it fits the parts next to it.**

![Figure 15. Joint 5: conduit on its saddle and into the hub](05-build-plan/joint-05.png)

*Figure 15. The spacer saddle holds the conduit 11 mm off the plate, square under the hub.*

The short leg stands upright 22 mm in front of the plate and screws into the hub under the box. Two spacer saddles, 100 and 230 mm up the plate, hold it with two M5 screws each through the plate, nyloc nuts behind. The long leg runs level 720 mm above the ground toward the well and takes the flexible tail's connector at its end.

**Check before moving on.** Both legs square to each other; the ends are smooth inside.

### 3.7 Seal plate with spigot rings, gasket and wraps

![Figure 16. Making sketch of the seal plate](../cad/drawings/WLS-DWG-107.png)

*Figure 16. Seal plate making sketch (WLS-DWG-107).*

![Figure 17. Seal plate holes and split line](05-build-plan/seal-holes.png)

*Figure 17. The three holes all lie on the split line.*

**What it is and what it is made from.** The cover that closes the top of the casing round the riser, the pump cable and the access tube, and carries the tube. Drinking-water grade HDPE sheet 20 mm (plate) and 10 mm (spigot ring); EPDM rubber sheet 3 mm (gasket) and 2 mm (wraps).

**How to make it.**

1. Measure the riser and the pump cable at the well. The design uses a 42.2 mm riser and a 12 mm cable; each hole is the part plus 2 mm of rubber each side.
2. Cut a 200 mm disc from the 20 mm sheet and a ring 148 mm outside and 128 mm inside from the 10 mm sheet, with a jigsaw and a circle jig, then file to the line. Check the ring slides into the casing.
3. Scribe a diameter across the disc. On it, bore the riser hole 46 mm at 30 left of centre, the pump cable hole 16 mm at 7 right and the tube hole 37.4 mm at 40 right, with hole saws or a step drill.
4. Saw the disc and the ring in half along that diameter, keeping the cut straight.
5. Screw each half ring under its plate half, centred, with three stainless 4 x 16 screws in 3 mm pilot holes.
6. Cut the gasket from 3 mm EPDM, 184 mm outside and 150 mm inside, and cut it once so it can go round the riser.
7. Cut three wraps from 2 mm EPDM, 20 mm wide, each one turn long for the riser, the pump cable and the tube.
8. Take the hex screw out of the rim band clamp and fit the security-head screw in its place, so the band can only be undone with the matching bit.

**How it fits the parts next to it.**

![Figure 18. Joint 6: seal plate on the casing, cut on the split line](05-build-plan/joint-06.png)

*Figure 18. The spigot sits inside the casing, the gasket on its rim; the collar on the plate carries the tube.*

![Figure 19. Joint 7: the split, seen from above](05-build-plan/joint-07.png)

*Figure 19. Both halves close round the wrapped riser, pump cable and tube; the band round the rim pulls them together.*

The gasket lies on the casing rim and the plate halves lie on the gasket, their spigots 1 mm inside the casing bore. Each wrap fills the gap between its part and the plate, so tightening the rim band squeezes all three. The tube collar sits on top of the plate. The rim band's security-head screw sits on the band's housing, on the side of the plate away from the riser, with its head clear of the plate rim.

**Check before moving on.** On a trial fit round a short length of riser, the halves meet with no daylight at the split.

### 3.8 Access tube, drilled, with its end cap

![Figure 20. Making sketch of the access tube's drilled end](../cad/drawings/WLS-DWG-108.png)

*Figure 20. Access tube making sketch (WLS-DWG-108), drilled end.*

**What it is and what it is made from.** The plastic tube the probe hangs in, beside the riser, so the probe cannot tangle with the pump. 1 in Sch 40 PVC pressure pipe, 33.4 mm outside and 26.6 mm bore, in 3 m lengths, with a 1 in slip cap on the bottom.

**How to make it.**

1. Work out the length: the probe depth plus 0.5 m below the probe plus 0.11 m above the casing top. Join 3 m lengths with solvent-weld couplings, wiping the inside of each joint smooth.
2. Over the bottom 0.5 m, drill ten rings of 8 mm holes 50 mm apart, the first 40 mm up from the end. Each ring is two holes drilled straight through at right angles (four holes); turn the next ring 45°. Hold the tube in a V-block to drill.
3. Deburr each hole inside with a round file.
4. Solvent-weld the slip cap on the bottom end and drill one 8 mm drain hole in it.
5. Cut the top square and deburr.

**How it fits the parts next to it.**

![Figure 21. Joint 9: probe in the drilled bottom of the tube](05-build-plan/joint-09.png)

*Figure 21. The 22 mm probe hangs 50 mm above the end cap with 2.3 mm clear all round; water reaches it through the holes.*

The tube hangs beside the riser, 32 mm clear of it and 18 mm from the casing wall, from a collar resting on the seal plate.

**Check before moving on.** A 22 mm rod drops through the whole tube freely.

### 3.9 Tube cap with eye bolt and support grip

![Figure 22. Making sketch of the tube cap](../cad/drawings/WLS-DWG-109.png)

*Figure 22. Tube cap making sketch (WLS-DWG-109).*

**What it is and what it is made from.** The cap on the top of the access tube; the probe hangs from it and the conduit's flexible tail plugs into it. A 1 in Sch 40 PVC slip cap, a stainless M5 x 50 eye bolt (a bolt with a swing eye in place of the head) with a nyloc nut, and a stainless single-eye cable support grip for 6 to 8 mm cable.

**How to make it.**

1. Do not glue the cap: it must lift off.
2. Drill 22.5 mm in the centre of the top for the conduit connector.
3. Drill 5 mm straight across the cap, 9 mm above the shoulder the tube end stops against and 9 mm off the centre line, for the eye bolt, which acts as the cross bolt.

**How it fits the parts next to it.**

![Figure 23. Joint 8: tube cap, cut open](05-build-plan/joint-08.png)

*Figure 23. The grip's eye hangs on the cross bolt; the cap rests on the tube end; the connector's locknut is inside the cap.*

![Figure 23a. Joint 10: padlock on the eye bolt of the tube cap](05-build-plan/joint-10.png)

*Figure 23a. The eye of the eye bolt stands out on the right-hand side of the cap, and the padlock's shackle passes through it.*

The connector goes through the top with its locknut inside. The support grip is pushed onto the cable at the mark for the probe depth, and its eye goes over the cross bolt, which carries the probe and cable. The bolt passes beside the cable, 3 mm clear of it. Its swing eye stands out of the cap on one side, with the nyloc nut on the other, and takes the padlock (step 18). The padlock stops the eye bolt being unscrewed, so the grip and the probe cannot be freed; it does not stop the cap being lifted off the tube, which is the job of the lockable steel wellhead cover at sites where the first visit shows open access or livestock.

**Check before moving on.** With the bolt in, the cap still slides on and off the tube by hand, and a 4 mm rod passes through the eye.

### 3.10 FieldNode core

Build one FieldNode core to the FieldNode build plan (FND-BLD-001), without the sun shield unless the site's hottest days pass 30 °C. WellSense uses it unchanged: its V-blocks fit this post, and the WellSense lead plugs into its sensor port A. Leave its fuse out and its cell out of the holder until its own safety stops say otherwise.

### 3.11 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Pressure transducer (line 1).** Vented (gauge), 0 to 10 m of water, 4 to 20 mA two-wire, 12 to 30 V supply, 0.25 % of full scale class, 316 stainless body 22 mm diameter or less, IP68, with a drinking-water certificate.
- **Vented cable (line 2).** Polyurethane or polyethylene jacket, two cores of 0.2 mm² or more, aramid strain member of 400 N or more, vent capillary, about 7 mm; the probe depth plus 2.7 m.
- **Access tube and end cap (line 3).** As section 3.8.
- **Seal plate parts (line 4).** HDPE and EPDM sheet as section 3.7; a stainless worm-drive band clamp for 180 to 210 mm (its hex screw is swapped for the security-head screw of line 16); a split aluminium shaft collar for 1-5/16 in (33.4 mm) pipe; six stainless 4 x 16 screws.
- **Tube cap parts (line 5).** As section 3.9, with an M5 x 50 stainless eye bolt.
- **Junction box (line 6).** As section 3.4, with an M16 gland for 4 to 8 mm cable, an M12 gland for 3 to 6.5 mm cable, a replaceable silica gel breather in an M20 thread, and four M5 x 16 button-head screws with nyloc nuts.
- **Interface modules (line 7).** As Table 2, with M3 screws and 6 mm nylon standoffs.
- **Barometric sensor (line 9).** BMP390 or BME280 class module in a louvred housing about 36 mm across with a flat two-screw flange, and a 0.3 m lead.
- **Post set (line 10).** The pipe and cap of section 3.1, the plate and V-blocks of sections 3.2 and 3.3, two 12 mm stainless worm-drive band clamps, four M4 x 12 countersunk screws.
- **Footing (line 13).** One 25 kg bag of premixed concrete and a bucket of gravel.
- **Conduit set (line 14).** The rigid conduit of section 3.6; 0.3 m of 1/2 in liquid-tight flexible conduit with two straight connectors; two 1/2 in spacer saddles with M5 screws and nyloc nuts; one 1/2 in conduit hub.
- **FieldNode lead (line 15).** 1.5 m of four-core screened cable, about 0.2 mm², with an M12 A-coded 5-pin plug, IP67, wired to pins 1 to 4 and leaving pin 5 unconnected; cable ties.
- **Locks (line 16).** One stainless security-head screw and its bit; two keyed-alike 20 mm stainless padlocks with a 4 mm shackle; one padlockable stainless hasp kit with two M3 screws and sealing washers for each tab.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in. Steps 1 to 11 build the surface unit; steps 12 to 18 fit the wellhead and lock it.

### Step 1: post into its footing

![Step 1](05-build-plan/step-01.png)

Dig a hole 300 mm across and 650 mm deep, 750 mm from the well's centre. Put in 50 mm of gravel, stand the post on it with its 600 mm mark at ground level, plumb it both ways and brace it. Pour one bag of concrete, slope the top away from the post, and leave it to cure for two days before loading the post.

### Step 2: V-blocks onto the junction box plate

![Step 2](05-build-plan/step-02.png)

Two M4 countersunk screws per block, from the front of the plate, with medium threadlocker, snug. The V opens away from the plate.

### Step 3: hub, glands and breather into the box

![Step 3](05-build-plan/step-03.png)

Each goes in from below with its seal outside and its nut inside, tightened to the maker's torque.

### Step 4: build the internal plate

![Step 4](05-build-plan/step-04.png)

Fit the modules and terminal strip on M3 screws and standoffs and wire them as Figure 13. **Hold point:** the wiring checks of section 3.5.1 pass before going on.

### Step 5: junction box onto the plate

![Step 5](05-build-plan/step-05.png)

Hold the box flat on the front of the plate, centred, its bottom 310 mm up the plate. Four M5 button-head screws through the lugs from behind the plate, nyloc nuts in front, snug.

### Step 6: internal plate into the box

![Step 6](05-build-plan/step-06.png)

Four M4 screws into the bosses. Leave the lid off until step 17.

### Step 7: barometric housing onto the plate

![Step 7](05-build-plan/step-07.png)

Two M4 screws with nyloc nuts through its flange and the plate, louvres down. Feed its lead up through the M12 gland and tighten the gland on it.

### Step 8: junction box onto the post

![Step 8](05-build-plan/step-08.png)

Hold the plate with both V-blocks on the post, the box facing the well and the plate's bottom edge 860 mm above the ground. Pass each band round the post, through its two slots and across the front of the plate, with the worm-drive housing at the back of the post. Tighten both bands to the band maker's torque and record it.

### Step 9: FieldNode core onto the post

![Step 9](05-build-plan/step-09.png)

The core is built to its own plan. Hold it with its V-blocks on the post, the panel facing the equator and its enclosure's base 1,750 mm above the ground, and tighten its two bands as its plan says.

### Step 10: FieldNode lead from the box to port A

![Step 10](05-build-plan/step-10.png)

Push the lead's bare end up through the M16 gland into the box and tighten the gland. Leave a drip loop below the box, run the lead round the edge of the plate and up the side of the post outside the bands, cable-tied every 200 mm, and plug the M12 plug into port A. **Hold point:** the FieldNode core's fuse is still out.

### Step 11: rigid conduit into the hub and saddles

![Step 11](05-build-plan/step-11.png)

Screw the short leg up into the hub, hand tight plus a quarter turn, with the long leg pointing at the well. Fit the two spacer saddles round the upright leg and screw them to the plate. Check the long leg is level.

### Step 12: access tube down the casing

![Step 12](05-build-plan/step-12.png)

**Hold point:** at a real well, safety stop S5 first. Disinfect the tube. With two people, lower it end cap first beside the riser and pump cable, hand over hand, until its top is about 110 mm above the casing; hold it there.

### Step 13: gasket, wraps and the two seal plate halves

![Step 13](05-build-plan/step-13.png)

Lay the gasket on the casing rim. Wrap one turn of EPDM round the riser, the pump cable and the tube at the height the plate will sit. Bring the two halves in from each side so their spigots drop inside the casing and they close round the three wraps.

### Step 14: rim band and tube collar

![Step 14](05-build-plan/step-14.png)

Put the band round the rim and tighten it with the security-head bit until the halves meet. Set the tube so its top is 110 mm above the casing top, clamp the collar on the tube and let it rest on the plate.

### Step 15: thread the cable

![Step 15](05-build-plan/step-15.png)

Fit the conduit connector through the cap and tighten its locknut. Push the cable's free end up through the cap, the flexible tail and the rigid conduit until it comes out of the hub into the box; then screw the tail's far connector onto the end of the rigid conduit. The probe stays on the bench.

### Step 16: lower the probe and hang it

![Step 16](05-build-plan/step-16.png)

Disinfect the probe and the cable. Mark the cable at the probe depth from the measuring point (the casing top). Lower the probe hand over hand down the tube, feeding cable from the box end, until the mark is at the cap. Push the support grip onto the cable at the mark, put its eye over the eye bolt, fit the bolt's nut and seat the cap on the tube.

### Step 17: service loop, terminals and lid

![Step 17](05-build-plan/step-17.png)

Coil 1.1 m of cable in the box in front of the internal plate, cut the rest, strip the cores to the terminal strip and leave the vent tube open. Put a fresh charge in the breather. Check the lid gasket is clean and seated with no wire across it, and tighten the lid screws in a cross pattern.

### Step 18: fit the padlocks

![Step 18](05-build-plan/step-18.png)

Hang the first padlock through the eye of the eye bolt on the tube cap and close it. Close the second padlock through the holes of both hasp tabs with the lid shut. Check that the one key opens and closes both, and that the security-head screw on the rim band is tight. Take the key with you.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of WLS-REQ-001.

*Table 3. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Probe runs freely | R10 | Lower and lift the probe the full tube length | It never catches; the support grip holds it at the mark |
| Seal | R9 | Look along the split, the rim and each wrap under a lamp; pour a cup of water on the plate | Halves meet with no daylight; no water passes into the casing |
| Tube carried by the collar | R2 | Pull down on the tube by hand at the collar | The collar does not slip |
| Loop supply | R8 | Bench supply at 12 V on the lead in place of FieldNode, 100 mA limit; measure at the transducer's terminals with a 20 mA loop calibrator in place of the probe | At least 20 V at 20 mA |
| Loop reading | R3, R4 | Loop calibrator at 4, 12 and 20 mA; read the ADC | Within 0.1 % of 0.60, 1.80 and 3.00 V across the shunt |
| ADC protection | R4 | Calibrator at 25 mA | ADC input stays below its 3.6 V limit |
| Barometric sensor | R15 | Read it over I2C with the box shut | Within 1 hPa of a reference barometer |
| Two-point calibration lift | R4 | Undo the tail's connector at the cap, lift cap and probe 1 m, read, lower, reconnect | The service loop feeds the 1 m without pulling on the terminals |
| Fixings | R16 | Push on the box, conduit and FieldNode core by hand | Nothing moves at any joint; the conduit does not touch the riser |
| Locks | R16 | With both padlocks shut, try to lift the lid, turn the eye bolt and undo the rim band screw with ordinary tools | None of the three can be undone; the one key opens both padlocks |
| Installation time | R11 | Time steps 12 to 18 with two people | 2 h or less at a well with the tube already in place |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before digging the footing.** Buried services located; the hole is at least 600 mm from the well's apron edge and from any pump cable trench.
- **S2. Before wiring the interface modules.** No supply connected; the boost module output is set to 24 V on the bench, measured, before it is wired to the loop.
- **S3. Before the FieldNode lead is plugged in.** The FieldNode core's fuse is out and its own stop points are followed; the lead's 12 V and ground are checked against port A's pinout with a meter.
- **S4. Before the junction box is closed.** No bare conductor outside a terminal; the vent tube is open; the boost output is 24 V or less.
- **S5. Before any work at a real well (outside this plan).** The pump supply is isolated and locked off, with the key held by the person at the wellhead; the well owner or water authority agrees; a second person is present; the open casing is covered whenever nobody is working at it.
- **S6. Before anything goes into a real well.** The probe, cable, tube, wraps and gasket are disinfected as the local water authority advises, and every wetted part has its drinking-water certificate.
- **S7. Before lowering the tube or the probe.** Two people; the cable or tube is fed hand over hand and never allowed to run; the cable never carries more than its strain member's rating.
- **S8. Before leaving the site.** The seal plate band is tight, the cap is seated, the junction box is shut, both padlocks are closed, and the FieldNode core's own final checks are done.

## 7. Tools, skills and workspace

**Tools.** Hacksaw with a 24 teeth per inch blade; pipe cutter; 1/2 in hand conduit bender; bench vice with soft jaws; bench drill or a drill in a stand; drills 2.5 to 12 mm; step drill to 22 mm; hole saws 38 and 46 mm; countersink; M4 tap and tap drill; jigsaw with metal and plastic blades and a circle jig; flat, half-round and round files; deburring tool; scriber, engineer's square, 45° square, steel rule and calipers; V-block for drilling tube; 3D printer with an enclosure and a bed of at least 100 x 130 mm that prints ASA; soldering iron; ferrule crimper and wire strippers; multimeter; bench power supply with an adjustable current limit; 4 to 20 mA loop calibrator; torque screwdriver; the security-head bit for the rim band screw; spirit level; spade, post-hole digger and bucket.

**Skills.** No certified trade is needed. Basic metalwork and plastic work (marking out, sawing, drilling, filing, tapping, bending conduit), through-hole soldering and crimping, safe use of a bench power supply, and mixing concrete. All circuits are extra-low voltage: 12 V from FieldNode and 24 V in the loop. Working at a real well with a mains-powered pump needs the owner's or water authority's agreement and a person who can isolate the pump safely.

**Workspace.** A bench about 1.2 x 0.6 m; a metalwork corner kept apart from the electronics; a ventilated place for the printer; a yard where the post can be set and the mock-up casing stood upright and held.

**Personal protective equipment.** Safety glasses for cutting, drilling and soldering; cut-resistant gloves for metal edges; gloves and eye protection when mixing concrete; nitrile gloves when using disinfectant and solvent cement; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 118 checks); STEP and STL exports in `cad/step/` and `cad/stl/`; FieldNode geometry in `cad/vendor/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/WLS-DWG-101` to `WLS-DWG-109`.
- General arrangement: `cad/drawings/WLS-DWG-001.pdf`, Rev P6.
- Calculations: `docs/04-calcs/01-sizing.md` (WLS-CAL-001 v0.5) and `docs/04-calcs/sizing.py`; loop supply [B1], loads [D3] to [D7], cost [H1] to [H3].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0004-design-for-construction.md` (WLS-DDR-004), with WLS-DDR-001 to WLS-DDR-003.
- Requirements: `docs/03-requirements.md` (WLS-REQ-001 v0.8).
- FieldNode core: the FieldNode build plan FND-BLD-001 and drawing FND-DWG-001.
