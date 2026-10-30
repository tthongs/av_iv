# Component Schematic Specification: QA, QB, QC, QD (Power MOSFET H-Bridge)

## 1. Component Metadata
* **Reference Designators**: `QA` (Buck High-Side), `QB` (Buck Low-Side Sync), `QC` (Boost Low-Side Sync), `QD` (Boost High-Side)
* **Component Type**: N-Channel OptiMOS™ 5 Logic-Level Power MOSFET
* **Manufacturer**: Infineon Technologies
* **Primary MPN**: `BSC034N04LS`
* **Alternate Manufacturer**: Texas Instruments
* **Alternate MPN**: `CSD18534Q5A` (40 V, 3.5 mΩ, SON-8)
* **Package / Footprint**: TDSON-8 / SuperSO8 (Power Stage SMD, $5.0 \times 6.0\,\text{mm}$, Height: $1.0\,\text{mm}$)
* **Subsystem**: Stage 4 (Synchronous Buck-Boost Power Bridge)

## 2. Electrical Ratings & Constraints
* **Drain-Source Breakdown Voltage ($V_{\text{DS}}$)**: $40.0\,\text{V}_{\text{DC}}$
  * Maximum operating bridge rail: $+24.0\,\text{V}_{\text{DC}}$ intermediate rail (with peak ringing clamped $\le 28.0\,\text{V}$).
  * Voltage Derating: $\frac{28.0\,\text{V}}{40.0\,\text{V}} = \mathbf{70.0\%}$ (Strictly satisfies VVDN $\le 75\%$ maximum limit).
* **Continuous Drain Current ($I_D$)**: $70.0\,\text{A}$ at $T_c = 25^\circ\text{C}$ / $55.0\,\text{A}$ at $T_c = 100^\circ\text{C}$
  * Worst-case peak operating inductor current: $I_{L,\text{peak}} = 4.00\,\text{A}$
  * Current Derating: $\frac{4.00\,\text{A}}{55.0\,\text{A}} = \mathbf{7.27\%}$ (Over 10x safety margin, zero electromigration risk).
* **Static Drain-Source On-Resistance ($R_{\text{DS(on)}}$)**:
  * $3.4\,\text{m}\Omega$ typical ($4.2\,\text{m}\Omega$ max) at $V_{\text{GS}} = 10\,\text{V}$.
  * $5.1\,\text{m}\Omega$ max at $V_{\text{GS}} = 4.5\,\text{V}$.
  * At $T_j = 85^\circ\text{C}$: $R_{\text{DS(on)}} \approx 1.35 \times 3.4\,\text{m}\Omega = \mathbf{4.59\,\text{m}\Omega}$.
* **Total Gate Charge ($Q_g$)**: $18.0\,\text{nC}$ at $V_{\text{GS}} = 10\,\text{V}$ ($8.8\,\text{nC}$ typical at $4.5\,\text{V}$)
  * Enables fast switching transition times ($t_r \approx 5.0\,\text{ns}$, $t_f \approx 4.0\,\text{ns}$) with ultra-low gate drive power:
    $$P_{\text{gate}} = 4 \times Q_g \times V_{\text{GS}} \times f_{\text{sw}} = 4 \times (18\,\text{nC}) \times 7.3\,\text{V} \times 300\,\text{kHz} = \mathbf{157.7\,\text{mW}}$$
* **Bridge Conduction & Switching Losses (Full Load $60\,\text{W}$)**:
  * In Buck mode ($V_{\text{OUT}} = 12\,\text{V}$, $D = 0.50$):
    $$P_{\text{cond,QA}} = I_{\text{RMS}}^2 \times R_{\text{DS(on)}} \times D = (3.03\,\text{A})^2 \times 4.59\,\text{m}\Omega \times 0.50 = 21.1\,\text{mW}$$
    $$P_{\text{sw,QA}} = \frac{1}{2} V_{\text{IN}} I_{\text{OUT}} (t_r + t_f) f_{\text{sw}} = \frac{1}{2} (24\,\text{V})(3\,\text{A})(9\,\text{ns})(300\,\text{kHz}) = 97.2\,\text{mW}$$
  * Total four-FET dissipated power is $< \mathbf{0.42\,\text{W}}$, resulting in a negligible case temperature rise ($\Delta T_c < 12^\circ\text{C}$).

## 3. Schematic Pin Connections & Bridge Configuration
Each TDSON-8 package features Pins 1-3 as Source, Pin 4 as Gate, and Pins 5-8 (plus bottom exposed thermal pad) as Drain:

| FET Ref Des | Role in H-Bridge | Source (Pins 1..3) Net | Gate (Pin 4) Net | Drain (Pins 5..8 + Pad) Net | Gate Series Resistor |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **`QA`** | Buck High-Side Switch | `SW1_NODE` | `GATE_QA` | `+24V_SEC` (Intermediate Bus) | $2.2\,\Omega \pm 1\%$ (`R_G1`) |
| **`QB`** | Buck Low-Side Synchronous | `PGND_SEC` | `GATE_QB` | `SW1_NODE` | $1.0\,\Omega \pm 1\%$ (`R_G2`) |
| **`QC`** | Boost Low-Side Synchronous | `PGND_SEC` | `GATE_QC` | `SW2_NODE` | $1.0\,\Omega \pm 1\%$ (`R_G3`) |
| **`QD`** | Boost High-Side Switch | `SW2_NODE` | `GATE_QD` | `+V_OUT_PRE` (Before Shunt) | $2.2\,\Omega \pm 1\%$ (`R_G4`) |

## 4. Schematic Symbol & Circuit Representation
```
               [ QA: BUCK HIGH-SIDE ]                 [ QD: BOOST HIGH-SIDE ]
                 TDSON-8 (BSC034N04LS)                  TDSON-8 (BSC034N04LS)
                 ┌───────────────────┐                  ┌───────────────────┐
  +24V_SEC ─────[5-8] D           S [1-3]─── SW1_NODE ──[1-3] S           D [5-8]─── +V_OUT_PRE
                 │         G         │                  │         G         │
                 └─────────┬─────────┘                  └─────────┬─────────┘
                           │ [4]                                  │ [4]
                        GATE_QA                                GATE_QD
                           │                                      │
                           └──[ 2.2Ω ]── U3 HDRV1                 └──[ 2.2Ω ]── U3 HDRV2

               [ QB: BUCK LOW-SIDE ]                  [ QC: BOOST LOW-SIDE ]
                 TDSON-8 (BSC034N04LS)                  TDSON-8 (BSC034N04LS)
                 ┌───────────────────┐                  ┌───────────────────┐
  SW1_NODE ─────[5-8] D           S [1-3]─── PGND_SEC ──[1-3] S           D [5-8]─── SW2_NODE
                 │         G         │                  │         G         │
                 └─────────┬─────────┘                  └─────────┬─────────┘
                           │ [4]                                  │ [4]
                        GATE_QB                                GATE_QC
                           │                                      │
                           └──[ 1.0Ω ]── U3 LDRV1                 └──[ 1.0Ω ]── U3 LDRV2
```

## 5. Schematic & PCB Layout Guidelines
1. **Loop Area Symmetrical Placement**: Place `QA` and `QB` in close proximity to form an ultra-compact Buck input loop with the $24\,\text{V}$ input ceramic capacitors. Place `QC` and `QD` in close proximity to form the Boost output loop with `C_OUT` ceramic capacitors.
2. **Switch Node Copper Areas**: Switch nodes `SW1_NODE` and `SW2_NODE` carry fast square waves ($300\,\text{kHz}$, $t_r < 10\,\text{ns}$). Keep the copper polygon area just large enough to carry $4\,\text{A}_{\text{RMS}}$ ($w \approx 2.5\,\text{mm}$), avoiding oversized copper planes that radiate capacitive electric field noise to adjacent sensitive analog traces.
3. **Thermal Vias on Drain Pours**: Connect the drain thermal tab (Pins 5-8) of each FET to Layer 1 copper and place an array of 6 thermal vias ($0.3\,\text{mm}$ drill) under each tab to dissipate heat to internal copper planes.
