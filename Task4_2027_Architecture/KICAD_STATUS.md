# KiCad Status: What Exists and What Is Still Needed

Checked 2026-11-09. Read-only: no .kicad_sch file was edited. ERC and netlist were run into a scratch folder.

## 1. What exists now

### Team repo (Paul-ECE/2027-UH-URC-Power), read via the public GitHub API

| File | Owner | State |
|---|---|---|
| `2027_URC_PowerDist_Schematics.kicad_sch` (root) | Paul, 10/13 | Title "2027 UH URC Power Distribution Architecture". 6 sheet symbols: Drivetrain, Compute_logic, Science Package, Power Distribution Panel, Communication_Navigation, Robotic Arm |
| `Comms_navi.kicad_sch` | Chris | **Empty** (title block only, 240 bytes) |
| `Compute_logic`, `Drivetrain`, `PDP`, `RoboArm`, `SciPkg` `.kicad_sch` | Paul, Krishna, Bryan, Ricky, Kaden | **All empty** |
| `.kicad_pcb` | | Empty |
| `URC_2027_Science_Rev5_FIXED_KiCad.zip` | Kaden, 10/28 | Separate draft, not in the shared project. Placeholder symbols (`SCI_DRAFT:*`), local labels only, no global labels. Its README says "NOT FABRICATION READY" and that ERC was not run |

The root project is probably the base for Toka's "shared KiCad". It has one sheet per subsystem and no cooling sheet.

### Team Drive

- `_2.2.3.2.6_Kicad_Schematic_Versions`: README only. It asks for one folder per KiCad sheet with dated screenshots.
- `_2.2.3.2.5_Component_Datasheets`: README and 5 empty folders (Power Distribution, Arm, Science, Drive, Protection). No Comms/Navi folder. The README says: use wires on the same board, and global tags only for off-board connections.
- No KiCad files yet. Toka's shared KiCad has not been posted.

### Chris's local drawing: `E:\UH_Robotic_Mars_Rover\Task4_Power_Design\Comms_Navi_2027\` (10/23, not in git)

**Update 2026-11-16:** this local copy is now a backup only. The master copy is `Integration/Comms_Navi.kicad_sch` (global labels instead of hierarchical labels). Edit only the repo copy.

Root `Comms_Navi_2027.kicad_sch` plus one sub-sheet `comms_navi.kicad_sch` and its own symbol library `comms_navi.kicad_sym` (LSM6DSV).

| Block | Parts drawn | Connections (from the netlist) |
|---|---|---|
| Power input | J1 Conn_01x04 (Phoenix 5.08): +12V, GND, +5V, GND; PWR_FLAG x3 | +12V and +5V use power symbols |
| 12 V loads | J2 switch, J3 PoE injector, J5 LiDAR (Conn_01x02 each) | Straight on +12V, **no fuses** |
| RGB LED | J4 Conn_01x04; F1 2 A; Q1-Q3 AO3400A; R1/R3/R5 100R; R2/R4/R6 100k | +12V -> F1 -> J4 pin 1; Q1-Q3 drains to J4 pins 2-4 |
| 5 V loads | J6 RFD900x (JST XH 1x04), J7 USB hub, J8 GPS (JST XH 1x04); C1 100uF | Straight on +5V, **no fuses**; RFD900x on the 5 V rail |
| IMU | U2 LSM6DSV (bare chip, LGA-14); U1 AP2112K-3.3; C2/C3 1uF; C4/C5 100nF; R7/R8 4.7k | 5V -> U1 -> +3V3_IMU; CS to 3V3 (I2C mode); SA0 to GND (address 0x6A) |
| Off-sheet signals | 10 **hierarchical** labels with directions | GPS_TX out, GPS_RX in, RFD_TX out, RFD_RX in, LED_R/G/B in, IMU_SDA bidir, IMU_SCL in, IMU_INT1 out |

ERC: 18 violations, all 18 excluded with the note "Waiting for Compute/Logic sheet" (10 sheet pins not connected, 8 labels with only one pin). Nothing else.

### Chris's personal repo (`Task2_Old_Architecture_Flowchart_Schematic`)

Old Task 2 architecture (RPLIDAR S2 + SparkFun RTK GPS, Ricky's old arm servo sheet). Keep it as a record. It is not the 2027 design.

## 2. What the 10/23 drawing still needs (Chris)

| # | Item | Why |
|---|---|---|
| 1 | Change the 10 hierarchical labels to **global labels** (Ctrl+L) and keep the same directions | Team rule (Toka, Bryan): off-board connections use global labels with Input/Output set. Directions are already set correctly |
| 2 | Agree the label names with Paul (GPS_TX, RFD_TX, LED_R...) | Global labels only connect if the names match exactly |
| 3 | Ask Bryan: +12V/+5V as power symbols or as global labels (`+12V_SW`)? | Power symbols are global across the whole project, so names must match the PDP sheet too |
| 4 | Add fuses F2-F7 (switch, PoE, LiDAR, RFD regulator, USB hub, GPS+IMU) | Only the LED has a fuse now; see the fuse table in COMMS_NAVI_SCHEMATIC_PLAN.md |
| 5 | Add a 12 V -> 5 V regulator for the RFD900x, fed from +12V, and move J6 onto it | RFD900x datasheet V1.2: 5.0 V minimum. On the shared 5 V rail any drop puts it out of spec |
| 6 | Move C1 (100uF) to the RFD900x supply | Covers the 1 A TX bursts |
| 7 | Add test points (`Connector:TestPoint`) | Task 4 asks for test locations; list in plan section 6 |
| 8 | Check LSM6DSV unused pins (SDx/SCx tied to GND, INT2/OCS_Aux/SDO_Aux open) against the ST datasheet | Not verified yet |
| 9 | Optional: wire GPS PPS | For time sync later |
| 10 | Copy the sheet into the shared project's `Comms_navi.kicad_sch` once Toka posts it | Shared project already has a Comms/Navi sheet slot |
| 11 | Put the project into git (personal repo) | It is untracked in the main checkout, so it has no backup |

## 3. What Chris must upload to the Drive

- [ ] `_2.2.3.2.6_Kicad_Schematic_Versions/Comms_Navi/`: a screenshot of the sheet, named with the date (e.g. `comms_navi_2026-11-09.png`)
- [ ] `_2.2.3.2.5_Component_Datasheets/Comms_Navi/`: datasheets for RFD900x, PA1616S, LSM6DSV, AP2112K, AO3400A, switch, PoE injector
- [ ] `Comms_Navi_Components.xlsx` (component list for Toka)
- [ ] Updated `PHYSICAL_LAYOUT.docx` (the one on the Drive still has the old fan text) and the two layout figures

## 4. Cooling in KiCad

The cooling parts (bay fan + 2N7002, DS18B20 probes + 4.7k, fan fuse) from COOLING_PLAN.md section 5 are not drawn anywhere. They connect to the Teensy (pins 32, 10, 11 proposed). The shared project has no cooling sheet. **Ask Tyler** whether they go on the Compute/Logic sheet (Paul), the PDP sheet (Bryan), or a new Cooling sheet that Chris draws.

## 5. Team-wide gaps (not Chris's to fix, but they block the global labels)

- Compute/Logic (Paul) is empty, so none of the Comms/Navi global labels have a partner yet.
- PDP (Bryan) is empty, so the power input names are not fixed yet.
- Drivetrain (Krishna said 10/28) and Robo Arm (Ricky) are not in the shared repo.
- The team has no global label naming list yet. A shared table (label, owner sheet, direction on each side) would stop name mismatches.
