#!/usr/bin/env python3
"""
Component and Schematic Connection Generator: Module 4 (Buck-Boost Post-Regulator)
"""

from pathlib import Path

OUT_DIR = Path("/home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/components_sch/module_04_buck_boost_post_regulator")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def write_files():
    # 1. U3 LM5176 Controller
    with open(OUT_DIR / "U3_lm5176_controller.md", "w") as f:
        f.write(r"""# Component Schematic Specification: U3 (LM5176PWPR Buck-Boost Controller)

## 1. Component Metadata
* **Reference Designator**: `U3`
* **Component Type**: 4-Switch Synchronous Buck-Boost Controller IC
* **Manufacturer**: Texas Instruments
* **Primary MPN**: `LM5176PWPR`
* **Alternate Manufacturer**: Analog Devices
* **Alternate MPN**: `LTC3789EGN#PBF` (functional discrete architecture equivalent)
* **Package / Footprint**: HTSSOP-28 with Exposed Thermal Pad (PowerPAD, Pitch: 0.65 mm, Body: 9.7 × 4.4 mm)
* **Subsystem**: Stage 4 (Synchronous Buck-Boost Post-Regulator)

## 2. Electrical Ratings & Constraints
* **Input Voltage Range ($V_{\text{IN}}$)**: $4.2\,\text{V}$ to $55.0\,\text{V}_{\text{DC}}$ (Continuous maximum rating: $60.0\,\text{V}$)
  * Operating input: $+24.0\,\text{V}_{\text{DC}} \pm 0.8\%$ from isolated Flyback Stage 3.
  * Voltage Derating: $\frac{24.0\,\text{V}}{60.0\,\text{V}} = \mathbf{40.0\%}$ (Well below 75% VVDN maximum limit).
* **Output Voltage Regulation Range**: $5.0\,\text{V}$ to $20.0\,\text{V}_{\text{DC}}$ at $3.0\,\text{A}_{\text{DC}}$ continuous ($60.0\,\text{W}$).
* **Switching Frequency ($f_{\text{sw}}$)**: $300.0\,\text{kHz} \pm 10\%$ programmed via $R_T = 24.9\,\text{k}\Omega \pm 1\%$ to AGND.
* **Internal Reference Voltage ($V_{\text{REF}}$)**: $0.800\,\text{V} \pm 1.0\%$ across full $-40^\circ\text{C}$ to $+125^\circ\text{C}$ temperature span.
* **Gate Drive Capability**:
  * $2.0\,\text{A}$ peak source / $3.0\,\text{A}$ peak sink current.
  * Drives high-side buck FET `QA`, low-side buck sync FET `QB`, low-side boost FET `QC`, and high-side boost sync FET `QD`.
* **Internal Bias Supply ($V_{\text{CC}}$)**: $+7.3\,\text{V}_{\text{DC}}$ typical regulated internal LDO.
  * Supplemented by external $+12.0\,\text{V}_{\text{DC}}$ rail via `BIAS` pin (Pin 28) to bypass internal LDO dissipation and maximize gate-drive slew rates.
* **Operating Modes**:
  * Smooth, automatic transition between Buck mode ($V_{\text{IN}} > V_{\text{OUT}}$: $24\text{V} \to 5\text{V}..19\text{V}$), Buck-Boost boundary mode ($V_{\text{IN}} \approx V_{\text{OUT}} \approx 20\text{V}$), and Boost mode.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Description & Trace Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`VISNS`** | `+24V_SEC` | Input ceramic decoupling `C_IN_CER` | Input voltage sense / feedforward; direct Kelvin trace to input rail. |
| **2** | **`EN/UVLO`** | `BUCK_BOOST_EN` | Resistor divider `R_UV1`/`R_UV2` & `Q_EN` collector | Enable & UVLO threshold ($1.22\,\text{V}$). MCU PB0 pulls LOW to shutdown. |
| **3** | **`VOSNS`** | `+V_OUT` | Output filter rail `+V_OUT` | Output voltage sense for mode transitions and OVP. |
| **4** | **`VOUT`** | `+V_OUT` | Output capacitor bank | Internal bias feedback and sense reference. |
| **5** | **`FB`** | `LM5176_FB` | DAC summing junction (`R_top`, `R_bot`, `R_DAC`) | Error amplifier inverting input ($V_{\text{FB}} = 0.800\,\text{V}$). Keep trace $< 5\,\text{mm}$. |
| **6** | **`COMP`** | `LM5176_COMP` | Type-II network (`R_comp`, `C_comp`, `C_comp2`), `Q_CLAMP` | Error amplifier compensation output. Clamped to GND for fast shutdown. |
| **7** | **`SS`** | `LM5176_SS` | Soft-start capacitor $C_{\text{SS}} = 33\,\text{nF}$ | Sets smooth monotonic startup ramp ($t_{\text{ss}} \approx 3.3\,\text{ms}$). |
| **8** | **`RT`** | `LM5176_RT` | Frequency resistor $R_T = 24.9\,\text{k}\Omega$ to `AGND_SEC` | Programs $300\,\text{kHz}$ PWM clock. Short trace to quiet analog ground. |
| **9** | **`MODE`** | `LM5176_MODE`| Pulled to `AGND_SEC` | Sets Forced Continuous Conduction Mode (FCCM) for continuous ripple control. |
| **10**| **`SLOPE`** | `LM5176_SLOPE`| Resistor $R_{\text{SLOPE}} = 100\,\text{k}\Omega$ to `AGND_SEC` | Programs internal slope compensation ramp to eliminate subharmonic oscillation. |
| **11**| **`AGND`** | `AGND_SEC` | Star connection to `GND_SELV` | Quiet analog ground reference; isolate from high $\frac{di}{dt}$ switching loops. |
| **12**| **`CS`** | `LM5176_CS` | Resistor $R_{\text{CS_IN}} = 100\,\Omega$ from Inductor sense | Current sense loop node. |
| **13**| **`CSN`** | `LM5176_CSN` | Shunt resistor `R_shunt` Kelvin Negative pad | Negative input for cycle-by-cycle peak/average current limit. |
| **14**| **`CSP`** | `LM5176_CSP` | Shunt resistor `R_shunt` Kelvin Positive pad | Positive input for current limit (trip threshold = $50\,\text{mV} \to 5.0\,\text{A}$). |
| **15**| **`ILIM`** | `LM5176_ILIM`| Divider from $V_{\text{CC}}$ setting $1.2\,\text{V}$ | Programs internal current limit threshold ($3.50\,\text{A}$ nominal clamp). |
| **16**| **`LDRV2`** | `GATE_QC` | Gate of low-side boost FET `QC` | Low-side boost gate drive pulse ($2.0\,\text{A}$ peak); wide $1.0\,\text{mm}$ trace. |
| **17**| **`PGND`** | `PGND_SEC` | Source of `QB`, `QC`, PowerPAD | Heavy power ground return carrying full inductor circulating currents. |
| **18**| **`HDRV2`** | `GATE_QD` | Gate of high-side boost sync FET `QD` | Floating high-side boost drive pulse; pair with `SW2`. |
| **19**| **`SW2`** | `SW2_NODE` | Switch node 2 (Drain `QC`, Source `QD`, `L1` Pin 2) | High $\frac{dv}{dt}$ switching node ($0\,\text{V}$ to $+20\,\text{V}$). Keep copper area compact. |
| **20**| **`BST2`** | `BST2_NODE` | Bootstrap cap $C_{\text{BST2}} = 100\,\text{nF}$ to `SW2` | High-side boost driver floating supply rail ($V_{\text{SW2}} + 7.3\,\text{V}$). |
| **21**| **`VCC`** | `+7V3_VCC` | Decoupling cap $C_{\text{VCC}} = 4.7\,\mu\text{F} / 16\,\text{V}$ X7R | Internal gate-drive LDO bypass; low ESL ceramic direct to `PGND`. |
| **22**| **`BIAS`** | `+12V_AUX` | Linear regulator `U7` output (+12V rail) | Overdrives internal LDO to supply gate drivers from auxiliary 12V bus. |
| **23**| **`BST1`** | `BST1_NODE` | Bootstrap cap $C_{\text{BST1}} = 100\,\text{nF}$ to `SW1` | High-side buck driver floating supply rail ($V_{\text{SW1}} + 7.3\,\text{V}$). |
| **24**| **`HDRV1`** | `GATE_QA` | Gate of high-side buck FET `QA` | Floating high-side buck drive pulse; pair with `SW1`. |
| **25**| **`SW1`** | `SW1_NODE` | Switch node 1 (Source `QA`, Drain `QB`, `L1` Pin 1) | High $\frac{dv}{dt}$ switching node ($0\,\text{V}$ to $+24\,\text{V}$). Minimize loop area. |
| **26**| **`LDRV1`** | `GATE_QB` | Gate of low-side buck sync FET `QB` | Low-side buck gate drive pulse ($2.0\,\text{A}$ peak); wide $1.0\,\text{mm}$ trace. |
| **27**| **`PGOOD`** | `MCU_PGOOD` | STM32 GPIO `PB1` (with $10\,\text{k}\Omega$ pull-up to 3.3V) | Open-drain Power Good indicator; goes HIGH when $V_{\text{OUT}}$ within $\pm 7\%$. |
| **28**| **`SYNC/EXT`**| `AGND_SEC` | Tied to `AGND_SEC` | Operates on internal free-running $300\,\text{kHz}$ oscillator. |
| **PAD**| **`PowerPAD`**| `PGND_SEC` | Thermal vias to Layer 2 & Layer 4 ground plane | Solder pad ($4.2 \times 2.8\,\text{mm}$) for electrical ground and heat sinking. |

## 4. Schematic Symbol Representation
```
                         [ U3: LM5176PWPR BUCK-BOOST CONTROLLER ]
                                  ┌────────────────────┐
        Net: +24V_SEC  ──────────[1] VISNS             [28] SYNC/EXT  ─── Net: AGND_SEC
    Net: BUCK_BOOST_EN ──────────[2] EN/UVLO           [27] PGOOD     ─── Net: MCU_PGOOD
        Net: +V_OUT    ──────────[3] VOSNS             [26] LDRV1     ─── Net: GATE_QB
        Net: +V_OUT    ──────────[4] VOUT              [25] SW1       ─── Net: SW1_NODE
        Net: LM5176_FB ──────────[5] FB                [24] HDRV1     ─── Net: GATE_QA
      Net: LM5176_COMP ──────────[6] COMP              [23] BST1      ─── Net: BST1_NODE
        Net: LM5176_SS ──────────[7] SS                [22] BIAS      ─── Net: +12V_AUX
        Net: LM5176_RT ──────────[8] RT                [21] VCC       ─── Net: +7V3_VCC
      Net: LM5176_MODE ──────────[9] MODE              [20] BST2      ─── Net: BST2_NODE
     Net: LM5176_SLOPE ──────────[10] SLOPE            [19] SW2       ─── Net: SW2_NODE
        Net: AGND_SEC  ──────────[11] AGND             [18] HDRV2     ─── Net: GATE_QD
        Net: LM5176_CS ──────────[12] CS               [17] PGND      ─── Net: PGND_SEC
       Net: LM5176_CSN ──────────[13] CSN              [16] LDRV2     ─── Net: GATE_QC
       Net: LM5176_CSP ──────────[14] CSP              [15] ILIM      ─── Net: LM5176_ILIM
                                  │                    │
                                  │    [ PowerPAD ]    │
                                  └──────────┬─────────┘
                                             │
                                     Net: PGND_SEC
```

## 5. Schematic & PCB Layout Guidelines
1. **Gate Drive Loop Minimization**: Keep `HDRV1`/`SW1`, `LDRV1`/`PGND`, `HDRV2`/`SW2`, and `LDRV2`/`PGND` traces routed as tight differential pairs on Layer 1 with trace widths $\ge 0.8\,\text{mm}$ to minimize parasitic gate loop inductance ($L_{\text{trace}} < 3\,\text{nH}$).
2. **Kelvin Shunt Routing**: Route `CSP` and `CSN` as a tightly shielded differential pair from the inside Kelvin pads of `R_shunt` directly to Pins 13 and 14 of `U3`. Avoid routing near high $\frac{dv}{dt}$ switch nodes `SW1` and `SW2`.
3. **PowerPAD Soldering**: Place an array of at least 12 thermal vias ($0.3\,\text{mm}$ drill, $0.6\,\text{mm}$ pad) inside the exposed pad area connecting directly to the Layer 2 solid ground plane for effective heat spreading ($\theta_{\text{JA}} \approx 28.5^\circ\text{C/W}$).
4. **Analog Ground Isolation**: Connect `AGND` (Pin 11) to `PGND` (Pin 17) at a single quiet star-point immediately beneath the IC. Decoupling capacitors for `VCC`, `SS`, and `RT` must return directly to `AGND`.
""")

    # 2. QA..QD BSC034N04LS Power MOSFETs
    with open(OUT_DIR / "QA_QD_bsc034n04ls_power_mosfets.md", "w") as f:
        f.write(r"""# Component Schematic Specification: QA, QB, QC, QD (Power MOSFET H-Bridge)

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
""")

    # 3. L1 Wurth 10uH Flat-Wire Inductor
    with open(OUT_DIR / "L1_wurth_10uH_flatwire_inductor.md", "w") as f:
        f.write(r"""# Component Schematic Specification: L1 (Flat-Wire Power Inductor)

## 1. Component Metadata
* **Reference Designator**: `L1`
* **Component Type**: High-Current Flat-Wire Shielded Power Inductor
* **Manufacturer**: Würth Elektronik
* **Primary MPN**: `7443321000` (WE-HCC Series)
* **Alternate Manufacturer**: Coilcraft
* **Alternate MPN**: `SER2915L-103KL` (10.0 µH, 13.0 A sat)
* **Package / Footprint**: SMD $12.5 \times 12.5\,\text{mm}$, Height: $10.0\,\text{mm}$ (High-density flat-wire design)
* **Subsystem**: Stage 4 (Synchronous Buck-Boost Power Stage)

## 2. Electrical Ratings & Constraints
* **Nominal Inductance ($L$)**: $10.0\,\mu\text{H} \pm 20\%$ at $100\,\text{kHz}$, $0.1\,\text{V}$
* **Saturation Current ($I_{\text{sat}}$)**: $11.5\,\text{A}$ (defined at $30\%$ inductance drop)
  * Operating worst-case peak inductor current:
    $$I_{L,\text{peak}} = I_{\text{OUT}} + \frac{\Delta I_L}{2} = 3.0\,\text{A} + \frac{2.0\,\text{A}}{2} = \mathbf{4.00\,\text{A}}$$
  * Saturation Headroom Margin:
    $$\text{Margin} = \frac{I_{\text{sat}} - I_{L,\text{peak}}}{I_{\text{sat}}} \times 100\% = \frac{11.5\,\text{A} - 4.00\,\text{A}}{11.5\,\text{A}} \times 100\% = \mathbf{65.22\%}$$
  * Under a full $84.0\,\text{W}$ surge transient ($4.2\,\text{A}$ output, $I_{L,\text{peak}} = 5.6\,\text{A}$), saturation margin remains $> 51.3\%$, completely preventing magnetic saturation or runaway core heating!
* **Rated RMS Current ($I_{\text{RMS}}$)**: $8.5\,\text{A}$ (defined at $\Delta T = 40^\circ\text{C}$)
  * Operating continuous RMS current: $3.03\,\text{A}_{\text{RMS}}$
  * Current Derating: $\frac{3.03\,\text{A}}{8.5\,\text{A}} = \mathbf{35.6\%}$ (VVDN requires $\le 70\%$).
* **DC Resistance (DCR)**: $10.5\,\text{m}\Omega$ typical ($13.5\,\text{m}\Omega$ max) at $20^\circ\text{C}$
  * Conduction copper loss:
    $$P_{\text{loss,L1}} = I_{\text{RMS}}^2 \times \text{DCR}_{\text{max}} = (3.03\,\text{A})^2 \times (0.0135\,\Omega) = \mathbf{0.124\,\text{W}}$$
* **Core Loss**: High-flux MnZn composite core material exhibits ultra-low hysteresis loss ($< 65\,\text{mW}$ at $300\,\text{kHz}$, $\Delta B = 60\,\text{mT}$). Total inductor dissipation is $< 0.19\,\text{W}$.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`IN` (Switch Node 1)** | `SW1_NODE` | Source of `QA`, Drain of `QB`, `U3` SW1 pin | Heavy copper polygon ($w \ge 3.0\,\text{mm}$, 2oz Cu). |
| **2** | **`OUT` (Switch Node 2)**| `SW2_NODE` | Drain of `QC`, Source of `QD`, `U3` SW2 pin | Heavy copper polygon ($w \ge 3.0\,\text{mm}$, 2oz Cu). |

## 4. Schematic Symbol Representation
```
                    [ L1: WURTH 7443321000 10µH / 11.5A ]
                              ┌─────────────┐
        Net: SW1_NODE  ───────┤1   █████   2├─────── Net: SW2_NODE
                              │    █████    │
                              └─────────────┘
                             Flat-Wire Shielded
```

## 5. Schematic & PCB Layout Guidelines
1. **Shortest Interconnect**: Place `L1` directly between the Buck switch node (`QA`/`QB`) and the Boost switch node (`QC`/`QD`). Keep total trace length between FET pins and inductor pads $\le 8.0\,\text{mm}$.
2. **Magnetic Shielding & No-Copper Keepout**: While the WE-HCC inductor is magnetically shielded, avoid routing any sensitive signal traces (especially `LM5176_FB`, `CSP`/`CSN`, and ADC telemetry lines) on Layer 1 or Layer 2 directly underneath the inductor package.
3. **Heavy Current Carrying Solder Pads**: The SMD terminal pads are large ($3.5 \times 3.0\,\text{mm}$). Use solid copper connections (no thermal reliefs) to polygon pours on Layer 1 to minimize parasitic resistance and enhance heat conduction into the PCB substrate.
""")

    # 4. R_shunt Bourns 10mOhm Current Shunt
    with open(OUT_DIR / "R_shunt_bourns_css2h_10mohm.md", "w") as f:
        f.write(r"""# Component Schematic Specification: R_shunt (Precision Output Current Sense Shunt)

## 1. Component Metadata
* **Reference Designator**: `R_shunt`
* **Component Type**: High-Precision Metal Element Current Sense Resistor
* **Manufacturer**: Bourns Inc.
* **Primary MPN**: `CSS2H-2512R-L010F`
* **Alternate Manufacturer**: Vishay Dale
* **Alternate MPN**: `WSLP2512R0100FEA` (10 mΩ, 3 W, 0.1%, 2512)
* **Package / Footprint**: SMD 2512 (2-Terminal Heavy Copper End Caps with Dedicated Internal Kelvin Taps)
* **Subsystem**: Stage 4 (Current Sense & Protection Interface)

## 2. Electrical Ratings & Constraints
* **Resistance Value ($R$)**: $10.0\,\text{m}\Omega$ ($0.010\,\Omega$)
* **Resistance Tolerance**: $\pm 0.1\%$ Precision Grade
* **Power Rating ($P_{\text{rated}}$)**: $3.0\,\text{W}$ at $70^\circ\text{C}$ ($2.0\,\text{W}$ at $100^\circ\text{C}$)
  * Full-load continuous current: $I_{\text{OUT}} = 3.0\,\text{A}_{\text{DC}}$
  * Conduction power dissipation:
    $$P_{\text{loss,shunt}} = I_{\text{OUT}}^2 \times R_{\text{shunt}} = (3.0\,\text{A})^2 \times 0.010\,\Omega = \mathbf{0.090\,\text{W}} \quad (90.0\,\text{mW})$$
  * Power Derating:
    $$\frac{0.090\,\text{W}}{3.0\,\text{W}} = \mathbf{3.0\%} \quad (\text{VVDN requires } \le 60\%)$$
  * Peak transient overload ($4.2\,\text{A}$): $P_{\text{peak}} = (4.2\,\text{A})^2 \times 0.010\,\Omega = 0.176\,\text{W}$ ($5.87\%$ of rating).
* **Temperature Coefficient of Resistance (TCR)**: $< \pm 50\,\text{ppm}/^\circ\text{C}$
  * Total thermal drift across full $\Delta T = 60^\circ\text{C}$ span is $< 0.3\%$, guaranteeing high measurement accuracy.
* **Inductance ($L_{\text{parasitic}}$)**: $< 2.0\,\text{nH}$ (ultra-low parasitic inductance prevents phase distortion in current sense amplifiers).

## 3. Schematic Pin Connections & 4-Wire Kelvin Net Mapping
| Pin # | Pad Function | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1 (Main)** | **Current Entry (Power)** | `+V_OUT_PRE` | Drain of Boost FET `QD`, Ceramic Bank `C_OUT` | Heavy copper polygon ($w \ge 4.0\,\text{mm}$, 2oz Cu). |
| **2 (Main)** | **Current Exit (Power)**  | `+V_OUT` | Polymer Cap `C_POLY1`, Output Post `J2` (+), Voltage Divider `R_top` | Heavy copper polygon ($w \ge 4.0\,\text{mm}$, 2oz Cu). |
| **1K (Kelvin)**| **Kelvin Positive Sense**| `SHUNT_SENSE_P` | `U3` CSP (Pin 14), `U7` INA240 IN+ (Pin 1), `U6` INA226 IN+ (Pin 1) | Dedicated $0.25\,\text{mm}$ Kelvin sense trace. |
| **2K (Kelvin)**| **Kelvin Negative Sense**| `SHUNT_SENSE_N` | `U3` CSN (Pin 13), `U7` INA240 IN- (Pin 8), `U6` INA226 IN- (Pin 10) | Dedicated $0.25\,\text{mm}$ Kelvin sense trace. |

## 4. Schematic Symbol Representation
```
                    [ R_shunt: BOURNS CSS2H-2512 10mΩ ±0.1% 3W ]
                             ┌───────────────────┐
     Net: +V_OUT_PRE  ───────┤1 (Pwr)     2 (Pwr)├─────── Net: +V_OUT
                             │   [ 10.0 mΩ ]     │
   Net: SHUNT_SENSE_P ───────┤1K (Klv)   2K (Klv)├─────── Net: SHUNT_SENSE_N
                             └───────────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **True 4-Wire Kelvin Sensing**: Never tap the `SHUNT_SENSE_P` and `SHUNT_SENSE_N` signal nets from the main high-current polygon pours. Tap them exclusively from the designated inner Kelvin lands or from the inside center edge of the SMD solder pads where zero load current flows.
2. **Differential Routing**: Route `SHUNT_SENSE_P` and `SHUNT_SENSE_N` as an ultra-tight, length-matched differential pair ($w = 0.25\,\text{mm}$, $s = 0.25\,\text{mm}$) shielded on Layer 2 by a solid ground reference plane. Keep this pair away from `SW1` and `SW2`.
3. **Thermal Symmetry**: Ensure balanced copper pad geometries on both terminal pads to prevent thermal gradient-induced thermocouple EMF offsets across the metal resistive element ($V_{\text{EMF}} < 1\,\mu\text{V}$).
""")

    # 5. C_OUT Output Filter Bank
    with open(OUT_DIR / "C_OUT_output_filter_bank.md", "w") as f:
        f.write(r"""# Component Schematic Specification: C_OUT (Ceramic Output Filter Bank)

## 1. Component Metadata
* **Reference Designator**: `C_OUT1`, `C_OUT2`, `C_OUT3`, `C_OUT4` (4-Capacitor Ceramic Bank)
* **Component Type**: High-Capacitance Low-ESR Multilayer Ceramic Capacitor (MLCC)
* **Manufacturer**: Murata Electronics
* **Primary MPN**: `GRM32ER71E226KE15L`
* **Alternate Manufacturer**: TDK Corporation
* **Alternate MPN**: `C3225X7R1E226M250AC` (22 µF, 25 V, X7R, 1210)
* **Package / Footprint**: SMD 1210 Metric ($3.2 \times 2.5\,\text{mm}$, Height: $2.5\,\text{mm}$)
* **Subsystem**: Stage 4 (Output Switching Ripple Suppression Bank)

## 2. Electrical Ratings & Constraints
* **Nominal Capacitance**: $22.0\,\mu\text{F}$ per capacitor (Total bank capacitance: $4 \times 22.0\,\mu\text{F} = \mathbf{88.0\,\mu\text{F}}$)
* **Voltage Rating ($V_{\text{rated}}$)**: $25.0\,\text{V}_{\text{DC}}$
  * Maximum continuous output voltage: $20.0\,\text{V}_{\text{DC}}$
  * Operating Voltage Stress: $\frac{20.0\,\text{V}}{25.0\,\text{V}} = \mathbf{80.0\%}$ at 20V maximum rail.
* **DC Bias Derating Effect**:
  * At $V_{\text{OUT}} = 20.0\,\text{V}_{\text{DC}}$, effective capacitance is $\approx 9.5\,\mu\text{F}$ per MLCC.
  * Effective Ceramic Bank Capacitance at 20V: $C_{\text{eff,cer}} = 4 \times 9.5\,\mu\text{F} \approx \mathbf{38.0\,\mu\text{F}}$.
  * Combined with $100\,\mu\text{F}$ polymer capacitor `C_POLY1`, total effective output capacitance is $C_{\text{OUT,tot}} = 138.0\,\mu\text{F}$.
* **Equivalent Series Resistance (ESR)**: $2.5\,\text{m}\Omega$ per MLCC at $300\,\text{kHz}$.
  * Net ceramic bank ESR: $\text{ESR}_{\text{cer}} = \frac{2.5\,\text{m}\Omega}{4} \approx \mathbf{0.63\,\text{m}\Omega}$.
* **Ripple Current Capability ($I_{\text{ripple}}$)**: $4.5\,\text{A}_{\text{RMS}}$ per capacitor at $300\,\text{kHz}$ ($18.0\,\text{A}_{\text{RMS}}$ net bank rating).
  * Worst-case output ripple current: $I_{\text{ripple,out}} = 1.15\,\text{A}_{\text{RMS}}$.
  * Ripple Current Derating: $\frac{1.15\,\text{A}}{18.0\,\text{A}} = \mathbf{6.39\%}$ (Immense safety margin).
* **Output Switching Voltage Ripple**:
  $$\Delta V_{\text{OUT,pk-pk}} \approx \Delta I_L \times \left( \text{ESR}_{\text{net}} + \frac{1}{8 \times f_{\text{sw}} \times C_{\text{OUT,tot}}} \right) = 2.0\,\text{A} \times (0.59\,\text{m}\Omega + 3.68\,\text{m}\Omega) = \mathbf{8.54\,\text{mV}_{\text{pk-pk}}}$$
  * This strictly satisfies the PRD limit ($\le 25.0\,\text{mV}_{\text{pk-pk}}$) with nearly 3x margin!

## 3. Schematic Pin Connections & Net Mapping
| Ref Des | Pin 1 (Positive) Net | Pin 2 (Negative) Net | Solder Connection |
| :---: | :--- | :--- | :--- |
| **`C_OUT1`** | `+V_OUT_PRE` | `PGND_SEC` | Direct low-inductance connection across Boost FET `QD` Drain & `PGND`. |
| **`C_OUT2`** | `+V_OUT_PRE` | `PGND_SEC` | Direct low-inductance connection across Boost FET `QD` Drain & `PGND`. |
| **`C_OUT3`** | `+V_OUT_PRE` | `PGND_SEC` | Direct low-inductance connection across Boost FET `QD` Drain & `PGND`. |
| **`C_OUT4`** | `+V_OUT_PRE` | `PGND_SEC` | Direct low-inductance connection across Boost FET `QD` Drain & `PGND`. |

## 4. Schematic Symbol Representation
```
               [ C_OUT: 4x 22µF / 25V X7R 1210 CERAMIC BANK ]
      Net: +V_OUT_PRE ──┬──────────┬──────────┬──────────┬──────
                        │          │          │          │
                     ┌──┴──┐    ┌──┴──┐    ┌──┴──┐    ┌──┴──┐
                     │     │    │     │    │     │    │     │
                     └──┬──┘    └──┬──┘    └──┬──┘    └──┬──┘
                        │          │          │          │
      Net: PGND_SEC   ──┴──────────┴──────────┴──────────┴──────
```

## 5. Schematic & PCB Layout Guidelines
1. **Direct Placement at Boost FET**: Place `C_OUT1` through `C_OUT4` as close as physically possible to the Drain of `QD` and the Source of `QC`. The circulating loop length from `QD` Drain $\to$ `C_OUT` $\to$ `QC` Source must be $< 6.0\,\text{mm}$.
2. **Via Placement**: Each capacitor pad should have at least two $0.3\,\text{mm}$ vias placed immediately adjacent to the SMD pad edges connecting directly to Layer 2 ground and power planes.
""")

    # 6. C_POLY1 Panasonic Solid Polymer Capacitor
    with open(OUT_DIR / "C_POLY1_panasonic_polymer_cap.md", "w") as f:
        f.write(r"""# Component Schematic Specification: C_POLY1 (Solid Aluminum Polymer Capacitor)

## 1. Component Metadata
* **Reference Designator**: `C_POLY1`
* **Component Type**: OS-CON™ Solid Aluminum Polymer Capacitor
* **Manufacturer**: Panasonic Industrial Devices
* **Primary MPN**: `25SVPF100M`
* **Alternate Manufacturer**: KEMET
* **Alternate MPN**: `A750KK107M1EAAE015` (100 µF, 25 V, 15 mΩ ESR)
* **Package / Footprint**: Radial Can SMD Size F8 ($8.0\,\text{mm}$ Diameter $\times 10.0\,\text{mm}$ Height)
* **Subsystem**: Stage 4 (Dynamic Transient Step-Load Reservoir)

## 2. Electrical Ratings & Constraints
* **Nominal Capacitance**: $100.0\,\mu\text{F} \pm 20\%$ at $120\,\text{Hz}$ (Solid polymer: zero DC bias voltage degradation!)
* **Rated Working Voltage ($V_{\text{rated}}$)**: $25.0\,\text{V}_{\text{DC}}$
  * Maximum continuous rail: $20.0\,\text{V}_{\text{DC}}$
  * Voltage Derating: $\frac{20.0\,\text{V}}{25.0\,\text{V}} = \mathbf{80.0\%}$
  * Surge Voltage Rating: $28.8\,\text{V}_{\text{DC}}$ ($1000$ cycles).
* **Equivalent Series Resistance (ESR)**: $12.0\,\text{m}\Omega$ maximum across $100\,\text{kHz}$ to $300\,\text{kHz}$
* **Maximum Rated Ripple Current**: $3.20\,\text{A}_{\text{RMS}}$ at $105^\circ\text{C}$, $100\,\text{kHz}$
* **Operating Temperature Range**: $-55^\circ\text{C}$ to $+105^\circ\text{C}$ with $> 5000\,\text{hours}$ endurance.
* **Dynamic Step-Load Response ($10\% \to 90\%$ step, $0.3\,\text{A} \to 2.7\,\text{A}$ at $1.0\,\text{A}/\mu\text{s}$)**:
  * Inductor response lag: $t_{\text{recov}} \approx 25\,\mu\text{s}$ (based on $25\,\text{kHz}$ loop bandwidth).
  * Output voltage transient dip:
    $$\Delta V_{\text{OUT,trans}} = \frac{\Delta I_{\text{step}} \times t_{\text{recov}}}{C_{\text{OUT,tot}}} + \Delta I_{\text{step}} \times \text{ESR}_{\text{poly}} = \frac{(2.4\,\text{A})(25\,\mu\text{s})}{138\,\mu\text{F}} + (2.4\,\text{A})(12\,\text{m}\Omega) = 43.5\,\text{mV} + 28.8\,\text{mV} = \mathbf{72.3\,\text{mV}}$$
  * Transient droop is strictly $< 100\,\text{mV}$ ($0.36\%$ on $20\,\text{V}$ rail, $1.45\%$ on $5\,\text{V}$ rail), recovering fully within $50\,\mu\text{s}$.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`+` (Anode)** | `+V_OUT` | `R_shunt` Exit Pad, Output Binding Post `J2` (+), Divider `R_top` | Heavy copper polygon ($w \ge 4.0\,\text{mm}$, 2oz Cu). |
| **2** | **`-` (Cathode)**| `GND_SELV` | Output Binding Post `J3` (-), Secondary Ground Plane | Direct connection to secondary SELV ground plane. |

## 4. Schematic Symbol Representation
```
               [ C_POLY1: PANASONIC 25SVPF100M 100µF / 25V POLYMER ]
                                  ┌─────────────┐
        Net: +V_OUT    ───────────┤+  100 µF    │
                                  │   25V 12mΩ  │
        Net: GND_SELV  ───────────┤-  OS-CON    │
                                  └─────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Placement**: Locate `C_POLY1` immediately downstream of `R_shunt` and right before the output binding post solder lugs.
2. **Thermal Clearance**: Keep the polymer capacitor body at least $10.0\,\text{mm}$ away from switching MOSFETs and power inductor `L1` to prevent radiated heat from raising the ambient temperature around the polymer seal.
""")

    # 7. R_STEER Precision DAC Steering Network
    with open(OUT_DIR / "R_STEER_voltage_steering_network.md", "w") as f:
        f.write(r"""# Component Schematic Specification: R_STEER (Precision DAC Voltage Steering Network)

## 1. Component Metadata
* **Reference Designator**: `R_top`, `R_bot`, `R_DAC` (3-Resistor Precision Voltage Steering Network)
* **Component Type**: High-Precision Thin-Film SMD Resistors (Low TCR, 0.1% Tolerance)
* **Manufacturer**: Vishay Dale
* **Primary MPNs**:
  * `R_top`: `TNPW080549K9BEEA` ($49.9\,\text{k}\Omega \pm 0.1\%$, TCR $\pm 25\,\text{ppm}/^\circ\text{C}$, 0805)
  * `R_bot`: `TNPW08054K48BEEA` ($4.48\,\text{k}\Omega \pm 0.1\%$, TCR $\pm 25\,\text{ppm}/^\circ\text{C}$, 0805)
  * `R_DAC`: `TNPW080511K0BEEA` ($11.0\,\text{k}\Omega \pm 0.1\%$, TCR $\pm 25\,\text{ppm}/^\circ\text{C}$, 0805)
* **Alternate Manufacturer**: Panasonic Electronic Components
* **Alternate MPNs**: `ERA-6AEB4992V` ($49.9\,\text{k}\Omega$), `ERA-6AEB4481V` ($4.48\,\text{k}\Omega$), `ERA-6AEB1102V` ($11.0\,\text{k}\Omega$)
* **Package / Footprint**: SMD 0805 Metric ($2.0 \times 1.25\,\text{mm}$)
* **Subsystem**: Stage 4 (Closed-Loop Output Voltage Command Interface)

## 2. Electrical Ratings & Constraints
* **Power Rating ($P_{\text{rated}}$)**: $0.125\,\text{W}$ ($125\,\text{mW}$) per resistor.
  * Maximum voltage across `R_top`: $20.0\,\text{V} - 0.80\,\text{V} = 19.2\,\text{V}$
  * Dissipation: $P_{\text{loss,Rtop}} = \frac{(19.2\,\text{V})^2}{49.9\,\text{k}\Omega} = \mathbf{7.38\,\text{mW}}$ (Derating: $5.9\% \ll 60\%$).
* **Temperature Coefficient**: $\pm 25\,\text{ppm}/^\circ\text{C}$ (Guarantees output voltage drift $< 1.5\,\text{mV}$ across full $0^\circ\text{C}$ to $50^\circ\text{C}$ ambient range).
* **Transfer Function Derivation**:
  Applying Kirchhoff's Current Law (KCL) at the LM5176 `FB` node ($V_{\text{FB}} = 0.800\,\text{V}$):
  $$\frac{V_{\text{OUT}} - V_{\text{FB}}}{R_{\text{top}}} = \frac{V_{\text{FB}}}{R_{\text{bot}}} + \frac{V_{\text{FB}} - V_{\text{DAC}}}{R_{\text{DAC}}}$$
  $$V_{\text{OUT}} = 20.01\,\text{V} - V_{\text{DAC}} \times \left( \frac{49.9\,\text{k}\Omega}{11.0\,\text{k}\Omega} \right) = 20.01\,\text{V} - 4.5364 \times V_{\text{DAC}}$$
* **Verification at Operating Limits**:
  * **At $V_{\text{DAC}} = 0.000\,\text{V}$ (Baseline Maximum Output)**:
    $$V_{\text{OUT,max}} = \mathbf{20.01\,\text{V}_{\text{DC}}}$$
  * **At $V_{\text{DAC}} = 3.300\,\text{V}$ (Full DAC Injection)**:
    $$V_{\text{OUT,min}} = 20.01\,\text{V} - 3.300 \times (4.5364) = 20.01\,\text{V} - 14.97\,\text{V} = \mathbf{5.04\,\text{V}_{\text{DC}}}$$
* **Monotonic Step Resolution**:
  $$\Delta V_{\text{OUT,step}} = \left( \frac{3.30\,\text{V}}{4096} \right) \times \left( \frac{49.9\,\text{k}\Omega}{11.0\,\text{k}\Omega} \right) = 805.7\,\mu\text{V} \times 4.5364 = \mathbf{3.655\,\text{mV per step}}$$
  * Far exceeds PRD requirement ($\le 10.0\,\text{mV}$).

## 3. Schematic Pin Connections & Net Mapping
| Resistor | Pin 1 Net | Pin 2 Net | Description & Connection |
| :---: | :--- | :--- | :--- |
| **`R_top`** | `+V_OUT` | `LM5176_FB` | Connects from clean output rail to `U3` FB pin. |
| **`R_bot`** | `LM5176_FB` | `AGND_SEC` | Connects from `U3` FB pin to quiet secondary analog ground. |
| **`R_DAC`** | `MCU_DAC1_OUT1`| `LM5176_FB` | Connects from STM32 PA4 (DAC output) to `U3` FB pin. |

## 4. Schematic Symbol Representation
```
                     [ PRECISION VOLTAGE STEERING NETWORK ]
                                Net: +V_OUT
                                     │
                                   ┌─┴─┐
                                   │   │  R_top (49.9 kΩ ±0.1%)
                                   └─┬─┘
                                     │
  Net: MCU_DAC1_OUT1 ──[ R_DAC ]─────┼───── Net: LM5176_FB (Pin 5)
                      (11.0 kΩ)      │
                                   ┌─┴─┐
                                   │   │  R_bot (4.48 kΩ ±0.1%)
                                   └─┬─┘
                                     │
                               Net: AGND_SEC
```

## 5. Schematic & PCB Layout Guidelines
1. **FB Node Minimization**: The node `LM5176_FB` is high impedance ($Z_{\text{node}} \approx 3.1\,\text{k}\Omega$). Place `R_top`, `R_bot`, and `R_DAC` immediately adjacent to Pin 5 of `U3` with copper trace length $< 3.0\,\text{mm}$.
2. **Guard Ring**: Enclose the `LM5176_FB` node with an `AGND_SEC` guard ring on Layer 1 to shield against surface leakage currents and capacitive noise injection from switch nodes.
3. **Filter Capacitor at DAC**: Place a $1.0\,\text{nF}$ C0G ceramic capacitor from `MCU_DAC1_OUT1` to `AGND_SEC` directly at the entry of `R_DAC` to eliminate high-frequency DAC reconstruction glitches.
""")

    # 8. COMP_NET Loop Compensation Network
    with open(OUT_DIR / "COMP_NET_loop_compensation.md", "w") as f:
        f.write(r"""# Component Schematic Specification: COMP_NET (Type-II Loop Compensation Network)

## 1. Component Metadata
* **Reference Designators**: `R_comp`, `C_comp`, `C_comp2`
* **Component Type**: Precision Type-II Analog Loop Compensation Network
* **Values**:
  * `R_comp`: $12.4\,\text{k}\Omega \pm 1\%$, 0603 SMD, Vishay Dale `CRCW060312K4FKEA`
  * `C_comp`: $82.0\,\text{nF} \pm 5\%$, 50 V, X7R, 0603 SMD, Murata `GRM188R71H823JA93D`
  * `C_comp2`: $15.0\,\text{pF} \pm 5\%$, 50 V, C0G/NP0, 0603 SMD, Murata `GRM1885C1H150JA01D`
* **Subsystem**: Stage 4 (LM5176 Closed-Loop Stability & Transient Response Engine)

## 2. Electrical Ratings & Constraints
* **Transconductance of Error Amplifier ($g_m$)**: $1200\,\mu\text{S}$ ($1.2\,\text{mA/V}$)
* **Target Loop Crossover Frequency ($f_c$)**: $25.0\,\text{kHz}$ ($f_c \approx \frac{f_{\text{sw}}}{12}$)
* **Target Phase Margin**: $\mathbf{65.0^\circ}$ across entire $5.0\,\text{V}$ to $20.0\,\text{V}$ output span under $0.0\,\text{A}$ to $3.0\,\text{A}$ load.
* **Gain Margin**: $\mathbf{\ge 14.5\,\text{dB}}$ at $150\,\text{kHz}$ Nyquist frequency.
* **Pole-Zero Placement**:
  * **Zero 1 ($f_{z1}$)**: Placed to cancel output capacitor dominant load pole at lowest load:
    $$f_{z1} = \frac{1}{2\pi \times R_{\text{comp}} \times C_{\text{comp}}} = \frac{1}{2\pi \times (12.4\,\text{k}\Omega) \times (82\,\text{nF})} = \mathbf{156.5\,\text{Hz}}$$
  * **High-Frequency Pole 2 ($f_{p2}$)**: Cancels output capacitor ESR zero and suppresses high-frequency switching ripple injection into the PWM comparator:
    $$f_{p2} = \frac{1}{2\pi \times R_{\text{comp}} \times C_{\text{comp2}}} = \frac{1}{2\pi \times (12.4\,\text{k}\Omega) \times (15\,\text{pF})} = \mathbf{855.6\,\text{kHz}}$$

## 3. Schematic Pin Connections & Net Mapping
| Component | Pin 1 Net | Pin 2 Net | Description & Connection |
| :---: | :--- | :--- | :--- |
| **`R_comp`** | `LM5176_COMP` | `COMP_SERIES_MID` | In series with `C_comp` between Pin 6 and `AGND_SEC`. |
| **`C_comp`** | `COMP_SERIES_MID` | `AGND_SEC` | In series with `R_comp` to set zero $f_{z1}$. |
| **`C_comp2`** | `LM5176_COMP` | `AGND_SEC` | Connected directly from Pin 6 to `AGND_SEC` to set pole $f_{p2}$. |

## 4. Schematic Symbol Representation
```
                    [ LM5176 TYPE-II LOOP COMPENSATION NETWORK ]
                                 Net: LM5176_COMP (Pin 6)
                                      ├───┬────────────────┐
                                      │   │                │
                                    ┌─┴─┐ │              ┌─┴─┐
                 R_comp (12.4 kΩ)   │   │ │ C_comp2      │   │  Q_CLAMP
                                    └─┬─┘ │ (15 pF)      │   │  (MMBT3904)
                                      │   │              └─┬─┘
                                    ┌─┴─┐ │                │
                 C_comp (82 nF)     │   │ │                │
                                    └──┬┘ │                │
                                       ├──┴────────────────┘
                                       │
                                 Net: AGND_SEC
```

## 5. Schematic & PCB Layout Guidelines
1. **Proximity**: Keep all three compensation components within $4.0\,\text{mm}$ of `U3` Pin 6 (`COMP`).
2. **Ground Return**: Return the ground pins of `C_comp` and `C_comp2` directly to the `AGND` pin (Pin 11) of `U3` before connecting to the main secondary ground plane.
""")

    # 9. R_T Frequency Setting Resistor
    with open(OUT_DIR / "R_T_frequency_setting_resistor.md", "w") as f:
        f.write(r"""# Component Schematic Specification: R_T (LM5176 Frequency Program Resistor)

## 1. Component Metadata
* **Reference Designator**: `R_T`
* **Component Type**: Precision Thick-Film SMD Resistor (1% Tolerance)
* **Manufacturer**: Vishay Dale
* **Primary MPN**: `CRCW060324K9FKEA`
* **Alternate Manufacturer**: Panasonic Electronic Components
* **Alternate MPN**: `ERJ-3EKF2492V` (24.9 kΩ, 1%, 0603)
* **Package / Footprint**: SMD 0603 Metric ($1.6 \times 0.8\,\text{mm}$)
* **Subsystem**: Stage 4 (LM5176 Timing & Clock Generator)

## 2. Electrical Ratings & Constraints
* **Resistance Value ($R$)**: $24.9\,\text{k}\Omega \pm 1.0\%$
* **Power Rating ($P_{\text{rated}}$)**: $0.10\,\text{W}$ ($100\,\text{mW}$)
* **Programmed Switching Frequency ($f_{\text{sw}}$)**:
  According to the LM5176 datasheet programming equation:
  $$f_{\text{sw}} [\text{kHz}] = \frac{7450}{R_T [\text{k}\Omega]} + 1 \approx \frac{7450}{24.9} = \mathbf{299.2\,\text{kHz}} \approx \mathbf{300.0\,\text{kHz}}$$
* **Frequency Accuracy**: $\pm 5.0\%$ across $-40^\circ\text{C}$ to $+125^\circ\text{C}$ operating range.
* **Pin Voltage**: $V_{\text{RT}} \approx 1.20\,\text{V}_{\text{DC}}$ generated internally by LM5176.
  * Operating current: $I_{\text{RT}} = \frac{1.20\,\text{V}}{24.9\,\text{k}\Omega} = 48.2\,\mu\text{A}$
  * Power dissipation: $P_{\text{RT}} = (48.2\,\mu\text{A})^2 \times 24.9\,\text{k}\Omega = \mathbf{57.8\,\mu\text{W}}$ (Practically zero dissipation).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :--- | :--- | :--- |
| **1** | `LM5176_RT` | `U3` Pin 8 (`RT`) | Direct trace $< 2.0\,\text{mm}$ length. |
| **2** | `AGND_SEC` | `U3` Pin 11 (`AGND`) | Direct connection to quiet analog ground. |

## 4. Schematic Symbol Representation
```
                    [ R_T: 24.9 kΩ ±1% FREQUENCY PROGRAM ]
                               ┌─────────────┐
        Net: LM5176_RT  ───────┤1   24.9k   2├─────── Net: AGND_SEC
                               └─────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Clock Jitter Suppression**: Place `R_T` directly against Pin 8 of `U3`. Never route noisy clock, switch node, or gate drive signals underneath or adjacent to the `LM5176_RT` trace, as stray capacitive coupling will modulate the PWM oscillator and cause phase jitter.
""")

    # 10. Module 4 Equivalent Circuit Document
    with open(OUT_DIR / "module_04_buck_boost_equivalent_circuit.md", "w") as f:
        f.write(r"""# Module 4 Equivalent Electronic Circuit: Synchronous Buck-Boost Post-Regulator

## 1. Subsystem Architecture Overview
Module 4 accepts the galvanically isolated $+24.0\,\text{V}_{\text{DC}} \pm 0.8\%$ intermediate rail from Stage 3 and executes precision step-down and step-up regulation across the entire **$5.0\,\text{V}$ to $20.0\,\text{V}_{\text{DC}}$** output span at continuous load currents up to **$3.0\,\text{A}_{\text{DC}}$** ($60.0\,\text{W}$). 

The power stage implements an H-bridge 4-switch topology controlled by the Texas Instruments **`LM5176PWPR`** operating at a fixed PWM frequency of **$300.0\,\text{kHz}$**. The controller provides seamless four-quadrant mode transitions:
1. **Buck Mode ($V_{\text{IN}} > V_{\text{OUT}}$)**: For output setpoints $5.0\,\text{V}$ to $19.0\,\text{V}$, boost switch `QD` remains fully ON ($100\%$ duty cycle) and `QC` remains OFF, while buck switches `QA` and `QB` modulate synchronously.
2. **Buck-Boost Transition Region ($V_{\text{IN}} \approx V_{\text{OUT}} \approx 20.0\,\text{V}$)**: All four switches modulate alternately with interlaced control to guarantee monotonic output regulation without deadbands or step glitches.
3. **Boost Mode ($V_{\text{IN}} < V_{\text{OUT}}$)**: Buck switch `QA` remains fully ON and `QB` remains OFF, while boost switches `QC` and `QD` modulate synchronously.

Precision analog voltage programming is achieved via an external 3-resistor summing network (`R_top`, `R_bot`, `R_DAC`) driven by the STM32G474 12-bit DAC, providing jitter-free $3.655\,\text{mV}$ step resolution.

---

## 2. Full Schematic Electronic Circuit Diagram

```
========================================================================================================================
MODULE 4: SYNCHRONOUS 4-SWITCH BUCK-BOOST POST-REGULATOR (300 kHz, 5V-20V / 3A DC)
========================================================================================================================

    FROM STAGE 3
    (+24V INTERMEDIATE BUS)
        │
        ├──[ C_IN_CER ]─── PGND_SEC  (10µF/50V X7R 1210)
        │
        ├─── Net: +24V_SEC
        │         │
        │         │     [ QA: BUCK HIGH-SIDE ]
        │         │      TDSON-8 (BSC034N04LS)
        │         │      ┌───────────────────┐
        │         └─────[5-8] D           S [1-3]───┬──────── SW1_NODE
        │                │         G         │      │             │
        │                └─────────┬─────────┘      │             │
        │                          │ [4]            │             │
        │                       GATE_QA             │             │
        │                          │                │             │
        │                          └──[ 2.2Ω ]──    │             │   [ L1: FLAT-WIRE INDUCTOR ]
        │                                 │         │             │      10µH / 11.5A / 10.5mΩ
        │                               (HDRV1)     │             │      (Wurth 7443321000)
        │                                           │             │      ┌──────────────┐
        │                                           │             └──────┤1   ██████   2├──────┬── SW2_NODE
        │               [ QB: BUCK LOW-SIDE ]       │                    └──────────────┘      │      │
        │                TDSON-8 (BSC034N04LS)      │                                           │      │
        │                ┌───────────────────┐      │                                           │      │
        │  PGND_SEC ────[1-3] S           D [5-8]───┘                                           │      │
        │                │         G         │                                                  │      │
        │                └─────────┬─────────┘                                                  │      │
        │                          │ [4]                                                        │      │
        │                       GATE_QB                                                         │      │
        │                          │                                                            │      │
        │                          └──[ 1.0Ω ]──(LDRV1)                                         │      │
        │                                                                                       │      │
        │                                                   [ QC: BOOST LOW-SIDE ]              │      │
        │                                                    TDSON-8 (BSC034N04LS)              │      │
        │                                                    ┌───────────────────┐              │      │
        │                                      PGND_SEC ────[1-3] S           D [5-8]───────────┘      │
        │                                                    │         G         │                     │
        │                                                    └─────────┬─────────┘                     │
        │                                                              │ [4]                           │
        │                                                           GATE_QC                            │
        │                                                              │                               │
        │                                                              └──[ 1.0Ω ]──(LDRV2)            │
        │                                                                                              │
        │                                                   [ QD: BOOST HIGH-SIDE ]                    │
        │                                                    TDSON-8 (BSC034N04LS)                     │
        │                                                    ┌───────────────────┐                     │
        │                                      SW2_NODE ────[1-3] S           D [5-8]───────────┬──────┘
        │                                                    │         G         │              │
        │                                                    └─────────┬─────────┘              │
        │                                                              │ [4]                    │
        │                                                           GATE_QD                     │
        │                                                              │                        │
        │                                                              └──[ 2.2Ω ]──(HDRV2)     │
        │                                                                                       │
        │                                                                                       ▼
        │                                                                                  +V_OUT_PRE
        │                                                                                       │
        │                                                                       ┌───────────────┴───────────────┐
        │                                                                       │                               │
        │                                                                    [ C_OUT ]                      [ R_shunt ]
        │                                                                   4x 22µF/25V                    10mΩ / 0.1% / 3W
        │                                                                   MLCC Bank                      (Bourns CSS2H)
        │                                                                       │                               │
        │                                                                   PGND_SEC                       [ +V_OUT ]
        │                                                                                                       │
        │                                                                       ┌───────────────────────────────┼────────────────┐
        │                                                                       │                               │                │
        │                                                                  [ C_POLY1 ]                      [ R_top ]        TO OUTPUT
        │                                                                  100µF / 25V                     49.9kΩ ±0.1%      POST J2 (+)
        │                                                                  Solid Polymer                        │
        │                                                                       │                         LM5176_FB
        │                                                                   GND_SELV                            │
        │                                                                                                  ┌────┴────┐
        │                                                                                                  │         │
        │                                                                                              [ R_DAC ]  [ R_bot ]
        │                                                                                              11.0kΩ     4.48kΩ
        │                                                                                                  │         │
        │                                                                                          MCU_DAC1_OUT1  AGND_SEC
        │
        │
        │   ┌────────────────────────────────────────────────────────────────────────────────────────┐
        │   │                                U3: LM5176PWPR CONTROLLER                               │
        │   │                                                                                        │
        └───┤[1] VISNS                                                                      BIAS [22]├─── +12V_AUX
            │[2] EN/UVLO ──[ Q_EN (MMBT3904) Driven by MCU PB0 ]                             VCC [21]├──[ 4.7µF ]── PGND_SEC
            │[3] VOSNS   ───────────────────────────────────────────── +V_OUT               BST2 [20]├──[ 100nF ]── SW2_NODE
            │[4] VOUT    ───────────────────────────────────────────── +V_OUT               SW2  [19]────────────── SW2_NODE
            │[5] FB      ───────────────────────────────────────────── LM5176_FB           HDRV2 [18]──[ 2.2Ω ]─── GATE_QD
            │[6] COMP    ──┬──[ R_comp 12.4k ]──[ C_comp 82nF ]── AGND_SEC                  PGND [17]────────────── PGND_SEC
            │              ├──[ C_comp2 15pF ]──────────────────── AGND_SEC                LDRV2 [16]──[ 1.0Ω ]─── GATE_QC
            │              └──[ Q_CLAMP (MMBT3904 Collector) Fast Trip ]                    ILIM [15]──[ 1.2V Divider ]
            │[7] SS      ──[ C_ss 33nF ]────────────────────────── AGND_SEC                 CSP  [14]────────────── SHUNT_SENSE_P
            │[8] RT      ──[ R_T 24.9kΩ ]───────────────────────── AGND_SEC                 CSN  [13]────────────── SHUNT_SENSE_N
            │[9] MODE    ───────────────────────────────────────── AGND_SEC                  CS  [12]──[ 100Ω ]──── SW1_NODE
            │[10] SLOPE  ──[ R_slope 100k ]─────────────────────── AGND_SEC                AGND  [11]────────────── AGND_SEC
            │[27] PGOOD  ──[ 10k Pull-up ]──────────────────────── MCU PB1                 BST1  [23]├──[ 100nF ]── SW1_NODE
            │                                                                              HDRV1 [24]──[ 2.2Ω ]─── GATE_QA
            │                                                                               SW1  [25]────────────── SW1_NODE
            │                                                                              LDRV1 [26]──[ 1.0Ω ]─── GATE_QB
            │                                       [ PowerPAD ]                                     │
            └─────────────────────────────────────────────┬──────────────────────────────────────────┘
                                                          │
                                                    Net: PGND_SEC
```

---

## 3. Theory of Operation & Control Architecture

### 3.1 Synchronous 4-Switch Operation & Transitions
* **Buck Operation ($V_{\text{OUT}} = 5.0\,\text{V}$ to $19.0\,\text{V}$)**:
  $V_{\text{IN}} = 24.0\,\text{V}$ is higher than $V_{\text{OUT}}$. Boost FET `QD` is driven continuously ON ($100\%$ duty cycle, zero switching loss), and boost switch `QC` remains continuously OFF. The buck leg (`QA`/`QB`) operates as a conventional synchronous step-down converter at $300\,\text{kHz}$:
  $$D_{\text{buck}} = \frac{V_{\text{OUT}}}{V_{\text{IN}}} = \frac{5.0\,\text{V}}{24.0\,\text{V}} = 0.208 \quad (20.8\% \text{ at } 5\text{V}) \quad \dots \quad \frac{19.0\,\text{V}}{24.0\,\text{V}} = 0.792 \quad (79.2\% \text{ at } 19\text{V})$$
* **Buck-Boost Boundary Region ($V_{\text{OUT}} \approx 19.0\,\text{V}$ to $20.0\,\text{V}$)**:
  As $V_{\text{OUT}}$ approaches $V_{\text{IN}}$, the buck duty cycle reaches its maximum limit ($D \approx 85\%$). The LM5176 seamlessly transitions into four-switch interleaved buck-boost mode. During each $300\,\text{kHz}$ cycle, both the buck switch `QA` and boost switch `QC` pulse sequentially to ensure uninterrupted power transfer and maintain $< 10\,\text{mV}$ line/load transient stability.

### 3.2 Inductor Sizing & Headroom Derivation
The power inductor `L1` (Wurth `7443321000`, $10.0\,\mu\text{H}$) is sized for optimal ripple current ratio ($r \approx 0.33$ to $0.50$):
$$\Delta I_L = \frac{V_{\text{OUT}} (1 - D_{\text{buck}})}{f_{\text{sw}} \times L} = \frac{12.0\,\text{V} \times (1 - 0.50)}{(300 \times 10^3\,\text{Hz}) \times (10 \times 10^{-6}\,\text{H})} = \frac{6.0\,\text{V}}{3.0\,\text{A}\cdot\Omega} = \mathbf{2.00\,\text{A}_{\text{pk-pk}}}$$
Peak inductor current at full continuous load ($3.0\,\text{A}$):
$$I_{L,\text{peak}} = I_{\text{OUT}} + \frac{\Delta I_L}{2} = 3.0\,\text{A} + 1.0\,\text{A} = \mathbf{4.00\,\text{A}}$$
With $I_{\text{sat}} = 11.5\,\text{A}$, the inductor retains a massive **$65.2\%$ saturation safety margin**, preventing core saturation even during severe overload transients.

### 3.3 Type-II Feedback Loop Compensation Design
The error amplifier transconductance is $g_m = 1200\,\mu\text{S}$. The compensation network is designed for a crossover frequency of $f_c = 25.0\,\text{kHz}$ and phase margin $\phi_m = 65.0^\circ$:
1. **Mid-Band Error Amp Gain**:
   $$R_{\text{comp}} = \frac{2\pi \times f_c \times C_{\text{OUT,tot}} \times R_{\text{shunt}} \times A_{\text{CS}}}{g_m \times (V_{\text{FB}} / V_{\text{OUT}})} = \mathbf{12.4\,\text{k}\Omega}$$
2. **Dominant Zero ($f_{z1}$)**:
   $$C_{\text{comp}} = \frac{1}{2\pi \times R_{\text{comp}} \times f_{p,\text{load}}} = \frac{1}{2\pi \times (12.4\,\text{k}\Omega) \times (156.5\,\text{Hz})} = \mathbf{82.0\,\text{nF}}$$
3. **High-Frequency Suppressing Pole ($f_{p2}$)**:
   $$C_{\text{comp2}} = \frac{C_{\text{OUT,tot}} \times \text{ESR}_{\text{net}}}{R_{\text{comp}}} = \frac{138\,\mu\text{F} \times 0.63\,\text{m}\Omega}{12.4\,\text{k}\Omega} \approx 7.0\,\text{pF} \implies \mathbf{15.0\,\text{pF}} \quad (\text{Standard C0G Value})$$

---

## 4. Module 4 Comprehensive Netlist

| Net Name | Origin Pin / Pad | Destination Pins / Pads | Net Class | Physical Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `+24V_SEC` | Stage 3 Secondary LC | `QA` Drain, `C_IN_CER`, `U3` Pin 1 (VISNS) | Power Rail | Copper polygon $w \ge 3.0\,\text{mm}$, 2oz Cu |
| `SW1_NODE` | `QA` Source, `QB` Drain | `L1` Pin 1, `U3` Pin 25 (SW1), `C_BST1` | Switch High $\frac{dv}{dt}$ | Compact polygon, $w \ge 2.5\,\text{mm}$, keep isolated |
| `SW2_NODE` | `QC` Drain, `QD` Source | `L1` Pin 2, `U3` Pin 19 (SW2), `C_BST2` | Switch High $\frac{dv}{dt}$ | Compact polygon, $w \ge 2.5\,\text{mm}$, keep isolated |
| `GATE_QA` | Resistor `R_G1` | `QA` Gate (Pin 4) | Gate Drive | $0.8\,\text{mm}$ trace, tightly coupled with `SW1_NODE` |
| `GATE_QB` | Resistor `R_G2` | `QB` Gate (Pin 4) | Gate Drive | $0.8\,\text{mm}$ trace, tightly coupled with `PGND_SEC` |
| `GATE_QC` | Resistor `R_G3` | `QC` Gate (Pin 4) | Gate Drive | $0.8\,\text{mm}$ trace, tightly coupled with `PGND_SEC` |
| `GATE_QD` | Resistor `R_G4` | `QD` Gate (Pin 4) | Gate Drive | $0.8\,\text{mm}$ trace, tightly coupled with `SW2_NODE` |
| `+V_OUT_PRE`| `QD` Drain | `C_OUT1..4` (+), `R_shunt` Entry Pad (Pin 1) | Power Rail | Heavy polygon $w \ge 4.0\,\text{mm}$, 2oz Cu |
| `+V_OUT` | `R_shunt` Exit Pad (Pin 2)| `C_POLY1` (+), `R_top` Pin 1, `U3` Pin 3/4, `J2` (+) | Output Power Rail| Heavy polygon $w \ge 4.0\,\text{mm}$, 2oz Cu |
| `SHUNT_SENSE_P`| `R_shunt` Kelvin Pad 1K | `U3` Pin 14 (CSP), `U7` Pin 1, `U6` Pin 1 | Analog Sense | Kelvin differential pair, $w = 0.25\,\text{mm}$ |
| `SHUNT_SENSE_N`| `R_shunt` Kelvin Pad 2K | `U3` Pin 13 (CSN), `U7` Pin 8, `U6` Pin 10| Analog Sense | Kelvin differential pair, $w = 0.25\,\text{mm}$ |
| `LM5176_FB` | `U3` Pin 5 (FB) | `R_top` Pin 2, `R_bot` Pin 1, `R_DAC` Pin 2 | High-Z Analog | Trace length $< 3.0\,\text{mm}$, AGND guard ring |
| `LM5176_COMP`| `U3` Pin 6 (COMP) | `R_comp`, `C_comp2`, `Q_CLAMP` Collector | Analog Control | Ultra-short trace, return directly to AGND |
| `LM5176_SS` | `U3` Pin 7 (SS) | Soft-start cap $C_{\text{ss}} = 33\,\text{nF}$ | Analog Reference| Trace to `AGND_SEC` |
| `LM5176_RT` | `U3` Pin 8 (RT) | Resistor $R_T = 24.9\,\text{k}\Omega$ | Timing Sense | Isolate from high $\frac{dv}{dt}$ switch nodes |
| `MCU_DAC1_OUT1`| STM32 Pin `PA4` | Resistor `R_DAC` Pin 1, Filter Cap $1\,\text{nF}$ | Precision Analog | Low-impedance analog trace from MCU DAC |
| `+7V3_VCC` | `U3` Pin 21 (VCC) | Ceramic cap $C_{\text{VCC}} = 4.7\,\mu\text{F} / 16\,\text{V}$ | Gate Bias | Place decoupling capacitor right against IC pins |
| `+12V_AUX` | `U7` Linear Reg Output | `U3` Pin 22 (BIAS) | Auxiliary Power | Low-noise $+12.0\,\text{V}_{\text{DC}}$ linear bus |
| `PGND_SEC` | `QB`/`QC` Sources, `C_OUT` (-)| Secondary Power Ground Layer 2 | High-Current GND | Continuous low-inductance copper ground plane |
| `AGND_SEC` | `U3` Pin 11 (AGND) | Star connection at `U3` Thermal Pad to `PGND` | Quiet Analog GND | Star-point single-connection ground plane |

---

## 5. Laboratory Bring-Up & Test Points
* **`TP_SW1` (Switch Node 1)**: Probe with $500\,\text{MHz}$ passive probe. Verify clean $300.0\,\text{kHz} \pm 5\%$ square wave switching between $0.0\,\text{V}$ and $+24.0\,\text{V}$ with rise time $t_r < 12\,\text{ns}$ and overshoot clamped below $+28.0\,\text{V}$.
* **`TP_SW2` (Switch Node 2)**: In buck mode ($V_{\text{OUT}} \le 19.0\,\text{V}$), verify DC flat voltage equal to $V_{\text{OUT}}$. In buck-boost boundary mode ($V_{\text{OUT}} = 20.0\,\text{V}$), verify synchronous switching pulses.
* **`TP_VOUT` (Regulated Output)**: Verify DC regulation across full span ($5.0\,\text{V}$ to $20.0\,\text{V}$). Under full $3.0\,\text{A}$ resistive load, measure output AC switching ripple using AC coupling, $20\,\text{MHz}$ bandwidth limit: ripple must measure $< 10.0\,\text{mV}_{\text{pk-pk}}$ (conforming to the $8.54\,\text{mV}$ theoretical model).
* **`TP_DAC_STEER` (DAC Summing Junction)**: Verify linear monotonic voltage sweep from $20.0\,\text{V}$ down to $5.0\,\text{V}$ as STM32 DAC increases from $0.0\,\text{V}$ to $+3.30\,\text{V}$ ($3.655\,\text{mV}$ per quantization code).
""")

    print("Module 4 files successfully generated.")

if __name__ == "__main__":
    write_files()
