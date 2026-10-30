# Module 7 Equivalent Electronic Circuit: Dual-Domain Power Telemetry Subsystem

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
