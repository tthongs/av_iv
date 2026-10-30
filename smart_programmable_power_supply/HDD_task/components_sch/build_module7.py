#!/usr/bin/env python3
"""
Component and Schematic Connection Generator: Module 7 (Dual-Domain Telemetry)
"""

from pathlib import Path

OUT_DIR = Path("/home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/components_sch/module_07_dual_domain_telemetry")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def write_files():
    # 1. U4 AMC1311 Isolated Amplifier
    with open(OUT_DIR / "U4_amc1311_isolated_amp.md", "w") as f:
        f.write(r"""# Component Schematic Specification: U4 (AMC1311BDWVR Reinforced Isolated Amplifier)

## 1. Component Metadata
* **Reference Designator**: `U4`
* **Component Type**: High-Impedance 2-V Input Reinforced Galvanically Isolated Amplifier
* **Manufacturer**: Texas Instruments
* **Primary MPN**: `AMC1311BDWVR`
* **Alternate Manufacturer**: Silicon Laboratories
* **Alternate MPN**: `Si8920BD-IS` (Wide SOIC-8, reinforced isolated amplifier)
* **Package / Footprint**: SOIC-8 Wide-Body (Pitch: 1.27 mm, Body: 5.85 mm creepage, Clearance: 8.0 mm)
* **Subsystem**: Stage 7 (Primary AC Mains Isolated Voltage Telemetry)

## 2. Electrical Ratings & Constraints
* **Galvanic Isolation Rating**:
  * Reinforced Working Insulation: $V_{\text{IOWM}} = 1500\,\text{V}_{\text{RMS}}$ ($2121\,\text{V}_{\text{peak}}$).
  * Reinforced Withstand Voltage ($V_{\text{ISO}}$): $\mathbf{7000\,\text{V}_{\text{peak}}} / \mathbf{5000\,\text{V}_{\text{RMS}}}$ for 1 minute (IEC 62368-1).
  * Common-Mode Transient Immunity (CMTI): $> 75.0\,\text{kV}/\mu\text{s}$ (immune to flyback and buck-boost switching noise).
* **Linear Input Voltage Range ($V_{\text{IN}}$)**: $0.0\,\text{V}$ to $+2.000\,\text{V}_{\text{DC}}$ (Unipolar input, optimized for divided DC bulk / rectified AC).
* **Input Impedance ($R_{\text{IN}}$)**: $> 1.0\,\text{G}\Omega$ (negligible loading on high-voltage divider).
* **Voltage Gain ($A_v$)**: $\mathbf{1.000\,\text{V/V}} \pm 0.20\%$ maximum gain error.
* **Nonlinearity**: $< 0.03\%$ full scale.
* **Bandwidth ($-3\,\text{dB}$)**: $220.0\,\text{kHz}$.
* **High-Side Supply ($V_{\text{DD1}}$)**: $+3.0\,\text{V}$ to $+5.5\,\text{V}_{\text{DC}}$ (Powered from isolated Flyback aux bias rail).
* **Low-Side Supply ($V_{\text{DD2}}$)**: $+3.0\,\text{V}$ to $+5.5\,\text{V}_{\text{DC}}$ (Powered from secondary $+3.30\,\text{V}_{\text{DC}}$ LDO rail).
* **Differential Output Stage**:
  * Emits differential signal $V_{\text{OUTP}} - V_{\text{OUTN}}$ with DC common-mode midpoint $V_{\text{CM,out}} = 1.44\,\text{V}_{\text{DC}}$.
  * A single-supply low-pass differential-to-single-ended operational amplifier circuit scales and filters the signal to feed STM32 ADC input `PC0`.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Isolation Domain | Description & Connection |
| :---: | :---: | :--- | :---: | :--- |
| **1** | **`VDD1`** | `+5V_HOT_ISO` | Primary (HOT) | High-side isolated supply rail; $100\,\text{nF}$ bypass cap. |
| **2** | **`INP`**  | `MAINS_DIV_SENSE` | Primary (HOT) | Tapped from high-voltage divider $1.5\,\text{M}\Omega / 7.5\,\text{k}\Omega$. |
| **3** | **`INN`**  | `PGND_HOT` | Primary (HOT) | Negative differential input tied directly to primary hot ground. |
| **4** | **`GND1`** | `PGND_HOT` | Primary (HOT) | High-side power ground reference. |
| **5** | **`GND2`** | `AGND_SEC` | Secondary (SELV)| Low-side secondary quiet analog ground plane. |
| **6** | **`OUTN`** | `AMC_OUT_N` | Secondary (SELV)| Differential negative analog output to differential filter. |
| **7** | **`OUTP`** | `AMC_OUT_P` | Secondary (SELV)| Differential positive analog output to differential filter. |
| **8** | **`VDD2`** | `+3V3_SEC` | Secondary (SELV)| Low-side secondary supply; $100\,\text{nF}$ bypass cap to `AGND_SEC`. |

## 4. Schematic Symbol Representation
```
                    [ U4: AMC1311BDWVR REINFORCED ISOLATED AMP ]
                      PRIMARY DOMAIN (HOT)  │  SECONDARY DOMAIN (SELV)
                                            │
                                ┌───────────┴───────────┐
     Net: +5V_HOT_ISO ─────────[1] VDD1             VDD2[8]───────── Net: +3V3_SEC
   Net: MAINS_DIV_SENSE ───────[2] INP              OUTP[7]───────── Net: AMC_OUT_P
     Net: PGND_HOT    ─────────[3] INN              OUTN[6]───────── Net: AMC_OUT_N
     Net: PGND_HOT    ─────────[4] GND1             GND2[5]───────── Net: AGND_SEC
                                └───────────────────────┘
                                     SOIC-8 Wide-Body
                                (>= 8.0 mm Creepage Across)
```

## 5. Schematic & PCB Layout Guidelines
1. **Creepage Barrier Keepout**: The PCB layout under `U4` must maintain a strict copper keepout zone of $\ge 8.0\,\text{mm}$ across all internal and external copper layers between Primary Hot Ground (`PGND_HOT`) and Secondary SELV Ground (`AGND_SEC`).
2. **Differential Output Filtering**: Route `AMC_OUT_P` and `AMC_OUT_N` as a balanced differential pair to a second-order active Sallen-Key low-pass filter ($f_c = 10.0\,\text{kHz}$) placed on the secondary side before feeding STM32 pin `PC0`.
""")

    # 2. R_DIV_HV High-Voltage Mains Divider
    with open(OUT_DIR / "R_DIV_HV_mains_divider.md", "w") as f:
        f.write(r"""# Component Schematic Specification: R_DIV_HV (High-Voltage AC Mains Divider)

## 1. Component Metadata
* **Reference Designators**: `R_HV1`, `R_HV2`, `R_HV3` (High-Side String), `R_HV_BOT` (Precision Bottom Resistor)
* **Component Type**: High-Voltage Precision Thick/Thin Film SMD Resistors
* **Values & Part Numbers**:
  * `R_HV1..3`: $3x\ 500.0\,\text{k}\Omega \pm 1\%$, 0.25 W, 200 V rating, 1206 SMD (Vishay Dale `CRCW1206500KFKEA`)
    * Total high-side resistance: $R_{\text{HV_top}} = 3 \times 500\,\text{k}\Omega = \mathbf{1.500\,\text{M}\Omega}$.
  * `R_HV_BOT`: $7.50\,\text{k}\Omega \pm 0.1\%$, 0.125 W, TCR $\pm 25\,\text{ppm}/^\circ\text{C}$, 0805 SMD (Vishay Dale `TNPW08057K50BEEA`)
* **Subsystem**: Stage 7 (Primary AC Mains Isolated Voltage Telemetry)

## 2. Electrical Ratings & Constraints
* **Total Resistance**: $R_{\text{tot}} = 1500\,\text{k}\Omega + 7.50\,\text{k}\Omega = \mathbf{1507.5\,\text{k}\Omega}$.
* **Voltage Division Ratio ($k_{\text{div}}$)**:
  $$k_{\text{div}} = \frac{R_{\text{HV_BOT}}}{R_{\text{HV_top}} + R_{\text{HV_BOT}}} = \frac{7.50\,\text{k}\Omega}{1507.5\,\text{k}\Omega} = \frac{1}{201.0} \approx \mathbf{0.0049751}$$
* **Maximum Peak Voltage Sensed ($265\,\text{V}_{\text{AC RMS}}$)**:
  $$V_{\text{bulk,peak}} = 265\,\text{V} \times \sqrt{2} = 374.8\,\text{V}_{\text{peak}}$$
  $$V_{\text{sense,peak}} = 374.8\,\text{V} \times 0.0049751 = \mathbf{1.8647\,\text{V}_{\text{peak}}}$$
  * Perfectly matches the linear input envelope of the `AMC1311` ($0.0\,\text{V}$ to $2.000\,\text{V}$), preserving a $6.8\%$ linear headroom margin.
* **Power Dissipation**:
  * Maximum continuous power at $265\,\text{V}_{\text{RMS}}$ ($375\,\text{V}_{\text{DC}}$ equivalent):
    $$P_{\text{loss,div}} = \frac{(374.8\,\text{V})^2}{1.5075 \times 10^6\,\Omega} = \mathbf{0.093\,\text{W}} \quad (93.2\,\text{mW})$$
  * Dissipation per 1206 high-side resistor:
    $$P_{\text{R_HV}} = \frac{93.2\,\text{mW}}{3} = \mathbf{31.1\,\text{mW}} \quad (\text{Rating: } 250\,\text{mW} \implies \text{Derating } 12.4\% \ll 60\%)$$
* **High-Voltage Creepage Across Divider**:
  * Slicing the high-side resistance across three 1206 packages distributes voltage stress to $\le 125\,\text{V}$ per package (well below the $200\,\text{V}$ rating).
  * Combined pad-to-pad creepage across the three resistors exceeds $7.2\,\text{mm}$.

## 3. Schematic Pin Connections & Net Mapping
| Resistor | Pin 1 Net | Pin 2 Net | Footprint | Trace Requirements |
| :---: | :--- | :--- | :---: | :--- |
| **`R_HV1`** | `+HV_BULK` | `HV_DIV_TAP1` | 1206 SMD | High-voltage trace, $\ge 3.0\,\text{mm}$ clearance to ground. |
| **`R_HV2`** | `HV_DIV_TAP1` | `HV_DIV_TAP2` | 1206 SMD | Series bridge resistor. |
| **`R_HV3`** | `HV_DIV_TAP2` | `MAINS_DIV_SENSE` | 1206 SMD | Connects to `AMC1311` INP (Pin 2). |
| **`R_HV_BOT`**| `MAINS_DIV_SENSE`| `PGND_HOT` | 0805 SMD | Precision bottom leg; connects to primary hot ground. |

## 4. Schematic Symbol Representation
```
                    [ HIGH-VOLTAGE AC MAINS DIVIDER STRING ]
                                Net: +HV_BULK
                                     │
                                   ┌─┴─┐
                                   │   │ R_HV1 (500 kΩ / 1206)
                                   └─┬─┘
                                     │
                                   ┌─┴─┐
                                   │   │ R_HV2 (500 kΩ / 1206)
                                   └─┬─┘
                                     │
                                   ┌─┴─┐
                                   │   │ R_HV3 (500 kΩ / 1206)
                                   └─┬─┘
                                     │
   Net: MAINS_DIV_SENSE ─────────────┼────────── U4 AMC1311 INP (Pin 2)
                                     │
                                   ┌─┴─┐
                                   │   │ R_HV_BOT (7.50 kΩ ±0.1% / 0805)
                                   └─┬─┘
                                     │
                               Net: PGND_HOT
```
""")

    # 3. CT1 Talema Current Transformer
    with open(OUT_DIR / "CT1_talema_current_transformer.md", "w") as f:
        f.write(r"""# Component Schematic Specification: CT1 (AC Mains Current Transformer)

## 1. Component Metadata
* **Reference Designator**: `CT1`
* **Component Type**: High-Accuracy Toroidal AC Current Transformer
* **Manufacturer**: Talema Group
* **Primary MPN**: `AC1010`
* **Alternate Manufacturer**: CR Magnetics
* **Alternate MPN**: `CR8410-1000` (10 A RMS, 1000:1 ratio, 4000 V isolation)
* **Package / Footprint**: Encapsulated Through-Hole Toroid with Central Primary Conductor Hole
* **Subsystem**: Stage 7 (Primary AC Mains Isolated Current Telemetry)

## 2. Electrical Ratings & Constraints
* **Current Transformation Turns Ratio ($N_{\text{pri}}:N_{\text{sec}}$)**: $1 : 1000$ ($1000$ secondary turns).
* **Rated Primary Continuous Current ($I_{\text{pri,rated}}$)**: $10.0\,\text{A}_{\text{RMS}}$ ($50/60\,\text{Hz}$).
  * Maximum operating AC input current: $1.604\,\text{A}_{\text{RMS}}$ at $85\,\text{V}_{\text{AC}}$ full load.
  * Current Derating: $\frac{1.604\,\text{A}}{10.0\,\text{A}} = \mathbf{16.0\%}$ (Enormous headroom).
* **Galvanic Isolation Withstand Voltage**: $4000\,\text{V}_{\text{RMS}}$ (certified reinforced safety barrier between AC Live line and secondary sensing circuitry).
* **Secondary Current Output**:
  $$I_{\text{sec}} = \frac{I_{\text{pri}}}{1000}$$
  * At $I_{\text{pri}} = 1.604\,\text{A}_{\text{RMS}}$: $I_{\text{sec}} = \mathbf{1.604\,\text{mA}_{\text{RMS}}}$ ($2.268\,\text{mA}_{\text{peak}}$).
  * At $I_{\text{pri}} = 0.310\,\text{A}_{\text{RMS}}$ ($230\,\text{V}_{\text{AC}}$ nominal): $I_{\text{sec}} = \mathbf{0.310\,\text{mA}_{\text{RMS}}}$.
* **Secondary DC Resistance ($R_{\text{sec}}$)**: $48.0\,\Omega \pm 10\%$.
* **Linearity**: $\pm 0.2\%$ across $0.1\,\text{A}$ to $10.0\,\text{A}$ primary range.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Function | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **APERTURE**| **Primary Conductor** | `AC_LINE_FUSED` | Pass-through of AC Line trace | AC mains current carrying line. |
| **Pin 1**   | **Secondary Terminal 1**| `CT_SEC_HI` | Burden Resistor `R_burden`, STM32 ADC filter | AC current signal tap. |
| **Pin 2**   | **Secondary Terminal 2**| `VREF_1V65_BIAS` | DC Midpoint Bias Divider ($+1.65\,\text{V}_{\text{DC}}$) | AC ground reference / DC offset. |

## 4. Schematic Symbol Representation
```
                    [ CT1: TALEMA AC1010 CURRENT TRANSFORMER ]
                                  1000 : 1 Ratio
                                ┌────────────────┐
     Net: AC_LINE_FUSED ───────( ) Aperture Pass ( )─────── Net: AC_LINE_FILT
                                └───────┬────────┘
                                        │
                                  ┌─────┴─────┐
                                  │   █████   │ Secondary Winding
                                  └─────┬─────┘ (1000 Turns)
                                        ├─── Pin 1: Net: CT_SEC_HI
                                        │
                                        └─── Pin 2: Net: VREF_1V65_BIAS (+1.65V DC)
```

## 5. Schematic & PCB Layout Guidelines
1. **Safety Isolation Spacing**: Maintain $\ge 6.5\,\text{mm}$ creepage clearance between the primary copper trace passing through the aperture and the secondary termination pins on the PCBA.
2. **Burden Placement**: Place the precision burden resistor `R_burden` immediately adjacent to Pins 1 and 2 of the CT to eliminate loop inductance.
""")

    # 4. R_burden Precision CT Burden Resistor
    with open(OUT_DIR / "R_burden_resistor.md", "w") as f:
        f.write(r"""# Component Schematic Specification: R_burden (Precision CT Burden & DC Bias Network)

## 1. Component Metadata
* **Reference Designators**: `R_burden` (Burden), `R_bias1`, `R_bias2` (Midpoint Divider), `C_bias` (Decoupling)
* **Values & Part Numbers**:
  * `R_burden`: $100.0\,\Omega \pm 0.1\%$, 0.25 W, TCR $\pm 25\,\text{ppm}/^\circ\text{C}$, 0805 SMD (Vishay Dale `TNPW0805100RBEEA`)
  * `R_bias1, R_bias2`: $2x\ 10.0\,\text{k}\Omega \pm 0.1\%$, 0.125 W, 0805 SMD (Vishay Dale `TNPW080510K0BEEA`)
  * `C_bias`: $1.0\,\mu\text{F} \pm 10\%$, 16 V, X7R, 0603 SMD (Murata `GRM188R71C105KA12D`)
* **Subsystem**: Stage 7 (Primary AC Mains Isolated Current Telemetry)

## 2. Electrical Ratings & Constraints
* **Secondary Voltage Generation**:
  At maximum input current ($1.604\,\text{A}_{\text{RMS}}$):
  $$V_{\text{burden,RMS}} = I_{\text{sec}} \times R_{\text{burden}} = (1.604 \times 10^{-3}\,\text{A}) \times 100.0\,\Omega = \mathbf{160.4\,\text{mV}_{\text{RMS}}}$$
  $$V_{\text{burden,peak}} = 160.4\,\text{mV} \times \sqrt{2} = \mathbf{226.8\,\text{mV}_{\text{peak}}}$$
* **DC Midpoint Bias Formulation**:
  Dividing the clean $+3.300\,\text{V}_{\text{DC}}$ analog supply with two matched $10.0\,\text{k}\Omega \pm 0.1\%$ resistors:
  $$V_{\text{bias}} = (+3.300\,\text{V}) \times \frac{10.0\,\text{k}\Omega}{10.0\,\text{k}\Omega + 10.0\,\text{k}\Omega} = \mathbf{1.650\,\text{V}_{\text{DC}}}$$
* **Net Signal Sensed at STM32 ADC Input (`PC1`)**:
  $$V_{\text{ADC,IN}} = 1.650\,\text{V}_{\text{DC}} \pm 226.8\,\text{mV} \implies \mathbf{1.423\,\text{V}} \le V_{\text{ADC,IN}} \le \mathbf{1.877\,\text{V}}$$
  * Centered directly in the $0.0\,\text{V}$ to $+3.30\,\text{V}$ dynamic span of STM32 ADC1 with $> 1.4\,\text{V}$ headroom margin to both rails, completely eliminating clipping.

## 3. Schematic Pin Connections & Net Mapping
| Component | Pin 1 Net | Pin 2 Net | Description & Connection |
| :---: | :--- | :--- | :--- |
| **`R_burden`** | `CT_SEC_HI` | `VREF_1V65_BIAS` | Direct Kelvin connection across CT secondary terminals. |
| **`R_bias1`** | `+3V3_SEC` | `VREF_1V65_BIAS` | Top leg of midpoint voltage divider. |
| **`R_bias2`** | `VREF_1V65_BIAS` | `AGND_SEC` | Bottom leg of midpoint voltage divider. |
| **`C_bias`** | `VREF_1V65_BIAS` | `AGND_SEC` | Low-impedance AC ground bypass capacitor ($1.0\,\mu\text{F}$). |

## 4. Schematic Symbol Representation
```
                    [ PRECISION BURDEN & DC MIDPOINT BIAS NETWORK ]
                                 Net: +3V3_SEC
                                       │
                                     ┌─┴─┐
                                     │   │ R_bias1 (10.0 kΩ ±0.1%)
                                     └─┬─┘
                                       │
      Net: VREF_1V65_BIAS ─────────────┼───────────────┬───────────────── Pin 2 of CT1
                                       │               │
                                     ┌─┴─┐          ┌──┴──┐
                  R_bias2 (10.0 kΩ)  │   │          │     │ C_bias (1.0 µF X7R)
                                     └─┬─┘          └──┬──┘
                                       │               │
                                 Net: AGND_SEC   Net: AGND_SEC
                                       │
                                       │
   Pin 1 of CT1 ──── Net: CT_SEC_HI ───┴──[ R_burden: 100.0 Ω ±0.1% ]── Net: VREF_1V65_BIAS
                            │
                       [ RC Filter: 1kΩ / 10nF ]
                            │
               Net: CT_ADC_IN ──> STM32 Pin 9 (PC1)
```
""")

    # 5. U6 INA226 Secondary I2C Power Monitor
    with open(OUT_DIR / "U6_ina226_power_monitor.md", "w") as f:
        f.write(r"""# Component Schematic Specification: U6 (INA226AIDGSR Secondary I2C Power Monitor)

## 1. Component Metadata
* **Reference Designator**: `U6`
* **Component Type**: High-Precision Bidirectional Current and Power Monitor with I2C Interface
* **Manufacturer**: Texas Instruments
* **Primary MPN**: `INA226AIDGSR`
* **Alternate Manufacturer**: Texas Instruments
* **Alternate MPN**: `INA238AIDGSR` (High-accuracy 16-bit power monitor, 85V bus)
* **Package / Footprint**: VSSOP-10 (Pitch: 0.50 mm, Body: 3.0 × 3.0 mm)
* **Subsystem**: Stage 7 (Secondary DC Output Power Telemetry Engine)

## 2. Electrical Ratings & Constraints
* **Bus Voltage Range ($V_{\text{BUS}}$)**: $0.0\,\text{V}$ to $+36.0\,\text{V}_{\text{DC}}$
  * Output rail operating span: $+5.0\,\text{V}$ to $+20.0\,\text{V}_{\text{DC}}$.
  * Maximum rated bus stress derating: $\frac{20.0\,\text{V}}{36.0\,\text{V}} = \mathbf{55.5\%} \le 75\%$.
* **Shunt Full-Scale Voltage Range**: $\pm 81.92\,\text{mV}_{\text{DC}}$
  * Maximum drop across $10.0\,\text{m}\Omega$ shunt at $3.0\,\text{A}$:
    $$V_{\text{shunt,max}} = 3.0\,\text{A} \times 0.010\,\Omega = \mathbf{30.00\,\text{mV}} \quad (\text{Derating: } 36.6\% \text{ of full scale})$$
  * At $4.2\,\text{A}$ transient overload: $V_{\text{shunt,peak}} = 42.0\,\text{mV} \ll 81.92\,\text{mV}$ (zero clipping).
* **Quantization Resolution**:
  * Shunt Voltage LSB: $2.5\,\mu\text{V}$ per bit.
    $$\text{Current LSB} = \frac{2.5\,\mu\text{V}}{10.0\,\text{m}\Omega} = \mathbf{250.0\,\mu\text{A per LSB}} \quad (0.25\,\text{mA})$$
  * Bus Voltage LSB: $\mathbf{1.25\,\text{mV per LSB}}$.
  * Power Register LSB: $25 \times \text{Current LSB} = \mathbf{6.25\,\text{mW per LSB}}$.
* **Measurement Accuracy**:
  * Gain Error: $\le 0.10\%$ maximum.
  * Offset Voltage: $\le 10.0\,\mu\text{V}$ maximum ($1.0\,\text{mA}$ offset).
* **Conversion Time & Digital Averaging**:
  * Programmed for $16\times$ internal hardware averaging with $1.10\,\text{ms}$ conversion time per channel ($V_{\text{BUS}}$ and $V_{\text{shunt}}$). Total sample cycle: $2.20\,\text{ms}$, updated at $10.0\,\text{Hz}$ rate.
* **I2C Bus Address**: `0x40` (7-bit address `1000000b`), configured by tying both Address pins `A0` and `A1` to `GND_SELV`.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`IN+`** | `SHUNT_SENSE_P` | `R_shunt` Kelvin Positive Pad (1K) | Dedicated Kelvin sense trace ($w = 0.25\,\text{mm}$). |
| **2** | **`IN-`** | `SHUNT_SENSE_N` | `R_shunt` Kelvin Negative Pad (2K) | Dedicated Kelvin sense trace ($w = 0.25\,\text{mm}$). |
| **3** | **`VBUS`**| `+V_OUT` | Regulated DC output rail | Senses bus voltage for power calculation. |
| **4** | **`ALERT`**| `NC` | Not used in baseline firmware | Open-drain alert output (optional interrupt). |
| **5** | **`SDA`** | `I2C1_SDA` | STM32 Pin 62 (`PB9`), $2.2\,\text{k}\Omega$ pull-up | Fast-Mode I2C serial data line. |
| **6** | **`SCL`** | `I2C1_SCL` | STM32 Pin 61 (`PB8`), $2.2\,\text{k}\Omega$ pull-up | Fast-Mode I2C serial clock line. |
| **7** | **`VS`**  | `+3V3_SEC` | Decoupling Cap $C_{\text{U6}} = 100\,\text{nF} / 16\,\text{V}$ | Supply rail ($+3.30\,\text{V}_{\text{DC}}$). |
| **8** | **`GND`** | `GND_SELV` | Secondary ground plane | Direct low-impedance ground connection. |
| **9** | **`A1`**  | `GND_SELV` | Tied to `GND_SELV` | Sets I2C Address bit A1 = 0. |
| **10**| **`A0`**  | `GND_SELV` | Tied to `GND_SELV` | Sets I2C Address bit A0 = 0. |

## 4. Schematic Symbol Representation
```
                    [ U6: INA226AIDGSR 16-BIT I2C POWER MONITOR ]
                                  ┌───────────────┐
   Net: SHUNT_SENSE_P ───────────[1] IN+       A0[10]────────── Net: GND_SELV
   Net: SHUNT_SENSE_N ───────────[2] IN-       A1 [9]────────── Net: GND_SELV
        Net: +V_OUT   ───────────[3] VBUS     GND [8]────────── Net: GND_SELV
             NC       ───────────[4] ALERT     VS [7]────────── Net: +3V3_SEC
       Net: I2C1_SDA  ───────────[5] SDA      SCL [6]────────── Net: I2C1_SCL
                                  └───────────────┘
                                   Address = 0x40
```

## 5. Schematic & PCB Layout Guidelines
1. **Differential Kelvin Pair**: Route `SHUNT_SENSE_P` and `SHUNT_SENSE_N` as a tight differential pair from `R_shunt`. Place a $10.0\,\Omega$ series resistor and $10.0\,\text{nF}$ filter capacitor across Pins 1 and 2 directly at the IC to attenuate high-frequency switching noise.
2. **Local Bypass**: Place the $100\,\text{nF}$ bypass capacitor within $1.5\,\text{mm}$ of Pin 7 (`VS`) and Pin 8 (`GND`).
""")

    # 6. Module 7 Equivalent Circuit Document
    with open(OUT_DIR / "module_07_dual_domain_telemetry_equivalent_circuit.md", "w") as f:
        f.write(r"""# Module 7 Equivalent Electronic Circuit: Dual-Domain Power Telemetry Subsystem

## 1. Subsystem Architecture Overview
The SPPS system implements a dual-domain telemetry engine capable of measuring both primary input AC power ($P_{\text{AC}}$) and secondary output DC power ($P_{\text{DC}}$) simultaneously to calculate real-time conversion efficiency $\eta = \frac{P_{\text{DC}}}{P_{\text{AC}}} \times 100\%$.

To maintain certified **$3000\,\text{V}_{\text{RMS}}$ reinforced isolation** across the safety boundary, the primary sensing circuits employ galvanic isolation:
1. **Primary AC Voltage Sensing**: AC line voltage is tapped after the bridge rectifier from the high-voltage link (`+HV_BULK`), attenuated by a $201:1$ precision resistive divider string (`R_HV1..3` and `R_HV_BOT`), and transmitted across the galvanic boundary via the Texas Instruments **`AMC1311BDWVR`** reinforced isolated amplifier ($5.85\,\text{mm}$ creepage, $7000\,\text{V}_{\text{peak}}$ barrier). The isolated differential output is filtered and sampled by STM32 ADC1 channel `PC0`.
2. **Primary AC Current Sensing**: The primary AC mains line passes through the central aperture of a **`Talema AC1010`** encapsulated toroidal current transformer ($1000:1$ ratio, $4000\,\text{V}_{\text{RMS}}$ isolation). Secondary current develops an AC voltage drop across a precision $100.0\,\Omega \pm 0.1\%$ thin-film burden resistor (`R_burden`) biased around a $+1.650\,\text{V}_{\text{DC}}$ midpoint reference, sampled by STM32 ADC1 channel `PC1`.
3. **Secondary DC Telemetry**: Sensed locally via the Texas Instruments **`INA226AIDGSR`** 16-bit power monitor at I2C address `0x40`. It samples load current through the $10.0\,\text{m}\Omega$ Bourns shunt and bus voltage directly from the `+V_OUT` rail, emitting digital power measurements over I2C at $10.0\,\text{Hz}$.

---

## 2. Full Schematic Electronic Circuit Diagram

```
========================================================================================================================
MODULE 7: DUAL-DOMAIN TELEMETRY SCHEMATIC (Isolated Primary & Digital Secondary)
========================================================================================================================

PRIMARY HIGH-VOLTAGE DOMAIN (HOT)                │ SECONDARY ISOLATED DOMAIN (SELV)
─────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────
                                                 │
  +HV_BULK (+120V to +375V DC)                   │
      │                                          │
    ┌─┴─┐ R_HV1 (500kΩ / 1206)                   │
    └─┬─┘                                        │
      │                                          │
    ┌─┴─┐ R_HV2 (500kΩ / 1206)                   │
    └─┬─┘                                        │
      │                                          │
    ┌─┴─┐ R_HV3 (500kΩ / 1206)                   │
    └─┬─┘                                        │
      │                                          │
      ├─── Net: MAINS_DIV_SENSE (0 - 1.86V)      │
      │                                          │
    ┌─┴─┐                                        │
    │   │ R_HV_BOT (7.50kΩ ±0.1%)                │
    └─┬─┘                                        │
      │                                          │
  PGND_HOT                                       │
      │                                          │
      │   [ U4: AMC1311BDWVR ISOLATED AMP ]      │
      │   ┌──────────────────────────────────────┼───────────────────────────┐
+5V_HOT ──┤[1] VDD1                              │                  VDD2 [8]├─── Net: +3V3_SEC
MAINS_DIV─┤[2] INP                               │                  OUTP [7]├──┬ Net: AMC_OUT_P
PGND_HOT──┤[3] INN                               │                  OUTN [6]├──┼ Net: AMC_OUT_N
PGND_HOT──┤[4] GND1                              │                  GND2 [5]├──┴ Net: AGND_SEC
          └──────────────────────────────────────┼───────────────────────────┘
                                                 │
                                                 │   [ DIFFERENTIAL-TO-SINGLE-ENDED ACTIVE FILTER ]
                                                 │   Net: AMC_OUT_P ──[ 10k ]──┐
                                                 │   Net: AMC_OUT_N ──[ 10k ]──┼──[ OPAMP ]── Net: AMC1311_ADC_IN
                                                 │                             │                  (To STM32 PC0)
                                                 │                             ▼
                                                 │
                                                 │
                                                 │
  [ CT1: TALEMA AC1010 CURRENT TRANSFORMER ]     │
  Net: AC_LINE_FUSED ──( Aperture Pass )── FILT  │
                       ┌─────────┴─────────┐     │
                       │ Secondary (1000T) │     │
                       └─────────┬─────────┘     │
                                 │               │
  Net: CT_SEC_HI ────────────────┼───────────────┼──────────────────────────────┬─[ 1kΩ / 10nF ]─> Net: CT_ADC_IN
                                 │               │                              │                  (To STM32 PC1)
                           [ R_burden ]          │                        [ R_burden: 100.0Ω ±0.1% ]
                                 │               │                              │
  Net: VREF_1V65_BIAS ───────────┴───────────────┼──────────────────────────────┴─ Net: VREF_1V65_BIAS
                                                 │                                        │
                                                 │                        +3V3_SEC ──[ 10kΩ ]──┬──[ 1.0µF ]── AGND_SEC
                                                 │                                             │
                                                 │                                           [ 10kΩ ]
                                                 │                                             │
                                                 │                                         AGND_SEC
                                                 │
─────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────
SECONDARY DIGITAL TELEMETRY                      │
                                                 │
          +V_OUT ──[ U6: INA226 Pin 3 VBUS ]     │
                                                 │
          SHUNT_SENSE_P ──[ INA226 Pin 1 IN+ ]   │
          SHUNT_SENSE_N ──[ INA226 Pin 2 IN- ]   │
                                                 │
          I2C1_SCL ───────[ INA226 Pin 6 SCL ]   │
          I2C1_SDA ───────[ INA226 Pin 5 SDA ]   │
          +3V3_SEC ───────[ INA226 Pin 7 VS  ]   │
          GND_SELV ───────[ INA226 Pins 8,9,10]  │
                                                 │
```

---

## 3. Mathematical Telemetry Calibration Models

### 3.1 AC Mains True RMS Voltage Calculation
The sampled ADC voltage $V_{\text{ADC}}(t)$ on pin `PC0` relates to instantaneous bulk voltage:
$$V_{\text{bulk}}(t) = V_{\text{ADC}}(t) \times \left( \frac{1507.5\,\text{k}\Omega}{7.50\,\text{k}\Omega} \right) \times \left( \frac{V_{\text{REF,ADC}}}{4096} \right) = V_{\text{ADC}}(t) \times 201.0 \times (805.7\,\mu\text{V})$$
The STM32 Cordic math engine accumulates $N = 1000$ samples over one full $50\,\text{Hz}$ mains period ($20.0\,\text{ms}$ window):
$$V_{\text{AC,RMS}} = \sqrt{\frac{1}{N} \sum_{k=1}^N \left( \frac{V_{\text{bulk}}[k]}{\sqrt{2}} \right)^2}$$

### 3.2 AC Mains True RMS Current Calculation
The sampled ADC voltage on pin `PC1` relates to instantaneous line current:
$$I_{\text{line}}(t) = \left( V_{\text{ADC}}(t) - 1.650\,\text{V} \right) \times \left( \frac{1000}{R_{\text{burden}}} \right) = \left( V_{\text{ADC}}(t) - 1.650\,\text{V} \right) \times 10.0\,\text{A/V}$$
Accumulating over the identical $20.0\,\text{ms}$ window:
$$I_{\text{AC,RMS}} = \sqrt{\frac{1}{N} \sum_{k=1}^N \left( I_{\text{line}}[k] \right)^2}$$
$$P_{\text{AC}} = \frac{1}{N} \sum_{k=1}^N \left( V_{\text{line}}[k] \times I_{\text{line}}[k] \right)$$

### 3.3 Conversion Efficiency Calculation
Every $100\,\text{ms}$, the MCU retrieves output power $P_{\text{DC}} = V_{\text{BUS}} \times I_{\text{shunt}}$ from the `INA226` and computes:
$$\eta = \left( \frac{P_{\text{DC}}}{P_{\text{AC}}} \right) \times 100\%$$

---

## 4. Module 7 Comprehensive Netlist

| Net Name | Origin Pin / Pad | Destination Pins / Pads | Net Class | Physical Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `+HV_BULK` | Bridge Rectifier Positive | Resistor `R_HV1` Pin 1 | High-Voltage DC | Creepage $\ge 3.0\,\text{mm}$ |
| `MAINS_DIV_SENSE`| Resistor `R_HV3` Pin 2 | `R_HV_BOT` Pin 1, `U4` Pin 2 (`INP`) | Analog Sense (HOT)| High-impedance node |
| `AMC_OUT_P` | `U4` Pin 7 (`OUTP`) | Differential Filter Input (+) | Differential Analog| Shielded balanced pair |
| `AMC_OUT_N` | `U4` Pin 6 (`OUTN`) | Differential Filter Input (-) | Differential Analog| Shielded balanced pair |
| `AMC1311_ADC_IN`| Active Filter Output | STM32 Pin 8 (`PC0`) | Analog Input | Filtered single-ended DC trace |
| `AC_LINE_FUSED` | Fuse `F1` Terminal | `CT1` Central Aperture Pass | AC Mains Live | Reinforced spacing |
| `CT_SEC_HI` | `CT1` Pin 1 | `R_burden` Pin 1, Low-pass filter | AC Sensor | Direct Kelvin trace |
| `VREF_1V65_BIAS`| Resistors `R_bias1`/`R_bias2`| `CT1` Pin 2, `R_burden` Pin 2, $1\,\mu\text{F}$ cap | DC Midpoint Ref | Low-impedance quiet analog trace |
| `CT_ADC_IN` | Low-pass filter output | STM32 Pin 9 (`PC1`) | Analog Input | Clean $1.65\,\text{V}$ centered AC trace |
| `SHUNT_SENSE_P` | `R_shunt` Kelvin Pad 1K | `U6` Pin 1 (`IN+`) | Kelvin Sense | Shielded differential pair |
| `SHUNT_SENSE_N` | `R_shunt` Kelvin Pad 2K | `U6` Pin 2 (`IN-`) | Kelvin Sense | Shielded differential pair |
| `+V_OUT` | Regulated DC Output | `U6` Pin 3 (`VBUS`) | Bus Voltage Sense | Connect after filter bank |
| `I2C1_SCL` | STM32 Pin 61 (`PB8`) | `U6` Pin 6 (`SCL`), Pull-up $2.2\,\text{k}\Omega$ | I2C Clock | $400\,\text{kHz}$ Fast-Mode |
| `I2C1_SDA` | STM32 Pin 62 (`PB9`) | `U6` Pin 5 (`SDA`), Pull-up $2.2\,\text{k}\Omega$ | I2C Data | $400\,\text{kHz}$ Fast-Mode |

---

## 5. Laboratory Bring-Up & Test Points
* **`TP_AMC_IN` (Mains Divider Sensed Voltage)**: Measure with DMM. Verify $1.144\,\text{V}_{\text{DC}}$ at $230\,\text{V}_{\text{AC RMS}}$ line ($1.865\,\text{V}$ peak at $265\,\text{V}$).
* **`TP_AMC_DIFF` (AMC1311 Differential Output)**: Measure differential voltage across `AMC_OUT_P` and `AMC_OUT_N`. Verify exact $1.000\,\text{V/V}$ tracking with $< 2.0\,\text{mV}$ offset.
* **`TP_CT_BIAS` (Midpoint Bias)**: Verify $+1.650\,\text{V}_{\text{DC}} \pm 0.5\%$ with DMM.
* **`TP_I2C_INA226` (Digital Bus Polling)**: Verify I2C acknowledge from Address `0x40`. Verify readback accuracy of $V_{\text{BUS}} \pm 0.1\%$ and $I_{\text{OUT}} \pm 0.2\%$.
""")

    print("Module 7 files successfully generated.")

if __name__ == "__main__":
    write_files()
