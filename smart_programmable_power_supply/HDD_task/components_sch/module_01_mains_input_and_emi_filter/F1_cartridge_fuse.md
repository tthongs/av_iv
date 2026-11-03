# Component Schematic Specification: F1 (AC Mains Input Cartridge Fuse)

## 1. Component Metadata
* **Reference Designator**: `F1` (Mounted in PCB clips `FC1`, `FC2`)
* **Component Type**: Time-Lag (Slow-Blow) Ceramic Cartridge Fuse
* **Manufacturer**: Littelfuse Inc.
* **Primary MPN**: `0218002.MXP`
* **Alternate Manufacturer**: Schurter
* **Alternate MPN**: `0001.2507`
* **Package / Footprint**: 5 imes 20 mm Cylindrical Cartridge (Clips: Keystone Electronics `3515`)
* **Subsystem**: Stage 1 (Mains AC Input & Protection)

## 2. Electrical Ratings & Constraints
* **Rated Current (I_n)**: 2.0 A_ RMS
* **Rated Voltage**: 250 V_ AC RMS
* **Melting Energy (I^2t)**: 19.6 A^2 s (Safely absorbs inrush I^2t approx 0.468 A^2 s << 19.6 A^2 s)
* **Interrupting Rating**: 1500 A @ 250 V_ AC (IEC 60127-2 Sheet 5)
* **Maximum Continuous Load Current**: 1.604 A_ RMS at 85 V_ AC (80.2% loading ≤ 85%)

## 3. Schematic Pin Connections & Net Mapping
| Pin / Clip # | Clip Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `FC1` (Input) | `AC_LINE_IN` | `J1` Terminal L | 2.5 mm width on Layer 1 (2oz Cu), reinforced with bottom trace. |
| **2** | `FC2` (Output) | `AC_LINE_FUSED`| `MOV1` (Terminal 1), `C_X1` (Terminal 1), `L_CM1` (Pin 1) | 2.5 mm width on Layer 1 (2oz Cu). Low-impedance bus. |

## 4. Schematic Symbol Representation
```
 Net: AC_LINE_IN Net: AC_LINE_FUSED
 ───────────────────[ F1: 2.0A TIME-LAG ]───────────────────> To MOV1, CX1, LCM1
 5x20mm Ceramic
```

## 5. Schematic & PCB Layout Guidelines
1. **Fuse Proximity**: Place `F1` immediately adjacent to AC inlet `J1` Live pin (< 15 mm trace length).
2. **No Polygon Copper Underneath**: Strip all copper polygon pours on all layers directly beneath the fuse body (5 imes 20 mm keepout) to prevent arcing during catastrophic rupture.
3. **Fuse Clips**: Use heavy-duty tin-plated phosphor bronze clips (`Keystone 3515`) to ensure low contact resistance and prevent thermal oxidation.
