# Cooling: Options and Schematic Plan

Task 4 assignment taken over from Hogan (Task 4 spreadsheet, TasksStatus: "Hogan is no longer apart of the team. Reassigning to Chris"):

- **Main focus, Cooling:** "Research cooling systems for the rovers circuitry. Decide between Active/Passive options. Prepare enough information to present options to Mechanical Team."
- **Secondary, Physical Layout:** "Figure out how each subsystem PCB will be arranged in space. Take into consideration designing access to each subsystem from the outside." (Not covered here yet.)

Status: draft, 2026-10-27. Hogan left no files on the team Drive. Values marked **EST** are estimates; **TBD** items need a part choice or a measurement.

## 1. Requirement

URC 2027 rule 3.d.iii: "Temperatures at MDRS can reach 100°F (37.8°C) and winds frequently whip up dust. Rovers shall be able to withstand these conditions and also light rain."

So the electronics bay must handle **37.8 C ambient plus direct sun**, keep **dust** out, and survive **light rain**. Those pull in opposite directions: open airflow cools but lets dust in; sealing keeps dust out but traps heat.

## 2. Heat sources in the electronics bay

| Source | Heat (W) | Basis | Own cooling |
|---|---|---|---|
| Jetson Orin Nano | up to 25 | NVIDIA power modes 7/15/25 W and MAXN SUPER (throttles above TDP) | Dev kit has its own fan heatsink |
| 24->12 V converter (Mean Well DDR-60G-12) | 5.9 at full load | 60 W / 0.91 - 60 W | Passive, -40 to +85 C with derating (datasheet) |
| 24->5 V converter (Pololu D36V28F5) | 0.3-1.8 **EST** | 2.5-10 W out at 80-90% efficiency | Passive |
| MDDS30 x3 | **TBD** | Manual gives no MOSFET Rds(on); measure on the bench | Heatsink + optional 5 V fan header (auto ON above 50 C) |
| Teensy, CAN boards | < 1 | | None needed |
| Contactor coil | **TBD** | Depends on Lance's part (economizer coils draw less) | Passive |
| **Total** | **~34 W + MDDS30 + coil** | | |

Outside the bay: the motors (own housings) and the battery (separate bay; Steven's parts list already has a DS18B20 battery temperature probe).

MDDS30 thermal derating (manual Rev 1.11): max current is 80 A below 50 C, 50 A at 50-70 C, 40 A at 70-100 C, and 30 A above 100 C. Keeping the drivers below 50 C keeps the full current headroom.

## 3. How hot does a sealed box get? (EST)

Rule of thumb: temperature rise = P / (h x A). Use h = 5-10 W/m2K for still air (natural convection plus radiation).

Example box, assumed 0.40 x 0.30 x 0.15 m:
- Surface area A = 2(0.12 + 0.06 + 0.045) = 0.45 m2
- With P = 34 W: temperature rise = 34 / (10 x 0.45) = 7.6 K up to 34 / (5 x 0.45) = 15 K

So the inside air reaches about **45-53 C** at 37.8 C ambient, **before** adding sun on the lid. That is at or above the 50 C point where the MDDS30 fans turn on and its current limit starts to drop. A fully passive sealed box is therefore borderline; the real numbers depend on the box size (mechanical team) and the measured MDDS30 losses.

## 4. Options for the mechanical team

| Option | How | Pros | Cons |
|---|---|---|---|
| **A. Passive, sealed** | Sealed box (IP5x); hot parts bolted to an aluminium plate that forms one wall, with fins outside; shade or reflective lid | No dust inside, no fans to fail, zero power | Inside air ~45-53 C **EST** plus sun; Jetson may throttle; needs a big conductive plate |
| **B. Active, filtered airflow** | Filtered intake fan + exhaust vent (positive pressure keeps dust out) | Inside stays near ambient + ~5 K; simple parts | Filters clog in dust; fans draw power and can fail; vents need rain shielding; filters must be reachable |
| **C. Hybrid (recommended)** | Sealed box, plus an aluminium heat-spreader wall carrying the MDDS30s and DDR-60G, external fins, and one small internal fan to stir the air across the plate (Jetson keeps its own fan) | Dust-sealed but avoids hot spots; fan failure is not fatal | More mechanical work (plate, thermal pads); still needs the sun shade |

Recommendation: plan for **C**, and confirm with a bench test (see section 6). For the **mid-November drivetrain prototype** there is no enclosure: it runs open-frame on the bench, so the only cooling item is the optional MDDS30 5 V fans.

## 5. Schematic plan (cooling part)

The cooling hardware is small: fans, temperature sensors and their connections to the Teensy. It can be one sheet, `cooling.kicad_sch`, or a block on the controller sheet.

### Parts (Tyler's style: off-board items as connectors)

| Ref | Item | Symbol | Notes |
|---|---|---|---|
| J_FAN_D1..D3 | MDDS30 fan headers | `Conn_01x03` (NC, +5V, GND) | Pin order from the MDDS30 manual. The driver powers the fan and switches it ON above 50 C; nothing to wire to the Teensy. Cytron's fan part is FAN-05-040040020 (5 V, 40x40x20 mm) |
| J_FAN_BAY | Bay fan, 12 V 4-wire PWM | `Conn_01x04`: 1 GND, 2 +12V, 3 SENSE (tach), 4 CONTROL (PWM) | Intel 4-wire fan spec: PWM target 25 kHz (21-28 kHz), open-drain, 5.25 V max open-circuit; tach gives 2 pulses per rev, open collector |
| Q_FAN | N-MOSFET (e.g. 2N7002) | `Transistor_FET:2N7002` | Pulls the fan's CONTROL pin low (open-drain). Keeps the fan's internal pull-up (up to 5.25 V) away from the 3.3 V-only Teensy pin |
| R_TACH | 10k pull-up to +3V3 on SENSE | `Device:R` | Keeps the tach signal at 3.3 V for the Teensy. The Intel spec and Intel's boxed-CPU table disagree on the pull-up voltage (12 V vs 5 V); 3.3 V works with an open-collector output, but verify on the chosen fan |
| F_FAN | Fan fuse, 1 A **EST** | `Device:Fuse` | On the 12 V branch; size from the chosen fan's current |
| J_TEMP1..n | DS18B20 probes | `Conn_01x03`: 1 GND, 2 DQ, 3 VDD | DS18B20 datasheet: 3.0-5.5 V supply, +-0.5 C from -10 to +85 C, TO-92 pins 1 GND / 2 DQ / 3 VDD. Probe cable colours vary; check the probe |
| R_1W | 4.7k pull-up DQ -> +3V3 | `Device:R` | Datasheet value. Supply the bus at 3.3 V so DQ never exceeds the Teensy's 3.3 V limit |

Suggested probe locations: battery pack, bay air, MDDS30 heatsink, DDR-60G case. All share one 1-Wire bus (each DS18B20 has its own 64-bit ID).

### Teensy pins (proposal; checked against the drivetrain pin list, confirm with Lance)

| Teensy pin | Net | Why this pin |
|---|---|---|
| 32 | `ONEWIRE_TEMP` | Unused by the drivetrain plan |
| 10 | `FAN_PWM` (to Q_FAN gate) | QuadTimer1: a separate timer from the drive PWM pins (FlexPWM), so the fan can run at 25 kHz without changing the motor PWM frequency |
| 11 | `FAN_TACH` | Any digital pin can take an interrupt |

Pins 10/11 are also the default SPI pins (CS/MOSI). If SPI is needed later, move the fan to another free pin.

### Power and E-stop
- Bay fan and temperature sensors are downstream of the contactor, so they turn OFF on E-stop, like every other rail (URC 2.a.v).
- Add the fan current to the 12 V rail total in the Power Rail Table once a fan is chosen.

## 6. Bench tests that decide between A and C

1. Run each MDDS30 at the expected drive current for 20-30 min, open-frame, and log the heatsink temperature (DS18B20 or IR thermometer). This gives the missing MDDS30 heat number.
2. Put the Jetson at its chosen power mode and log the module temperature (`tegrastats`).
3. Re-run the section 3 estimate with the real numbers and the mechanical team's box size.

## 7. Open items / questions

- [ ] Box size and material from the mechanical team (drives section 3)
- [ ] MDDS30 losses (bench test 1)
- [ ] Jetson power mode the software team will run (7/15/25 W)
- [ ] Contactor coil power (Lance)
- [ ] Choose the bay fan (dust-rated, 12 V, 4-wire) and filter
- [ ] Physical Layout secondary task: not started
- [ ] The live Power Rail Table rows 1-4 now describe a 6S LiPo, an STM32 Nucleo, an OAK-D, an Ouster OS0 and "eight 24 V motors". That does not match the Teensy/Jetson/6-motor architecture and lists "fans" on the 5 V rail. Ask Toka where it came from.

## Sources

- URC 2027 Requirements and Guidelines, rules 2.a.v and 3.d.iii (repo root PDF)
- Task 4 spreadsheet (team Drive), TasksStatus and Power Rail Table tabs, read 2026-10-27
- Cytron MDDS30 User's Manual Rev 1.11 (fan connector, thermal protection): https://forum.dronebotworkshop.com/wp-content/uploads/wpforo/attachments/5360/6077-MDDS30UserManual.pdf
- NVIDIA, JetPack 6.2 Super Mode (Orin Nano power modes): https://developer.nvidia.com/blog/nvidia-jetpack-6-2-brings-super-mode-to-nvidia-jetson-orin-nano-and-jetson-orin-nx-modules/
- Mean Well DDR-60 datasheet: https://www.meanwell.com/Upload/PDF/DDR-60/DDR-60-SPEC.PDF
- Pololu D36V28F5: https://www.pololu.com/product/3782
- Intel 4-Wire PWM Controlled Fans Specification: https://www.mikrocontroller.net/attachment/414199/4-Wire_PWM_Controlled_Fans_Specification.pdf
- Intel boxed processor fan connector table: https://htmlapp.alldatasheet.com/html-pdf/394713/INTEL/E2000/14932/97/E2000.html
- DS18B20 datasheet: https://cdn.sparkfun.com/datasheets/Sensors/Temp/DS18B20.pdf
- PJRC Teensy 4.1 PWM timers: https://www.pjrc.com/teensy/td_pulse.html
