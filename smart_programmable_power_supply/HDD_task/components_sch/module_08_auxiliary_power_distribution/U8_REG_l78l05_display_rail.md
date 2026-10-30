# Component Schematic Specification: U8_REG (L78L05ABUTR +5V Display & Logic Regulator)

## 1. Component Metadata
* **Reference Designator**: `U8_REG`
* **Component Type**: Positive Voltage 3-Terminal Linear Voltage Regulator
* **Manufacturer**: STMicroelectronics
* **Primary MPN**: `L78L05ABUTR`
* **Alternate Manufacturer**: Texas Instruments
* **Alternate MPN**: `LM78L05ACMX/NOPB` (SOIC-8 or SOT-89 equivalent)
* **Package / Footprint**: SOT-89-3 (Pitch: 1.50 mm, Exposed Center Tab Ground)
* **Subsystem**: Stage 8 (Auxiliary Power Tree: +5V Display & Sub-Regulator Intermediate Rail)

## 2. Electrical Ratings & Constraints
* **Input Voltage Range ($V_{\text{IN}}$)**: $+7.0\,\text{V}$ to $+30.0\,\text{V}_{\text{DC}}$
  * Operating input: $+12.0\,\text{V}_{\text{DC}}$ from `U7_REG` output.
  * Input Voltage Stress Derating: $\frac{12.0\,\text{V}}{30.0\,\text{V}} = \mathbf{40.0\%} \le 75\%$.
* **Nominal Output Voltage ($V_{\text{OUT}}$)**: $+5.0\,\text{V}_{\text{DC}} \pm 4.0\%$ ($+4.8\,\text{V}$ to $+5.2\,\text{V}$)
* **Maximum Output Current ($I_{\text{OUT,max}}$)**: $100.0\,\text{mA}$
  * Average load current: $I_{\text{load}} \approx 40.0\,\text{mA}$ ($15\,\text{mA}$ for OLED display logic + $25\,\text{mA}$ feeding the 3.3V LDO).
  * Current Derating: $\frac{40.0\,\text{mA}}{100.0\,\text{mA}} = \mathbf{40.0\%} \le 70\%$.
* **Power Dissipation & Thermal Stress**:
  $$P_{\text{loss,U8}} = (V_{\text{IN}} - V_{\text{OUT}}) \times I_{\text{load}} = (12.0\,\text{V} - 5.0\,\text{V}) \times (0.040\,\text{A}) = \mathbf{0.280\,\text{W}} \quad (280.0\,\text{mW})$$
  * Junction temperature rise ($\theta_{\text{JA}} \approx 80^\circ\text{C/W}$):
    $$\Delta T_j = 0.28\,\text{W} \times 80^\circ\text{C/W} = \mathbf{22.4^\circ\text{C}}$$
  * At $50^\circ\text{C}$ ambient: $T_j = 50 + 22.4 = \mathbf{72.4^\circ\text{C}} \ll 110.0^\circ\text{C}$ (PASS).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`OUT`** | `+5V_SEC` | Ceramic cap $C_{\text{OUT,5V}} = 1.0\,\mu\text{F} / 16\,\text{V}$, OLED Header Pin 1, `U9_REG` IN | $1.0\,\text{mm}$ trace width. |
| **2** | **`GND`** | `GND_SELV` | Secondary ground plane (Layer 2) | Direct thermal connection to tab. |
| **3** | **`IN`**  | `+12V_AUX` | Ceramic cap $C_{\text{IN,5V}} = 1.0\,\mu\text{F} / 25\,\text{V}$, `U7_REG` OUT | $1.0\,\text{mm}$ trace width. |
| **TAB**| **`GND`**| `GND_SELV` | Array of 4 thermal vias ($0.3\,\text{mm}$ drill) to Layer 2 ground plane | Thermal dissipation tab. |

## 4. Schematic Symbol Representation
```
                    [ U8_REG: L78L05ABUTR +5V LINEAR REGULATOR ]
                                   SOT-89 Package
                                  ┌───────────────┐
         Net: +12V_AUX  ─────────[3] IN       OUT[1]───────── Net: +5V_SEC
                                  │      GND      │
                                  └───────┬───────┘
                                         [2] (Tab)
                                          │
                                    Net: GND_SELV
```
