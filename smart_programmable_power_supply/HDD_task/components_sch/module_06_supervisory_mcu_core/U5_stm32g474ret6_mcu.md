# Component Schematic Specification: U5 (STM32G474RET6 Microcontroller)

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
