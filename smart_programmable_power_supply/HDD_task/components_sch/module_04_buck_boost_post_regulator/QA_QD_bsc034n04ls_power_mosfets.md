# Component Schematic Specification: QA, QB, QC, QD (Power MOSFET H-Bridge)

## 1. Component Metadata
* **Reference Designators**: `QA` (Buck High-Side), `QB` (Buck Low-Side Sync), `QC` (Boost Low-Side Sync), `QD` (Boost High-Side)
* **Component Type**: N-Channel OptiMOS™ 5 Logic-Level Power MOSFET
* **Manufacturer**: Infineon Technologies
* **Primary MPN**: `BSC034N04LS`
* **Alternate Manufacturer**: Texas Instruments
* **Alternate MPN**: `CSD18534Q5A` (40 V, 3.5 mΩ, SON-8)
* **Package / Footprint**: TDSON-8 / SuperSO8 (Power Stage SMD, 5.0 × 6.0 mm, Height: 1.0 mm)
* **Subsystem**: Stage 4 (Synchronous Buck-Boost Power Bridge)

## 2. Electrical Ratings & Constraints
* **Drain-Source Breakdown Voltage (V_DS)**: 40.0 V_DC
 * Maximum operating bridge rail: +24.0 V_DC intermediate rail (with peak ringing clamped ≤ 28.0 V).
 * Voltage Derating: (28.0 V / 40.0 V) = 70.0% (Strictly satisfies VVDN ≤ 75% maximum limit).
* **Continuous Drain Current (I_D)**: 70.0 A at T_c = 25°C / 55.0 A at T_c = 100°C
 * Worst-case peak operating inductor current: I_L,peak = 4.00 A
 * Current Derating: (4.00 A / 55.0 A) = 7.27% (Over 10x safety margin, zero electromigration risk).
* **Static Drain-Source On-Resistance (R_DS(on)**:
 * 3.4 mΩ typical (4.2 mΩ max) at V_GS = 10 V.
 * 5.1 mΩ max at V_GS = 4.5 V.
 * At T_j = 85°C: R_DS(on) ≈ 1.35 × 3.4 mΩ = 4.59 mΩ.
* **Total Gate Charge (Q_g)**: 18.0 nC at V_GS = 10 V (8.8 nC typical at 4.5 V)
 * Enables fast switching transition times (t_r ≈ 5.0 ns, t_f ≈ 4.0 ns) with ultra-low gate drive power:
 P_gate = 4 × Q_g × V_GS × f_sw = 4 × (18 nC) × 7.3 V × 300 kHz = 157.7 mW
* **Bridge Conduction & Switching Losses (Full Load 60 W)**:
 * In Buck mode (V_OUT = 12 V, D = 0.50):
 P_cond,QA = I_RMS^2 × R_DS(on) × D = (3.03 A)^2 × 4.59 mΩ × 0.50 = 21.1 mW
 P_sw,QA = (1 / 2) V_IN I_OUT (t_r + t_f) f_sw = (1 / 2) (24 V)(3 A)(9 ns)(300 kHz) = 97.2 mW
 * Total four-FET dissipated power is < 0.42 W, resulting in a negligible case temperature rise (Δ T_c < 12°C).

## 3. Schematic Pin Connections & Bridge Configuration
Each TDSON-8 package features Pins 1-3 as Source, Pin 4 as Gate, and Pins 5-8 (plus bottom exposed thermal pad) as Drain:

| FET Ref Des | Role in H-Bridge | Source (Pins 1..3) Net | Gate (Pin 4) Net | Drain (Pins 5..8 + Pad) Net | Gate Series Resistor |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **`QA`** | Buck High-Side Switch | `SW1_NODE` | `GATE_QA` | `+24V_SEC` (Intermediate Bus) | 2.2 Ω ± 1% (`R_G1`) |
| **`QB`** | Buck Low-Side Synchronous | `PGND_SEC` | `GATE_QB` | `SW1_NODE` | 1.0 Ω ± 1% (`R_G2`) |
| **`QC`** | Boost Low-Side Synchronous | `PGND_SEC` | `GATE_QC` | `SW2_NODE` | 1.0 Ω ± 1% (`R_G3`) |
| **`QD`** | Boost High-Side Switch | `SW2_NODE` | `GATE_QD` | `+V_OUT_PRE` (Before Shunt) | 2.2 Ω ± 1% (`R_G4`) |

## 4. Schematic Symbol & Circuit Representation
```
 [ QA: BUCK HIGH-SIDE ] [ QD: BOOST HIGH-SIDE ]
 TDSON-8 (BSC034N04LS) TDSON-8 (BSC034N04LS)
 ┌───────────────────┐ ┌───────────────────┐
 +24V_SEC ─────[5-8] D S [1-3]─── SW1_NODE ──[1-3] S D [5-8]─── +V_OUT_PRE
 │ G │ │ G │
 └─────────┬─────────┘ └─────────┬─────────┘
 │ [4] │ [4]
 GATE_QA GATE_QD
 │ │
 └──[ 2.2Ω ]── U3 HDRV1 └──[ 2.2Ω ]── U3 HDRV2

 [ QB: BUCK LOW-SIDE ] [ QC: BOOST LOW-SIDE ]
 TDSON-8 (BSC034N04LS) TDSON-8 (BSC034N04LS)
 ┌───────────────────┐ ┌───────────────────┐
 SW1_NODE ─────[5-8] D S [1-3]─── PGND_SEC ──[1-3] S D [5-8]─── SW2_NODE
 │ G │ │ G │
 └─────────┬─────────┘ └─────────┬─────────┘
 │ [4] │ [4]
 GATE_QB GATE_QC
 │ │
 └──[ 1.0Ω ]── U3 LDRV1 └──[ 1.0Ω ]── U3 LDRV2
```

## 5. Schematic & PCB Layout Guidelines
1. **Loop Area Symmetrical Placement**: Place `QA` and `QB` in close proximity to form an ultra-compact Buck input loop with the 24 V input ceramic capacitors. Place `QC` and `QD` in close proximity to form the Boost output loop with `C_OUT` ceramic capacitors.
2. **Switch Node Copper Areas**: Switch nodes `SW1_NODE` and `SW2_NODE` carry fast square waves (300 kHz, t_r < 10 ns). Keep the copper polygon area just large enough to carry 4 A_RMS (w ≈ 2.5 mm), avoiding oversized copper planes that radiate capacitive electric field noise to adjacent sensitive analog traces.
3. **Thermal Vias on Drain Pours**: Connect the drain thermal tab (Pins 5-8) of each FET to Layer 1 copper and place an array of 6 thermal vias (0.3 mm drill) under each tab to dissipate heat to internal copper planes.
