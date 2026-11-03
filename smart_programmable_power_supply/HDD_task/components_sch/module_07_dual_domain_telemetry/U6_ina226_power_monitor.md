# Component Schematic Specification: U6 (INA226AIDGSR Secondary I2C Power Monitor)

## 1. Component Metadata
* **Reference Designator**: `U6`
* **Component Type**: High-Precision Bidirectional Current and Power Monitor with I2C Interface
* **Manufacturer**: Texas Instruments
* **Primary MPN**: `INA226AIDGSR`
* **Alternate Manufacturer**: Texas Instruments
* **Alternate MPN**: `INA238AIDGSR` (High-accuracy 16-bit power monitor, 85V bus)
* **Package / Footprint**: VSSOP-10 (Pitch: 0.50 mm, Body: 3.0 × 3.0 mm)
* **Subsystem**: Stage 7 (Secondary DC Output Power Telemetry Engine)

## 2. Electrical Ratings & Constraints
* **Bus Voltage Range (V_BUS)**: 0.0 V to +36.0 V_DC
 * Output rail operating span: +5.0 V to +20.0 V_DC.
 * Maximum rated bus stress derating: (20.0 V / 36.0 V) = 55.5% ≤ 75%.
* **Shunt Full-Scale Voltage Range**: ± 81.92 mV_DC
 * Maximum drop across 10.0 mΩ shunt at 3.0 A:
 V_shunt,max = 3.0 A × 0.010 Ω = 30.00 mV (Derating: 36.6% of full scale)
 * At 4.2 A transient overload: V_shunt,peak = 42.0 mV << 81.92 mV (zero clipping).
* **Quantization Resolution**:
 * Shunt Voltage LSB: 2.5 µV per bit.
 Current LSB = (2.5 µV / 10.0 mΩ) = 250.0 muA per LSB (0.25 mA)
 * Bus Voltage LSB: 1.25 mV per LSB.
 * Power Register LSB: 25 × Current LSB = 6.25 mW per LSB.
* **Measurement Accuracy**:
 * Gain Error: ≤ 0.10% maximum.
 * Offset Voltage: ≤ 10.0 µV maximum (1.0 mA offset).
* **Conversion Time & Digital Averaging**:
 * Programmed for 16× internal hardware averaging with 1.10 ms conversion time per channel (V_BUS and V_shunt). Total sample cycle: 2.20 ms, updated at 10.0 Hz rate.
* **I2C Bus Address**: `0x40` (7-bit address `1000000b`), configured by tying both Address pins `A0` and `A1` to `GND_SELV`.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`IN+`** | `SHUNT_SENSE_P` | `R_shunt` Kelvin Positive Pad (1K) | Dedicated Kelvin sense trace (w = 0.25 mm). |
| **2** | **`IN-`** | `SHUNT_SENSE_N` | `R_shunt` Kelvin Negative Pad (2K) | Dedicated Kelvin sense trace (w = 0.25 mm). |
| **3** | **`VBUS`**| `+V_OUT` | Regulated DC output rail | Senses bus voltage for power calculation. |
| **4** | **`ALERT`**| `NC` | Not used in baseline firmware | Open-drain alert output (optional interrupt). |
| **5** | **`SDA`** | `I2C1_SDA` | STM32 Pin 62 (`PB9`), 2.2 kΩ pull-up | Fast-Mode I2C serial data line. |
| **6** | **`SCL`** | `I2C1_SCL` | STM32 Pin 61 (`PB8`), 2.2 kΩ pull-up | Fast-Mode I2C serial clock line. |
| **7** | **`VS`** | `+3V3_SEC` | Decoupling Cap C_U6 = 100 nF / 16 V | Supply rail (+3.30 V_DC). |
| **8** | **`GND`** | `GND_SELV` | Secondary ground plane | Direct low-impedance ground connection. |
| **9** | **`A1`** | `GND_SELV` | Tied to `GND_SELV` | Sets I2C Address bit A1 = 0. |
| **10**| **`A0`** | `GND_SELV` | Tied to `GND_SELV` | Sets I2C Address bit A0 = 0. |

## 4. Schematic Symbol Representation
```
 [ U6: INA226AIDGSR 16-BIT I2C POWER MONITOR ]
 ┌───────────────┐
 Net: SHUNT_SENSE_P ───────────[1] IN+ A0[10]────────── Net: GND_SELV
 Net: SHUNT_SENSE_N ───────────[2] IN- A1 [9]────────── Net: GND_SELV
 Net: +V_OUT ───────────[3] VBUS GND [8]────────── Net: GND_SELV
 NC ───────────[4] ALERT VS [7]────────── Net: +3V3_SEC
 Net: I2C1_SDA ───────────[5] SDA SCL [6]────────── Net: I2C1_SCL
 └───────────────┘
 Address = 0x40
```

## 5. Schematic & PCB Layout Guidelines
1. **Differential Kelvin Pair**: Route `SHUNT_SENSE_P` and `SHUNT_SENSE_N` as a tight differential pair from `R_shunt`. Place a 10.0 Ω series resistor and 10.0 nF filter capacitor across Pins 1 and 2 directly at the IC to attenuate high-frequency switching noise.
2. **Local Bypass**: Place the 100 nF bypass capacitor within 1.5 mm of Pin 7 (`VS`) and Pin 8 (`GND`).
