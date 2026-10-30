# Component Schematic Specification: J5 (UART Serial Telemetry Header)

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
