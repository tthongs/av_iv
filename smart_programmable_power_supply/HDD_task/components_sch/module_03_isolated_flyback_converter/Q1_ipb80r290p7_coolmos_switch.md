# Component Schematic Specification: Q1 (Primary High-Voltage Power MOSFET)

## 1. Component Metadata
* **Reference Designator**: `Q1`
* **Component Type**: Superjunction N-Channel Power MOSFET
* **Manufacturer**: Infineon Technologies AG
* **Primary MPN**: `IPB80R290P7`
* **Alternate Manufacturer**: STMicroelectronics
* **Alternate MPN**: `STP10NK80Z`
* **Package / Footprint**: D2PAK / TO-263-3 (SMD Surface Mount with Heavy Drain Thermal Tab)
* **Subsystem**: Stage 3 (Isolated Flyback Subsystem)

## 2. Electrical Ratings & Constraints
* **Drain-Source Breakdown Voltage (V_DSS)**: 800.0 V_DC
 * Maximum Drain-Source Operating Voltage:
 V_DS,peak = V_bulk,max + V_R + V_spike = 374.8 V + 144.0 V + 80.2 V = mathbf{599.0 V_peak}
 * Voltage Derating: (599.0 V / 800.0 V) = 74.88% ≤ 75.0% (Strictly complies with VVDN guideline).
* **Continuous Drain Current (I_D)**: 17.0 A @ 25°C / 11.0 A @ 100°C
 * Maximum Primary Peak Current: I_pk = 3.03 A_peak (I_RMS = 1.17 A_RMS)
 * Current Derating: (1.17 A / 11.0 A) = 10.6% (Immense safety margin).
* **Static Drain-Source On-Resistance (R_DS(on)**: 0.290 Ω max @ 25°C (0.435 Ω @ 100°C)
* **Total Gate Charge (Q_g)**: 24.0 nC (Fast switching with low gate drive loss)
* **Power Dissipation Budget**:
 * Conduction Loss: P_cond = (1.17 A)^2 × (0.435 Ω) = 0.59 W
 * Capacitive Switching Loss: P_sw ≈ (1 / 2) C_oss V_DS^2 f_sw ≈ 0.26 W
 * Total Dissipation: P_loss,Q1 = 0.59 + 0.26 = 0.85 W

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **Gate (G)** | `FLY_GATE_PIN` | Series gate damping resistor R_g = 10.0 Ω ± 1% (`FLY_GATE`) | Short, direct trace (< 10.0 mm). |
| **2 / Tab** | **Drain (D)** | `FLY_DRAIN` | Transformer `TX1` Primary Pin 2, Snubber Diode `D_snub` Cathode | Large copper polygon pour on Layer 1 (400 mm^2). |
| **3** | **Source (S)** | `FLY_SOURCE` | Primary current sense shunt network `R_CS` (Pins 1) | Kelvin sense tap to controller `CS` pin. |

## 4. Schematic Symbol Representation
```
 Net: FLY_DRAIN (To TX1 Pin 2 & Snubber)
 │
 ┌──┴──┐
 │ D │ Q1: Infineon IPB80R290P7
 Net: FLY_GATE ──[ 10Ω ]──┤G S│ 800V, 17A, 0.29Ω (D2PAK)
 └──┬──┘
 │
 Net: FLY_SOURCE ────> To Current Shunt R_CS
```

## 5. Schematic & PCB Layout Guidelines
1. **Thermal Copper Pour**: Solder the D2PAK drain tab to a dedicated 400 mm^2 copper polygon on Layer 1 with an array of 4 × 4 thermal vias (0.3 mm drill) conducting heat to the Layer 4 bottom copper pour (T_j ≤ 100.4°C @ 50°C ambient).
2. **Gate Ringing Suppression**: Place the 10 Ω gate resistor and anti-parallel Schottky diode (BAT54) directly adjacent to Pin 1 to damp gate parasitic ringing.
