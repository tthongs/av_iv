# Component Schematic Specification: TX1 (Isolated Flyback Power Transformer)

## 1. Component Metadata
* **Reference Designator**: `TX1`
* **Component Type**: High-Frequency Isolated Flyback Energy Transfer Transformer
* **Core Geometry**: PQ26/20 (A_e = 122.0 mm^2, V_e = 5490 mm^3)
* **Core Material**: Ferroxcube `3C95` / TDK `PC47` (High-flux saturation ferrite: B_sat = 0.380 T @ 100°C)
* **Bobbin**: Horizontal 12-Pin Through-Hole Bobbin (Creepage distance ≥ 6.4 mm)
* **Manufacturer**: Custom wound to VVDN specification / Ferroxcube (`3C95-PQ2620-72W`)
* **Subsystem**: Stage 3 (Isolated Flyback Subsystem)

## 2. Electrical Specifications & Derived Magnetics
* **Primary Inductance (L_p)**: 220.0 µH ± 10% @ 10 kHz, 0.1 V
* **Turns Ratio (N_p : N_s : N_aux)**:
 * Primary Winding (N_p): 36 turns (Double-strand 0.35 mm Grade 2 enamel wire, L_p = 220 µH)
 * Secondary Winding (N_s): 6 turns (N_p / N_s = 6.0:1) Furukawa `TEX-E` 0.80 mm Triple-Insulated Wire (TIW)
 * Auxiliary Bias Winding (N_aux): 4 turns (Single-strand 0.25 mm enamel wire, generates +14.0 V_DC)
* **Maximum Operating Flux Density**:
 B_max = (L_p × I_pk / N_p × A_e) = (220 × 10^-6 H) × (3.03 A) / 36 × (122 × 10^-6 m^2) = (6.666 × 10^-4 / 4.392 × 10^-3) = 0.1518 Tesla
 Leaves an exceptional **60.0% safety margin** below the core saturation point (B_sat = 0.380 T).
* **Primary Leakage Inductance (L_lk)**: Sized at ≤ 2.0% × L_p ≈ 4.40 µH max.
* **Galvanic Dielectric Withstand**: Certified **3000 V_AC RMS (1 minute)** primary-to-secondary proof rating compliant with IEC 62368-1 reinforced isolation standards.

## 3. Schematic Pin Connections & Winding Pinout
| Bobbin Pin # | Domain | Winding Designation | Net Name | Connected To | Phase Dot |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **1** | Primary | Pri Winding Start (N_p) | `+HV_BULK` | High-voltage DC link (+), `C_BULK1` (+), `C_HF` (Pin 1) | [Dot] |
| **2** | Primary | Pri Winding Finish (N_p) | `FLY_DRAIN` | Primary CoolMOS `Q1` Drain, Snubber Diode `D_snub` Cathode | — |
| **3** | Primary | Aux Winding Start (N_aux)| `FLY_AUX_AC` | Aux Rectifier Diode `D_AUX` (UF4004) Anode | [Dot] |
| **4** | Primary | Aux Winding Finish (N_aux)| `PGND_HOT` | Primary hot power ground return plane | — |
| **5, 6** | Secondary| Sec Winding Start (N_s) | `FLY_SEC_ANODE` | Secondary Schottky Rectifier `D_SEC` Anode (Pins tied in parallel)| [Dot] |
| **7, 8** | Secondary| Sec Winding Finish (N_s) | `PGND_SEC` | Secondary touch-safe SELV ground plane (`PGND_SEC`) | — |

## 4. Schematic Symbol Representation
```
 Net: +HV_BULK
 │
 [1] ●═══╗ Primary Winding (Np = 36 Turns)
 ║ L_p = 220µH ± 10%
 ║
 [2] ────╢──────────────────> Net: FLY_DRAIN (To Q1 Drain & Snubber)
 ║║
 Net: FLY_AUX ║║ PQ26/20 3C95 FERRITE CORE
 │ ║║ Reinforced Isolation Barrier (3000 V RMS)
 [3] ●═══╝║
 ║ Aux Winding (Naux = 4 Turns)
 [4] ────╢──────────────────> Net: PGND_HOT (Primary Hot Ground)
 ║║
 ║║
 [5,6]●══╗ Secondary Winding (Ns = 6 Turns)
 ║ Furukawa TEX-E Triple-Insulated Wire
 ║
 [7,8]───╢──────────────────> Net: PGND_SEC (Secondary Touch-Safe Ground)
 │
 Net: FLY_SEC_ANODE (To D_SEC Anode)
```

## 5. Schematic & PCB Layout Guidelines
1. **Safety Isolation Barrier**: Route a **2.0 mm wide milled PCB air slot** directly through the FR4 substrate beneath the transformer core separating primary bobbin pins (1-4) from secondary bobbin pins (5-8). Surface creepage must strictly exceed ≥ 6.4 mm.
2. **Leakage Inductance Control**: Transformer windings must use interleaved construction (Primary half rightarrow Secondary TIW rightarrow Primary second half) to minimize leakage inductance below 4.4 µH.
