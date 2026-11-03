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
* **Current Transformation Turns Ratio (N_pri:N_sec)**: 1 : 1000 (1000 secondary turns).
* **Rated Primary Continuous Current (I_pri,rated)**: 10.0 A_RMS (50/60 Hz).
 * Maximum operating AC input current: 1.604 A_RMS at 85 V_AC full load.
 * Current Derating: (1.604 A / 10.0 A) = 16.0% (Enormous headroom).
* **Galvanic Isolation Withstand Voltage**: 4000 V_RMS (certified reinforced safety barrier between AC Live line and secondary sensing circuitry).
* **Secondary Current Output**:
 I_sec = (I_pri / 1000)
 * At I_pri = 1.604 A_RMS: I_sec = mathbf{1.604 mA_RMS} (2.268 mA_peak).
 * At I_pri = 0.310 A_RMS (230 V_AC nominal): I_sec = mathbf{0.310 mA_RMS}.
* **Secondary DC Resistance (R_sec)**: 48.0 Ω ± 10%.
* **Linearity**: ± 0.2% across 0.1 A to 10.0 A primary range.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Function | Schematic Net Name | Connected To | Description & Connection |
| :---: | :---: | :--- | :--- | :--- |
| **APERTURE**| **Primary Conductor** | `AC_LINE_FUSED` | Pass-through of AC Line trace | AC mains current carrying line. |
| **Pin 1** | **Secondary Terminal 1**| `CT_SEC_HI` | Burden Resistor `R_burden`, STM32 ADC filter | AC current signal tap. |
| **Pin 2** | **Secondary Terminal 2**| `VREF_1V65_BIAS` | DC Midpoint Bias Divider (+1.65 V_DC) | AC ground reference / DC offset. |

## 4. Schematic Symbol Representation
```
 [ CT1: TALEMA AC1010 CURRENT TRANSFORMER ]
 1000 : 1 Ratio
 ┌────────────────┐
 Net: AC_LINE_FUSED ───────() Aperture Pass ()─────── Net: AC_LINE_FILT
 └───────┬────────┘
 │
 ┌─────┴─────┐
 │ █████ │ Secondary Winding
 └─────┬─────┘ (1000 Turns)
 ├─── Pin 1: Net: CT_SEC_HI
 │
 └─── Pin 2: Net: VREF_1V65_BIAS (+1.65V DC)
```

## 5. Schematic & PCB Layout Guidelines
1. **Safety Isolation Spacing**: Maintain ≥ 6.5 mm creepage clearance between the primary copper trace passing through the aperture and the secondary termination pins on the PCBA.
2. **Burden Placement**: Place the precision burden resistor `R_burden` immediately adjacent to Pins 1 and 2 of the CT to eliminate loop inductance.
