# Task 5 (draft): Comms/Navi Protection, Wiring and Connectors

Power Task 5 ("Protection, wiring, and connector selection", Tyler, on the Drive) applied to the **Comms/Navi** branch. Status: draft, 2026-11-16, for review by Tyler and Bryan before anything changes in KiCad.

Inputs:
- Chris's Comms/Navi KiCad sheet (10/23): J1-J8, F1, U1/U2, Q1-Q3.
- Task 4 spreadsheet, "Comms Navi" tab, load detail (Chris, 10/19): nominal and peak current per load.
- Bryan's PDP sheet (team repo, merged 11/14).
- [COMMS_NAVI_SCHEMATIC_PLAN.md](COMMS_NAVI_SCHEMATIC_PLAN.md), [HEATSINK_HARNESS_RESEARCH.md](HEATSINK_HARNESS_RESEARCH.md), [PHYSICAL_LAYOUT.md](PHYSICAL_LAYOUT.md).

**EST** = our own estimate or arithmetic. **TBD** = needs a part choice, a measurement, or a source we could not open.

## 1. Rules used

| Rule | Source |
|---|---|
| Continuous load <= 80% of the fuse rating | Blue Sea Systems, Choosing Circuit Protection |
| Fuse rating <= ampacity of the wire it protects (Task 5 sec. 4) | Task 5; ABYC E-11 table (via Blue Sea) |
| Voltage drop V = I x R, loss P = I^2 x R, R for the round trip (2 x length) | Task 5 sec. 5 |
| Wire resistance (stranded tinned copper, 20 C): 18 AWG 7.0 ohm/1000 ft (22.97 ohm/km), 22 AWG 16.2 ohm/1000 ft (53.15 ohm/km) | Alpha Wire 3055 and 3051 spec sheets |
| 18 AWG ampacity, bundled, 105 C insulation: 14 A | ABYC E-11 Table VI-B (Blue Sea excerpt) |
| 22 AWG: 7 A "chassis wiring" rule of thumb (single wire in air) | PowerStream wire table; no manufacturer ampacity found (**TBD**) |
| Every Comms/Navi rail comes after the contactor, so E-stop removes it | Task 4 sheet note; URC 2.a.v |

Wire lengths are one-way estimates from the bay layout figure (400 x 300 mm bay; LiDAR at the front, GPS on the mast). **EST** until the chassis exists.

## 2. Branch protection table (Tyler's format)

All branches are E-stop affected: **Yes** (downstream of the contactor).

| Branch | Voltage | Nominal current | Peak current | Fuse / protection | Wire gauge | Connector | E-stop affected? |
|---|---|---|---|---|---|---|---|
| **Comms feed 12 V** (PDP -> Comms board J1) | 12 V | 0.65 A (LED, LiDAR TBD) | 6.58 A with 12 V LiDAR, 3.58 A without **EST** | At the PDP: own "Communications Branch Fuse", 10 A (with LiDAR) or 5 A (LiDAR fed from PDP) MINI blade | 18 AWG | Micro-Fit 3.0, 2x3 (2 pins for 12 V) | Yes |
| **Comms feed 5 V** (PDP -> J1) | 5 V | 1.37 A | 1.48 A + USB hub's own draw (TBD) | At the PDP: 3 A MINI blade | 18 AWG | Same 2x3 Micro-Fit (1 pin 5 V) | Yes |
| Gigabit switch (J2) | 12 V | 0.225 A | 0.5 A | F2: 2 A MINI | 18 AWG | Micro-Fit 3.0, 1x2 | Yes |
| PoE injector -> Groove (J3) | 12 V | 0.39 A | 0.49 A; inrush TBD | F3: 2 A MINI | 18 AWG | Micro-Fit 3.0, 1x2 | Yes |
| LiDAR (J5) | 12 V | TBD | 3.0 A worst case; spin-up TBD | F4: 5 A MINI | 18 AWG | Micro-Fit 3.0, 1x2 on the board; Deutsch DT at the bay wall | Yes |
| RGB status LED (J4) | 12 V | TBD | must stay <= 1.6 A (80% of 2 A) | F1: 2 A (already drawn; change to MINI) | 18 AWG | Micro-Fit 3.0, 1x4; Deutsch DT at the bay wall | Yes |
| RFD900x regulator input (U_RFD5V, new) | 12 V | 0.03 A | 0.59 A **EST** | F5: 2 A MINI | PCB trace | On board | Yes |
| RFD900x modem (J6) | 5 V from U_RFD5V | 0.06 A (RX) | 1.0 A at 30 dBm (datasheet); 1.2 A budget | Upstream F5; regulator current limit (TBD) | 22 AWG | JST XH 1x4 | Yes |
| Powered USB hub, 5 cameras + D435i (J7) | 5 V | 1.35 A | 1.45 A + hub (TBD); inrush TBD | F6: 3 A MINI | 18 AWG | Micro-Fit 3.0, **1x3** (so it cannot mate with a 12 V 1x2) | Yes |
| GPS PA1616S (J8) + IMU LDO | 5 V | 0.021 A | 0.026 A | F7: 2 A MINI | 22 AWG | JST XH **1x5** (adds PPS; cannot mate with the RFD 1x4) | Yes |
| IMU LSM6DSV (U2, on board) | 3.3 V from U1 | 0.65 mA | 0.65 mA | Upstream F7 | PCB trace | On board | Yes |

### Fuse checks

| Fuse | Peak / rating | Wire ampacity >= fuse? | Note |
|---|---|---|---|
| Comms 12 V, 10 A | 66% | 18 AWG 14 A: yes | 5 A if LiDAR is fed from the PDP (72%) |
| Comms 5 V, 3 A | 49% + hub | yes | |
| F2, F3, F5, F7 (2 A) | 1-30% | yes; F7 feeds 22 AWG (7 A rule of thumb) | 2 A is the smallest MINI fuse we could confirm. These fuses protect the wire, not the module; the modules need their own protection |
| F4, 5 A | 60% | yes | Fast-blow; check against LiDAR spin-up current |
| F6, 3 A | 48% + hub | yes | Check camera hot-plug inrush |
| F1, 2 A | LED current TBD | yes | LED must draw <= 1.6 A |

The MINI 297 parts confirmed on DigiKey are **fast-blow**. For the loads with inrush (PoE, LiDAR, USB hub), check the fuse's time-current curve or pick a slow-blow fuse (TBD).

### Voltage drop (V = I x R, worst-case peak current)

| Branch | One-way length | Wire | Round-trip R | Drop | % of rail | Loss P = I^2 R |
|---|---|---|---|---|---|---|
| Comms feed 12 V, 6.58 A | 0.4 m | 18 AWG | 0.018 ohm | 0.121 V | 1.0% | 0.80 W |
| Comms feed 5 V, 1.48 A | 0.4 m | 18 AWG | 0.018 ohm | 0.027 V | 0.5% | 0.04 W |
| LiDAR, 3.0 A | 1.0 m | 18 AWG | 0.046 ohm | 0.138 V | 1.15% | 0.41 W |
| RGB LED, 2.0 A | 0.5 m | 18 AWG | 0.023 ohm | 0.046 V | 0.4% | 0.09 W |
| USB hub, 1.45 A | 0.3 m | 18 AWG | 0.014 ohm | 0.020 V | 0.4% | 0.03 W |
| RFD900x, 1.2 A | 0.15 m | 22 AWG | 0.016 ohm | 0.019 V | 0.4% | 0.02 W |
| GPS, 0.025 A | 1.5 m | 22 AWG | 0.16 ohm | 0.004 V | 0.1% | ~0 W |

Every branch is at or below about 1%. So 18 AWG is set by the connectors and by mechanical strength, not by voltage drop. Task 5 asks for "the smallest reasonable wire", and 20 AWG would also work electrically. We keep 18 AWG because the Micro-Fit 18 AWG terminal is rated 8.5 A per contact and 18 AWG is sturdier for the wires that leave the bay. The RFD900x drop matters most because the modem needs at least 5.0 V. Its regulator sits close to J6, so the drop is only 0.019 V.

## 3. Connector families (Task 5 sec. 6)

| Category | Family | Rating (source) | Used for | Why |
|---|---|---|---|---|
| Medium-current power, inside the bay | Molex Micro-Fit 3.0 (receptacle 43025 / 43645, 18 AWG terminal 0430300038) | 8.5 A max per contact with 18 AWG (Molex part PDF); housing has a latch lock (DigiKey 43025) | J1, J2, J3, J4, J5, J7 | Latching and polarized, vibration-safe. Replaces the Phoenix MKDS screw terminals now in the drawing (15 A, 14-30 AWG per DigiKey, but no latch or keying) |
| Low-current power + signal | JST XH, 2.5 mm pitch | 3 A at 22 AWG, 250 V, wire AWG 30-22 (JST datasheet) | J6 (RFD900x), J8 (GPS), signal harnesses | Small; fine for < 1.2 A |
| Through the sealed bay wall | TE Deutsch DT / DTM | DT 13 A, 14-20 AWG, IP68 (DigiKey); DTM 7.5 A | LiDAR, LED, GPS (if on the mast) | Sealed against dust and rain (URC 3.d.iii) |

Misconnection rules (Task 5: "avoid using the same connector style for incompatible voltages"):
- 12 V loads use 2-pin Micro-Fit and 5 V loads use 3-pin, so a 5 V device cannot be plugged into a 12 V socket.
- RFD900x uses a 4-pin XH and the GPS a 5-pin XH, so their cables cannot be swapped.
- J1 is a 2x3 Micro-Fit and nothing else on the board has that shape.

## 4. PCB-to-harness interfaces (Task 5 sec. 7)

The two signal connectors J9 and J10 are **new**. Global labels connect the nets in KiCad, but in the real rover the GPS, IMU, RFD and LED signals still need a cable from this board to the Jetson and the Teensy, and that cable needs a **GND wire**: UART and I2C only work when both ends share the same ground reference.

| ID | Function | Voltage | Current | Pins | Pin assignment | Mating connector | Harness goes to |
|---|---|---|---|---|---|---|---|
| J1 | Power in | 12 V, 5 V | 6.58 A / 1.48 A peak | 6 | 1-2 +12V, 3 +5V, 4-6 GND | Micro-Fit 2x3 receptacle 43025-0600 (TBD exact P/N) | PDP (Bryan) |
| J2 | Switch power | 12 V | 0.5 A | 2 | 1 +12V, 2 GND | Micro-Fit 1x2 | L-com switch (its input connector TBD) |
| J3 | PoE injector power | 12 V | 0.49 A | 2 | 1 +12V, 2 GND | Micro-Fit 1x2 | Tycon TP-DCDC-1224G (input TBD) |
| J4 | RGB LED | 12 V | <= 1.6 A | 4 | 1 +12V, 2 R, 3 G, 4 B (low side) | Micro-Fit 1x4 -> Deutsch DT at the wall | LED on the exterior |
| J5 | LiDAR power | 12 V | 3.0 A | 2 | 1 +12V, 2 GND | Micro-Fit 1x2 -> Deutsch DT at the wall | LiDAR (TBD) |
| J6 | RFD900x | 5 V | 1.2 A | 4 | 1 +5V_RFD, 2 GND, 3 RFD_TX, 4 RFD_RX | JST XHP-4 | RFD900x header pins 4, 2, 9, 7 |
| J7 | USB hub power | 5 V | 1.45 A + hub | 3 | 1 +5V, 2 GND, 3 not used (key) | Micro-Fit 1x3 | Powered USB hub (TBD) |
| J8 | GPS | 5 V | 0.026 A | 5 | 1 +5V, 2 GND, 3 GPS_TX, 4 GPS_RX, 5 GPS_PPS | JST XHP-5 | Adafruit PA1616S |
| **J9 (new)** | Signals to Jetson | 3.3 V logic | < 0.1 A | 6 | 1 GPS_TX, 2 GPS_RX, 3 IMU_SDA, 4 IMU_SCL, 5 IMU_INT1, 6 GND | JST XHP-6 on this board; 2.54 mm Dupont housings at the Jetson 40-pin header | Jetson J12 pins 10, 8, 3, 5, GPIO TBD, 6 |
| **J10 (new)** | Signals to Teensy | 3.3 V logic | < 0.1 A | 6 | 1 RFD_TX, 2 RFD_RX, 3 LED_R, 4 LED_G, 5 LED_B, 6 GND | JST XHP-6 | Compute/Logic board (Paul), pins TBD |

## 5. Reverse polarity (Task 5 sec. 8)

| Input | Consequence if reversed | Protection |
|---|---|---|
| J1 +12 V | Destroys U_RFD5V, Q1-Q3 and the loads | **Keyed connector** (Micro-Fit 2x3 only fits one way), plus a reverse-polarity stage on 12 V. Candidate: TI LM74700-Q1 ideal-diode controller (3.2-65 V input, 80 uA typ, < 0.75 us reverse blocking) with an external N-FET (FET **TBD**). Smaller option: a P-FET (part TBD) |
| J1 +5 V | Damages the GPS, LDO and USB hub | Keyed connector only. A series diode would drop 0.3-0.5 V and push the USB hub below 5 V, so no diode here |
| J2-J10 | Each is keyed and only fits one way | Connector keying |

## 6. Transient protection and bulk capacitance (Task 5 sec. 9-10)

| Location | What | Purpose | Preliminary rating | Source |
|---|---|---|---|---|
| J1, +12 V to GND | TVS **SMAJ15A** | Clamp spikes on the 0.4 m feed from the PDP (shared bus with motor drivers) | VWM 15 V, VBR 16.7 V min, VC 24.4 V at 16.4 A, 400 W | Vishay SMAJ datasheet doc 88390 |
| J1, +5 V to GND | TVS **SMAJ5.0A** | Same, 5 V side | VWM 5.0 V, VBR 6.40 V min, VC 9.2 V at 43.5 A | Vishay doc 88390 |
| J1, +12 V | Bulk electrolytic, 47-100 uF / 25 V **EST** | Ride through load steps; damp the harness inductance | Value TBD | |
| U_RFD5V output, at J6 | Move C1 (100 uF) here + regulator's own caps | Covers the 1 A TX bursts; keeps the modem >= 5.0 V | Per the regulator datasheet (TBD) | RFD900x datasheet V1.2 (5.0 V min) |
| U1 (AP2112K) in/out | C2, C3 1 uF (drawn) | LDO stability | Per AP2112 datasheet | |
| U2 (IMU) | C4, C5 100 nF (drawn) | Local decoupling | | |
| J4 LED | No flyback diode | LED is not an inductive load | | |
| Long runs (LiDAR 1 m, GPS 1.5 m) | No extra TVS on this board for now | Low current; the modules carry their own input protection (check datasheets, TBD) | | |

Check: when the SMAJ15A clamps a full pulse, the 12 V rail can briefly reach 24.4 V. AO3400A V_DS max is 30 V (AOS datasheet), so Q1-Q3 are fine. The **U_RFD5V input rating** and the 12 V modules' maximum input are **TBD**. The SMAJ5.0A clamps at 9.2 V at full pulse current, which may exceed the AP2112K's maximum input (**TBD**: check the Diodes datasheet).

LED MOSFET dissipation: AO3400A R_DS(on) max 48 mohm at V_GS = 2.5 V (Teensy drives 3.3 V). At 2 A on one channel: P = 2^2 x 0.048 = 0.19 W, well under the 1.4 W rating (AOS datasheet).

## 7. Grounding / return (Task 5 sec. 11)

- All Comms/Navi current returns through the **three GND pins of J1** to the PDP's low-voltage ground (Bryan's sheet: each converter's ground pin is tied to the common ground).
- This return must **not share the motor-driver negative wires**. The motor return current stays in zone 1; the Comms return goes straight from J1 to the converter grounds.
- J9 and J10 each carry a GND wire, so the UART and I2C signals have a reference at the Jetson and the Teensy.
- On the board: one ground plane. The LED MOSFET sources and C1 return to it near J1, not under the IMU.

```
 Battery - ---- PDP common ground (Bryan) ---- 12V/5V converter GND pins
                         |                               |
              motor-driver returns (zone 1)      J1 GND x3 (Comms board)
                                                         |
                                       Comms ground plane --- J9 GND -> Jetson
                                                          --- J10 GND -> Teensy
```

## 8. Test points (Task 5 sec. 12)

TP_12V_IN, TP_5V_IN, TP_GND (at J1), one after each fuse F1-F7, TP_5V_RFD (at J6, check >= 5.0 V during TX), TP_3V3_IMU, and signal pads GPS_TX, RFD_TX, RFD_RX. Use `Connector:TestPoint` pads near the board edge.

## 9. KiCad changes this implies (Task 5 sec. 13; Chris draws them)

1. J1: Phoenix 1x4 -> Micro-Fit 2x3; add TVS SMAJ15A, SMAJ5.0A, a 12 V bulk cap and the reverse-polarity stage.
2. Add F2-F7 (MINI blade, Keystone 3568 holder: 30 A UL, through-hole, fits MINI 297) and change F1 from 1206 SMD to MINI. Seven holders take board space; SMD fuses are the smaller fallback if space is short.
3. Add U_RFD5V (12 V -> 5 V) and move J6 and C1 onto it.
4. Change J2/J3/J5 to Micro-Fit 1x2, J4 to 1x4, J7 to 1x3, J8 to XH 1x5 (+PPS).
5. Add J9 and J10 with GND, and change the hierarchical labels to global labels.
6. Add the test points.

## 10. Answers to Tyler's five questions (example: LiDAR branch)

- **What protects this branch?** F4, a 5 A MINI fuse on the Comms board, behind the Comms 12 V branch fuse at the PDP.
- **What wire carries this current?** 18 AWG, about 1 m, 0.14 V drop at 3 A.
- **What connector connects these two devices?** Micro-Fit 3.0 1x2 at J5, then a Deutsch DT at the bay wall.
- **What happens if this branch shorts?** F4 (5 A) should open before the 10 A Comms branch fuse upstream, so the other Comms loads keep running. Confirm on the two fuses' time-current curves.
- **Does E-stop remove this branch?** Yes: the Comms feed is downstream of the contactor.

## 11. Open items (need answers before this is final)

- [ ] **Bryan:** add a separate Comms branch fuse at the PDP (his F12 5 A currently feeds Jetson + video encoder + PoE + LiDAR, about 5.6 A peak EST). Decide whether the LiDAR and PoE get power from the PDP or from this board.
- [ ] **Bryan:** fix the PDP U1 (12 V converter) polarity and the `5A_MAIN` / `5V_MAIN` name mismatch (found with KiCad netlist and ERC on his merged sheet).
- [ ] LiDAR and RGB LED parts (their current sets F4 and F1).
- [ ] USB hub part (its own current and inrush set F6).
- [ ] Inrush of the PoE injector, LiDAR and hub -> fast or slow-blow fuses.
- [ ] U_RFD5V part; its input rating vs the 24.4 V TVS clamp.
- [ ] AP2112K maximum input vs the 9.2 V TVS clamp.
- [ ] N-FET for the LM74700-Q1, or a P-FET choice.
- [ ] Teensy pins for J10 (Paul).
- [ ] Molex Micro-Fit current derating for 2 and 6 circuits (Molex pages timed out).

## Sources

- Power Task 5 (Tyler), team Drive `_2.2.3.2.4_2027_Architecture/Power_Task_5.docx`, read 2026-11-16
- Task 4 spreadsheet, "Comms Navi" tab, read 2026-11-16
- Bryan's PDP sheet: github.com/Paul-ECE/2027-UH-URC-Power, `PDP.kicad_sch` (merged 2026-11-14), checked read-only
- Alpha Wire 3055 (18 AWG) and 3051 (22 AWG) spec sheets: https://www.alphawire.com/disteAPI/SpecPDF/DownloadProductSpecPdf?productPartNumber=3055 and ...=3051
- PowerStream wire table (chassis-wiring rule of thumb): https://www.powerstream.com/Wire_Size.htm
- ABYC E-11 ampacity table, Blue Sea excerpt: see HEATSINK_HARNESS_RESEARCH.md sources
- Littelfuse MINI 297 on DigiKey (32 V DC, 1 kA breaking, fast-blow; 2 A and 30 A parts): https://www.digikey.com/en/products/detail/littelfuse-inc/0297005-WXNV/146583
- Keystone 3568 MINI fuse holder, catalog p.48: https://www.keyelco.com/userAssets/file/K75p48.pdf
- Vishay SMAJ5.0A-SMAJ188CA datasheet (doc 88390): https://www.vishay.com/docs/88390/smaj50a.pdf
- AOS AO3400A datasheet Rev 3.1: https://www.aosmd.com/res/datasheets/AO3400A.pdf
- Molex Micro-Fit 18 AWG terminal (8.5 A max): https://docs.rs-online.com/f973/A700000015226748.pdf ; DigiKey 0430300038 and 43025 housing (latch lock)
- JST XH datasheet (3 A at AWG 22, AWG 30-22): https://www.digikey.be/en/resources/datasheets/jst/xh-connector
- Phoenix MKDS 1,5/2-5,08 on DigiKey (15 A, 300 V, 14-30 AWG): https://www.digikey.com/en/products/detail/phoenix-contact/1715721/260631
- TI LM74700-Q1: https://www.ti.com/product/LM74700-Q1
- RFDesign RFD900x datasheet V1.2 (5 V min, 1 A at 30 dBm): see COMMS_NAVI_SCHEMATIC_PLAN.md
- Blue Sea Systems, Choosing Circuit Protection (80% rule): https://www.bluesea.com/support/articles/Circuit_Protection/95/Choosing_Circuit_Protection
