# Component Schematic Specification: U1 (Isolated Flyback PWM Controller)

## 1. Component Metadata
* **Reference Designator**: `U1`
* **Component Type**: High-Efficiency Flyback Controller
* **Primary Selection**: Texas Instruments `UCC28740DR` (Quasi-Resonant Valley Switching, Constant Voltage / Constant Current, Ultra-Low Standby)
* **Alternate Selection**: Texas Instruments `UCC28C43DR` (BiCMOS Current-Mode Controller, Fixed 65 kHz Uniform Clock)
* **Package / Footprint**: SOIC-7 / SOIC-8 Narrow Body (3.9 × 4.9 mm)
* **Subsystem**: Stage 3 (Isolated Flyback Subsystem)

## 2. Electrical Ratings & Constraints
* **Supply Voltage (V_CC)**: Up to 35.0 V_DC (Operating range: 9.0 V - 28.0 V)
 * Startup Threshold: V_CC,start = 14.5 V (UCC28740) / 8.4 V (UCC28C43)
 * UVLO Stop Threshold: V_CC,stop = 9.0 V (UCC28740) / 7.6 V (UCC28C43)
* **Operating Quiescent Current (I_q)**: < 35 µA in standby burst mode (Delivers < 30 mW idle power)
* **Gate Drive Output Current**: Peak +1.0 A source / -1.0 A sink totem-pole driver
* **Current Sense Clamp Threshold**: V_CS(max) = 1.00 V_DC internal comparator threshold
* **Switching Frequency**: Programmed to 65.0 kHz ± 5% nominal operating frequency

## 3. Schematic Pin Connections & Net Mapping (UCC28740 / UCC28C43)
| Pin # | Pin Name | Schematic Net Name | Connected To | Functional Description & External Passives |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `COMP` / `FB` | `FLY_COMP` | Optocoupler `OPTO1` Collector (Pin 4), Compensation Cap `C_comp` (10 nF) | Feedback control voltage node. Optical feedback pulls COMP low to reduce duty cycle. |
| **2** | `VS` / `VFB` | `FLY_VS` | Auxiliary winding resistor divider (R_VS1 = 100 kΩ, R_VS2 = 20 kΩ) | Voltage sensing / demagnetization detection for valley switching and OVP. |
| **3** | `CS` / `ISENSE`| `FLY_CS` | Current sense shunt `R_CS` through 1 kΩ series resistor and 470 pF filter | Senses primary MOSFET peak current for cycle-by-cycle pulse truncation. |
| **4** | `GND` | `PGND_HOT` | Primary hot power ground plane | Controller quiet signal ground reference. |
| **5** | `DRV` / `OUT` | `FLY_GATE` | Primary CoolMOS `Q1` Gate via 10.0 Ω series damping resistor and 1N4148 turn-off diode | Direct totem-pole gate drive output for switching `Q1`. |
| **6** | `VDD` / `VCC` | `FLY_VCC` | Auxiliary bias diode `D_AUX` (UF4004), 47 µF / 35 V cap, and 1.5 MΩ startup string | Operating power supply pin. Startup trickle bleed followed by aux winding bias. |
| **7** | `HV` / `N/C` | `+HV_BULK` (HV) | High-voltage bulk DC link link via 1.5 MΩ startup resistor | Internal high-voltage startup current source (UCC28740) or external bleed string. |

## 4. Schematic Symbol Representation
```
 [ U1: UCC28740 / UCC28C43 FLYBACK PWM CONTROLLER ]
 ┌─────────────────┐
 Net: FLY_COMP ─────────[1] COMP HV [7]─── Net: +HV_BULK (via 1.5MΩ startup)
 │ │
 Net: FLY_VS ─────────[2] VS VDD [6]─── Net: FLY_VCC (from Aux Winding)
 │ │
 Net: FLY_CS ─────────[3] CS DRV [5]─── Net: FLY_GATE ──[ 10Ω ]──> To Q1 Gate
 │ │
 Net: PGND_HOT ─────────[4] GND N/C [8]
 └─────────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Decoupling**: Solder a 1.0 µF / 50 V X7R ceramic bypass capacitor directly between Pin 6 (`VDD`) and Pin 4 (`GND`) with trace length < 2.0 mm.
2. **Current Sense Filtering**: Place the 1 kΩ / 470 pF RC low-pass filter directly adjacent to Pin 3 (`CS`) to reject leading-edge gate charge recovery spikes.
