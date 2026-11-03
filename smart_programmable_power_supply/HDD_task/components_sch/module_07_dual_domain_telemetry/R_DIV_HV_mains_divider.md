# Component Schematic Specification: R_DIV_HV (High-Voltage AC Mains Divider)

## 1. Component Metadata
* **Reference Designators**: `R_HV1`, `R_HV2`, `R_HV3` (High-Side String), `R_HV_BOT` (Precision Bottom Resistor)
* **Component Type**: High-Voltage Precision Thick/Thin Film SMD Resistors
* **Values & Part Numbers**:
 * `R_HV1..3`: 3x 500.0 kΩ ± 1%, 0.25 W, 200 V rating, 1206 SMD (Vishay Dale `CRCW1206500KFKEA`)
 * Total high-side resistance: R_HV_top = 3 × 500 kΩ = 1.500 MΩ.
 * `R_HV_BOT`: 7.50 kΩ ± 0.1%, 0.125 W, TCR ± 25 ppm/°C, 0805 SMD (Vishay Dale `TNPW08057K50BEEA`)
* **Subsystem**: Stage 7 (Primary AC Mains Isolated Voltage Telemetry)

## 2. Electrical Ratings & Constraints
* **Total Resistance**: R_tot = 1500 kΩ + 7.50 kΩ = 1507.5 kΩ.
* **Voltage Division Ratio (k_div)**:
 k_div = (R_HV_BOT / R_HV_top + R_HV_BOT) = (7.50 kΩ / 1507.5 kΩ) = (1 / 201.0) ≈ 0.0049751
* **Maximum Peak Voltage Sensed (265 V_AC RMS)**:
 V_bulk,peak = 265 V × √(2) = 374.8 V_peak
 V_sense,peak = 374.8 V × 0.0049751 = mathbf{1.8647 V_peak}
 * Perfectly matches the linear input envelope of the `AMC1311` (0.0 V to 2.000 V), preserving a 6.8% linear headroom margin.
* **Power Dissipation**:
 * Maximum continuous power at 265 V_RMS (375 V_DC equivalent):
 P_loss,div = (374.8 V)^2 / 1.5075 × 10^6 Ω) = 0.093 W (93.2 mW)
 * Dissipation per 1206 high-side resistor:
 P_R_HV = (93.2 mW / 3) = 31.1 mW (Rating: 250 mW implies Derating 12.4% << 60%)
* **High-Voltage Creepage Across Divider**:
 * Slicing the high-side resistance across three 1206 packages distributes voltage stress to ≤ 125 V per package (well below the 200 V rating).
 * Combined pad-to-pad creepage across the three resistors exceeds 7.2 mm.

## 3. Schematic Pin Connections & Net Mapping
| Resistor | Pin 1 Net | Pin 2 Net | Footprint | Trace Requirements |
| :---: | :--- | :--- | :---: | :--- |
| **`R_HV1`** | `+HV_BULK` | `HV_DIV_TAP1` | 1206 SMD | High-voltage trace, ≥ 3.0 mm clearance to ground. |
| **`R_HV2`** | `HV_DIV_TAP1` | `HV_DIV_TAP2` | 1206 SMD | Series bridge resistor. |
| **`R_HV3`** | `HV_DIV_TAP2` | `MAINS_DIV_SENSE` | 1206 SMD | Connects to `AMC1311` INP (Pin 2). |
| **`R_HV_BOT`**| `MAINS_DIV_SENSE`| `PGND_HOT` | 0805 SMD | Precision bottom leg; connects to primary hot ground. |

## 4. Schematic Symbol Representation
```
 [ HIGH-VOLTAGE AC MAINS DIVIDER STRING ]
 Net: +HV_BULK
 │
 ┌─┴─┐
 │ │ R_HV1 (500 kΩ / 1206)
 └─┬─┘
 │
 ┌─┴─┐
 │ │ R_HV2 (500 kΩ / 1206)
 └─┬─┘
 │
 ┌─┴─┐
 │ │ R_HV3 (500 kΩ / 1206)
 └─┬─┘
 │
 Net: MAINS_DIV_SENSE ─────────────┼────────── U4 AMC1311 INP (Pin 2)
 │
 ┌─┴─┐
 │ │ R_HV_BOT (7.50 kΩ ±0.1% / 0805)
 └─┬─┘
 │
 Net: PGND_HOT
```
