# Component Schematic Specification: C_HF (High-Voltage Decoupling Ceramic Capacitor)

## 1. Component Metadata
* **Reference Designator**: `C_HF`
* **Component Type**: High-Voltage Multilayer Ceramic Capacitor (MLCC)
* **Manufacturer**: Murata Manufacturing Co., Ltd.
* **Primary MPN**: `GA342QR7GD102KW01L`
* **Alternate Manufacturer**: TDK Corporation
* **Alternate MPN**: `C4532X7R2J104K230KA`
* **Package / Footprint**: SMD 1812 (4.5 × 3.2 mm)
* **Subsystem**: Stage 2 (Rectification & Bulk Link)

## 2. Electrical Ratings & Constraints
* **Nominal Capacitance**: 100.0 nF ± 10% (0.10 µF)
* **Rated DC Voltage**: 630 V_DC
 * Voltage Derating: (374.8 V / 630 V) = 59.49% ≤ 75% (Excellent reliability margin).
* **Dielectric Characteristic**: X7R (-55°C to +125°C, Δ C ≤ ± 15%)
* **ESR**: < 15.0 mΩ @ 1.0 MHz
* **Functional Role**: Electrolytic capacitors (`C_BULK1`) have significant parasitic internal inductance (ESL ≈ 10 - 20 nH), rendering them ineffective at bypassing 65 kHz fast switching edges (t_r ≈ 25 ns). `C_HF` provides an ultra-low impedance local high-frequency bypass path.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Placement Requirement |
| :---: | :---: | :--- | :--- | :--- |
| **1** | Terminal 1 | `+HV_BULK` | Transformer `TX1` Primary Pin 1, Snubber Diode `D_snub` | Placed < 3.0 mm from `TX1` Pin 1 pad. |
| **2** | Terminal 2 | `PGND_HOT` | CoolMOS `Q1` Source sense resistor return `R_CS` | Direct via return to primary ground plane. |

## 4. Schematic Symbol Representation
```
 Net: +HV_BULK
 │
 ┌─┴─┐
 │ │ C_HF: 100nF / 630V X7R
 │ │ Murata 1812
 └─┬─┘
 │
 Net: PGND_HOT
```

## 5. Schematic & PCB Layout Guidelines
1. **Critical High-Frequency Loop**: `C_HF` must be placed directly between `TX1` primary pin 1 and the source return of `Q1`. Traces connecting `C_HF` must be short, wide polygons (> 2.0 mm) to eliminate stray inductance.
