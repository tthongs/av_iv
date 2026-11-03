# Component Schematic Specification: Y2 (32.768 kHz LSE RTC Crystal)

## 1. Component Metadata
* **Reference Designator**: `Y2`
* **Component Type**: Tuning Fork Low-Speed External Quartz Crystal Resonator
* **Manufacturer**: Abracon LLC
* **Primary MPN**: `ABS07-32.768KHZ-T`
* **Alternate Manufacturer**: Citizen Micro
* **Alternate MPN**: `CM7V-T1A-32.768KHZ` (12.5 pF, 3.2 × 1.5 mm)
* **Package / Footprint**: SMD 2-Pad Ultra-Miniature Ceramic (3.2 × 1.5 mm, Height: 0.9 mm)
* **Subsystem**: Stage 6 (Real-Time Telemetry Loop Timekeeping Engine)

## 2. Electrical Ratings & Constraints
* **Nominal Frequency (f_0)**: 32.768 kHz (Tuning Fork)
* **Frequency Tolerance at 25°C**: ± 20.0 ppm
* **Load Capacitance (C_L)**: 12.5 pF
* **Equivalent Series Resistance (ESR)**: < 70.0 kΩ max (55.0 kΩ typical)
* **Shunt Capacitance (C_0)**: 1.0 pF typical
* **Drive Level**: 0.1 µW typical (0.5 µW max)
* **Load Capacitor Calculation**:
 C_L = (C_3 × C_4 / C_3 + C_4) + C_stray
 With C_stray ≈ 2.5 pF:
 12.5 pF - 2.5 pF = 10.0 pF implies C_3 = C_4 = 20.0 pF
 Selected standard capacitors: 2x 18.0 pF ± 5% 50V C0G 0603 (`Murata GRM1885C1H180JA01D`).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Function | Schematic Net Name | Connected To | Solder / Trace Notes |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`XIN`** | `OSC32_IN` | STM32 Pin 3 (`PC14-OSC32_IN`), Load Cap C_3 (18 pF) | High-Z trace, keep < 5.0 mm. |
| **2** | **`XOUT`**| `OSC32_OUT`| STM32 Pin 4 (`PC15-OSC32_OUT`), Load Cap C_4 (18 pF) | High-Z trace, keep < 5.0 mm. |

## 4. Schematic Symbol Representation
```
 [ Y2: ABRACON 32.768 kHz LSE RTC CRYSTAL ]
 ┌─────────────┐
 Net: OSC32_IN ──────[1] 32.768 [2]────── Net: OSC32_OUT
 │ kHz │
 └─────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Ultra-High Impedance Node Protection**: The 32.768 kHz tuning-fork circuit operates at nanoampere currents. Moisture, flux residue, or adjacent switching tracks will induce frequency drift or stall oscillations. Enclose completely within an analog ground shield guard ring.
