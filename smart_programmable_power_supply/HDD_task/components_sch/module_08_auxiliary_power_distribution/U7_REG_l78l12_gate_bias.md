# Component Schematic Specification: U7_REG (L78L12ACUTR +12V Gate Bias Regulator)

## 1. Component Metadata
* **Reference Designator**: `U7_REG`
* **Component Type**: Positive Voltage 3-Terminal Linear Voltage Regulator
* **Manufacturer**: STMicroelectronics
* **Primary MPN**: `L78L12ACUTR`
* **Alternate Manufacturer**: ON Semiconductor
* **Alternate MPN**: `MC78L12ABPRPG` (SOT-89 or TO-92 equivalent)
* **Package / Footprint**: SOT-89-3 (Pitch: 1.50 mm, Exposed Center Tab Ground)
* **Subsystem**: Stage 8 (Auxiliary Power Tree: Gate Driver Bias Rail)

## 2. Electrical Ratings & Constraints
* **Input Voltage Range (V_IN)**: +14.5 V to +35.0 V_DC
 * Operating input: +24.0 V_DC ± 0.8% intermediate bus.
 * Input Voltage Stress Derating: (24.0 V / 35.0 V) = 68.57% ≤ 75%.
* **Nominal Output Voltage (V_OUT)**: +12.0 V_DC ± 4.0% (+11.5 V to +12.5 V)
* **Maximum Output Current (I_OUT,max)**: 100.0 mA
 * Average load current: I_load ≈ 25.0 mA (LM5176 `BIAS` pin gate-drive replenishment + downstream 5V regulator quiescent current).
 * Current Derating: (25.0 mA / 100.0 mA) = 25.0% ≤ 70%.
* **Power Dissipation & Thermal Stress**:
 P_loss,U7 = (V_IN - V_OUT) × I_load = (24.0 V - 12.0 V) × (0.025 A) = 0.300 W (300.0 mW)
 * Thermal resistance on 4-layer PCB with thermal vias under center tab: θ_JA ≈ 80°C/W.
 * Junction temperature rise:
 Δ T_j = P_loss × θ_JA = 0.30 W × 80°C/W = 24.0°C
 * At 50°C worst-case ambient: T_j = 50 + 24 = 74.0°C << 110.0°C (VVDN Derating PASS).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`OUT`** | `+12V_AUX` | Ceramic cap C_OUT,12V = 1.0 µF / 25 V, `U3` BIAS (Pin 22), `U8_REG` IN | 1.0 mm trace width. |
| **2** | **`GND`** | `GND_SELV` | Secondary ground plane (Layer 2) | Direct thermal connection to tab. |
| **3** | **`IN`** | `+24V_SEC` | Ceramic cap C_IN,12V = 1.0 µF / 50 V, Stage 3 24V rail | 1.0 mm trace width. |
| **TAB**| **`GND`**| `GND_SELV` | Array of 4 thermal vias (0.3 mm drill) to Layer 2 ground plane | Thermal dissipation tab. |

## 4. Schematic Symbol Representation
```
 [ U7_REG: L78L12ACUTR +12V LINEAR REGULATOR ]
 SOT-89 Package
 ┌───────────────┐
 Net: +24V_SEC ─────────[3] IN OUT[1]───────── Net: +12V_AUX
 │ GND │
 └───────┬───────┘
 [2] (Tab)
 │
 Net: GND_SELV
```

## 5. Schematic & PCB Layout Guidelines
1. **Decoupling**: Place a 1.0 µF / 50 V X7R MLCC directly between Pin 3 and GND tab, and a 1.0 µF / 25 V X7R MLCC between Pin 1 and GND tab.
2. **Thermal Spreading**: Connect Pin 2 / center tab to an exposed top-layer copper polygon (10 × 10 mm) stitched with 4 thermal vias directly into the internal ground plane.
