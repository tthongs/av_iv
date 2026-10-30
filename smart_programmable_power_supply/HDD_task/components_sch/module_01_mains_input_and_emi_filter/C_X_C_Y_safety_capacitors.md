# Component Schematic Specification: C_X1, C_X2 & C_Y1, C_Y2 (Safety Capacitors)

## 1. Component Metadata
* **Reference Designators**:
  * `C_X1`, `C_X2`: Class X2 Across-The-Line Metallized Polypropylene Film Capacitors
  * `C_Y1`, `C_Y2`: Class Y1 Line-To-Earth Double Reinforced Ceramic Capacitors
* **Manufacturers**: KEMET (`R46` Series for X2, `PHE850` Series for Y1) / Murata (`DE1E3KX222M`)
* **Primary MPNs**:
  * `C_X1, C_X2`: `R46KI32200001M` ($0.22\,\mu	ext{F} \pm 20\%$, $310\,	ext{V}_{	ext{AC RMS}}$, Pitch $15.0\,	ext{mm}$)
  * `C_Y1, C_Y2`: `PHE850ED6220MD15R06L2` ($2.2\,	ext{nF} \pm 20\%$, $400\,	ext{V}_{	ext{AC RMS}}$, Pitch $10.0\,	ext{mm}$)
* **Subsystem**: Stage 1 (Mains AC Input & EMI Filter)

## 2. Electrical Ratings & Safety Limits
* **Class X2 Capacitors**:
  * Rated AC Voltage: $310\,	ext{V}_{	ext{AC RMS}}$ (Continuous line-to-line operation)
  * Self-healing metallized polypropylene dielectric.
  * Role: Attenuates differential-mode switching noise.
* **Class Y1 Capacitors**:
  * Rated AC Voltage: $400\,	ext{V}_{	ext{AC RMS}}$ (Reinforced line-to-earth insulation)
  * Proof withstand voltage: $> 4000\,	ext{V}_{	ext{AC}}$ for $60\,	ext{seconds}$.
  * Earth Leakage Current Calculation:
    $$I_{	ext{leak}} = 2\pi 	imes f 	imes V_{	ext{IN,max}} 	imes (C_{	ext{Y1}} + C_{	ext{Y2}}) = 2\pi 	imes 50\,	ext{Hz} 	imes 265\,	ext{V} 	imes 4.4\,	ext{nF} = \mathbf{0.366\,	ext{mA}}$$
    Strictly complies with the IEC 62368-1 allowable touch-current limit of $< 0.75\,	ext{mA}$.

## 3. Schematic Pin Connections & Net Mapping
| Ref Des | Pin 1 Net Name | Connected To | Pin 2 Net Name | Connected To | Safety Role |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **`C_X1`** | `AC_LINE_FUSED` | Fuse `F1`, `MOV1`, `L_CM1` Pin 1 | `AC_NEUTRAL_PROT` | `NTC1`, `MOV1`, `L_CM1` Pin 4 | Pre-filter differential noise bypass. |
| **`C_X2`** | `AC_LINE_FILT` | `L_CM2` Pin 2, Bridge `BR1` Pin 2 | `AC_NEUTRAL_FILT` | `L_CM2` Pin 3, Bridge `BR1` Pin 3 | Post-filter differential noise bypass. |
| **`C_Y1`** | `AC_LINE_CM1` | Node between `L_CM1` & `L_CM2` | `EARTH_GND` | Chassis Earth Stud / Earth Pin of J1 | Line-to-Earth common mode noise drain. |
| **`C_Y2`** | `AC_NEUTRAL_CM1`| Node between `L_CM1` & `L_CM2` | `EARTH_GND` | Chassis Earth Stud / Earth Pin of J1 | Neutral-to-Earth common mode noise drain. |

## 4. Schematic Symbol Representation
```
     Net: AC_LINE_FUSED                                           Net: AC_LINE_FILT
    ───────────────┬───────────────────[ L_CM1/2 ]───────────────────────┬──────────> To Bridge
                   │                                                     │
                 ┌─┴─┐                                                 ┌─┴─┐
                 │CX1│ (0.22µF X2)                                     │CX2│ (0.22µF X2)
                 └─┬─┘                                                 └─┬─┘
                   │             Net: AC_LINE_CM1                        │
    ───────────────┼───────────────┬───────────                    ──────┼──────────> To Bridge
                   │             ┌─┴─┐                             │     │
                   │             │CY1│ (2.2nF Y1)                  │   Net: AC_NEUTRAL_FILT
                   │             └─┬─┘                             │
                   │               │                               │
                   │               └─── Net: EARTH_GND ────────────┤
                   │               ┌───                            │
                   │             ┌─┴─┐                             │
                   │             │CY2│ (2.2nF Y1)                  │
                   │             └─┬─┘                             │
                   │             Net: AC_NEUTRAL_CM1               │
                   │               │                               │
    ───────────────┴───────────────┴───────────────────────────────┴──────────> To Bridge
     Net: AC_NEUTRAL_PROT
```

## 5. Schematic & PCB Layout Guidelines
1. **Low-Inductive Ground Return**: The ground pin of `C_Y1` and `C_Y2` must return to the chassis earth terminal via a short, wide copper pour ($> 2.0\,	ext{mm}$ width).
2. **Creepage**: Maintain $\ge 6.4\,	ext{mm}$ creepage distance between the AC line pins of the Y-capacitors and secondary ground planes.
