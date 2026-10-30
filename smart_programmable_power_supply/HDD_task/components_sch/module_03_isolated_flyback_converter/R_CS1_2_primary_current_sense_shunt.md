# Component Schematic Specification: R_CS1 & R_CS2 (Primary Current Sense Shunt)

## 1. Component Metadata
* **Reference Designators**: `R_CS1`, `R_CS2` (Two identical low-inductance resistors in parallel)
* **Component Type**: Metal Strip Power Current Sense Resistors
* **Manufacturer**: Vishay Dale
* **Primary MPN**: `WSL1206R5000FEA`
* **Alternate Manufacturer**: Bourns Inc.
* **Alternate MPN**: `CRA2512-FZ-R500ELF`
* **Package / Footprint**: SMD 1206 ($3.2 \times 1.6\,\text{mm}$)
* **Subsystem**: Stage 3 (Isolated Flyback Subsystem)

## 2. Electrical Ratings & Constraints
* **Individual Resistance**: $0.50\,\Omega \pm 1.0\%$ each ($1.0\,\text{W}$ rated power)
* **Equivalent Parallel Resistance ($R_{\text{CS}}$)**:
  $$R_{\text{CS}} = \frac{0.50\,\Omega}{2} = \mathbf{0.250\,\Omega \pm 1.0\%}$$
* **Maximum Peak Primary Current**: $I_{\text{pk}} = 3.03\,\text{A}_{\text{peak}}$
* **Peak Sense Voltage**:
  $$V_{\text{CS,peak}} = I_{\text{pk}} \times R_{\text{CS}} = (3.03\,\text{A}) \times (0.250\,\Omega) = \mathbf{0.758\,\text{V}_{\text{DC}}}$$
  Safely operates below the controller's internal $1.00\,\text{V}$ hard clamp limit ($24.2\%$ headroom).
* **Power Dissipation Budget**:
  $$P_{\text{CS}} = I_{\text{RMS,pri}}^2 \times R_{\text{CS}} = (1.17\,\text{A})^2 \times (0.250\,\Omega) = 1.369 \times 0.25 = \mathbf{0.342\,\text{W}}$$
  Dissipation per resistor is $0.171\,\text{W}$ ($17.1\%$ of $1.0\,\text{W}$ package rating, zero thermal drift).

## 3. Schematic Pin Connections & Net Mapping
| Ref Des | Pin 1 Net Name | Connected To | Pin 2 Net Name | Connected To | Role |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **`R_CS1`** | `FLY_SOURCE` | CoolMOS `Q1` Source | `PGND_HOT` | Primary hot power ground plane | Primary peak current sensing. |
| **`R_CS2`** | `FLY_SOURCE` | CoolMOS `Q1` Source | `PGND_HOT` | Primary hot power ground plane | Paralleled for lower inductance and rating. |

## 4. Schematic Symbol Representation
```
             Net: FLY_SOURCE (From Q1 Source)
                    │
         ┌──────────┴──────────┐
       ┌─┴─┐                 ┌─┴─┐
       │   │ R_CS1           │   │ R_CS2
       │   │ 0.50Ω / 1W      │   │ 0.50Ω / 1W
       └─┬─┘ (Net = 0.25Ω)   └─┬─┘
         └──────────┬──────────┘
                    │
             Net: PGND_HOT (Primary Hot Ground)
```

## 5. Schematic & PCB Layout Guidelines
1. **Kelvin Sense Connection**: Route a dedicated differential pair from the pads of `R_CS` back to controller Pin 3 (`CS`) and Pin 4 (`GND`). Do not mix high-current primary switching current with the small-signal sensing trace.
