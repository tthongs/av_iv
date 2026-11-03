# Component Schematic Specification: C_X1, C_X2 & C_Y1, C_Y2 (Safety Capacitors)

## 1. Component Metadata
* **Reference Designators**:
 * `C_X1`, `C_X2`: Class X2 Across-The-Line Metallized Polypropylene Film Capacitors
 * `C_Y1`, `C_Y2`: Class Y1 Line-To-Earth Double Reinforced Ceramic Capacitors
* **Manufacturers**: KEMET (`R46` Series for X2, `PHE850` Series for Y1) / Murata (`DE1E3KX222M`)
* **Primary MPNs**:
 * `C_X1, C_X2`: `R46KI32200001M` (0.22 µ F ± 20%, 310 V_ AC RMS, Pitch 15.0 mm)
 * `C_Y1, C_Y2`: `PHE850ED6220MD15R06L2` (2.2 nF ± 20%, 400 V_ AC RMS, Pitch 10.0 mm)
* **Subsystem**: Stage 1 (Mains AC Input & EMI Filter)

## 2. Electrical Ratings & Safety Limits
* **Class X2 Capacitors**:
 * Rated AC Voltage: 310 V_ AC RMS (Continuous line-to-line operation)
 * Self-healing metallized polypropylene dielectric.
 * Role: Attenuates differential-mode switching noise.
* **Class Y1 Capacitors**:
 * Rated AC Voltage: 400 V_ AC RMS (Reinforced line-to-earth insulation)
 * Proof withstand voltage: > 4000 V_ AC for 60 seconds.
 * Earth Leakage Current Calculation:
 I_ leak = 2π imes f imes V_ IN,max imes (C_ Y1 + C_ Y2) = 2π imes 50 Hz imes 265 V imes 4.4 nF = 0.366 mA
 Strictly complies with the IEC 62368-1 allowable touch-current limit of < 0.75 mA.

## 3. Schematic Pin Connections & Net Mapping
| Ref Des | Pin 1 Net Name | Connected To | Pin 2 Net Name | Connected To | Safety Role |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **`C_X1`** | `AC_LINE_FUSED` | Fuse `F1`, `MOV1`, `L_CM1` Pin 1 | `AC_NEUTRAL_PROT` | `NTC1`, `MOV1`, `L_CM1` Pin 4 | Pre-filter differential noise bypass. |
| **`C_X2`** | `AC_LINE_FILT` | `L_CM2` Pin 2, Bridge `BR1` Pin 2 | `AC_NEUTRAL_FILT` | `L_CM2` Pin 3, Bridge `BR1` Pin 3 | Post-filter differential noise bypass. |
| **`C_Y1`** | `AC_LINE_CM1` | Node between `L_CM1` & `L_CM2` | `EARTH_GND` | Chassis Earth Stud / Earth Pin of J1 | Line-to-Earth common mode noise drain. |
| **`C_Y2`** | `AC_NEUTRAL_CM1`| Node between `L_CM1` & `L_CM2` | `EARTH_GND` | Chassis Earth Stud / Earth Pin of J1 | Neutral-to-Earth common mode noise drain. |

## 4. Schematic Symbol Representation
```
 Net: AC_LINE_FUSED Net: AC_LINE_FILT
 ───────────────┬───────────────────[ L_CM1/2 ]───────────────────────┬──────────> To Bridge
 │ │
 ┌─┴─┐ ┌─┴─┐
 │CX1│ (0.22µF X2) │CX2│ (0.22µF X2)
 └─┬─┘ └─┬─┘
 │ Net: AC_LINE_CM1 │
 ───────────────┼───────────────┬─────────── ──────┼──────────> To Bridge
 │ ┌─┴─┐ │ │
 │ │CY1│ (2.2nF Y1) │ Net: AC_NEUTRAL_FILT
 │ └─┬─┘ │
 │ │ │
 │ └─── Net: EARTH_GND ────────────┤
 │ ┌─── │
 │ ┌─┴─┐ │
 │ │CY2│ (2.2nF Y1) │
 │ └─┬─┘ │
 │ Net: AC_NEUTRAL_CM1 │
 │ │ │
 ───────────────┴───────────────┴───────────────────────────────┴──────────> To Bridge
 Net: AC_NEUTRAL_PROT
```

## 5. Schematic & PCB Layout Guidelines
1. **Low-Inductive Ground Return**: The ground pin of `C_Y1` and `C_Y2` must return to the chassis earth terminal via a short, wide copper pour (> 2.0 mm width).
2. **Creepage**: Maintain ≥ 6.4 mm creepage distance between the AC line pins of the Y-capacitors and secondary ground planes.
