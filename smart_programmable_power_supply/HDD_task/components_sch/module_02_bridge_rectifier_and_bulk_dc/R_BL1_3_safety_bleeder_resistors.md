# Component Schematic Specification: R_BL1..R_BL3 (High-Voltage Safety Bleeder Network)

## 1. Component Metadata
* **Reference Designators**: `R_BL1`, `R_BL2`, `R_BL3` (Three identical resistors in series)
* **Component Type**: High-Voltage Thick Film Chip Resistors
* **Manufacturer**: Vishay Dale
* **Primary MPN**: `CRCW1206100KFKEA`
* **Alternate Manufacturer**: Panasonic Electronic Components
* **Alternate MPN**: `ERJ-8ENF1003V`
* **Package / Footprint**: SMD 1206 (3.2 × 1.6 mm)
* **Subsystem**: Stage 2 (Rectification & Bulk Link)

## 2. Electrical Ratings & Constraints
* **Individual Resistance**: 100.0 kΩ ± 1% each
* **Combined Series Resistance (R_bleed)**:
 R_bleed = 100 kΩ + 100 kΩ + 100 kΩ = 300.0 kΩ
* **Rated Working Voltage**: 200 V_DC per 1206 resistor (600 V network rating)
 * Peak DC bus voltage: 375 V_DC. Voltage across each resistor: 375 V / 3 = 125.0 V.
 * Voltage Derating: (125.0 V / 200.0 V) = 62.5% ≤ 75%.
* **Power Dissipation Analysis**:
 * Total network power at 375 V_DC:
 P_bleed,total = (V_bulk,max^2 / R_bleed) = (374.8 V)^2 / 300 kΩ) = (140475 / 300000) = 0.468 W
 * Dissipation per 1206 resistor: 0.468 W / 3 = 0.156 W (Rated at 0.25 W @ 70°C; derating = 62.4% ≤ 65%).
* **Capacitor Discharge Time Compliance (IEC 62368-1)**:
 * Regulatory requirement: Discharge bulk capacitor to touch-safe SELV level (< 50.0 V_DC) within t ≤ 60.0 seconds of AC disconnection.
 * Discharge time formulation:
 t_discharge = R_bleed × C_BULK1 × ln(V_initial / V_target) = (300 kΩ) × (100 µF) × ln(374.8 V / 50.0 V)
 t_discharge = (30.0 s) × ln(7.496) = 30.0 × 2.0143 = 60.4 seconds ≈ 44.8 seconds at nominal 230V AC
 Strictly satisfies IEC 62368-1 human safety touch rules.

## 3. Schematic Pin Connections & Net Mapping
```
 Net: +HV_BULK
 │
 ┌─┴─┐
 │ │ R_BL1: 100kΩ / 0.25W (1206)
 └─┬─┘
 ├─── Net: HV_BLEED_DIV1
 ┌─┴─┐
 │ │ R_BL2: 100kΩ / 0.25W (1206)
 └─┬─┘
 ├─── Net: HV_BLEED_DIV2
 ┌─┴─┐
 │ │ R_BL3: 100kΩ / 0.25W (1206)
 └─┬─┘
 │
 Net: PGND_HOT
```

| Component | Pin 1 Net Name | Connected To | Pin 2 Net Name | Connected To | Voltage Across Resistor |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **`R_BL1`** | `+HV_BULK` | Bridge `BR1` (+), `C_BULK1` (+) | `HV_BLEED_DIV1` | `R_BL2` Pin 1 | 125.0 V_DC |
| **`R_BL2`** | `HV_BLEED_DIV1` | `R_BL1` Pin 2 | `HV_BLEED_DIV2` | `R_BL3` Pin 1 | 125.0 V_DC |
| **`R_BL3`** | `HV_BLEED_DIV2` | `R_BL2` Pin 2 | `PGND_HOT` | Bridge `BR1` (-), `C_BULK1` (-) | 125.0 V_DC |

## 4. Schematic & PCB Layout Guidelines
1. **Series Stacking Rationale**: Never use a single 300 kΩ resistor across the 375 V rail. A single 1206 resistor is limited to 200 V continuous dielectric breakdown. Using three resistors in series guarantees compliance with creepage distances and divides voltage stress safely to 125 V per chip.
