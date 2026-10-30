# Component Schematic Specification: R_STEER (Precision DAC Voltage Steering Network)

## 1. Component Metadata
* **Reference Designator**: `R_top`, `R_bot`, `R_DAC` (3-Resistor Precision Voltage Steering Network)
* **Component Type**: High-Precision Thin-Film SMD Resistors (Low TCR, 0.1% Tolerance)
* **Manufacturer**: Vishay Dale
* **Primary MPNs**:
  * `R_top`: `TNPW080549K9BEEA` ($49.9\,\text{k}\Omega \pm 0.1\%$, TCR $\pm 25\,\text{ppm}/^\circ\text{C}$, 0805)
  * `R_bot`: `TNPW08054K48BEEA` ($4.48\,\text{k}\Omega \pm 0.1\%$, TCR $\pm 25\,\text{ppm}/^\circ\text{C}$, 0805)
  * `R_DAC`: `TNPW080511K0BEEA` ($11.0\,\text{k}\Omega \pm 0.1\%$, TCR $\pm 25\,\text{ppm}/^\circ\text{C}$, 0805)
* **Alternate Manufacturer**: Panasonic Electronic Components
* **Alternate MPNs**: `ERA-6AEB4992V` ($49.9\,\text{k}\Omega$), `ERA-6AEB4481V` ($4.48\,\text{k}\Omega$), `ERA-6AEB1102V` ($11.0\,\text{k}\Omega$)
* **Package / Footprint**: SMD 0805 Metric ($2.0 \times 1.25\,\text{mm}$)
* **Subsystem**: Stage 4 (Closed-Loop Output Voltage Command Interface)

## 2. Electrical Ratings & Constraints
* **Power Rating ($P_{\text{rated}}$)**: $0.125\,\text{W}$ ($125\,\text{mW}$) per resistor.
  * Maximum voltage across `R_top`: $20.0\,\text{V} - 0.80\,\text{V} = 19.2\,\text{V}$
  * Dissipation: $P_{\text{loss,Rtop}} = \frac{(19.2\,\text{V})^2}{49.9\,\text{k}\Omega} = \mathbf{7.38\,\text{mW}}$ (Derating: $5.9\% \ll 60\%$).
* **Temperature Coefficient**: $\pm 25\,\text{ppm}/^\circ\text{C}$ (Guarantees output voltage drift $< 1.5\,\text{mV}$ across full $0^\circ\text{C}$ to $50^\circ\text{C}$ ambient range).
* **Transfer Function Derivation**:
  Applying Kirchhoff's Current Law (KCL) at the LM5176 `FB` node ($V_{\text{FB}} = 0.800\,\text{V}$):
  $$\frac{V_{\text{OUT}} - V_{\text{FB}}}{R_{\text{top}}} = \frac{V_{\text{FB}}}{R_{\text{bot}}} + \frac{V_{\text{FB}} - V_{\text{DAC}}}{R_{\text{DAC}}}$$
  $$V_{\text{OUT}} = 20.01\,\text{V} - V_{\text{DAC}} \times \left( \frac{49.9\,\text{k}\Omega}{11.0\,\text{k}\Omega} \right) = 20.01\,\text{V} - 4.5364 \times V_{\text{DAC}}$$
* **Verification at Operating Limits**:
  * **At $V_{\text{DAC}} = 0.000\,\text{V}$ (Baseline Maximum Output)**:
    $$V_{\text{OUT,max}} = \mathbf{20.01\,\text{V}_{\text{DC}}}$$
  * **At $V_{\text{DAC}} = 3.300\,\text{V}$ (Full DAC Injection)**:
    $$V_{\text{OUT,min}} = 20.01\,\text{V} - 3.300 \times (4.5364) = 20.01\,\text{V} - 14.97\,\text{V} = \mathbf{5.04\,\text{V}_{\text{DC}}}$$
* **Monotonic Step Resolution**:
  $$\Delta V_{\text{OUT,step}} = \left( \frac{3.30\,\text{V}}{4096} \right) \times \left( \frac{49.9\,\text{k}\Omega}{11.0\,\text{k}\Omega} \right) = 805.7\,\mu\text{V} \times 4.5364 = \mathbf{3.655\,\text{mV per step}}$$
  * Far exceeds PRD requirement ($\le 10.0\,\text{mV}$).

## 3. Schematic Pin Connections & Net Mapping
| Resistor | Pin 1 Net | Pin 2 Net | Description & Connection |
| :---: | :--- | :--- | :--- |
| **`R_top`** | `+V_OUT` | `LM5176_FB` | Connects from clean output rail to `U3` FB pin. |
| **`R_bot`** | `LM5176_FB` | `AGND_SEC` | Connects from `U3` FB pin to quiet secondary analog ground. |
| **`R_DAC`** | `MCU_DAC1_OUT1`| `LM5176_FB` | Connects from STM32 PA4 (DAC output) to `U3` FB pin. |

## 4. Schematic Symbol Representation
```
                     [ PRECISION VOLTAGE STEERING NETWORK ]
                                Net: +V_OUT
                                     │
                                   ┌─┴─┐
                                   │   │  R_top (49.9 kΩ ±0.1%)
                                   └─┬─┘
                                     │
  Net: MCU_DAC1_OUT1 ──[ R_DAC ]─────┼───── Net: LM5176_FB (Pin 5)
                      (11.0 kΩ)      │
                                   ┌─┴─┐
                                   │   │  R_bot (4.48 kΩ ±0.1%)
                                   └─┬─┘
                                     │
                               Net: AGND_SEC
```

## 5. Schematic & PCB Layout Guidelines
1. **FB Node Minimization**: The node `LM5176_FB` is high impedance ($Z_{\text{node}} \approx 3.1\,\text{k}\Omega$). Place `R_top`, `R_bot`, and `R_DAC` immediately adjacent to Pin 5 of `U3` with copper trace length $< 3.0\,\text{mm}$.
2. **Guard Ring**: Enclose the `LM5176_FB` node with an `AGND_SEC` guard ring on Layer 1 to shield against surface leakage currents and capacitive noise injection from switch nodes.
3. **Filter Capacitor at DAC**: Place a $1.0\,\text{nF}$ C0G ceramic capacitor from `MCU_DAC1_OUT1` to `AGND_SEC` directly at the entry of `R_DAC` to eliminate high-frequency DAC reconstruction glitches.
