# Meeting Notes: Hogan's Part (Cooling + Physical Layout) / 会议笔记：Hogan 的部分（散热 + 布局）

Based on COOLING_PLAN.md and PHYSICAL_LAYOUT.md (commit 9e4ad54). Numbers marked EST are estimates.
依据 COOLING_PLAN.md 和 PHYSICAL_LAYOUT.md（commit 9e4ad54）。标 EST 的数字是估算。

**One-line summary:** Recommend option C (hybrid cooling) and a three-zone layout. Final numbers wait on the box size from the mechanical team and bench measurements of the MDDS30 heat.
**一句话总结：** 散热推荐 C（混合方案），布局按三个分区摆。最终数字要等机械组给箱子尺寸、MDDS30 台架实测发热之后才能定。

## 1. What Hogan's task is / Hogan 的任务是什么

Task 4 sheet: "Hogan is no longer apart of the team. Reassigning to Chris". He left no files.
Task 4 表格写着 Hogan 已离队、任务转给 Chris。他没有留下任何文件。

- **Main task, Cooling:** research cooling for the rover electronics, choose active vs passive, and prepare options for the mechanical team.
  **主任务 Cooling：** 调研电路散热方案，在主动/被动之间选择，整理成能给机械组讲的选项。
- **Secondary task, Physical Layout:** plan where each subsystem PCB sits in the rover, with access from the outside.
  **次任务 Physical Layout：** 规划各子系统 PCB 在车里怎么摆，并且能从外面检修。

Mostly research and options. The only schematic part is a small block of fans and temperature sensors.
主要是调研和出方案，真正要画的原理图只有风扇和温度传感器那一小块。

## 2. Cooling / 散热

### 2.1 The problem / 要解决的问题

URC rule 3.d.iii: up to 37.8 °C, frequent dust, light rain. The bay must shed heat and keep out dust and water, and those two goals conflict.
URC 规则 3.d.iii：现场最高 37.8 °C，常有扬尘，可能小雨。电子舱既要散热又要防尘防雨，这两点互相矛盾。

### 2.2 Heat sources (EST) / 热源（估算）

| Source / 热源 | Heat / 发热 |
|---|---|
| Jetson / Jetson | Up to ~25 W, depends on power mode 7/15/25 W / 最多约 25 W，取决于功率模式 |
| 24→12 V converter / 24→12 V 降压 | ~5.9 W at full load / 满载约 5.9 W |
| 24→5 V converter / 24→5 V 降压 | 0.3–1.8 W |
| Teensy, CAN boards / Teensy、CAN 板 | < 1 W |
| **Total / 合计** | **~34 W + 3× MDDS30 + contactor coil (unknown) / 约 34 W，另加 MDDS30 和线圈（未知）** |

Caveat: the converter models come from the drivetrain prototype parts. The 2027 bay also has the switch, RFD900x and other loads, so total heat will be higher. Same method, re-run with the final parts.
注意：降压模块型号用的是 drivetrain 原型那套。2027 正式版舱里还有交换机、RFD900x 等，总发热会更高。方法不变，零件定了再重算。

### 2.3 Key estimate: how hot a sealed box gets / 关键估算：密封箱有多热

- Assumed box 0.40 × 0.30 × 0.15 m, surface area ≈ 0.45 m².
  假设箱子 0.40 × 0.30 × 0.15 m，表面积约 0.45 m²。
- Temperature rise ΔT = P ÷ (h × A), still air h = 5–10 W/m²K → rise 7.6–15 K.
  温升 ΔT = P ÷ (h × A)，静止空气 h = 5–10 W/m²K → 温升 7.6–15 K。
- **Inside air ≈ 45–53 °C**, before sun on the lid.
  **箱内空气约 45–53 °C**，还没算太阳直晒。
- Why it matters: the MDDS30 starts derating above 50 °C (max current drops from 80 A to 50 A). A fully passive sealed box is borderline.
  为什么重要：MDDS30 超过 50 °C 开始降额（最大电流从 80 A 降到 50 A），纯被动密封处于临界，偏危险。

### 2.4 Three options for the mechanical team / 给机械组的三个方案

| Option / 方案 | How / 做法 | Pros / 优点 | Cons / 缺点 |
|---|---|---|---|
| A. Passive sealed / 被动密封 | Sealed box, hot parts on an aluminium wall with external fins / 密封箱，发热件贴铝墙，外加散热片 | No dust, no fans to fail / 不进灰，无风扇故障 | Inside 45–53 °C, Jetson may throttle / 箱内 45–53 °C，Jetson 可能降频 |
| B. Active filtered / 主动风冷 | Filtered intake fan, positive pressure / 带滤网进风，正压 | Inside near ambient / 箱内接近环境温度 | Filters clog, fans fail, vents need rain shielding / 滤网堵、风扇坏、通风口要防雨 |
| **C. Hybrid (recommended) / 混合（推荐）** | Sealed box + aluminium heat-spreader wall (MDDS30 + DDR-60G) + external fins + one small internal fan / 密封箱 + 铝散热墙（MDDS30 和 DDR-60G）+ 外部散热片 + 舱内小风扇 | Dust-sealed, no hot spots, fan failure not fatal / 防尘、无局部过热、风扇坏了不致命 | More mechanical work, still needs a sun shade / 机械加工多，仍要遮阳 |

### 2.5 Schematic part (small) / 原理图部分（很小）

- 3× MDDS30 fan headers: powered by the driver, auto ON above 50 °C, no Teensy connection.
  3 个 MDDS30 风扇接口：驱动器自己供电，50 °C 以上自动开，不接 Teensy。
- 1× 12 V 4-wire PWM bay fan: Teensy drives it through a 2N7002 MOSFET, because the fan pulls its control line up to 5.25 V and Teensy pins are not 5 V tolerant. Tach line: 10k pull-up to 3.3 V.
  1 个 12 V 四线 PWM 舱内风扇：Teensy 经 2N7002 MOSFET 控制，因为风扇会把控制线上拉到最高 5.25 V，而 Teensy 不耐 5 V。转速线 10k 上拉到 3.3 V。
- 4× DS18B20 probes (battery, bay air, MDDS30 heatsink, converter) on one 1-Wire bus, 4.7k pull-up to 3.3 V.
  4 个 DS18B20 温度探头（电池、舱内空气、MDDS30 散热片、降压模块），共用一条 1-Wire 总线，4.7k 上拉到 3.3 V。
- Proposed Teensy pins 32 / 10 / 11; confirm with Lance or Paul.
  Teensy 引脚提案 32 / 10 / 11，待 Lance 或 Paul 确认。

### 2.6 How to decide between A and C / 如何在 A 和 C 之间定案

Bench tests / 台架测试：
1. Run each MDDS30 at the expected current for 20–30 min and log heatsink temperature.
   MDDS30 按预期电流跑 20–30 分钟，记录散热片温度。
2. Log Jetson temperature in the chosen power mode.
   Jetson 在选定功率模式下记录温度。
3. Re-run the estimate with the real numbers and the mechanical team's box size.
   用实测数据和机械组的箱子尺寸重算。

## 3. Physical Layout / 布局

### 3.1 Rules / 规则约束

- 2.a.ii: rover must fit a 1.2 m cube, antenna mast included, so it must fold.
  2.a.ii：整车放进 1.2 m 立方体，天线杆也算，要能折叠。
- 2.a.iii: arm and science modules are swapped, so their electronics use a quick-disconnect at the bay wall.
  2.a.iii：机械臂和科学模块会换装，电子部分在舱壁用快拆接头。
- 2.a.v: E-stop on the exterior, visible and reachable.
  2.a.v：E-stop 装在车外显眼位置。

### 3.2 Area budget / 面积预算

- Verified module sizes (3× MDDS30, Jetson, DDR-60G, 5 V converter, Teensy, RFD900x, switch) add up to ≈ **0.05 m²**.
  已核实尺寸的模块（3 块 MDDS30、Jetson、DDR-60G、5 V 降压、Teensy、RFD900x、交换机）合计约 **0.05 m²**。
- With wiring, connectors and airflow: **0.10–0.13 m² plate** (≈ 400 × 250 to 400 × 300 mm), inside height **100–150 mm** (tallest part DDR-60G, 54.5 mm).
  加上走线、接头、通风：需要 **0.10–0.13 m² 安装板**（约 400 × 250 到 400 × 300 mm），舱内高度 **100–150 mm**（最高的 DDR-60G 是 54.5 mm）。
- Matches the box assumed for cooling; will get tighter once subsystem PCB sizes are known.
  跟散热假设的箱子对得上；其他子系统板尺寸定了之后会更挤。

### 3.3 Three zones / 三个分区

- **Power/drive zone:** main fuse → contactor → fuse block → 3× MDDS30, near the battery, on the heat-spreader wall.
  **功率/驱动区：** 主保险丝 → contactor → fuse block → 3 块 MDDS30，靠近电池，贴散热墙。
- **Logic zone:** converters, Teensy + CAN, Jetson (needs open air above its fan).
  **逻辑区：** 降压模块、Teensy + CAN、Jetson（风扇上方要留空间）。
- **Comms/RF zone:** switch, RFD900x next to the antenna feed-through, short coax.
  **通信/RF 区：** 交换机、RFD900x 放在天线出线口旁，同轴线短。

Rules / 原则：
- Short high-current path. / 大电流路径短。
- Drivers (18 kHz, tens of amps) away from signal and RF. / 驱动器远离信号线和射频。
- CAN as one line, 120 Ω at both ends. / CAN 接成一条线，两端各一个 120 Ω 终端电阻。
- Every board on connectors, removable on its own. / 每块板用接插件，可单独拆下。

### 3.4 Access from outside / 外部检修

- E-stop and start button on an exterior panel. / E-stop 和启动按钮在外部面板。
- Fuse block behind the access panel; change fuses without removing boards. / 保险丝座在检修面板后，换保险丝不用拆板。
- Panel-mount USB and RJ45 on the bulkhead; flash firmware with the lid closed. / USB 和网口用面板式延长口引到舱壁，盖着盖子也能刷固件。
- Battery in its own bay, swapped from outside. / 电池独立舱，从外面换。
- One quick-disconnect each for the arm and science modules. / 机械臂和科学模块各一个快拆接头。

### 3.5 Correction / 一处修正

The optional MDDS30 fan mounts **between the two PCBs** and needs intake clearance **below** the driver, not space above (MDDS30 manual Rev 1.3). Fixed in commit 9e4ad54; the PHYSICAL_LAYOUT.docx on the Drive is still the old version.
MDDS30 的可选风扇装在**上下两层 PCB 之间**，下面要留进风空间，不是在上方留空间（MDDS30 手册 Rev 1.3）。已在 commit 9e4ad54 修正；Drive 上的 PHYSICAL_LAYOUT.docx 还是旧版。

## 4. What to ask for at the meeting / 会上要向别人要的东西

- **Mechanical team:** box size and material, battery bay location. Biggest gap.
  **机械组：** 箱子尺寸和材料、电池舱位置。这是最大的缺口。
- **Software team:** which Jetson power mode (7/15/25 W).
  **软件组：** Jetson 跑哪个功率模式（7/15/25 W）。
- **Lance:** contactor part (coil heat, zone 1 size), Teensy pin sign-off.
  **Lance：** contactor 型号（线圈发热、zone 1 尺寸），确认 Teensy 引脚。
- **Subsystem owners (Bryan, Paul, Krishna, Ricky, Kaden):** board sizes and interface lists.
  **各子系统负责人（Bryan、Paul、Krishna、Ricky、Kaden）：** 板子尺寸和接口清单。
- **Toka:** Power Rail Table rows 1–4 list a 6S LiPo, STM32, OAK-D, Ouster and "eight 24 V motors", which do not match our Teensy/Jetson/6-motor architecture. Where did they come from?
  **Toka：** Power Rail Table 第 1–4 行写的是 6S LiPo、STM32、OAK-D、Ouster、"eight 24 V motors"，跟 Teensy/Jetson/6 电机架构对不上，这些是从哪来的？

## 5. Likely questions / 可能被问到的问题

**Q: Why not seal it completely? / 为什么不直接全密封？**
A: The estimate puts the inside at 45–53 °C, right at the 50 °C point where the MDDS30 starts derating. With sun on top there is not enough margin.
答：估算箱内 45–53 °C，正好卡在 MDDS30 开始降额的 50 °C，加上太阳直晒，余量不够。

**Q: Why not just cut vents and add fans? / 为什么不直接开孔加风扇？**
A: Dust clogs filters, fans fail, and rain gets in. Option C keeps working if its fan fails.
答：现场灰大，滤网会堵，风扇会坏，雨会进来。C 方案风扇坏了也还能撑住。

**Q: How accurate are these numbers? / 这些数准吗？**
A: They are estimates, marked EST. The box size is my assumption and the MDDS30 heat is not in its manual. The mechanical team's dimensions and bench tests will set the final numbers. Today I'm presenting the method and the direction, not final values.
答：是估算，已标 EST。箱子尺寸是我假设的，MDDS30 发热手册里没给。要靠机械组尺寸和台架实测来定。今天提出的是方法和方向，不是最终数字。

## Notes / 笔记

-
-
-
