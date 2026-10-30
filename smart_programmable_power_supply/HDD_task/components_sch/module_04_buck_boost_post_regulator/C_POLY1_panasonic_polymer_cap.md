# Component Schematic Specification: C_POLY1 (Solid Aluminum Polymer Capacitor)

## 1. Component Metadata
* **Reference Designator**: `C_POLY1`
* **Component Type**: OS-CON™ Solid Aluminum Polymer Capacitor
* **Manufacturer**: Panasonic Industrial Devices
* **Primary MPN**: `25SVPF100M`
* **Alternate Manufacturer**: KEMET
* **Alternate MPN**: `A750KK107M1EAAE015` (100 µF, 25 V, 15 mΩ ESR)
* **Package / Footprint**: Radial Can SMD Size F8 ($8.0\,\text{mm}$ Diameter $\times 10.0\,\text{mm}$ Height)
* **Subsystem**: Stage 4 (Dynamic Transient Step-Load Reservoir)

## 2. Electrical Ratings & Constraints
* **Nominal Capacitance**: $100.0\,\mu\text{F} \pm 20\%$ at $120\,\text{Hz}$ (Solid polymer: zero DC bias voltage degradation!)
* **Rated Working Voltage ($V_{\text{rated}}$)**: $25.0\,\text{V}_{\text{DC}}$
  * Maximum continuous rail: $20.0\,\text{V}_{\text{DC}}$
  * Voltage Derating: $\frac{20.0\,\text{V}}{25.0\,\text{V}} = \mathbf{80.0\%}$
  * Surge Voltage Rating: $28.8\,\text{V}_{\text{DC}}$ ($1000$ cycles).
* **Equivalent Series Resistance (ESR)**: $12.0\,\text{m}\Omega$ maximum across $100\,\text{kHz}$ to $300\,\text{kHz}$
* **Maximum Rated Ripple Current**: $3.20\,\text{A}_{\text{RMS}}$ at $105^\circ\text{C}$, $100\,\text{kHz}$
* **Operating Temperature Range**: $-55^\circ\text{C}$ to $+105^\circ\text{C}$ with $> 5000\,\text{hours}$ endurance.
* **Dynamic Step-Load Response ($10\% \to 90\%$ step, $0.3\,\text{A} \to 2.7\,\text{A}$ at $1.0\,\text{A}/\mu\text{s}$)**:
  * Inductor response lag: $t_{\text{recov}} \approx 25\,\mu\text{s}$ (based on $25\,\text{kHz}$ loop bandwidth).
  * Output voltage transient dip:
    $$\Delta V_{\text{OUT,trans}} = \frac{\Delta I_{\text{step}} \times t_{\text{recov}}}{C_{\text{OUT,tot}}} + \Delta I_{\text{step}} \times \text{ESR}_{\text{poly}} = \frac{(2.4\,\text{A})(25\,\mu\text{s})}{138\,\mu\text{F}} + (2.4\,\text{A})(12\,\text{m}\Omega) = 43.5\,\text{mV} + 28.8\,\text{mV} = \mathbf{72.3\,\text{mV}}$$
  * Transient droop is strictly $< 100\,\text{mV}$ ($0.36\%$ on $20\,\text{V}$ rail, $1.45\%$ on $5\,\text{V}$ rail), recovering fully within $50\,\mu\text{s}$.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`+` (Anode)** | `+V_OUT` | `R_shunt` Exit Pad, Output Binding Post `J2` (+), Divider `R_top` | Heavy copper polygon ($w \ge 4.0\,\text{mm}$, 2oz Cu). |
| **2** | **`-` (Cathode)**| `GND_SELV` | Output Binding Post `J3` (-), Secondary Ground Plane | Direct connection to secondary SELV ground plane. |

## 4. Schematic Symbol Representation
```
               [ C_POLY1: PANASONIC 25SVPF100M 100µF / 25V POLYMER ]
                                  ┌─────────────┐
        Net: +V_OUT    ───────────┤+  100 µF    │
                                  │   25V 12mΩ  │
        Net: GND_SELV  ───────────┤-  OS-CON    │
                                  └─────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Placement**: Locate `C_POLY1` immediately downstream of `R_shunt` and right before the output binding post solder lugs.
2. **Thermal Clearance**: Keep the polymer capacitor body at least $10.0\,\text{mm}$ away from switching MOSFETs and power inductor `L1` to prevent radiated heat from raising the ambient temperature around the polymer seal.
