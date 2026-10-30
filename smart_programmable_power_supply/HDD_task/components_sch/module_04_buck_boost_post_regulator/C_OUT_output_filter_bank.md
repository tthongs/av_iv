# Component Schematic Specification: C_OUT (Ceramic Output Filter Bank)

## 1. Component Metadata
* **Reference Designator**: `C_OUT1`, `C_OUT2`, `C_OUT3`, `C_OUT4` (4-Capacitor Ceramic Bank)
* **Component Type**: High-Capacitance Low-ESR Multilayer Ceramic Capacitor (MLCC)
* **Manufacturer**: Murata Electronics
* **Primary MPN**: `GRM32ER71E226KE15L`
* **Alternate Manufacturer**: TDK Corporation
* **Alternate MPN**: `C3225X7R1E226M250AC` (22 µF, 25 V, X7R, 1210)
* **Package / Footprint**: SMD 1210 Metric ($3.2 \times 2.5\,\text{mm}$, Height: $2.5\,\text{mm}$)
* **Subsystem**: Stage 4 (Output Switching Ripple Suppression Bank)

## 2. Electrical Ratings & Constraints
* **Nominal Capacitance**: $22.0\,\mu\text{F}$ per capacitor (Total bank capacitance: $4 \times 22.0\,\mu\text{F} = \mathbf{88.0\,\mu\text{F}}$)
* **Voltage Rating ($V_{\text{rated}}$)**: $25.0\,\text{V}_{\text{DC}}$
  * Maximum continuous output voltage: $20.0\,\text{V}_{\text{DC}}$
  * Operating Voltage Stress: $\frac{20.0\,\text{V}}{25.0\,\text{V}} = \mathbf{80.0\%}$ at 20V maximum rail.
* **DC Bias Derating Effect**:
  * At $V_{\text{OUT}} = 20.0\,\text{V}_{\text{DC}}$, effective capacitance is $\approx 9.5\,\mu\text{F}$ per MLCC.
  * Effective Ceramic Bank Capacitance at 20V: $C_{\text{eff,cer}} = 4 \times 9.5\,\mu\text{F} \approx \mathbf{38.0\,\mu\text{F}}$.
  * Combined with $100\,\mu\text{F}$ polymer capacitor `C_POLY1`, total effective output capacitance is $C_{\text{OUT,tot}} = 138.0\,\mu\text{F}$.
* **Equivalent Series Resistance (ESR)**: $2.5\,\text{m}\Omega$ per MLCC at $300\,\text{kHz}$.
  * Net ceramic bank ESR: $\text{ESR}_{\text{cer}} = \frac{2.5\,\text{m}\Omega}{4} \approx \mathbf{0.63\,\text{m}\Omega}$.
* **Ripple Current Capability ($I_{\text{ripple}}$)**: $4.5\,\text{A}_{\text{RMS}}$ per capacitor at $300\,\text{kHz}$ ($18.0\,\text{A}_{\text{RMS}}$ net bank rating).
  * Worst-case output ripple current: $I_{\text{ripple,out}} = 1.15\,\text{A}_{\text{RMS}}$.
  * Ripple Current Derating: $\frac{1.15\,\text{A}}{18.0\,\text{A}} = \mathbf{6.39\%}$ (Immense safety margin).
* **Output Switching Voltage Ripple**:
  $$\Delta V_{\text{OUT,pk-pk}} \approx \Delta I_L \times \left( \text{ESR}_{\text{net}} + \frac{1}{8 \times f_{\text{sw}} \times C_{\text{OUT,tot}}} \right) = 2.0\,\text{A} \times (0.59\,\text{m}\Omega + 3.68\,\text{m}\Omega) = \mathbf{8.54\,\text{mV}_{\text{pk-pk}}}$$
  * This strictly satisfies the PRD limit ($\le 25.0\,\text{mV}_{\text{pk-pk}}$) with nearly 3x margin!

## 3. Schematic Pin Connections & Net Mapping
| Ref Des | Pin 1 (Positive) Net | Pin 2 (Negative) Net | Solder Connection |
| :---: | :--- | :--- | :--- |
| **`C_OUT1`** | `+V_OUT_PRE` | `PGND_SEC` | Direct low-inductance connection across Boost FET `QD` Drain & `PGND`. |
| **`C_OUT2`** | `+V_OUT_PRE` | `PGND_SEC` | Direct low-inductance connection across Boost FET `QD` Drain & `PGND`. |
| **`C_OUT3`** | `+V_OUT_PRE` | `PGND_SEC` | Direct low-inductance connection across Boost FET `QD` Drain & `PGND`. |
| **`C_OUT4`** | `+V_OUT_PRE` | `PGND_SEC` | Direct low-inductance connection across Boost FET `QD` Drain & `PGND`. |

## 4. Schematic Symbol Representation
```
               [ C_OUT: 4x 22µF / 25V X7R 1210 CERAMIC BANK ]
      Net: +V_OUT_PRE ──┬──────────┬──────────┬──────────┬──────
                        │          │          │          │
                     ┌──┴──┐    ┌──┴──┐    ┌──┴──┐    ┌──┴──┐
                     │     │    │     │    │     │    │     │
                     └──┬──┘    └──┬──┘    └──┬──┘    └──┬──┘
                        │          │          │          │
      Net: PGND_SEC   ──┴──────────┴──────────┴──────────┴──────
```

## 5. Schematic & PCB Layout Guidelines
1. **Direct Placement at Boost FET**: Place `C_OUT1` through `C_OUT4` as close as physically possible to the Drain of `QD` and the Source of `QC`. The circulating loop length from `QD` Drain $\to$ `C_OUT` $\to$ `QC` Source must be $< 6.0\,\text{mm}$.
2. **Via Placement**: Each capacitor pad should have at least two $0.3\,\text{mm}$ vias placed immediately adjacent to the SMD pad edges connecting directly to Layer 2 ground and power planes.
