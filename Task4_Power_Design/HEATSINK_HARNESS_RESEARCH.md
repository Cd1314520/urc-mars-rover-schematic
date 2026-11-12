# Hybrid Heat Sinks and Wire Harness: Research Notes

Task 4 (power), follow-up to `COOLING_PLAN.md`. Tyler asked: "look up hybrid heat sinks to see if this will be compatible for us, look for wire harness as well".

Status: research, 2026-11-09. The MDDS30 facts in section 1 (101.60 x 96.52 mm bottom cover, heat sink on top, fins up, 30 A continuous / 80 A peak) were re-checked against the manual pages. The other numbers come from the linked sources and were not re-checked one by one. Every number has a source in section 6. **TBD** = not verified. **EST** = our own arithmetic, not a datasheet value.

Inputs from the cooling plan: about 34 W in the bay (Jetson Orin Nano up to 25 W, DDR-60G-12 about 5.9 W, D36V28F5 0.3-1.8 W, 3x MDDS30 unknown, Teensy under 1 W). URC 3.d.iii: 37.8 C ambient, dust, light rain. Example box 0.40 x 0.30 x 0.15 m.

---

## 1. What "hybrid heat sink" means here

"Hybrid heat sink" is not a standard product category. Vendors use it for three different things:

1. **Passive + active:** a finned heat sink with a fan. It works passively if the fan stops and works much better with the fan running. Example: Fischer LA 6 fan-cooled heat sink tunnels.
2. **Through-wall (sealed) exchanger:** one heat sink or fan loop inside the box and one outside. Only metal crosses the wall, so the box stays sealed. Commercial forms are air-to-air heat exchangers, heat-pipe coolers and thermoelectric (Peltier) coolers.
3. **Heat pipe or vapour chamber + fins:** heat pipes carry heat from a small hot part to a larger fin stack, sometimes outside the box.

For our bay, the useful meaning is **2 built from parts in 1**: a sealed box with a finned heat sink inside, a finned heat sink outside, both on an aluminium wall section, and a fan on each.

### Finding that changes option C of the cooling plan

Option C assumed the MDDS30s and the DDR-60G bolt to an aluminium heat-spreader wall. The datasheets do not support that:

- **MDDS30 (manual Rev 1.11):** the board is two stacked PCBs on standoffs. The finned heat sink sits on top of the main board with the fins facing up. The bottom cover PCB (101.60 x 96.52 mm) has a cut-out for the optional 40 x 40 x 20 mm 5 V fan. Height is about 42 mm. The manual says to mount the driver to the platform with "the original short PCB standoffs", leaving clearance for the fan intake. There is no flat metal base for a thermal pad. **Mounting the MDDS30 heat sink to a plate: not supported by the manual (TBD whether any custom mount is practical).** The MDDS30 has to be cooled by air moving over its fins.
- **DDR-60G-12:** DIN-rail module, 52.5 x 90 x 54.5 mm, 216 g. The datasheet lists no heat-sink mounting face. **Conduction to a plate: TBD.**
- **Jetson Orin Nano dev kit:** has its own fan heat sink that takes air from the bay. A conduction plate would need a different heat sink (**TBD**).

So almost all 34 W goes into the **bay air** first. The cooling hardware has to move heat from the bay air, through the sealed wall, to the outside air. That is what an air-to-air exchanger does.

### Quick check: how good does the path have to be?

Required thermal resistance from bay air to outside air = allowable rise / power:

| Case | Calculation | Required R (K/W) | Required G (W/K) |
|---|---|---|---|
| 40 W, 15 K rise (inside 52.8 C) | 15 / 40 | 0.375 | 2.7 |
| 40 W, 10 K rise (inside 47.8 C) | 10 / 40 | 0.25 | 4.0 |
| 50 W, 10 K rise | 10 / 50 | 0.20 | 5.0 |

To stay under the MDDS30 50 C derating point at 37.8 C ambient, the rise must be **under 12.2 K**. At 40 W that needs R ≤ 0.30 K/W (EST).

The sealed box alone (cooling plan: h = 5-10 W/m2K, A = 0.45 m2) gives R = 1/(h·A) = **0.22-0.44 K/W** (EST). That is borderline before sun load (sun load TBD). The hybrid hardware must add a parallel path of roughly 2-5 W/K (EST) to give margin.

---

## 2. Candidate table

| # | Part (supplier) | Type | Key thermal spec | Size | Weight | Power | IP / sealing | Price | Compatible? Why |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Fischer Elektronik LA 6 100 12** (DigiKey 5496-LA610012-ND) | Passive + active: aluminium tunnel heat sink with 60 mm fan | 0.205 K/W (forced air), mounting face to air. LA 6 family 0.2-0.1 K/W depending on length; LA V 6 200: 0.175-0.095 K/W | 100 x 62 x 74 mm | Extrusion TBD; fan 66 g | Fan ebm-papst 612 NHH-118: 12 V DC, 2.9 W, 56 m3/h, 41 dB(A). 24 V fan (614 NHH-119) also offered | Fan IP not stated (TBD). Fan rated -20 to +70 C | USD 94.86 (qty 1) | **Yes, as a building block.** One LA 6 alone (0.205 K/W) beats the 0.375 K/W target, but only for parts bolted flat to it. Use two through the wall (one inside, one outside), see section 3 |
| 2 | **Wakefield Thermal DC0602512U2B-BT0-68** | IP68 fan (60 x 60 x 25 mm, same frame size as the LA 6 fan) | 44.0 CFM (1.23 m3/min), 139.5 Pa static | 60 x 60 x 25 mm | TBD | 12 V, 0.380 A, 4.56 W; PWM + tach (4-wire) | **IP68**; -10 to 70 C | USD 28.72 (qty 1); 26-week lead time listed | **Yes.** Can replace the LA 6 fan outside the box, where dust and rain hit it. Also fits as the internal stirring fan. Effect on LA 6 R value after the swap: TBD |
| 3 | **Tark (ex-Laird) AA-040-12-22-00-00** | Thermoelectric (Peltier) air-to-air cooler, through-panel | Qc max 41 W at ΔT = 0 (35 C ambient); max ΔT 43 C at Qc = 0 | 160 x 122 x 146.9 mm | 1.80 kg | 12 V nominal (15 V max), 6.3 A running, 7.0 A start, 76 W | Not stated (TBD). Operating range -10 to 48 C | USD 357.66 (qty 1) | **Marginal.** 41 W only at ΔT = 0, so it barely covers 34 W. It draws 76 W from the battery and rejects about 117 W (Qc + Pin, EST) outside. Only worth it if the bay must sit below ambient |
| 4 | **nVent Hoffman TE090624011** (MCLT, TE09, shrouded) | Thermoelectric enclosure cooler, partial recess mount | 178 BTU/h (about 52 W). Distributor listings conflict between 52 W and 60 W | 9.29 x 5.02 x 6.94 in (236 x 128 x 176 mm) | TBD | 24 V DC; 4.4 A per distributor listing (TBD, about 106 W EST) | **NEMA 12/3R/4/4X, IP65**; -40 to 55 C | Not shown | **Possible but costly in power.** Sealing is good. It needs about 100 W from the 24 V bus and a cut-out in the 300 mm face. Its 176 mm depth exceeds the 150 mm box depth (partial recess; fit TBD) |
| 5 | **Rittal SK 3201.300** | Thermoelectric enclosure cooler, wall-mounted | 80 W at L35/L35; 100 W at L35/L30; EER 0.9 | 125 x 400 x 155 mm, 100 mm installation depth | 2.6 kg (summary) or 3.249 kg net; page conflicts | 24 V DC, 4.5 A max, 10 A pre-fuse | Internal circuit IP54, **external circuit IP34** (splash only) | Not shown | **No.** It is 400 mm long (the whole box length), up to 3.2 kg, and only IP34 on the outside, which is not dust-tight |
| 6 | **Advanced Cooling Technologies ACT-HPC-15** | Heat-pipe enclosure cooler (sealed, fans inside and outside) | 15.0 W/C (0.067 K/W); 300 W at 20 C ΔT | 287 x 138 x 136 mm; insertion depth 143 mm; mounting plate 171.5 x 171.5 mm | 3.2 kg (NEMA 4X version heavier) | Fans 12 V DC 1.80 A (about 22 W EST) or 24 V DC 0.92 A | NEMA 4, 4X, 3R, 12; -10 to +60 C | Not shown | **No (oversized).** About 8x more capacity than needed. The 143 mm insertion uses almost the full 150 mm box depth, and it weighs 3.2 kg |
| 7 | **Elmeko PK 100** (reference only) | Thermoelectric cooler | 100 W | TBD | 7.20 kg net | 24 V DC, 5.2 A | IP67; -20 to +70 C | TBD (PK 50 from EUR 479) | **No.** 7.2 kg is too heavy for a 50 kg rover |

Not included: Ohmite, Same Sky, Alpha Novatech and Advanced Thermal Solutions. The searches only found small fan heat sinks for single chips (TO-220, BGA, LED), with no datasheet for a plate-size fan heat sink. Wakefield's DUAL LED fan heat sinks are round LED coolers and were not checked in detail (the datasheet did not load).

---

## 3. Recommendation for our bay

1. **Keep option C ("hybrid") but change what it means.** The MDDS30s (fins up, PCB stack on standoffs) and the Jetson (own fan) cannot conduct into a wall plate. Build a **DIY through-wall air-to-air exchanger** instead:
   - one aluminium wall section (or the box wall itself, if aluminium);
   - **inside:** a finned heat sink with a fan pulling bay air through it (for example an LA 6 tunnel), placed so its air path also passes over the MDDS30 fins;
   - **outside:** a second finned heat sink with an **IP68 fan** (for example an LA 6 with the Wakefield DC0602512U2B-BT0-68). Shade it from direct sun.
   - Only metal crosses the wall, so the box stays sealed. If a fan fails, the fins still work passively.
2. **Rough performance (EST):** two LA 6 100 at 0.205 K/W each, in series through the wall, plus a contact layer (TBD), give about 0.45 K/W, or 2.2 W/K. In parallel with the box walls (2.25-4.5 W/K), the total is about 4.5-6.7 W/K. At 40 W that is a **6-9 K rise**, or about 44-47 C inside at 37.8 C ambient, under the 50 C MDDS30 limit. This is a hand estimate: it ignores sun load and how the R value changes with the fan swap. It must be bench-tested.
3. **Power:** two 4.56 W fans is about 9 W at 12 V (datasheet values). This adds about 0.8 A to the 12 V rail (EST). Weight: under 1 kg EST (extrusion mass TBD).
4. **Avoid Peltier coolers** unless the bench test shows the bay cannot stay under 50 C. They need 76-108 W of battery power for 41-80 W of cooling and weigh 1.8-3.2 kg.
5. **Heat pipes:** commercial heat-pipe coolers (ACT-HPC-15) are too big. Heat pipes only become relevant if we later move the Jetson to a conduction-cooled heat sink (TBD).
6. **Bench test first** (cooling plan section 6). The MDDS30 losses are still unknown and decide whether even the DIY exchanger is needed.

---

## 4. Wire harness

### 4a. URC 2027 rules that touch wiring

- **2.a.v:** red push-button E-stop, readily visible and accessible on the rover exterior. Not a knob or rotating switch. It "shall immediately stop the rover's movement and cease all power draw from any and all batteries". "All systems on the rover must have the power switched off by this single E-stop."
- **2.a.vi:** mobile deployables need their own E-stop (except the drone); "a fuse will suffice" for devices that cannot move on their own.
- **2.a.iii:** 50 kg maximum deployed mass (5% penalty per kg over).
- **3.d.iii:** 37.8 C, blowing dust, light rain.
- No other wiring, connector or gauge rules were found in the 2027 Requirements and Guidelines text.

### 4b. Connector table

| Use | Family | Current per contact | Wire range | Locking | IP | Source / notes |
|---|---|---|---|---|---|---|
| Battery main, high current | **Anderson Powerpole PP75** | 120 A UL 1977 / 70 A CSA, wire-to-wire with 6 AWG; 55 A wire-to-PCB | 16-6 AWG (with reducing bushings) | No latch on standard housing. Separate "locking dovetail" housings lock stacked housings together; mated-pair latch TBD | IP10, IP20 | 600 V UL; -20 to 105 C; silver contacts 10,000 cycles. Rating with 8/10 AWG: TBD (datasheet derating chart) |
| Per-driver 24 V feed, motor leads | **Anderson Powerpole PP15/30/45** | 45 A contact: **55 A UL / 40 A CSA** single-pole wire-to-wire with 10 AWG; 3x3 block 40 A UL | 20-10 AWG (barrels 20-16, 16-12, 14-10) | No latch (spring retention); accessory clips/shells TBD | IP10, IP20 | 600 V; -20 to 105 C; silver 10,000 / tin 1,500 cycles; UL hot plug 45 A at 72 V DC (250 cycles); vibration per MIL-STD-202 |
| Battery / power (hobby) | **Amass XT60** (XT60E1 panel-mount sheet) | UL 1977: 20 A with 16 AWG. Wiring table: 12 AWG 40 A (60 K rise) / 45 A (85 K rise); 14 AWG 30/35 A; 16 AWG 25/30 A | 16-12 AWG | Friction fit, no latch | IP40 | DC 500 V; -20 to 120 C; **100 mating cycles**. Machine-translated Amass sheet; check the exact part |
| Battery / power (hobby) | **Amass XT90** | **TBD.** No official Amass sheet found; secondary sources say 40-45 A continuous, 90 A peak | TBD (10 AWG typical) | Friction fit | TBD | Do not use until an Amass sheet is found |
| Board-to-board power and signal inside bay | **Molex Micro-Fit 3.0** | 8.5 A max per contact | 30-26 AWG for terminal 43030-0012. Series range up to 18 AWG per Molex overview (TBD verify) | Latching housing (TBD verify in Molex PS-43045-001) | Unsealed | 3.00 mm pitch |
| Low-current signal inside bay | **JST XH** | 3 A AC/DC (with AWG 22) | AWG 30-22 | Not stated on datasheet p.1 (TBD) | Unsealed | 250 V; -25 to +85 C including self-heating; 2.5 mm pitch |
| Sealed, through the bay wall, signal / small power | **TE Deutsch DTM** | 7.5 A (size 20 contact) | 16-22 AWG (TE page; one TE graphic says 14-22) | Integrated latch + wedgelock | Immersion under 3 ft of water (TE page); IP68 per TE datasheet (TBD verify) | -55 to +125 C; 2-12 positions |
| Sealed, sensors / fans / 12 V branches | **TE Deutsch DT** | 13 A continuous (size 16) | 14-20 AWG | Integrated latch + wedgelock | IP68 (DigiKey); TE brochure says IP67/IP68/IP6K9K with backshell | -55 to +125 C; 2, 3, 4, 6, 8, 12 positions |
| Sealed, motor leads up to 25 A | **TE Deutsch DTP** | 25 A continuous (size 12) | 10-14 AWG | Integrated latch + wedgelock | Immersion under 3 ft of water; IP code not stated (TBD) | -55 to +125 C; 2 and 4 positions. **Below the 30 A MDDS30 continuous rating**, so check real motor current |
| Sealed alternative | **Molex MX150 / MX150L** | **TBD.** Molex pages timed out. Secondary: MX150 up to 22 A (22-14 AWG, USCAR-2); MX150L up to 40 A (8-22 AWG, IP67) | TBD | TBD | TBD | Verify before use |

### 4c. Wire gauge ampacity (ABYC E-11, as published by Blue Sea Systems, at 30 C ambient)

Amps per conductor. "Free air" = E-11 Table VI-A (single conductor in free air). "Bundled" = Table VI-B (up to 3 conductors in a sheath, conduit or bundle). Values outside engine spaces.

| AWG | Free air, 75 C insulation | Free air, 90 C | Free air, 105 C | Bundled, 105 C | Resistance (ohm/1000 m) |
|---|---|---|---|---|---|
| 18 | 10 | 20 | 20 | 14 | 21.88 |
| 16 | 15 | 25 | 25 | 18 | 13.70 |
| 14 | 20 | 30 | 35 | 25 | 8.63 |
| 12 | 25 | 40 | 45 | 32 | 5.42 |
| 10 | 40 | 55 | 60 | 42 | 3.41 |
| 8 | 65 | 70 | 80 | 56 | 2.14 |
| 6 | 95 | 100 | 120 | 84 | 1.35 |

- Bundles of 4-6 conductors: x 0.857. 7-24: x 0.714. 25 or more: x 0.571.
- Blue Sea's conservative rule: use 105 C wire but size circuit protection to the 75 C column unless the wire is openly exposed for cooling.
- The table is at 30 C ambient. **Correction for 37.8 C outside or about 50 C in the bay: TBD** (not in this source).
- Example (EST): 60 A (both MDDS30 channels at 30 A) through 2 m round-trip of 8 AWG gives 0.26 V drop (1.1% of 24 V). The same run in 10 AWG gives 0.41 V.
- What this means for us (EST): an MDDS30 supply at a full 2 x 30 A needs **8 AWG** (bundled 105 C: 56 A, slightly short) or 6 AWG. Motor leads at 30 A: **10 AWG** (bundled 42 A). 12 AWG (bundled 32 A) is tight. **MDDS30 terminal block maximum wire size: TBD.** The manual only says "use wire with proper thickness".
- The real continuous motor current is TBD. It may be well below 30 A, which would allow smaller wire.

### 4d. Harness practices (NASA-STD-8739.4A unless noted)

- **Prevent mis-mating (7.1.2):** different connector sizes next to each other, keying or polarization, clear marking. Battery and motor connectors must not be swappable.
- **Live side gets the socket (7.2.14):** line voltage must sit on socket (female) contacts so no live pins are exposed when unplugged. Battery side = female. Powerpole is genderless, so this needs care.
- **Labelling (7.2.4):** identify every cable, connector and wire. Label both ends with the net name from the schematic.
- **Strain relief (7.2.20, 7.2.28):** wires leaving connectors must be stress-relieved (backshell, boot, or a tie to a fixed point), so the load does not go into the crimp.
- **Support against vibration (7.2.29):** secure harnesses to structure. Tie spacing (Table 9-1): harness ≤6.4 mm diameter, ties at most 19.1 mm apart; 12.7 mm, 38.1 mm; 25.4 mm, 50.8 mm; above 25.4 mm, 76.2 mm. First tie from the connector (Table 9-2): bundle under 12.7 mm, 25.4-50.8 mm; 12.7-25.4 mm, 50.8-76.2 mm; 25.4 mm or larger, 76.2-101.6 mm. These are spaceflight values; a rover can be looser, but they are a good reference.
- **Bend radius (Table 7-1):** harness with AWG 10 or smaller: 10 x OD optimum, 3 x OD minimum. Harness with AWG 8 or larger (or coax): 10 x OD optimum, 6 x OD minimum.
- **Abrasion and sharp edges (7.2.11, 7.2.30, 7.2.31):** protect against chafing and cut-through. Use grommets at every wall hole. Sleeving (braid, spiral wrap, heat-shrink) is covered in sections 9.3-9.11.
- **Crimps (7.2.26):** stranded wire only. No solid or pre-tinned wire in crimp contacts. Use the connector maker's crimp tool.
- **Splices (7.2.12, 7.2.32-7.2.37):** avoid them. If needed, stagger them and keep them out of flex zones.
- **Power vs signal:** the standard requires designing for EMI (7.2.5) but gives no spacing numbers. Practice: run 24 V motor power and CAN/USB/sensor wiring in separate bundles, and twist each motor pair and the CAN pair. **Separation distance: TBD** (no sourced number).
- **Redundant/safety circuits (7.2.7):** redundant wiring must not share a bundle or connector. Apply the same idea to the E-stop loop: route it on its own, away from the motor power bundle.
- **Sealing at the wall:** use sealed bulkhead connectors (Deutsch DT/DTM/DTP) or rated cable glands where wires cross the bay wall. Plug unused cavities with sealing plugs (7.2.15).

---

## 5. Open questions for the mechanical team / Tyler

1. Box material and final size. Is the wall aluminium? Can one 0.30 x 0.15 m or 0.40 x 0.15 m face take two heat-sink cut-outs (about 62 x 100 mm each)?
2. Where can the external heat sink go so it is shaded, not in the wheel spray, and not blocking the E-stop?
3. Weight budget for cooling hardware (DIY exchanger estimated under 1 kg, TBD).
4. MDDS30 orientation: the fins face up and the optional fan blows through the bottom PCB. Can the internal fan airflow pass over all three drivers?
5. Is about 9 W of fan power on 12 V acceptable (vs 76-108 W for a Peltier)?
6. Motor continuous and stall current (sets the motor lead gauge and DTP vs Powerpole outside the box).
7. MDDS30 power terminal maximum wire size (measure the terminal block).
8. Connector standard for the whole rover. Suggested: PP75 battery, PP45 inside the bay for 24 V branches, Micro-Fit 3.0 for board power, JST XH only for light signals, Deutsch DT/DTM/DTP at wall penetrations. Budget for crimp tools: TBD.
9. Does the E-stop open the contactor only, or also a separate logic feed? (2.a.v: "all systems ... switched off by this single E-stop".)

---

## 6. Sources

Heat sinks and coolers
- Cytron MDDS30 User's Manual Rev 1.11 (July 2019): dimensions p.4-5, derating, fan mounting section 9: https://forum.dronebotworkshop.com/wp-content/uploads/wpforo/attachments/5360/6077-MDDS30UserManual.pdf
- Mean Well DDR-60 datasheet (dimensions, 216 g, 91% efficiency for DDR-60G-12, DIN rail): https://www.meanwell.com/Upload/PDF/DDR-60/DDR-60-SPEC.PDF
- DigiKey, Fischer Elektronik LA 6 100 12 (0.205 C/W, 100 x 62 mm, USD 94.86; links Fischer datasheet https://www.fischerelektronik.de/web_fischer/en_GB/VA/LA610012/datasheet.xhtml , which returned 403 to us): https://www.digikey.com/en/products/detail/fischer-elektronik/LA-6-100-12/25992817
- Fischer Elektronik datasheet printout, LA V 6 200 12 (62 x 74 mm, 0.175-0.095 K/W, ebm-papst 612 NHH-118 fan 12 V 2.9 W 56 m3/h, 66 g, -20 to +70 C): https://doc.7-el.ru/l/lav620012.pdf
- Fischer Elektronik datasheet printout, LA 6 250 12 (0.2-0.1 K/W, 12 V/24 V fan): https://doc.7-el.ru/l/la6_250.pdf
- DigiKey, Wakefield Thermal DC0602512U2B-BT0-68 IP68 fan: https://www.digikey.com/en/products/detail/wakefield-thermal-solutions/DC0602512U2B-BT0-68/26859448
- Tark Thermal Solutions AA-040-12-22 datasheet (Qc 41 W, 12 V, 6.3/7.0 A, 76 W, 1.80 kg, -10 to 48 C): https://www.tark-solutions.com/datasheets/AA-040-12-22-LTS-datasheet.pdf
- DigiKey AA-040-12-22-00-00 (160 x 122 x 146.9 mm, USD 357.66): https://www.digikey.com/en/products/detail/laird-thermal-systems-inc/AA-040-12-22-00-00/2269607
- nVent Hoffman TE090624011 product page (24 V DC, NEMA 12/3R/4/4X, IP65, -40 to 55 C, 9.29 x 5.02 x 6.94): https://www.nvent.com/en-us/hoffman/products/encte090624011
- Gexpro listing TE090624011 (178 BTU, 52 W): https://www.gexpro.com/p/461370/nvent-hoffman/thermoelectric-cooler-with-shroud-for-enclosure/783510210762/te090624011
- Steiner Electric listing title TE090624011 (24 VDC, 4.4 A, 24/80 cfm) - page body did not load; TBD: https://www.steinerelectric.com/Product/nVent-HOFFMAN-TE090624011-MCLT-Thermoelectric-Cooler-With-Stainless-Steel-Shrouded24-VDC4-4-A24-cfm-Internal-Loop-80-cfm-External-LoopNEMA-12-3R-4-4X-IP65-Enclosure-626756
- Rittal SK 3201.300: https://www.rittal.com/uk-en/products/deep/3201300
- Advanced Cooling Technologies, sealed enclosure heat pipe coolers (ACT-HPC-15): https://www.1-act.com/?p=37397
- Elmeko PK 100: https://www.elmeko.de/en/details/peltier-kuhlgerat-pk-100

Wire harness
- URC 2027 Requirements and Guidelines (repo root PDF), rules 2.a.iii, 2.a.v, 2.a.vi, 3.d.iii
- Anderson Power Products catalog (PP15-45 and Powerpole Pak specifications, contact tables), mirror: https://www.wagneronline.com.au/attachments/Datasheets/Anderson-PP.pdf
- Anderson Power PP15-45 contact product page (IP10/IP20, -20 to 105 C): https://www.andersonpower.com/?p=405
- Anderson PP75 datasheet (120 A UL / 70 A CSA with 6 AWG, 16-6 AWG, 600 V), CERN mirror: https://sy-dep-epc-lpc.web.cern.ch/components/datasheets/epc-lpc%20(converters)/PP75-power-poles-connectors_(ANDERSON).pdf
- Anderson PP75 product page (IP10/IP20, 10,000 cycles): https://www.andersonpower.com/product/powerpole-pp75-standard-housings-blue/
- Amass XT60E1 product specification (machine-translated): https://electrokit.com/upload/quick/cc/af/7822_410235149en-tds.pdf
- JST XH connector datasheet: https://www.jst-mfg.com/product/pdf/eng/eXH.pdf
- Molex Micro-Fit 3.0 terminal 43030-0012 datasheet (8.5 A max per contact): https://assets.testequity.com/te1/Documents/pdf/Molex/Molex_43030-0012_Datasheet_0725.pdf
- DigiKey, TE Deutsch DT series highlight (13 A, 14-20 AWG, IP68): https://www.digikey.ie/en/product-highlight/t/te-connectivity-deutsch-ict/dt-series-connectors
- TE Deutsch DTM: https://www.te.com/en/products/connectors/automotive-connectors/intersection/deutsch-dtm-connectors.html
- TE Deutsch DTP: https://www.te.com/en/products/connectors/automotive-connectors/intersection/deutsch-dtp-connectors.html
- Blue Sea Systems, ABYC excerpts 2010 ("ABYC Ampacity Rating Table at 30 C", E-11 Tables VI-A/VI-B), mirror: https://stroboflash.com/searaydocs_public/Electrical%20-%20Battery%20-%20Charging/Blue%20Sea/2010_ABYCexcerpts.pdf
- NASA-STD-8739.4A (2016-06-30), Crimping, Interconnecting Cables, Harnesses, and Wiring: https://nepp.nasa.gov/files/27631/nstd87394a.pdf

Sites that blocked or timed out (not bypassed): fischerelektronik.de (403), rs-online (403), farnell (timeout), mouser (timeout), molex.com (timeout), bluesea.com (403).
