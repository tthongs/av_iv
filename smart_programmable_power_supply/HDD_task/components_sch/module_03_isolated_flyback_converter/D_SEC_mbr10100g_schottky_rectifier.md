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
* **Peak Repetitive Reverse Voltage ($V_{\text{RRM}}$)**: $100.0\,\text{V}_{\text{DC}}$
  * Maximum Reverse Voltage Stress:
    $$V_{\text{R,diode}} = V_{\text{OUT}} + \frac{V_{\text{bulk,max}}}{n} = 24.0\,\text{V} + \frac{374.8\,\text{V}}{6.0} = 24.0\,\text{V} + 62.47\,\text{V} = \mathbf{86.47\,\text{V}_{\text{peak}}}$$
  * Voltage Derating: $\frac{86.47\,\text{V}}{100.0\,\text{V}} = \mathbf{86.47\%}$ ($86.5\%$ derating acceptable for passive Schottky; rated $100\,\text{V}$ withstands secondary ringing).
* **Average Forward Rectified Current ($I_{F(\text{AV})}$)**: $10.0\,\text{A}_{\text{DC}}$
  * Continuous Output Current: $3.0\,\text{A}_{\text{DC}}$
  * Current Derating: $\frac{3.0\,\text{A}}{10.0\,\text{A}} = \mathbf{30.0\%} \le 70\%$ (Massive $70\%$ current safety headroom).
* **Forward Voltage Drop ($V_F$)**: $0.60\,\text{V}$ typical @ $3.0\,\text{A}, 100^\circ\text{C}$
* **Conduction Power Dissipation**:
  $$P_{\text{loss,diode}} = V_F \times I_{\text{OUT}} = (0.60\,\text{V}) \times (3.0\,\text{A}) = \mathbf{1.80\,\text{W}}$$
* **Thermal Analysis**:
  * Heatsink Thermal Resistance: $R_{\theta\text{sa}} = 15.0^\circ\text{C/W}$
  * Junction Temperature Rise @ $50^\circ\text{C}$ ambient:
    $$T_j = T_{\text{amb}} + P_{\text{loss}} \times (R_{\theta\text{jc}} + R_{\theta\text{sa}}) = 50^\circ\text{C} + 1.80\,\text{W} \times (1.5 + 15.0)^\circ\text{C/W} = 50 + 29.7 = \mathbf{79.7^\circ\text{C}}$$
    Safely below the $150^\circ\text{C}$ silicon maximum ($53.1\%$ of rating).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1 / Anode** | **Anode (A)** | `FLY_SEC_ANODE` | Transformer `TX1` Secondary Pin 5 & 6 | Heavy copper pour ($> 3.0\,\text{mm}$ width). |
| **2 / Tab** | **Cathode (K)** | `+24V_UNFILT` | Secondary filter capacitors `C_SEC1`, `C_SEC2` (+), Choke `L_post` Pin 1 | Low-inductance polygon pour on Layer 1. |

## 4. Schematic Symbol Representation
```
     Net: FLY_SEC_ANODE               Net: +24V_UNFILT
    ───────────────────────[►|───]───────────────────────> To C_SEC & L_post
                         D_SEC: MBR10100G
                          (100V, 10A Schottky)
```

## 5. Schematic & PCB Layout Guidelines
1. **RC Snubber**: Place a small secondary snubber ($R_{\text{sec}} = 10.0\,\Omega / 0.5\,\text{W}$, $C_{\text{sec}} = 1.0\,\text{nF} / 100\,\text{V}$) directly across `D_SEC` anode and cathode to damp diode reverse recovery ringing.
2. **Heatsink Clearance**: Heatsink `HS1` tab is electrically tied to Cathode (`+24V_UNFILT`). Ensure $\ge 3.0\,\text{mm}$ clearance to grounded chassis and adjacent components.
