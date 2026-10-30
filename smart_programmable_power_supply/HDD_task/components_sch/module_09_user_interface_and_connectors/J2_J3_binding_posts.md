# Component Schematic Specification: J2, J3 (4mm Heavy-Duty Output Binding Posts)

## 1. Component Metadata
* **Reference Designators**:
  * `J2`: DC Output Positive Terminal (Red)
  * `J3`: DC Output Negative Terminal (Black)
* **Component Type**: Heavy-Duty Gold-Plated $4\,\text{mm}$ Safety Banana Binding Posts
* **Manufacturer**: Pomona Electronics
* **Primary MPNs**:
  * `J2` (Red Positive): `3770-2`
  * `J3` (Black Negative): `3770-0`
* **Alternate Manufacturer**: Mueller Electric
* **Alternate MPNs**: `BU-P3770-2` (Red) / `BU-P3770-0` (Black)
* **Package / Mounting**: Panel-Mount Threaded Stud with Heavy Solder Lug (Pitch: Standard $19.05\,\text{mm}$ / $0.75\,\text{in}$)
* **Subsystem**: Stage 9 (High-Current Regulated DC Power Delivery Terminals)

## 2. Electrical Ratings & Constraints
* **Rated Current ($I_{\text{rated}}$)**: $30.0\,\text{A}_{\text{DC}}$ continuous
  * Operating continuous current: $3.0\,\text{A}_{\text{DC}}$ ($4.2\,\text{A}$ peak surge).
  * Current Derating: $\frac{3.0\,\text{A}}{30.0\,\text{A}} = \mathbf{10.0\%} \ll 70\%$ (Virtually zero heating or resistance loss).
* **Rated Voltage ($V_{\text{rated}}$)**: $1000\,\text{V}_{\text{CAT I}}$ ($2500\,\text{V}$ peak breakdown).
* **Contact Resistance**: $< 1.0\,\text{m}\Omega$ (Gold-plated brass core prevents galvanic oxidation).
* **Mechanical Features**: Accepts standard $4\,\text{mm}$ shrouded banana plugs, bare wire up to $10\,\text{AWG}$ clamped through cross-hole, or spade lugs up to $8.0\,\text{mm}$ width.

## 3. Schematic Pin Connections & Net Mapping
| Ref Des | Terminal Function | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **`J2`** | **`+` (Positive DC Out)** | `+V_OUT` | `R_shunt` Exit Pad, `C_POLY1` (+), `U3` VOSNS | Heavy 2oz copper polygon ($w \ge 5.0\,\text{mm}$). |
| **`J3`** | **`-` (Negative DC Out)** | `GND_SELV` | Secondary ground plane, `C_POLY1` (-) | Heavy 2oz copper polygon ($w \ge 5.0\,\text{mm}$). |

## 4. Schematic Symbol Representation
```
                    [ 4mm HEAVY-DUTY OUTPUT BINDING POSTS ]
                                Standard 19.05 mm Spacing

          Net: +V_OUT    ──────────────[ J2: RED (+) POST ]
                                               (30A / 1000V)

          Net: GND_SELV  ──────────────[ J3: BLACK (-) POST ]
                                               (30A / 1000V)
```

## 5. Schematic & PCB Layout Guidelines
1. **Reinforced Annular Solder Rings**: The PCBA mounting pads for the binding post studs must feature heavy through-hole barrels ($\varnothing 4.5\,\text{mm}$) surrounded by an array of eight $0.5\,\text{mm}$ vias stitching Layers 1, 2, 3, and 4 together to support both mechanical torque and $3\,\text{A}$ continuous conduction without thermal delamination.
