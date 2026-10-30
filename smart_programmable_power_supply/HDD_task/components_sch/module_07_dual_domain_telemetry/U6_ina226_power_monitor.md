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
* **Bus Voltage Range ($V_{\text{BUS}}$)**: $0.0\,\text{V}$ to $+36.0\,\text{V}_{\text{DC}}$
  * Output rail operating span: $+5.0\,\text{V}$ to $+20.0\,\text{V}_{\text{DC}}$.
  * Maximum rated bus stress derating: $\frac{20.0\,\text{V}}{36.0\,\text{V}} = \mathbf{55.5\%} \le 75\%$.
* **Shunt Full-Scale Voltage Range**: $\pm 81.92\,\text{mV}_{\text{DC}}$
  * Maximum drop across $10.0\,\text{m}\Omega$ shunt at $3.0\,\text{A}$:
    $$V_{\text{shunt,max}} = 3.0\,\text{A} \times 0.010\,\Omega = \mathbf{30.00\,\text{mV}} \quad (\text{Derating: } 36.6\% \text{ of full scale})$$
  * At $4.2\,\text{A}$ transient overload: $V_{\text{shunt,peak}} = 42.0\,\text{mV} \ll 81.92\,\text{mV}$ (zero clipping).
* **Quantization Resolution**:
  * Shunt Voltage LSB: $2.5\,\mu\text{V}$ per bit.
    $$\text{Current LSB} = \frac{2.5\,\mu\text{V}}{10.0\,\text{m}\Omega} = \mathbf{250.0\,\mu\text{A per LSB}} \quad (0.25\,\text{mA})$$
  * Bus Voltage LSB: $\mathbf{1.25\,\text{mV per LSB}}$.
  * Power Register LSB: $25 \times \text{Current LSB} = \mathbf{6.25\,\text{mW per LSB}}$.
* **Measurement Accuracy**:
  * Gain Error: $\le 0.10\%$ maximum.
  * Offset Voltage: $\le 10.0\,\mu\text{V}$ maximum ($1.0\,\text{mA}$ offset).
* **Conversion Time & Digital Averaging**:
  * Programmed for $16\times$ internal hardware averaging with $1.10\,\text{ms}$ conversion time per channel ($V_{\text{BUS}}$ and $V_{\text{shunt}}$). Total sample cycle: $2.20\,\text{ms}$, updated at $10.0\,\text{Hz}$ rate.
* **I2C Bus Address**: `0x40` (7-bit address `1000000b`), configured by tying both Address pins `A0` and `A1` to `GND_SELV`.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`IN+`** | `SHUNT_SENSE_P` | `R_shunt` Kelvin Positive Pad (1K) | Dedicated Kelvin sense trace ($w = 0.25\,\text{mm}$). |
| **2** | **`IN-`** | `SHUNT_SENSE_N` | `R_shunt` Kelvin Negative Pad (2K) | Dedicated Kelvin sense trace ($w = 0.25\,\text{mm}$). |
| **3** | **`VBUS`**| `+V_OUT` | Regulated DC output rail | Senses bus voltage for power calculation. |
| **4** | **`ALERT`**| `NC` | Not used in baseline firmware | Open-drain alert output (optional interrupt). |
| **5** | **`SDA`** | `I2C1_SDA` | STM32 Pin 62 (`PB9`), $2.2\,\text{k}\Omega$ pull-up | Fast-Mode I2C serial data line. |
| **6** | **`SCL`** | `I2C1_SCL` | STM32 Pin 61 (`PB8`), $2.2\,\text{k}\Omega$ pull-up | Fast-Mode I2C serial clock line. |
| **7** | **`VS`**  | `+3V3_SEC` | Decoupling Cap $C_{\text{U6}} = 100\,\text{nF} / 16\,\text{V}$ | Supply rail ($+3.30\,\text{V}_{\text{DC}}$). |
| **8** | **`GND`** | `GND_SELV` | Secondary ground plane | Direct low-impedance ground connection. |
| **9** | **`A1`**  | `GND_SELV` | Tied to `GND_SELV` | Sets I2C Address bit A1 = 0. |
| **10**| **`A0`**  | `GND_SELV` | Tied to `GND_SELV` | Sets I2C Address bit A0 = 0. |

## 4. Schematic Symbol Representation
```
                    [ U6: INA226AIDGSR 16-BIT I2C POWER MONITOR ]
                                  ┌───────────────┐
   Net: SHUNT_SENSE_P ───────────[1] IN+       A0[10]────────── Net: GND_SELV
   Net: SHUNT_SENSE_N ───────────[2] IN-       A1 [9]────────── Net: GND_SELV
        Net: +V_OUT   ───────────[3] VBUS     GND [8]────────── Net: GND_SELV
             NC       ───────────[4] ALERT     VS [7]────────── Net: +3V3_SEC
       Net: I2C1_SDA  ───────────[5] SDA      SCL [6]────────── Net: I2C1_SCL
                                  └───────────────┘
                                   Address = 0x40
```

## 5. Schematic & PCB Layout Guidelines
1. **Differential Kelvin Pair**: Route `SHUNT_SENSE_P` and `SHUNT_SENSE_N` as a tight differential pair from `R_shunt`. Place a $10.0\,\Omega$ series resistor and $10.0\,\text{nF}$ filter capacitor across Pins 1 and 2 directly at the IC to attenuate high-frequency switching noise.
2. **Local Bypass**: Place the $100\,\text{nF}$ bypass capacitor within $1.5\,\text{mm}$ of Pin 7 (`VS`) and Pin 8 (`GND`).
