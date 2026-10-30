# Component Schematic Specification: MOV1 (Line Surge Varistor)

## 1. Component Metadata
* **Reference Designator**: `MOV1`
* **Component Type**: Metal Oxide Varistor (MOV) Transient Surge Suppressor
* **Manufacturer**: Bourns Inc.
* **Primary MPN**: `MOV-14D471K`
* **Alternate Manufacturer**: Littelfuse
* **Alternate MPN**: `V300LA20AP`
* **Package / Footprint**: Radial Disc (Body diameter: $14.0\,	ext{mm}$, Lead spacing: $7.5\,	ext{mm}$)
* **Subsystem**: Stage 1 (Mains AC Input & Protection)

## 2. Electrical Ratings & Constraints
* **Max Continuous Operating Voltage**: $300\,	ext{V}_{	ext{AC RMS}}$ / $385\,	ext{V}_{	ext{DC}}$ ($13.2\%$ safety margin above $265\,	ext{V}_{	ext{AC}}$)
* **Nominal Varistor Voltage ($V_N$)**: $470\,	ext{V} \pm 10\%$ @ $1\,	ext{mA}_{	ext{DC}}$
* **Maximum Clamping Voltage ($V_C$)**: $775\,	ext{V}$ @ $50.0\,	ext{A}$ ($8/20\,\mu	ext{s}$ surge)
* **Peak Surge Current ($I_{	ext{max}}$)**: $4500\,	ext{A}$ ($8/20\,\mu	ext{s}$ single wave)
* **Energy Absorption Capacity**: $125.0\,	ext{Joules}$
* **Compliance**: IEC 61000-4-5 Level 3 ($1.0\,	ext{kV}$ line-to-line surge test, derating $3.1\% \ll 60\%$)

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Terminal 1 | `AC_LINE_FUSED` | Fuse `F1` output, `C_X1` Pin 1, `L_CM1` Pin 1 | $2.5\,	ext{mm}$ width (2oz Cu). Solder directly across line bus. |
| **2** | Terminal 2 | `AC_NEUTRAL_PROT`| `NTC1` output, `C_X1` Pin 2, `L_CM1` Pin 2 | $2.5\,	ext{mm}$ width (2oz Cu). Solder directly across line bus. |

## 4. Schematic Symbol Representation
```
                     Net: AC_LINE_FUSED
                             │
                           ┌─┴─┐
                           │   │  MOV1: 300V RMS / 470V
                           │   │  Bourns MOV-14D471K
                           └─┬─┘
                             │
                   Net: AC_NEUTRAL_PROT
```

## 5. Schematic & PCB Layout Guidelines
1. **Parallel Placement**: Solder `MOV1` directly between `AC_LINE_FUSED` and `AC_NEUTRAL_PROT` immediately downstream of `F1` and `NTC1`. If the MOV degrades into a thermal short, `F1` opens instantly without fire hazard.
2. **Clearance**: Maintain $\ge 3.0\,	ext{mm}$ copper clearance around `MOV1` terminals.
