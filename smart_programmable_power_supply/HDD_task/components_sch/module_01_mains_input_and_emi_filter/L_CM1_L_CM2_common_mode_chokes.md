# Component Schematic Specification: L_CM1 & L_CM2 (Common-Mode EMI Chokes)

## 1. Component Metadata
* **Reference Designators**: `L_CM1` (Stage 1 LF Choke), `L_CM2` (Stage 2 HF Choke)
* **Component Type**: Two-Winding Common-Mode Inductors
* **Manufacturer**: Wurth Elektronik
* **Primary MPNs**:
 * `L_CM1`: `744823215` (15.0 mH ± 30%, 1.10 A_ RMS, Toroid Core)
 * `L_CM2`: `744822472` (4.70 mH ± 30%, 1.60 A_ RMS, Sectional Winding Core)
* **Alternate Manufacturers**: KEMET (`SC-10-10J`) / Bourns (`7355-V-RC`)
* **Package / Footprint**: 4-Pin Through-Hole Toroidal Header (Pitch 15.0 imes 10.0 mm)
* **Subsystem**: Stage 1 (Mains AC Input & EMI Filter)

## 2. Electrical Ratings & Constraints
* **Operating Voltage**: 250 V_ AC RMS continuous (500 V dielectric test withstand between windings)
* **Current Rating**: 1.10 A (`L_CM1`) / 1.60 A (`L_CM2`) (Operating RMS: 0.55 A @ 230 V, 1.60 A @ 85 V)
* **Frequency Coverage**:
 * `L_CM1` (15 mH): Sized for 150 kHz - 2.0 MHz low-frequency attenuation.
 * `L_CM2` (4.7 mH): Sized for 2.0 MHz - 30.0 MHz high-frequency attenuation.
* **Combined CM Attenuation**: > 35.4 dB at 150 kHz, ensuring CISPR 32 Class B compliance.

## 3. Schematic Pin Connections & Net Mapping
### L_CM1 (Stage 1 Choke)
| Pin # | Winding | Net Name (In/Out) | Connected To | Phase Dot |
| :---: | :---: | :--- | :--- | :---: |
| **1** | W1 (Line) In | `AC_LINE_FUSED` | Fuse `F1`, `MOV1`, `C_X1` Pin 1 | [Dot] |
| **2** | W1 (Line) Out | `AC_LINE_CM1` | `L_CM2` Pin 1, `C_Y1` Pin 1 | — |
| **3** | W2 (Neut) Out | `AC_NEUTRAL_CM1` | `L_CM2` Pin 2, `C_Y2` Pin 1 | — |
| **4** | W2 (Neut) In | `AC_NEUTRAL_PROT` | `NTC1`, `MOV1`, `C_X1` Pin 2 | [Dot] |

### L_CM2 (Stage 2 Choke)
| Pin # | Winding | Net Name (In/Out) | Connected To | Phase Dot |
| :---: | :---: | :--- | :--- | :---: |
| **1** | W1 (Line) In | `AC_LINE_CM1` | `L_CM1` Pin 2, `C_Y1` Pin 1 | [Dot] |
| **2** | W1 (Line) Out | `AC_LINE_FILT` | `C_X2` Pin 1, Bridge Rectifier `BR1` Pin 2 (AC) | — |
| **3** | W2 (Neut) Out | `AC_NEUTRAL_FILT`| `C_X2` Pin 2, Bridge Rectifier `BR1` Pin 3 (AC) | — |
| **4** | W2 (Neut) In | `AC_NEUTRAL_CM1` | `L_CM1` Pin 3, `C_Y2` Pin 1 | [Dot] |

## 4. Schematic Symbol Representation
```
 Net: AC_LINE_FUSED L_CM1 Net: AC_LINE_CM1 L_CM2 Net: AC_LINE_FILT
 ──────────────────────●═══[ W1: 15mH ]═══───────────────●═══[ W1: 4.7mH ]═══────────────> To BR1 Pin 2
 ║║ ║║
 ──────────────────────●═══[ W2: 15mH ]═══───────────────●═══[ W2: 4.7mH ]═══────────────> To BR1 Pin 3
 Net: AC_NEUTRAL_PROT Net: AC_NEUTRAL_CM1 Net: AC_NEUTRAL_FILT
```

## 5. Schematic & PCB Layout Guidelines
1. **Winding Phasing**: Strict adherence to winding phase dots is essential. If one winding is reversed, common-mode impedance collapses to near zero.
2. **Symmetric Routing**: Keep Live and Neutral traces perfectly parallel and identical in length through both chokes.
3. **No Cross-Talk**: Route input traces and output traces on opposite sides of the choke body to prevent capacitive bypass coupling.
