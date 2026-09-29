# URC Mars Rover: Project Overview and Progress

Last updated: September 29, 2026

## 1. Project purpose

This project supports a university rover team preparing a robotic rover for the University Rover Challenge (URC). The work covered here focuses on the rover's electrical power system: battery selection, load calculations, voltage distribution, circuit protection, modular interfaces, and translation of system flowcharts into KiCad schematics.

The rover must power its drive and other actuators, onboard computer, controller, sensing, navigation, and communications equipment. The electrical design must fit the mechanical installation, deliver operating and transient loads, and support the mission duration and competition requirements.

**Rules reference:** the official **URC 2027 Requirements and Guidelines** (published September 2026, competition June 2–5, 2027) replaces the team-supplied 2026 guideline as the rules reference. The review is in [URC_2027_Rules_Review.md](URC_2027_Rules_Review.md). URC Q&A amendments still need to be checked.

## 2. My contribution

I am Chris. My initial responsibility was researching battery options rather than drawing the team's flowchart. The work has since expanded into organizing electrical loads, learning KiCad, and owning the **lidar + navigation subsystem schematic** (see Section 9).

The main selection priorities are:

1. **Voltage:** nominal, fully charged, and operating voltage range, with compatibility across connected equipment.
2. **Dimensions:** battery length, width, height, mounting space, and connector clearance.
3. **Power:** continuous output, peak output, peak duration, and load requirements.
4. **Architecture:** battery configuration, voltage rails, power distribution, protection, and subsystem interfaces.

Energy in Wh and capacity in Ah are also needed to estimate runtime. Power in W and energy in Wh are different quantities.

## 3. Design references and their relationship

### Task 2 report: accepted report baseline

The team member explicitly confirmed that **URC Task 2 Report.pdf** is the current report baseline. Its proposed system includes:

- A single main battery bus using a 6S battery configuration.
- A 6S LiPo sizing basis of 22.2V nominal and 25.2V fully charged.
- A 10–12Ah LiPo or 21700 NMC battery direction. The conclusion proposes two 10Ah packs for swapping between mission heats.
- A regulated 12V rail proposed at 8A and a regulated 5V rail proposed at 6A.
- STM32H743ZI / NUCLEO-H743ZI2 control hardware.
- Eight Pololu #4693 24V 37D motors and eight Pololu G2 24v13 drivers.
- Jetson Orin Nano Super Dev Kit, Ouster OS0, OAK-D Pro W, GNSS, networking, fans, and monitoring devices.
- Proposed BMS, power monitoring, and cutoff/protection hardware.

These are report proposals and estimates. The report alone does not establish completed procurement, assembled hardware, or measured system performance. The report's LiPo and NMC voltage/capacity assumptions must be reconciled for the exact selected pack.

Under the 2027 rules, the report's 45-minute mission basis and 10–12Ah pack size need revisiting (Section 8).

### Latest Canva-to-KiCad assignment

The latest screenshot supplied for schematic translation shows a different component set: **Adafruit Feather, Jetson, RDLidar, SparkFun GPS-RTK-SMA, arm servos, and Smart Drive motor blocks**, among other items.

This screenshot is the visual reference for the current KiCad teaching task. It must remain distinguishable from the STM32/Ouster report configuration. The report's load totals cannot automatically be assigned to the pictured architecture.

The screenshot is cropped. Complete connections, device variants, pinouts, and the color legend have not been established. Automated web access to the Canva view link failed; only the supplied screenshot was inspected. This does not establish whether team members can access the link in their browsers.

Interpretation decisions for the lidar + navigation block (Chris's own decisions, not confirmed by the team lead):

- "RDLidar" is taken to be a Slamtec RPLIDAR. The **RPLIDAR S2** was selected for its DTOF ranging, outdoor/IP65 rating, 5V supply, 3.3V TTL UART, and ROS 2 support. Pin order and current draw must be taken from the Slamtec datasheet.
- The GNSS antenna connects to the GPS-RTK-SMA board through SMA coax, not to the Jetson as the flowchart arrows suggest.
- 5V is drawn from the Jetson, as the flowchart shows. The Task 2 Report instead places sensors on the 5V buck rail. The schematic uses a +5V power symbol, so the source can change without redrawing the sheet.

## 4. Work completed and progress recorded

| Work item | Status | Evidence or limitation |
|---|---|---|
| Battery research | Completed initial comparison | Six candidate packs compared, with prices/specifications as of September 15, 2026 |
| English battery workbook | Created and checked | Workbook contains comparison, runtime calculator, rules, and team evidence sheets. Its rules sheet still cites 2026 section numbers |
| URC 2026 rule review | Completed initial review | Based on the user-supplied 2026 guideline |
| **Battery swap report (URC 2027)** | Drafted, pending review | Excel with 7 sheets: summary, comparison, pros & cons, swap calculator, tier list, rules, 12-team survey. Tattu 6S 30Ah ranks tier S at the 350 W placeholder load |
| **URC 2027 rule review** | Completed | Official 2027 PDF downloaded and archived locally. Comparison against 2026 uses the workbook's 2026 summary; the full 2026 PDF was unavailable |
| Other rover team research | Completed initial review | Team examples support chemistry/architecture choices, not adoption of the exact shortlisted products |
| Task 2 report archive | Completed | Original PDF copied into the project root and identical file hashes checked |
| Task 2 report review | Completed | All 12 pages reviewed, including power tables, architecture, battery sizing, and protection proposals |
| Load-list and rail calculations | Walked through in conversation | Tables, formulas, and example results are recorded below; the user's working spreadsheet has not been inspected |
| KiCad master project | Created | `Task2_Flowchart_Schematic/` with root sheet and project-specific symbol library `rover_modules` |
| **Lidar + navigation schematic** | Completed, ERC 0 errors | `lidar_navigation.kicad_sch`. Remaining violations are excluded because the Jetson sheet does not exist yet |
| Git repository | Published (private) | `github.com/Cd1314520/urc-mars-rover-schematic`. Repo root is the project folder: docs at root, `Task1_Battery/`, `Task2_Flowchart_Schematic/`. Excel files are git-ignored. Collaborator invites not verified |
| Canva edits | None performed by the assistant | Flowchart work belongs to the team's assigned contributors |

The user progressed through the calculation tutorial by requesting each next step. This records tutorial progress; it is not proof that each step has been saved in a separate workbook or checked in Excel.

## 5. Initial battery research

The comparison included:

- Tattu G-Tech 6S 30Ah LiPo.
- Tattu G-Tech 6S 22Ah LiPo.
- LiTime 24V 50Ah LiFePO4.
- Bioenno BLF-2430A.
- Turnigy High Capacity 6S 20Ah LiPo.
- MaxAmps 6S2P 22Ah LiPo.

The initial research favored validating the Tattu 30Ah pack for a weight/energy compromise, with LiTime 50Ah as a heavier endurance alternative. That work preceded acceptance of the Task 2 report's 10–12Ah direction. The 2027 runtime check (Section 8) brings the 20–30Ah class back into consideration.

No final battery purchase, dimensions, connector selection, or installed mass has been confirmed.

Team evidence covered Georgia Tech RoboJackets, UIU AURION, Iowa State MAVRIC, WeMars, and AGH Phobos. The workbook records sources and limitations for these examples.

## 6. Report-based calculations covered so far

### 6.1 Component load inventory

All values below were transcribed from report pages 2–3. They have not been independently verified against each manufacturer's documentation or measured on the rover.

| Component/group | Quantity | Continuous min W | Continuous max W | Listed peak W | Power basis |
|---|---:|---:|---:|---:|---|
| Jetson Orin Nano Super Dev Kit | 1 | 15 | 20 | 25 | Per device |
| STM32 NUCLEO-H743ZI2 | 1 | 0.3 | 0.5 | 1.65 | Per board |
| Ouster OS0 | 1 | 14 | 18 | 23 | Per device |
| OAK-D Pro W | 1 | 5 | 8 | 15 | Per device |
| ZED-F9P-05B GNSS | 1 | 0.33 | 0.33 | 0.85 | Per listed unit |
| Moxa EDS-205 | 1 | 0.5 | 0.5 | 0.77 | Per device |
| Two Noctua fans, INA228, TMP117 | 4 grouped items | 0.51 | 0.51 | 0.52 | Whole group |
| Pololu motors | 8 | 120 | 200 | 576 | Whole group |
| Pololu driver losses | 8 | 12 | 20 | TBD | Whole group, losses only |
| **Total / listed subtotal** | | **167.64** | **267.34** | **642.79** | **Peak is incomplete** |

Group totals must not be multiplied by quantity again. The peak subtotal excludes unspecified peak driver losses. A spreadsheet SUM ignoring a TBD cell does not make that subtotal complete.

**Loads not yet in this list:**

| Load | Why it matters |
|---|---|
| Arm actuators | Objects up to 5 kg (1.c.iii, 1.d.ii) |
| Astrobiology instruments | Life detection required (1.b.v) |
| Rover-side radios | Needed for comms |
| Autonomy LED indicator | Required by 1.e.ii |
| RPLIDAR S2 | Canva architecture only; replaces the report's Ouster OS0 there |

### 6.2 Provisional rail grouping and current

| Rail/group | Assigned loads | Min W | Max W | Listed peak W | Min A | Max A | Listed peak A |
|---|---|---:|---:|---:|---:|---:|---:|
| Regulated 12V | Jetson + Ouster + Moxa | 29.5 | 38.5 | 48.77 | 2.46 | 3.21 | 4.06 |
| Regulated 5V | STM32 + OAK-D | 5.3 | 8.5 | 16.65 | 1.06 | 1.70 | 3.33 |
| Main bus | Motors + driver losses | 132 | 220 | 576, incomplete | — | — | — |
| Rail assignment pending | GNSS + fans/monitoring group | 0.84 | 0.84 | 1.37 | — | — | — |

Formula: **rail current A = rail power W / regulated rail voltage V**.

For example, the 12V maximum continuous current is `(20 + 18 + 0.5) / 12 = 3.21A`. These are calculated output currents, not measured currents or battery currents. Peak calculations assume the listed peaks coincide.

The camera is counted on the 5V rail provisionally. If it is powered through Jetson USB, its upstream power path and potential overlap with Jetson power figures must be reconciled. The mixed GNSS/fan/monitoring entries need actual rail assignments. The Canva flowchart places the GNSS on 5V.

### 6.3 Battery-side continuous power

A provisional **90% DC-DC efficiency** was introduced as a planning assumption, not a verified converter specification.

Formula: **battery input power = converter output load power / efficiency**.

| Group | Min battery-side W | Max battery-side W |
|---|---:|---:|
| 12V loads, divided by 0.90 | 32.78 | 42.78 |
| 5V loads, divided by 0.90 | 5.89 | 9.44 |
| Motors and already-listed driver losses | 132.00 | 220.00 |
| Unassigned auxiliaries, provisionally divided by 0.90 | 0.93 | 0.93 |
| **Total** | **171.60** | **273.16** |

No additional buck loss was applied to the direct motor branch. This does not imply 100% motor/driver efficiency; the report's driver losses are already included. Wiring and other unlisted losses are not separately quantified. Full battery-side peak power has not been established.

### 6.4 Runtime estimates

Assumptions: 22.2V nominal LiPo voltage, **80% usable energy**, and the battery-side continuous-power estimates above. The 80% allowance is a separate planning assumption from converter efficiency. No additional 35% report margin was stacked on top of it.

| Candidate capacity | Nominal Wh | Usable Wh at 80% | Minutes at 171.60W | Minutes at 273.16W |
|---|---:|---:|---:|---:|
| 6S LiPo 10Ah | 222.0 | 177.60 | 62.1 | 39.0 |
| 6S LiPo 12Ah | 266.4 | 213.12 | 74.5 | 46.8 |

Formulas:

- `Nominal Wh = Nominal V × Ah`
- `Usable Wh = Nominal Wh × Usable Energy Fraction`
- `Runtime min = Usable Wh / Battery-Side W × 60`

Converter loss must not be applied again to these battery-side power values. Runtime estimates assume a sustained average load at the chosen level. Neither candidate establishes a 60-minute mission capability across the entire estimated load range.

## 7. Findings to carry into implementation

These findings refine the accepted report baseline; they are not instructions to replace its architecture. Section references are to the 2027 rules.

- **Mission duration:** the report uses 45 minutes. Delivery allows 30–60 minutes on course (1.c.i). Autonomy is now 40 minutes (1.e.i), and Equipment Servicing may start as soon as 10 minutes after Autonomy ends (1.a.iv, 1.d.i). Setup allows 15 minutes (1.a.ii).
- **Battery swaps:** a swap during a mission is an intervention with a 20% penalty (3.e.vii–viii). A swap between missions is allowed (1.a.v), but the Autonomy → Equipment Servicing gap may be only 10 minutes.
- **Runtime margin:** the report's 66.6-minute result for 10Ah at 200W uses all 222Wh of nominal energy. It is not a demonstrated mission runtime.
- **Discharge requirement:** 30C for a 10Ah pack corresponds to 300A. The report does not explain why that minimum follows from its estimated load.
- **Undervoltage thresholds:** the report lists a 19.8V cutoff in sizing and 3.0V/cell, or 18V for 6S, in the BMS section. Normal shutdown and emergency protection thresholds need explicit roles.
- **Emergency stop:** 2.a.v requires a red **push button, not a knob or rotating switch**. It must cut all power draw from all batteries, including in a battery fire, and a single E-stop must switch off all systems. The report's mechanical switch + 100A fuse does not meet this.
- **Budget:** the fielded-system cap is **$26,000** (3.c.iii, up from $24,000). It includes rover power sources, the drone, EVA suit, and C2 equipment, plus shipping and tax.
- **Stowed size:** the rover must fit a 1.2 m cube including antennas (2.a.ii), or take a 40% penalty. GNSS and radio masts must fold.
- **Dimensions:** no final pack envelope or mechanical installation dimensions have been established.
- **Protection ratings:** proposed BMS and fuse values need coordination with actual pack, wires, connectors, converters, and load transients.
- **Load coverage:** arm, steering, science, wireless communications, the Autonomy LED indicator, and other auxiliary loads are not yet in the list.

Unknowns are recorded as TBD so work can continue without inventing values.

## 8. Battery plan under URC 2027

### 8.1 Energy targets

Rated Wh needed at 80% usable energy:

| Average battery-side load | 60-min Delivery | 70-min Autonomy + Equipment, no swap, plus 10 min at 60W standby |
|---|---:|---:|
| 273 W (report high estimate) | 341 Wh | 411 Wh |
| 350 W (report high + ~28% for unlisted loads, placeholder) | 438 Wh | 523 Wh |
| 500 W (workbook example) | 625 Wh | 742 Wh |

The 350W and 500W rows and the 60W standby are planning placeholders, not measurements.

### 8.2 Runtime by pack, 80% usable energy

| Pack | Usable Wh | Min at 273 W | Min at 350 W | Min at 500 W | Mass kg |
|---|---:|---:|---:|---:|---:|
| Report 6S 10Ah | 177.6 | 39.0 | 30.4 | 21.3 | ~1.35 (report est.) |
| Report 6S 12Ah | 213.1 | 46.8 | 36.5 | 25.6 | ~1.60 (report est.) |
| Turnigy 6S 20Ah | 355.2 | 78.0 | 60.9 | 42.6 | 2.63 |
| Tattu 6S 22Ah / MaxAmps 6S 22Ah | 390.7 | 85.8 | 67.0 | 46.9 | 2.46 / 2.48 |
| **Tattu 6S 30Ah** | 532.8 | 117.0 | 91.3 | 63.9 | 3.5 |
| Bioenno 24V 30Ah | 576.0 | 126.5 | 98.7 | 69.1 | 7.2 |
| LiTime 24V 50Ah | 1024.0 | 224.9 | 175.5 | 122.9 | 9.6 |

### 8.3 Working proposal (for team review)

- **Primary pack:** one 6S LiPo in the 22–30Ah class. The report's 10–12Ah does not cover 60 minutes at its own high estimate.
  - **Tattu 30Ah** is the first to validate. It covers setup + the 60-min Delivery up to about 518 W, and the 70-min Autonomy + Equipment block without a swap up to about 435 W (with 60 W standby for setup and the gap). See `Task1_Battery/URC_2027_Battery_Swap_Report.xlsx` (local only, not in Git).
  - It keeps the report's 6S voltage (25.2V max), so drivers and bucks are unchanged.
- **Second identical pack** for swaps between missions or days. Use a quick-disconnect connector and an accessible pack bay, and rehearse the swap to fit inside 10 minutes.
  - Confirm with URC whether a second pack used in rotation counts toward the $26,000 cap. The exclusion in 3.c.v covers only one-for-one damage replacements.
- **Protection:** the Tattu pack has no internal BMS. Plan for:
  - a fuse at the battery
  - a red latching push-button E-stop driving a main contactor that cuts all battery output
  - an external BMS or monitor with undervoltage cutoff
  - the INA228 telemetry already proposed in the report
- **Heavier fallback:** LiTime 50Ah only if the mass budget allows. It is 9.6 kg, about 19% of 50 kg, and its 50A BMS is less than the report's 30C target.
- **Gate before purchase:** complete the new-architecture load list, measure average and peak loads, and run a mission-length test.

## 9. Team task sequence and current KiCad progress

The latest team message gives this sequence:

1. Edit the original circuit architecture.
2. Translate the original architecture into KiCad.
3. Calculate loads for the new architecture.
4. Create the new architecture flowchart.
5. Translate the new architecture into KiCad.

The team requested familiarity with KiCad by Wednesday/Thursday and aimed for the original schematic before the following Monday meeting. Items 4–5 could continue into the following week. The exact calendar deadlines were not confirmed here. The **PDR on December 2, 2026** needs the current state of design, which sets a later hard deadline.

Subsystem assignments from the team recap:

- **Krishna:** drivetrain subsystem schematic.
- **Chris:** lidar + navigation subsystem schematic.

KiCad status (KiCad 10.0.6), project `Task2_Flowchart_Schematic/`:

- **Root sheet** holds one hierarchical sheet per subsystem.
- **`lidar_navigation.kicad_sch`** is complete:
  - U1 RPLIDAR_S2, U2 SparkFun GPS-RTK-SMA, AE1 antenna
  - +5V/GND power symbols with PWR_FLAGs
  - hierarchical labels LIDAR_TX, LIDAR_RX, GPS_SDA, GPS_SCL, matched to sheet pins on the root
- **Planned Jetson 40-pin connections:** LIDAR_TX → pin 10, LIDAR_RX → pin 8, GPS_SDA → pin 3, GPS_SCL → pin 5.
- **ERC:** 0 errors. Unconnected sheet pins, the undriven lidar RX input, and single-pin label warnings are excluded until the Jetson sheet exists. When it does:
  - remove those exclusions
  - move the PWR_FLAGs to the sheet that actually sources power
- **Custom symbols** are in project library `rover_modules.kicad_sym`, registered in the project `sym-lib-table`.
- **Git:** repository initialized with a team workflow README. Each member edits only their own sheet; the root sheet and symbol library are edited one person at a time.

The next useful work:

- obtain the complete flowchart
- add the remaining subsystem sheets and the Jetson interface sheet
- specify the E-stop/contactor circuit on the power sheet
- place the Autonomy LED indicator in the new architecture

The bulk capacitor and TVS blocks need real circuit connections; the flowchart arrows alone do not specify them. Unknown model details and pin assignments remain TBD.

## 10. Files and references

### Verified local files

- [Task 2 report](Task1_Battery/URC%20Task%202%20Report.pdf)
- [URC 2027 Requirements and Guidelines](URC%202027%20Requirements%20and%20Guidelines.pdf) (official PDF, downloaded September 29, 2026)
- [URC 2027 rules review](URC_2027_Rules_Review.md)
- `Task1_Battery/URC_Rover_Battery_Comparison.xlsx`: initial battery comparison workbook (local only, not in Git; dated September 15, 2026. A SharePoint copy exists; any online edits were not inspected)
- `Task1_Battery/URC_2027_Battery_Swap_Report.xlsx`: URC 2027 battery swap report with pros/cons, tier list, swap calculator and team survey (local only, not in Git)
- [KiCad project](Task2_Flowchart_Schematic/Task2_Flowchart_Schematic.kicad_pro)

The separate `Task_2_Power_Load_List.xlsx` discussed in the tutorial was a suggested user-created file. It was not found in this workspace.

### Team flowchart links

- [Team's new flowchart short link](https://canva.link/serjms94xbzgbdh)
- [Latest supplied Canva view](https://www.canva.com/design/DAHVOCROqQ0/0B4g02gMw_OpIs9eN6DTnw/view)

### Learning and competition references

- [KiCad 9 Schematic Editor documentation](https://docs.kicad.org/9.0/en/eeschema/eeschema.html)
- [URC requirements and guidelines landing page](https://urc.marssociety.org/home/requirements-guidelines)

## 11. Current status in one paragraph

The project has an archived and reviewed Task 2 power report, an initial battery research workbook, a documented calculation path from component loads to battery runtime, and a review of the official URC 2027 rules. The 2027 rules call for a 60-minute Delivery basis, a 40-minute Autonomy mission followed closely by Equipment Servicing, and a stricter push-button E-stop. These point the battery choice back toward the 22–30Ah 6S class with a quick-swap second pack. The lidar + navigation KiCad subsystem is drawn and passes ERC within the master project, which is under local Git version control. Final battery selection, the new-architecture load list, the E-stop circuit, remaining subsystem sheets, measured loads, and integration testing remain outstanding.
