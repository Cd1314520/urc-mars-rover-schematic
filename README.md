# URC Rover – Original Architecture Schematic

KiCad 10 project translating the team's Canva flowchart (original architecture) into a schematic.

## Structure

The root sheet `Task2_Flowchart_Schematic.kicad_sch` holds one hierarchical sheet per subsystem:

| Sheet file | Subsystem | Owner |
|---|---|---|
| `lidar_navigation.kicad_sch` | RPLIDAR S2, SparkFun GPS-RTK-SMA, antenna | Chris |
| `drivetrain.kicad_sch` (to be added) | Drivetrain | Krishna |

Custom symbols live in `rover_modules.kicad_sym` (project-specific library, already registered in `sym-lib-table`).

## Workflow

1. **Pull** before you open KiCad.
2. Only edit **your own** subsystem sheet.
3. The root sheet and `rover_modules.kicad_sym` are shared: say so in the team chat before editing them, and push right after.
4. Run ERC, save, then **commit + push** with a short message saying what changed.
5. Never have the same `.kicad_sch` open by two people at once.

## Adding your subsystem

1. Pull, open `Task2_Flowchart_Schematic.kicad_pro`.
2. On the root sheet press **S** (Place → Hierarchical Sheet), name the file `<subsystem>.kicad_sch`.
3. Use `+5V` / `GND` power symbols for power, and hierarchical labels (**H**) for signals leaving your sheet.
