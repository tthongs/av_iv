# Component Schematic Specification: U9_REG (AP2114H-3.3TRG1 Low-Dropout Regulator)

## 1. Component Metadata
* **Reference Designator**: `U9_REG`
* **Component Type**: CMOS High-Accuracy Low-Dropout Linear Regulator (LDO)
* **Manufacturer**: Diodes Incorporated
* **Primary MPN**: `AP2114H-3.3TRG1`
* **Alternate Manufacturer**: Texas Instruments
* **Alternate MPN**: `TLV1117-33IDCYR` (SOT-223, 800 mA, 3.3 V fixed)
* **Package / Footprint**: SOT-223-3 (Pitch: 2.30 mm, Large Center Thermal Tab)
* **Subsystem**: Stage 8 (Auxiliary Power Tree: +3.3V High-Precision Supervisory Rail)

## 2. Electrical Ratings & Constraints
* **Input Voltage Range ($V_{\text{IN}}$)**: $+3.8\,\text{V}$ to $+6.0\,\text{V}_{\text{DC}}$ (Maximum rating: $+6.5\,\text{V}$)
  * Operating input: $+5.0\,\text{V}_{\text{DC}} \pm 4\%$ from `U8_REG`.
  * Voltage Stress Derating: $\frac{5.0\,\text{V}}{6.5\,\text{V}} = \mathbf{76.9\%}$ (Well within transient margins).
* **Nominal Output Voltage ($V_{\text{OUT}}$)**: $+3.300\,\text{V}_{\text{DC}} \pm 1.0\%$ across $-40^\circ\text{C}$ to $+85^\circ\text{C}$.
* **Dropout Voltage ($V_{\text{drop}}$)**: $240\,\text{mV}$ typical at $1.0\,\text{A}$ ($< 50\,\text{mV}$ at $65\,\text{mA}$).
  * Headroom: $5.0\,\text{V} - 3.3\,\text{V} = 1.70\,\text{V} \gg 0.24\,\text{V}$ (Guarantees perfect regulation without dropout!).
* **Maximum Output Current Rating**: $1.0\,\text{A}_{\text{DC}}$ continuous.
  * Operating load current:
    * STM32G474RET6 MCU Core: $\approx 42.0\,\text{mA}$
    * INA226 Power Monitor: $\approx 0.33\,\text{mA}$
    * INA240 Current Sense Amp: $\approx 1.80\,\text{mA}$
    * TLV3501 Ultra-Fast Comparator: $\approx 3.20\,\text{mA}$
    * AMC1311 Isolated Amp Low-Side: $\approx 5.50\,\text{mA}$
    * Pull-ups and status logic: $\approx 12.0\,\text{mA}$
    * Total Load Current: $I_{\text{load,3V3}} \approx \mathbf{64.83\,\text{mA}} \quad (\text{Peak: } 85\,\text{mA})$
  * Current Derating: $\frac{64.83\,\text{mA}}{1000\,\text{mA}} = \mathbf{6.48\%} \ll 70\%$ (Massive headroom).
* **Power Dissipation & Thermal Stress**:
  $$P_{\text{loss,U9}} = (V_{\text{IN}} - V_{\text{OUT}}) \times I_{\text{load}} = (5.0\,\text{V} - 3.3\,\text{V}) \times (0.065\,\text{A}) = \mathbf{0.110\,\text{W}} \quad (110.5\,\text{mW})$$
  * Thermal resistance $\theta_{\text{JA}}$ (SOT-223 on PCB with thermal pad): $\approx 65^\circ\text{C/W}$.
  * Junction temperature rise:
    $$\Delta T_j = 0.1105\,\text{W} \times 65^\circ\text{C/W} = \mathbf{7.18^\circ\text{C}}$$
  * At $50^\circ\text{C}$ ambient: $T_j = 50 + 7.2 = \mathbf{57.2^\circ\text{C}} \ll 110.0^\circ\text{C}$ (PASS).
* **Power Supply Rejection Ratio (PSRR)**: $> 65\,\text{dB}$ at $100\,\text{kHz}$, providing ultra-clean, noise-free DC power for sensitive 12-bit ADC and DAC analog reference rails.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`GND`** | `GND_SELV` | Secondary ground plane (Layer 2) | Direct connection to ground plane. |
| **2** | **`OUT`** | `+3V3_SEC` | Ceramic caps $C_{\text{OUT,3V3}} = 2x\ 4.7\,\mu\text{F} / 10\,\text{V}$, MCU, sensors | Low-inductance power polygon ($w \ge 2.0\,\text{mm}$). |
| **3** | **`IN`**  | `+5V_SEC` | Ceramic cap $C_{\text{IN,3V3}} = 4.7\,\mu\text{F} / 16\,\text{V}$, `U8_REG` OUT | $1.5\,\text{mm}$ trace width. |
| **TAB**| **`OUT`**| `+3V3_SEC` | Large copper polygon pour on Layer 1 | Connected internally to Pin 2 (`OUT`). |

## 4. Schematic Symbol Representation
```
                    [ U9_REG: AP2114H-3.3TRG1 1.0A LDO REGULATOR ]
                                  SOT-223 Package
                                  ┌───────────────┐
          Net: +5V_SEC  ─────────[3] IN       OUT[2]───────── Net: +3V3_SEC
                                  │      GND      │
                                  └───────┬───────┘
                                         [1]
                                          │
                                    Net: GND_SELV
```

## 5. Schematic & PCB Layout Guidelines
1. **Stability MLCC**: AP2114 requires low-ESR ceramic output capacitors for stable loop operation. Place two $4.7\,\mu\text{F} / 10\,\text{V}$ X7R 0805 MLCCs within $2.0\,\text{mm}$ of Pin 2 and the GND return.
2. **Tab Solder Pour**: Pin 2 and the large Tab are connected internally to the `OUT` node (`+3V3_SEC`). Flood the tab with a heavy copper polygon pour ($8 \times 8\,\text{mm}$) to minimize impedance and conduct heat away from the die.
