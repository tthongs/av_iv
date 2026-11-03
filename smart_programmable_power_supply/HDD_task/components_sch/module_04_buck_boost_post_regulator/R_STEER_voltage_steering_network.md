# Component Schematic Specification: R_STEER (Precision DAC Voltage Steering Network)

## 1. Component Metadata
* **Reference Designator**: `R_top`, `R_bot`, `R_DAC` (3-Resistor Precision Voltage Steering Network)
* **Component Type**: High-Precision Thin-Film SMD Resistors (Low TCR, 0.1% Tolerance)
* **Manufacturer**: Vishay Dale
* **Primary MPNs**:
 * `R_top`: `TNPW080549K9BEEA` (49.9 kΩ ± 0.1%, TCR ± 25 ppm/°C, 0805)
 * `R_bot`: `TNPW08054K48BEEA` (4.48 kΩ ± 0.1%, TCR ± 25 ppm/°C, 0805)
 * `R_DAC`: `TNPW080511K0BEEA` (11.0 kΩ ± 0.1%, TCR ± 25 ppm/°C, 0805)
* **Alternate Manufacturer**: Panasonic Electronic Components
* **Alternate MPNs**: `ERA-6AEB4992V` (49.9 kΩ), `ERA-6AEB4481V` (4.48 kΩ), `ERA-6AEB1102V` (11.0 kΩ)
* **Package / Footprint**: SMD 0805 Metric (2.0 × 1.25 mm)
* **Subsystem**: Stage 4 (Closed-Loop Output Voltage Command Interface)

## 2. Electrical Ratings & Constraints
* **Power Rating (P_rated)**: 0.125 W (125 mW) per resistor.
 * Maximum voltage across `R_top`: 20.0 V - 0.80 V = 19.2 V
 * Dissipation: P_loss,Rtop = (19.2 V)^2 / 49.9 kΩ) = 7.38 mW (Derating: 5.9% << 60%).
* **Temperature Coefficient**: ± 25 ppm/°C (Guarantees output voltage drift < 1.5 mV across full 0°C to 50°C ambient range).
* **Transfer Function Derivation**:
 Applying Kirchhoff's Current Law (KCL) at the LM5176 `FB` node (V_FB = 0.800 V):
 (V_OUT - V_FB / R_top) = (V_FB / R_bot) + (V_FB - V_DAC / R_DAC)
 V_OUT = 20.01 V - V_DAC × (49.9 kΩ / 11.0 kΩ) = 20.01 V - 4.5364 × V_DAC
* **Verification at Operating Limits**:
 * **At V_DAC = 0.000 V (Baseline Maximum Output)**:
 V_OUT,max = mathbf{20.01 V_DC}
 * **At V_DAC = 3.300 V (Full DAC Injection)**:
 V_OUT,min = 20.01 V - 3.300 × (4.5364) = 20.01 V - 14.97 V = mathbf{5.04 V_DC}
* **Monotonic Step Resolution**:
 Δ V_OUT,step = (3.30 V / 4096) × (49.9 kΩ / 11.0 kΩ) = 805.7 µV × 4.5364 = 3.655 mV per step
 * Far exceeds PRD requirement (≤ 10.0 mV).

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
 │ │ R_top (49.9 kΩ ±0.1%)
 └─┬─┘
 │
 Net: MCU_DAC1_OUT1 ──[ R_DAC ]─────┼───── Net: LM5176_FB (Pin 5)
 (11.0 kΩ) │
 ┌─┴─┐
 │ │ R_bot (4.48 kΩ ±0.1%)
 └─┬─┘
 │
 Net: AGND_SEC
```

## 5. Schematic & PCB Layout Guidelines
1. **FB Node Minimization**: The node `LM5176_FB` is high impedance (Z_node ≈ 3.1 kΩ). Place `R_top`, `R_bot`, and `R_DAC` immediately adjacent to Pin 5 of `U3` with copper trace length < 3.0 mm.
2. **Guard Ring**: Enclose the `LM5176_FB` node with an `AGND_SEC` guard ring on Layer 1 to shield against surface leakage currents and capacitive noise injection from switch nodes.
3. **Filter Capacitor at DAC**: Place a 1.0 nF C0G ceramic capacitor from `MCU_DAC1_OUT1` to `AGND_SEC` directly at the entry of `R_DAC` to eliminate high-frequency DAC reconstruction glitches.
