# Component Schematic Specification: U8_REG (L78L05ABUTR +5V Display & Logic Regulator)

## 1. Component Metadata
* **Reference Designator**: `U8_REG`
* **Component Type**: Positive Voltage 3-Terminal Linear Voltage Regulator
* **Manufacturer**: STMicroelectronics
* **Primary MPN**: `L78L05ABUTR`
* **Alternate Manufacturer**: Texas Instruments
* **Alternate MPN**: `LM78L05ACMX/NOPB` (SOIC-8 or SOT-89 equivalent)
* **Package / Footprint**: SOT-89-3 (Pitch: 1.50 mm, Exposed Center Tab Ground)
* **Subsystem**: Stage 8 (Auxiliary Power Tree: +5V Display & Sub-Regulator Intermediate Rail)

## 2. Electrical Ratings & Constraints
* **Input Voltage Range (V_IN)**: +7.0 V to +30.0 V_DC
 * Operating input: +12.0 V_DC from `U7_REG` output.
 * Input Voltage Stress Derating: (12.0 V / 30.0 V) = 40.0% ≤ 75%.
* **Nominal Output Voltage (V_OUT)**: +5.0 V_DC ± 4.0% (+4.8 V to +5.2 V)
* **Maximum Output Current (I_OUT,max)**: 100.0 mA
 * Average load current: I_load ≈ 40.0 mA (15 mA for OLED display logic + 25 mA feeding the 3.3V LDO).
 * Current Derating: (40.0 mA / 100.0 mA) = 40.0% ≤ 70%.
* **Power Dissipation & Thermal Stress**:
 P_loss,U8 = (V_IN - V_OUT) × I_load = (12.0 V - 5.0 V) × (0.040 A) = 0.280 W (280.0 mW)
 * Junction temperature rise (θ_JA ≈ 80°C/W):
 Δ T_j = 0.28 W × 80°C/W = 22.4°C
 * At 50°C ambient: T_j = 50 + 22.4 = 72.4°C << 110.0°C (PASS).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`OUT`** | `+5V_SEC` | Ceramic cap C_OUT,5V = 1.0 µF / 16 V, OLED Header Pin 1, `U9_REG` IN | 1.0 mm trace width. |
| **2** | **`GND`** | `GND_SELV` | Secondary ground plane (Layer 2) | Direct thermal connection to tab. |
| **3** | **`IN`** | `+12V_AUX` | Ceramic cap C_IN,5V = 1.0 µF / 25 V, `U7_REG` OUT | 1.0 mm trace width. |
| **TAB**| **`GND`**| `GND_SELV` | Array of 4 thermal vias (0.3 mm drill) to Layer 2 ground plane | Thermal dissipation tab. |

## 4. Schematic Symbol Representation
```
 [ U8_REG: L78L05ABUTR +5V LINEAR REGULATOR ]
 SOT-89 Package
 ┌───────────────┐
 Net: +12V_AUX ─────────[3] IN OUT[1]───────── Net: +5V_SEC
 │ GND │
 └───────┬───────┘
 [2] (Tab)
 │
 Net: GND_SELV
```
