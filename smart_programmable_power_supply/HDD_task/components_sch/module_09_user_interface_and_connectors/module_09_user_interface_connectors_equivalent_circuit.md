# Module 9 Equivalent Electronic Circuit: User Interface & Connectors Subsystem

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
