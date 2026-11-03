# Component Schematic Specification: L1 (Flat-Wire Power Inductor)

## 1. Component Metadata
* **Reference Designator**: `L1`
* **Component Type**: High-Current Flat-Wire Shielded Power Inductor
* **Manufacturer**: Würth Elektronik
* **Primary MPN**: `7443321000` (WE-HCC Series)
* **Alternate Manufacturer**: Coilcraft
* **Alternate MPN**: `SER2915L-103KL` (10.0 µH, 13.0 A sat)
* **Package / Footprint**: SMD 12.5 × 12.5 mm, Height: 10.0 mm (High-density flat-wire design)
* **Subsystem**: Stage 4 (Synchronous Buck-Boost Power Stage)

## 2. Electrical Ratings & Constraints
* **Nominal Inductance (L)**: 10.0 µH ± 20% at 100 kHz, 0.1 V
* **Saturation Current (I_sat)**: 11.5 A (defined at 30% inductance drop)
 * Operating worst-case peak inductor current:
 I_L,peak = I_OUT + (Δ I_L / 2) = 3.0 A + (2.0 A / 2) = 4.00 A
 * Saturation Headroom Margin:
 Margin = (I_sat - I_L,peak / I_sat) × 100% = (11.5 A - 4.00 A / 11.5 A) × 100% = 65.22%
 * Under a full 84.0 W surge transient (4.2 A output, I_L,peak = 5.6 A), saturation margin remains > 51.3%, completely preventing magnetic saturation or runaway core heating!
* **Rated RMS Current (I_RMS)**: 8.5 A (defined at Δ T = 40°C)
 * Operating continuous RMS current: 3.03 A_RMS
 * Current Derating: (3.03 A / 8.5 A) = 35.6% (VVDN requires ≤ 70%).
* **DC Resistance (DCR)**: 10.5 mΩ typical (13.5 mΩ max) at 20°C
 * Conduction copper loss:
 P_loss,L1 = I_RMS^2 × DCR_max = (3.03 A)^2 × (0.0135 Ω) = 0.124 W
* **Core Loss**: High-flux MnZn composite core material exhibits ultra-low hysteresis loss (< 65 mW at 300 kHz, Δ B = 60 mT). Total inductor dissipation is < 0.19 W.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`IN` (Switch Node 1)** | `SW1_NODE` | Source of `QA`, Drain of `QB`, `U3` SW1 pin | Heavy copper polygon (w ≥ 3.0 mm, 2oz Cu). |
| **2** | **`OUT` (Switch Node 2)**| `SW2_NODE` | Drain of `QC`, Source of `QD`, `U3` SW2 pin | Heavy copper polygon (w ≥ 3.0 mm, 2oz Cu). |

## 4. Schematic Symbol Representation
```
 [ L1: WURTH 7443321000 10µH / 11.5A ]
 ┌─────────────┐
 Net: SW1_NODE ───────┤1 █████ 2├─────── Net: SW2_NODE
 │ █████ │
 └─────────────┘
 Flat-Wire Shielded
```

## 5. Schematic & PCB Layout Guidelines
1. **Shortest Interconnect**: Place `L1` directly between the Buck switch node (`QA`/`QB`) and the Boost switch node (`QC`/`QD`). Keep total trace length between FET pins and inductor pads ≤ 8.0 mm.
2. **Magnetic Shielding & No-Copper Keepout**: While the WE-HCC inductor is magnetically shielded, avoid routing any sensitive signal traces (especially `LM5176_FB`, `CSP`/`CSN`, and ADC telemetry lines) on Layer 1 or Layer 2 directly underneath the inductor package.
3. **Heavy Current Carrying Solder Pads**: The SMD terminal pads are large (3.5 × 3.0 mm). Use solid copper connections (no thermal reliefs) to polygon pours on Layer 1 to minimize parasitic resistance and enhance heat conduction into the PCB substrate.
