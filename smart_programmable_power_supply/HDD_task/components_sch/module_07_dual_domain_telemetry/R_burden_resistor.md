# Component Schematic Specification: R_burden (Precision CT Burden & DC Bias Network)

## 1. Component Metadata
* **Reference Designators**: `R_burden` (Burden), `R_bias1`, `R_bias2` (Midpoint Divider), `C_bias` (Decoupling)
* **Values & Part Numbers**:
  * `R_burden`: $100.0\,\Omega \pm 0.1\%$, 0.25 W, TCR $\pm 25\,\text{ppm}/^\circ\text{C}$, 0805 SMD (Vishay Dale `TNPW0805100RBEEA`)
  * `R_bias1, R_bias2`: $2x\ 10.0\,\text{k}\Omega \pm 0.1\%$, 0.125 W, 0805 SMD (Vishay Dale `TNPW080510K0BEEA`)
  * `C_bias`: $1.0\,\mu\text{F} \pm 10\%$, 16 V, X7R, 0603 SMD (Murata `GRM188R71C105KA12D`)
* **Subsystem**: Stage 7 (Primary AC Mains Isolated Current Telemetry)

## 2. Electrical Ratings & Constraints
* **Secondary Voltage Generation**:
  At maximum input current ($1.604\,\text{A}_{\text{RMS}}$):
  $$V_{\text{burden,RMS}} = I_{\text{sec}} \times R_{\text{burden}} = (1.604 \times 10^{-3}\,\text{A}) \times 100.0\,\Omega = \mathbf{160.4\,\text{mV}_{\text{RMS}}}$$
  $$V_{\text{burden,peak}} = 160.4\,\text{mV} \times \sqrt{2} = \mathbf{226.8\,\text{mV}_{\text{peak}}}$$
* **DC Midpoint Bias Formulation**:
  Dividing the clean $+3.300\,\text{V}_{\text{DC}}$ analog supply with two matched $10.0\,\text{k}\Omega \pm 0.1\%$ resistors:
  $$V_{\text{bias}} = (+3.300\,\text{V}) \times \frac{10.0\,\text{k}\Omega}{10.0\,\text{k}\Omega + 10.0\,\text{k}\Omega} = \mathbf{1.650\,\text{V}_{\text{DC}}}$$
* **Net Signal Sensed at STM32 ADC Input (`PC1`)**:
  $$V_{\text{ADC,IN}} = 1.650\,\text{V}_{\text{DC}} \pm 226.8\,\text{mV} \implies \mathbf{1.423\,\text{V}} \le V_{\text{ADC,IN}} \le \mathbf{1.877\,\text{V}}$$
  * Centered directly in the $0.0\,\text{V}$ to $+3.30\,\text{V}$ dynamic span of STM32 ADC1 with $> 1.4\,\text{V}$ headroom margin to both rails, completely eliminating clipping.

## 3. Schematic Pin Connections & Net Mapping
| Component | Pin 1 Net | Pin 2 Net | Description & Connection |
| :---: | :--- | :--- | :--- |
| **`R_burden`** | `CT_SEC_HI` | `VREF_1V65_BIAS` | Direct Kelvin connection across CT secondary terminals. |
| **`R_bias1`** | `+3V3_SEC` | `VREF_1V65_BIAS` | Top leg of midpoint voltage divider. |
| **`R_bias2`** | `VREF_1V65_BIAS` | `AGND_SEC` | Bottom leg of midpoint voltage divider. |
| **`C_bias`** | `VREF_1V65_BIAS` | `AGND_SEC` | Low-impedance AC ground bypass capacitor ($1.0\,\mu\text{F}$). |

## 4. Schematic Symbol Representation
```
                    [ PRECISION BURDEN & DC MIDPOINT BIAS NETWORK ]
                                 Net: +3V3_SEC
                                       │
                                     ┌─┴─┐
                                     │   │ R_bias1 (10.0 kΩ ±0.1%)
                                     └─┬─┘
                                       │
      Net: VREF_1V65_BIAS ─────────────┼───────────────┬───────────────── Pin 2 of CT1
                                       │               │
                                     ┌─┴─┐          ┌──┴──┐
                  R_bias2 (10.0 kΩ)  │   │          │     │ C_bias (1.0 µF X7R)
                                     └─┬─┘          └──┬──┘
                                       │               │
                                 Net: AGND_SEC   Net: AGND_SEC
                                       │
                                       │
   Pin 1 of CT1 ──── Net: CT_SEC_HI ───┴──[ R_burden: 100.0 Ω ±0.1% ]── Net: VREF_1V65_BIAS
                            │
                       [ RC Filter: 1kΩ / 10nF ]
                            │
               Net: CT_ADC_IN ──> STM32 Pin 9 (PC1)
```
