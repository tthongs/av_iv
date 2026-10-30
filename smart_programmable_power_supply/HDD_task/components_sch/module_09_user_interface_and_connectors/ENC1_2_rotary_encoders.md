# Component Schematic Specification: ENC1, ENC2 (Incremental Rotary Encoders)

## 1. Component Metadata
* **Reference Designators**: `ENC1` (Voltage Adjust / Fine-Coarse Toggle), `ENC2` (Current Adjust / Output Enable Toggle)
* **Component Type**: Incremental Contacting Mechanical Rotary Encoder with Integrated Push Switch
* **Manufacturer**: Bourns Inc.
* **Primary MPN**: `PEC11R-4220F-S0024`
* **Alternate Manufacturer**: Alps Alpine
* **Alternate MPN**: `EC11E2424407` (24 Pulses/Rev, with push switch)
* **Package / Footprint**: Through-Hole Right-Angle Bracket Mount (Shaft Length: 20 mm, D-Cut Flat)
* **Subsystem**: Stage 9 (Front-Panel User Interface & Adjustment Controls)

## 2. Electrical Ratings & Constraints
* **Pulses per Revolution**: $24$ Pulses / $24$ Detents ($360^\circ$ continuous rotation).
* **Contact Rating**: $10.0\,\text{mA}$ at $5.0\,\text{V}_{\text{DC}}$ ($0.5\,\text{W}$ max).
* **Rotational Life**: $> 30,000$ cycles.
* **Integrated Push Switch**: SPST Normally Open momentary tactile switch ($20,000$ cycles).
* **Quadrature Channel Phasing**: Channel A leads Channel B in clockwise (CW) rotation.
* **Hardware Debouncing Filter Design**:
  Mechanical switch contacts exhibit bouncing noise for up to $t_{\text{bounce}} \approx 3.0\,\text{ms}$. To guarantee glitch-free decoding by the STM32 timer hardware without CPU polling overhead, each phase line is buffered by an external passive RC filter:
  * Pull-Up Resistor: $R_{\text{pull}} = 10.0\,\text{k}\Omega \pm 1\%$ tied to $+3.30\,\text{V}_{\text{SEC}}$.
  * Filter Capacitor: $C_{\text{deb}} = 10.0\,\text{nF} \pm 10\%$ 50V C0G ceramic to `GND_SELV`.
  * Time Constant:
    $$\tau = R_{\text{pull}} \times C_{\text{deb}} = (10.0\,\text{k}\Omega) \times (10.0\,\text{nF}) = \mathbf{100.0\,\mu\text{s}}$$
  * Eliminates mechanical contact bounce while allowing fast manual rotation up to $600\,\text{RPM}$ ($4.16\,\text{ms}$ per detent step) without missing pulses.

## 3. Schematic Pin Connections & Net Mapping

### 3.1 Encoder 1: Voltage Setting & Coarse/Fine Switch
| Pin # | Pin Designation | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **A** | **Phase A** | `ENC1_CH_A` | STM32 Pin 14 (`PA0` / TIM2_CH1) | Filtered quadrature Phase A ($10\,\text{k}\Omega + 10\,\text{nF}$). |
| **C** | **Common**  | `GND_SELV` | Secondary ground plane | Signal return ground. |
| **B** | **Phase B** | `ENC1_CH_B` | STM32 Pin 15 (`PA1` / TIM2_CH2) | Filtered quadrature Phase B ($10\,\text{k}\Omega + 10\,\text{nF}$). |
| **S1**| **Switch Terminal 1**| `ENC1_PUSH_SW`| STM32 Pin 21 (`PA5`), $10\,\text{k}\Omega$ pull-up| Toggles Voltage Adjustment Step: Coarse ($1.0\,\text{V}$) vs Fine ($10\,\text{mV}$). |
| **S2**| **Switch Terminal 2**| `GND_SELV` | Secondary ground plane | Pushbutton ground return. |

### 3.2 Encoder 2: Current Limit & Output Enable Switch
| Pin # | Pin Designation | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **A** | **Phase A** | `ENC2_CH_A` | STM32 Pin 22 (`PA6` / TIM3_CH1) | Filtered quadrature Phase A ($10\,\text{k}\Omega + 10\,\text{nF}$). |
| **C** | **Common**  | `GND_SELV` | Secondary ground plane | Signal return ground. |
| **B** | **Phase B** | `ENC2_CH_B` | STM32 Pin 23 (`PA7` / TIM3_CH2) | Filtered quadrature Phase B ($10\,\text{k}\Omega + 10\,\text{nF}$). |
| **S1**| **Switch Terminal 1**| `ENC2_PUSH_SW`| STM32 Pin 28 (`PB2`), $10\,\text{k}\Omega$ pull-up| Momentary press toggles Output DC Power Enable / Inhibit. |
| **S2**| **Switch Terminal 2**| `GND_SELV` | Secondary ground plane | Pushbutton ground return. |

## 4. Schematic Symbol Representation
```
                    [ BOURNS PEC11R ROTARY ENCODER INTERFACE ]
                                  Net: +3V3_SEC
                                   │         │
                                [10kΩ]    [10kΩ]
                                   │         │
                                   ├──[10nF]─┼──[10nF]── Net: GND_SELV
                                   │         │
                                ┌──┴──┐   ┌──┴──┐
       Phase A (Net: ENC_CH_A) ─┤A   C├─┬─┤B   S├─ (Net: ENC_CH_B) Phase B
                                └─────┘ │ └─────┘
                                        │    │
                                 Net: GND   └── Net: ENC_PUSH_SW (To MCU Pin)
```

## 5. Schematic & PCB Layout Guidelines
1. **Chassis Standoff**: The through-hole mounting bracket lugs provide mechanical rigidity against user torque. Solder the two mounting tabs solidly into plated through-holes tied to chassis earth or secondary ground.
2. **Debounce Placement**: Place the $10\,\text{k}\Omega$ pull-up resistors and $10\,\text{nF}$ capacitors close to the MCU input pins to reject capacitive pickup along the front-panel routing harness.
