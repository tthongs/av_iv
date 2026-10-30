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
* **Supply Voltage ($V_{\text{S}}$)**: $+2.7\,\text{V}$ to $+5.5\,\text{V}_{\text{DC}}$ (Powered from $+3.30\,\text{V}_{\text{DC}}$ LDO rail)
* **Common-Mode Input Range ($V_{\text{CM}}$)**: $-4.0\,\text{V}$ to $+80.0\,\text{V}_{\text{DC}}$
  * Output rail operating common-mode voltage: $+5.0\,\text{V}$ to $+20.0\,\text{V}_{\text{DC}}$.
  * Operates well within the $-4\text{V}$ to $+80\text{V}$ linear common-mode operating range!
* **Fixed Voltage Gain ($A_v$)**: $\mathbf{50.0\,\text{V/V}} \pm 0.20\%$ maximum gain error.
* **Bandwidth ($-3\,\text{dB}$)**: $400.0\,\text{kHz}$
* **Slew Rate ($SR$)**: $2.0\,\text{V}/\mu\text{s}$
* **Enhanced PWM Common-Mode Rejection**:
  * Features internal active EMI/PWM rejection filters providing $> 90\,\text{dB}$ rejection at $300\,\text{kHz}$ switching edges.
* **Input Offset Voltage ($V_{\text{OS}}$)**: $\pm 25\,\mu\text{V}$ maximum ($\pm 5\,\mu\text{V}$ typical)
* **Transfer Function & Sizing**:
  $$V_{\text{CS,out}} = I_{\text{OUT}} \times R_{\text{shunt}} \times A_v + V_{\text{REF}}$$
  With $V_{\text{REF}}$ tied to `AGND_SEC` ($0.0\,\text{V}$) for unidirectional sensing:
  $$V_{\text{CS,out}} = I_{\text{OUT}} \times (0.010\,\Omega) \times 50.0\,\text{V/V} = I_{\text{OUT}} \times \mathbf{0.500\,\text{V/A}}$$
  * **At $I_{\text{OUT}} = 0.0\,\text{A}$ (Zero Load)**: $V_{\text{CS,out}} = 0.000\,\text{V}$
  * **At $I_{\text{OUT}} = 3.0\,\text{A}$ (Continuous Rated Load)**: $V_{\text{CS,out}} = 3.0 \times 0.500 = \mathbf{1.500\,\text{V}_{\text{DC}}}$
  * **At $I_{\text{OUT}} = 3.20\,\text{A}$ (Hardware Trip Setpoint)**: $V_{\text{CS,out}} = 3.20 \times 0.500 = \mathbf{1.600\,\text{V}_{\text{DC}}}$
  * **At $I_{\text{OUT}} = 4.20\,\text{A}$ (Surge Overload)**: $V_{\text{CS,out}} = 4.20 \times 0.500 = \mathbf{2.100\,\text{V}_{\text{DC}}}$

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`IN+`** | `SHUNT_SENSE_P` | `R_shunt` Kelvin Positive terminal (1K) | Dedicated Kelvin differential trace ($w = 0.25\,\text{mm}$). |
| **2** | **`GND`** | `AGND_SEC` | Quiet secondary analog ground plane | Direct low-inductance connection to `AGND_SEC`. |
| **3** | **`REF2`**| `AGND_SEC` | Tied to `AGND_SEC` | Sets unidirectional zero-volt output reference. |
| **4** | **`OUT`** | `FAST_CC_SENSE` | Non-inverting input (Pin 3) of comparator `U8_FAST_CC` | Short $0.3\,\text{mm}$ trace ($< 5.0\,\text{mm}$). |
| **5** | **`NC`**  | `NC` | No internal connection | Leave floating. |
| **6** | **`REF1`**| `AGND_SEC` | Tied to `AGND_SEC` | Sets unidirectional zero-volt output reference. |
| **7** | **`VS`**  | `+3V3_SEC` | Local decoupling cap $C_{\text{U7}} = 100\,\text{nF} / 16\,\text{V}$ X7R | Connects to clean $+3.30\,\text{V}_{\text{DC}}$ analog rail. |
| **8** | **`IN-`** | `SHUNT_SENSE_N` | `R_shunt` Kelvin Negative terminal (2K) | Dedicated Kelvin differential trace ($w = 0.25\,\text{mm}$). |

## 4. Schematic Symbol Representation
```
                     [ U7_FAST_CC: INA240A2EDCKR CURRENT AMP ]
                                 ┌───────────────┐
   Net: SHUNT_SENSE_P ──────────[1] IN+       IN-[8]────────── Net: SHUNT_SENSE_N
   Net: AGND_SEC      ──────────[2] GND        VS[7]────────── Net: +3V3_SEC
   Net: AGND_SEC      ──────────[3] REF2       NC[6]────────── NC
   Net: FAST_CC_SENSE ──────────[4] OUT      REF1[5]────────── Net: AGND_SEC
                                 └───────────────┘
                                   Av = 50.0 V/V
```

## 5. Schematic & PCB Layout Guidelines
1. **Direct Shunt Connection**: Route `SHUNT_SENSE_P` and `SHUNT_SENSE_N` directly from the Kelvin sense terminals of Bourns `R_shunt` as a tightly coupled differential pair. Shield with ground planes on adjacent layers.
2. **Local Bypass**: Place a $100\,\text{nF}$ X7R ceramic bypass capacitor within $1.5\,\text{mm}$ of Pin 7 (`VS`) and Pin 2 (`GND`).
3. **Bandwidth Preservation**: Keep the output trace `FAST_CC_SENSE` short and direct to Pin 3 of `U8_FAST_CC`. Total parasitic capacitive loading must be $< 15\,\text{pF}$ to preserve the $2.0\,\text{V}/\mu\text{s}$ slew rate.
