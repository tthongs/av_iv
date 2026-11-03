# Component Schematic Specification: C_POLY1 (Solid Aluminum Polymer Capacitor)

## 1. Component Metadata
* **Reference Designator**: `C_POLY1`
* **Component Type**: OS-CON™ Solid Aluminum Polymer Capacitor
* **Manufacturer**: Panasonic Industrial Devices
* **Primary MPN**: `25SVPF100M`
* **Alternate Manufacturer**: KEMET
* **Alternate MPN**: `A750KK107M1EAAE015` (100 µF, 25 V, 15 mΩ ESR)
* **Package / Footprint**: Radial Can SMD Size F8 (8.0 mm Diameter × 10.0 mm Height)
* **Subsystem**: Stage 4 (Dynamic Transient Step-Load Reservoir)

## 2. Electrical Ratings & Constraints
* **Nominal Capacitance**: 100.0 µF ± 20% at 120 Hz (Solid polymer: zero DC bias voltage degradation!)
* **Rated Working Voltage (V_rated)**: 25.0 V_DC
 * Maximum continuous rail: 20.0 V_DC
 * Voltage Derating: (20.0 V / 25.0 V) = 80.0%
 * Surge Voltage Rating: 28.8 V_DC (1000 cycles).
* **Equivalent Series Resistance (ESR)**: 12.0 mΩ maximum across 100 kHz to 300 kHz
* **Maximum Rated Ripple Current**: 3.20 A_RMS at 105°C, 100 kHz
* **Operating Temperature Range**: -55°C to +105°C with > 5000 hours endurance.
* **Dynamic Step-Load Response (10% -> 90% step, 0.3 A -> 2.7 A at 1.0 A/µs)**:
 * Inductor response lag: t_recov ≈ 25 µs (based on 25 kHz loop bandwidth).
 * Output voltage transient dip:
 Δ V_OUT,trans = (Δ I_step × t_recov / C_OUT,tot) + Δ I_step × ESR_poly = (2.4 A)(25 µs) / 138 µF) + (2.4 A)(12 mΩ) = 43.5 mV + 28.8 mV = 72.3 mV
 * Transient droop is strictly < 100 mV (0.36% on 20 V rail, 1.45% on 5 V rail), recovering fully within 50 µs.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`+` (Anode)** | `+V_OUT` | `R_shunt` Exit Pad, Output Binding Post `J2` (+), Divider `R_top` | Heavy copper polygon (w ≥ 4.0 mm, 2oz Cu). |
| **2** | **`-` (Cathode)**| `GND_SELV` | Output Binding Post `J3` (-), Secondary Ground Plane | Direct connection to secondary SELV ground plane. |

## 4. Schematic Symbol Representation
```
 [ C_POLY1: PANASONIC 25SVPF100M 100µF / 25V POLYMER ]
 ┌─────────────┐
 Net: +V_OUT ───────────┤+ 100 µF │
 │ 25V 12mΩ │
 Net: GND_SELV ───────────┤- OS-CON │
 └─────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Placement**: Locate `C_POLY1` immediately downstream of `R_shunt` and right before the output binding post solder lugs.
2. **Thermal Clearance**: Keep the polymer capacitor body at least 10.0 mm away from switching MOSFETs and power inductor `L1` to prevent radiated heat from raising the ambient temperature around the polymer seal.
