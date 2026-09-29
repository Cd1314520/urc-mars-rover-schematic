# URC 2027 Rules Review: Impact on Power & Navigation Design

Prepared: September 29, 2026
Source: *University Rover Challenge 2027 – Requirements and Guidelines* (15 pages), downloaded from the official [Requirements & Guidelines page](https://urc.marssociety.org/home/requirements-guidelines). Local copy: [URC 2027 Requirements and Guidelines.pdf](URC%202027%20Requirements%20and%20Guidelines.pdf).

**Comparison basis.** The 2026 values below come from the "URC 2026 requirements and integration" sheet of the battery workbook, which summarized the 2026 guideline the team supplied. The full 2026 PDF could not be re-downloaded for a line-by-line diff because the Internet Archive was offline. Items marked **New or not compared** are 2027 requirements that were not in that 2026 summary. They may or may not be new. Check the URC Q&A page for amendments before relying on any of this.

---

## 1. Key dates

| Milestone | Date | Section |
|---|---|---|
| Registration opens / closes | Oct 1 / **Fri Oct 30, 2026** | 3.a.i |
| Preliminary Design Review (PDR) | **Wed Dec 2, 2026** | 3.a.ii |
| System Acceptance Review (SAR, written + video, top 36 advance) | **Fri Mar 5, 2027** | 3.a.iii |
| Communications devices and licenses submission | Fri Apr 30, 2027 | 2.c.ii |
| Science Plan | May 21, 2027 | 1.b.i |
| Rover Expense Report | May 26, 2027 (10%/day late penalty) | 3.c.ii |
| Field competition, MDRS, Hanksville UT | **June 2–5, 2027** | 3.a.iv |

The PDR needs the "current state of design," so the KiCad schematics and power budget should be in presentable shape by early December.

---

## 2. What changed from 2026

| Topic | 2026 (workbook summary) | 2027 | Impact |
|---|---|---|---|
| **Budget cap** | $24,000 | **$26,000** (3.c.iii) | +$2,000 headroom. The cap still covers rover power sources, comms, drone, EVA suit and all C2 equipment. Shipping and tax count. |
| **Autonomy duration** | 30 min, up to 2 km | **40 min**, two sub-missions (Astronaut Assistance + Route-Finding) (1.e.i). Rover not expected beyond 1 km (3.d.ii). | Longer autonomous driving time per mission. |
| **Mission order** | Autonomy may begin 10 min after Equipment | **Equipment Servicing may begin 10 min after Autonomy**, same C2 station (1.a.iv, 1.d.i) | Back-to-back window: 40 min Autonomy + ≤10 min gap + 30 min Equipment Servicing. See §3.1. |
| **Science mission** | "Science," 20–30 min | Renamed **Astrobiology**, still 20–30 min. Requires ≥2 life-detection capabilities (one a bioassay), a ≥5 g sample from ≥10 cm depth, and a sealed cache (1.b) | Science-module loads (pumps, heaters, sensors) are not yet in the load list. |
| **2.4 GHz band** | Not in summary | "Frequency restrictions in the 2.4 GHz band **have been removed**" (2.c.vi). This is an explicit change. | Comms team is free to choose channels. Interference tolerance is still expected. |
| Section numbering | Rover rules under 3.a, budget under 2.d | Rover rules now **2.a**, drones 2.b, comms 2.c, finances **3.c**, interventions **3.e** | Update section references in the Task 2 Report and workbook. |

### Unchanged from 2026 (still binding)
- **Delivery 30–60 min** on course (1.c.i). This remains the longest single mission.
- **Setup 15 min / tear-down 10 min** (1.a.ii).
- **Mass:** 50 kg deployed, 70 kg for all fielded parts, 5% penalty per kg over (2.a.iii).
- **Battery swap during a mission is an intervention**, with a 20% penalty each and the clock running (3.e.vii–viii).
- **Environment:** up to 37.8 °C (100 °F), blowing dust, light rain (3.d.iii).
- **Red push-button E-stop** that cuts all battery draw (2.a.v). The 2027 wording is stricter; see §3.2.

### New or not compared (2027 requirements not in the 2026 summary)
- **Stowed size:** the rover must fit in a **1.2 × 1.2 × 1.2 m** box *including antennas*, folded but not disassembled. Failing this is a **40% penalty** (2.a.ii).
- **Autonomy LED indicator** on the back of the rover, visible in daylight: **red** = autonomous, **blue** = teleop, **flashing green** = arrived (1.e.ii).
- **Mobile deployables** need their own E-stop. A fuse is enough for devices that cannot move (2.a.vi).
- **GNSS:** WGS 84 datum (3.d.v). Astrobiology site documentation needs GNSS coordinates **with elevation and accuracy range** (1.b.iii).
- **Route-Finding:** stop **within 1 m** of each target (25 pts each). Targets are ArUco 4x4_50 tags on 20 × 20 cm faces, 0.5–1.5 m above ground. One target is placed behind a hill **out of radio line of sight** (1.e.xii–xvii).
- **Astronaut Assistance:** stop within 3 m of a GNSS point. Follow / stay / fetch a hammer / come / give commands; the full 15 follow points go to **gesture recognition** (1.e.iv–x).
- **900 MHz:** each channel ≤ 8 MHz wide. Teams must be able to operate in each of the Low / Mid / High sub-bands when told (2.c.v).

---

## 3. What we should adjust

### 3.1 Power / battery (Task 2 Report)
1. **Mission-duration basis.** The report sizes for 45 min. Size for at least the **60 min Delivery** maximum, plus powered setup time (up to 15 min).
2. **Autonomy → Equipment Servicing back-to-back.** Energy for 40 + 30 min of operation, with only ≤10 min between them. Choose one:
   - size one pack for about 70 min plus standby, **or**
   - keep the report's two-pack plan and make the swap **fast enough for the ≤10 min gap**, using a quick-disconnect connector and an accessible pack bay. A swap *between* missions is allowed (1.a.v). A swap *during* a mission is a 20% intervention.
3. **Runtime check against current estimates.** Using the workbook numbers (80% usable energy):
   - 10 Ah: 39–62 min
   - 12 Ah: 47–75 min

   Neither pack covers 60 min at the high-load estimate (273 W). Re-run the calculation once the new-architecture load list exists.
4. **E-stop wording.** 2.a.v says:
   - it must be a **push button, not a knob or rotating switch**
   - it must **"cease all power draw from any and all batteries"**, including in "a battery fire"
   - **all systems** must be switched off by this **single** E-stop

   The report's "high-current mechanical switch + 100 A fuse" does not meet this. Specify a red latching push-button E-stop that cuts the entire battery output, compute and comms included. A common approach is a push button driving a contactor rated for the main-bus current. Also confirm what the BMS draws when the E-stop is pressed.
5. **Budget.** The cap is now $26,000. Battery packs and fielded power electronics count toward it.
6. **Thermal / dust.** 37.8 °C ambient plus dust applies to the battery bay, DC-DC converters and Jetson. Plan enclosures and airflow; this is unchanged but still open in the report.

### 3.2 New loads to add to the load list
| Load | Rule | Notes |
|---|---|---|
| Autonomy status LED array (R / B / flashing G) | 1.e.ii | Daylight-visible, so likely a high-power LED or LED array. Needs a driver and a control line from Jetson or MCU. |
| RPLIDAR S2 | — | 5 V. Current is TBD from the Slamtec datasheet. Not in the Task 2 Report, which used Ouster OS0. |
| Science / Astrobiology instruments | 1.b.v | TBD with the science team. |
| Radios (rover side, 900 MHz / 2.4 GHz) | 2.c | TBD with the comms team. |
| Arm actuators and end effector | 1.c.iii, 1.d.ii | Objects up to 5 kg. Not in the current load list. |

### 3.3 Lidar + navigation subsystem (Chris)
- **SparkFun GPS-RTK-SMA (u-blox ZED-F9P):** a good fit. It reports elevation and horizontal/vertical accuracy estimates, which Astrobiology documentation needs (1.b.iii).
- **1 m stop tolerance** on Route-Finding. Standalone GNSS (no RTK) is roughly meter-level, so final approach should rely on **camera ArUco detection**. RTK corrections from a base station at C2 would help, but the link is lost behind the hill (1.e.xvi), so don't depend on RTK there. A base-station GNSS would count toward the budget.
- **RPLIDAR S2:** still the right choice. It is outdoor-rated (IP65) for dust and 37.8 °C, and useful for hill-route obstacle avoidance and astronaut following.
- **GNSS antenna mast:** it must fold to fit the 1.2 m box, including antennas (2.a.ii). Plan the SMA coax routing and mount with that in mind.
- **Schematic:** no change needed to `lidar_navigation.kicad_sch` for these rules. The Autonomy LED indicator needs to appear somewhere in the new-architecture flowchart and schematic, likely on the Jetson or MCU interface sheet.

---

## 4. Open items
- [ ] Check the URC Q&A page for 2027 amendments.
- [ ] Update section references in the Task 2 Report and battery workbook to the 2027 numbering.
- [ ] Re-run runtime calculations for 60 min Delivery and the 40 + 30 min Autonomy/Equipment block.
- [ ] Specify the E-stop circuit (push button + contactor) and add it to the power schematic.
- [ ] Add LED indicator, RPLIDAR S2, science, radio and arm loads to the new-architecture load list.
- [ ] Decide between a single large pack and two packs with a ≤10 min swap.
