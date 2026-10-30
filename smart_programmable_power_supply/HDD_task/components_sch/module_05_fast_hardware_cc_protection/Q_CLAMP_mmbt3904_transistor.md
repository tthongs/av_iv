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
* **Collector-Emitter Breakdown Voltage ($V_{\text{CEO}}$)**: $40.0\,\text{V}_{\text{DC}}$
  * Clamping node voltage (`LM5176_COMP`): Normal operating span $0.80\,\text{V}$ to $2.80\,\text{V}_{\text{DC}}$.
  * Voltage Derating: $\frac{2.80\,\text{V}}{40.0\,\text{V}} = \mathbf{7.0\%}$ (Negligible voltage stress).
* **Continuous Collector Current ($I_C$)**: $200.0\,\text{mA}$
  * LM5176 internal error amplifier sourcing capability: $I_{\text{COMP,source}} \approx 1.20\,\text{mA}$.
  * Current Derating: $\frac{1.20\,\text{mA}}{200\,\text{mA}} = \mathbf{0.60\%}$ (Enormous margin).
* **Collector-Emitter Saturation Voltage ($V_{\text{CE(sat)}}$)**:
  * $< 0.150\,\text{V}_{\text{DC}}$ at $I_C = 10\,\text{mA}, I_B = 1.0\,\text{mA}$.
  * At $I_C = 1.2\,\text{mA}$: $V_{\text{CE(sat)}} \approx \mathbf{0.080\,\text{V}_{\text{DC}}}$.
  * The LM5176 controller guarantees $0\%$ duty cycle and immediate PWM gating inhibit when `COMP` is pulled below $0.400\,\text{V}_{\text{DC}}$. $0.080\,\text{V} \ll 0.400\,\text{V}$ guarantees **$100\%$ positive PWM shutdown**!
* **Switching Turn-On Time ($t_{\text{on}}$)**:
  * Delay time ($t_d$): $10.0\,\text{ns}$
  * Rise time ($t_r$): $25.0\,\text{ns}$
  * Total saturation turn-on latency: $t_{\text{sat}} \le \mathbf{250.0\,\text{ns}}$ under $2.5\,\text{mA}$ overdrive.
* **Base Drive Sizing**:
  * Base Series Resistor: $R_{\text{B_CLAMP}} = 1.0\,\text{k}\Omega \pm 1\%$ (0603 SMD).
  * Base Pull-Down Resistor: $R_{\text{BE}} = 10.0\,\text{k}\Omega \pm 1\%$ (0603 SMD) from Base to Emitter (`AGND_SEC`).
  * Base Drive Current when TLV3501 trips ($V_{\text{OUT}} = 3.3\,\text{V}$):
    $$I_B = \frac{3.30\,\text{V} - V_{\text{BE}}}{R_{\text{B_CLAMP}}} = \frac{3.30\,\text{V} - 0.75\,\text{V}}{1000\,\Omega} = \mathbf{2.55\,\text{mA}}$$
  * Forced beta: $\beta_{\text{forced}} = \frac{I_C}{I_B} = \frac{1.20\,\text{mA}}{2.55\,\text{mA}} = 0.47 \ll 10$ (Deep saturation guaranteed!).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`BASE`** | `Q_CLAMP_BASE` | Base resistor `R_B_CLAMP` ($1.0\,\text{k}\Omega$), Pull-down `R_BE` ($10\,\text{k}\Omega$) | Driven by comparator output `FAST_CC_TRIP`. |
| **2** | **`EMITTER`**| `AGND_SEC` | Quiet secondary analog ground plane | Direct low-impedance ground connection. |
| **3** | **`COLLECTOR`**| `LM5176_COMP` | LM5176 Pin 6 (`COMP`), Type-II compensation network | Direct connection to error amp output. |

## 4. Schematic Symbol Representation
```
                     [ Q_CLAMP: MMBT3904 NPN CLAMP TRANSISTOR ]
                                    Collector (Pin 3)
                                          │
                                          ├─── Net: LM5176_COMP (Pin 6)
                                      ┌───┴───┐
                                      │  NPN  │
  Net: FAST_CC_TRIP ──[ 1.0 kΩ ]──────┤B     E├── Net: AGND_SEC (Pin 2)
                                      └───────┘
                                      Base (Pin 1)
                                          │
                                       [ 10 kΩ ]
                                          │
                                    Net: AGND_SEC
```

## 5. Schematic & PCB Layout Guidelines
1. **Direct COMP Pin Placement**: Place `Q_CLAMP` immediately adjacent to Pin 6 (`COMP`) of `U3` LM5176. The collector trace must be $< 2.0\,\text{mm}$ to prevent adding stray capacitance to the sensitive feedback loop.
2. **Quiet Emitter Ground**: Return Pin 2 (`EMITTER`) directly to `AGND_SEC` at `U3` Pin 11, avoiding power ground planes that carry switching currents.
