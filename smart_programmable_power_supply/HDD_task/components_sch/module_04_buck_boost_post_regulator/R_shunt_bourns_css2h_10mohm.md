# Component Schematic Specification: R_shunt (Precision Output Current Sense Shunt)

## 1. Component Metadata
* **Reference Designator**: `R_shunt`
* **Component Type**: High-Precision Metal Element Current Sense Resistor
* **Manufacturer**: Bourns Inc.
* **Primary MPN**: `CSS2H-2512R-L010F`
* **Alternate Manufacturer**: Vishay Dale
* **Alternate MPN**: `WSLP2512R0100FEA` (10 mΩ, 3 W, 0.1%, 2512)
* **Package / Footprint**: SMD 2512 (2-Terminal Heavy Copper End Caps with Dedicated Internal Kelvin Taps)
* **Subsystem**: Stage 4 (Current Sense & Protection Interface)

## 2. Electrical Ratings & Constraints
* **Resistance Value ($R$)**: $10.0\,\text{m}\Omega$ ($0.010\,\Omega$)
* **Resistance Tolerance**: $\pm 0.1\%$ Precision Grade
* **Power Rating ($P_{\text{rated}}$)**: $3.0\,\text{W}$ at $70^\circ\text{C}$ ($2.0\,\text{W}$ at $100^\circ\text{C}$)
  * Full-load continuous current: $I_{\text{OUT}} = 3.0\,\text{A}_{\text{DC}}$
  * Conduction power dissipation:
    $$P_{\text{loss,shunt}} = I_{\text{OUT}}^2 \times R_{\text{shunt}} = (3.0\,\text{A})^2 \times 0.010\,\Omega = \mathbf{0.090\,\text{W}} \quad (90.0\,\text{mW})$$
  * Power Derating:
    $$\frac{0.090\,\text{W}}{3.0\,\text{W}} = \mathbf{3.0\%} \quad (\text{VVDN requires } \le 60\%)$$
  * Peak transient overload ($4.2\,\text{A}$): $P_{\text{peak}} = (4.2\,\text{A})^2 \times 0.010\,\Omega = 0.176\,\text{W}$ ($5.87\%$ of rating).
* **Temperature Coefficient of Resistance (TCR)**: $< \pm 50\,\text{ppm}/^\circ\text{C}$
  * Total thermal drift across full $\Delta T = 60^\circ\text{C}$ span is $< 0.3\%$, guaranteeing high measurement accuracy.
* **Inductance ($L_{\text{parasitic}}$)**: $< 2.0\,\text{nH}$ (ultra-low parasitic inductance prevents phase distortion in current sense amplifiers).

## 3. Schematic Pin Connections & 4-Wire Kelvin Net Mapping
| Pin # | Pad Function | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1 (Main)** | **Current Entry (Power)** | `+V_OUT_PRE` | Drain of Boost FET `QD`, Ceramic Bank `C_OUT` | Heavy copper polygon ($w \ge 4.0\,\text{mm}$, 2oz Cu). |
| **2 (Main)** | **Current Exit (Power)**  | `+V_OUT` | Polymer Cap `C_POLY1`, Output Post `J2` (+), Voltage Divider `R_top` | Heavy copper polygon ($w \ge 4.0\,\text{mm}$, 2oz Cu). |
| **1K (Kelvin)**| **Kelvin Positive Sense**| `SHUNT_SENSE_P` | `U3` CSP (Pin 14), `U7` INA240 IN+ (Pin 1), `U6` INA226 IN+ (Pin 1) | Dedicated $0.25\,\text{mm}$ Kelvin sense trace. |
| **2K (Kelvin)**| **Kelvin Negative Sense**| `SHUNT_SENSE_N` | `U3` CSN (Pin 13), `U7` INA240 IN- (Pin 8), `U6` INA226 IN- (Pin 10) | Dedicated $0.25\,\text{mm}$ Kelvin sense trace. |

## 4. Schematic Symbol Representation
```
                    [ R_shunt: BOURNS CSS2H-2512 10mΩ ±0.1% 3W ]
                             ┌───────────────────┐
     Net: +V_OUT_PRE  ───────┤1 (Pwr)     2 (Pwr)├─────── Net: +V_OUT
                             │   [ 10.0 mΩ ]     │
   Net: SHUNT_SENSE_P ───────┤1K (Klv)   2K (Klv)├─────── Net: SHUNT_SENSE_N
                             └───────────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **True 4-Wire Kelvin Sensing**: Never tap the `SHUNT_SENSE_P` and `SHUNT_SENSE_N` signal nets from the main high-current polygon pours. Tap them exclusively from the designated inner Kelvin lands or from the inside center edge of the SMD solder pads where zero load current flows.
2. **Differential Routing**: Route `SHUNT_SENSE_P` and `SHUNT_SENSE_N` as an ultra-tight, length-matched differential pair ($w = 0.25\,\text{mm}$, $s = 0.25\,\text{mm}$) shielded on Layer 2 by a solid ground reference plane. Keep this pair away from `SW1` and `SW2`.
3. **Thermal Symmetry**: Ensure balanced copper pad geometries on both terminal pads to prevent thermal gradient-induced thermocouple EMF offsets across the metal resistive element ($V_{\text{EMF}} < 1\,\mu\text{V}$).
