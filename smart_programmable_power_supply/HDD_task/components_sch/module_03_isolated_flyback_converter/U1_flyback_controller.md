# Component Schematic Specification: U1 (Isolated Flyback PWM Controller)

## 1. Component Metadata
* **Reference Designator**: `U1`
* **Component Type**: High-Efficiency Flyback Controller
* **Primary Selection**: Texas Instruments `UCC28740DR` (Quasi-Resonant Valley Switching, Constant Voltage / Constant Current, Ultra-Low Standby)
* **Alternate Selection**: Texas Instruments `UCC28C43DR` (BiCMOS Current-Mode Controller, Fixed 65 kHz Uniform Clock)
* **Package / Footprint**: SOIC-7 / SOIC-8 Narrow Body ($3.9 \times 4.9\,\text{mm}$)
* **Subsystem**: Stage 3 (Isolated Flyback Subsystem)

## 2. Electrical Ratings & Constraints
* **Supply Voltage ($V_{\text{CC}}$)**: Up to $35.0\,\text{V}_{\text{DC}}$ (Operating range: $9.0\,\text{V} - 28.0\,\text{V}$)
  * Startup Threshold: $V_{\text{CC,start}} = 14.5\,\text{V}$ (UCC28740) / $8.4\,\text{V}$ (UCC28C43)
  * UVLO Stop Threshold: $V_{\text{CC,stop}} = 9.0\,\text{V}$ (UCC28740) / $7.6\,\text{V}$ (UCC28C43)
* **Operating Quiescent Current ($I_q$)**: $< 35\,\mu\text{A}$ in standby burst mode (Delivers $< 30\,\text{mW}$ idle power)
* **Gate Drive Output Current**: Peak $+1.0\,\text{A}$ source / $-1.0\,\text{A}$ sink totem-pole driver
* **Current Sense Clamp Threshold**: $V_{\text{CS(max)}} = 1.00\,\text{V}_{\text{DC}}$ internal comparator threshold
* **Switching Frequency**: Programmed to $65.0\,\text{kHz} \pm 5\%$ nominal operating frequency

## 3. Schematic Pin Connections & Net Mapping (UCC28740 / UCC28C43)
| Pin # | Pin Name | Schematic Net Name | Connected To | Functional Description & External Passives |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `COMP` / `FB` | `FLY_COMP` | Optocoupler `OPTO1` Collector (Pin 4), Compensation Cap `C_comp` ($10\,\text{nF}$) | Feedback control voltage node. Optical feedback pulls COMP low to reduce duty cycle. |
| **2** | `VS` / `VFB` | `FLY_VS` | Auxiliary winding resistor divider ($R_{\text{VS1}} = 100\,\text{k}\Omega$, $R_{\text{VS2}} = 20\,\text{k}\Omega$) | Voltage sensing / demagnetization detection for valley switching and OVP. |
| **3** | `CS` / `ISENSE`| `FLY_CS` | Current sense shunt `R_CS` through $1\,\text{k}\Omega$ series resistor and $470\,\text{pF}$ filter | Senses primary MOSFET peak current for cycle-by-cycle pulse truncation. |
| **4** | `GND` | `PGND_HOT` | Primary hot power ground plane | Controller quiet signal ground reference. |
| **5** | `DRV` / `OUT` | `FLY_GATE` | Primary CoolMOS `Q1` Gate via $10.0\,\Omega$ series damping resistor and 1N4148 turn-off diode | Direct totem-pole gate drive output for switching `Q1`. |
| **6** | `VDD` / `VCC` | `FLY_VCC` | Auxiliary bias diode `D_AUX` (UF4004), $47\,\mu\text{F} / 35\,\text{V}$ cap, and $1.5\,\text{M}\Omega$ startup string | Operating power supply pin. Startup trickle bleed followed by aux winding bias. |
| **7** | `HV` / `N/C` | `+HV_BULK` (HV) | High-voltage bulk DC link link via $1.5\,\text{M}\Omega$ startup resistor | Internal high-voltage startup current source (UCC28740) or external bleed string. |

## 4. Schematic Symbol Representation
```
               [ U1: UCC28740 / UCC28C43 FLYBACK PWM CONTROLLER ]
                             ┌─────────────────┐
     Net: FLY_COMP ─────────[1] COMP       HV [7]─── Net: +HV_BULK (via 1.5MΩ startup)
                             │                 │
       Net: FLY_VS ─────────[2] VS        VDD [6]─── Net: FLY_VCC (from Aux Winding)
                             │                 │
       Net: FLY_CS ─────────[3] CS        DRV [5]─── Net: FLY_GATE ──[ 10Ω ]──> To Q1 Gate
                             │                 │
     Net: PGND_HOT ─────────[4] GND       N/C [8]
                             └─────────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Decoupling**: Solder a $1.0\,\mu\text{F} / 50\,\text{V}$ X7R ceramic bypass capacitor directly between Pin 6 (`VDD`) and Pin 4 (`GND`) with trace length $< 2.0\,\text{mm}$.
2. **Current Sense Filtering**: Place the $1\,\text{k}\Omega / 470\,\text{pF}$ RC low-pass filter directly adjacent to Pin 3 (`CS`) to reject leading-edge gate charge recovery spikes.
