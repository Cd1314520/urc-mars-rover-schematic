# Integration: Everybody's KiCad in One Project

This folder brings every subsystem schematic into **one KiCad project**, so the whole rover can be checked with one ERC and later turned into PCBs. It matches the Drive folder `_2.2.3.2.7 Integration of everybody's KiCad`.

Repo: https://github.com/Cd1314520/urc-mars-rover-schematic (public: anyone can read it, only collaborators can push).

---

## 1. What the KiCad files are

A KiCad project is a folder of several files. Each file holds a different part of the design.

| File | What it is | Push it? |
|---|---|---|
| `.kicad_pro` | The **project file**. It opens the project and stores its settings: ERC rules, net classes, text sizes. It does not contain the drawing itself. | **Yes**, once (Chris owns the integration one) |
| `.kicad_sch` | A **schematic sheet**: the symbols, wires and labels. This is the file you draw in. One project can have many sheets: one root sheet plus one sheet per subsystem. | **Yes**, your own sheet |
| `.kicad_pcb` | The **PCB layout**: board outline, footprints, copper traces. It is empty until we start layout. | Later, when we do PCBs |
| `.kicad_sym` | A **symbol library**: custom symbols you drew yourself (for example a module that is not in KiCad's library). | **Yes**, into `libraries/` |
| `.pretty/` folder | A **footprint library**: one `.kicad_mod` file per custom footprint. | Later, into `libraries/` |
| `sym-lib-table`, `fp-lib-table` | Lists of which libraries this project uses and where they are. | Yes (Chris maintains them) |
| `.kicad_prl` | Your **personal view settings**: zoom, open windows, layer visibility. | **No** (ignored automatically) |
| `*-backups/`, `_autosave-*`, `*.lck`, `fp-info-cache` | Auto-backups, lock files and caches made by KiCad while you work. | **No** (ignored automatically) |

The repo's `.gitignore` already skips the "No" files, so you cannot push them by accident.

**Simple version:** `.kicad_pro` = the binder, `.kicad_sch` = the drawing pages inside it, `.kicad_pcb` = the board you build from those pages.

---

## 2. Folder layout

```
Integration/
  README.md                       <- this file
  URC2027_Integration.kicad_pro   <- project file (Chris)
  URC2027_Integration.kicad_sch   <- root sheet: one box per subsystem (Chris)
  PDP.kicad_sch                   <- Bryan
  Compute_Logic.kicad_sch         <- Paul
  Drivetrain.kicad_sch            <- Krishna
  Comms_Navi.kicad_sch            <- Chris
  Robo_Arm.kicad_sch              <- Ricky
  Sci_Package.kicad_sch           <- Kaden
  Wheel_Encoders.kicad_sch        <- owner TBD
  libraries/
    URC2027.kicad_sym             <- shared custom symbols
  exports/
    <Subsystem>_<YYYY-MM-DD>.pdf  <- PDF of each sheet for people without KiCad
```

**Use these exact file names.** The root sheet looks for your sheet by its file name. If you rename it, your box on the root sheet goes blank.

Every sheet already exists. Comms_Navi is the real sheet; the others are **placeholders** that say "PLACEHOLDER" on the page. Upload your sheet with the same file name and it replaces the placeholder.

---

## 3. Rules for your sheet

1. **KiCad 10 only.** Our files are KiCad 10 format. KiCad 8 or 9 cannot open them.
2. **Edit only your own sheet.** The root sheet, `libraries/` and the `.kicad_pro` are shared. Ask in the group chat before you change them.
3. **Power: use the agreed net names** (section 4). Two nets with different names are two different wires to KiCad, even if they are both "12 V" to us.
4. **Signals that leave your sheet: global labels (Ctrl+L)** with the right shape. Use **Output** if your sheet drives the signal, **Input** if your sheet receives it, and **Bidirectional** for I2C SDA or CAN. Signals that stay on your sheet use local labels (L).
5. **Off-board parts are connectors.** A motor, sensor or module that plugs in by cable is drawn as a connector, not as the whole device (Tyler's style).
6. **Fill in the title block:** title, date, rev and your name.
7. **Run ERC** (Inspect → Electrical Rules Checker) before you push. Fix the errors, or write a note saying why one is OK.
8. **Custom symbols go into `libraries/URC2027.kicad_sym`**, not into a library on your own C: drive. If the library path starts with `C:/Users/...`, it only works on your computer.
9. **Reference numbers:** when everything is merged, Chris will run Annotate with "first free number after sheet number x 100". The sheet number is the page number in the root sheet, so PDP parts become 2xx, Compute/Logic 3xx, Drivetrain 4xx, Comms/Navi 5xx, Robo Arm 6xx, Sci Package 7xx and Wheel Encoders 8xx. Two `F1`s then cannot clash. You do not need to do anything for this. (Compute/Logic already uses 3xx.)

---

## 4. Net names (to agree as a team)

The sheets use different names for the same rail today. KiCad will not join them until the names match. **This table is a proposal.** Bryan's PDP sheet is the source of the rails, so his names are the starting point. Tyler and Bryan should confirm it before anyone renames anything.

| Rail | PDP (Bryan) | Drivetrain | Robo Arm | Comms/Navi | Sci Package | Proposed name |
|---|---|---|---|---|---|---|
| 24 V after contactor | `24V_MAIN`, `24V_FUSED`, `24V_AUX` | `+24V` (local) | `24V_MAIN`, `24V_MAIN_IN` (local) | – | `24V_FROM_PDB` (local) | `24V_MAIN` / `24V_FUSED` (Bryan to say which is which) |
| 12 V | `12V_MAIN` | – | – | `+12V` | `12V_IN` (local) | `12V_MAIN` |
| 5 V | `5V_MAIN` (plus a typo `5A_MAIN`) | `+5V` (local) | `5V_MAIN` (local) | `+5V` | `5V_SCI` (local) | `5V_MAIN` |
| 3.3 V | – | `+3V3` (local) | `3.3V` (local) | `+3V3_IMU` (local) | `3V3_SCI` (local) | Keep local: each sheet makes its own 3.3 V |
| Ground | `GND` plus `12V_GND`, `5V_GND` | `GND` | `GND`, `SERVO_GND` | `GND` | `GND` | `GND` (one ground; Bryan to confirm `12V_GND` and `5V_GND` join it) |

A **local label** only works inside its own sheet. A rail that comes from the PDP has to be a **power symbol or a global label**, with exactly the agreed name.

---

## 5. How to push your file

You need **collaborator access** first. Send Chris your GitHub username; he adds you, then you accept the email invite.

**Your email becomes public.** Every commit shows the author's email. To hide yours: GitHub → Settings → Emails → tick "Keep my email addresses private". Then use the `...@users.noreply.github.com` address it shows you.

### Option A: in the browser (easiest, no install)

1. Open the repo, then click into the `Integration` folder.
2. Click **Add file → Upload files**.
3. Drag in your `.kicad_sch` (and a PDF into `exports/` if you want).
   - Uploading a file with the same name **replaces** the old one. That is how you update.
4. Under "Commit changes", write what you changed, for example `Drivetrain: add encoder level shifters`.
5. Leave **Commit directly to the main branch** selected and click **Commit changes**.

### Option B: GitHub Desktop (easy, keeps a copy on your PC)

1. Install GitHub Desktop and sign in.
2. **File → Clone repository → URL** and paste the repo link. Pick a folder, for example `Documents\GitHub`.
3. Before you start working, click **Fetch origin**, then **Pull**. This gets everyone else's latest files.
4. Copy or save your sheet into `Integration\` with the exact file name from section 2.
5. GitHub Desktop lists the changed files. **Tick only your own files**, write a summary, then click **Commit to main**.
6. Click **Push origin**.

### Option C: command line (Git for Windows)

One-time setup (Windows Terminal or PowerShell):

```bash
git config --global user.name "Your Name"
git config --global user.email "your-id+username@users.noreply.github.com"
git clone https://github.com/Cd1314520/urc-mars-rover-schematic.git
```

Every time:

```bash
cd urc-mars-rover-schematic
git pull
```

Copy or save your sheet into `Integration/`, then add **only your files** (not `git add .`), commit and push:

```bash
git add Integration/Drivetrain.kicad_sch
git commit -m "Drivetrain: add encoder level shifters"
git push
```

The first push opens a browser window to sign in to GitHub. If `git push` says "rejected", someone pushed before you. Run `git pull`, then `git push` again.

### If two people changed the same file

KiCad files are text, but Git cannot merge two drawings safely. That is why **one person owns each sheet**. If you get a "merge conflict", stop and message Chris instead of guessing.

---

## 6. Checklist before you push

- [ ] Opened in KiCad 10, saved, file name matches section 2
- [ ] Title block filled in (title, date, rev, name)
- [ ] ERC run; errors fixed or explained in a text note on the sheet
- [ ] Power rails use the agreed names (section 4); signals leaving the sheet use global labels with a direction
- [ ] No `C:/Users/...` library paths; custom symbols in `libraries/URC2027.kicad_sym`
- [ ] Only your own files in the commit
- [ ] PDF exported to `exports/` (File → Plot → PDF) for teammates without KiCad
