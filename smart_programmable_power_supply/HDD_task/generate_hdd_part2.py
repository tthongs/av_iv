#!/usr/bin/env python3
"""
HDD Generator Part 2: Sections 5 to 12
"""

def get_sections_5_to_7():
    return """---

# 5. Digital Interface Design

## 5.1 Subsystem1 [Main Board]

### 5.1.1 Module1: STM32G474RET6 Microcontroller
The STMicroelectronics `STM32G474RET6` mixed-signal MCU serves as the supervisory intelligence of the SPPS board. It coordinates the user interface, executes the $10\,\text{Hz}$ telemetry loop, computes real-time efficiency, commands the 12-bit DAC steering network, and provides supervisor-level fault protection.

#### Boot Strapping
The STM32G474RET6 boot configuration is determined by the logic state of the `BOOT0` pin and internal Flash option bytes. To ensure deterministic operation in high-noise power environments, `BOOT0` is tied to ground through a dedicated pull-down resistor:

### Table 4: Boot Strapping Pin Table
| BOOT0 Pin State | nBOOT1 Option Bit | Boot Mode Selected | Target Memory Space | Engineering Implementation / Selection |
| :---: | :---: | :--- | :--- | :--- |
| **0 (GND)** | **X** | **Main Flash Memory** | **Bank 1 (0x0800 0000)** | **DEFAULT HARDWARE BASELINE: 10 kΩ pull-down to GND. Boots primary application firmware.** |
| 1 (VDD) | 1 | System Memory | System ROM (0x1FFF 0000) | Factory bootloader mode (DFU via USART1). Accessible via 3-pin jumper `JP3`. |
| 1 (VDD) | 0 | Embedded SRAM | SRAM1 (0x2000 0000) | Debug SRAM execution. Not used in production. |

#### Memory Interface
The STM32G474RET6 integrates internal high-speed memories with zero wait-state read capability using the ST ART Accelerator:
* **Flash Memory**: $512\,\text{kB}$ organized as dual banks of $256\,\text{kB}$ each ($2\,\text{kB}$ page size, 10,000 write/erase cycles endurance, $> 20$ years data retention at $85^\circ\text{C}$). Bank 1 hosts the core application firmware ($< 120\,\text{kB}$ footprint), while the upper $16\,\text{kB}$ sector is reserved for EEPROM emulation to persist user setpoints, voltage calibration offsets, and fault history logs.
* **Embedded SRAM**: $128\,\text{kB}$ total internal SRAM partitioned into $80\,\text{kB}$ SRAM1, $16\,\text{kB}$ SRAM2, and $32\,\text{kB}$ CCM (Core Coupled Memory) data RAM with hardware parity check. The CCM RAM executes critical ADC sampling ISRs and math routines with zero bus arbitration latency.

#### Programming Interface
The PCBA provides an onboard 4-pin shrouded $2.54\,\text{mm}$ Serial Wire Debug (SWD) header (`J4`) for production flashing and in-circuit emulation:
* **Pin 1**: `+3.3V_VDD` (Target reference supply)
* **Pin 2**: `SWDIO` (PA13, internal pull-up)
* **Pin 3**: `SWCLK` (PA14, internal pull-down, external $100\,\text{k}\Omega$ pull-down to GND)
* **Pin 4**: `GND` (Secondary SELV ground)
* The active-low reset signal (`NRST`) is supervised by an external RC filter ($10\,\text{k}\Omega$ pull-up to $+3.3\,\text{V}$, $100\,\text{nF}$ ceramic capacitor to ground).

#### Peripheral Interface
* **I2C1 Bus Interface (Fast-Mode 400 kHz)**:
  * Connects STM32 `PB8` (`I2C1_SCL`) and `PB9` (`I2C1_SDA`) to the `INA226AIDGSR` secondary power monitor (Address `0x40`) and the $1.3\text{"}$ OLED display controller `SSD1306` (Address `0x3C`).
  * Total bus capacitance is estimated at $C_{\text{bus}} \approx 35\,\text{pF}$ (PCB trace capacitance $\approx 15\,\text{pF}$, pin input capacitance $\approx 20\,\text{pF}$).
  * Pull-up resistors $R_p = 2.2\,\text{k}\Omega \pm 1\%$ (`R_PU1`, `R_PU2`) are tied to $+3.3\,\text{V}$.
  * Bus rise time: $t_r = 0.8473 \times R_p \times C_{\text{bus}} = 0.8473 \times 2200\,\Omega \times 35 \times 10^{-12}\,\text{F} = 65.2\,\text{ns}$, well within the I2C Fast-Mode maximum limit ($t_{r,\text{max}} = 300\,\text{ns}$).
  * High-level noise margin exceeds $1.8\,\text{V}$ ($V_{\text{IH,min}} = 2.31\,\text{V}$).
* **USART1 Serial Telemetry Interface**:
  * Pins `PA9` (`USART1_TX`) and `PA10` (`USART1_RX`) route to a dedicated 3-pin $2.54\,\text{mm}$ header (`J5`) operating at $115,200\,\text{baud}$, 8 data bits, no parity, 1 stop bit ($8\text{N}1$). Emits an ASCII telemetry string once every $100\,\text{ms}$ ($10.0\,\text{Hz}$) containing $V_{\text{AC}}$, $I_{\text{AC}}$, $P_{\text{AC}}$, $V_{\text{OUT}}$, $I_{\text{OUT}}$, $P_{\text{DC}}$, and efficiency $\eta$.

#### GPIO Interface
* **LM5176 Supervisory Enable**: STM32 pin `PB0` drives the base of an NPN transistor (`MMBT3904`) through a $4.7\,\text{k}\Omega$ series resistor. When `PB0` is driven HIGH, the NPN pulls the LM5176 `ENABLE` pin (Pin 6) below $0.2\,\text{V}$, instantly inhibiting gate drive pulses.
* **Rotary Encoders**: Pins `PA0`/`PA1` (Encoder 1) and `PA6`/`PA7` (Encoder 2) connect to external Bourns mechanical encoders with onboard $10\,\text{k}\Omega$ pull-ups and $10\,\text{nF}$ ceramic RC low-pass debouncing filters ($\tau = 100\,\mu\text{s}$), feeding hardware timer quadrature decoder inputs (`TIM2` and `TIM3`).
* **Front-Panel Status LEDs**: Pins `PC6` (Green - CV Mode), `PC7` (Amber - CC Clamped Mode), and `PC8` (Red - Fault / Trip) drive low-current SMD LEDs through $1.0\,\text{k}\Omega$ current-limiting resistors ($I_{\text{LED}} \approx 1.5\,\text{mA}$).

---

# 6. RF Design

## 6.1 Subsystem1 [Main Board]
**Engineering Status: NOT APPLICABLE (Out of Scope per PRD Baseline)**

* **Design Scope & Regulatory Justification**:
  * The Smart Programmable Power Supply (`VVDN_SPPS_2026`) is a purely wired AC-to-DC laboratory power supply and modular ATE bench instrument.
  * In strict compliance with the authoritative PRD ([`prd_final_spps.docx`](../PRD_task/reference_docs/prd_final_spps.docx), Section 10 "Out of Scope"), wireless transceivers (Wi-Fi, Bluetooth, BLE, Zigbee, Cellular, or LoRa) are intentionally excluded from the hardware architecture.
  * Unintentional radiated RF emissions from the high-frequency switching cells ($65.0\,\text{kHz}$ Flyback and $300.0\,\text{kHz}$ Buck-Boost) are suppressed to strictly below CISPR 32 / EN 55032 Class B commercial radiated emission limits via:
    1. Four-layer balanced PCB stackup featuring continuous, low-impedance ground planes.
    2. Minimization of high-current di/dt switching loops to $< 1.5\,\text{cm}^2$.
    3. Fully shielded flat-wire power inductor (`Wurth 7443321000`) and ferrite-shielded transformer (`PQ26/20`).
    4. Two-stage common-mode LC input EMI filtering and RC snubber damping on switching nodes.

---

# 7. Analog Design

## 7.1 Subsystem1 [Main Board]

### 7.1.1 Module1: 12-Bit DAC Precision Voltage Steering Network
The LM5176 regulates output voltage by modulating its 4-switch H-bridge to maintain its feedback pin (`FB`, Pin 24) at an internal bandgap reference voltage of $V_{\text{REF}} = 1.200\,\text{V}_{\text{DC}}$. 

Rather than altering the internal reference, an active resistive summing junction is implemented at the `FB` node. The STM32G474 internal 12-bit DAC channel (`DAC1_OUT1`, Pin `PA4`) injects or extracts current into the summing junction through resistor $R_{\text{DAC}}$, steering the regulated output voltage $V_{\text{OUT}}$ smoothly from $5.0\,\text{V}$ to $20.0\,\text{V}_{\text{DC}}$:

```
                  V_OUT
                    │
                  ┌─┴─┐
                  │R_top│  (49.9 kΩ, 0.1%)
                  └─┬─┘
                    │
                    ├─── FB Node (LM5176 Pin 24, V_REF = 1.200V)
                    │
         ┌──────────┼──────────┐
         │          │          │
       ┌─┴─┐      ┌─┴─┐      ┌─┴─┐
       │R_bot│    │R_DAC│    │C_ff│  (15 pF Feedforward)
       └─┬─┘      └─┬─┘      └─┬─┘
         │          │          │
        GND       V_DAC       GND
               (0V - 3.3V)
```

#### Governing Nodal Equation
Applying Kirchhoff's Current Law (KCL) at the `FB` node:
$$\\frac{V_{\\text{OUT}} - V_{\\text{REF}}}{R_{\\text{top}}} = \\frac{V_{\\text{REF}}}{R_{\\text{bot}}} + \\frac{V_{\\text{REF}} - V_{\\text{DAC}}}{R_{\\text{DAC}}}$$

Solving explicitly for $V_{\\text{OUT}}$:
$$V_{\\text{OUT}} = V_{\\text{REF}} \\left( 1 + \\frac{R_{\\text{top}}}{R_{\\text{bot}}} + \\frac{R_{\\text{top}}}{R_{\\text{DAC}}} \\right) - V_{\\text{DAC}} \\left( \\frac{R_{\\text{top}}}{R_{\\text{DAC}}} \\right)$$

#### Component Sizing & Values
To maximize noise immunity and eliminate DC loading errors on the internal DAC output buffer, standard $0.1\%$ thin-film SMD resistors (Vishay Dale `TNPW0805`, $\\text{TCR} < 25\\,\\text{ppm}/^\\circ\\text{C}$) are selected:
* $V_{\\text{REF}} = 1.200\\,\\text{V}_{\\text{DC}}$ (LM5176 internal bandgap reference)
* $R_{\\text{top}} = 49.9\\,\\text{k}\\Omega \\pm 0.1\\%$ (`TNPW080549K9BEEA`)
* $R_{\\text{bot}} = 4.48\\,\\text{k}\\Omega \\pm 0.1\\%$ (`TNPW08054K48BEEA`)
* $R_{\\text{DAC}} = 11.0\\,\\text{k}\\Omega \\pm 0.1\\%$ (`TNPW080511K0BEEA`)

#### Mathematical Verification Across Operating Envelope
1. **Upper Setpoint ($V_{\\text{OUT}} = 20.0\\,\\text{V}$)**: Command $V_{\\text{DAC}} = 0.000\\,\\text{V}$:
   $$V_{\\text{OUT}} = 1.200 \\left( 1 + \\frac{49.9}{4.48} + \\frac{49.9}{11.0} \\right) - 0.000 = 1.200 \\left( 1 + 11.1384 + 4.5364 \\right) = 1.200 \\times 16.6748 = \\mathbf{20.01\\,\\text{V}_{\\text{DC}}}$$
2. **Nominal Mid-Point ($V_{\\text{OUT}} = 12.5\\,\\text{V}$)**: Command $V_{\\text{DAC}} = 1.650\\,\\text{V}$:
   $$V_{\\text{OUT}} = 20.01 - 1.650 \\left( \\frac{49.9}{11.0} \\right) = 20.01 - 1.650 \\times 4.5364 = 20.01 - 7.485 = \\mathbf{12.525\\,\\text{V}_{\\text{DC}}}$$
3. **Lower Setpoint ($V_{\\text{OUT}} = 5.0\\,\\text{V}$)**: Command $V_{\\text{DAC}} = 3.300\\,\\text{V}$:
   $$V_{\\text{OUT}} = 20.01 - 3.300 \\left( 4.5364 \\right) = 20.01 - 14.97 = \\mathbf{5.04\\,\\text{V}_{\\text{DC}}}$$

#### Monotonic Digital Resolution
The STM32G474 12-bit DAC features $2^{12} = 4096$ quantization codes spanning $0.0\\,\\text{V}$ to $+3.30\\,\\text{V}$ ($V_{\\text{LSB}} = 3.30\\,\\text{V} / 4096 = 805.7\\,\\mu\\text{V}$). The resulting output voltage step resolution is:
$$\\Delta V_{\\text{OUT,step}} = V_{\\text{LSB}} \\times \\left( \\frac{R_{\\text{top}}}{R_{\\text{DAC}}} \\right) = (805.7\\,\\mu\\text{V}) \\times \\left( \\frac{49.9\\,\\text{k}\\Omega}{11.0\\,\\text{k}\\Omega} \\right) = \\mathbf{3.655\\,\\text{mV per step}}$$
This guarantees monotonic, jitter-free tuning that exceeds the PRD requirement (<= 10.0 mV step resolution) by nearly 3x.

### 7.1.2 Module2: Sub-5µs Fast Hardware Current Limit Clamping
To protect the BSC034N04LS switching MOSFETs from destructive avalanche breakdown during a dead short circuit, an autonomous analog hardware current clamp is implemented directly on the PCBA, operating completely independent of firmware:
1. **Precision Metal Current Sense Shunt ($R_{\\text{shunt}}$)**: Bourns `CSS2H-2512R-L010F` ($10.0\\,\\text{m}\\Omega \\pm 0.1\\%$, $3.0\\,\\text{W}$, 2512 package, $\\text{TCR} < 50\\,\\text{ppm}/^\\circ\\text{C}$). Senses total load current directly in the return path.
2. **Current Sense Amplifier (`U7`)**: Texas Instruments `INA240A2EDCKR` (enhanced PWM common-mode rejection, fixed gain $A_v = 50.0\\,\\text{V/V}$, bandwidth $400\\,\\text{kHz}$):
   $$V_{\\text{CS,out}} = I_{\\text{OUT}} \\times R_{\\text{shunt}} \\times A_v = I_{\\text{OUT}} \\times (0.010\\,\\Omega) \\times 50.0 = I_{\\text{OUT}} \\times 0.500\\,\\text{V/A}$$
   * At $I_{\\text{OUT}} = 3.0\\,\\text{A}$ (Full Load): $V_{\\text{CS,out}} = 1.500\\,\\text{V}$.
   * At $I_{\\text{OUT}} = 3.20\\,\\text{A}$ (Hardware Trip Setpoint): $V_{\\text{CS,out}} = 1.600\\,\\text{V}$.
3. **High-Speed Analog Comparator (`U8`)**: Texas Instruments `TLV3501AIDBVR` (push-pull rail-to-rail output, propagation delay $t_{\\text{pd}} = 4.5\\,\\text{ns}$). The inverting input is biased to $1.600\\,\\text{V}$ via a precision divider from $+3.3\\,\\text{V}$.
4. **COMP Pin Pull-Down Transistor**: Diodes Inc. `MMBT3904` NPN transistor connected from LM5176 `COMP` (Pin 25) to quiet analog ground.
5. **Total Autonomous Clamping Latency Breakdown**:
   * Current trip threshold exceeded ($I_{\\text{OUT}} > 3.2\\,\\text{A}$): $t = 0$
   * INA240 amplifier output slew to $1.60\\,\\text{V}$ ($400\\,\\text{kHz}$ BW): $1.20\\,\\mu\\text{s}$
   * TLV3501 comparator trip and transition: $4.5\\,\\text{ns}$
   * MMBT3904 base turn-on and collector saturation: $250\\,\\text{ns}$
   * LM5176 internal error amplifier compensation discharge, duty cycle truncation: $800\\,\\text{ns}$
   * **Total Response Time**: $\\mathbf{2.25\\,\\mu\\text{s}} \\ll \\mathbf{5.0\\,\\mu\\text{s}}$ (Guaranteed safe envelope!).

### 7.1.3 Module3: Primary Isolated AC Voltage & Current Telemetry
To measure primary AC power ($P_{\\text{AC}}$) while maintaining certified $3000\\,\\text{V}_{\\text{RMS}}$ reinforced galvanic isolation:
* **Isolated Primary Voltage Sensing (`U4`)**: Texas Instruments `AMC1311BDWVR` (SOIC-8 Wide, $5.85\\,\\text{mm}$ creepage, $7000\\,\\text{V}_{\\text{peak}}$ reinforced isolation, differential $2.0\\,\\text{V}$ input range). A high-voltage divider ($1.5\\,\\text{M}\\Omega$ string of three $500\\,\\text{k}\\Omega$ 1206 resistors in series, and a $7.5\\,\\text{k}\\Omega$ bottom resistor) scales full-scale $375\\,\\text{V}_{\\text{peak}}$ down to $1.86\\,\\text{V}$, feeding the AMC1311 input. The isolated differential output is low-pass filtered and sampled by STM32 ADC channels.
* **Primary Current Sensing (`CT1`)**: Talema `AC1010` encapsulated current transformer ($1000:1$ turns ratio, $10.0\\,\\text{A}_{\\text{RMS}}$ rating, $4000\\,\\text{V}_{\\text{RMS}}$ isolation). Senses AC mains Live current. Secondary current ($I_{\\text{sec}} = I_{\\text{pri}} / 1000 = 1.60\\,\\text{mA}$ at $1.60\\,\\text{A}_{\\text{RMS}}$) flows through a precision $100.0\\,\\Omega \\pm 0.1\\%$ thin-film burden resistor (`R_burden`, Vishay Dale `TNPW0805100R`), generating an AC signal of $160.0\\,\\text{mV}_{\\text{RMS}}$ biased at $+1.65\\,\\text{V}_{\\text{DC}}$ midpoint, sampled by the STM32 ADC.

### 7.1.4 Module4: Secondary DC Power Telemetry
* Texas Instruments `INA226AIDGSR` (16-bit I2C power monitor, VSSOP-10) is placed on the secondary side to sample load telemetry.
* Connected differentially across the $10.0\\,\\text{m}\\Omega$ Bourns shunt resistor `R_shunt`.
* Shunt voltage LSB: $2.5\\,\\mu\\text{V}$, yielding current resolution of $250\\,\\mu\\text{A}$ ($0.25\\,\\text{mA}$).
* Bus voltage LSB: $1.25\\,\\text{mV}$, full-scale range $36.0\\,\\text{V}$.
* Programmed via I2C for 16-sample averaging ($1.1\\,\\text{ms}$ conversion time per channel). Emits calibrated voltage, current, and computed DC load power ($P_{\\text{DC}}$) at $10.0\\,\\text{Hz}$ rate.
"""

def get_sections_8_to_12():
    return """---

# 8. Power Design

## 8.1 Subsystem1 Power Architecture
The SPPS power architecture comprises a four-stage conversion topology feeding secondary post-regulation and auxiliary housekeeping rails:

```mermaid
flowchart TD
    AC["Universal AC Mains<br/>85V - 265V AC RMS"] --> STAGE1["Stage 1: Input Protection & EMI<br/>Fuse (2A), NTC (15Ω), MOV (300V), 2-Stage Filter"]
    STAGE1 --> STAGE2["Stage 2: Rectifier & Bulk Link<br/>GBU606 Bridge + 100µF/450V Electrolytic"]
    STAGE2 --> HVDC["High-Voltage DC Link<br/>+120V to +375V DC"]
    HVDC --> STAGE3["Stage 3: Galvanically Isolated Flyback<br/>PQ26/20 Core (3C95), IPB80R290P7 CoolMOS, MBR10100 Diode"]
    STAGE3 --> BUS24["+24.0V DC Intermediate Rail<br/>(72W Continuous / 84W Peak)"]
    BUS24 --> STAGE4["Stage 4: Synchronous 4-Switch Buck-Boost<br/>LM5176 Controller + 4x BSC034N04LS MOSFETs"]
    STAGE4 --> VOUT["Regulated Output Binding Posts<br/>5.0V - 20.0V DC @ 3.0A (60W)"]
    BUS24 --> REG12["L78L12 Linear Regulator<br/>+12V DC Gate Drive Bias"]
    BUS24 --> REG5["L78L05 Linear Regulator<br/>+5V DC OLED Display Rail"]
    REG5 --> REG33["AP2114-3.3 LDO Regulator<br/>+3.3V DC Quiet Logic & MCU VDD"]
```

### 8.1.1 Power Sequencing

#### Power Up Sequence
To prevent inductive inrush stress, output overshoot, and MCU race conditions, the hardware enforces a deterministic 5-phase startup sequence:

### Table 6: Power Sequencing
| Time (ms) | Operational State / Event | Circuit Behavior & Hardware Control | Output Voltage State |
| :---: | :--- | :--- | :---: |
| **0.0 ms** | **AC Mains Applied** | $85\,\text{V} - 265\,\text{V}_{\text{AC RMS}}$ energizes circuit. $15\,\Omega$ NTC limits inrush charging current to $< 25\,\text{A}_{\text{peak}}$. Bridge rectifier charges bulk capacitor. | $0.0\,\text{V}$ |
| **15.0 ms** | **Bulk DC Bus Stabilized** | Bulk DC rail reaches $> 120\,\text{V}_{\text{DC}}$. High-voltage trickle resistor charges Flyback controller $V_{\text{CC}}$ capacitor to startup threshold ($14.5\,\text{V}$). | $0.0\,\text{V}$ |
| **25.0 ms** | **Flyback Stage Starts** | Controller initiates $65\,\text{kHz}$ PWM. Auxiliary winding takes over controller bias. Secondary Schottky rectifies pulses. | $+24.0\,\text{V}$ ramp begins |
| **40.0 ms** | **+24.0V Rail Reaches Steady-State**| $+24.0\,\text{V} \pm 1.0\%$ intermediate bus stabilizes. Housekeeping regulators power up: $+12\,\text{V}$ gate bias, $+5\,\text{V}$ display, $+3.3\,\text{V}$ MCU rail. | $+24.0\,\text{V}$ stable |
| **50.0 ms** | **MCU Boot & Peripheral Init** | STM32 POR releases at $+3.3\,\text{V}$. DAC output set to $+3.30\,\text{V}$ (defaulting output command to safe minimum $5.0\,\text{V}$). LM5176 `ENABLE` pin held LOW by MCU NPN clamp. OLED initializes. | $0.0\,\text{V}$ (Output Disabled) |
| **70.0 ms** | **System Standby Ready** | Idle power $< 150\,\text{mW}$. System awaits user enable command. | $0.0\,\text{V}$ (Standby) |
| **User Run** | **Output Enable Toggle** | MCU releases `ENABLE` clamp. LM5176 executes internal $5\,\text{ms}$ soft-start ramp to commanded setpoint ($5.0\,\text{V}$ to $20.0\,\text{V}$) with zero overshoot ($< 1.0\%$). | Commanded setpoint reached |

#### Power Down Sequence
1. **User Commanded Output Disable**: STM32 drives pin `PB0` HIGH, turning on NPN clamp to ground LM5176 `ENABLE`. Buck-boost gate drivers immediately turn OFF all four MOSFETs. Active output bleeder resistor discharges output filter capacitors to $< 0.8\,\text{V}$ within $250\,\text{ms}$.
2. **AC Mains Grid Dropout**: `AMC1311` detects AC input line falling below $70\,\text{V}_{\text{RMS}}$. Bulk capacitor sustains continuous operation for $> 50\,\text{ms}$ (at $230\,\text{V}_{\text{AC}}$). MCU captures current setpoint and calibration data to Flash EEPROM emulation sector within $2.0\,\text{ms}$. As bulk rail collapses below Flyback UVLO, PWM switching stops. Safety bleeder resistors ($300\,\text{k}\Omega$) safely discharge bulk electrolytic capacitor from $375\,\text{V}$ to $< 50\,\text{V}$ within $44.8\,\text{seconds}$.

### 8.1.2 Power Consumption
The table below details current consumption across all operational voltage rails in Standby and Full Load states:

### Table 7: Subsystem1 – Power Consumption
| Rail Name | Nominal Voltage | Standby Current | 5V / 3A Load (15W) | 12V / 3A Load (36W) | 20V / 3A Load (60W) | Subsystem Loads Served |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **High-Voltage Bulk**| $+325\,\text{V}_{\text{DC}}$ | $0.85\,\text{mA}$ | $58.2\,\text{mA}$ | $134.1\,\text{mA}$ | $215.8\,\text{mA}$ | Primary Flyback switching stage, snubber, primary bleeders. |
| **+24.0V Inter Rail** | $+24.0\,\text{V}_{\text{DC}}$ | $12.0\,\text{mA}$ | $685\,\text{mA}$ | $1580\,\text{mA}$ | $2605\,\text{mA}$ | LM5176 power stage, $+12\,\text{V}$ gate bias, $+5\,\text{V}$ display rail. |
| **+12.0V Gate Bias** | $+12.0\,\text{V}_{\text{DC}}$ | $2.5\,\text{mA}$ | $18.5\,\text{mA}$ | $18.5\,\text{mA}$ | $18.5\,\text{mA}$ | LM5176 `VCC` supply, internal MOSFET gate charge drive circuits. |
| **+5.0V OLED Rail** | $+5.0\,\text{V}_{\text{DC}}$ | $1.2\,\text{mA}$ | $15.0\,\text{mA}$ | $15.0\,\text{mA}$ | $15.0\,\text{mA}$ | $1.3\text{"}$ OLED display controller, display logic, AP2114 LDO. |
| **+3.3V Logic Rail** | $+3.30\,\text{V}_{\text{DC}}$| $22.0\,\text{mA}$ | $38.5\,\text{mA}$ | $38.5\,\text{mA}$ | $38.5\,\text{mA}$ | STM32G474 MCU ($170\,\text{MHz}$), INA226 monitor, DAC reference, LEDs. |
| **Net Input Power** | **$230\,\text{V}_{\text{AC}}$** | **$< 120\,\text{mW}$** | **$18.4\,\text{W}$** | **$42.8\,\text{W}$** | **$70.14\,\text{W}$** | **Total System Grid Power Consumption** |

### 8.1.3 Power Dissipation & Thermal Losses
The table below documents the stage-by-stage power loss analysis under maximum continuous full load ($20.0\,\text{V} / 3.0\,\text{A} = 60.0\,\text{W}$ DC output at $230\,\text{V}_{\text{AC RMS}}$):

### Table 8: Subsystem1 – Power Dissipation
| Circuit Stage / Component | Component Ref Des | Calculated Loss (W) | Primary Loss Mechanism | Thermal Mitigation / Heat Sinking |
| :--- | :---: | :---: | :--- | :--- |
| **Mains Input & EMI Filter** | `F1`, `NTC1`, `L_CM1/2` | $0.38\,\text{W}$ | $I^2R$ copper winding resistance and fuse element loss. | Natural convection, through-hole thermal conduction. |
| **Bridge Rectifier** | `BR1` (GBU606) | $1.62\,\text{W}$ | Conduction loss: $2 \times V_F \times I_{\text{avg}} = 2 \times 0.95\,\text{V} \times 0.85\,\text{A}$. | Through-hole leads to 2oz copper polygon pour. |
| **High-Voltage Bulk Cap** | `C_BULK1` (100µF/450V)| $0.15\,\text{W}$ | $I_{\text{RMS}}^2 \times \text{ESR} = (0.95\,\text{A})^2 \times 0.165\,\Omega$. | Large aluminum snap-in can, $105^\circ\text{C}$ rated. |
| **Primary CoolMOS Switch** | `Q1` (IPB80R290P7) | $0.85\,\text{W}$ | Conduction loss ($0.59\,\text{W}$) + switching capacitive loss ($0.26\,\text{W}$).| D2PAK tab soldered to 2oz copper plane ($400\,\text{mm}^2$). |
| **Primary RCD Snubber** | `R_snub1..3` | $2.40\,\text{W}$ | Dissipation of leakage inductance energy ($E_{\text{lk}} = 20.2\,\mu\text{J}$). | Three 2512 SMD resistors in parallel ($3.0\,\text{W}$ total rating).|
| **Flyback Transformer** | `TX1` (PQ26/20 3C95) | $1.85\,\text{W}$ | Core hysteresis/eddy loss ($0.95\,\text{W}$) + copper loss ($0.90\,\text{W}$). | Ferrite core natural convection ($R_{\theta\text{ca}} \approx 18^\circ\text{C/W}$).|
| **Secondary Schottky Diode**| `D_SEC` (MBR10100G) | $1.80\,\text{W}$ | Conduction forward loss: $V_F \times I_{\text{OUT}} = 0.60\,\text{V} \times 3.0\,\text{A}$. | TO-220 mounted on stamped aluminum heatsink ($15^\circ\text{C/W}$).|
| **Buck-Boost Power MOSFETs**| `QA..QD` (BSC034N04LS)| $0.42\,\text{W}$ | Conduction loss ($0.08\,\text{W}$) + gate drive & switching ($0.34\,\text{W}$). | SuperSO8 package with thermal vias to bottom copper plane. |
| **Power Inductor** | `L1` (Wurth 7443321000) | $0.15\,\text{W}$ | Copper loss ($I^2 \times \text{DCR} = 9 \times 0.0105\,\Omega$) + core loss. | Flat-wire coil, direct surface thermal dissipation. |
| **Current Sense Shunt** | `R_shunt` (Bourns 10mΩ) | $0.09\,\text{W}$ | $I^2R = (3.0\,\text{A})^2 \times 0.010\,\Omega = 0.090\,\text{W}$ ($3.0\%$ of 3W).| Metal alloy element, negligible heating ($< 5^\circ\text{C}$ rise). |
| **Auxiliary Regulators & MCU**| `U5`, `U7..U9`, `DISP1` | $0.43\,\text{W}$ | LDO voltage drop and microcontroller dynamic power. | SOT-89 / SOT-223 PCB copper heatsinking tabs. |
| **Total System Dissipation** | **All Stages Combined** | **$10.14\,\text{W}$** | **Total internal heat generated at 60.0W full DC output** | **Full-Load System Efficiency: $\eta = \mathbf{85.54\%}$ @ 230V AC** |

## 8.2 Subsystem2 Power Architecture
The secondary SELV subsystem distributes regulated bias power generated from the $+24.0\,\text{V}_{\text{DC}}$ intermediate rail:
* **$+12.0\,\text{V}_{\text{DC}}$ Gate Drive Bias Rail**: Regulated by STMicroelectronics `L78L12ACUTR` (SOT-89, $100\,\text{mA}$ capacity) stepping down $+24\,\text{V}$ to provide a quiet, stable bias for the LM5176 internal gate charge pumps and gate driver circuitry.
* **$+5.0\,\text{V}_{\text{DC}}$ Display & Sensor Rail**: Regulated by STMicroelectronics `L78L05ABUTR` (SOT-89, $100\,\text{mA}$ capacity) powering the $1.3\text{"}$ OLED display module logic and input supply of the $+3.3\,\text{V}$ LDO.
* **$+3.30\,\text{V}_{\text{DC}}$ Ultra-Quiet MCU & Analog Rail**: Regulated by Diodes Inc. `AP2114H-3.3TRG1` (SOT-223, $1.0\,\text{A}$ capacity, low dropout voltage $240\,\text{mV}$, high PSRR of $65\,\text{dB}$ @ $1\,\text{kHz}$). Decoupled with a $10\,\mu\text{F}$ X7R ceramic capacitor and individual $100\,\text{nF}$ bypass capacitors on every microcontroller $V_{\text{DD}}/V_{\text{DDA}}$ pin pair.

## 8.3 Power Input Protection
* **Overcurrent Protection (`F1`)**: Littelfuse `0218002.MXP` ($2.0\,\text{A}$, $250\,\text{V}_{\text{AC}}$, $5 \times 20\,\text{mm}$ Time-Lag Ceramic Cartridge Fuse). Melting $I^2t = 19.6\,\text{A}^2\text{s}$ safely absorbs repetitive capacitive inrush pulses ($0.468\,\text{A}^2\text{s}$) while opening safely during short-circuit conditions up to $1500\,\text{A}$ interrupting rating.
* **Inrush Current Suppression (`NTC1`)**: EPCOS `B57236S0150M000` ($15.0\,\Omega$ cold resistance at $25^\circ\text{C}$, $2.9\,\text{A}_{\text{RMS}}$ steady-state current). Clamps maximum cold-start inrush current at $265\,\text{V}_{\text{AC RMS}}$ ($374.8\,\text{V}_{\text{peak}}$) to strictly $24.98\,\text{A}_{\text{peak}}$ even with zero external line impedance, satisfying PRD requirement `PR-02` ($< 25.0\,\text{A}_{\text{peak}}$).
* **Surge Voltage Clamp (`MOV1`)**: Bourns `MOV-14D471K` ($14\,\text{mm}$ disc, $300\,\text{V}_{\text{RMS}}$ continuous voltage, clamping voltage $775\,\text{V}$ @ $50\,\text{A}$, peak surge current $4500\,\text{A}$ for $8/20\,\mu\text{s}$ transient, energy absorption $125\,\text{J}$). Protects against IEC 61000-4-5 Level 3 differential line surges ($1.0\,\text{kV}$).

## 8.4 System Power Source
The SPPS module operates from commercial single-phase AC utility grids worldwide:
* Nominal Voltage: $100\,\text{V} - 240\,\text{V}_{\text{AC RMS}}$
* Operating Voltage Tolerance: Universal $85.0\,\text{V}$ to $265.0\,\text{V}_{\text{AC RMS}}$ continuous
* Nominal Frequency: $50\,\text{Hz} / 60\,\text{Hz}$ (Operating frequency range: $47\,\text{Hz} - 63\,\text{Hz}$)
* Maximum Steady-State Input Current: $1.604\,\text{A}_{\text{RMS}}$ at $85.0\,\text{V}_{\text{AC RMS}}$ under full $60.0\,\text{W}$ DC load.

---

# 9. Battery Powered Design

**Engineering Status: NOT APPLICABLE (Out of Scope per PRD Baseline)**

* **Design Scope & Operational Justification**:
  * The SPPS module is an AC-mains line-powered benchtop and ATE rack-mount instrument.
  * In strict conformance with the authoritative PRD ([`prd_final_spps.docx`](../PRD_task/reference_docs/prd_final_spps.docx), Section 10 "Out of Scope"), internal electrochemical battery storage, battery charging circuitry, and cell balancing architectures are excluded from the design.
  * Line dropout immunity is provided purely through the high-voltage electrostatic bulk capacitor bank (`C_BULK1`, $100\,\mu\text{F} / 450\,\text{V}$), which delivers $> 50\,\text{ms}$ holdup time at nominal $230\,\text{V}_{\text{AC}}$ and $> 12\,\text{ms}$ at low-line $85\,\text{V}_{\text{AC}}$, guaranteeing uninterrupted operation through half-cycle and full-cycle utility line dropouts ($> 10.0\,\text{ms}$ requirement).

---

# 10. Clock Scheme

The PCBA clock scheme establishes clean, jitter-free timing references across the mixed-signal microcontroller and switching controllers while mitigating electromagnetic interference (EMI):

### Table 11: Clock Scheme
| Clock Domain / Source | Oscillator Component | Nominal Frequency | Tolerance / Accuracy | Circuit Destinations & Functions Served |
| :---: | :--- | :---: | :---: | :--- |
| **High-Speed Ext (HSE)**| Abracon `ABM8G-24.000MHZ-18-D2Y-T` | $24.000\,\text{MHz}$ | $\pm 10\,\text{ppm}$ | MCU `OSC_IN` / `OSC_OUT` (Pins 5/6). Multiplied by internal PLL to generate $170\,\text{MHz}$ CPU core clock and high-resolution timers. |
| **Low-Speed Ext (LSE)**| Abracon `ABS07-32.768KHZ-T` | $32.768\,\text{kHz}$ | $\pm 20\,\text{ppm}$ | MCU `PC14` / `PC15`. Drives internal Real-Time Clock (RTC) and precise $100\,\text{ms}$ ($10.0\,\text{Hz}$) telemetry interrupt scheduling. |
| **Buck-Boost Clock** | TI LM5176 Internal Oscillator | $300.0\,\text{kHz}$ | $\pm 10\%$ | Synchronous 4-switch Buck-Boost H-bridge PWM clock. Programmed via precision resistor $R_T = 24.9\,\text{k}\Omega \pm 1\%$ on Pin 27 (`RT`). |
| **Flyback PWM Clock** | TI UCC28C43 / UC3843 Oscillator | $65.0\,\text{kHz}$ | $\pm 5\%$ | Primary Flyback switching frequency. Programmed via $R_T = 10.0\,\text{k}\Omega \pm 1\%$ and $C_T = 2.2\,\text{nF} \pm 5\%$ C0G ceramic on Pin 4 (`RT/CT`). |

* **EMI Harmonic Mitigation**: By fixing the Flyback switching frequency at a constant $65.0\,\text{kHz}$ and the Buck-Boost frequency at $300.0\,\text{kHz}$, all fundamental and harmonic emission spikes fall at predictable, deterministic frequencies. The two-stage input EMI filter is specifically designed to provide $> 35\,\text{dB}$ attenuation at $150\,\text{kHz}$ (the start of CISPR 32 conducted limits), ensuring zero harmonic overlap with sensitive radio frequency bands.

---

# 11. Reset Scheme

The reset architecture guarantees fail-safe initialization, brownout protection, and supervisor-level shutdown across all voltage rails:
* **Microcontroller Reset (`NRST`, Pin 7)**:
  * Supervised by an external active-low RC network ($10\,\text{k}\Omega$ pull-up to $+3.3\,\text{V}$, $100\,\text{nF}$ ceramic capacitor to ground).
  * Front-panel tactile push-button allows manual hardware system reset.
  * Internal Programmable Brown-Out Reset (BOR): Configured in Flash option bytes to **BOR Level 3** ($V_{\text{BOR}} \approx 2.70\,\text{V}_{\text{DC}}$). If the $+3.3\,\text{V}$ rail dips below $2.70\,\text{V}$, the MCU core is held in hard reset, preventing corrupted Flash writes or errant DAC register updates.
* **Flyback Controller Under-Voltage Lockout (UVLO)**:
  * Primary Flyback controller (`U1`) features an internal precision UVLO comparator on $V_{\text{CC}}$ (Pin 7).
  * Startup threshold: $V_{\text{CC,start}} = 14.5\,\text{V}$ (UCC28740) / $8.4\,\text{V}$ (UCC28C43).
  * Minimum operating threshold: $V_{\text{CC,stop}} = 9.0\,\text{V}$ (UCC28740) / $7.6\,\text{V}$ (UCC28C43).
  * Prevents gate drive pulsing if the bulk DC bus voltage is insufficient to sustain secondary regulation.
* **LM5176 Buck-Boost Enable & Hardware UVLO**:
  * Pin 6 (`ENABLE`) features an internal precision comparator with a $1.20\,\text{V}$ turn-on threshold and $100\,\text{mV}$ hysteresis.
  * An external resistor divider from the $+24.0\,\text{V}$ intermediate rail ($R_1 = 100\,\text{k}\Omega$, $R_2 = 6.8\,\text{k}\Omega$) sets a hardware UVLO threshold:
    $$V_{\text{bus,UVLO}} = 1.20\,\text{V} \times \left( \frac{100\,\text{k}\Omega + 6.8\,\text{k}\Omega}{6.8\,\text{k}\Omega} \right) = \mathbf{18.85\,\text{V}_{\text{DC}}}$$
    The Buck-Boost stage is held in hard shutdown until the intermediate rail exceeds $+18.85\,\text{V}_{\text{DC}}$, preventing abnormal switching currents during primary ramp-up.
  * Active NPN pull-down transistor (`MMBT3904`) driven by MCU pin `PB0` allows the supervisory firmware to override the enable pin and collapse power delivery within $500\,\text{ns}$ upon fault detection.

---

# 12. Hardware Configurations

## 12.1 Subsystem1 HW Configurations

### 12.1.1 Board Type / Assembly Variant
The SPPS PCBA supports two qualified manufacturing assembly variants:
1. **Standard Production Variant (Build Code: `SPPS-STD-01`)**:
   * Current Shunt: $10.0\,\text{m}\Omega$ Bourns `CSS2H-2512R-L010F` (Native $3.50\,\text{A}$ hardware clamp via LM5176 internal $35\,\text{mV}$ threshold).
   * Inrush Limiter: $15.0\,\Omega$ EPCOS `B57236S0150M000` (Guaranteed inrush $< 25.0\,\text{A}_{\text{peak}}$ at $265\,\text{V}_{\text{AC}}$ with zero line impedance).
   * Primary Controller: TI `UCC28740DR` Quasi-Resonant Valley Switching Flyback controller.
2. **Industrial Uniform-Clock Variant (Build Code: `SPPS-IND-02`)**:
   * Current Shunt: $10.0\,\text{m}\Omega$ Bourns `CSS2H-2512R-L010F`.
   * Inrush Limiter: $15.0\,\Omega$ EPCOS `B57236S0150M000`.
   * Primary Controller: TI `UCC28C43DR` (BiCMOS uniform $65.0\,\text{kHz}$ fixed PWM clock).

### 12.1.2 Board Revision
The revision history of the physical PCBA hardware layout is tracked below:

### Table 12: Board Revision
| PCBA Revision | Release Date | Description of Changes | ECO / Release Note |
| :---: | :---: | :--- | :--- |
| **Rev A0_01** | 06-Oct-2026 | Initial prototype feasibility layout. Dual-board architecture. | Initial Concept Draft |
| **Rev A1_000** | 15-Oct-2026 | Consolidated into single 4-layer PCBA with 6.4mm isolation slot. | Baseline Restructuring |
| **Rev A1_001** | 30-Oct-2026 | Production-grade release: 15Ω NTC, 10mΩ shunt, 3.66mV DAC steering, Class A BOM. | Authoritative HDD Release |

### 12.1.3 Jumper Configuration
The PCBA includes three 3-pin $2.54\,\text{mm}$ configuration headers for factory testing and serial telemetry routing:

### Table 13: Jumper Configuration
| Jumper Ref Des | Jumper Function / Description | Default Setting | Alternate Setting | Functional Behavior |
| :---: | :--- | :---: | :---: | :--- |
| **`JP1`** | **UART Telemetry Stream Enable** | **Pins 1-2 Shorted (ENABLE)** | Pins 2-3 Shorted (DISABLE) | Pins 1-2 connects MCU `TX` (`PA9`) to telemetry header `J5`. Pins 2-3 isolates UART to eliminate serial EMI during lab EMC testing. |
| **`JP2`** | **Auxiliary 24V DC Input Bypass** | **Pins 1-2 Shorted (AC Mains)** | Pins 2-3 Shorted (DC Bench) | Pins 1-2 routes Flyback secondary into Buck-Boost. Pins 2-3 connects external $24\,\text{V}$ DC barrel jack (DNP footprint) for battery/bench operation. |
| **`JP3`** | **MCU Bootloader Mode Select** | **Pins 1-2 Shorted (Flash Boot)** | Pins 2-3 Shorted (System DFU) | Pins 1-2 ties `BOOT0` to GND ($10\,\text{k}\Omega$). Pins 2-3 ties `BOOT0` to $+3.3\,\text{V}$ to invoke factory STM32 ROM bootloader via UART. |
"""

def append_part2():
    target = "smart_programmable_power_supply/HDD_task/HARDWARE_DESIGN_DOCUMENT_HDD.md"
    print(f"Appending sections 5 to 12 to {target}...")
    with open(target, "a") as f:
        f.write(get_sections_5_to_7())
        f.write(get_sections_8_to_12())
    print("Part 2 successfully appended.")

if __name__ == "__main__":
    append_part2()
