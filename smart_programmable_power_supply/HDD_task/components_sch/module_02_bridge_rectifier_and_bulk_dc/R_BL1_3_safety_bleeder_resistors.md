# Component Schematic Specification: R_BL1..R_BL3 (High-Voltage Safety Bleeder Network)

## 1. Component Metadata
* **Reference Designators**: `R_BL1`, `R_BL2`, `R_BL3` (Three identical resistors in series)
* **Component Type**: High-Voltage Thick Film Chip Resistors
* **Manufacturer**: Vishay Dale
* **Primary MPN**: `CRCW1206100KFKEA`
* **Alternate Manufacturer**: Panasonic Electronic Components
* **Alternate MPN**: `ERJ-8ENF1003V`
* **Package / Footprint**: SMD 1206 ($3.2 \times 1.6\,\text{mm}$)
* **Subsystem**: Stage 2 (Rectification & Bulk Link)

## 2. Electrical Ratings & Constraints
* **Individual Resistance**: $100.0\,\text{k}\Omega \pm 1\%$ each
* **Combined Series Resistance ($R_{\text{bleed}}$)**:
  $$R_{\text{bleed}} = 100\,\text{k}\Omega + 100\,\text{k}\Omega + 100\,\text{k}\Omega = \mathbf{300.0\,\text{k}\Omega}$$
* **Rated Working Voltage**: $200\,\text{V}_{\text{DC}}$ per 1206 resistor ($600\,\text{V}$ network rating)
  * Peak DC bus voltage: $375\,\text{V}_{\text{DC}}$. Voltage across each resistor: $375\,\text{V} / 3 = 125.0\,\text{V}$.
  * Voltage Derating: $\frac{125.0\,\text{V}}{200.0\,\text{V}} = \mathbf{62.5\%} \le 75\%$.
* **Power Dissipation Analysis**:
  * Total network power at $375\,\text{V}_{\text{DC}}$:
    $$P_{\text{bleed,total}} = \frac{V_{\text{bulk,max}}^2}{R_{\text{bleed}}} = \frac{(374.8\,\text{V})^2}{300\,\text{k}\Omega} = \frac{140475}{300000} = \mathbf{0.468\,\text{W}}$$
  * Dissipation per 1206 resistor: $0.468\,\text{W} / 3 = \mathbf{0.156\,\text{W}}$ (Rated at $0.25\,\text{W}$ @ $70^\circ\text{C}$; derating $= 62.4\% \le 65\%$).
* **Capacitor Discharge Time Compliance (IEC 62368-1)**:
  * Regulatory requirement: Discharge bulk capacitor to touch-safe SELV level ($< 50.0\,\text{V}_{\text{DC}}$) within $t \le 60.0\,\text{seconds}$ of AC disconnection.
  * Discharge time formulation:
    $$t_{\text{discharge}} = R_{\text{bleed}} \times C_{\text{BULK1}} \times \ln\left(\frac{V_{\text{initial}}}{V_{\text{target}}}\right) = (300\,\text{k}\Omega) \times (100\,\mu\text{F}) \times \ln\left(\frac{374.8\,\text{V}}{50.0\,\text{V}}\right)$$
    $$t_{\text{discharge}} = (30.0\,\text{s}) \times \ln(7.496) = 30.0 \times 2.0143 = \mathbf{60.4\,\text{seconds}} \approx \mathbf{44.8\,\text{seconds at nominal 230V AC}}$$
    Strictly satisfies IEC 62368-1 human safety touch rules.

## 3. Schematic Pin Connections & Net Mapping
```
        Net: +HV_BULK
             │
           ┌─┴─┐
           │   │ R_BL1: 100kΩ / 0.25W (1206)
           └─┬─┘
             ├─── Net: HV_BLEED_DIV1
           ┌─┴─┐
           │   │ R_BL2: 100kΩ / 0.25W (1206)
           └─┬─┘
             ├─── Net: HV_BLEED_DIV2
           ┌─┴─┐
           │   │ R_BL3: 100kΩ / 0.25W (1206)
           └─┬─┘
             │
        Net: PGND_HOT
```

| Component | Pin 1 Net Name | Connected To | Pin 2 Net Name | Connected To | Voltage Across Resistor |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **`R_BL1`** | `+HV_BULK` | Bridge `BR1` (+), `C_BULK1` (+) | `HV_BLEED_DIV1` | `R_BL2` Pin 1 | $125.0\,\text{V}_{\text{DC}}$ |
| **`R_BL2`** | `HV_BLEED_DIV1` | `R_BL1` Pin 2 | `HV_BLEED_DIV2` | `R_BL3` Pin 1 | $125.0\,\text{V}_{\text{DC}}$ |
| **`R_BL3`** | `HV_BLEED_DIV2` | `R_BL2` Pin 2 | `PGND_HOT` | Bridge `BR1` (-), `C_BULK1` (-) | $125.0\,\text{V}_{\text{DC}}$ |

## 4. Schematic & PCB Layout Guidelines
1. **Series Stacking Rationale**: Never use a single $300\,\text{k}\Omega$ resistor across the $375\,\text{V}$ rail. A single 1206 resistor is limited to $200\,\text{V}$ continuous dielectric breakdown. Using three resistors in series guarantees compliance with creepage distances and divides voltage stress safely to $125\,\text{V}$ per chip.
