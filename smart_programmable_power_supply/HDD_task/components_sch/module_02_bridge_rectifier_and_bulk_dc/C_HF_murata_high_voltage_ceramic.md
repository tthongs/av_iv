# Component Schematic Specification: C_HF (High-Voltage Decoupling Ceramic Capacitor)

## 1. Component Metadata
* **Reference Designator**: `C_HF`
* **Component Type**: High-Voltage Multilayer Ceramic Capacitor (MLCC)
* **Manufacturer**: Murata Manufacturing Co., Ltd.
* **Primary MPN**: `GA342QR7GD102KW01L`
* **Alternate Manufacturer**: TDK Corporation
* **Alternate MPN**: `C4532X7R2J104K230KA`
* **Package / Footprint**: SMD 1812 ($4.5 \times 3.2\,\text{mm}$)
* **Subsystem**: Stage 2 (Rectification & Bulk Link)

## 2. Electrical Ratings & Constraints
* **Nominal Capacitance**: $100.0\,\text{nF} \pm 10\%$ ($0.10\,\mu\text{F}$)
* **Rated DC Voltage**: $630\,\text{V}_{\text{DC}}$
  * Voltage Derating: $\frac{374.8\,\text{V}}{630\,\text{V}} = \mathbf{59.49\%} \le 75\%$ (Excellent reliability margin).
* **Dielectric Characteristic**: X7R ($-55^\circ\text{C}$ to $+125^\circ\text{C}$, $\Delta C \le \pm 15\%$)
* **ESR**: $< 15.0\,\text{m}\Omega$ @ $1.0\,\text{MHz}$
* **Functional Role**: Electrolytic capacitors (`C_BULK1`) have significant parasitic internal inductance ($ESL \approx 10 - 20\,\text{nH}$), rendering them ineffective at bypassing $65\,\text{kHz}$ fast switching edges ($t_r \approx 25\,\text{ns}$). `C_HF` provides an ultra-low impedance local high-frequency bypass path.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Placement Requirement |
| :---: | :---: | :--- | :--- | :--- |
| **1** | Terminal 1 | `+HV_BULK` | Transformer `TX1` Primary Pin 1, Snubber Diode `D_snub` | Placed $< 3.0\,\text{mm}$ from `TX1` Pin 1 pad. |
| **2** | Terminal 2 | `PGND_HOT` | CoolMOS `Q1` Source sense resistor return `R_CS` | Direct via return to primary ground plane. |

## 4. Schematic Symbol Representation
```
               Net: +HV_BULK
                     │
                   ┌─┴─┐
                   │   │  C_HF: 100nF / 630V X7R
                   │   │  Murata 1812
                   └─┬─┘
                     │
               Net: PGND_HOT
```

## 5. Schematic & PCB Layout Guidelines
1. **Critical High-Frequency Loop**: `C_HF` must be placed directly between `TX1` primary pin 1 and the source return of `Q1`. Traces connecting `C_HF` must be short, wide polygons ($> 2.0\,\text{mm}$) to eliminate stray inductance.
