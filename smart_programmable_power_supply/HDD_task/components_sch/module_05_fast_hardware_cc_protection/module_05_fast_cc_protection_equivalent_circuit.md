# Module 5 Equivalent Electronic Circuit: Fast Hardware CC Protection Subsystem

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
