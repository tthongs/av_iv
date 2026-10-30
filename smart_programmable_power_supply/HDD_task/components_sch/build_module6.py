#!/usr/bin/env python3
"""
Component and Schematic Connection Generator: Module 6 (Supervisory MCU Core)
"""

from pathlib import Path

OUT_DIR = Path("/home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/components_sch/module_06_supervisory_mcu_core")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def write_files():
    # 1. U5 STM32G474RET6 Microcontroller
    with open(OUT_DIR / "U5_stm32g474ret6_mcu.md", "w") as f:
        f.write(r"""# Component Schematic Specification: U5 (STM32G474RET6 Microcontroller)

## 1. Component Metadata
* **Reference Designator**: `U5`
* **Component Type**: High-Performance Mixed-Signal ARM Cortex-M4 Microcontroller
* **Manufacturer**: STMicroelectronics
* **Primary MPN**: `STM32G474RET6`
* **Alternate Manufacturer**: STMicroelectronics
* **Alternate MPN**: `STM32G473RET6` (Pin-compatible, reduced HRTIM features)
* **Package / Footprint**: LQFP-64 (Low-Profile Quad Flat Package, 64-lead, $10 \times 10\,\text{mm}$, Pitch: $0.50\,\text{mm}$)
* **Subsystem**: Stage 6 (Supervisory Intelligence, UI & Dual-Domain Telemetry Engine)

## 2. Electrical Ratings & Constraints
* **Operating Supply Voltage ($V_{\text{DD}}$ / $V_{\text{DDA}}$)**: $+1.71\,\text{V}$ to $+3.60\,\text{V}_{\text{DC}}$ (Operates from $+3.30\,\text{V}_{\text{DC}} \pm 1.0\%$ LDO rail).
* **Maximum Core Frequency**: $170.0\,\text{MHz}$ (delivers up to $213\,\text{DMIPS}$ / $550\,\text{CoreMark}$).
* **Memory Resources**:
  * Flash Memory: $512\,\text{kB}$ Dual-Bank with ECC (Bank 1: Application Firmware, Bank 2 upper sector: EEPROM emulation).
  * SRAM: $128\,\text{kB}$ total ($80\,\text{kB}$ SRAM1, $16\,\text{kB}$ SRAM2, $32\,\text{kB}$ CCM-SRAM for time-critical ISR routines).
* **Power Consumption**:
  * Run Mode ($170\,\text{MHz}$ with all peripherals active): $I_{\text{DD}} \approx 42.0\,\text{mA}$ ($138.6\,\text{mW}$ dissipation).
  * Low-Power Sleep / Idle: $< 8.5\,\text{mA}$.
* **Internal Analog Peripherals**:
  * 12-Bit DAC1 (Output 1 on `PA4`): Monotonic voltage steering into LM5176 FB junction.
  * 12-Bit ADC1 (Inputs on `PC0`, `PC1`): Primary AC mains voltage and current telemetry sampling at up to $4.0\,\text{MSPS}$.
* **Digital Peripherals**:
  * I2C1 (Fast-Mode $400\,\text{kHz}$ on `PB8`/`PB9`): Queries INA226 power monitor and updates SSD1306 OLED display.
  * USART1 ($115,200\,\text{baud}$ on `PA9`/`PA10`): Emits $10\,\text{Hz}$ telemetry data packet to external logging systems.
  * TIM2 / TIM3: Hardware Quadrature Decoders for dual rotary encoders.

## 3. Schematic Pin Connections & 64-Pin Net Mapping
| Pin # | Pin Name | Schematic Net Name | Functional Role / Connection |
| :---: | :---: | :--- | :--- |
| **1** | **`VBAT`** | `+3V3_SEC` | Battery backup domain; tied to $+3.30\,\text{V}$ rail with $100\,\text{nF}$ bypass cap. |
| **2** | **`PC13`** | `LED_CV` | GPIO Output: Constant Voltage Mode Green LED drive (via $1\,\text{k}\Omega$). |
| **3** | **`PC14-OSC32_IN`** | `OSC32_IN` | Low-Speed External Crystal `Y2` input ($32.768\,\text{kHz}$, $12.5\,\text{pF}$). |
| **4** | **`PC15-OSC32_OUT`**| `OSC32_OUT` | Low-Speed External Crystal `Y2` output ($32.768\,\text{kHz}$). |
| **5** | **`PF0-OSC_IN`** | `OSC_IN` | High-Speed External Crystal `Y1` input ($24.000\,\text{MHz}$, $18\,\text{pF}$). |
| **6** | **`PF1-OSC_OUT`**| `OSC_OUT` | High-Speed External Crystal `Y1` output ($24.000\,\text{MHz}$) via $47\,\Omega$ damping. |
| **7** | **`NRST`** | `MCU_NRST` | Active-low system reset; $10\,\text{k}\Omega$ pull-up to $3.3\text{V}$, $100\,\text{nF}$ filter cap. |
| **8** | **`PC0`** | `AMC1311_ADC_IN` | ADC1_IN6: Filtered analog input from AMC1311 primary AC voltage telemetry. |
| **9** | **`PC1`** | `CT_ADC_IN` | ADC1_IN7: Biased AC voltage from Talema AC1010 current transformer. |
| **10**| **`PC2`** | `NC` | Reserved analog test pad. |
| **11**| **`PC3`** | `NC` | Reserved analog test pad. |
| **12**| **`VSSA`** | `AGND_SEC` | Analog ground reference. Solid low-impedance star connection to ground. |
| **13**| **`VDDA`** | `+3V3A_ANALOG` | Analog supply rail; filtered via ferrite bead `FB1` + $1\,\mu\text{F} + 10\,\text{nF}$ MLCC. |
| **14**| **`PA0`** | `ENC1_CH_A` | TIM2_CH1: Rotary Encoder 1 Phase A input (RC debounced). |
| **15**| **`PA1`** | `ENC1_CH_B` | TIM2_CH2: Rotary Encoder 1 Phase B input (RC debounced). |
| **16**| **`PA2`** | `NC` | Unused GPIO; internal pull-down. |
| **17**| **`PA3`** | `NC` | Unused GPIO; internal pull-down. |
| **18**| **`VSS`** | `GND_SELV` | Digital ground reference (Layer 2 plane). |
| **19**| **`VDD`** | `+3V3_SEC` | Digital power supply pin 1; $100\,\text{nF}$ 0402 ceramic bypass cap. |
| **20**| **`PA4`** | `MCU_DAC1_OUT1`| DAC1_OUT1: Precision voltage steering output into LM5176 FB junction. |
| **21**| **`PA5`** | `ENC1_PUSH_SW` | GPIO Input: Rotary Encoder 1 push-button (Coarse/Fine voltage toggle). |
| **22**| **`PA6`** | `ENC2_CH_A` | TIM3_CH1: Rotary Encoder 2 Phase A input (RC debounced). |
| **23**| **`PA7`** | `ENC2_CH_B` | TIM3_CH2: Rotary Encoder 2 Phase B input (RC debounced). |
| **24**| **`PC4`** | `LED_CC` | GPIO Output: Constant Current Mode Amber LED drive (via $1\,\text{k}\Omega$). |
| **25**| **`PC5`** | `LED_FAULT` | GPIO Output: Fault Shutdown Red LED drive (via $1\,\text{k}\Omega$). |
| **26**| **`PB0`** | `LM5176_EN_CTRL`| GPIO Output: Controls LM5176 shutdown NPN pull-down transistor (`MMBT3904`). |
| **27**| **`PB1`** | `MCU_PGOOD` | GPIO Input: LM5176 Power Good status (with external $10\,\text{k}\Omega$ pull-up). |
| **28**| **`PB2`** | `ENC2_PUSH_SW` | GPIO Input: Rotary Encoder 2 push-button (Output Enable/Disable toggle). |
| **29**| **`PB10`**| `NC` | Unused GPIO; internal pull-down. |
| **30**| **`PB11`**| `NC` | Unused GPIO; internal pull-down. |
| **31**| **`VSS`** | `GND_SELV` | Digital ground reference (Layer 2 plane). |
| **32**| **`VDD`** | `+3V3_SEC` | Digital power supply pin 2; $100\,\text{nF}$ 0402 ceramic bypass cap. |
| **33**| **`PB12`**| `NC` | Unused GPIO; internal pull-down. |
| **34**| **`PB13`**| `NC` | Unused GPIO; internal pull-down. |
| **35**| **`PB14`**| `NC` | Unused GPIO; internal pull-down. |
| **36**| **`PB15`**| `NC` | Unused GPIO; internal pull-down. |
| **37**| **`PC6`** | `NC` | Reserved GPIO header tap. |
| **38**| **`PC7`** | `NC` | Reserved GPIO header tap. |
| **39**| **`PC8`** | `NC` | Reserved GPIO header tap. |
| **40**| **`PC9`** | `NC` | Reserved GPIO header tap. |
| **41**| **`PA8`** | `NC` | Unused GPIO; internal pull-down. |
| **42**| **`PA9`** | `USART1_TX` | USART1_TX: Telemetry serial output to Header `J5` (Pin 1, $115,200\,\text{baud}$). |
| **43**| **`PA10`**| `USART1_RX` | USART1_RX: Telemetry serial input from Header `J5` (Pin 2). |
| **44**| **`PA11`**| `NC` | Unused GPIO; internal pull-down. |
| **45**| **`PA12`**| `NC` | Unused GPIO; internal pull-down. |
| **46**| **`PA13`**| `SWDIO` | SWD Debug Data: Connects to Header `J4` (Pin 2). Internal pull-up. |
| **47**| **`VSS`** | `GND_SELV` | Digital ground reference (Layer 2 plane). |
| **48**| **`VDD`** | `+3V3_SEC` | Digital power supply pin 3; $100\,\text{nF}$ 0402 ceramic bypass cap. |
| **49**| **`PA14`**| `SWCLK` | SWD Debug Clock: Connects to Header `J4` (Pin 3). $100\,\text{k}\Omega$ pull-down. |
| **50**| **`PA15`**| `NC` | Unused GPIO; internal pull-down. |
| **51**| **`PC10`**| `NC` | Unused GPIO; internal pull-down. |
| **52**| **`PC11`**| `NC` | Unused GPIO; internal pull-down. |
| **53**| **`PC12`**| `NC` | Unused GPIO; internal pull-down. |
| **54**| **`PD2`** | `NC` | Unused GPIO; internal pull-down. |
| **55**| **`PB3`** | `SWO` | SWO Trace output: Connects to SWD debug pad for trace logging. |
| **56**| **`PB4`** | `NC` | Reserved GPIO. |
| **57**| **`PB5`** | `NC` | Reserved GPIO. |
| **58**| **`PB6`** | `NC` | Reserved GPIO. |
| **59**| **`PB7`** | `NC` | Reserved GPIO. |
| **60**| **`BOOT0`**| `MCU_BOOT0` | Boot configuration pin: Pulled LOW via $10\,\text{k}\Omega$ resistor to `GND_SELV`. |
| **61**| **`PB8`** | `I2C1_SCL` | I2C1_SCL: Fast-Mode clock ($400\,\text{kHz}$) to INA226 & SSD1306 ($2.2\,\text{k}\Omega$ pull-up). |
| **62**| **`PB9`** | `I2C1_SDA` | I2C1_SDA: Fast-Mode data ($400\,\text{kHz}$) to INA226 & SSD1306 ($2.2\,\text{k}\Omega$ pull-up). |
| **63**| **`VSS`** | `GND_SELV` | Digital ground reference (Layer 2 plane). |
| **64**| **`VDD`** | `+3V3_SEC` | Digital power supply pin 4; $100\,\text{nF}$ 0402 ceramic bypass cap. |

## 4. Schematic Symbol Representation
```
                        [ U5: STM32G474RET6 LQFP-64 MCU ]
                               ┌─────────────────┐
       Net: MCU_NRST  ────────[7] NRST     BOOT0 [60]─────── Net: MCU_BOOT0 (10k to GND)
       Net: OSC_IN    ────────[5] PF0/OSC_IN     │
       Net: OSC_OUT   ────────[6] PF1/OSC_OUT    │
       Net: OSC32_IN  ────────[3] PC14/OSC32_IN  │
       Net: OSC32_OUT ────────[4] PC15/OSC32_OUT │
                               │                 │
  Net: AMC1311_ADC_IN ────────[8] PC0 (ADC1_IN6) │
      Net: CT_ADC_IN  ────────[9] PC1 (ADC1_IN7) │
   Net: MCU_DAC1_OUT1 ───────[20] PA4 (DAC1_OUT1)│
                               │                 │
     Net: ENC1_CH_A   ───────[14] PA0 (TIM2_CH1) │
     Net: ENC1_CH_B   ───────[15] PA1 (TIM2_CH2) │
    Net: ENC1_PUSH_SW ───────[21] PA5 (GPIO)     │
     Net: ENC2_CH_A   ───────[22] PA6 (TIM3_CH1) │
     Net: ENC2_CH_B   ───────[23] PA7 (TIM3_CH2) │
    Net: ENC2_PUSH_SW ───────[28] PB2 (GPIO)     │
                               │                 │
   Net: LM5176_EN_CTRL───────[26] PB0 (GPIO)     │
     Net: MCU_PGOOD   ───────[27] PB1 (GPIO)     │
                               │                 │
       Net: LED_CV    ────────[2] PC13 (GPIO)    │
       Net: LED_CC    ───────[24] PC4 (GPIO)     │
     Net: LED_FAULT   ───────[25] PC5 (GPIO)     │
                               │                 │
      Net: I2C1_SCL   ───────[61] PB8 (I2C1_SCL) │
      Net: I2C1_SDA   ───────[62] PB9 (I2C1_SDA) │
      Net: USART1_TX  ───────[42] PA9 (USART1_TX)│
      Net: USART1_RX  ───────[43] PA10(USART1_RX)│
        Net: SWDIO    ───────[46] PA13(SWDIO)    │
        Net: SWCLK    ───────[49] PA14(SWCLK)    │
                               └─────────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Decoupling Array**: Each `VDD`/`VSS` pair (Pins 18/19, 31/32, 47/48, 63/64) must have a dedicated $100\,\text{nF}$ 0402 X7R ceramic bypass capacitor placed within $1.5\,\text{mm}$ of the package pins on Layer 1. Connect ground vias directly into the Layer 2 ground plane.
2. **Analog Plane Integrity**: Keep `VDDA` and `VSSA` strictly separated from digital switching noise. Route `+3V3A_ANALOG` through ferrite bead `FB1` and decouple with $1.0\,\mu\text{F}$ and $10\,\text{nF}$ ceramic capacitors directly at Pin 13.
3. **BOOT0 Pull-Down**: Solder a $10.0\,\text{k}\Omega$ pull-down resistor from Pin 60 (`BOOT0`) to `GND_SELV` immediately adjacent to the pin to ensure deterministic Flash memory booting upon power-up.
""")

    # 2. Y1 ABM8G 24MHz HSE Crystal
    with open(OUT_DIR / "Y1_abm8g_24mhz_crystal.md", "w") as f:
        f.write(r"""# Component Schematic Specification: Y1 (24.000 MHz HSE Master Crystal)

## 1. Component Metadata
* **Reference Designator**: `Y1`
* **Component Type**: High-Frequency Fundamental Quartz Crystal Resonator
* **Manufacturer**: Abracon LLC
* **Primary MPN**: `ABM8G-24.000MHZ-18-D2Y-T`
* **Alternate Manufacturer**: TXC Corporation
* **Alternate MPN**: `7M-24.000MAAJ-T` (24.000 MHz, 18 pF, 3.2 × 2.5 mm)
* **Package / Footprint**: SMD 4-Pad Ceramic Seam Seal ($3.2 \times 2.5\,\text{mm}$, Height: $0.8\,\text{mm}$)
* **Subsystem**: Stage 6 (Supervisory MCU Core Clocking Engine)

## 2. Electrical Ratings & Constraints
* **Nominal Frequency ($f_0$)**: $24.000\,\text{MHz}$ (Fundamental Mode)
* **Frequency Tolerance at $25^\circ\text{C}$**: $\pm 10.0\,\text{ppm}$
* **Frequency Stability over $-40^\circ\text{C}$ to $+85^\circ\text{C}$**: $\pm 20.0\,\text{ppm}$
* **Load Capacitance ($C_L$)**: $18.0\,\text{pF}$
* **Equivalent Series Resistance (ESR)**: $< 40.0\,\Omega$ max ($25.0\,\Omega$ typical)
* **Drive Level**: $10.0\,\mu\text{W}$ typical ($100.0\,\mu\text{W}$ max)
* **Load Capacitor Sizing Formulation**:
  $$C_L = \frac{C_1 \times C_2}{C_1 + C_2} + C_{\text{stray}}$$
  Assuming PCB stray capacitance $C_{\text{stray}} \approx 3.0\,\text{pF}$ and symmetric load capacitors $C_1 = C_2 = C_{\text{ext}}$:
  $$18.0\,\text{pF} = \frac{C_{\text{ext}}}{2} + 3.0\,\text{pF} \implies \frac{C_{\text{ext}}}{2} = 15.0\,\text{pF} \implies C_{\text{ext}} = \mathbf{30.0\,\text{pF}}$$
  Standard high-stability C0G/NP0 capacitor selection: $2x\ 27.0\,\text{pF} \pm 5\%$ 50V 0603 SMD (`Murata GRM1885C1H270JA01D`).
* **Series Damping Resistor ($R_{\text{damp}}$)**:
  A $47.0\,\Omega \pm 1\%$ 0603 resistor is inserted in series with the oscillator output (`OSC_OUT`) to limit crystal drive level below $50\,\mu\text{W}$ and prevent mechanical stress or harmonic overtone spurious oscillations.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Function | Schematic Net Name | Connected To | Solder / Trace Notes |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`XIN` (Crystal Input)** | `OSC_IN` | STM32 Pin 5 (`PF0-OSC_IN`), Load Cap $C_1$ ($27\,\text{pF}$) | $0.25\,\text{mm}$ trace, guarded. |
| **2** | **`GND` (Case Ground)** | `GND_SELV` | Secondary ground plane (Layer 2) | Thermal ground via. |
| **3** | **`XOUT` (Crystal Output)**| `OSC_OUT_DAMP` | Damping Resistor `R_damp` ($47\,\Omega$), Load Cap $C_2$ ($27\,\text{pF}$) | $0.25\,\text{mm}$ trace, guarded. |
| **4** | **`GND` (Case Ground)** | `GND_SELV` | Secondary ground plane (Layer 2) | Thermal ground via. |

## 4. Schematic Symbol Representation
```
                    [ Y1: ABRACON 24.000 MHz HSE CRYSTAL ]
                               ┌─────────────┐
        Net: OSC_IN     ──────[1] XIN    GND [4]────── Net: GND_SELV
        Net: GND_SELV   ──────[2] GND   XOUT [3]────── Net: OSC_OUT_DAMP
                               └─────────────┘
                                  24.000 MHz
                                       │
                                   [ 47 Ω ] R_damp
                                       │
                                Net: OSC_OUT (MCU Pin 6)
```

## 5. Schematic & PCB Layout Guidelines
1. **Ultra-Compact Loop**: Place `Y1`, $C_1$, $C_2$, and $R_{\text{damp}}$ directly beside Pins 5 and 6 of `U5`. Total trace length must be $< 6.0\,\text{mm}$.
2. **Ground Guard Ring**: Surround the entire oscillator tank circuit with a dedicated ground guard trace on Layer 1 tied with vias to the Layer 2 ground plane.
3. **Keepout Under Crystal**: Prohibit any digital signal, PWM line, or power rail routing on any PCB layer directly underneath the crystal resonator.
""")

    # 3. Y2 ABS07 32.768kHz LSE Crystal
    with open(OUT_DIR / "Y2_abs07_32khz_crystal.md", "w") as f:
        f.write(r"""# Component Schematic Specification: Y2 (32.768 kHz LSE RTC Crystal)

## 1. Component Metadata
* **Reference Designator**: `Y2`
* **Component Type**: Tuning Fork Low-Speed External Quartz Crystal Resonator
* **Manufacturer**: Abracon LLC
* **Primary MPN**: `ABS07-32.768KHZ-T`
* **Alternate Manufacturer**: Citizen Micro
* **Alternate MPN**: `CM7V-T1A-32.768KHZ` (12.5 pF, 3.2 × 1.5 mm)
* **Package / Footprint**: SMD 2-Pad Ultra-Miniature Ceramic ($3.2 \times 1.5\,\text{mm}$, Height: $0.9\,\text{mm}$)
* **Subsystem**: Stage 6 (Real-Time Telemetry Loop Timekeeping Engine)

## 2. Electrical Ratings & Constraints
* **Nominal Frequency ($f_0$)**: $32.768\,\text{kHz}$ (Tuning Fork)
* **Frequency Tolerance at $25^\circ\text{C}$**: $\pm 20.0\,\text{ppm}$
* **Load Capacitance ($C_L$)**: $12.5\,\text{pF}$
* **Equivalent Series Resistance (ESR)**: $< 70.0\,\text{k}\Omega$ max ($55.0\,\text{k}\Omega$ typical)
* **Shunt Capacitance ($C_0$)**: $1.0\,\text{pF}$ typical
* **Drive Level**: $0.1\,\mu\text{W}$ typical ($0.5\,\mu\text{W}$ max)
* **Load Capacitor Calculation**:
  $$C_L = \frac{C_3 \times C_4}{C_3 + C_4} + C_{\text{stray}}$$
  With $C_{\text{stray}} \approx 2.5\,\text{pF}$:
  $$12.5\,\text{pF} - 2.5\,\text{pF} = 10.0\,\text{pF} \implies C_3 = C_4 = \mathbf{20.0\,\text{pF}}$$
  Selected standard capacitors: $2x\ 18.0\,\text{pF} \pm 5\%$ 50V C0G 0603 (`Murata GRM1885C1H180JA01D`).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Function | Schematic Net Name | Connected To | Solder / Trace Notes |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`XIN`** | `OSC32_IN` | STM32 Pin 3 (`PC14-OSC32_IN`), Load Cap $C_3$ ($18\,\text{pF}$) | High-Z trace, keep $< 5.0\,\text{mm}$. |
| **2** | **`XOUT`**| `OSC32_OUT`| STM32 Pin 4 (`PC15-OSC32_OUT`), Load Cap $C_4$ ($18\,\text{pF}$) | High-Z trace, keep $< 5.0\,\text{mm}$. |

## 4. Schematic Symbol Representation
```
                    [ Y2: ABRACON 32.768 kHz LSE RTC CRYSTAL ]
                               ┌─────────────┐
        Net: OSC32_IN   ──────[1]   32.768  [2]────── Net: OSC32_OUT
                               │     kHz     │
                               └─────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Ultra-High Impedance Node Protection**: The $32.768\,\text{kHz}$ tuning-fork circuit operates at nanoampere currents. Moisture, flux residue, or adjacent switching tracks will induce frequency drift or stall oscillations. Enclose completely within an analog ground shield guard ring.
""")

    # 4. MCU Decoupling and Analog Filtering
    with open(OUT_DIR / "MCU_DECOUPLING_filters.md", "w") as f:
        f.write(r"""# Component Schematic Specification: MCU Decoupling & Analog Power Filters

## 1. Subsystem Metadata
* **Subsystem**: Stage 6 (STM32G474 Power Integrity & Noise Decoupling Subsystem)
* **Supply Rails Covered**:
  * Digital Supply Domain: `+3V3_SEC` ($+3.30\,\text{V}_{\text{DC}}$)
  * Analog Supply Domain: `+3V3A_ANALOG` ($+3.30\,\text{V}_{\text{DC}}$ filtered)
  * Reference Voltage Domain: `VREF+` (Tied to `+3V3A_ANALOG`)

## 2. Decoupling Component Sizing & Bill of Materials
| Ref Des | Component Description | Value / Rating | Footprint | Primary MPN | Placement Location |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **`C_VDD1`** | High-Frequency Bypass MLCC | $100\,\text{nF}, 16\,\text{V}, \text{X7R}$ | 0402 SMD | Murata `GRM155R71C104KA88D` | Pin 19 (`VDD1`) / Pin 18 (`VSS1`) |
| **`C_VDD2`** | High-Frequency Bypass MLCC | $100\,\text{nF}, 16\,\text{V}, \text{X7R}$ | 0402 SMD | Murata `GRM155R71C104KA88D` | Pin 32 (`VDD2`) / Pin 31 (`VSS2`) |
| **`C_VDD3`** | High-Frequency Bypass MLCC | $100\,\text{nF}, 16\,\text{V}, \text{X7R}$ | 0402 SMD | Murata `GRM155R71C104KA88D` | Pin 48 (`VDD3`) / Pin 47 (`VSS3`) |
| **`C_VDD4`** | High-Frequency Bypass MLCC | $100\,\text{nF}, 16\,\text{V}, \text{X7R}$ | 0402 SMD | Murata `GRM155R71C104KA88D` | Pin 64 (`VDD4`) / Pin 63 (`VSS4`) |
| **`C_VBAT`** | Battery Domain Bypass MLCC | $100\,\text{nF}, 16\,\text{V}, \text{X7R}$ | 0402 SMD | Murata `GRM155R71C104KA88D` | Pin 1 (`VBAT`) |
| **`C_BULK_MCU`**| MCU Bulk Reservoir MLCC | $4.7\,\mu\text{F}, 10\,\text{V}, \text{X7R}$ | 0805 SMD | Murata `GRM21BR71A475KA73L` | Adjacent to Pin 64 |
| **`FB1`** | Analog Domain Ferrite Bead | $120\,\Omega \text{ at } 100\,\text{MHz}, 1.5\,\text{A}$ | 0603 SMD | Murata `BLM18PG121SN1D` | Between `+3V3_SEC` and `+3V3A_ANALOG` |
| **`C_VDDA1`**| Analog High-Frequency Bypass| $10\,\text{nF}, 25\,\text{V}, \text{C0G}$ | 0603 SMD | Murata `GRM1885C1E103JA01D` | Pin 13 (`VDDA`) / Pin 12 (`VSSA`) |
| **`C_VDDA2`**| Analog Medium-Freq Bypass | $1.0\,\mu\text{F}, 16\,\text{V}, \text{X7R}$ | 0603 SMD | Murata `GRM188R71C105KA12D` | Pin 13 (`VDDA`) / Pin 12 (`VSSA`) |

## 3. Schematic Symbol Representation
```
                    [ MCU POWER DECOUPLING & ANALOG PI-FILTER ]

    Net: +3V3_SEC ──┬──────────────┬──────────────┬──────────────┬──────┐
                    │              │              │              │      │
                 [100nF]        [100nF]        [100nF]        [100nF] [4.7µF]
                 (Pin 19)       (Pin 32)       (Pin 48)       (Pin 64)  │
                    │              │              │              │      │
    Net: GND_SELV ──┴──────────────┴──────────────┴──────────────┴──────┘

    Net: +3V3_SEC ──[ FB1: BLM18PG121 ]──┬── Net: +3V3A_ANALOG (Pin 13 VDDA)
                                         │
                                      [10nF C0G]   [1.0µF X7R]
                                         │              │
    Net: AGND_SEC ───────────────────────┴──────────────┴────── (Pin 12 VSSA)
```
""")

    # 5. MCU Reset Circuit
    with open(OUT_DIR / "MCU_RESET_CIRCUIT.md", "w") as f:
        f.write(r"""# Component Schematic Specification: MCU_RESET (STM32 NRST Supervisory Circuit)

## 1. Component Metadata
* **Subsystem**: Stage 6 (System Hardware Reset & Brown-Out Reset Protection)
* **Active Components**: Passive RC timing network with optional manual tactile push-button `SW_RST`.
* **Values**:
  * Pull-Up Resistor: $R_{\text{PU_NRST}} = 10.0\,\text{k}\Omega \pm 1\%$ (0603 SMD, Vishay `CRCW060310K0FKEA`)
  * Filter Capacitor: $C_{\text{NRST}} = 100.0\,\text{nF} \pm 10\%$ 50V X7R (0603 SMD, Murata `GRM188R71H104KA93D`)
  * Manual Reset Switch: Tactile SPST normally open SMD switch (C&K `PTS645SL43-2 LFS`)

## 2. Electrical Operation & Timing
* **Reset Threshold ($V_{\text{IL,max}}$)**: $< 0.3 \times V_{\text{DD}} = 0.99\,\text{V}$
* **Reset Release Threshold ($V_{\text{IH,min}}$)**: $> 0.7 \times V_{\text{DD}} = 2.31\,\text{V}$
* **Power-On Reset Time Constant ($\tau$)**:
  $$\tau = R_{\text{PU_NRST}} \times C_{\text{NRST}} = (10.0\,\text{k}\Omega) \times (100.0\,\text{nF}) = \mathbf{1.0\,\text{ms}}$$
  * Guarantees that the reset line remains held LOW during supply voltage ramp-up until $V_{\text{DD}}$ stabilizes well above the internal brown-out reset threshold ($V_{\text{BOR0}} = 1.71\,\text{V}$).
* **Manual Reset**: Pressing `SW_RST` grounds Pin 7 (`NRST`), discharging $C_{\text{NRST}}$ through an internal $40\,\Omega$ ESD clamp and triggering instantaneous CPU re-initialization.

## 3. Schematic Symbol Representation
```
                      [ STM32 NRST SUPERVISORY RESET CIRCUIT ]
                                  Net: +3V3_SEC
                                        │
                                      ┌─┴─┐
                                      │   │ R_PU_NRST (10.0 kΩ ±1%)
                                      └─┬─┘
                                        │
    MCU Pin 7 (NRST) ───────────────────┼────────── Net: MCU_NRST
                                        │
                                 ┌──────┴──────┐
                                 │             │
                              ┌──┴──┐       ┌──o  o──┐
                              │     │       │  SW_RST│ (Tactile Pushbutton)
                              └──┬──┘       └──o──o──┘
                                 │             │
    Net: GND_SELV    ────────────┴─────────────┴──────────────
                              C_NRST (100 nF)
```
""")

    # 6. Module 6 Equivalent Circuit Document
    with open(OUT_DIR / "module_06_supervisory_mcu_equivalent_circuit.md", "w") as f:
        f.write(r"""# Module 6 Equivalent Electronic Circuit: Supervisory MCU Core Subsystem

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
""")

    print("Module 6 files successfully generated.")

if __name__ == "__main__":
    write_files()
