# Component Schematic Specification: C_OUT (Ceramic Output Filter Bank)

## 1. Component Metadata
* **Reference Designator**: `C_OUT1`, `C_OUT2`, `C_OUT3`, `C_OUT4` (4-Capacitor Ceramic Bank)
* **Component Type**: High-Capacitance Low-ESR Multilayer Ceramic Capacitor (MLCC)
* **Manufacturer**: Murata Electronics
* **Primary MPN**: `GRM32ER71E226KE15L`
* **Alternate Manufacturer**: TDK Corporation
* **Alternate MPN**: `C3225X7R1E226M250AC` (22 µF, 25 V, X7R, 1210)
* **Package / Footprint**: SMD 1210 Metric (3.2 × 2.5 mm, Height: 2.5 mm)
* **Subsystem**: Stage 4 (Output Switching Ripple Suppression Bank)

## 2. Electrical Ratings & Constraints
* **Nominal Capacitance**: 22.0 µF per capacitor (Total bank capacitance: 4 × 22.0 µF = 88.0 µF)
* **Voltage Rating (V_rated)**: 25.0 V_DC
 * Maximum continuous output voltage: 20.0 V_DC
 * Operating Voltage Stress: (20.0 V / 25.0 V) = 80.0% at 20V maximum rail.
* **DC Bias Derating Effect**:
 * At V_OUT = 20.0 V_DC, effective capacitance is ≈ 9.5 µF per MLCC.
 * Effective Ceramic Bank Capacitance at 20V: C_eff,cer = 4 × 9.5 µF ≈ 38.0 µF.
 * Combined with 100 µF polymer capacitor `C_POLY1`, total effective output capacitance is C_OUT,tot = 138.0 µF.
* **Equivalent Series Resistance (ESR)**: 2.5 mΩ per MLCC at 300 kHz.
 * Net ceramic bank ESR: ESR_cer = (2.5 mΩ / 4) ≈ 0.63 mΩ.
* **Ripple Current Capability (I_ripple)**: 4.5 A_RMS per capacitor at 300 kHz (18.0 A_RMS net bank rating).
 * Worst-case output ripple current: I_ripple,out = 1.15 A_RMS.
 * Ripple Current Derating: (1.15 A / 18.0 A) = 6.39% (Immense safety margin).
* **Output Switching Voltage Ripple**:
 Δ V_OUT,pk-pk ≈ Δ I_L × (ESR_net + (1 / 8 × f_sw × C_OUT,tot) = 2.0 A × (0.59 mΩ + 3.68 mΩ) = mathbf{8.54 mV_pk-pk}
 * This strictly satisfies the PRD limit (≤ 25.0 mV_pk-pk) with nearly 3x margin!

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
 │ │ │ │
 ┌──┴──┐ ┌──┴──┐ ┌──┴──┐ ┌──┴──┐
 │ │ │ │ │ │ │ │
 └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘
 │ │ │ │
 Net: PGND_SEC ──┴──────────┴──────────┴──────────┴──────
```

## 5. Schematic & PCB Layout Guidelines
1. **Direct Placement at Boost FET**: Place `C_OUT1` through `C_OUT4` as close as physically possible to the Drain of `QD` and the Source of `QC`. The circulating loop length from `QD` Drain -> `C_OUT` -> `QC` Source must be < 6.0 mm.
2. **Via Placement**: Each capacitor pad should have at least two 0.3 mm vias placed immediately adjacent to the SMD pad edges connecting directly to Layer 2 ground and power planes.
