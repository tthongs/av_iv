#!/usr/bin/env python3
"""
Component and Schematic Connection Generator: Module 9 (User Interface and Connectors)
"""

from pathlib import Path

OUT_DIR = Path("/home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/components_sch/module_09_user_interface_and_connectors")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def write_files():
    # 1. DISP1 1.3" I2C OLED Display
    with open(OUT_DIR / "DISP1_ssd1306_oled.md", "w") as f:
        f.write(r"""# Component Schematic Specification: DISP1 (1.3" Monochrome I2C OLED Module)

## 1. Component Metadata
* **Reference Designator**: `DISP1`
* **Component Type**: 1.3-Inch Monochrome Graphic OLED Display Module
* **Driver IC**: Solomon Systech `SSD1306` (or `SH1106`)
* **Resolution**: $128 \times 64$ Dots
* **Primary Sourcing**: Generic Industrial 4-Pin I2C OLED Module
* **Alternate Sourcing**: Adafruit Industries `938` / Waveshare `1.3inch OLED (A)`
* **Package / Interface**: 4-Pin $2.54\,\text{mm}$ Right-Angle Header / Flexible Flat Cable (FFC)
* **Subsystem**: Stage 9 (Front-Panel User Interface & Real-Time Telemetry Dashboard)

## 2. Electrical Ratings & Constraints
* **Operating Supply Voltage ($V_{\text{CC}}$)**: $+3.3\,\text{V}$ to $+5.0\,\text{V}_{\text{DC}}$ (Powered from $+5.0\,\text{V}_{\text{SEC}}$ auxiliary rail).
* **Current Consumption ($I_{\text{CC}}$)**:
  * Typical operating current: $\approx 15.0\,\text{mA}$ (with $50\%$ pixels illuminated).
  * Maximum full-white display current: $28.0\,\text{mA}$.
* **Communication Interface**: I2C Fast-Mode ($400.0\,\text{kHz}$)
* **Default 7-Bit I2C Address**: `0x3C` (`0111100b`)
* **Display Data Refresh Rate**: $10.0\,\text{Hz}$ ($100.0\,\text{ms}$ frame update rate), perfectly synchronized with the telemetry sampling engine.
* **On-Screen Dashboard Layout**:
  * Line 1: `SET: 20.00V  3.00A` (Target voltage & current limit setpoints)
  * Line 2: `OUT: 19.98V  2.99A` (Real-time calibrated output voltage & load current)
  * Line 3: `PWR:  59.8W  η:91.2%` (Output DC load power & true AC-to-DC conversion efficiency)
  * Line 4: `MODE: [CV]  AC: 230V` (Regulator state [CV/CC/FLT] & primary line voltage)

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`VCC`** | `+5V_SEC` | Module 8 Linear Reg `U8_REG` Output (+5V) | Filtered $+5.0\,\text{V}_{\text{DC}}$ supply rail; $100\,\text{nF}$ bypass cap. |
| **2** | **`GND`** | `GND_SELV` | Secondary ground plane (Layer 2) | Direct connection to SELV ground. |
| **3** | **`SCL`** | `I2C1_SCL` | STM32 Pin 61 (`PB8`), $2.2\,\text{k}\Omega$ pull-up | Fast-Mode I2C clock line. |
| **4** | **`SDA`** | `I2C1_SDA` | STM32 Pin 62 (`PB9`), $2.2\,\text{k}\Omega$ pull-up | Fast-Mode I2C data line. |

## 4. Schematic Symbol Representation
```
                    [ DISP1: 1.3" 128x64 MONOCHROME OLED MODULE ]
                                   SSD1306 Controller
                                  ┌─────────────────┐
          Net: +5V_SEC  ─────────[1] VCC            │
          Net: GND_SELV ─────────[2] GND    128x64  │
          Net: I2C1_SCL ─────────[3] SCL     OLED   │
          Net: I2C1_SDA ─────────[4] SDA   (0x3C)   │
                                  └─────────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Connector Location**: Position header `J_DISP` near the front edge of the PCBA directly behind the chassis front panel window.
2. **I2C Signal Integrity**: Route `I2C1_SCL` and `I2C1_SDA` as length-matched tracks ($< 80\,\text{mm}$ total routing length) away from noisy buck-boost switch nodes `SW1` and `SW2`.
""")

    # 2. ENC1..2 Bourns Rotary Encoders
    with open(OUT_DIR / "ENC1_2_rotary_encoders.md", "w") as f:
        f.write(r"""# Component Schematic Specification: ENC1, ENC2 (Incremental Rotary Encoders)

## 1. Component Metadata
* **Reference Designators**: `ENC1` (Voltage Adjust / Fine-Coarse Toggle), `ENC2` (Current Adjust / Output Enable Toggle)
* **Component Type**: Incremental Contacting Mechanical Rotary Encoder with Integrated Push Switch
* **Manufacturer**: Bourns Inc.
* **Primary MPN**: `PEC11R-4220F-S0024`
* **Alternate Manufacturer**: Alps Alpine
* **Alternate MPN**: `EC11E2424407` (24 Pulses/Rev, with push switch)
* **Package / Footprint**: Through-Hole Right-Angle Bracket Mount (Shaft Length: 20 mm, D-Cut Flat)
* **Subsystem**: Stage 9 (Front-Panel User Interface & Adjustment Controls)

## 2. Electrical Ratings & Constraints
* **Pulses per Revolution**: $24$ Pulses / $24$ Detents ($360^\circ$ continuous rotation).
* **Contact Rating**: $10.0\,\text{mA}$ at $5.0\,\text{V}_{\text{DC}}$ ($0.5\,\text{W}$ max).
* **Rotational Life**: $> 30,000$ cycles.
* **Integrated Push Switch**: SPST Normally Open momentary tactile switch ($20,000$ cycles).
* **Quadrature Channel Phasing**: Channel A leads Channel B in clockwise (CW) rotation.
* **Hardware Debouncing Filter Design**:
  Mechanical switch contacts exhibit bouncing noise for up to $t_{\text{bounce}} \approx 3.0\,\text{ms}$. To guarantee glitch-free decoding by the STM32 timer hardware without CPU polling overhead, each phase line is buffered by an external passive RC filter:
  * Pull-Up Resistor: $R_{\text{pull}} = 10.0\,\text{k}\Omega \pm 1\%$ tied to $+3.30\,\text{V}_{\text{SEC}}$.
  * Filter Capacitor: $C_{\text{deb}} = 10.0\,\text{nF} \pm 10\%$ 50V C0G ceramic to `GND_SELV`.
  * Time Constant:
    $$\tau = R_{\text{pull}} \times C_{\text{deb}} = (10.0\,\text{k}\Omega) \times (10.0\,\text{nF}) = \mathbf{100.0\,\mu\text{s}}$$
  * Eliminates mechanical contact bounce while allowing fast manual rotation up to $600\,\text{RPM}$ ($4.16\,\text{ms}$ per detent step) without missing pulses.

## 3. Schematic Pin Connections & Net Mapping

### 3.1 Encoder 1: Voltage Setting & Coarse/Fine Switch
| Pin # | Pin Designation | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **A** | **Phase A** | `ENC1_CH_A` | STM32 Pin 14 (`PA0` / TIM2_CH1) | Filtered quadrature Phase A ($10\,\text{k}\Omega + 10\,\text{nF}$). |
| **C** | **Common**  | `GND_SELV` | Secondary ground plane | Signal return ground. |
| **B** | **Phase B** | `ENC1_CH_B` | STM32 Pin 15 (`PA1` / TIM2_CH2) | Filtered quadrature Phase B ($10\,\text{k}\Omega + 10\,\text{nF}$). |
| **S1**| **Switch Terminal 1**| `ENC1_PUSH_SW`| STM32 Pin 21 (`PA5`), $10\,\text{k}\Omega$ pull-up| Toggles Voltage Adjustment Step: Coarse ($1.0\,\text{V}$) vs Fine ($10\,\text{mV}$). |
| **S2**| **Switch Terminal 2**| `GND_SELV` | Secondary ground plane | Pushbutton ground return. |

### 3.2 Encoder 2: Current Limit & Output Enable Switch
| Pin # | Pin Designation | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **A** | **Phase A** | `ENC2_CH_A` | STM32 Pin 22 (`PA6` / TIM3_CH1) | Filtered quadrature Phase A ($10\,\text{k}\Omega + 10\,\text{nF}$). |
| **C** | **Common**  | `GND_SELV` | Secondary ground plane | Signal return ground. |
| **B** | **Phase B** | `ENC2_CH_B` | STM32 Pin 23 (`PA7` / TIM3_CH2) | Filtered quadrature Phase B ($10\,\text{k}\Omega + 10\,\text{nF}$). |
| **S1**| **Switch Terminal 1**| `ENC2_PUSH_SW`| STM32 Pin 28 (`PB2`), $10\,\text{k}\Omega$ pull-up| Momentary press toggles Output DC Power Enable / Inhibit. |
| **S2**| **Switch Terminal 2**| `GND_SELV` | Secondary ground plane | Pushbutton ground return. |

## 4. Schematic Symbol Representation
```
                    [ BOURNS PEC11R ROTARY ENCODER INTERFACE ]
                                  Net: +3V3_SEC
                                   │         │
                                [10kΩ]    [10kΩ]
                                   │         │
                                   ├──[10nF]─┼──[10nF]── Net: GND_SELV
                                   │         │
                                ┌──┴──┐   ┌──┴──┐
       Phase A (Net: ENC_CH_A) ─┤A   C├─┬─┤B   S├─ (Net: ENC_CH_B) Phase B
                                └─────┘ │ └─────┘
                                        │    │
                                 Net: GND   └── Net: ENC_PUSH_SW (To MCU Pin)
```

## 5. Schematic & PCB Layout Guidelines
1. **Chassis Standoff**: The through-hole mounting bracket lugs provide mechanical rigidity against user torque. Solder the two mounting tabs solidly into plated through-holes tied to chassis earth or secondary ground.
2. **Debounce Placement**: Place the $10\,\text{k}\Omega$ pull-up resistors and $10\,\text{nF}$ capacitors close to the MCU input pins to reject capacitive pickup along the front-panel routing harness.
""")

    # 3. LED1..3 Front-Panel Status Indicators
    with open(OUT_DIR / "LED1_3_status_leds.md", "w") as f:
        f.write(r"""# Component Schematic Specification: LED1..3 (Front-Panel Status Indicators)

## 1. Component Metadata
* **Reference Designators**:
  * `LED1`: Constant Voltage (CV) Active Mode Indicator (Green)
  * `LED2`: Constant Current (CC) Clamped Mode Indicator (Amber)
  * `LED3`: Fault Shutdown / Tripped Indicator (Red)
* **Component Type**: High-Efficiency Surface-Mount Indicating LEDs
* **Manufacturer**: Kingbright
* **Primary MPNs**:
  * `LED1` (Green): `APT2012SGC` (568 nm, $15\,\text{mcd}$, 0805)
  * `LED2` (Amber): `APT2012SEC` (601 nm, $30\,\text{mcd}$, 0805)
  * `LED3` (Red): `APT2012SRC` (640 nm, $50\,\text{mcd}$, 0805)
* **Alternate Manufacturer**: Lite-On Inc.
* **Alternate MPN Series**: `LTST-C170 Series`
* **Package / Footprint**: SMD 0805 Metric ($2.0 \times 1.25\,\text{mm}$, Height: $0.75\,\text{mm}$)
* **Subsystem**: Stage 9 (Visual Operating State Annunciators)

## 2. Electrical Ratings & Constraints
* **Forward Voltage Drop ($V_F$)**:
  * Green (`LED1`): $V_F = 2.10\,\text{V}$ typical at $1.5\,\text{mA}$.
  * Amber (`LED2`): $V_F = 2.00\,\text{V}$ typical at $1.5\,\text{mA}$.
  * Red (`LED3`): $V_F = 1.90\,\text{V}$ typical at $1.5\,\text{mA}$.
* **Drive Resistor Sizing**:
  Driven directly by STM32 3.3V CMOS GPIO outputs through dedicated $1.00\,\text{k}\Omega \pm 1\%$ current-limiting resistors (`R_LED1`, `R_LED2`, `R_LED3`, 0603 SMD):
  $$I_{F,\text{Green}} = \frac{3.30\,\text{V} - 2.10\,\text{V}}{1000\,\Omega} = \mathbf{1.20\,\text{mA}}$$
  $$I_{F,\text{Amber}} = \frac{3.30\,\text{V} - 2.00\,\text{V}}{1000\,\Omega} = \mathbf{1.30\,\text{mA}}$$
  $$I_{F,\text{Red}} = \frac{3.30\,\text{V} - 1.90\,\text{V}}{1000\,\Omega} = \mathbf{1.40\,\text{mA}}$$
  * At $\approx 1.3\,\text{mA}$, the LEDs provide crisp front-panel visibility without excessive brightness or battery/power overhead, drawing $< 4.5\,\text{mW}$ per channel.

## 3. Schematic Pin Connections & Net Mapping
| LED Ref Des | Indicator Function | Anode Driven By | Cathode Tied To | Series Limiting Resistor |
| :---: | :--- | :--- | :--- | :---: |
| **`LED1`** | **Green (CV Mode)** | STM32 Pin 2 (`PC13`) | `GND_SELV` | `R_LED1` ($1.0\,\text{k}\Omega \pm 1\%$, 0603) |
| **`LED2`** | **Amber (CC Mode)** | STM32 Pin 24 (`PC4`) | `GND_SELV` | `R_LED2` ($1.0\,\text{k}\Omega \pm 1\%$, 0603) |
| **`LED3`** | **Red (Fault Mode)** | STM32 Pin 25 (`PC5`) | `GND_SELV` | `R_LED3` ($1.0\,\text{k}\Omega \pm 1\%$, 0603) |

## 4. Schematic Symbol Representation
```
                     [ FRONT-PANEL STATUS LED INDICATORS ]

  STM32 Pin 2 (PC13)  ──[ 1.0 kΩ ]──>|── (LED1: Green CV)  ── Net: GND_SELV
  STM32 Pin 24 (PC4)  ──[ 1.0 kΩ ]──>|── (LED2: Amber CC)  ── Net: GND_SELV
  STM32 Pin 25 (PC5)  ──[ 1.0 kΩ ]──>|── (LED3: Red FAULT) ── Net: GND_SELV
```
""")

    # 4. J2..J3 Pomona 4mm Output Binding Posts
    with open(OUT_DIR / "J2_J3_binding_posts.md", "w") as f:
        f.write(r"""# Component Schematic Specification: J2, J3 (4mm Heavy-Duty Output Binding Posts)

## 1. Component Metadata
* **Reference Designators**:
  * `J2`: DC Output Positive Terminal (Red)
  * `J3`: DC Output Negative Terminal (Black)
* **Component Type**: Heavy-Duty Gold-Plated $4\,\text{mm}$ Safety Banana Binding Posts
* **Manufacturer**: Pomona Electronics
* **Primary MPNs**:
  * `J2` (Red Positive): `3770-2`
  * `J3` (Black Negative): `3770-0`
* **Alternate Manufacturer**: Mueller Electric
* **Alternate MPNs**: `BU-P3770-2` (Red) / `BU-P3770-0` (Black)
* **Package / Mounting**: Panel-Mount Threaded Stud with Heavy Solder Lug (Pitch: Standard $19.05\,\text{mm}$ / $0.75\,\text{in}$)
* **Subsystem**: Stage 9 (High-Current Regulated DC Power Delivery Terminals)

## 2. Electrical Ratings & Constraints
* **Rated Current ($I_{\text{rated}}$)**: $30.0\,\text{A}_{\text{DC}}$ continuous
  * Operating continuous current: $3.0\,\text{A}_{\text{DC}}$ ($4.2\,\text{A}$ peak surge).
  * Current Derating: $\frac{3.0\,\text{A}}{30.0\,\text{A}} = \mathbf{10.0\%} \ll 70\%$ (Virtually zero heating or resistance loss).
* **Rated Voltage ($V_{\text{rated}}$)**: $1000\,\text{V}_{\text{CAT I}}$ ($2500\,\text{V}$ peak breakdown).
* **Contact Resistance**: $< 1.0\,\text{m}\Omega$ (Gold-plated brass core prevents galvanic oxidation).
* **Mechanical Features**: Accepts standard $4\,\text{mm}$ shrouded banana plugs, bare wire up to $10\,\text{AWG}$ clamped through cross-hole, or spade lugs up to $8.0\,\text{mm}$ width.

## 3. Schematic Pin Connections & Net Mapping
| Ref Des | Terminal Function | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **`J2`** | **`+` (Positive DC Out)** | `+V_OUT` | `R_shunt` Exit Pad, `C_POLY1` (+), `U3` VOSNS | Heavy 2oz copper polygon ($w \ge 5.0\,\text{mm}$). |
| **`J3`** | **`-` (Negative DC Out)** | `GND_SELV` | Secondary ground plane, `C_POLY1` (-) | Heavy 2oz copper polygon ($w \ge 5.0\,\text{mm}$). |

## 4. Schematic Symbol Representation
```
                    [ 4mm HEAVY-DUTY OUTPUT BINDING POSTS ]
                                Standard 19.05 mm Spacing

          Net: +V_OUT    ──────────────[ J2: RED (+) POST ]
                                               (30A / 1000V)

          Net: GND_SELV  ──────────────[ J3: BLACK (-) POST ]
                                               (30A / 1000V)
```

## 5. Schematic & PCB Layout Guidelines
1. **Reinforced Annular Solder Rings**: The PCBA mounting pads for the binding post studs must feature heavy through-hole barrels ($\varnothing 4.5\,\text{mm}$) surrounded by an array of eight $0.5\,\text{mm}$ vias stitching Layers 1, 2, 3, and 4 together to support both mechanical torque and $3\,\text{A}$ continuous conduction without thermal delamination.
""")

    # 5. J4 SWD Firmware Debug Header
    with open(OUT_DIR / "J4_swd_header.md", "w") as f:
        f.write(r"""# Component Schematic Specification: J4 (SWD Firmware Programming & Debug Header)

## 1. Component Metadata
* **Reference Designator**: `J4`
* **Component Type**: 4-Pin Shrouded Vertical Male Pin Header ($2.54\,\text{mm}$ Pitch)
* **Manufacturer**: Molex Incorporated
* **Primary MPN**: `22-28-4040`
* **Alternate Manufacturer**: Samtec
* **Alternate MPN**: `TSW-104-07-G-S`
* **Package / Footprint**: Through-Hole 1x4 Pin Header (Pitch: 2.54 mm)
* **Subsystem**: Stage 9 (Production Firmware Flashing & In-Circuit Debug)

## 2. Electrical Ratings & Constraints
* **Contact Current Rating**: $3.0\,\text{A}$ per pin.
* **Operating Voltage**: $+3.30\,\text{V}_{\text{DC}}$.
* **Clock Frequency**: Supports high-speed SWD clocking up to $10.0\,\text{MHz}$ via ST-LINK V3 or J-Link debugger.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`VTref`** | `+3V3_SEC` | Microcontroller supply rail | Provides target reference voltage sensing to debugger. |
| **2** | **`SWDIO`** | `SWDIO` | STM32 Pin 46 (`PA13`) | Bidirectional Serial Wire Data IO (internal pull-up). |
| **3** | **`SWCLK`** | `SWCLK` | STM32 Pin 49 (`PA14`), Pull-down $100\,\text{k}\Omega$ | Serial Wire Clock input. |
| **4** | **`GND`** | `GND_SELV` | Secondary ground plane | Debug signal ground return. |

## 4. Schematic Symbol Representation
```
                    [ J4: 4-PIN SWD FIRMWARE DEBUG HEADER ]
                                ┌─────────────┐
          Net: +3V3_SEC  ───────┤[1] VTref    │
          Net: SWDIO     ───────┤[2] SWDIO    │ 2.54 mm
          Net: SWCLK     ───────┤[3] SWCLK    │ Shrouded Header
          Net: GND_SELV  ───────┤[4] GND      │
                                └─────────────┘
```
""")

    # 6. J5 UART Serial Telemetry Header
    with open(OUT_DIR / "J5_uart_header.md", "w") as f:
        f.write(r"""# Component Schematic Specification: J5 (UART Serial Telemetry Header)

## 1. Component Metadata
* **Reference Designator**: `J5`
* **Component Type**: 3-Pin Vertical Male Pin Header ($2.54\,\text{mm}$ Pitch)
* **Manufacturer**: Molex Incorporated
* **Primary MPN**: `22-28-4030`
* **Alternate Manufacturer**: Samtec
* **Alternate MPN**: `TSW-103-07-G-S`
* **Package / Footprint**: Through-Hole 1x3 Pin Header (Pitch: 2.54 mm)
* **Subsystem**: Stage 9 (External Telemetry Data Stream Interface)

## 2. Electrical Ratings & Constraints
* **Logic Level**: $3.3\,\text{V}$ CMOS UART ($V_{\text{OH}} \ge 2.9\,\text{V}$, $V_{\text{OL}} \le 0.4\,\text{V}$).
* **Baud Rate**: $115,200\,\text{baud}$, 8 data bits, no parity, 1 stop bit ($8\text{N}1$).
* **Transmission Rate**: 10 Hz telemetry frame stream ($100.0\,\text{ms}$ periodic report).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`TX` (Output)** | `USART1_TX` | STM32 Pin 42 (`PA9`) | Serial transmit data stream to host PC / ATE system. |
| **2** | **`RX` (Input)**  | `USART1_RX` | STM32 Pin 43 (`PA10`) | Serial receive command input from host PC. |
| **3** | **`GND`**         | `GND_SELV` | Secondary ground plane | Signal ground return. |

## 4. Schematic Symbol Representation
```
                    [ J5: 3-PIN UART SERIAL TELEMETRY HEADER ]
                                ┌─────────────┐
          Net: USART1_TX ───────┤[1] TX       │
          Net: USART1_RX ───────┤[2] RX       │ 2.54 mm Pitch
          Net: GND_SELV  ───────┤[3] GND      │
                                └─────────────┘
```
""")

    # 7. Module 9 Equivalent Circuit Document
    with open(OUT_DIR / "module_09_user_interface_connectors_equivalent_circuit.md", "w") as f:
        f.write(r"""# Module 9 Equivalent Electronic Circuit: User Interface & Connectors Subsystem

## 1. Subsystem Architecture Overview
Module 9 encompasses all user-facing visual annunciators, electro-mechanical controls, programming headers, and external power delivery terminals for the Smart Programmable Power Supply (`VVDN_SPPS_2026`). 

The subsystem interfaces directly with the supervisory microcontroller (Module 6) and regulated output stage (Module 4) to deliver a seamless instrument-grade bench experience:
1. **Graphical Telemetry Dashboard (`DISP1`)**: A $1.3\text{"}$ monochrome OLED display ($128 \times 64$, SSD1306 controller at I2C address `0x3C`) provides real-time readouts of programmed setpoints, live measured voltages, currents, output power, and overall conversion efficiency at a crisp $10.0\,\text{Hz}$ refresh rate.
2. **Dual Quadrature Rotary Controls (`ENC1`, `ENC2`)**: High-reliability Bourns mechanical encoders featuring integrated push switches allow tactile, jitter-free voltage tuning (Coarse $1.0\,\text{V}$ / Fine $10\,\text{mV}$ steps) and momentary output power toggling. Hardware RC debounce filters guarantee clean edge transitions into STM32 timer inputs.
3. **Tri-Color Status Annunciation (`LED1..3`)**: Front-panel SMD LEDs indicate operating state: Green for Constant Voltage (CV) mode, Amber for Constant Current (CC) mode, and Red for Protective Fault Shutdown.
4. **Heavy-Duty Output Binding Posts (`J2`, `J3`)**: Standard Pomona gold-plated $4\,\text{mm}$ safety banana binding posts spaced at international $19.05\,\text{mm}$ centers provide robust connection to external loads with $< 1\,\text{m}\Omega$ contact resistance and $30\,\text{A}$ current rating.
5. **Debug & Telemetry Headers (`J4`, `J5`)**: Dedicated 4-pin SWD programming header and 3-pin $115,200\,\text{baud}$ UART streaming header allow in-circuit firmware flashing and automated data logging.

---

## 2. Full Schematic Electronic Circuit Diagram

```
========================================================================================================================
MODULE 9: COMPLETE USER INTERFACE, STATUS ANNUNCIATORS & CONNECTORS SCHEMATIC
========================================================================================================================

    [ DISP1: 1.3" I2C OLED MODULE (128x64 SSD1306 @ 0x3C) ]
    ┌───────────────────────┐
    │[1] VCC  ──────────────┼─── Net: +5V_SEC
    │[2] GND  ──────────────┼─── Net: GND_SELV
    │[3] SCL  ──────────────┼─── Net: I2C1_SCL (To STM32 Pin 61, 2.2kΩ Pull-up)
    │[4] SDA  ──────────────┼─── Net: I2C1_SDA (To STM32 Pin 62, 2.2kΩ Pull-up)
    └───────────────────────┘


    [ ROTARY ENCODER 1: VOLTAGE ADJUST / COARSE-FINE ]
    Net: +3V3_SEC ──[ 10kΩ ]──┬──[ 10nF ]── GND_SELV
                              │
    Pin A ────────────────────┼─── Net: ENC1_CH_A (To STM32 Pin 14 / TIM2_CH1)
    Pin C ────────────────────┼─── Net: GND_SELV
    Pin B ────────────────────┼─── Net: ENC1_CH_B (To STM32 Pin 15 / TIM2_CH2)
                              │
    Net: +3V3_SEC ──[ 10kΩ ]──┴──[ 10nF ]── GND_SELV
    Push Switch S1 ───────────┬─── Net: ENC1_PUSH_SW (To STM32 Pin 21, 10k Pull-up)
    Push Switch S2 ───────────┴─── Net: GND_SELV


    [ ROTARY ENCODER 2: CURRENT LIMIT / OUTPUT ENABLE ]
    Net: +3V3_SEC ──[ 10kΩ ]──┬──[ 10nF ]── GND_SELV
                              │
    Pin A ────────────────────┼─── Net: ENC2_CH_A (To STM32 Pin 22 / TIM3_CH1)
    Pin C ────────────────────┼─── Net: GND_SELV
    Pin B ────────────────────┼─── Net: ENC2_CH_B (To STM32 Pin 23 / TIM3_CH2)
                              │
    Net: +3V3_SEC ──[ 10kΩ ]──┴──[ 10nF ]── GND_SELV
    Push Switch S1 ───────────┬─── Net: ENC2_PUSH_SW (To STM32 Pin 28, 10k Pull-up)
    Push Switch S2 ───────────┴─── Net: GND_SELV


    [ FRONT-PANEL STATUS LEDS ]
    STM32 Pin 2  (PC13) ──[ 1.0kΩ ]──>|── [ LED1: Green (Constant Voltage Mode) ] ── Net: GND_SELV
    STM32 Pin 24 (PC4)  ──[ 1.0kΩ ]──>|── [ LED2: Amber (Constant Current Mode) ] ── Net: GND_SELV
    STM32 Pin 25 (PC5)  ──[ 1.0kΩ ]──>|── [ LED3: Red (Fault / Protective Trip) ] ── Net: GND_SELV


    [ EXTERNAL DC POWER TERMINALS (19.05 mm Pitch) ]
    Net: +V_OUT   ────────────[ J2: RED (+) POMONA 3770-2 BINDING POST ] ─── 30A / 1000V
    Net: GND_SELV ────────────[ J3: BLACK (-) POMONA 3770-0 BINDING POST ] ── 30A / 1000V


    [ J4: 4-PIN SWD DEBUG HEADER ]           [ J5: 3-PIN UART TELEMETRY HEADER ]
    ┌───────────────────────────┐           ┌───────────────────────────┐
    │[1] VTref ── Net: +3V3_SEC │           │[1] TX  ── Net: USART1_TX  │
    │[2] SWDIO ── Net: SWDIO    │           │[2] RX  ── Net: USART1_RX  │
    │[3] SWCLK ── Net: SWCLK    │           │[3] GND ── Net: GND_SELV   │
    │[4] GND   ── Net: GND_SELV │           └───────────────────────────┘
    └───────────────────────────┘
```

---

## 3. Module 9 Comprehensive Netlist

| Net Name | Origin Pin / Pad | Destination Pins / Pads | Net Class | Physical Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `+5V_SEC` | Module 8 Linear Reg | `DISP1` Pin 1 (`VCC`) | Auxiliary Rail | Trace width $1.0\,\text{mm}$ |
| `I2C1_SCL` | STM32 Pin 61 (`PB8`) | `DISP1` Pin 3 (`SCL`), Pull-up $2.2\,\text{k}\Omega$ | I2C Clock | $400\,\text{kHz}$ Fast-Mode |
| `I2C1_SDA` | STM32 Pin 62 (`PB9`) | `DISP1` Pin 4 (`SDA`), Pull-up $2.2\,\text{k}\Omega$ | I2C Data | $400\,\text{kHz}$ Fast-Mode |
| `ENC1_CH_A` | Encoder 1 Pin A | STM32 Pin 14 (`PA0`), Filter Cap $10\,\text{nF}$ | Quadrature Input | Debounced trace |
| `ENC1_CH_B` | Encoder 1 Pin B | STM32 Pin 15 (`PA1`), Filter Cap $10\,\text{nF}$ | Quadrature Input | Debounced trace |
| `ENC1_PUSH_SW`| Encoder 1 Push Switch | STM32 Pin 21 (`PA5`), Pull-up $10\,\text{k}\Omega$ | Digital Input | Tactile momentary input |
| `ENC2_CH_A` | Encoder 2 Pin A | STM32 Pin 22 (`PA6`), Filter Cap $10\,\text{nF}$ | Quadrature Input | Debounced trace |
| `ENC2_CH_B` | Encoder 2 Pin B | STM32 Pin 23 (`PA7`), Filter Cap $10\,\text{nF}$ | Quadrature Input | Debounced trace |
| `ENC2_PUSH_SW`| Encoder 2 Push Switch | STM32 Pin 28 (`PB2`), Pull-up $10\,\text{k}\Omega$ | Digital Input | Tactile momentary input |
| `LED_CV` | STM32 Pin 2 (`PC13`) | Resistor $1.0\,\text{k}\Omega$ to `LED1` Anode | Indicator Drive | Green LED |
| `LED_CC` | STM32 Pin 24 (`PC4`) | Resistor $1.0\,\text{k}\Omega$ to `LED2` Anode | Indicator Drive | Amber LED |
| `LED_FAULT` | STM32 Pin 25 (`PC5`) | Resistor $1.0\,\text{k}\Omega$ to `LED3` Anode | Indicator Drive | Red LED |
| `+V_OUT` | Regulated DC Rail | Output Binding Post `J2` (Red) | Power Output | Heavy 2oz copper polygon |
| `GND_SELV` | Secondary Ground Plane | Output Binding Post `J3` (Black), Returns | Power Output Ground| Heavy 2oz copper polygon |
| `USART1_TX` | STM32 Pin 42 (`PA9`) | Header `J5` Pin 1 | Serial Stream | $115,200\,\text{baud}$ |
| `USART1_RX` | STM32 Pin 43 (`PA10`)| Header `J5` Pin 2 | Serial Command | $115,200\,\text{baud}$ |
| `SWDIO` | STM32 Pin 46 (`PA13`)| Header `J4` Pin 2 | Debug Bus | Bidirectional data |
| `SWCLK` | STM32 Pin 49 (`PA14`)| Header `J4` Pin 3 | Debug Clock | Clock input |

---

## 4. Laboratory Bring-Up & Test Points
* **`TP_OLED_I2C` (Display Comm Check)**: Probe SCL and SDA lines. Verify I2C acknowledge from Address `0x3C` and steady $10\,\text{Hz}$ frame transmissions.
* **`TP_ENC_PULSE` (Encoder Quadrature Check)**: Rotate knob CW and CCW. Verify 90-degree phase shift between Channel A and Channel B with $< 20\,\mu\text{s}$ switch bounce.
* **`TP_POST_VOUT` (Terminal Conduction)**: Connect a $4\,\text{mm}$ calibrated Kelvin load to `J2` and `J3`. Under full $3.00\,\text{A}$ output, measure voltage drop across binding post studs: drop must measure $< 3.0\,\text{mV}$ ($R_{\text{contact}} < 1.0\,\text{m}\Omega$).
""")

    print("Module 9 files successfully generated.")

if __name__ == "__main__":
    write_files()
