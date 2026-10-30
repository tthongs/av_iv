# Component Schematic Specification: DISP1 (1.3" Monochrome I2C OLED Module)

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
