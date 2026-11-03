# Component Schematic Specification: LED1..3 (Front-Panel Status Indicators)

## 1. Component Metadata
* **Reference Designators**:
 * `LED1`: Constant Voltage (CV) Active Mode Indicator (Green)
 * `LED2`: Constant Current (CC) Clamped Mode Indicator (Amber)
 * `LED3`: Fault Shutdown / Tripped Indicator (Red)
* **Component Type**: High-Efficiency Surface-Mount Indicating LEDs
* **Manufacturer**: Kingbright
* **Primary MPNs**:
 * `LED1` (Green): `APT2012SGC` (568 nm, 15 mcd, 0805)
 * `LED2` (Amber): `APT2012SEC` (601 nm, 30 mcd, 0805)
 * `LED3` (Red): `APT2012SRC` (640 nm, 50 mcd, 0805)
* **Alternate Manufacturer**: Lite-On Inc.
* **Alternate MPN Series**: `LTST-C170 Series`
* **Package / Footprint**: SMD 0805 Metric (2.0 × 1.25 mm, Height: 0.75 mm)
* **Subsystem**: Stage 9 (Visual Operating State Annunciators)

## 2. Electrical Ratings & Constraints
* **Forward Voltage Drop (V_F)**:
 * Green (`LED1`): V_F = 2.10 V typical at 1.5 mA.
 * Amber (`LED2`): V_F = 2.00 V typical at 1.5 mA.
 * Red (`LED3`): V_F = 1.90 V typical at 1.5 mA.
* **Drive Resistor Sizing**:
 Driven directly by STM32 3.3V CMOS GPIO outputs through dedicated 1.00 kΩ ± 1% current-limiting resistors (`R_LED1`, `R_LED2`, `R_LED3`, 0603 SMD):
 I_F,Green = (3.30 V - 2.10 V / 1000 Ω) = 1.20 mA
 I_F,Amber = (3.30 V - 2.00 V / 1000 Ω) = 1.30 mA
 I_F,Red = (3.30 V - 1.90 V / 1000 Ω) = 1.40 mA
 * At ≈ 1.3 mA, the LEDs provide crisp front-panel visibility without excessive brightness or battery/power overhead, drawing < 4.5 mW per channel.

## 3. Schematic Pin Connections & Net Mapping
| LED Ref Des | Indicator Function | Anode Driven By | Cathode Tied To | Series Limiting Resistor |
| :---: | :--- | :--- | :--- | :---: |
| **`LED1`** | **Green (CV Mode)** | STM32 Pin 2 (`PC13`) | `GND_SELV` | `R_LED1` (1.0 kΩ ± 1%, 0603) |
| **`LED2`** | **Amber (CC Mode)** | STM32 Pin 24 (`PC4`) | `GND_SELV` | `R_LED2` (1.0 kΩ ± 1%, 0603) |
| **`LED3`** | **Red (Fault Mode)** | STM32 Pin 25 (`PC5`) | `GND_SELV` | `R_LED3` (1.0 kΩ ± 1%, 0603) |

## 4. Schematic Symbol Representation
```
 [ FRONT-PANEL STATUS LED INDICATORS ]

 STM32 Pin 2 (PC13) ──[ 1.0 kΩ ]──>|── (LED1: Green CV) ── Net: GND_SELV
 STM32 Pin 24 (PC4) ──[ 1.0 kΩ ]──>|── (LED2: Amber CC) ── Net: GND_SELV
 STM32 Pin 25 (PC5) ──[ 1.0 kΩ ]──>|── (LED3: Red FAULT) ── Net: GND_SELV
```
