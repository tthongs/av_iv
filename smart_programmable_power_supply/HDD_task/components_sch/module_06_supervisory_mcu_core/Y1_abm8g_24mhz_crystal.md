# Component Schematic Specification: Y1 (24.000 MHz HSE Master Crystal)

## 1. Component Metadata
* **Reference Designator**: `Y1`
* **Component Type**: High-Frequency Fundamental Quartz Crystal Resonator
* **Manufacturer**: Abracon LLC
* **Primary MPN**: `ABM8G-24.000MHZ-18-D2Y-T`
* **Alternate Manufacturer**: TXC Corporation
* **Alternate MPN**: `7M-24.000MAAJ-T` (24.000 MHz, 18 pF, 3.2 × 2.5 mm)
* **Package / Footprint**: SMD 4-Pad Ceramic Seam Seal (3.2 × 2.5 mm, Height: 0.8 mm)
* **Subsystem**: Stage 6 (Supervisory MCU Core Clocking Engine)

## 2. Electrical Ratings & Constraints
* **Nominal Frequency (f_0)**: 24.000 MHz (Fundamental Mode)
* **Frequency Tolerance at 25°C**: ± 10.0 ppm
* **Frequency Stability over -40°C to +85°C**: ± 20.0 ppm
* **Load Capacitance (C_L)**: 18.0 pF
* **Equivalent Series Resistance (ESR)**: < 40.0 Ω max (25.0 Ω typical)
* **Drive Level**: 10.0 µW typical (100.0 µW max)
* **Load Capacitor Sizing Formulation**:
 C_L = (C_1 × C_2 / C_1 + C_2) + C_stray
 Assuming PCB stray capacitance C_stray ≈ 3.0 pF and symmetric load capacitors C_1 = C_2 = C_ext:
 18.0 pF = (C_ext / 2) + 3.0 pF implies (C_ext / 2) = 15.0 pF implies C_ext = 30.0 pF
 Standard high-stability C0G/NP0 capacitor selection: 2x 27.0 pF ± 5% 50V 0603 SMD (`Murata GRM1885C1H270JA01D`).
* **Series Damping Resistor (R_damp)**:
 A 47.0 Ω ± 1% 0603 resistor is inserted in series with the oscillator output (`OSC_OUT`) to limit crystal drive level below 50 µW and prevent mechanical stress or harmonic overtone spurious oscillations.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Function | Schematic Net Name | Connected To | Solder / Trace Notes |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`XIN` (Crystal Input)** | `OSC_IN` | STM32 Pin 5 (`PF0-OSC_IN`), Load Cap C_1 (27 pF) | 0.25 mm trace, guarded. |
| **2** | **`GND` (Case Ground)** | `GND_SELV` | Secondary ground plane (Layer 2) | Thermal ground via. |
| **3** | **`XOUT` (Crystal Output)**| `OSC_OUT_DAMP` | Damping Resistor `R_damp` (47 Ω), Load Cap C_2 (27 pF) | 0.25 mm trace, guarded. |
| **4** | **`GND` (Case Ground)** | `GND_SELV` | Secondary ground plane (Layer 2) | Thermal ground via. |

## 4. Schematic Symbol Representation
```
 [ Y1: ABRACON 24.000 MHz HSE CRYSTAL ]
 ┌─────────────┐
 Net: OSC_IN ──────[1] XIN GND [4]────── Net: GND_SELV
 Net: GND_SELV ──────[2] GND XOUT [3]────── Net: OSC_OUT_DAMP
 └─────────────┘
 24.000 MHz
 │
 [ 47 Ω ] R_damp
 │
 Net: OSC_OUT (MCU Pin 6)
```

## 5. Schematic & PCB Layout Guidelines
1. **Ultra-Compact Loop**: Place `Y1`, C_1, C_2, and R_damp directly beside Pins 5 and 6 of `U5`. Total trace length must be < 6.0 mm.
2. **Ground Guard Ring**: Surround the entire oscillator tank circuit with a dedicated ground guard trace on Layer 1 tied with vias to the Layer 2 ground plane.
3. **Keepout Under Crystal**: Prohibit any digital signal, PWM line, or power rail routing on any PCB layer directly underneath the crystal resonator.
