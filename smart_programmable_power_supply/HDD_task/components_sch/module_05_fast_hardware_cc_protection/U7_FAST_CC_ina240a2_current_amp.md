# Component Schematic Specification: U7_FAST_CC (INA240A2 Precision Current Sense Amplifier)

## 1. Component Metadata
* **Reference Designator**: `U7_FAST_CC`
* **Component Type**: High-Bandwidth Current Sense Amplifier with Enhanced PWM Rejection
* **Manufacturer**: Texas Instruments
* **Primary MPN**: `INA240A2EDCKR`
* **Alternate Manufacturer**: Analog Devices
* **Alternate MPN**: `AD8418AWBRZ` (Bidirectional, Av = 20/50 V/V equivalent)
* **Package / Footprint**: SC70-8 (Thin Shrink Small Outline, Pitch: 0.65 mm, Body: 2.0 × 1.25 mm)
* **Subsystem**: Stage 5 (Autonomous Fast Hardware Current Clamping Subsystem)

## 2. Electrical Ratings & Constraints
* **Supply Voltage (V_S)**: +2.7 V to +5.5 V_DC (Powered from +3.30 V_DC LDO rail)
* **Common-Mode Input Range (V_CM)**: -4.0 V to +80.0 V_DC
 * Output rail operating common-mode voltage: +5.0 V to +20.0 V_DC.
 * Operates well within the -4V to +80V linear common-mode operating range!
* **Fixed Voltage Gain (A_v)**: 50.0 V/V ± 0.20% maximum gain error.
* **Bandwidth (-3 dB)**: 400.0 kHz
* **Slew Rate (SR)**: 2.0 V/µs
* **Enhanced PWM Common-Mode Rejection**:
 * Features internal active EMI/PWM rejection filters providing > 90 dB rejection at 300 kHz switching edges.
* **Input Offset Voltage (V_OS)**: ± 25 µV maximum (± 5 µV typical)
* **Transfer Function & Sizing**:
 V_CS,out = I_OUT × R_shunt × A_v + V_REF
 With V_REF tied to `AGND_SEC` (0.0 V) for unidirectional sensing:
 V_CS,out = I_OUT × (0.010 Ω) × 50.0 V/V = I_OUT × 0.500 V/A
 * **At I_OUT = 0.0 A (Zero Load)**: V_CS,out = 0.000 V
 * **At I_OUT = 3.0 A (Continuous Rated Load)**: V_CS,out = 3.0 × 0.500 = mathbf{1.500 V_DC}
 * **At I_OUT = 3.20 A (Hardware Trip Setpoint)**: V_CS,out = 3.20 × 0.500 = mathbf{1.600 V_DC}
 * **At I_OUT = 4.20 A (Surge Overload)**: V_CS,out = 4.20 × 0.500 = mathbf{2.100 V_DC}

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`IN+`** | `SHUNT_SENSE_P` | `R_shunt` Kelvin Positive terminal (1K) | Dedicated Kelvin differential trace (w = 0.25 mm). |
| **2** | **`GND`** | `AGND_SEC` | Quiet secondary analog ground plane | Direct low-inductance connection to `AGND_SEC`. |
| **3** | **`REF2`**| `AGND_SEC` | Tied to `AGND_SEC` | Sets unidirectional zero-volt output reference. |
| **4** | **`OUT`** | `FAST_CC_SENSE` | Non-inverting input (Pin 3) of comparator `U8_FAST_CC` | Short 0.3 mm trace (< 5.0 mm). |
| **5** | **`NC`** | `NC` | No internal connection | Leave floating. |
| **6** | **`REF1`**| `AGND_SEC` | Tied to `AGND_SEC` | Sets unidirectional zero-volt output reference. |
| **7** | **`VS`** | `+3V3_SEC` | Local decoupling cap C_U7 = 100 nF / 16 V X7R | Connects to clean +3.30 V_DC analog rail. |
| **8** | **`IN-`** | `SHUNT_SENSE_N` | `R_shunt` Kelvin Negative terminal (2K) | Dedicated Kelvin differential trace (w = 0.25 mm). |

## 4. Schematic Symbol Representation
```
 [ U7_FAST_CC: INA240A2EDCKR CURRENT AMP ]
 ┌───────────────┐
 Net: SHUNT_SENSE_P ──────────[1] IN+ IN-[8]────────── Net: SHUNT_SENSE_N
 Net: AGND_SEC ──────────[2] GND VS[7]────────── Net: +3V3_SEC
 Net: AGND_SEC ──────────[3] REF2 NC[6]────────── NC
 Net: FAST_CC_SENSE ──────────[4] OUT REF1[5]────────── Net: AGND_SEC
 └───────────────┘
 Av = 50.0 V/V
```

## 5. Schematic & PCB Layout Guidelines
1. **Direct Shunt Connection**: Route `SHUNT_SENSE_P` and `SHUNT_SENSE_N` directly from the Kelvin sense terminals of Bourns `R_shunt` as a tightly coupled differential pair. Shield with ground planes on adjacent layers.
2. **Local Bypass**: Place a 100 nF X7R ceramic bypass capacitor within 1.5 mm of Pin 7 (`VS`) and Pin 2 (`GND`).
3. **Bandwidth Preservation**: Keep the output trace `FAST_CC_SENSE` short and direct to Pin 3 of `U8_FAST_CC`. Total parasitic capacitive loading must be < 15 pF to preserve the 2.0 V/µs slew rate.
