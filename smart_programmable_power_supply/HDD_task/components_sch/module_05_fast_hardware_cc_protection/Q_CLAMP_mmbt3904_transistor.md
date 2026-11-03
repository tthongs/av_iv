# Component Schematic Specification: Q_CLAMP (COMP Pin Pull-Down Clamping Transistor)

## 1. Component Metadata
* **Reference Designator**: `Q_CLAMP`
* **Component Type**: General-Purpose High-Speed NPN Bipolar Junction Transistor
* **Manufacturer**: Diodes Incorporated / ON Semiconductor
* **Primary MPN**: `MMBT3904`
* **Alternate Manufacturer**: Nexperia
* **Alternate MPN**: `PMBT3904`
* **Package / Footprint**: SOT-23-3 (TO-236AB, Pitch: 0.95 mm, Body: 2.9 × 1.3 mm)
* **Subsystem**: Stage 5 (Autonomous Fast Hardware Current Clamping Subsystem)

## 2. Electrical Ratings & Constraints
* **Collector-Emitter Breakdown Voltage (V_CEO)**: 40.0 V_DC
 * Clamping node voltage (`LM5176_COMP`): Normal operating span 0.80 V to 2.80 V_DC.
 * Voltage Derating: (2.80 V / 40.0 V) = 7.0% (Negligible voltage stress).
* **Continuous Collector Current (I_C)**: 200.0 mA
 * LM5176 internal error amplifier sourcing capability: I_COMP,source ≈ 1.20 mA.
 * Current Derating: (1.20 mA / 200 mA) = 0.60% (Enormous margin).
* **Collector-Emitter Saturation Voltage (V_CE(sat)**:
 * < 0.150 V_DC at I_C = 10 mA, I_B = 1.0 mA.
 * At I_C = 1.2 mA: V_CE(sat) ≈ mathbf{0.080 V_DC}.
 * The LM5176 controller guarantees 0% duty cycle and immediate PWM gating inhibit when `COMP` is pulled below 0.400 V_DC. 0.080 V << 0.400 V guarantees **100% positive PWM shutdown**!
* **Switching Turn-On Time (t_on)**:
 * Delay time (t_d): 10.0 ns
 * Rise time (t_r): 25.0 ns
 * Total saturation turn-on latency: t_sat ≤ 250.0 ns under 2.5 mA overdrive.
* **Base Drive Sizing**:
 * Base Series Resistor: R_B_CLAMP = 1.0 kΩ ± 1% (0603 SMD).
 * Base Pull-Down Resistor: R_BE = 10.0 kΩ ± 1% (0603 SMD) from Base to Emitter (`AGND_SEC`).
 * Base Drive Current when TLV3501 trips (V_OUT = 3.3 V):
 I_B = (3.30 V - V_BE / R_B_CLAMP) = (3.30 V - 0.75 V / 1000 Ω) = 2.55 mA
 * Forced beta: β_forced = (I_C / I_B) = (1.20 mA / 2.55 mA) = 0.47 << 10 (Deep saturation guaranteed!).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`BASE`** | `Q_CLAMP_BASE` | Base resistor `R_B_CLAMP` (1.0 kΩ), Pull-down `R_BE` (10 kΩ) | Driven by comparator output `FAST_CC_TRIP`. |
| **2** | **`EMITTER`**| `AGND_SEC` | Quiet secondary analog ground plane | Direct low-impedance ground connection. |
| **3** | **`COLLECTOR`**| `LM5176_COMP` | LM5176 Pin 6 (`COMP`), Type-II compensation network | Direct connection to error amp output. |

## 4. Schematic Symbol Representation
```
 [ Q_CLAMP: MMBT3904 NPN CLAMP TRANSISTOR ]
 Collector (Pin 3)
 │
 ├─── Net: LM5176_COMP (Pin 6)
 ┌───┴───┐
 │ NPN │
 Net: FAST_CC_TRIP ──[ 1.0 kΩ ]──────┤B E├── Net: AGND_SEC (Pin 2)
 └───────┘
 Base (Pin 1)
 │
 [ 10 kΩ ]
 │
 Net: AGND_SEC
```

## 5. Schematic & PCB Layout Guidelines
1. **Direct COMP Pin Placement**: Place `Q_CLAMP` immediately adjacent to Pin 6 (`COMP`) of `U3` LM5176. The collector trace must be < 2.0 mm to prevent adding stray capacitance to the sensitive feedback loop.
2. **Quiet Emitter Ground**: Return Pin 2 (`EMITTER`) directly to `AGND_SEC` at `U3` Pin 11, avoiding power ground planes that carry switching currents.
