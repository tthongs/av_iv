# Component Schematic Specification: NTC1 (Inrush Current Limiter)

## 1. Component Metadata
* **Reference Designator**: `NTC1`
* **Component Type**: Negative Temperature Coefficient (NTC) Power Thermistor
* **Manufacturer**: TDK / EPCOS
* **Primary MPN**: `B57236S0150M000`
* **Alternate Manufacturer**: Amphenol Ametherm
* **Alternate MPN**: `SL15 15003`
* **Package / Footprint**: Radial Disc (Body diameter: 13.0 mm, Lead spacing: 7.5 mm)
* **Subsystem**: Stage 1 (Mains AC Input & Protection)

## 2. Electrical Ratings & Constraints
* **Cold Resistance (R_25)**: 15.0 Ω ± 20%
* **Maximum Continuous Current**: 2.90 A_ RMS (Derating margin: 1.604 A / 2.90 A = 55.3% ≤ 70%)
* **Maximum Cold-Start Inrush Current**: I_ pk = (265 V imes √(2) / 15.0 Ω = mathbf{24.98 A_ peak} (Guaranteed < 25.0 A)
* **Hot Steady-State Resistance (R_ hot)**: approx 0.48 Ω @ 100°C
* **Full-Load Power Dissipation**: P = (0.55 A)^2 imes 0.48 Ω = 0.145 W (Negligible loss)

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Thermal Requirements |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Input Lead | `AC_NEUTRAL_IN` | `J1` Terminal N | 2.5 mm width on Layer 1 (2oz Cu). |
| **2** | Output Lead | `AC_NEUTRAL_PROT`| `MOV1` (Terminal 2), `C_X1` (Terminal 2), `L_CM1` (Pin 2) | 2.5 mm width on Layer 1 (2oz Cu). |

## 4. Schematic Symbol Representation
```
 Net: AC_NEUTRAL_IN Net: AC_NEUTRAL_PROT
 ──────────────────────[ NTC1: 15.0Ω ]───────────────────────> To MOV1, CX1, LCM1
 B57236S0150M
```

## 5. Schematic & PCB Layout Guidelines
1. **Thermal Separation**: NTC thermistors operate hot (approx 80°C - 110°C under full load). Maintain at least 10.0 mm physical spacing from temperature-sensitive electrolytic capacitors (`C_BULK1`).
2. **Elevated Mounting**: In through-hole assembly, mount `NTC1` with 3 mm - 5 mm standoff height above the PCB to promote airflow and prevent localized board scorching.
