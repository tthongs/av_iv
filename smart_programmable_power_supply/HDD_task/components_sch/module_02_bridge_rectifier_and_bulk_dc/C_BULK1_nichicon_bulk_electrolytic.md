# Component Schematic Specification: C_BULK1 (High-Voltage Bulk Electrolytic Capacitor)

## 1. Component Metadata
* **Reference Designator**: `C_BULK1`
* **Component Type**: Long-Life Snap-In Aluminum Electrolytic Capacitor
* **Manufacturer**: Nichicon Corporation
* **Primary MPN**: `LGW2W101MELZ25`
* **Alternate Manufacturer**: Panasonic Electronic Components
* **Alternate MPN**: `EEU-ED2W101`
* **Package / Footprint**: Snap-In Radial Can (Diameter: $22.0\,\text{mm}$, Length: $25.0\,\text{mm}$, Lead Pitch: $10.0\,\text{mm}$)
* **Subsystem**: Stage 2 (Rectification & Bulk Link)

## 2. Electrical Ratings & Constraints
* **Nominal Capacitance**: $100.0\,\mu\text{F} \pm 20\%$ at $120\,\text{Hz}$
* **Rated DC Voltage**: $450\,\text{V}_{\text{DC}}$
  * Maximum DC operating voltage: $V_{\text{bulk,max}} = 265\,\text{V} \times \sqrt{2} = 374.8\,\text{V}_{\text{DC}}$
  * Voltage Derating: $\frac{374.8\,\text{V}}{450\,\text{V}} = \mathbf{83.29\%}$ (Acceptable for passive bulk aluminum electrolytics; rated $450\,\text{V}$ handles grid surge headroom).
* **Operating Temperature**: $-40^\circ\text{C}$ to $+105^\circ\text{C}$ ($3000\,\text{hours}$ endurance @ $105^\circ\text{C}$)
* **Ripple Current Rating**: $0.78\,\text{A}_{\text{RMS}}$ @ $120\,\text{Hz}, 105^\circ\text{C}$ ($1.10\,\text{A}_{\text{RMS}}$ @ $10\,\text{kHz}$)
* **Equivalent Series Resistance (ESR)**: $\approx 0.165\,\Omega$ @ $100\,\text{kHz}, 25^\circ\text{C}$
* **Stored Electrostatic Energy**:
  $$E_{\text{stored}} = \frac{1}{2} C V^2 = \frac{1}{2} (100 \times 10^{-6}) (374.8)^2 = \mathbf{7.02\,\text{Joules}}$$
* **Calculated Holdup Time Duration**:
  * At $230\,\text{V}_{\text{AC}}$ nominal ($V_{\text{bulk}} = 325\,\text{V}$):
    $$t_{\text{holdup}} = \frac{C \times (V_{\text{bulk,nom}}^2 - V_{\text{bulk,min}}^2)}{2 \times P_{\text{in}}} = \frac{(100\,\mu\text{F}) \times (325^2 - 120^2)}{2 \times 81.8\,\text{W}} = \frac{10^{-4} \times (105625 - 14400)}{163.6} = \mathbf{55.86\,\text{ms}}$$
    Exceeds the PRD $> 10.0\,\text{ms}$ requirement by over $5.5\times$!
  * At $85\,\text{V}_{\text{AC}}$ low-line brownout ($V_{\text{bulk}} = 120\,\text{V}$): Sustains continuous regulation for $> 12.5\,\text{ms}$ through single half-cycle grid interruptions.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Terminal Polarity | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`+` (Positive Anode)**| `+HV_BULK` | Bridge `BR1` Pin 1, `C_HF` Pin 1, Bleeder `R_BL1`, Transformer `TX1` Pin 1 | Heavy copper polygon ($> 3.0\,\text{mm}$ width). |
| **2** | **`-` (Negative Cathode)**| `PGND_HOT` | Bridge `BR1` Pin 4, `C_HF` Pin 2, Bleeder `R_BL3`, Primary Shunt `R_CS` | Connects directly to primary power ground plane. |

## 4. Schematic Symbol Representation
```
               Net: +HV_BULK (+120V to +375V DC)
                       │
                     ┌─┴─┐ +
                     │   │   C_BULK1: 100µF / 450V
                     │   │   Nichicon LGW2W101MELZ25
                     └───┘ -
                       │
               Net: PGND_HOT (Primary Hot Ground)
```

## 5. Schematic & PCB Layout Guidelines
1. **Loop Minimization**: Position `C_BULK1` immediately between bridge rectifier `BR1` and Flyback transformer `TX1`. The high-frequency switching loop area between `C_BULK1`, `TX1`, and `Q1` must be strictly $< 4.0\,\text{cm}^2$.
2. **Thermal Clearance**: Aluminum electrolytic capacitors degrade exponentially with heat (electrolyte evaporation). Maintain $\ge 12.0\,\text{mm}$ physical spacing from power resistors (`R_snub`), NTC, and transformer core.
