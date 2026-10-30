# Module 6 Equivalent Electronic Circuit: Supervisory MCU Core Subsystem

## 1. Subsystem Architecture Overview
Module 6 forms the central computational intelligence and supervisory brain of the Smart Programmable Power Supply (`VVDN_SPPS_2026`). Built around the high-performance STMicroelectronics **`STM32G474RET6`** ARM Cortex-M4 microcontroller running at $170.0\,\text{MHz}$, the subsystem coordinates five mission-critical operational domains:
1. **Precision Voltage DAC Steering**: Drives internal 12-bit DAC1 (Channel 1 on `PA4`) into the Stage 4 feedback summing junction to program output voltage with monotonic $3.655\,\text{mV}$ step resolution across $5.0\,\text{V}$ to $20.0\,\text{V}_{\text{DC}}$.
2. **Dual-Domain Telemetry & Live Efficiency Engine**: Periodically samples isolated primary AC mains voltage (via `AMC1311` on `PC0`) and line current (via `Talema AC1010` CT on `PC1`) using internal ADC1, while synchronously polling the secondary side `INA226` power monitor over I2C1 at a precision $10.0\,\text{Hz}$ rate ($100\,\text{ms}$ loop). The hardware FPU computes true RMS input power $P_{\text{AC}}$, output power $P_{\text{DC}}$, and real-time conversion efficiency $\eta$.
3. **Local User Interface Management**: Updates the $1.3\text{"}$ monochrome OLED display (`SSD1306` at I2C address `0x3C`) and decodes quadrature signals from dual Bourns rotary encoders (`ENC1` and `ENC2`) using hardware timers `TIM2` and `TIM3`.
4. **Supervisory Protection & Interlocks**: Monitors output voltage regulation, power boundaries, and thermal thresholds. Drives an active NPN pull-down transistor on `PB0` to force LM5176 shutdown within $500\,\text{ns}$ upon sustained fault conditions.
5. **External Serial Telemetry**: Emits ASCII-formatted telemetry frames at $115,200\,\text{baud}$ over `USART1` (Pins `PA9`/`PA10`) for automated bench testing and datalogging.

---

## 2. Full Schematic Electronic Circuit Diagram

```
========================================================================================================================
MODULE 6: SUPERVISORY MCU CORE & PERIPHERAL INTERFACE SCHEMATIC
========================================================================================================================

           +3V3_SEC ──[ 10kΩ ]──┬── Net: MCU_NRST
                                │
                             [100nF]
                                │
                            GND_SELV
                                │
                                ▼
                       [ U5: STM32G474RET6 LQFP-64 ]
                       ┌───────────────────────────┐
      Net: MCU_NRST ───┤[7]  NRST                  │
                       │                           │
     Net: OSC_IN    ───┤[5]  PF0/OSC_IN            │
    (From Y1 24MHz)    │                           │
     Net: OSC_OUT   ───┤[6]  PF1/OSC_OUT           │
    (Via 47Ω to Y1)    │                           │
                       │                           │
     Net: OSC32_IN  ───┤[3]  PC14/OSC32_IN         │
   (From Y2 32.768k)   │                           │
     Net: OSC32_OUT ───┤[4]  PC15/OSC32_OUT        │
                       │                           │
 Net: AMC1311_ADC_IN ──┤[8]  PC0 (ADC1_IN6)        │
 (Isolated AC Volt)    │                           │
  Net: CT_ADC_IN    ───┤[9]  PC1 (ADC1_IN7)        │
 (Isolated AC Curr)    │                           │
                       │                           │
Net: MCU_DAC1_OUT1  ───┤[20] PA4 (DAC1_OUT1)       ├───── To LM5176 FB Junction (Module 4)
                       │                           │
  Net: ENC1_CH_A    ───┤[14] PA0 (TIM2_CH1)        │
  Net: ENC1_CH_B    ───┤[15] PA1 (TIM2_CH2)        │
 Net: ENC1_PUSH_SW  ───┤[21] PA5 (GPIO In)         ├───── From Rotary Encoder 1 (Module 9)
                       │                           │
  Net: ENC2_CH_A    ───┤[22] PA6 (TIM3_CH1)        │
  Net: ENC2_CH_B    ───┤[23] PA7 (TIM3_CH2)        │
 Net: ENC2_PUSH_SW  ───┤[28] PB2 (GPIO In)         ├───── From Rotary Encoder 2 (Module 9)
                       │                           │
Net: LM5176_EN_CTRL ───┤[26] PB0 (GPIO Out)        ├─[ 4.7kΩ ]─(Base Q_EN MMBT3904)──> LM5176 EN
  Net: MCU_PGOOD    ───┤[27] PB1 (GPIO In)         ├─[ 10kΩ Pull-up ]─────────────────> LM5176 PGOOD
                       │                           │
   Net: LED_CV      ───┤[2]  PC13 (GPIO Out)       ├─[ 1.0kΩ ]─(Green LED)────────────> GND_SELV
   Net: LED_CC      ───┤[24] PC4 (GPIO Out)        ├─[ 1.0kΩ ]─(Amber LED)────────────> GND_SELV
  Net: LED_FAULT    ───┤[25] PC5 (GPIO Out)        ├─[ 1.0kΩ ]─(Red LED)──────────────> GND_SELV
                       │                           │
  Net: I2C1_SCL     ───┤[61] PB8 (I2C1_SCL)        ├─[ 2.2kΩ Pull-up ]────────────────> INA226 / OLED
  Net: I2C1_SDA     ───┤[62] PB9 (I2C1_SDA)        ├─[ 2.2kΩ Pull-up ]────────────────> INA226 / OLED
                       │                           │
  Net: USART1_TX    ───┤[42] PA9 (USART1_TX)       ├──────────────────────────────────> Header J5 Pin 1
  Net: USART1_RX    ───┤[43] PA10 (USART1_RX)      ├──────────────────────────────────> Header J5 Pin 2
                       │                           │
    Net: SWDIO      ───┤[46] PA13 (SWDIO)          ├──────────────────────────────────> Header J4 Pin 2
    Net: SWCLK      ───┤[49] PA14 (SWCLK)          ├─[ 100kΩ Pull-down ]──────────────> Header J4 Pin 3
                       │                           │
  Net: MCU_BOOT0    ───┤[60] BOOT0                 ├─[ 10kΩ Pull-down ]───────────────> GND_SELV
                       │                           │
                       │   VDD Pins: 19,32,48,64   ├───── 4x [ 100nF MLCC ]───────────> GND_SELV
                       │   VSS Pins: 18,31,47,63   ├──────────────────────────────────> GND_SELV
                       │   VDDA (Pin 13)           ├───── From +3V3_SEC via BLM18PG121 + 1µF
                       │   VSSA (Pin 12)           ├──────────────────────────────────> AGND_SEC
                       └───────────────────────────┘
```

---

## 3. Firmware Execution Architecture & Timing Loops

The supervisory firmware runs under a deterministic bare-metal or RTOS super-loop architecture synchronized by hardware timers:

```
+───────────────────────────────────────────────────────────────────────────────────+
| 100 ms Telemetry Loop Timer (TIM6 @ 10 Hz)                                        |
+───────────────────────────────────────────────────────────────────────────────────+
  │
  ├── 1. Read INA226 over I2C1 (V_OUT, I_OUT, P_DC)               --> Latency: 2.4 ms
  ├── 2. Trigger ADC1 DMA conversion (AMC1311 V_AC, CT1 I_AC)     --> Latency: 1.2 ms
  ├── 3. Math Accelerator: Calculate true RMS P_AC & Efficiency η --> Latency: 0.1 ms
  ├── 4. State Machine Evaluation (CV, CC, Fault check)           --> Latency: 0.05 ms
  ├── 5. Update SSD1306 OLED Frame Buffer (I2C1 Fast-Mode DMA)    --> Latency: 8.5 ms
  └── 6. Transmit Telemetry ASCII String over USART1 (115.2 kbps) --> Latency: 2.1 ms
                                                  Total Frame Time: 14.35 ms << 100 ms
```

---

## 4. Module 6 Comprehensive Netlist

| Net Name | Origin Pin / Pad | Destination Pins / Pads | Net Class | Physical Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `MCU_NRST` | STM32 Pin 7 (`NRST`) | Pull-up `R_PU_NRST`, Cap `C_NRST`, `SW_RST` | Reset Sense | Keep trace $< 10.0\,\text{mm}$ |
| `OSC_IN` | Crystal `Y1` Pin 1 | STM32 Pin 5 (`PF0-OSC_IN`), Cap $C_1$ ($27\,\text{pF}$) | High-Speed Clock | Guarded differential pair, length $< 6.0\,\text{mm}$ |
| `OSC_OUT` | STM32 Pin 6 (`PF1-OSC_OUT`)| Damping Resistor `R_damp` ($47\,\Omega$) | High-Speed Clock | Direct trace to damping resistor |
| `OSC_OUT_DAMP`| Resistor `R_damp` Pin 2 | Crystal `Y1` Pin 3, Cap $C_2$ ($27\,\text{pF}$) | High-Speed Clock | Keep trace short |
| `OSC32_IN` | Crystal `Y2` Pin 1 | STM32 Pin 3 (`PC14-OSC32_IN`), Cap $C_3$ ($18\,\text{pF}$) | Low-Speed Clock | Isolated high-Z analog trace |
| `OSC32_OUT` | Crystal `Y2` Pin 2 | STM32 Pin 4 (`PC15-OSC32_OUT`), Cap $C_4$ ($18\,\text{pF}$) | Low-Speed Clock | Isolated high-Z analog trace |
| `MCU_DAC1_OUT1`| STM32 Pin 20 (`PA4`) | Resistor `R_DAC` Pin 1 (Module 4) | Precision Analog | Low-impedance trace, filter cap $1\,\text{nF}$ |
| `AMC1311_ADC_IN`| Stage 7 Filter Output | STM32 Pin 8 (`PC0`) | Analog Input | Differential-to-single-ended filtered input |
| `CT_ADC_IN` | Stage 7 Burden Network | STM32 Pin 9 (`PC1`) | Analog Input | Biased AC signal ($1.65\,\text{V}_{\text{DC}}$ midpoint) |
| `LM5176_EN_CTRL`| STM32 Pin 26 (`PB0`)| Resistor $4.7\,\text{k}\Omega$ to `Q_EN` Base | Digital Control | Direct GPIO drive |
| `MCU_PGOOD` | STM32 Pin 27 (`PB1`)| Pull-up $10\,\text{k}\Omega$, LM5176 Pin 27 | Digital Input | Open-drain status monitoring |
| `LED_CV` | STM32 Pin 2 (`PC13`) | Current limiting resistor $1\,\text{k}\Omega$ to Green LED | Indicator | $1.5\,\text{mA}$ logic drive |
| `LED_CC` | STM32 Pin 24 (`PC4`) | Current limiting resistor $1\,\text{k}\Omega$ to Amber LED | Indicator | $1.5\,\text{mA}$ logic drive |
| `LED_FAULT` | STM32 Pin 25 (`PC5`) | Current limiting resistor $1\,\text{k}\Omega$ to Red LED | Indicator | $1.5\,\text{mA}$ logic drive |
| `I2C1_SCL` | STM32 Pin 61 (`PB8`) | Pull-up $2.2\,\text{k}\Omega$, `INA226` Pin 6, `SSD1306` Pin 3 | Fast-Mode I2C | Controlled rise time, length-matched |
| `I2C1_SDA` | STM32 Pin 62 (`PB9`) | Pull-up $2.2\,\text{k}\Omega$, `INA226` Pin 5, `SSD1306` Pin 4 | Fast-Mode I2C | Controlled rise time, length-matched |
| `USART1_TX` | STM32 Pin 42 (`PA9`) | Header `J5` Pin 1 | Serial Comm | Standard $3.3\,\text{V}$ UART |
| `USART1_RX` | STM32 Pin 43 (`PA10`)| Header `J5` Pin 2 | Serial Comm | Standard $3.3\,\text{V}$ UART |
| `SWDIO` | STM32 Pin 46 (`PA13`)| Header `J4` Pin 2 | Debug Bus | Bidirectional data line |
| `SWCLK` | STM32 Pin 49 (`PA14`)| Header `J4` Pin 3, Pull-down $100\,\text{k}\Omega$ | Debug Clock | Clock line with external pull-down |
| `MCU_BOOT0` | STM32 Pin 60 (`BOOT0`)| Pull-down $10\,\text{k}\Omega$ to `GND_SELV` | Boot Configuration | Guarantees deterministic Flash boot |

---

## 5. Laboratory Bring-Up & Test Points
* **`TP_3V3_MCU` (MCU Supply Rail)**: Verify stable $+3.30\,\text{V}_{\text{DC}} \pm 1.0\%$ with peak ripple $< 15\,\text{mV}_{\text{pk-pk}}$.
* **`TP_VDDA` (Analog Rail)**: Verify clean $+3.30\,\text{V}_{\text{DC}}$ with switching ripple $< 2.0\,\text{mV}_{\text{RMS}}$.
* **`TP_HSE` (24 MHz Oscillator)**: Probe `OSC_OUT` using an active FET probe ($< 1\,\text{pF}$ loading). Verify clean $24.000\,\text{MHz} \pm 10\,\text{ppm}$ sine/square wave.
* **`TP_SWD` (Firmware Flashing)**: Connect ST-LINK V3 probe to Header `J4`. Verify target MCU ID detection (`0x474`) and successful Flash programming.
* **`TP_UART_LOG` (Telemetry Stream)**: Connect $115,200\,\text{baud}$ FTDI serial cable to `J5`. Verify incoming telemetry string every $100\,\text{ms}$ formatted as:
  `[SPPS] VAC=230.1V IAC=0.31A PAC=66.2W VDC=20.00V IDC=3.00A PDC=60.0W EFF=90.6% STATE=CV`
