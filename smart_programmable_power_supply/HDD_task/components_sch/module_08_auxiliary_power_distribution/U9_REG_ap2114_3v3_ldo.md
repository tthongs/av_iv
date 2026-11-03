# Component Schematic Specification: U9_REG (AP2114H-3.3TRG1 Low-Dropout Regulator)

## 1. Component Metadata
* **Reference Designator**: `U9_REG`
* **Component Type**: CMOS High-Accuracy Low-Dropout Linear Regulator (LDO)
* **Manufacturer**: Diodes Incorporated
* **Primary MPN**: `AP2114H-3.3TRG1`
* **Alternate Manufacturer**: Texas Instruments
* **Alternate MPN**: `TLV1117-33IDCYR` (SOT-223, 800 mA, 3.3 V fixed)
* **Package / Footprint**: SOT-223-3 (Pitch: 2.30 mm, Large Center Thermal Tab)
* **Subsystem**: Stage 8 (Auxiliary Power Tree: +3.3V High-Precision Supervisory Rail)

## 2. Electrical Ratings & Constraints
* **Input Voltage Range (V_IN)**: +3.8 V to +6.0 V_DC (Maximum rating: +6.5 V)
 * Operating input: +5.0 V_DC ± 4% from `U8_REG`.
 * Voltage Stress Derating: (5.0 V / 6.5 V) = 76.9% (Well within transient margins).
* **Nominal Output Voltage (V_OUT)**: +3.300 V_DC ± 1.0% across -40°C to +85°C.
* **Dropout Voltage (V_drop)**: 240 mV typical at 1.0 A (< 50 mV at 65 mA).
 * Headroom: 5.0 V - 3.3 V = 1.70 V >> 0.24 V (Guarantees perfect regulation without dropout!).
* **Maximum Output Current Rating**: 1.0 A_DC continuous.
 * Operating load current:
 * STM32G474RET6 MCU Core: ≈ 42.0 mA
 * INA226 Power Monitor: ≈ 0.33 mA
 * INA240 Current Sense Amp: ≈ 1.80 mA
 * TLV3501 Ultra-Fast Comparator: ≈ 3.20 mA
 * AMC1311 Isolated Amp Low-Side: ≈ 5.50 mA
 * Pull-ups and status logic: ≈ 12.0 mA
 * Total Load Current: I_load,3V3 ≈ 64.83 mA (Peak: 85 mA)
 * Current Derating: (64.83 mA / 1000 mA) = 6.48% << 70% (Massive headroom).
* **Power Dissipation & Thermal Stress**:
 P_loss,U9 = (V_IN - V_OUT) × I_load = (5.0 V - 3.3 V) × (0.065 A) = 0.110 W (110.5 mW)
 * Thermal resistance θ_JA (SOT-223 on PCB with thermal pad): ≈ 65°C/W.
 * Junction temperature rise:
 Δ T_j = 0.1105 W × 65°C/W = 7.18°C
 * At 50°C ambient: T_j = 50 + 7.2 = 57.2°C << 110.0°C (PASS).
* **Power Supply Rejection Ratio (PSRR)**: > 65 dB at 100 kHz, providing ultra-clean, noise-free DC power for sensitive 12-bit ADC and DAC analog reference rails.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`GND`** | `GND_SELV` | Secondary ground plane (Layer 2) | Direct connection to ground plane. |
| **2** | **`OUT`** | `+3V3_SEC` | Ceramic caps C_OUT,3V3 = 2x 4.7 µF / 10 V, MCU, sensors | Low-inductance power polygon (w ≥ 2.0 mm). |
| **3** | **`IN`** | `+5V_SEC` | Ceramic cap C_IN,3V3 = 4.7 µF / 16 V, `U8_REG` OUT | 1.5 mm trace width. |
| **TAB**| **`OUT`**| `+3V3_SEC` | Large copper polygon pour on Layer 1 | Connected internally to Pin 2 (`OUT`). |

## 4. Schematic Symbol Representation
```
 [ U9_REG: AP2114H-3.3TRG1 1.0A LDO REGULATOR ]
 SOT-223 Package
 ┌───────────────┐
 Net: +5V_SEC ─────────[3] IN OUT[2]───────── Net: +3V3_SEC
 │ GND │
 └───────┬───────┘
 [1]
 │
 Net: GND_SELV
```

## 5. Schematic & PCB Layout Guidelines
1. **Stability MLCC**: AP2114 requires low-ESR ceramic output capacitors for stable loop operation. Place two 4.7 µF / 10 V X7R 0805 MLCCs within 2.0 mm of Pin 2 and the GND return.
2. **Tab Solder Pour**: Pin 2 and the large Tab are connected internally to the `OUT` node (`+3V3_SEC`). Flood the tab with a heavy copper polygon pour (8 × 8 mm) to minimize impedance and conduct heat away from the die.
