# Module 4 Equivalent Electronic Circuit: Synchronous Buck-Boost Post-Regulator

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
