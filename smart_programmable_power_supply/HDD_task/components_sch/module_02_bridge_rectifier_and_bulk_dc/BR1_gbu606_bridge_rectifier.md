# Component Schematic Specification: BR1 (Single-Phase Bridge Rectifier)

## 1. Component Metadata
* **Reference Designator**: `BR1`
* **Component Type**: Glass Passivated Single-Phase Bridge Rectifier
* **Manufacturer**: Diodes Incorporated
* **Primary MPN**: `GBU606`
* **Alternate Manufacturer**: Vishay Semiconductors
* **Alternate MPN**: `GBU6J` (or `GBU8K`)
* **Package / Footprint**: GBU-4 Through-Hole (In-line 4-pin, Pitch: 5.08 mm)
* **Subsystem**: Stage 2 (Rectification & Bulk Link)

## 2. Electrical Ratings & Constraints
* **Peak Repetitive Reverse Voltage ($V_{\text{RRM}}$)**: $600\,\text{V}_{\text{DC}}$
  * Worst-case peak AC line: $V_{\text{peak}} = 265\,\text{V}_{\text{RMS}} \times \sqrt{2} = 374.8\,\text{V}_{\text{peak}}$
  * Voltage Derating: $\frac{374.8\,\text{V}}{600\,\text{V}} = \mathbf{62.46\%}$ (Strictly complies with VVDN $\le 75\%$ reliability limit).
* **Average Forward Rectified Current ($I_{F(\text{AV})}$)**: $6.0\,\text{A}$ (with heatsink) / $3.8\,\text{A}$ (free air)
  * Maximum operating continuous RMS current: $1.604\,\text{A}_{\text{RMS}}$ at $85\,\text{V}_{\text{AC}}$
  * Current Derating: $\frac{1.604\,\text{A}}{6.0\,\text{A}} = \mathbf{26.7\%}$ (Massive safety headroom).
* **Forward Voltage Drop ($V_F$)**: $1.0\,\text{V}$ per diode at $3.0\,\text{A}$ ($0.95\,\text{V}$ typical)
* **Peak Forward Surge Current ($I_{\text{FSM}}$)**: $175.0\,\text{A}$ ($8.3\,\text{ms}$ single half-sine wave)
  * Peak inrush surge ($24.98\,\text{A}$) is only $14.3\%$ of $I_{\text{FSM}}$ capacity!
* **Conduction Power Dissipation**:
  $$P_{\text{loss,BR}} = 2 \times V_F \times I_{\text{avg}} = 2 \times (0.95\,\text{V}) \times (0.85\,\text{A}) = \mathbf{1.62\,\text{W}}$$

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`+` (Positive DC)** | `+HV_BULK` | `C_BULK1` (+), `C_HF` (Pin 1), `R_BL1` (Pin 1), `TX1` Primary (Pin 1) | High-voltage polygon pour ($w \ge 3.0\,\text{mm}$, 2oz Cu). |
| **2** | **`~` (AC Input 1)** | `AC_LINE_FILT` | `L_CM2` Pin 2, `C_X2` Pin 1 | $2.5\,\text{mm}$ trace width (2oz Cu). |
| **3** | **`~` (AC Input 2)** | `AC_NEUTRAL_FILT`| `L_CM2` Pin 3, `C_X2` Pin 2 | $2.5\,\text{mm}$ trace width (2oz Cu). |
| **4** | **`-` (Negative DC)** | `PGND_HOT` | `C_BULK1` (-), `C_HF` (Pin 2), `R_BL3` (Pin 2), Primary Sense `R_CS` | Solid primary ground plane return (`PGND_HOT`). |

## 4. Schematic Symbol Representation
```
                     [ BR1: GBU606 BRIDGE RECTIFIER ]
                             ┌───────────────┐
      Net: AC_LINE_FILT  ───[2] ~          + [1]─── Net: +HV_BULK (+120V to +375V DC)
                             │               │
   Net: AC_NEUTRAL_FILT  ───[3] ~          - [4]─── Net: PGND_HOT (Primary Hot Ground)
                             └───────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **High-Voltage Creepage**: Maintain $\ge 3.0\,\text{mm}$ copper clearance between `+HV_BULK` and `PGND_HOT` on outer PCB layers.
2. **Thermal Spreading**: Pin 1 and Pin 4 should connect to heavy copper polygon pours on Layer 1 with thermal vias to Layer 4 to dissipate $1.62\,\text{W}$ without requiring an external bolt-on heatsink ($T_j \approx 85.6^\circ\text{C}$ at $50^\circ\text{C}$ ambient).
