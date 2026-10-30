# Component Schematic Specification: J4 (SWD Firmware Programming & Debug Header)

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
