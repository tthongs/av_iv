# Component Schematic Specification: D_SEC (Secondary Schottky Barrier Rectifier)

## 1. Component Metadata
* **Reference Designator**: `D_SEC` (Mounted on Heatsink `HS1`, Aavid / Boyd `577002B00000G`)
* **Component Type**: High-Power Schottky Barrier Diode
* **Manufacturer**: ON Semiconductor
* **Primary MPN**: `MBR10100G`
* **Alternate Manufacturer**: STMicroelectronics
* **Alternate MPN**: `STPS10H100D`
* **Package / Footprint**: TO-220-2 Through-Hole Solder Mount
* **Subsystem**: Stage 3 (Isolated Flyback Subsystem)

## 2. Electrical Ratings & Constraints
* **Peak Repetitive Reverse Voltage (V_RRM)**: 100.0 V_DC
 * Maximum Reverse Voltage Stress:
 V_R,diode = V_OUT + (V_bulk,max / n) = 24.0 V + (374.8 V / 6.0) = 24.0 V + 62.47 V = mathbf{86.47 V_peak}
 * Voltage Derating: (86.47 V / 100.0 V) = 86.47% (86.5% derating acceptable for passive Schottky; rated 100 V withstands secondary ringing).
* **Average Forward Rectified Current (I_F(AV)**: 10.0 A_DC
 * Continuous Output Current: 3.0 A_DC
 * Current Derating: (3.0 A / 10.0 A) = 30.0% ≤ 70% (Massive 70% current safety headroom).
* **Forward Voltage Drop (V_F)**: 0.60 V typical @ 3.0 A, 100°C
* **Conduction Power Dissipation**:
 P_loss,diode = V_F × I_OUT = (0.60 V) × (3.0 A) = 1.80 W
* **Thermal Analysis**:
 * Heatsink Thermal Resistance: R_thetasa = 15.0°C/W
 * Junction Temperature Rise @ 50°C ambient:
 T_j = T_amb + P_loss × (R_thetajc + R_thetasa) = 50°C + 1.80 W × (1.5 + 15.0)°C/W = 50 + 29.7 = 79.7°C
 Safely below the 150°C silicon maximum (53.1% of rating).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1 / Anode** | **Anode (A)** | `FLY_SEC_ANODE` | Transformer `TX1` Secondary Pin 5 & 6 | Heavy copper pour (> 3.0 mm width). |
| **2 / Tab** | **Cathode (K)** | `+24V_UNFILT` | Secondary filter capacitors `C_SEC1`, `C_SEC2` (+), Choke `L_post` Pin 1 | Low-inductance polygon pour on Layer 1. |

## 4. Schematic Symbol Representation
```
 Net: FLY_SEC_ANODE Net: +24V_UNFILT
 ───────────────────────[►|───]───────────────────────> To C_SEC & L_post
 D_SEC: MBR10100G
 (100V, 10A Schottky)
```

## 5. Schematic & PCB Layout Guidelines
1. **RC Snubber**: Place a small secondary snubber (R_sec = 10.0 Ω / 0.5 W, C_sec = 1.0 nF / 100 V) directly across `D_SEC` anode and cathode to damp diode reverse recovery ringing.
2. **Heatsink Clearance**: Heatsink `HS1` tab is electrically tied to Cathode (`+24V_UNFILT`). Ensure ≥ 3.0 mm clearance to grounded chassis and adjacent components.
