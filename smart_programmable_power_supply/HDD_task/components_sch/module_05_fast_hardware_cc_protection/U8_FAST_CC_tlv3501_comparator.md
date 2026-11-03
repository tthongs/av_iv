# Component Schematic Specification: U8_FAST_CC (TLV3501 High-Speed Comparator)

## 1. Component Metadata
* **Reference Designator**: `U8_FAST_CC`
* **Component Type**: Ultra-Fast Push-Pull Rail-to-Rail Output Comparator
* **Manufacturer**: Texas Instruments
* **Primary MPN**: `TLV3501AIDBVR`
* **Alternate Manufacturer**: Analog Devices
* **Alternate MPN**: `ADCMP600BKSZ` (Single-supply high-speed TTL/CMOS comparator, 3.5 ns)
* **Package / Footprint**: SOT-23-6 (Pitch: 0.95 mm, Body: 2.9 × 1.6 mm)
* **Subsystem**: Stage 5 (Autonomous Fast Hardware Current Clamping Subsystem)

## 2. Electrical Ratings & Constraints
* **Supply Voltage (V_CC)**: +2.7 V to +5.5 V_DC (Operates on +3.30 V_DC rail)
* **Ultra-Fast Propagation Delay (t_pd)**: 4.5 ns typical (6.0 ns max) with 20 mV overdrive.
* **Overdrive Dispersion**: < 1.5 ns across 10 mV to 100 mV overdrive.
* **Toggle Frequency**: Up to 80.0 MHz
* **Output Stage**: Full CMOS Push-Pull Rail-to-Rail.
 * Drives high logic level to +3.30 V and low logic level to < 0.10 V.
 * Capable of sourcing 25.0 mA directly into the base of clamping transistor `Q_CLAMP`.
* **Trip Reference Threshold Voltage (V_trip)**:
 Generated via precision 2-resistor voltage divider from clean +3.30 V_DC rail:
 * Top Divider Resistor: R_ref1 = 10.6 kΩ ± 0.1% (Vishay `TNPW080510K6BEEA`)
 * Bottom Divider Resistor: R_ref2 = 10.0 kΩ ± 0.1% (Vishay `TNPW080510K0BEEA`)
 V_trip = (+3.300 V) × (R_ref2 / R_ref1 + R_ref2) = 3.300 V × (10.0 kΩ / 20.6 kΩ) = mathbf{1.6019 V_DC}
 * Perfectly matches the 3.20 A current limit threshold:
 I_trip = (V_trip / 0.500 V/A) = (1.602 V / 0.500) = mathbf{3.204 A_DC}
* **Hysteresis Resistor (R_hys)**: 470.0 kΩ connected from Push-Pull Output (Pin 1) to Non-Inverting input (Pin 3), providing ≈ 35 mV clean hysteresis (70 mA load current hysteresis) to eliminate chatter during transition.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Description & Trace Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`OUT`** | `FAST_CC_TRIP` | Base resistor `R_B_CLAMP` (1.0 kΩ), Hysteresis `R_hys` | Fast CMOS output. Connects to `Q_CLAMP` base. |
| **2** | **`GND`** | `AGND_SEC` | Quiet secondary analog ground plane | Direct low-inductance connection. |
| **3** | **`IN+`** | `FAST_CC_SENSE` | INA240 output (Pin 4), Hysteresis `R_hys` | Senses amplified current voltage (0.500 V/A). |
| **4** | **`IN-`** | `VREF_1V60_TRIP`| Reference divider node (`R_ref1` / `R_ref2`) | Precision 1.602 V trip threshold reference. |
| **5** | **`SHDN_N`**| `+3V3_SEC` | Tied to +3.3 V rail | Comparator permanently enabled in active operating state. |
| **6** | **`VCC`** | `+3V3_SEC` | Local decoupling cap C_U8 = 100 nF / 16 V C0G | Clean +3.30 V_DC analog supply rail. |

## 4. Schematic Symbol Representation
```
 [ U8_FAST_CC: TLV3501AIDBVR 4.5ns COMPARATOR ]
 ┌───────────────┐
 Net: FAST_CC_TRIP ──────────[1] OUT VCC[6]────────── Net: +3V3_SEC
 Net: AGND_SEC ──────────[2] GND SHDN[5]────────── Net: +3V3_SEC
 Net: FAST_CC_SENSE ──────────[3] IN+ IN-[4]────────── Net: VREF_1V60_TRIP
 └───────────────┘
 t_pd = 4.5 ns
```

## 5. Schematic & PCB Layout Guidelines
1. **Ultra-Low Parasitic Inductance**: TLV3501 switches in 4.5 ns. Route output trace `FAST_CC_TRIP` with minimal length (< 4.0 mm) to base resistor `R_B_CLAMP` to prevent parasitic ringing.
2. **Decoupling**: Decouple Pin 6 (`VCC`) with a 100 nF high-frequency C0G/X7R ceramic capacitor directly to Pin 2 (`GND`) with wide surface traces and no via indirection.
3. **Reference Decoupling**: Place a 10 nF C0G capacitor from `VREF_1V60_TRIP` (Pin 4) to `AGND_SEC` to suppress any noise coupling onto the trip threshold.
