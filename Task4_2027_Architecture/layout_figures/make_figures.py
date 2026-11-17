"""Physical layout visualisation: (1) electronics bay top view to scale, (2) rover side view (illustrative)."""
import sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Polygon, FancyArrowPatch

out = sys.argv[1]
os.makedirs(out, exist_ok=True)

Z1, Z2, Z3 = "#F4CCCC", "#D9EAD3", "#CFE2F3"
KNOWN, TBD = "#FFFFFF", "#FFF2CC"


def box(ax, x, y, w, h, label, fc=KNOWN, tbd=False, fs=7, ls="-"):
    ax.add_patch(Rectangle((x, y), w, h, fc=TBD if tbd else fc, ec="#333", lw=1, ls="--" if tbd else ls, zorder=3))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, zorder=4, wrap=True)


# ---------- Figure 1: bay top view, to scale (mm) ----------
W, H = 400, 300  # plate, matches COOLING_PLAN.md assumed box
fig, ax = plt.subplots(figsize=(13, 10.5))
ax.set_xlim(-75, W + 60)
ax.set_ylim(H + 100, -75)  # y down: front (access panel) at top
ax.set_aspect("equal")
ax.axis("off")

# zones
ax.add_patch(Rectangle((0, 0), 195, H, fc=Z1, ec="none", zorder=1))
ax.add_patch(Rectangle((195, 0), 205, 172, fc=Z2, ec="none", zorder=1))
ax.add_patch(Rectangle((195, 172), 205, 128, fc=Z3, ec="none", zorder=1))
ax.add_patch(Rectangle((0, 0), W, H, fc="none", ec="black", lw=2.5, zorder=5))
ax.text(124, 297, "ZONE 1\nPOWER /\nDRIVE", fontsize=8, weight="bold", color="#990000", va="bottom", zorder=6)
ax.text(397, 166, "ZONE 2  LOGIC", fontsize=8, weight="bold", color="#38761D", ha="right", va="bottom", zorder=6)
ax.text(200, 298, "ZONE 3  COMMS / RF", fontsize=8, weight="bold", color="#0B5394", ha="left", va="bottom", zorder=6)

# zone 1: three MDDS30, footprint = bottom cover 101.60 x 96.52 (manual Rev 1.11 p.5) + power path (TBD sizes)
for i, (y, lbl) in enumerate([(2, "LF / RF"), (101.5, "LM / RM"), (201, "LR / RR")]):
    box(ax, 8, y, 101.6, 96.52, f"MDDS30 #{i+1}\n101.6 x 96.5\n(fins up, ~42 tall)\nmotors {lbl}", fs=7.5)
box(ax, 122, 205, 62, 40, "Class T fuse\n+ holder\n(size TBD)", tbd=True, fs=6.5)
box(ax, 122, 140, 62, 55, "Contactor\n+ pre-charge\n(size TBD)", tbd=True, fs=6.5)
box(ax, 122, 12, 62, 70, "Fuse block\n(blade fuses,\nbehind access\npanel; TBD)", tbd=True, fs=6.5)
box(ax, 122, 90, 62, 40, "PDP board\n(Bryan, TBD)", tbd=True, fs=6.5)

# zone 2
box(ax, 202, 8, 52.5, 54.5, "DDR-60G-12\n24->12 V\nDIN, 90 tall", fs=6.5)
box(ax, 262, 8, 17.8, 20.3, "", fs=5)
ax.annotate("D36V28F5\n24->5 V", (271, 28), (272, 52), fontsize=6, ha="center", zorder=6,
            arrowprops=dict(arrowstyle="-", lw=0.6))
box(ax, 290, 8, 100, 79, "Jetson Orin Nano\n100 x 79\n(own fan: keep\nspace above clear)", fs=7)
box(ax, 202, 95, 120, 70, "", tbd=True)
ax.text(262, 101, "Compute/Logic board (Paul, size TBD)", fontsize=6.3, ha="center", va="top", zorder=6)
box(ax, 210, 125, 61, 17.8, "Teensy 4.1  61 x 17.8", fs=6)
box(ax, 278, 120, 38, 28, "CAN\nboard", tbd=True, fs=6)
ax.annotate("", (340, 87), (316, 134), arrowprops=dict(arrowstyle="-", lw=1.4, color="#38761D"), zorder=6)
ax.text(346, 115, "CAN bus: one line,\n120 ohm at both ends\n(Teensy <-> Jetson J17)", fontsize=6, color="#38761D", zorder=6)

# zone 3
box(ax, 202, 182, 94, 104, "Gigabit switch\nL-com SWTC-GS105NA\n~94 x 104 EST", fs=6.5)
box(ax, 304, 180, 90, 62, "Comms/Navi board\n(Chris, size TBD)\nfuses F1-F7, GPS/IMU\nconn., RFD 5 V reg.", tbd=True, fs=6)
box(ax, 304, 252, 57, 30, "RFD900x\n57 x 30", fs=6.5)
box(ax, 366, 248, 28, 44, "PoE\ninj.\nTBD", tbd=True, fs=6)

# access panel (front) and bulkhead (rear)
ax.add_patch(Rectangle((0, -14), W, 10, fc="#666", ec="none", zorder=5))
ax.text(W / 2, -18, "FRONT: access panel on captive screws  |  panel-mount USB + RJ45 for Teensy / Jetson  |  blade fuses reachable here",
        fontsize=7.5, ha="center", va="bottom", weight="bold")
ax.add_patch(Rectangle((0, H + 4), W, 10, fc="#666", ec="none", zorder=5))
ax.text(W / 2, H + 18, "REAR: bulkhead connectors and cable glands (dust + light rain, rule 3.d.iii)",
        fontsize=7.5, ha="center", va="top", weight="bold")
for x, lbl, c in [(150, "24 V battery cable IN\n(8 AWG min / 6 AWG)", "#990000"),
                  (55, "motor harness OUT\n(10-12 AWG, TBD)", "#990000"),
                  (250, "arm + science\nquick-disconnect\n(power + CAN, 2.a.iii)", "#555"),
                  (355, "antenna coax +\nEthernet to mast", "#0B5394")]:
    ax.add_patch(FancyArrowPatch((x, H + 55), (x, H + 3), arrowstyle="<|-|>", mutation_scale=10, lw=1.4, color=c, zorder=6))
    ax.text(x, H + 58, lbl, fontsize=6.5, ha="center", va="top", color=c)

# heat-spreader wall hint and E-stop
ax.add_patch(Rectangle((-10, 0), 8, H, fc="#999", ec="none", zorder=5))
ax.add_patch(Rectangle((-46, 100), 34, 100, fc=TBD, ec="#333", ls="--", zorder=5))
ax.text(-29, 150, "outside\nheat sink\n+ IP68 fan", fontsize=5.5, ha="center", va="center", zorder=6)
ax.text(-50, H / 2, "through-wall air-to-air exchanger (COOLING option C, revised): position TBD with mech team", rotation=90, fontsize=7, ha="right", va="center")
ax.add_patch(Circle((-35, -40), 14, fc="#CC0000", ec="black", zorder=6))
ax.text(-35, -40, "E-STOP", fontsize=5.5, color="white", ha="center", va="center", weight="bold", zorder=7)
ax.text(-15, -40, "on the rover exterior (2.a.v),\nwired to the contactor coil", fontsize=6.5, va="center")

# scale bar
ax.plot([300, 400], [-50, -50], color="black", lw=2)
ax.text(350, -47, "100 mm", ha="center", va="top", fontsize=7)
ax.set_title("URC 2027 electronics bay - top view, to scale (400 x 300 mm plate, ~100-150 mm tall)\n"
             "White = verified size from datasheet.  Yellow dashed = size TBD (placeholder).  Draft 2026-11-09",
             fontsize=10)
fig.savefig(os.path.join(out, "bay_top_view.png"), dpi=170, bbox_inches="tight")
plt.close(fig)

# ---------- Figure 2: rover side view, illustrative ----------
fig, ax = plt.subplots(figsize=(13, 8))
ax.set_xlim(-150, 1450)
ax.set_ylim(-80, 1330)
ax.set_aspect("equal")
ax.axis("off")
# 1.2 m cube outline
ax.add_patch(Rectangle((0, 0), 1200, 1200, fc="none", ec="#999", ls="--", lw=1.2))
ax.text(5, 1210, "1.2 m stowed-size limit (rule 2.a.ii)", ha="left", fontsize=8, color="#666")
# wheels + rocker-bogie
for x in (170, 600, 1030):
    ax.add_patch(Circle((x, 130), 125, fc="#444", ec="black", zorder=2))
    ax.add_patch(Circle((x, 130), 30, fc="#999", ec="black", zorder=3))
ax.plot([170, 385, 600], [130, 330, 130], color="#777", lw=6, zorder=1)
ax.plot([385, 700, 1030], [330, 400, 130], color="#777", lw=6, zorder=1)
ax.text(600, -30, "6 wheel motors (3 x MDDS30, 2 channels each)  -  harness to bay through glands", ha="center", fontsize=8)
# chassis body
ax.add_patch(FancyBboxPatch((180, 380), 860, 280, boxstyle="round,pad=4", fc="#EEEEEE", ec="black", lw=1.5, zorder=3))
ax.text(1030, 392, "Chassis body" + chr(10) + "(size TBD, mech team)", fontsize=7.5, ha="right", va="bottom", zorder=5)
# battery bay low and central
ax.add_patch(Rectangle((430, 395), 340, 95, fc="#FCE5CD", ec="black", zorder=4))
ax.text(600, 442, "BATTERY BAY" + chr(10) + "(low + central, swap from outside)", ha="center", va="center", fontsize=7.5, zorder=5)
# electronics bay above it
ax.add_patch(Rectangle((300, 505), 600, 140, fc="#FFFFFF", ec="black", lw=1.5, zorder=4))
ax.text(600, 575, "ELECTRONICS BAY\nsealed, ~400 x 300 x 150 mm EST\n(zones 1-3 and parts: see top view)", ha="center", va="center", fontsize=8, zorder=6)
# fins on side
for k in range(6):
    ax.plot([300 - 6 - 8 * k, 300 - 6 - 8 * k], [515, 635], color="#888", lw=1, zorder=4)
ax.text(275, 505, "fins", fontsize=7, ha="center", va="top", zorder=6)
# E-stop
ax.add_patch(Rectangle((930, 660), 50, 30, fc="#333", zorder=5))
ax.add_patch(Circle((955, 708), 22, fc="#CC0000", ec="black", zorder=6))
ax.annotate("E-stop: red, exterior,\nhigh and visible (2.a.v)", (955, 730), (1000, 880), fontsize=8,
            arrowprops=dict(arrowstyle="->"), ha="left")
# mast
ax.add_patch(Rectangle((840, 660), 26, 440, fc="#999", ec="black", zorder=3))
ax.add_patch(Rectangle((800, 1060), 106, 40, fc="#CFE2F3", ec="black", zorder=4))
ax.text(853, 1080, "Groove", fontsize=6.5, ha="center", va="center", zorder=5)
ax.plot([820, 820], [1100, 1190], color="black", lw=2)
ax.plot([886, 886], [1100, 1190], color="black", lw=2)
ax.add_patch(Rectangle((845, 1100), 18, 14, fc="#B4A7D6", ec="black", zorder=5))
ax.annotate("Mast: Groove 52ac + antennas (fold for 1.2 m),\nGPS antenna on top (open sky),\ncameras on the mast", (870, 1150), (960, 1180),
            fontsize=8, arrowprops=dict(arrowstyle="->"), va="center")
ax.add_patch(Rectangle((870, 900), 50, 34, fc="#D9D2E9", ec="black", zorder=4))
ax.text(925, 917, "cams", fontsize=6.5, va="center")
# lidar front
ax.add_patch(Rectangle((1040, 600), 60, 50, fc="#D9D2E9", ec="black", zorder=4))
ax.text(1105, 625, "LiDAR / D435i\n(front, field of view)", fontsize=7.5, va="center")
# arm front, science rear
ax.plot([1040, 1120, 1185], [450, 560, 470], color="#E69138", lw=8, solid_capstyle="round", zorder=2)
ax.text(1215, 560, "Robo arm (stowed)\n(swappable, 2.a.iii)\nquick-disconnect\nat bay wall", fontsize=7.5, va="top")
ax.add_patch(Rectangle((30, 420), 145, 190, fc="#D0E0E3", ec="black", zorder=4))
ax.text(102, 515, "Science\nmodule\n(swappable)", fontsize=7.5, ha="center", va="center", zorder=5)
ax.text(-140, 1300, "REAR", fontsize=9, weight="bold")
ax.text(1420, 1300, "FRONT", fontsize=9, weight="bold", ha="right")
ax.set_title("URC 2027 rover - where things go (side view, ILLUSTRATIVE ONLY, not to scale; chassis is TBD)\n"
             "Draft 2026-11-09 from PHYSICAL_LAYOUT.md", fontsize=10)
fig.savefig(os.path.join(out, "rover_side_view.png"), dpi=170, bbox_inches="tight")
print("ok")
