# Component Schematic Specification: Q1 (Primary High-Voltage Power MOSFET)

## 1. Component Metadata
* **Reference Designator**: `Q1`
* **Component Type**: Superjunction N-Channel Power MOSFET
* **Manufacturer**: Infineon Technologies AG
* **Primary MPN**: `IPB80R290P7`
* **Alternate Manufacturer**: STMicroelectronics
* **Alternate MPN**: `STP10NK80Z`
* **Package / Footprint**: D2PAK / TO-263-3 (SMD Surface Mount with Heavy Drain Thermal Tab)
* **Subsystem**: Stage 3 (Isolated Flyback Subsystem)

## 2. Electrical Ratings & Constraints
* **Drain-Source Breakdown Voltage ($V_{\text{DSS}}$)**: $800.0\,\text{V}_{\text{DC}}$
  * Maximum Drain-Source Operating Voltage:
    $$V_{\text{DS,peak}} = V_{\text{bulk,max}} + V_R + V_{\text{spike}} = 374.8\,\text{V} + 144.0\,\text{V} + 80.2\,\text{V} = \mathbf{599.0\,\text{V}_{\text{peak}}}$$
  * Voltage Derating: $\frac{599.0\,\text{V}}{800.0\,\text{V}} = \mathbf{74.88\%} \le 75.0\%$ (Strictly complies with VVDN guideline).
* **Continuous Drain Current ($I_D$)**: $17.0\,\text{A}$ @ $25^\circ\text{C}$ / $11.0\,\text{A}$ @ $100^\circ\text{C}$
  * Maximum Primary Peak Current: $I_{\text{pk}} = 3.03\,\text{A}_{\text{peak}}$ ($I_{\text{RMS}} = 1.17\,\text{A}_{\text{RMS}}$)
  * Current Derating: $\frac{1.17\,\text{A}}{11.0\,\text{A}} = \mathbf{10.6\%}$ (Immense safety margin).
* **Static Drain-Source On-Resistance ($R_{\text{DS(on)}}$)**: $0.290\,\Omega$ max @ $25^\circ\text{C}$ ($0.435\,\Omega$ @ $100^\circ\text{C}$)
* **Total Gate Charge ($Q_g$)**: $24.0\,\text{nC}$ (Fast switching with low gate drive loss)
* **Power Dissipation Budget**:
  * Conduction Loss: $P_{\text{cond}} = (1.17\,\text{A})^2 \times (0.435\,\Omega) = \mathbf{0.59\,\text{W}}$
  * Capacitive Switching Loss: $P_{\text{sw}} \approx \frac{1}{2} C_{\text{oss}} V_{\text{DS}}^2 f_{\text{sw}} \approx \mathbf{0.26\,\text{W}}$
  * Total Dissipation: $P_{\text{loss,Q1}} = 0.59 + 0.26 = \mathbf{0.85\,\text{W}}$

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **Gate (G)** | `FLY_GATE_PIN` | Series gate damping resistor $R_g = 10.0\,\Omega \pm 1\%$ (`FLY_GATE`) | Short, direct trace ($< 10.0\,\text{mm}$). |
| **2 / Tab** | **Drain (D)** | `FLY_DRAIN` | Transformer `TX1` Primary Pin 2, Snubber Diode `D_snub` Cathode | Large copper polygon pour on Layer 1 ($400\,\text{mm}^2$). |
| **3** | **Source (S)** | `FLY_SOURCE` | Primary current sense shunt network `R_CS` (Pins 1) | Kelvin sense tap to controller `CS` pin. |

## 4. Schematic Symbol Representation
```
                     Net: FLY_DRAIN (To TX1 Pin 2 & Snubber)
                              │
                           ┌──┴──┐
                           │  D  │   Q1: Infineon IPB80R290P7
  Net: FLY_GATE ──[ 10Ω ]──┤G   S│   800V, 17A, 0.29Ω (D2PAK)
                           └──┬──┘
                              │
                     Net: FLY_SOURCE ────> To Current Shunt R_CS
```

## 5. Schematic & PCB Layout Guidelines
1. **Thermal Copper Pour**: Solder the D2PAK drain tab to a dedicated $400\,\text{mm}^2$ copper polygon on Layer 1 with an array of $4 \times 4$ thermal vias ($0.3\,\text{mm}$ drill) conducting heat to the Layer 4 bottom copper pour ($T_j \le 100.4^\circ\text{C}$ @ $50^\circ\text{C}$ ambient).
2. **Gate Ringing Suppression**: Place the $10\,\Omega$ gate resistor and anti-parallel Schottky diode (BAT54) directly adjacent to Pin 1 to damp gate parasitic ringing.
