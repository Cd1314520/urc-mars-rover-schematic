# Physical Layout: Electronics Bay Plan

Task 4 secondary task taken over from Hogan (Task 4 spreadsheet, Secondary Task Descriptions): "Figure out how each subsystem PCB will be arranged in space. Take into consideration designing access to each subsystem from the outside."

Status: draft, 2026-10-27. The chassis and the electronics box are not designed yet, and most subsystem PCBs do not have a size yet. So this plan gives **zones, placement rules, an area budget and access rules**, not final coordinates. Values marked **EST** are estimates; **TBD** needs a part choice or a number from another team. Companion to [COOLING_PLAN.md](COOLING_PLAN.md).

## 1. Rules that constrain the layout

| Rule | Text (URC 2027 Requirements and Guidelines) | Layout impact |
|---|---|---|
| 2.a.ii | Rover must fit in a 1.2 m x 1.2 m x 1.2 m box; "may not be disassembled to do so" (includes antennas) | Antenna mast and anything on the outside of the bay must fold or fit inside the cube |
| 2.a.iii | 50 kg max deployed; arm and science module may be swapped, rover + arm + science < 70 kg | Arm and science electronics need a **quick-disconnect** at the bay wall, so a module can come off without opening the bay |
| 2.a.v | Red push-button E-stop "readily visible and accessible on the exterior of the rover"; one E-stop switches off all systems | E-stop on the outside of the bay, wired to the contactor coil inside |
| 3.d.iii | 37.8 C, dust, light rain | Sealed bay, cable glands, see COOLING_PLAN.md |

## 2. What goes in the bay

### Subsystem PCBs (Task 4 owners; sizes TBD)

| Subsystem board | Owner | Size | Notes |
|---|---|---|---|
| PDP (power distribution) | Bryan | TBD | Ask Bryan whether the main fuse, contactor and fuse block sit on the PDP or next to it |
| Compute/Logic | Paul | TBD | Teensy 4.1 + CAN transceivers |
| Drivetrain | Krishna | TBD | MDDS30s are modules, not on a custom PCB |
| Comms/Navi | Chris | TBD | RFD900x, switch, PoE injector, GPS, IMU |
| Robo Arm | Ricky | TBD | Arm MCCs may sit on the arm module instead (rule 2.a.iii) |
| Sci Package | Kaden | TBD | Sits on the science module (rule 2.a.iii) |

### Modules with verified sizes

| Part | Qty | Size (mm) | Plate area (mm2) | Mounting | Source |
|---|---|---|---|---|---|
| Cytron MDDS30 | 3 | 101.60 x 81.28, height ~42 | 24,774 total | 4 corner holes; optional 40x40x20 mm fan fits between the top and bottom PCB on 30 mm stands | Cytron manual Rev 1.11 p.4 (size), Rev 1.3 section 9 (fan) |
| Jetson Orin Nano dev kit | 1 | 100 x 79 x 21 (height incl. feet, module, heatsink) | 7,900 | Carrier board holes | NVIDIA datasheet value (quoted on NVIDIA forum); JetsonHacks measured 103 x 90.5 x 35 with the plastic base |
| Mean Well DDR-60G-12 | 1 | 52.5 W x 90 H x 54.5 D, 216 g | 4,725 (W x H on the rail) | DIN rail | Mean Well DDR-60 datasheet |
| Pololu D36V28F5 | 1 | 17.8 x 20.3 x 8.8 | 361 | Two M2 holes | Pololu product page |
| Teensy 4.1 | 1 | 60.96 x 17.78, pin rows 15.24 apart | 1,084 | Headers on a carrier PCB | PJRC dimension drawing |
| RFD900x | 1 | 30 x 57 x 12.8, 14 g | 1,710 | | RFDesign datasheet v1.1 (one table says 57.7, likely a typo) |
| Gigabit switch (L-com SWTC-GS105NA) | 1 | ~94 x 104 x 28 **EST** | 9,776 | | Retailer figures for the Netgear GS105NA it is based on; L-com's own drawing was blocked by their site |
| Waveshare SN65HVD230 board | 1-3 | TBD | | | Waveshare gives a STEP model only |
| Class T fuse + holder, contactor, pre-charge, fuse block, PoE injector, USB hub | 1 each | TBD | | | Parts not chosen yet |

**Sum of known modules: about 50,300 mm2 = 0.050 m2.** With 2x to 2.5x for wiring, connectors, terminal access and airflow, plan for **0.10-0.13 m2 of mounting plate**, before the TBD parts and subsystem PCBs. That is roughly a 400 x 250 to 400 x 300 mm plate. The tallest known part is the DDR-60G at 54.5 mm (MDDS30 ~42 mm, more with the fan), so the inside height needs about **100-150 mm EST** once connector and cable bend room are added. This matches the 0.40 x 0.30 x 0.15 m box assumed in COOLING_PLAN.md section 3, but it will get tighter when the subsystem PCBs get sizes.

### Outside the bay

| Item | Where | Why |
|---|---|---|
| Battery | Separate bay, low and central | Centre of gravity; swappable from outside (see URC_2027_Battery_Swap_Report.xlsx on the Drive) |
| E-stop + start button | Exterior panel, high and visible | Rule 2.a.v |
| Wheel motors + encoders | At the wheels | Harness to the MDDS30s and Teensy through glands |
| MikroTik Groove, antennas | Mast | RF line of sight; must fold for the 1.2 m cube |
| GPS antenna | Top of rover | Needs open sky |
| Cameras, LiDAR | Mast / chassis | Field of view |
| Arm MCCs, science electronics | On their modules | Modules are swapped (rule 2.a.iii) |

## 3. Zones and placement rules

Split the bay into three zones so heavy current, heat and RF stay apart.

```
            FRONT (access panel side)
 +------------------------------------------------------+
 |  ZONE 1: POWER / DRIVE      |  ZONE 2: LOGIC          |
 |  (heat-spreader wall)       |                         |
 |  main fuse -> contactor ->  |  DDR-60G-12 (DIN)       |
 |  fuse block                 |  D36V28F5               |
 |  MDDS30 #1 #2 #3 in a row,  |  Teensy + CAN board     |
 |  fins vertical              |  Jetson (own fan, air)  |
 |                             |---------------------------|
 |                             |  ZONE 3: COMMS / RF     |
 |                             |  switch, PoE injector,  |
 |                             |  RFD900x near antenna   |
 |                             |  feed-through           |
 +------------------------------------------------------+
   ^ battery cable in      ^ motor harness out    ^ antenna / Ethernet out
            REAR (bulkhead connectors, glands)
```

Rules:

1. **Short, fat power path.** Battery -> Class T fuse -> contactor -> fuse block -> MDDS30s all in zone 1, nearest the battery bay. The 24 V high-current runs (main path 8 AWG min / 6 AWG per Trade Study, 12 AWG to each MDDS30, per the drivetrain fuse/wire table) stay as short as possible.
2. **Drivers on the heat-spreader wall.** Mount the three MDDS30s and the DDR-60G on the aluminium wall from COOLING_PLAN.md option C, with fins vertical so hot air rises. If the optional fan is fitted, it mounts on the inner side of the bottom PCB, the two PCBs go back together on the longer 30 mm stands, and the original short stands hold the driver off the plate "to allow some clearance between the platform and the fan intake" (MDDS30 manual Rev 1.3, section 9). So the driver gets taller, and the plate under it must stay open for intake air. Measure the final height once a fan is fitted.
3. **Keep logic and RF away from the drivers.** MDDS30s switch at 18 kHz with tens of amps; put the Teensy, CAN transceivers, Jetson and radios on the other side of the bay. Cross motor cables and signal cables at 90 degrees where they must cross.
4. **CAN as one line.** Teensy CAN board and Jetson J17 close together; the bus is a line, not a star, with 120 ohm termination only at the two ends.
5. **Jetson gets free air.** Its fan heatsink needs open space above it; do not put it under a shelf or next to the drivers.
6. **RF at the edge.** RFD900x near its antenna feed-through, so the coax is short. Ethernet to the Groove on the mast leaves through a bulkhead.
7. **Vibration.** Every board on standoffs; locking connectors (not bare 0.1 inch headers) on anything that leaves a board; strain relief at each gland.
8. **Each subsystem board removable on its own.** Every board connects through connectors, not soldered wires, so one board can be pulled for repair without unwiring the others. This is the "access" part of the task.

## 4. Access from the outside

| What must be reachable | How |
|---|---|
| E-stop, start button | Exterior panel (rule 2.a.v) |
| Blade fuses (F1-F5) | Fuse block right behind the access panel, so a blown fuse is changed without removing boards |
| Teensy USB, Jetson USB / Ethernet / display | Panel-mount USB and RJ45 extension jacks on the bulkhead, so firmware can be flashed with the lid closed |
| Battery | Own bay, swappable without opening the electronics bay |
| Arm and science modules | One power + CAN connector each at the bay wall (quick-disconnect) |
| Status | RGB status LED (Comms/Navi list) visible from outside |
| Whole bay | Lid or front panel on captive screws; harnesses labelled at both ends |

## 5. Mid-November drivetrain prototype: bench board

The prototype runs open-frame, so the "layout" is a test board, not the rover bay. Suggested arrangement on one plywood or acrylic board (~600 x 400 mm **EST**):

```
 FRONT EDGE (operator side)
 [E-STOP] [START]                                  [12V/5V test points]
 +--------------------------------------------------------------------+
 | battery leads -> Class T fuse -> contactor + pre-charge -> fuse block|
 |                                                                    |
 |   MDDS30 #1      MDDS30 #2      MDDS30 #3        DDR-60G   D36V28F5 |
 |   (LF, RF)       (LM, RM)       (LR, RR)                            |
 |                                                  Teensy + CAN board |
 |                                                  Jetson             |
 +--------------------------------------------------------------------+
   motor terminal blocks / Anderson connectors along the BACK EDGE
```

- Power flows left to right, logic stays on the right, motors leave from the back edge.
- E-stop on the front edge where the person running the test can hit it.
- Same zone idea as the real bay, so the wiring lengths learned here carry over.

## 6. Open items

- [ ] Chassis and electronics box size, material, and where the battery bay is (mechanical team)
- [ ] Board size and connector list from each subsystem owner (Bryan, Paul, Krishna, Ricky, Kaden; Comms/Navi is mine)
- [ ] Contactor, Class T holder, fuse block, pre-charge part numbers (Lance) to fill in zone 1 sizes
- [ ] Waveshare SN65HVD230 board size from its STEP model
- [ ] Confirm the L-com switch size from L-com's drawing
- [ ] Decide whether arm MCCs live on the arm or in the bay (Ricky, Lance)
- [ ] Coordinate with Krishna: Task 4 lists him on the Drivetrain schematic, and the mid-November prototype schematic is mine
- [ ] Build a 1:1 paper or CAD mock-up of zone 1 once the power parts are chosen

## Sources

- URC 2027 Requirements and Guidelines, rules 2.a.ii, 2.a.iii, 2.a.v, 3.d.iii (repo root PDF)
- Task 4 spreadsheet (team Drive), TasksStatus, Components and Power Rail Table tabs, read 2026-10-27
- Cytron MDDS30 User's Manual Rev 1.11, p.4 dimensions: https://forum.dronebotworkshop.com/wp-content/uploads/wpforo/attachments/5360/6077-MDDS30UserManual.pdf
- Cytron MDDS30 User's Manual Rev 1.3 (October 2026), section 9 "Assemble Optional Fan": Google Doc linked from the Task 4 spreadsheet, TasksStatus, Cooling row
- NVIDIA forum, Orin Nano dev kit mechanical dimensions (quotes the datasheet): https://forums.developer.nvidia.com/t/mechanical-dimensions-jetson-orin-nano-development-kit/316529
- JetsonHacks Orin Nano dev kit review (measured with base): https://jetsonhacks.com/2023/03/22/nvidia-jetson-orin-nano-developer-kit-the-perfect-solution-for-makers-and-developers-a-review/
- Mean Well DDR-60 datasheet: https://www.meanwell.com/Upload/PDF/DDR-60/DDR-60-SPEC.PDF
- Pololu D36V28F5: https://www.pololu.com/product/3782
- PJRC Teensy 4.1 dimension drawing: https://www.pjrc.com/teensy/dimensions_teensy41.png
- RFD900x datasheet v1.1: https://cdn.hackaday.io/files/276031180966752/RFD900x%20DataSheet.pdf
- Netgear GS105NA size (retailer): https://www.fullcompass.com/prod/203071-netgear-gs105na-5-port-gigabit-ethernet-desktop-switch
