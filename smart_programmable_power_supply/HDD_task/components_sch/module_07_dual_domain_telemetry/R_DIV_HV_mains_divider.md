# Component Schematic Specification: R_DIV_HV (High-Voltage AC Mains Divider)

## 1. Component Metadata
* **Reference Designators**: `R_HV1`, `R_HV2`, `R_HV3` (High-Side String), `R_HV_BOT` (Precision Bottom Resistor)
* **Component Type**: High-Voltage Precision Thick/Thin Film SMD Resistors
* **Values & Part Numbers**:
  * `R_HV1..3`: $3x\ 500.0\,\text{k}\Omega \pm 1\%$, 0.25 W, 200 V rating, 1206 SMD (Vishay Dale `CRCW1206500KFKEA`)
    * Total high-side resistance: $R_{\text{HV_top}} = 3 \times 500\,\text{k}\Omega = \mathbf{1.500\,\text{M}\Omega}$.
  * `R_HV_BOT`: $7.50\,\text{k}\Omega \pm 0.1\%$, 0.125 W, TCR $\pm 25\,\text{ppm}/^\circ\text{C}$, 0805 SMD (Vishay Dale `TNPW08057K50BEEA`)
* **Subsystem**: Stage 7 (Primary AC Mains Isolated Voltage Telemetry)

## 2. Electrical Ratings & Constraints
* **Total Resistance**: $R_{\text{tot}} = 1500\,\text{k}\Omega + 7.50\,\text{k}\Omega = \mathbf{1507.5\,\text{k}\Omega}$.
* **Voltage Division Ratio ($k_{\text{div}}$)**:
  $$k_{\text{div}} = \frac{R_{\text{HV_BOT}}}{R_{\text{HV_top}} + R_{\text{HV_BOT}}} = \frac{7.50\,\text{k}\Omega}{1507.5\,\text{k}\Omega} = \frac{1}{201.0} \approx \mathbf{0.0049751}$$
* **Maximum Peak Voltage Sensed ($265\,\text{V}_{\text{AC RMS}}$)**:
  $$V_{\text{bulk,peak}} = 265\,\text{V} \times \sqrt{2} = 374.8\,\text{V}_{\text{peak}}$$
  $$V_{\text{sense,peak}} = 374.8\,\text{V} \times 0.0049751 = \mathbf{1.8647\,\text{V}_{\text{peak}}}$$
  * Perfectly matches the linear input envelope of the `AMC1311` ($0.0\,\text{V}$ to $2.000\,\text{V}$), preserving a $6.8\%$ linear headroom margin.
* **Power Dissipation**:
  * Maximum continuous power at $265\,\text{V}_{\text{RMS}}$ ($375\,\text{V}_{\text{DC}}$ equivalent):
    $$P_{\text{loss,div}} = \frac{(374.8\,\text{V})^2}{1.5075 \times 10^6\,\Omega} = \mathbf{0.093\,\text{W}} \quad (93.2\,\text{mW})$$
  * Dissipation per 1206 high-side resistor:
    $$P_{\text{R_HV}} = \frac{93.2\,\text{mW}}{3} = \mathbf{31.1\,\text{mW}} \quad (\text{Rating: } 250\,\text{mW} \implies \text{Derating } 12.4\% \ll 60\%)$$
* **High-Voltage Creepage Across Divider**:
  * Slicing the high-side resistance across three 1206 packages distributes voltage stress to $\le 125\,\text{V}$ per package (well below the $200\,\text{V}$ rating).
  * Combined pad-to-pad creepage across the three resistors exceeds $7.2\,\text{mm}$.

## 3. Schematic Pin Connections & Net Mapping
| Resistor | Pin 1 Net | Pin 2 Net | Footprint | Trace Requirements |
| :---: | :--- | :--- | :---: | :--- |
| **`R_HV1`** | `+HV_BULK` | `HV_DIV_TAP1` | 1206 SMD | High-voltage trace, $\ge 3.0\,\text{mm}$ clearance to ground. |
| **`R_HV2`** | `HV_DIV_TAP1` | `HV_DIV_TAP2` | 1206 SMD | Series bridge resistor. |
| **`R_HV3`** | `HV_DIV_TAP2` | `MAINS_DIV_SENSE` | 1206 SMD | Connects to `AMC1311` INP (Pin 2). |
| **`R_HV_BOT`**| `MAINS_DIV_SENSE`| `PGND_HOT` | 0805 SMD | Precision bottom leg; connects to primary hot ground. |

## 4. Schematic Symbol Representation
```
                    [ HIGH-VOLTAGE AC MAINS DIVIDER STRING ]
                                Net: +HV_BULK
                                     │
                                   ┌─┴─┐
                                   │   │ R_HV1 (500 kΩ / 1206)
                                   └─┬─┘
                                     │
                                   ┌─┴─┐
                                   │   │ R_HV2 (500 kΩ / 1206)
                                   └─┬─┘
                                     │
                                   ┌─┴─┐
                                   │   │ R_HV3 (500 kΩ / 1206)
                                   └─┬─┘
                                     │
   Net: MAINS_DIV_SENSE ─────────────┼────────── U4 AMC1311 INP (Pin 2)
                                     │
                                   ┌─┴─┐
                                   │   │ R_HV_BOT (7.50 kΩ ±0.1% / 0805)
                                   └─┬─┘
                                     │
                               Net: PGND_HOT
```
