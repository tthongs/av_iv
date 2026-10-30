# Component Schematic Specification: L1 (Flat-Wire Power Inductor)

## 1. Component Metadata
* **Reference Designator**: `L1`
* **Component Type**: High-Current Flat-Wire Shielded Power Inductor
* **Manufacturer**: Würth Elektronik
* **Primary MPN**: `7443321000` (WE-HCC Series)
* **Alternate Manufacturer**: Coilcraft
* **Alternate MPN**: `SER2915L-103KL` (10.0 µH, 13.0 A sat)
* **Package / Footprint**: SMD $12.5 \times 12.5\,\text{mm}$, Height: $10.0\,\text{mm}$ (High-density flat-wire design)
* **Subsystem**: Stage 4 (Synchronous Buck-Boost Power Stage)

## 2. Electrical Ratings & Constraints
* **Nominal Inductance ($L$)**: $10.0\,\mu\text{H} \pm 20\%$ at $100\,\text{kHz}$, $0.1\,\text{V}$
* **Saturation Current ($I_{\text{sat}}$)**: $11.5\,\text{A}$ (defined at $30\%$ inductance drop)
  * Operating worst-case peak inductor current:
    $$I_{L,\text{peak}} = I_{\text{OUT}} + \frac{\Delta I_L}{2} = 3.0\,\text{A} + \frac{2.0\,\text{A}}{2} = \mathbf{4.00\,\text{A}}$$
  * Saturation Headroom Margin:
    $$\text{Margin} = \frac{I_{\text{sat}} - I_{L,\text{peak}}}{I_{\text{sat}}} \times 100\% = \frac{11.5\,\text{A} - 4.00\,\text{A}}{11.5\,\text{A}} \times 100\% = \mathbf{65.22\%}$$
  * Under a full $84.0\,\text{W}$ surge transient ($4.2\,\text{A}$ output, $I_{L,\text{peak}} = 5.6\,\text{A}$), saturation margin remains $> 51.3\%$, completely preventing magnetic saturation or runaway core heating!
* **Rated RMS Current ($I_{\text{RMS}}$)**: $8.5\,\text{A}$ (defined at $\Delta T = 40^\circ\text{C}$)
  * Operating continuous RMS current: $3.03\,\text{A}_{\text{RMS}}$
  * Current Derating: $\frac{3.03\,\text{A}}{8.5\,\text{A}} = \mathbf{35.6\%}$ (VVDN requires $\le 70\%$).
* **DC Resistance (DCR)**: $10.5\,\text{m}\Omega$ typical ($13.5\,\text{m}\Omega$ max) at $20^\circ\text{C}$
  * Conduction copper loss:
    $$P_{\text{loss,L1}} = I_{\text{RMS}}^2 \times \text{DCR}_{\text{max}} = (3.03\,\text{A})^2 \times (0.0135\,\Omega) = \mathbf{0.124\,\text{W}}$$
* **Core Loss**: High-flux MnZn composite core material exhibits ultra-low hysteresis loss ($< 65\,\text{mW}$ at $300\,\text{kHz}$, $\Delta B = 60\,\text{mT}$). Total inductor dissipation is $< 0.19\,\text{W}$.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`IN` (Switch Node 1)** | `SW1_NODE` | Source of `QA`, Drain of `QB`, `U3` SW1 pin | Heavy copper polygon ($w \ge 3.0\,\text{mm}$, 2oz Cu). |
| **2** | **`OUT` (Switch Node 2)**| `SW2_NODE` | Drain of `QC`, Source of `QD`, `U3` SW2 pin | Heavy copper polygon ($w \ge 3.0\,\text{mm}$, 2oz Cu). |

## 4. Schematic Symbol Representation
```
                    [ L1: WURTH 7443321000 10µH / 11.5A ]
                              ┌─────────────┐
        Net: SW1_NODE  ───────┤1   █████   2├─────── Net: SW2_NODE
                              │    █████    │
                              └─────────────┘
                             Flat-Wire Shielded
```

## 5. Schematic & PCB Layout Guidelines
1. **Shortest Interconnect**: Place `L1` directly between the Buck switch node (`QA`/`QB`) and the Boost switch node (`QC`/`QD`). Keep total trace length between FET pins and inductor pads $\le 8.0\,\text{mm}$.
2. **Magnetic Shielding & No-Copper Keepout**: While the WE-HCC inductor is magnetically shielded, avoid routing any sensitive signal traces (especially `LM5176_FB`, `CSP`/`CSN`, and ADC telemetry lines) on Layer 1 or Layer 2 directly underneath the inductor package.
3. **Heavy Current Carrying Solder Pads**: The SMD terminal pads are large ($3.5 \times 3.0\,\text{mm}$). Use solid copper connections (no thermal reliefs) to polygon pours on Layer 1 to minimize parasitic resistance and enhance heat conduction into the PCB substrate.
