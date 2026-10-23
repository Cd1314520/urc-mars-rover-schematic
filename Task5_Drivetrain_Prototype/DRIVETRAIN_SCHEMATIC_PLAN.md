# Drivetrain Rapid Prototype: Schematic Plan

Working plan for turning Tyler's drawing ("If we have 2x 12 V battery in series and Jetson Hookup") into a KiCad schematic. Status: draft, 2026-10-23. Deadline for the prototype: mid-November 2026.

Values marked **EST** are estimates and must be replaced once the motor datasheet is in hand. Items marked **TBD** are waiting on a part decision or a measurement.

## 1. Changes from Tyler's drawing

| # | Drawing | Change | Why |
|---|---|---|---|
| 1 | Jetson and Teensy fuses fed "+24 V from battery" | Feed them from the switched bus (`+24V_SW`, after the contactor) | URC 2.a.v: "All systems on the rover must have the power switched off by this single E-stop." |
| 2 | Contactor box labelled "E-Stop Switch" | Draw the contactor (K1) and a separate red NC E-stop push button in the coil circuit, plus a start/enable button, a coil fuse and a flyback diode (DNP until the contactor is chosen) | The E-stop is the button, not the contactor. There is no coil supply or start button in the drawing |
| 3 | No pre-charge | Add a pre-charge resistor across the K1 contacts (value TBD) | Limits inrush into the MDDS30 input capacitors. Their capacitance is not in the manual, so measure it |
| 4 | One red/black pair from each MDDS30 split to two motors | Each motor gets its own pair: MA/MB (LEFT) and MA/MB (RIGHT) | The MDDS30 has two independent H-bridge outputs. The outputs are A/B, not +/- |
| 5 | Waveshare boards show only 3.3 V and GND | Add the CTX/CRX lines to the Teensy and the Jetson | "Add rest of pins" |
| 6 | No wheel encoders | Add 6 encoder connectors and Teensy inputs | Component Status lists 6 wheel encoders |
| 7 | Main fuse 40 A | 60 A Class T (EST, see section 3) | At 40 A of continuous load, a 40 A fuse runs at 100% of its rating |
| 8 | Jetson on 24->19 V | Suggest 24->12 V (Mean Well DDR-60G-12) | Jetson input is 9-20 V. A 24->19 V buck drops out when the battery sags to ~20 V. The 2027 architecture already puts the Jetson on 12 V |

## 2. Key part facts (verified)

- **MDDS30** (Cytron manual Rev 1.11)
  - Input: 7-35 V, over-voltage cut-out above 35 V, no reverse-polarity protection
  - Current: 30 A continuous and 80 A peak (1 s) per channel
  - Logic: V_IH 1.3-5 V, V_IL 0-0.7 V
  - PWM mode low-pass filters the input to an analog voltage, and full speed is at 5 V. So 3.3 V PWM may cap top speed near 66%; bench-test this
  - Grove AN connector: AN2, AN1, NC, GND. Grove IN connector: IN2, IN1, NC, GND
  - Terminal block, top to bottom: MB(R), MA(R), V+, V-, MA(L), MB(L)
  - Cytron notes a bug in the "Independent Both" mode (the two channels respond in opposite directions to the same input)
  - On the bench, a power supply needs a battery in parallel to absorb regen current
- **Teensy 4.1** (PJRC)
  - VIN 3.6-5.5 V. VIN and VUSB are joined; cut the pads before using USB with external power
  - Pins are not 5 V tolerant. The 3.3 V output is 250 mA max
  - CAN1: pin 22 = CTX1, pin 23 = CRX1
- **Jetson Orin Nano dev kit**: DC jack 9-20 V. CAN is on **J17: pin 1 CAN_RX, pin 2 CAN_TX** (not on the 40-pin header)
- **SN65HVD230** (TI): 3-3.6 V, 10 mA typ / 17 mA max, up to 1 Mbps. Rs pin to GND = high-speed mode. Waveshare on-board termination is not documented; measure CANH-CANL with power off (target about 60 ohm)
- **Wheel motor**: Mechatronics ICD names the "60D Brushed Planetary Gear Motor (255 RPM)", which matches E-S Motor **60PG-997-47-EN** (24 V, 120 W, 1:47, 14 PPR encoder). Current figures are still missing; the datasheet is behind a Cloudflare check on RobotShop. Steven's parts list says the lab motor model is unknown, so confirm it from the nameplate

## 3. Fuse and wire sizing (EST)

Rules: fuse continuous load <= 80% of the fuse rating; fuse rating <= 80% of wire ampacity (Blue Sea Systems). Ampacity is for 105 C insulation, single conductor (33 CFR 183.425 / ABYC E-11): 18 AWG 20 A, 16 AWG 25 A, 14 AWG 35 A, 12 AWG 45 A, 10 AWG 60 A, 8 AWG 80 A, 6 AWG 120 A. Derate x0.7 for 3 conductors in a bundle.

| Branch | Continuous current | Fuse | Wire |
|---|---|---|---|
| Motor (each) | 6 A **EST** (120 W / 24 V / 0.8) | (behind the driver fuse) | 14 AWG |
| MDDS30 feed (each) | 12 A **EST** | 15 A ATO (or 20 A if starting current trips it) | 12 AWG |
| Jetson (DDR-60G-12, 60 W at 20 V in) | 3.3 A | 5 A ATO | 18 AWG |
| Teensy (D36V28F5, 16 W at 20 V in) | 0.94 A | 2 A ATO | 18 AWG |
| Contactor coil | TBD | TBD | 18 AWG |
| Main (battery -> fuse -> contactor -> fuse block) | ~40 A **EST** | 60 A Class T (JJN-60, 160 VDC) | 8 AWG min (6 AWG per Trade Study) |

- ATO/ATM fuses are rated 32 VDC. That is fine for 2x12 V SLA (28.8 V) or LiFePO4 (29.2 V), but **not** for an 8S LiPo (33.6 V).
- Trade Study contactor candidates (DPE25G7, RS 2842354) are 25 A. That is below the ~40 A main load, and DPE25 is an AC (AC-3) contactor. Raise this with Lance.

## 4. KiCad project layout

New project: `Task5_Drivetrain_Prototype/Drivetrain_Prototype.kicad_pro`, with a project symbol library for the Teensy symbol.

| Sheet | File | Contents |
|---|---|---|
| Root | `Drivetrain_Prototype.kicad_sch` | Title block, 3 sheet symbols, overall notes |
| 1. Power | `power_distribution.kicad_sch` | Battery, main fuse, K1 + E-stop coil circuit, pre-charge, fuse block F1-F6, both step-downs |
| 2. Motor drivers | `motor_drivers.kicad_sch` | 3x MDDS30, 6 motors, 6 encoders, PWM pull-downs |
| 3. Controller + CAN | `controller_can.kicad_sch` | Teensy 4.1, 2x Waveshare SN65HVD230, Jetson J17/J12 |

Signals between sheets use hierarchical labels and sheet pins, the same as the lidar sheet.

### Symbols vs. connectors (Tyler's style: off-board parts are connectors with the device name as Value)

| Item | Symbol | Value |
|---|---|---|
| Battery | `Connector_Generic:Conn_01x02` | 24V Battery (2x12V) |
| Main fuse, F1-F6 | `Device:Fuse` | e.g. 60A Class T, 15A ATO |
| Contactor K1 | `Relay:Relay_SPST-NO` | Contactor TBD (Lance) |
| E-stop | `Switch:SW_Push_Open` (NC push button) | E-STOP red NC |
| Start/enable | `Switch:SW_Push` | START |
| Coil flyback | `Device:D` | DNP until contactor chosen |
| Pre-charge | `Device:R` | TBD |
| DDR-60G-12, D36V28F5 | `Conn_01x04` / `Conn_01x05` per module silkscreen | module name |
| MDDS30 (each) | 3 connectors: terminals `Conn_01x06`, AN Grove `Conn_01x04`, IN Grove `Conn_01x04`, grouped in a dashed box | MDDS30 Driver n |
| Motor | `Conn_01x02` | Motor LF 60PG-997 |
| Encoder | `Conn_01x04` (VCC, GND, A, B; order TBD) | Encoder LF |
| Waveshare CAN | `Conn_01x04` (3V3, GND, CTX, CRX) + `Conn_01x02` (CANH, CANL) | Waveshare SN65HVD230 #n |
| Jetson | J17 connector (pin count TBD) + J12 pins 1/6 | Jetson J17 CAN / Jetson J12 |
| Teensy 4.1 | Custom symbol `Teensy4.1` (48 outer pins, names like `22/CTX1`). KiCad has no built-in one | Teensy 4.1 |
| PWM pull-downs | `Device:R` | 10k |

## 5. Pin lists

### Teensy -> MDDS30 (proposed; confirm with firmware/Lance)

The PWM pins are all FlexPWM. Pins sharing a timer share a frequency, which is fine here. These pins are avoided because the ICDs reserve them or they have another job: 0/1 (Serial1/CAN2), 7/8 (RFD900x), 14/15 (GNSS), 13 (LED), 22/23 (CAN1), 30/31 (CAN3).

| Wheel | Driver / channel | PWM pin -> MDDS30 | DIR pin -> MDDS30 | Labels |
|---|---|---|---|---|
| Left front | D1 / CH1 LEFT | 2 -> AN1 | 24 -> IN1 | `LF_PWM`, `LF_DIR` |
| Right front | D1 / CH2 RIGHT | 3 -> AN2 | 25 -> IN2 | `RF_PWM`, `RF_DIR` |
| Left middle | D2 / CH1 | 4 -> AN1 | 26 -> IN1 | `LM_PWM`, `LM_DIR` |
| Right middle | D2 / CH2 | 5 -> AN2 | 27 -> IN2 | `RM_PWM`, `RM_DIR` |
| Left rear | D3 / CH1 | 6 -> AN1 | 28 -> IN1 | `LR_PWM`, `LR_DIR` |
| Right rear | D3 / CH2 | 9 -> AN2 | 29 -> IN2 | `RR_PWM`, `RR_DIR` |

- Teensy GND goes to the GND pin of both Grove connectors on every MDDS30.
- Each `xx_PWM` line gets a 10k pull-down to GND, so a reset or unpowered Teensy means 0 V = stop (Signed Magnitude mode). The driver also needs a stop signal at power-up, or it shows Input Error. Get Tyler's OK for this.
- DIP switches on every MDDS30 (put a one-line note next to each driver):
  - SW1=1, SW2=0: PWM mode
  - SW3=1, SW4=1: Independent Both
  - SW5=0: Linear
  - SW6=1: Signed Magnitude
  - SW7-8: 10 for SLA, 11 for monitor off
- Do not connect the MDDS30 RC header (SIG/5V/GND).

### Encoders (proposal; not in Tyler's drawing)

| Motor | LF | RF | LM | RM | LR | RR |
|---|---|---|---|---|---|---|
| A / B | 34 / 35 | 36 / 37 | 38 / 39 | 40 / 41 | 16 / 17 | 20 / 21 |

Encoder supply and output voltage are TBD. A 5 V output needs a divider or level shifter before it reaches the Teensy.

### CAN

| From | To |
|---|---|
| Teensy 22 (CTX1) | Waveshare #2 CTX |
| Teensy 23 (CRX1) | Waveshare #2 CRX |
| Teensy 3.3V | Waveshare #2 3V3 |
| Teensy GND | Waveshare #2 GND |
| Jetson J17 pin 2 (CAN_TX) | Waveshare #1 CTX |
| Jetson J17 pin 1 (CAN_RX) | Waveshare #1 CRX |
| Jetson J12 pin 1 (3.3V) | Waveshare #1 3V3 |
| Jetson J12 pin 6 (GND) | Waveshare #1 GND |
| Waveshare #1 CANH / CANL | Waveshare #2 CANH / CANL (twisted pair) |

TX goes to TX and RX to RX (no crossover): the transceiver's CTX pin is its driver input. If anything disagrees, follow the board silkscreen.

### Power sheet topology

```
BATT+ -- F_MAIN 60A -- K1 contacts --+-- (pre-charge R across K1, TBD)
                                     +-- +24V_SW --+-- F1 -- MDDS30 D1 V+
                                                   +-- F2 -- MDDS30 D2 V+
                                                   +-- F3 -- MDDS30 D3 V+
                                                   +-- F4 5A -- DDR-60G-12 -- +12V -- Jetson DC jack
                                                   +-- F5 2A -- D36V28F5 -- +5V -- Teensy VIN
BATT+ -- F6 (coil, TBD) -- E-STOP (NC) -- START -- K1 coil -- GND   (flyback D DNP)
BATT- -- GND (all MDDS30 V-, step-down inputs, Teensy GND)
```

The DDR-60G-12 output is isolated, so tie its Vout- to GND on purpose.

## 6. Drawing order (run ERC after each step)

1. Create the project, set up the title block, and place the 3 empty sheet symbols on the root sheet.
2. Make the `Teensy4.1` symbol in the Symbol Editor.
3. Power sheet: draw the main current path first, then the coil circuit, then the step-downs. Add PWR_FLAGs and run ERC.
4. Motor driver sheet: draw Driver 1 completely (3 connectors, 2 motors, 2 encoders, 2 pull-downs) and get it reviewed. Then copy it for Drivers 2 and 3 and re-annotate.
5. Controller sheet: put labels on the Teensy pins (12 drive signals, encoders, CAN1, power), then add the Waveshare boards and the Jetson connectors.
6. Wire the hierarchical labels and sheet pins. Aim for ERC 0 errors / 0 warnings, then send to Tyler.

## 7. Open items

- [ ] Motor datasheet (60PG-997-EN): rated/stall current, lead gauge, encoder supply and pinout. Then redo section 3
- [ ] Confirm the lab motor model with Steven (nameplate)
- [ ] Battery chemistry of the 2x12 V packs
- [ ] Contactor model with a DC rating >= 60 A (Lance); coil current; whether coil suppression is built in
- [ ] MDDS30 input capacitance -> pre-charge resistor
- [ ] Waveshare header order and on-board termination (measure)
- [ ] Jetson J17 pin count (Carrier Board Specification)
- [ ] Pololu D36V28F5 pin order (module silkscreen)
- [ ] Teensy pin assignment sign-off (Lance / firmware)
- [ ] Bench test: does 3.3 V PWM reach full speed? If not, add 3x 74AHCT125 (5 V supply)
- [ ] Bench test: MDDS30 IN/AN pin open-circuit voltage before connecting the Teensy
- [ ] Bench test: starting current per driver vs. the 15 A fuse

## Sources

- URC 2027 Requirements and Guidelines, rule 2.a.v (repo root PDF)
- Cytron MDDS30 User's Manual Rev 1.11: https://forum.dronebotworkshop.com/wp-content/uploads/wpforo/attachments/5360/6077-MDDS30UserManual.pdf
- PJRC Teensy 4.1: https://www.pjrc.com/store/teensy41.html, pinout card https://www.pjrc.com/teensy/card11a_rev4_web.pdf, PWM timers https://www.pjrc.com/teensy/td_pulse.html
- NVIDIA Jetson CAN guide: https://docs.nvidia.com/jetson/archives/r36.5/DeveloperGuide/HR/ControllerAreaNetworkCan.html
- NVIDIA forum, Orin Nano DC jack 9-20 V: https://forums.developer.nvidia.com/t/powering-the-nano-orin/366665
- TI SN65HVD230 datasheet (SLOS346O): https://www.ti.com/lit/ds/symlink/sn65hvd230.pdf
- Mean Well DDR-60 datasheet: https://www.meanwell.com/Upload/PDF/DDR-60/DDR-60-SPEC.PDF
- Pololu D36V28F5: https://www.pololu.com/product/3782
- Blue Sea Systems, Choosing Circuit Protection: https://www.bluesea.com/support/articles/Circuit_Protection/95/Choosing_Circuit_Protection
- 33 CFR 183.425 ampacity table (reproduction): https://newboatbuilders.com/pages/elect2.html
- RobotShop 60D 255 RPM motor: https://www.robotshop.com/products/e-s-motor-60d-brushed-planetary-gear-motor-with-encoder-24v-255rpm
- Team Drive: Mechatronics System ICD, Embedded Controller ICD, Component Status, Trade Study, Firmware CAN Setup Guide
