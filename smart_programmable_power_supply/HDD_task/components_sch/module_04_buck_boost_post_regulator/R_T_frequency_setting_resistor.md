# Component Schematic Specification: R_T (LM5176 Frequency Program Resistor)

## 1. Component Metadata
* **Reference Designator**: `R_T`
* **Component Type**: Precision Thick-Film SMD Resistor (1% Tolerance)
* **Manufacturer**: Vishay Dale
* **Primary MPN**: `CRCW060324K9FKEA`
* **Alternate Manufacturer**: Panasonic Electronic Components
* **Alternate MPN**: `ERJ-3EKF2492V` (24.9 kΩ, 1%, 0603)
* **Package / Footprint**: SMD 0603 Metric (1.6 × 0.8 mm)
* **Subsystem**: Stage 4 (LM5176 Timing & Clock Generator)

## 2. Electrical Ratings & Constraints
* **Resistance Value (R)**: 24.9 kΩ ± 1.0%
* **Power Rating (P_rated)**: 0.10 W (100 mW)
* **Programmed Switching Frequency (f_sw)**:
 According to the LM5176 datasheet programming equation:
 f_sw [kHz] = (7450 / R_T [kΩ]) + 1 ≈ (7450 / 24.9) = 299.2 kHz ≈ 300.0 kHz
* **Frequency Accuracy**: ± 5.0% across -40°C to +125°C operating range.
* **Pin Voltage**: V_RT ≈ 1.20 V_DC generated internally by LM5176.
 * Operating current: I_RT = (1.20 V / 24.9 kΩ) = 48.2 µA
 * Power dissipation: P_RT = (48.2 µA)^2 × 24.9 kΩ = 57.8 µW (Practically zero dissipation).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :--- | :--- | :--- |
| **1** | `LM5176_RT` | `U3` Pin 8 (`RT`) | Direct trace < 2.0 mm length. |
| **2** | `AGND_SEC` | `U3` Pin 11 (`AGND`) | Direct connection to quiet analog ground. |

## 4. Schematic Symbol Representation
```
 [ R_T: 24.9 kΩ ±1% FREQUENCY PROGRAM ]
 ┌─────────────┐
 Net: LM5176_RT ───────┤1 24.9k 2├─────── Net: AGND_SEC
 └─────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Clock Jitter Suppression**: Place `R_T` directly against Pin 8 of `U3`. Never route noisy clock, switch node, or gate drive signals underneath or adjacent to the `LM5176_RT` trace, as stray capacitive coupling will modulate the PWM oscillator and cause phase jitter.
