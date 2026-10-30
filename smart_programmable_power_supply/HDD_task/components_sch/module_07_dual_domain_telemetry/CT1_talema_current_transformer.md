# Component Schematic Specification: CT1 (AC Mains Current Transformer)

## 1. Component Metadata
* **Reference Designator**: `CT1`
* **Component Type**: High-Accuracy Toroidal AC Current Transformer
* **Manufacturer**: Talema Group
* **Primary MPN**: `AC1010`
* **Alternate Manufacturer**: CR Magnetics
* **Alternate MPN**: `CR8410-1000` (10 A RMS, 1000:1 ratio, 4000 V isolation)
* **Package / Footprint**: Encapsulated Through-Hole Toroid with Central Primary Conductor Hole
* **Subsystem**: Stage 7 (Primary AC Mains Isolated Current Telemetry)

## 2. Electrical Ratings & Constraints
* **Current Transformation Turns Ratio ($N_{\text{pri}}:N_{\text{sec}}$)**: $1 : 1000$ ($1000$ secondary turns).
* **Rated Primary Continuous Current ($I_{\text{pri,rated}}$)**: $10.0\,\text{A}_{\text{RMS}}$ ($50/60\,\text{Hz}$).
  * Maximum operating AC input current: $1.604\,\text{A}_{\text{RMS}}$ at $85\,\text{V}_{\text{AC}}$ full load.
  * Current Derating: $\frac{1.604\,\text{A}}{10.0\,\text{A}} = \mathbf{16.0\%}$ (Enormous headroom).
* **Galvanic Isolation Withstand Voltage**: $4000\,\text{V}_{\text{RMS}}$ (certified reinforced safety barrier between AC Live line and secondary sensing circuitry).
* **Secondary Current Output**:
  $$I_{\text{sec}} = \frac{I_{\text{pri}}}{1000}$$
  * At $I_{\text{pri}} = 1.604\,\text{A}_{\text{RMS}}$: $I_{\text{sec}} = \mathbf{1.604\,\text{mA}_{\text{RMS}}}$ ($2.268\,\text{mA}_{\text{peak}}$).
  * At $I_{\text{pri}} = 0.310\,\text{A}_{\text{RMS}}$ ($230\,\text{V}_{\text{AC}}$ nominal): $I_{\text{sec}} = \mathbf{0.310\,\text{mA}_{\text{RMS}}}$.
* **Secondary DC Resistance ($R_{\text{sec}}$)**: $48.0\,\Omega \pm 10\%$.
* **Linearity**: $\pm 0.2\%$ across $0.1\,\text{A}$ to $10.0\,\text{A}$ primary range.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Function | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **APERTURE**| **Primary Conductor** | `AC_LINE_FUSED` | Pass-through of AC Line trace | AC mains current carrying line. |
| **Pin 1**   | **Secondary Terminal 1**| `CT_SEC_HI` | Burden Resistor `R_burden`, STM32 ADC filter | AC current signal tap. |
| **Pin 2**   | **Secondary Terminal 2**| `VREF_1V65_BIAS` | DC Midpoint Bias Divider ($+1.65\,\text{V}_{\text{DC}}$) | AC ground reference / DC offset. |

## 4. Schematic Symbol Representation
```
                    [ CT1: TALEMA AC1010 CURRENT TRANSFORMER ]
                                  1000 : 1 Ratio
                                ┌────────────────┐
     Net: AC_LINE_FUSED ───────( ) Aperture Pass ( )─────── Net: AC_LINE_FILT
                                └───────┬────────┘
                                        │
                                  ┌─────┴─────┐
                                  │   █████   │ Secondary Winding
                                  └─────┬─────┘ (1000 Turns)
                                        ├─── Pin 1: Net: CT_SEC_HI
                                        │
                                        └─── Pin 2: Net: VREF_1V65_BIAS (+1.65V DC)
```

## 5. Schematic & PCB Layout Guidelines
1. **Safety Isolation Spacing**: Maintain $\ge 6.5\,\text{mm}$ creepage clearance between the primary copper trace passing through the aperture and the secondary termination pins on the PCBA.
2. **Burden Placement**: Place the precision burden resistor `R_burden` immediately adjacent to Pins 1 and 2 of the CT to eliminate loop inductance.
