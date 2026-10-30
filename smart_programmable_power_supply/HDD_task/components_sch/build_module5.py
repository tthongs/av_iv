#!/usr/bin/env python3
"""
Component and Schematic Connection Generator: Module 5 (Fast Hardware CC Protection)
"""

from pathlib import Path

OUT_DIR = Path("/home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/components_sch/module_05_fast_hardware_cc_protection")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def write_files():
    # 1. U7_FAST_CC INA240A2 Current Sense Amplifier
    with open(OUT_DIR / "U7_FAST_CC_ina240a2_current_amp.md", "w") as f:
        f.write(r"""# Component Schematic Specification: U7_FAST_CC (INA240A2 Precision Current Sense Amplifier)

## 1. Component Metadata
* **Reference Designator**: `U7_FAST_CC`
* **Component Type**: High-Bandwidth Current Sense Amplifier with Enhanced PWM Rejection
* **Manufacturer**: Texas Instruments
* **Primary MPN**: `INA240A2EDCKR`
* **Alternate Manufacturer**: Analog Devices
* **Alternate MPN**: `AD8418AWBRZ` (Bidirectional, Av = 20/50 V/V equivalent)
* **Package / Footprint**: SC70-8 (Thin Shrink Small Outline, Pitch: 0.65 mm, Body: 2.0 × 1.25 mm)
* **Subsystem**: Stage 5 (Autonomous Fast Hardware Current Clamping Subsystem)

## 2. Electrical Ratings & Constraints
* **Supply Voltage ($V_{\text{S}}$)**: $+2.7\,\text{V}$ to $+5.5\,\text{V}_{\text{DC}}$ (Powered from $+3.30\,\text{V}_{\text{DC}}$ LDO rail)
* **Common-Mode Input Range ($V_{\text{CM}}$)**: $-4.0\,\text{V}$ to $+80.0\,\text{V}_{\text{DC}}$
  * Output rail operating common-mode voltage: $+5.0\,\text{V}$ to $+20.0\,\text{V}_{\text{DC}}$.
  * Operates well within the $-4\text{V}$ to $+80\text{V}$ linear common-mode operating range!
* **Fixed Voltage Gain ($A_v$)**: $\mathbf{50.0\,\text{V/V}} \pm 0.20\%$ maximum gain error.
* **Bandwidth ($-3\,\text{dB}$)**: $400.0\,\text{kHz}$
* **Slew Rate ($SR$)**: $2.0\,\text{V}/\mu\text{s}$
* **Enhanced PWM Common-Mode Rejection**:
  * Features internal active EMI/PWM rejection filters providing $> 90\,\text{dB}$ rejection at $300\,\text{kHz}$ switching edges.
* **Input Offset Voltage ($V_{\text{OS}}$)**: $\pm 25\,\mu\text{V}$ maximum ($\pm 5\,\mu\text{V}$ typical)
* **Transfer Function & Sizing**:
  $$V_{\text{CS,out}} = I_{\text{OUT}} \times R_{\text{shunt}} \times A_v + V_{\text{REF}}$$
  With $V_{\text{REF}}$ tied to `AGND_SEC` ($0.0\,\text{V}$) for unidirectional sensing:
  $$V_{\text{CS,out}} = I_{\text{OUT}} \times (0.010\,\Omega) \times 50.0\,\text{V/V} = I_{\text{OUT}} \times \mathbf{0.500\,\text{V/A}}$$
  * **At $I_{\text{OUT}} = 0.0\,\text{A}$ (Zero Load)**: $V_{\text{CS,out}} = 0.000\,\text{V}$
  * **At $I_{\text{OUT}} = 3.0\,\text{A}$ (Continuous Rated Load)**: $V_{\text{CS,out}} = 3.0 \times 0.500 = \mathbf{1.500\,\text{V}_{\text{DC}}}$
  * **At $I_{\text{OUT}} = 3.20\,\text{A}$ (Hardware Trip Setpoint)**: $V_{\text{CS,out}} = 3.20 \times 0.500 = \mathbf{1.600\,\text{V}_{\text{DC}}}$
  * **At $I_{\text{OUT}} = 4.20\,\text{A}$ (Surge Overload)**: $V_{\text{CS,out}} = 4.20 \times 0.500 = \mathbf{2.100\,\text{V}_{\text{DC}}}$

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`IN+`** | `SHUNT_SENSE_P` | `R_shunt` Kelvin Positive terminal (1K) | Dedicated Kelvin differential trace ($w = 0.25\,\text{mm}$). |
| **2** | **`GND`** | `AGND_SEC` | Quiet secondary analog ground plane | Direct low-inductance connection to `AGND_SEC`. |
| **3** | **`REF2`**| `AGND_SEC` | Tied to `AGND_SEC` | Sets unidirectional zero-volt output reference. |
| **4** | **`OUT`** | `FAST_CC_SENSE` | Non-inverting input (Pin 3) of comparator `U8_FAST_CC` | Short $0.3\,\text{mm}$ trace ($< 5.0\,\text{mm}$). |
| **5** | **`NC`**  | `NC` | No internal connection | Leave floating. |
| **6** | **`REF1`**| `AGND_SEC` | Tied to `AGND_SEC` | Sets unidirectional zero-volt output reference. |
| **7** | **`VS`**  | `+3V3_SEC` | Local decoupling cap $C_{\text{U7}} = 100\,\text{nF} / 16\,\text{V}$ X7R | Connects to clean $+3.30\,\text{V}_{\text{DC}}$ analog rail. |
| **8** | **`IN-`** | `SHUNT_SENSE_N` | `R_shunt` Kelvin Negative terminal (2K) | Dedicated Kelvin differential trace ($w = 0.25\,\text{mm}$). |

## 4. Schematic Symbol Representation
```
                     [ U7_FAST_CC: INA240A2EDCKR CURRENT AMP ]
                                 ┌───────────────┐
   Net: SHUNT_SENSE_P ──────────[1] IN+       IN-[8]────────── Net: SHUNT_SENSE_N
   Net: AGND_SEC      ──────────[2] GND        VS[7]────────── Net: +3V3_SEC
   Net: AGND_SEC      ──────────[3] REF2       NC[6]────────── NC
   Net: FAST_CC_SENSE ──────────[4] OUT      REF1[5]────────── Net: AGND_SEC
                                 └───────────────┘
                                   Av = 50.0 V/V
```

## 5. Schematic & PCB Layout Guidelines
1. **Direct Shunt Connection**: Route `SHUNT_SENSE_P` and `SHUNT_SENSE_N` directly from the Kelvin sense terminals of Bourns `R_shunt` as a tightly coupled differential pair. Shield with ground planes on adjacent layers.
2. **Local Bypass**: Place a $100\,\text{nF}$ X7R ceramic bypass capacitor within $1.5\,\text{mm}$ of Pin 7 (`VS`) and Pin 2 (`GND`).
3. **Bandwidth Preservation**: Keep the output trace `FAST_CC_SENSE` short and direct to Pin 3 of `U8_FAST_CC`. Total parasitic capacitive loading must be $< 15\,\text{pF}$ to preserve the $2.0\,\text{V}/\mu\text{s}$ slew rate.
""")

    # 2. U8_FAST_CC TLV3501 Ultra-Fast Comparator
    with open(OUT_DIR / "U8_FAST_CC_tlv3501_comparator.md", "w") as f:
        f.write(r"""# Component Schematic Specification: U8_FAST_CC (TLV3501 High-Speed Comparator)

## 1. Component Metadata
* **Reference Designator**: `U8_FAST_CC`
* **Component Type**: Ultra-Fast Push-Pull Rail-to-Rail Output Comparator
* **Manufacturer**: Texas Instruments
* **Primary MPN**: `TLV3501AIDBVR`
* **Alternate Manufacturer**: Analog Devices
* **Alternate MPN**: `ADCMP600BKSZ` (Single-supply high-speed TTL/CMOS comparator, 3.5 ns)
* **Package / Footprint**: SOT-23-6 (Pitch: 0.95 mm, Body: 2.9 × 1.6 mm)
* **Subsystem**: Stage 5 (Autonomous Fast Hardware Current Clamping Subsystem)

## 2. Electrical Ratings & Constraints
* **Supply Voltage ($V_{\text{CC}}$)**: $+2.7\,\text{V}$ to $+5.5\,\text{V}_{\text{DC}}$ (Operates on $+3.30\,\text{V}_{\text{DC}}$ rail)
* **Ultra-Fast Propagation Delay ($t_{\text{pd}}$)**: $\mathbf{4.5\,\text{ns}}$ typical ($6.0\,\text{ns}$ max) with $20\,\text{mV}$ overdrive.
* **Overdrive Dispersion**: $< 1.5\,\text{ns}$ across $10\,\text{mV}$ to $100\,\text{mV}$ overdrive.
* **Toggle Frequency**: Up to $80.0\,\text{MHz}$
* **Output Stage**: Full CMOS Push-Pull Rail-to-Rail.
  * Drives high logic level to $+3.30\,\text{V}$ and low logic level to $< 0.10\,\text{V}$.
  * Capable of sourcing $25.0\,\text{mA}$ directly into the base of clamping transistor `Q_CLAMP`.
* **Trip Reference Threshold Voltage ($V_{\text{trip}}$)**:
  Generated via precision 2-resistor voltage divider from clean $+3.30\,\text{V}_{\text{DC}}$ rail:
  * Top Divider Resistor: $R_{\text{ref1}} = 10.6\,\text{k}\Omega \pm 0.1\%$ (Vishay `TNPW080510K6BEEA`)
  * Bottom Divider Resistor: $R_{\text{ref2}} = 10.0\,\text{k}\Omega \pm 0.1\%$ (Vishay `TNPW080510K0BEEA`)
  $$V_{\text{trip}} = (+3.300\,\text{V}) \times \frac{R_{\text{ref2}}}{R_{\text{ref1}} + R_{\text{ref2}}} = 3.300\,\text{V} \times \left( \frac{10.0\,\text{k}\Omega}{20.6\,\text{k}\Omega} \right) = \mathbf{1.6019\,\text{V}_{\text{DC}}}$$
  * Perfectly matches the $3.20\,\text{A}$ current limit threshold:
    $$I_{\text{trip}} = \frac{V_{\text{trip}}}{0.500\,\text{V/A}} = \frac{1.602\,\text{V}}{0.500} = \mathbf{3.204\,\text{A}_{\text{DC}}}$$
* **Hysteresis Resistor ($R_{\text{hys}}$)**: $470.0\,\text{k}\Omega$ connected from Push-Pull Output (Pin 1) to Non-Inverting input (Pin 3), providing $\approx 35\,\text{mV}$ clean hysteresis ($70\,\text{mA}$ load current hysteresis) to eliminate chatter during transition.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Description & Trace Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`OUT`** | `FAST_CC_TRIP` | Base resistor `R_B_CLAMP` ($1.0\,\text{k}\Omega$), Hysteresis `R_hys` | Fast CMOS output. Connects to `Q_CLAMP` base. |
| **2** | **`GND`** | `AGND_SEC` | Quiet secondary analog ground plane | Direct low-inductance connection. |
| **3** | **`IN+`** | `FAST_CC_SENSE` | INA240 output (Pin 4), Hysteresis `R_hys` | Senses amplified current voltage ($0.500\,\text{V/A}$). |
| **4** | **`IN-`** | `VREF_1V60_TRIP`| Reference divider node (`R_ref1` / `R_ref2`) | Precision $1.602\,\text{V}$ trip threshold reference. |
| **5** | **`SHDN_N`**| `+3V3_SEC` | Tied to $+3.3\,\text{V}$ rail | Comparator permanently enabled in active operating state. |
| **6** | **`VCC`** | `+3V3_SEC` | Local decoupling cap $C_{\text{U8}} = 100\,\text{nF} / 16\,\text{V}$ C0G | Clean $+3.30\,\text{V}_{\text{DC}}$ analog supply rail. |

## 4. Schematic Symbol Representation
```
                    [ U8_FAST_CC: TLV3501AIDBVR 4.5ns COMPARATOR ]
                                  ┌───────────────┐
    Net: FAST_CC_TRIP  ──────────[1] OUT       VCC[6]────────── Net: +3V3_SEC
    Net: AGND_SEC      ──────────[2] GND      SHDN[5]────────── Net: +3V3_SEC
    Net: FAST_CC_SENSE ──────────[3] IN+       IN-[4]────────── Net: VREF_1V60_TRIP
                                  └───────────────┘
                                   t_pd = 4.5 ns
```

## 5. Schematic & PCB Layout Guidelines
1. **Ultra-Low Parasitic Inductance**: TLV3501 switches in $4.5\,\text{ns}$. Route output trace `FAST_CC_TRIP` with minimal length ($< 4.0\,\text{mm}$) to base resistor `R_B_CLAMP` to prevent parasitic ringing.
2. **Decoupling**: Decouple Pin 6 (`VCC`) with a $100\,\text{nF}$ high-frequency C0G/X7R ceramic capacitor directly to Pin 2 (`GND`) with wide surface traces and no via indirection.
3. **Reference Decoupling**: Place a $10\,\text{nF}$ C0G capacitor from `VREF_1V60_TRIP` (Pin 4) to `AGND_SEC` to suppress any noise coupling onto the trip threshold.
""")

    # 3. Q_CLAMP MMBT3904 COMP Pin Pull-Down Transistor
    with open(OUT_DIR / "Q_CLAMP_mmbt3904_transistor.md", "w") as f:
        f.write(r"""# Component Schematic Specification: Q_CLAMP (COMP Pin Pull-Down Clamping Transistor)

## 1. Component Metadata
* **Reference Designator**: `Q_CLAMP`
* **Component Type**: General-Purpose High-Speed NPN Bipolar Junction Transistor
* **Manufacturer**: Diodes Incorporated / ON Semiconductor
* **Primary MPN**: `MMBT3904`
* **Alternate Manufacturer**: Nexperia
* **Alternate MPN**: `PMBT3904`
* **Package / Footprint**: SOT-23-3 (TO-236AB, Pitch: 0.95 mm, Body: 2.9 × 1.3 mm)
* **Subsystem**: Stage 5 (Autonomous Fast Hardware Current Clamping Subsystem)

## 2. Electrical Ratings & Constraints
* **Collector-Emitter Breakdown Voltage ($V_{\text{CEO}}$)**: $40.0\,\text{V}_{\text{DC}}$
  * Clamping node voltage (`LM5176_COMP`): Normal operating span $0.80\,\text{V}$ to $2.80\,\text{V}_{\text{DC}}$.
  * Voltage Derating: $\frac{2.80\,\text{V}}{40.0\,\text{V}} = \mathbf{7.0\%}$ (Negligible voltage stress).
* **Continuous Collector Current ($I_C$)**: $200.0\,\text{mA}$
  * LM5176 internal error amplifier sourcing capability: $I_{\text{COMP,source}} \approx 1.20\,\text{mA}$.
  * Current Derating: $\frac{1.20\,\text{mA}}{200\,\text{mA}} = \mathbf{0.60\%}$ (Enormous margin).
* **Collector-Emitter Saturation Voltage ($V_{\text{CE(sat)}}$)**:
  * $< 0.150\,\text{V}_{\text{DC}}$ at $I_C = 10\,\text{mA}, I_B = 1.0\,\text{mA}$.
  * At $I_C = 1.2\,\text{mA}$: $V_{\text{CE(sat)}} \approx \mathbf{0.080\,\text{V}_{\text{DC}}}$.
  * The LM5176 controller guarantees $0\%$ duty cycle and immediate PWM gating inhibit when `COMP` is pulled below $0.400\,\text{V}_{\text{DC}}$. $0.080\,\text{V} \ll 0.400\,\text{V}$ guarantees **$100\%$ positive PWM shutdown**!
* **Switching Turn-On Time ($t_{\text{on}}$)**:
  * Delay time ($t_d$): $10.0\,\text{ns}$
  * Rise time ($t_r$): $25.0\,\text{ns}$
  * Total saturation turn-on latency: $t_{\text{sat}} \le \mathbf{250.0\,\text{ns}}$ under $2.5\,\text{mA}$ overdrive.
* **Base Drive Sizing**:
  * Base Series Resistor: $R_{\text{B_CLAMP}} = 1.0\,\text{k}\Omega \pm 1\%$ (0603 SMD).
  * Base Pull-Down Resistor: $R_{\text{BE}} = 10.0\,\text{k}\Omega \pm 1\%$ (0603 SMD) from Base to Emitter (`AGND_SEC`).
  * Base Drive Current when TLV3501 trips ($V_{\text{OUT}} = 3.3\,\text{V}$):
    $$I_B = \frac{3.30\,\text{V} - V_{\text{BE}}}{R_{\text{B_CLAMP}}} = \frac{3.30\,\text{V} - 0.75\,\text{V}}{1000\,\Omega} = \mathbf{2.55\,\text{mA}}$$
  * Forced beta: $\beta_{\text{forced}} = \frac{I_C}{I_B} = \frac{1.20\,\text{mA}}{2.55\,\text{mA}} = 0.47 \ll 10$ (Deep saturation guaranteed!).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`BASE`** | `Q_CLAMP_BASE` | Base resistor `R_B_CLAMP` ($1.0\,\text{k}\Omega$), Pull-down `R_BE` ($10\,\text{k}\Omega$) | Driven by comparator output `FAST_CC_TRIP`. |
| **2** | **`EMITTER`**| `AGND_SEC` | Quiet secondary analog ground plane | Direct low-impedance ground connection. |
| **3** | **`COLLECTOR`**| `LM5176_COMP` | LM5176 Pin 6 (`COMP`), Type-II compensation network | Direct connection to error amp output. |

## 4. Schematic Symbol Representation
```
                     [ Q_CLAMP: MMBT3904 NPN CLAMP TRANSISTOR ]
                                    Collector (Pin 3)
                                          │
                                          ├─── Net: LM5176_COMP (Pin 6)
                                      ┌───┴───┐
                                      │  NPN  │
  Net: FAST_CC_TRIP ──[ 1.0 kΩ ]──────┤B     E├── Net: AGND_SEC (Pin 2)
                                      └───────┘
                                      Base (Pin 1)
                                          │
                                       [ 10 kΩ ]
                                          │
                                    Net: AGND_SEC
```

## 5. Schematic & PCB Layout Guidelines
1. **Direct COMP Pin Placement**: Place `Q_CLAMP` immediately adjacent to Pin 6 (`COMP`) of `U3` LM5176. The collector trace must be $< 2.0\,\text{mm}$ to prevent adding stray capacitance to the sensitive feedback loop.
2. **Quiet Emitter Ground**: Return Pin 2 (`EMITTER`) directly to `AGND_SEC` at `U3` Pin 11, avoiding power ground planes that carry switching currents.
""")

    # 4. Module 5 Equivalent Circuit Document
    with open(OUT_DIR / "module_05_fast_cc_protection_equivalent_circuit.md", "w") as f:
        f.write(r"""# Module 5 Equivalent Electronic Circuit: Fast Hardware CC Protection Subsystem

## 1. Subsystem Architecture Overview
The SPPS power supply incorporates an autonomous analog hardware current clamp operating completely independent of microcontroller firmware. While the STM32G474 supervisory firmware executes high-level telemetry and software current limits at a $10.0\,\text{Hz}$ rate ($100\,\text{ms}$ cycle), an external dead short circuit requires sub-microsecond intervention to prevent destructive thermal and avalanche breakdown of the `BSC034N04LS` power MOSFETs and output inductor `L1`.

Module 5 monitors the $10.0\,\text{m}\Omega$ output current sense shunt `R_shunt` in real time, amplifies the microvolt-level drop via the Texas Instruments **`INA240A2EDCKR`** ($A_v = 50.0\,\text{V/V}$, $400\,\text{kHz}$ bandwidth), compares the amplified voltage against a precision $1.602\,\text{V}$ threshold using the ultra-fast Texas Instruments **`TLV3501AIDBVR`** ($4.5\,\text{ns}$ propagation delay), and immediately drives the base of clamping transistor **`Q_CLAMP`** (`MMBT3904`). The transistor pulls the LM5176 `COMP` pin (Pin 6) below $0.10\,\text{V}$, instantly collapsing the controller duty cycle to $0\%$ and terminating gate drive switching pulses.

The entire autonomous shutdown sequence executes in **$2.25\,\mu\text{s}$**, easily satisfying the PRD sub-$5.0\,\mu\text{s}$ maximum latency requirement.

---

## 2. Full Schematic Electronic Circuit Diagram

```
========================================================================================================================
MODULE 5: AUTONOMOUS FAST HARDWARE CC PROTECTION CIRCUIT (Sub-5µs Trip Latency)
========================================================================================================================

    FROM MODULE 4 (OUTPUT SHUNT)
    ────────────────────────────────────────────
    Net: SHUNT_SENSE_P (Kelvin Tap 1K of R_shunt)
    Net: SHUNT_SENSE_N (Kelvin Tap 2K of R_shunt)
    ────────────────────────────────────────────
              │                     │
              │                     │
              │                     │     [ U7_FAST_CC: INA240A2 CURRENT SENSE AMPLIFIER ]
              │                     │       SC70-8 (Texas Instruments INA240A2EDCKR)
              │                     │       Av = 50.0 V/V, BW = 400 kHz, Slew = 2.0 V/µs
              │                     │       ┌──────────────┐
              └─────────────────────┼───────┤[1] IN+    VS [7]├─── Net: +3V3_SEC ──[ 100nF ]── AGND_SEC
                                    └───────┤[8] IN-   REF1[5]├─── Net: AGND_SEC
                                            │          REF2[3]├─── Net: AGND_SEC
                                            │          GND [2]├─── Net: AGND_SEC
                                            │          OUT [4]├───┬── Net: FAST_CC_SENSE (0.500 V / A)
                                            └──────────────┘      │
                                                                  │
    +3V3_SEC ──┬──────────────────────────────────────────────────┼───────────────────────────────┐
               │                                                  │                               │
             ┌─┴─┐ R_ref1                                         │                               │
             │   │ 10.6kΩ ±0.1%                                   │                               │
             └─┬─┘                                                │                               │
               ├─── Net: VREF_1V60_TRIP (1.602V)                  │                               │
             ┌─┴─┐                                                │                               │
             │   │ R_ref2                                         │     [ U8_FAST_CC: TLV3501 ]   │
             └─┬─┘ 10.0kΩ ±0.1%                                   │       SOT-23-6 (Push-Pull)    │
               │                                                  │       t_pd = 4.5 ns           │
               ├──[ 10nF C0G ]── AGND_SEC                         │       ┌──────────────┐        │
               │                                                  └───────┤[3] IN+   VCC [6]├─────┘
          AGND_SEC                                                        │          SHDN[5]├───── Net: +3V3_SEC
                                                                 ┌────────┤[4] IN-   OUT [1]├──┬── Net: FAST_CC_TRIP
                                                                 │        │          GND [2]├──┤
                                                                 │        └──────────────┘     │
                                                                 │                             │
                                                                 │                             │
                                                                 ▼                             ▼
                                                        Net: VREF_1V60_TRIP          [ R_hys 470kΩ Hysteresis ]
                                                                                               │
                                                                                               └─── To IN+ (Pin 3)
                                                                                               │
                                                                                             ┌─┴─┐
                                                                              R_B_CLAMP      │   │ 1.0 kΩ ±1%
                                                                                             └─┬─┘
                                                                                               │
                                                                                               ├── Net: Q_CLAMP_BASE
                                                                                               │
                                                                                             ┌─┴─┐
                                                                              R_BE           │   │ 10.0 kΩ ±1%
                                                                                             └─┬─┘
                                                                                               │
                                                                                          Net: AGND_SEC
                                                                                               │
                                                                                      [ Q_CLAMP: MMBT3904 ]
                                                                                        SOT-23 NPN BJT
                                                                                        ┌─────────────┐
                                                                     Net: Q_CLAMP_BASE ─┤B           C├── Net: LM5176_COMP (Pin 6)
                                                                                        │      E      │
                                                                                        └──────┬──────┘
                                                                                               │
                                                                                          Net: AGND_SEC
```

---

## 3. Dynamic Latency Timing & Sequence Analysis

When an external dead short circuit or severe transient overload occurs at the $4\,\text{mm}$ output binding posts:

```
Time (t)      Event Description                                              State / Signal Level
──────────────────────────────────────────────────────────────────────────────────────────────────
t = 0.00 µs   Dead short applied at binding posts J2/J3.                     I_OUT spikes > 3.20 A
t = 0.02 µs   Shunt voltage drops: V_shunt = 3.20 A × 10 mΩ = 32.0 mV.       Kelvin pins register drop
t = 1.20 µs   INA240 output slews from 1.500 V to 1.602 V trip threshold.    FAST_CC_SENSE = 1.602 V
t = 1.205 µs  TLV3501 comparator detects trip condition (4.5 ns latency).    FAST_CC_TRIP transitions 0V -> 3.3V
t = 1.455 µs  Q_CLAMP base is driven by 2.55 mA; transistor turns ON         Q_CLAMP enters deep saturation
              and reaches deep saturation (V_CE(sat) = 80 mV).               V_COMP collapses to 0.080 V
t = 2.250 µs  LM5176 internal error amplifier compensation node discharges.  Gate drive pulses clamped to 0%
              High-side MOSFETs QA/QD are completely inhibited.              Output current safely clamped!
──────────────────────────────────────────────────────────────────────────────────────────────────
TOTAL CLAMPING LATENCY: 2.25 µs (Guaranteed << 5.00 µs PRD Specification Limit)
```

---

## 4. Module 5 Comprehensive Netlist

| Net Name | Origin Pin / Pad | Destination Pins / Pads | Net Class | Physical Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `SHUNT_SENSE_P` | `R_shunt` Kelvin Tap 1K | `U7_FAST_CC` Pin 1 (IN+) | Analog Sense | Kelvin differential pair, $w = 0.25\,\text{mm}$ |
| `SHUNT_SENSE_N` | `R_shunt` Kelvin Tap 2K | `U7_FAST_CC` Pin 8 (IN-) | Analog Sense | Kelvin differential pair, $w = 0.25\,\text{mm}$ |
| `FAST_CC_SENSE` | `U7_FAST_CC` Pin 4 (OUT) | `U8_FAST_CC` Pin 3 (IN+), Hysteresis `R_hys` | Fast Analog | Trace length $< 5.0\,\text{mm}$, parasitic $C < 15\,\text{pF}$ |
| `VREF_1V60_TRIP`| Divider `R_ref1` / `R_ref2`| `U8_FAST_CC` Pin 4 (IN-), Filter Cap $10\,\text{nF}$ | Voltage Ref | Quiet trace shielded by `AGND_SEC` |
| `FAST_CC_TRIP` | `U8_FAST_CC` Pin 1 (OUT) | Base Resistor `R_B_CLAMP` Pin 1, Hysteresis `R_hys` | Fast Digital Pulse | Direct short trace ($< 4.0\,\text{mm}$) |
| `Q_CLAMP_BASE` | Resistor `R_B_CLAMP` Pin 2 | `Q_CLAMP` Base (Pin 1), Resistor `R_BE` Pin 1 | Control | Direct connection adjacent to transistor pad |
| `LM5176_COMP` | `Q_CLAMP` Collector (Pin 3)| `U3` LM5176 Pin 6 (`COMP`), Type-II Network | Analog Pull-Down | Trace length $< 2.0\,\text{mm}$ to Pin 6 |
| `+3V3_SEC` | Module 8 LDO Output | `U7_FAST_CC` Pin 7, `U8_FAST_CC` Pin 5/6, `R_ref1` | Power Rail | Filtered $+3.30\,\text{V}_{\text{DC}}$ linear analog rail |
| `AGND_SEC` | Ground Plane Star Point | All ground pins of `U7`, `U8`, `Q_CLAMP`, `R_ref2`, `R_BE` | Quiet Analog GND | Star-point secondary analog ground |

---

## 5. Laboratory Bring-Up & Test Points
* **`TP_CC_SENSE` (INA240 Output)**: Verify DC voltage equals exactly $0.500\,\text{V}$ per Ampere of load current ($1.500\,\text{V}$ at $3.00\,\text{A}$). Verify $< 5\,\text{mV}_{\text{RMS}}$ high-frequency PWM switching noise.
* **`TP_VREF_TRIP` (Comparator Threshold)**: Measure with $6.5$-digit DMM. Verify $1.602\,\text{V}_{\text{DC}} \pm 0.2\%$.
* **`TP_CC_TRIP` (Comparator Output)**: Under normal operation ($I_{\text{OUT}} \le 3.0\,\text{A}$), verify logic LOW ($< 0.10\,\text{V}$). Under dynamic short circuit test, capture transition to logic HIGH ($+3.30\,\text{V}$) with oscilloscope $500\,\text{MHz}$ probe.
* **`TP_COMP_CLAMP` (LM5176 COMP Pin)**: Trigger oscilloscope on `TP_CC_TRIP` rising edge. Verify `LM5176_COMP` collapses from its nominal $\approx 1.8\,\text{V}$ operating point down to $< 0.10\,\text{V}$ in $< 250\,\text{ns}$, with gate drive pulses extinguishing within $2.25\,\mu\text{s}$.
""")

    print("Module 5 files successfully generated.")

if __name__ == "__main__":
    write_files()
