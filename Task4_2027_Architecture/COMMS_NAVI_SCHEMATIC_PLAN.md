# Comms/Navi Subsystem: 2027 Schematic Plan

Task 4 main task (Task 4 spreadsheet, TasksStatus, Chris row): "Draft subsystem schematic for 2027 architecture. For respective subsystem: define PCB (see Task 4, pg 2), define board to board/harness interface locations, choose components as needed (refer to Systems Trade Study), identify high current and heat components, and determine test locations."

Status: draft, 2026-11-02. Step 1 (components) and step 2 (rail currents) were done on 10/19 in the Task 4 spreadsheet ("Comms Navi" tab and Power Rail Table). This plan covers the remaining steps. Values marked **EST** are estimates; **TBD** needs a part choice or a number from another owner.

I have not read "Task 4, pg 2", so check its PCB definition against section 2.

## 1. Why a new schematic

The current KiCad sheet, `Task2_Old_Architecture_Flowchart_Schematic/lidar_navigation.kicad_sch`, belongs to the **original (Task 2) architecture**. It does not match the 2027 component list:

| Item | Current sheet (Task 2) | 2027 list (Task 4, 10/19) |
|---|---|---|
| GPS | SparkFun GPS-RTK-SMA, I2C | Adafruit Ultimate GPS PA1616S, UART |
| LiDAR | RPLIDAR S2, UART | TBD (plan worst case 12 V 3 A) |
| Power | From the Jetson 40-pin 5 V pins (2 and 4) | "5V made on main power board; harness to Comms/Navi board" |
| Radio, network, IMU, RGB LED | Not drawn | RFD900x, switch, PoE injector, LSM6DSV, RGB LED |

Keep the Task 2 project unchanged as the record of the old architecture, and start a new project for 2027 (section 4).

## 2. Board definition

**Comms/Navi board** = one small interface PCB in zone 3 of the electronics bay ([PHYSICAL_LAYOUT.md](PHYSICAL_LAYOUT.md)). Its jobs:

1. Take +12 V and +5 V from the main power board (PDP, Bryan) over one harness.
2. Fuse each Comms/Navi load separately.
3. Give every off-board module its own connector: power, plus data where the data goes to the Teensy or the Jetson.
4. Carry the parts that cannot live on a cable: the RFD900x 5 V regulator, the RGB LED MOSFET, the IMU, and test points.

Not on this board: the antennas, the Groove 52ac (on the mast), the cameras (USB to the hub), the HaLow card (in the Jetson M.2 slot) and the Ethernet cables (plugged module to module).

### Board-to-board / harness interfaces

| Connector | Goes to | Carries |
|---|---|---|
| J_PWR_IN | Main power board (PDP) | +12V_SW, +5V_SW, GND (both downstream of the contactor, so OFF on E-stop, URC 2.a.v) |
| J_JETSON | Jetson 40-pin header J12 | GPS UART (pins 8/10), IMU I2C (pins 3/5), GND (pin 6) |
| J_TEENSY | Compute/Logic board (Paul) | RFD900x UART, RGB LED control, GND |
| J_SW_PWR, J_POE_PWR, J_LIDAR_PWR, J_LED, J_USBHUB_PWR | Each module | Fused power |
| J_RFD, J_GPS | RFD900x, PA1616S | Power + UART |

## 3. Parts and verified facts

### Facts checked against datasheets

- **RFD900x** (RFDesign datasheet V1.2):
  - Supply: "+5V nominal (+5V min, +5.5V Max, +6V ABS Max)".
  - Current: "1A peak at 30dBm", 60 mA receive.
  - 16-pin header: 1 GND, 2 GND, 3 CTS (in), 4 Vcc, 5-6 Vusb, 7 RX (in), 8 GPIO5, 9 TX (out), 10 GPIO4, 11 RTS (out), 12-15 GPIO, 16 GND. All signals are 3.3 V max.
  - Power entry: "connect the power to pins 2 (GND) and 4 (+5V)".
  - Default serial: 57600 baud, 8N1.
- **Adafruit Ultimate GPS, PA1616S** (Adafruit product 746 and learn guide):
  - Pins: VIN, GND, VBAT, EN, 3.3V, TX, RX, FIX, PPS.
  - VIN 3.0-5.5 V (product page). The learn guide says 3-5 V, so stay at 5 V.
  - TX is 3.3 V logic, 9600 baud default. RX is a "5V-safe input".
  - EN is pulled high by 10k; pulling it to ground turns the GPS off. PPS gives one 3.3 V pulse per second.
- **Jetson J12** (JetsonHacks pinout, "Preliminary"): pin 3 I2C1_SDA, pin 5 I2C1_SCL (I2C bus 7), pin 8 UART1_TX, pin 10 UART1_RX (`/dev/ttyTHS0`), pin 1 3.3 V, pins 2/4 5 V, pin 6 GND. The I2C/UART voltage level and on-board pull-ups are **not confirmed** from NVIDIA; check the Orin Nano carrier board spec.
- **Teensy 4.1 serial ports** (PJRC UART page): Serial2 RX 7 / TX 8, Serial3 RX 15 / TX 14, Serial4 RX 16 / TX 17, Serial5 RX 21 / TX 20, Serial6 RX 25 / TX 24, Serial7 RX 28 / TX 29.

### Two flags for the Task 4 sheet

1. The Comms Navi tab lists the RFD900x at "1.2 A TX peak". Datasheet V1.2 says 1 A peak at 30 dBm. Keep 1.2 A as the margin for fuse sizing, but fix the source note.
2. RFD900x minimum supply is **5.0 V**, so any drop in the fuse, wire or connector takes it out of spec. This is why the Task 4 list says "own 5V supply". Give it its own 12 V -> 5 V regulator on this board, close to J_RFD, and measure Vcc at the modem during a TX burst. It must be fed from **12 V**, not from the 5 V rail: a regulator cannot hold 5.0 V out of a 5 V input. That moves the RFD900x from the 5 V rail to the 12 V rail in the Power Rail Table (about 5 V x 1.2 A / 0.85 / 12 V = 0.59 A at 12 V **EST**, assuming 85% efficiency).

### Symbol / connector table (Tyler's style: off-board parts are connectors with the device name as Value)

| Ref | Item | KiCad symbol | Value / notes |
|---|---|---|---|
| J_PWR_IN | Harness from PDP | `Connector_Generic:Conn_01x04` | +12V, +5V, GND, GND |
| F1-F7 | Blade fuses | `Device:Fuse` | See fuse table |
| J_SW_PWR | Gigabit switch L-com SWTC-GS105NA | `Conn_01x02` | 12 V; barrel/terminal TBD from the switch |
| J_POE_PWR | PoE injector Tycon TP-DCDC-1224G | `Conn_01x02` | 12 V in (9-36 V per Task 4 list); input connector TBD (Tycon page 404) |
| J_LIDAR_PWR | LiDAR | `Conn_01x02` | 12 V, TBD until the LiDAR is chosen; data TBD (Ethernet to the switch or UART/USB) |
| J_USBHUB_PWR | Powered USB hub | `Conn_01x02` | 5 V, hub TBD |
| U_RFD5V | RFD900x 12 V -> 5 V regulator | Module as `Conn_01x03`, or a regulator symbol | Part TBD; fed from +12V through F5; must hold >= 5.0 V at 1.2 A |
| J_RFD | RFD900x | `Conn_02x08_Odd_Even` | Pin numbers as in the datasheet table above; pitch TBD (check the modem) |
| J_GPS | Adafruit PA1616S | `Conn_01x05` | VIN, GND, TX, RX, PPS |
| IMU | LSM6DSV breakout | `Conn_01x04` | VCC, GND, SDA, SCL. Board TBD: no Adafruit LSM6DSV board found, so pick one with a regulator, or put the bare chip on this PCB with an LDO (e.g. `Regulator_Linear:AP2112K-3.3`, check its datasheet) |
| Q_LED | RGB LED low-side switch | `Device:Q_NMOS` or a library part such as `Transistor_FET:AO3400A` | Logic-level at Vgs = 3.3 V, rated above 2 A; one per colour if RGB channels are separate |
| R_G, R_PD | Gate resistor, gate pull-down | `Device:R` | 100R, 10k EST |
| J_LED | RGB LED | `Conn_01x02` or `01x04` | 12 V common + channel(s) |
| TP1-TPn | Test points | `Connector:TestPoint` | See section 6 |

### Fuse table (EST until each part is chosen)

Rule from the drivetrain plan: continuous load <= 80% of the fuse rating (Blue Sea Systems). All runs are short and light, so 18 AWG (20 A, 105 C) is fine throughout.

| Fuse | Load | Peak (A) | Fuse |
|---|---|---|---|
| F1 | Switch, 12 V | 0.5 | 1 A |
| F2 | PoE injector -> Groove, 12 V | 0.49 | 1 A |
| F3 | RGB LED, 12 V | TBD | 2 A (ICD value) |
| F4 | LiDAR, 12 V | 3.0 worst case | 5 A **EST** (3 / 0.8 = 3.75) |
| F5 | RFD900x 12 -> 5 V regulator, 12 V side | 0.59 **EST** | 1 A |
| F6 | USB hub (5 cameras + D435i), 5 V | 1.45 + hub | 2 A **EST** |
| F7 | GPS + IMU, 5 V | 0.03 | 1 A (smallest common blade) |

The Power Rail Table rows Chris added on 10/19 say 12 V peak 0.99 A (3.99 A with the 12 V LiDAR) and 5 V peak 2.675 A. With the RFD900x moved to its own regulator on 12 V, they become about **1.58 A (4.58 A with LiDAR)** on 12 V and **1.475 A** on 5 V **EST**. Update the Task 4 sheet.

## 4. KiCad project layout

Drawn as `Integration/Comms_Navi.kicad_sch` inside the shared project `Integration/URC2027_Integration.kicad_pro` (this plan first proposed a separate `Comms_Navi.kicad_pro`).

| Sheet | File | Contents |
|---|---|---|
| Root | `Comms_Navi.kicad_sch` | Title block "URC 2027 - Comms/Navi", 2 sheet symbols, one-line notes |
| 1. Power | `comms_power.kicad_sch` | J_PWR_IN, F1-F7, RFD900x regulator, power connectors, test points |
| 2. Signals | `comms_signals.kicad_sch` | J_JETSON (pins drawn with "Jetson pin N" text, like the old sheet), J_TEENSY, J_RFD, J_GPS, IMU, Q_LED |

Fused rails cross between sheets as hierarchical labels (`+5V_RFD`, `+5V_GPS`, `+12V_LED`). Signals use labels at the Jetson / Teensy pins (Tyler's style).

## 5. Signal pin list (proposal; confirm Teensy pins with Paul, and drivetrain pins with Krishna)

| Signal | From | To | Notes |
|---|---|---|---|
| GPS_TX | J_GPS TX | Jetson pin 10 (UART1_RX) | 3.3 V out, 9600 baud |
| GPS_RX | Jetson pin 8 (UART1_TX) | J_GPS RX | 5V-safe input |
| GPS_PPS | J_GPS PPS | Test point, optional Jetson GPIO | For time sync later |
| IMU_SDA / IMU_SCL | IMU | Jetson pins 3 / 5 (I2C bus 7) | Freed up now that the GPS is UART; pull-ups depend on the breakout |
| RFD_TX | J_RFD pin 9 | Teensy pin 15 (Serial3 RX) | 3.3 V max |
| RFD_RX | Teensy pin 14 (Serial3 TX) | J_RFD pin 7 | 3.3 V max |
| RFD_CTS / RFD_RTS | J_RFD pins 3 / 11 | Test points | Not used by default |
| LED_CTRL | Teensy PWM pin TBD | Q_LED gate | Pin TBD with Paul |

Serial3 (14/15) is only a proposal. If Krishna's drivetrain sheet uses 14/15, use Serial7 (28/29) or another free port from the PJRC table.

## 6. High-current / heat parts and test locations

High current or heat:
- LiDAR at 12 V, up to 3 A (if a 12 V unit is chosen): the largest load on this board.
- USB hub at about 1.5 A on 5 V.
- RFD900x 1-1.2 A TX bursts: put a bulk capacitor at the modem (value TBD) and keep the regulator close.
- Q_LED at up to 2 A: check its dissipation (I^2 x Rds(on)) for the chosen MOSFET.
- Everything else is under 0.5 A.

Test points (`Connector:TestPoint`):
- TP_12V_IN, TP_5V_IN, TP_GND at the harness input
- One after each fuse (F1-F7), so a blown fuse shows as a missing voltage
- TP_5V_RFD at J_RFD (to check the 5.0 V minimum during TX)
- TP_3V3 if an LDO is used
- GPS_TX, GPS_PPS, RFD_TX, RFD_RX for a logic analyser

## 7. Drawing order

1. New project and the two sheet files; title block.
2. Power sheet: J_PWR_IN, then F1-F7 and the power connectors, then the RFD900x regulator, then test points. Run ERC.
3. Signals sheet: J_JETSON pins and J_TEENSY pins first, then J_GPS, J_RFD, IMU, Q_LED. Run ERC.
4. Hierarchical labels between the sheets; ERC on the root.
5. Assign footprints last, once the connector types are known.

## 8. Open items

- [ ] LiDAR choice (voltage, current, interface): changes F4, J_LIDAR_PWR and the data path
- [ ] Powered USB hub part
- [ ] RGB status LED part, and whether its channels are separate
- [ ] RFD900x 5 V regulator part; RFD900x header pitch
- [ ] LSM6DSV breakout, or bare chip + LDO
- [ ] Tycon TP-DCDC-1224G input connector; L-com switch power connector
- [ ] Jetson J12 logic level and I2C pull-ups from NVIDIA's carrier board spec
- [ ] Teensy pins (Paul, Compute/Logic) and a clash check against Krishna's drivetrain sheet
- [ ] Read "Task 4, pg 2" and check the board definition against it
- [ ] Update the Task 4 sheet: RFD900x current note (1 A per datasheet V1.2), and move the RFD900x from the 5 V rail to the 12 V rail (section 3)

## Sources

- Task 4 spreadsheet (team Drive): TasksStatus, "Comms Navi" tab, Power Rail Table, read 2026-11-02
- URC 2027 Requirements and Guidelines, rule 2.a.v (repo root PDF)
- RFDesign RFD900x / RFD868x Data Sheet V1.2 (updated 17/12/2020), sections 2 and 4: https://files.rfdesign.com.au/Files/documents/RFD900x%20DataSheet%20V1.2.pdf
- Adafruit Ultimate GPS Breakout (product 746): https://www.adafruit.com/product/746 and pinouts: https://learn.adafruit.com/adafruit-ultimate-gps/pinouts
- JetsonHacks, Jetson Orin Nano GPIO header pinout: https://jetsonhacks.com/nvidia-jetson-orin-nano-gpio-header-pinout/
- PJRC Teensy UART serial ports: https://www.pjrc.com/teensy/td_uart.html
- Blue Sea Systems, Choosing Circuit Protection: https://www.bluesea.com/support/articles/Circuit_Protection/95/Choosing_Circuit_Protection
- KiCad 10 built-in libraries (symbol names checked in the installed library)
