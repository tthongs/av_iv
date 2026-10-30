# Component Schematic Specification: U7_REG (L78L12ACUTR +12V Gate Bias Regulator)

## 1. Component Metadata
* **Reference Designator**: `U7_REG`
* **Component Type**: Positive Voltage 3-Terminal Linear Voltage Regulator
* **Manufacturer**: STMicroelectronics
* **Primary MPN**: `L78L12ACUTR`
* **Alternate Manufacturer**: ON Semiconductor
* **Alternate MPN**: `MC78L12ABPRPG` (SOT-89 or TO-92 equivalent)
* **Package / Footprint**: SOT-89-3 (Pitch: 1.50 mm, Exposed Center Tab Ground)
* **Subsystem**: Stage 8 (Auxiliary Power Tree: Gate Driver Bias Rail)

## 2. Electrical Ratings & Constraints
* **Input Voltage Range ($V_{\text{IN}}$)**: $+14.5\,\text{V}$ to $+35.0\,\text{V}_{\text{DC}}$
  * Operating input: $+24.0\,\text{V}_{\text{DC}} \pm 0.8\%$ intermediate bus.
  * Input Voltage Stress Derating: $\frac{24.0\,\text{V}}{35.0\,\text{V}} = \mathbf{68.57\%} \le 75\%$.
* **Nominal Output Voltage ($V_{\text{OUT}}$)**: $+12.0\,\text{V}_{\text{DC}} \pm 4.0\%$ ($+11.5\,\text{V}$ to $+12.5\,\text{V}$)
* **Maximum Output Current ($I_{\text{OUT,max}}$)**: $100.0\,\text{mA}$
  * Average load current: $I_{\text{load}} \approx 25.0\,\text{mA}$ (LM5176 `BIAS` pin gate-drive replenishment + downstream 5V regulator quiescent current).
  * Current Derating: $\frac{25.0\,\text{mA}}{100.0\,\text{mA}} = \mathbf{25.0\%} \le 70\%$.
* **Power Dissipation & Thermal Stress**:
  $$P_{\text{loss,U7}} = (V_{\text{IN}} - V_{\text{OUT}}) \times I_{\text{load}} = (24.0\,\text{V} - 12.0\,\text{V}) \times (0.025\,\text{A}) = \mathbf{0.300\,\text{W}} \quad (300.0\,\text{mW})$$
  * Thermal resistance on 4-layer PCB with thermal vias under center tab: $\theta_{\text{JA}} \approx 80^\circ\text{C/W}$.
  * Junction temperature rise:
    $$\Delta T_j = P_{\text{loss}} \times \theta_{\text{JA}} = 0.30\,\text{W} \times 80^\circ\text{C/W} = \mathbf{24.0^\circ\text{C}}$$
  * At $50^\circ\text{C}$ worst-case ambient: $T_j = 50 + 24 = \mathbf{74.0^\circ\text{C}} \ll 110.0^\circ\text{C}$ (VVDN Derating PASS).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`OUT`** | `+12V_AUX` | Ceramic cap $C_{\text{OUT,12V}} = 1.0\,\mu\text{F} / 25\,\text{V}$, `U3` BIAS (Pin 22), `U8_REG` IN | $1.0\,\text{mm}$ trace width. |
| **2** | **`GND`** | `GND_SELV` | Secondary ground plane (Layer 2) | Direct thermal connection to tab. |
| **3** | **`IN`**  | `+24V_SEC` | Ceramic cap $C_{\text{IN,12V}} = 1.0\,\mu\text{F} / 50\,\text{V}$, Stage 3 24V rail | $1.0\,\text{mm}$ trace width. |
| **TAB**| **`GND`**| `GND_SELV` | Array of 4 thermal vias ($0.3\,\text{mm}$ drill) to Layer 2 ground plane | Thermal dissipation tab. |

## 4. Schematic Symbol Representation
```
                    [ U7_REG: L78L12ACUTR +12V LINEAR REGULATOR ]
                                   SOT-89 Package
                                  ┌───────────────┐
         Net: +24V_SEC  ─────────[3] IN       OUT[1]───────── Net: +12V_AUX
                                  │      GND      │
                                  └───────┬───────┘
                                         [2] (Tab)
                                          │
                                    Net: GND_SELV
```

## 5. Schematic & PCB Layout Guidelines
1. **Decoupling**: Place a $1.0\,\mu\text{F} / 50\,\text{V}$ X7R MLCC directly between Pin 3 and GND tab, and a $1.0\,\mu\text{F} / 25\,\text{V}$ X7R MLCC between Pin 1 and GND tab.
2. **Thermal Spreading**: Connect Pin 2 / center tab to an exposed top-layer copper polygon ($10 \times 10\,\text{mm}$) stitched with 4 thermal vias directly into the internal ground plane.
