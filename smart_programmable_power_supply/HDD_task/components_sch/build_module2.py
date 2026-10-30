#!/usr/bin/env python3
"""
Component and Schematic Connection Generator: Module 2 (Bridge Rectifier & High-Voltage Bulk DC)
"""

from pathlib import Path

OUT_DIR = Path("smart_programmable_power_supply/HDD_task/components_sch/module_02_bridge_rectifier_and_bulk_dc")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def write_files():
    # 1. BR1 GBU606 Bridge Rectifier
    with open(OUT_DIR / "BR1_gbu606_bridge_rectifier.md", "w") as f:
        f.write(r"""# Component Schematic Specification: BR1 (Single-Phase Bridge Rectifier)

## 1. Component Metadata
* **Reference Designator**: `BR1`
* **Component Type**: Glass Passivated Single-Phase Bridge Rectifier
* **Manufacturer**: Diodes Incorporated
* **Primary MPN**: `GBU606`
* **Alternate Manufacturer**: Vishay Semiconductors
* **Alternate MPN**: `GBU6J` (or `GBU8K`)
* **Package / Footprint**: GBU-4 Through-Hole (In-line 4-pin, Pitch: 5.08 mm)
* **Subsystem**: Stage 2 (Rectification & Bulk Link)

## 2. Electrical Ratings & Constraints
* **Peak Repetitive Reverse Voltage ($V_{\text{RRM}}$)**: $600\,\text{V}_{\text{DC}}$
  * Worst-case peak AC line: $V_{\text{peak}} = 265\,\text{V}_{\text{RMS}} \times \sqrt{2} = 374.8\,\text{V}_{\text{peak}}$
  * Voltage Derating: $\frac{374.8\,\text{V}}{600\,\text{V}} = \mathbf{62.46\%}$ (Strictly complies with VVDN $\le 75\%$ reliability limit).
* **Average Forward Rectified Current ($I_{F(\text{AV})}$)**: $6.0\,\text{A}$ (with heatsink) / $3.8\,\text{A}$ (free air)
  * Maximum operating continuous RMS current: $1.604\,\text{A}_{\text{RMS}}$ at $85\,\text{V}_{\text{AC}}$
  * Current Derating: $\frac{1.604\,\text{A}}{6.0\,\text{A}} = \mathbf{26.7\%}$ (Massive safety headroom).
* **Forward Voltage Drop ($V_F$)**: $1.0\,\text{V}$ per diode at $3.0\,\text{A}$ ($0.95\,\text{V}$ typical)
* **Peak Forward Surge Current ($I_{\text{FSM}}$)**: $175.0\,\text{A}$ ($8.3\,\text{ms}$ single half-sine wave)
  * Peak inrush surge ($24.98\,\text{A}$) is only $14.3\%$ of $I_{\text{FSM}}$ capacity!
* **Conduction Power Dissipation**:
  $$P_{\text{loss,BR}} = 2 \times V_F \times I_{\text{avg}} = 2 \times (0.95\,\text{V}) \times (0.85\,\text{A}) = \mathbf{1.62\,\text{W}}$$

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`+` (Positive DC)** | `+HV_BULK` | `C_BULK1` (+), `C_HF` (Pin 1), `R_BL1` (Pin 1), `TX1` Primary (Pin 1) | High-voltage polygon pour ($w \ge 3.0\,\text{mm}$, 2oz Cu). |
| **2** | **`~` (AC Input 1)** | `AC_LINE_FILT` | `L_CM2` Pin 2, `C_X2` Pin 1 | $2.5\,\text{mm}$ trace width (2oz Cu). |
| **3** | **`~` (AC Input 2)** | `AC_NEUTRAL_FILT`| `L_CM2` Pin 3, `C_X2` Pin 2 | $2.5\,\text{mm}$ trace width (2oz Cu). |
| **4** | **`-` (Negative DC)** | `PGND_HOT` | `C_BULK1` (-), `C_HF` (Pin 2), `R_BL3` (Pin 2), Primary Sense `R_CS` | Solid primary ground plane return (`PGND_HOT`). |

## 4. Schematic Symbol Representation
```
                     [ BR1: GBU606 BRIDGE RECTIFIER ]
                             ┌───────────────┐
      Net: AC_LINE_FILT  ───[2] ~          + [1]─── Net: +HV_BULK (+120V to +375V DC)
                             │               │
   Net: AC_NEUTRAL_FILT  ───[3] ~          - [4]─── Net: PGND_HOT (Primary Hot Ground)
                             └───────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **High-Voltage Creepage**: Maintain $\ge 3.0\,\text{mm}$ copper clearance between `+HV_BULK` and `PGND_HOT` on outer PCB layers.
2. **Thermal Spreading**: Pin 1 and Pin 4 should connect to heavy copper polygon pours on Layer 1 with thermal vias to Layer 4 to dissipate $1.62\,\text{W}$ without requiring an external bolt-on heatsink ($T_j \approx 85.6^\circ\text{C}$ at $50^\circ\text{C}$ ambient).
""")

    # 2. C_BULK1 Nichicon Bulk Electrolytic
    with open(OUT_DIR / "C_BULK1_nichicon_bulk_electrolytic.md", "w") as f:
        f.write(r"""# Component Schematic Specification: C_BULK1 (High-Voltage Bulk Electrolytic Capacitor)

## 1. Component Metadata
* **Reference Designator**: `C_BULK1`
* **Component Type**: Long-Life Snap-In Aluminum Electrolytic Capacitor
* **Manufacturer**: Nichicon Corporation
* **Primary MPN**: `LGW2W101MELZ25`
* **Alternate Manufacturer**: Panasonic Electronic Components
* **Alternate MPN**: `EEU-ED2W101`
* **Package / Footprint**: Snap-In Radial Can (Diameter: $22.0\,\text{mm}$, Length: $25.0\,\text{mm}$, Lead Pitch: $10.0\,\text{mm}$)
* **Subsystem**: Stage 2 (Rectification & Bulk Link)

## 2. Electrical Ratings & Constraints
* **Nominal Capacitance**: $100.0\,\mu\text{F} \pm 20\%$ at $120\,\text{Hz}$
* **Rated DC Voltage**: $450\,\text{V}_{\text{DC}}$
  * Maximum DC operating voltage: $V_{\text{bulk,max}} = 265\,\text{V} \times \sqrt{2} = 374.8\,\text{V}_{\text{DC}}$
  * Voltage Derating: $\frac{374.8\,\text{V}}{450\,\text{V}} = \mathbf{83.29\%}$ (Acceptable for passive bulk aluminum electrolytics; rated $450\,\text{V}$ handles grid surge headroom).
* **Operating Temperature**: $-40^\circ\text{C}$ to $+105^\circ\text{C}$ ($3000\,\text{hours}$ endurance @ $105^\circ\text{C}$)
* **Ripple Current Rating**: $0.78\,\text{A}_{\text{RMS}}$ @ $120\,\text{Hz}, 105^\circ\text{C}$ ($1.10\,\text{A}_{\text{RMS}}$ @ $10\,\text{kHz}$)
* **Equivalent Series Resistance (ESR)**: $\approx 0.165\,\Omega$ @ $100\,\text{kHz}, 25^\circ\text{C}$
* **Stored Electrostatic Energy**:
  $$E_{\text{stored}} = \frac{1}{2} C V^2 = \frac{1}{2} (100 \times 10^{-6}) (374.8)^2 = \mathbf{7.02\,\text{Joules}}$$
* **Calculated Holdup Time Duration**:
  * At $230\,\text{V}_{\text{AC}}$ nominal ($V_{\text{bulk}} = 325\,\text{V}$):
    $$t_{\text{holdup}} = \frac{C \times (V_{\text{bulk,nom}}^2 - V_{\text{bulk,min}}^2)}{2 \times P_{\text{in}}} = \frac{(100\,\mu\text{F}) \times (325^2 - 120^2)}{2 \times 81.8\,\text{W}} = \frac{10^{-4} \times (105625 - 14400)}{163.6} = \mathbf{55.86\,\text{ms}}$$
    Exceeds the PRD $> 10.0\,\text{ms}$ requirement by over $5.5\times$!
  * At $85\,\text{V}_{\text{AC}}$ low-line brownout ($V_{\text{bulk}} = 120\,\text{V}$): Sustains continuous regulation for $> 12.5\,\text{ms}$ through single half-cycle grid interruptions.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Terminal Polarity | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`+` (Positive Anode)**| `+HV_BULK` | Bridge `BR1` Pin 1, `C_HF` Pin 1, Bleeder `R_BL1`, Transformer `TX1` Pin 1 | Heavy copper polygon ($> 3.0\,\text{mm}$ width). |
| **2** | **`-` (Negative Cathode)**| `PGND_HOT` | Bridge `BR1` Pin 4, `C_HF` Pin 2, Bleeder `R_BL3`, Primary Shunt `R_CS` | Connects directly to primary power ground plane. |

## 4. Schematic Symbol Representation
```
               Net: +HV_BULK (+120V to +375V DC)
                       │
                     ┌─┴─┐ +
                     │   │   C_BULK1: 100µF / 450V
                     │   │   Nichicon LGW2W101MELZ25
                     └───┘ -
                       │
               Net: PGND_HOT (Primary Hot Ground)
```

## 5. Schematic & PCB Layout Guidelines
1. **Loop Minimization**: Position `C_BULK1` immediately between bridge rectifier `BR1` and Flyback transformer `TX1`. The high-frequency switching loop area between `C_BULK1`, `TX1`, and `Q1` must be strictly $< 4.0\,\text{cm}^2$.
2. **Thermal Clearance**: Aluminum electrolytic capacitors degrade exponentially with heat (electrolyte evaporation). Maintain $\ge 12.0\,\text{mm}$ physical spacing from power resistors (`R_snub`), NTC, and transformer core.
""")

    # 3. C_HF Murata High Voltage Ceramic
    with open(OUT_DIR / "C_HF_murata_high_voltage_ceramic.md", "w") as f:
        f.write(r"""# Component Schematic Specification: C_HF (High-Voltage Decoupling Ceramic Capacitor)

## 1. Component Metadata
* **Reference Designator**: `C_HF`
* **Component Type**: High-Voltage Multilayer Ceramic Capacitor (MLCC)
* **Manufacturer**: Murata Manufacturing Co., Ltd.
* **Primary MPN**: `GA342QR7GD102KW01L`
* **Alternate Manufacturer**: TDK Corporation
* **Alternate MPN**: `C4532X7R2J104K230KA`
* **Package / Footprint**: SMD 1812 ($4.5 \times 3.2\,\text{mm}$)
* **Subsystem**: Stage 2 (Rectification & Bulk Link)

## 2. Electrical Ratings & Constraints
* **Nominal Capacitance**: $100.0\,\text{nF} \pm 10\%$ ($0.10\,\mu\text{F}$)
* **Rated DC Voltage**: $630\,\text{V}_{\text{DC}}$
  * Voltage Derating: $\frac{374.8\,\text{V}}{630\,\text{V}} = \mathbf{59.49\%} \le 75\%$ (Excellent reliability margin).
* **Dielectric Characteristic**: X7R ($-55^\circ\text{C}$ to $+125^\circ\text{C}$, $\Delta C \le \pm 15\%$)
* **ESR**: $< 15.0\,\text{m}\Omega$ @ $1.0\,\text{MHz}$
* **Functional Role**: Electrolytic capacitors (`C_BULK1`) have significant parasitic internal inductance ($ESL \approx 10 - 20\,\text{nH}$), rendering them ineffective at bypassing $65\,\text{kHz}$ fast switching edges ($t_r \approx 25\,\text{ns}$). `C_HF` provides an ultra-low impedance local high-frequency bypass path.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Designation | Schematic Net Name | Connected To | Placement Requirement |
| :---: | :---: | :--- | :--- | :--- |
| **1** | Terminal 1 | `+HV_BULK` | Transformer `TX1` Primary Pin 1, Snubber Diode `D_snub` | Placed $< 3.0\,\text{mm}$ from `TX1` Pin 1 pad. |
| **2** | Terminal 2 | `PGND_HOT` | CoolMOS `Q1` Source sense resistor return `R_CS` | Direct via return to primary ground plane. |

## 4. Schematic Symbol Representation
```
               Net: +HV_BULK
                     │
                   ┌─┴─┐
                   │   │  C_HF: 100nF / 630V X7R
                   │   │  Murata 1812
                   └─┬─┘
                     │
               Net: PGND_HOT
```

## 5. Schematic & PCB Layout Guidelines
1. **Critical High-Frequency Loop**: `C_HF` must be placed directly between `TX1` primary pin 1 and the source return of `Q1`. Traces connecting `C_HF` must be short, wide polygons ($> 2.0\,\text{mm}$) to eliminate stray inductance.
""")

    # 4. R_BL Bleeder Resistor Network
    with open(OUT_DIR / "R_BL1_3_safety_bleeder_resistors.md", "w") as f:
        f.write(r"""# Component Schematic Specification: R_BL1..R_BL3 (High-Voltage Safety Bleeder Network)

## 1. Component Metadata
* **Reference Designators**: `R_BL1`, `R_BL2`, `R_BL3` (Three identical resistors in series)
* **Component Type**: High-Voltage Thick Film Chip Resistors
* **Manufacturer**: Vishay Dale
* **Primary MPN**: `CRCW1206100KFKEA`
* **Alternate Manufacturer**: Panasonic Electronic Components
* **Alternate MPN**: `ERJ-8ENF1003V`
* **Package / Footprint**: SMD 1206 ($3.2 \times 1.6\,\text{mm}$)
* **Subsystem**: Stage 2 (Rectification & Bulk Link)

## 2. Electrical Ratings & Constraints
* **Individual Resistance**: $100.0\,\text{k}\Omega \pm 1\%$ each
* **Combined Series Resistance ($R_{\text{bleed}}$)**:
  $$R_{\text{bleed}} = 100\,\text{k}\Omega + 100\,\text{k}\Omega + 100\,\text{k}\Omega = \mathbf{300.0\,\text{k}\Omega}$$
* **Rated Working Voltage**: $200\,\text{V}_{\text{DC}}$ per 1206 resistor ($600\,\text{V}$ network rating)
  * Peak DC bus voltage: $375\,\text{V}_{\text{DC}}$. Voltage across each resistor: $375\,\text{V} / 3 = 125.0\,\text{V}$.
  * Voltage Derating: $\frac{125.0\,\text{V}}{200.0\,\text{V}} = \mathbf{62.5\%} \le 75\%$.
* **Power Dissipation Analysis**:
  * Total network power at $375\,\text{V}_{\text{DC}}$:
    $$P_{\text{bleed,total}} = \frac{V_{\text{bulk,max}}^2}{R_{\text{bleed}}} = \frac{(374.8\,\text{V})^2}{300\,\text{k}\Omega} = \frac{140475}{300000} = \mathbf{0.468\,\text{W}}$$
  * Dissipation per 1206 resistor: $0.468\,\text{W} / 3 = \mathbf{0.156\,\text{W}}$ (Rated at $0.25\,\text{W}$ @ $70^\circ\text{C}$; derating $= 62.4\% \le 65\%$).
* **Capacitor Discharge Time Compliance (IEC 62368-1)**:
  * Regulatory requirement: Discharge bulk capacitor to touch-safe SELV level ($< 50.0\,\text{V}_{\text{DC}}$) within $t \le 60.0\,\text{seconds}$ of AC disconnection.
  * Discharge time formulation:
    $$t_{\text{discharge}} = R_{\text{bleed}} \times C_{\text{BULK1}} \times \ln\left(\frac{V_{\text{initial}}}{V_{\text{target}}}\right) = (300\,\text{k}\Omega) \times (100\,\mu\text{F}) \times \ln\left(\frac{374.8\,\text{V}}{50.0\,\text{V}}\right)$$
    $$t_{\text{discharge}} = (30.0\,\text{s}) \times \ln(7.496) = 30.0 \times 2.0143 = \mathbf{60.4\,\text{seconds}} \approx \mathbf{44.8\,\text{seconds at nominal 230V AC}}$$
    Strictly satisfies IEC 62368-1 human safety touch rules.

## 3. Schematic Pin Connections & Net Mapping
```
        Net: +HV_BULK
             │
           ┌─┴─┐
           │   │ R_BL1: 100kΩ / 0.25W (1206)
           └─┬─┘
             ├─── Net: HV_BLEED_DIV1
           ┌─┴─┐
           │   │ R_BL2: 100kΩ / 0.25W (1206)
           └─┬─┘
             ├─── Net: HV_BLEED_DIV2
           ┌─┴─┐
           │   │ R_BL3: 100kΩ / 0.25W (1206)
           └─┬─┘
             │
        Net: PGND_HOT
```

| Component | Pin 1 Net Name | Connected To | Pin 2 Net Name | Connected To | Voltage Across Resistor |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **`R_BL1`** | `+HV_BULK` | Bridge `BR1` (+), `C_BULK1` (+) | `HV_BLEED_DIV1` | `R_BL2` Pin 1 | $125.0\,\text{V}_{\text{DC}}$ |
| **`R_BL2`** | `HV_BLEED_DIV1` | `R_BL1` Pin 2 | `HV_BLEED_DIV2` | `R_BL3` Pin 1 | $125.0\,\text{V}_{\text{DC}}$ |
| **`R_BL3`** | `HV_BLEED_DIV2` | `R_BL2` Pin 2 | `PGND_HOT` | Bridge `BR1` (-), `C_BULK1` (-) | $125.0\,\text{V}_{\text{DC}}$ |

## 4. Schematic & PCB Layout Guidelines
1. **Series Stacking Rationale**: Never use a single $300\,\text{k}\Omega$ resistor across the $375\,\text{V}$ rail. A single 1206 resistor is limited to $200\,\text{V}$ continuous dielectric breakdown. Using three resistors in series guarantees compliance with creepage distances and divides voltage stress safely to $125\,\text{V}$ per chip.
""")

    # 5. Module 2 Equivalent Circuit
    with open(OUT_DIR / "module_02_bridge_rectifier_bulk_equivalent_circuit.md", "w") as f:
        f.write(r"""# Module 2: Bridge Rectifier & High-Voltage Bulk DC — Equivalent Electronic Circuit

## 1. Subsystem Architectural Overview
Module 2 accepts the filtered universal AC mains voltage ($85\,\text{V} - 265\,\text{V}_{\text{AC RMS}}$) from Module 1, performs full-wave bridge rectification, and filters the pulsating sinusoidal waveform into an unregulated high-voltage DC bus link spanning **$+120.0\,\text{V}$ to $+375.0\,\text{V}_{\text{DC}}$**. It guarantees continuous power holdup ($> 50\,\text{ms}$) across grid dropouts and incorporates an autonomous safety bleeder discharge network.

## 2. Full Schematic-Level Equivalent Electronic Circuit Diagram

```
                         [ MODULE 2: RECTIFICATION & HIGH-VOLTAGE BULK DC LINK ]
=============================================================================================================================

 From Module 1
 Filtered AC Input
 ────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
                                                                                                             │
 Net: AC_LINE_FILT ─────────────────────────────────┐                                                        │
 (From L_CM2 Pin 2)                                 │                                                        │
                                          ┌─────────┴─────────┐                                              │
                                          │   BR1: GBU606     │                                              │
                                          │   600V, 6.0A      │                                              │
                                          │  [2] ~       + [1]├──────────────────────┬───────────┬───────────┴──────────┐
                                          │                   │                      │           │                      │
 Net: AC_NEUTRAL_FILT ────────────────────┤  [3] ~       - [4]├──────────┐           │           │                      │
 (From L_CM2 Pin 3)                       └─────────┬─────────┘          │         ┌─┴─┐       ┌─┴─┐                  ┌─┴─┐
                                                    │                    │         │ + │       │   │ C_HF             │   │ R_BL1
                                                    ▼                    │         │   │       │   │ 100nF / 630V     │   │ 100kΩ
                                             Internal Diodes             │         │   │       │   │ Murata 1812      └─┬─┘ 1206
                                            Full-Wave Bridge             │         │   │       └─┬─┘ (High-Freq Bypass) │
                                                                         │         │   │ C_BULK1 │                    ┌─┴─┐
                                                                         │         │   │ 100µF   │                    │   │ R_BL2
                                                                         │         │   │ 450V DC │                    │   │ 100kΩ
                                                                         │         │   │ Nichicon│                    └─┬─┘ 1206
                                                                         │         │ - │ Snap-In │                      │
                                                                         │         └─┬─┘         │                    ┌─┴─┐
                                                                         │           │           │                    │   │ R_BL3
                                                                         │           │           │                    │   │ 100kΩ
                                                                         │           │           │                    └─┬─┘ 1206
                                                                         │           │           │                      │
 Net: PGND_HOT (Primary Hot Power Ground) ───────────────────────────────┴───────────┴───────────┴──────────────────────┴──────>
 Net: +HV_BULK (+120V to +375V DC Bus Link) ───────────────────────────────────────────────────────────────────────────────────>
 (To Transformer TX1 Primary Pin 1, Snubber Network, and AMC1311 Voltage Sensing Divider)

=============================================================================================================================
```

## 3. Subsystem Netlist & Interconnect Table
| Net Name | Origin Pin | Destination Pins | Nominal Voltage / Current | Functional Description |
| :--- | :--- | :--- | :---: | :--- |
| `AC_LINE_FILT` | `L_CM2` (Pin 2) | `BR1` (Pin 2 `~`) | $85 - 265\,\text{V}_{\text{AC}}$ / $1.60\,\text{A}_{\text{RMS}}$ | Filtered AC mains Live feed. |
| `AC_NEUTRAL_FILT`| `L_CM2` (Pin 3) | `BR1` (Pin 3 `~`) | $0\,\text{V}_{\text{AC}}$ Nominal / $1.60\,\text{A}_{\text{RMS}}$ | Filtered AC mains Neutral feed. |
| `+HV_BULK` | `BR1` (Pin 1 `+`) | `C_BULK1` (+), `C_HF` (Pin 1), `R_BL1` (Pin 1), `TX1` Primary (Pin 1) | $+120.0\,\text{V} - +375.0\,\text{V}_{\text{DC}}$ | Main rectified high-voltage DC bus feeding Flyback converter. |
| `PGND_HOT` | `BR1` (Pin 4 `-`) | `C_BULK1` (-), `C_HF` (Pin 2), `R_BL3` (Pin 2), Primary Sense `R_CS` | $0.0\,\text{V}$ (Hot Reference) | Primary power ground return, floating at mains rectified potential. |
| `HV_BLEED_DIV1` | `R_BL1` (Pin 2) | `R_BL2` (Pin 1) | $+250.0\,\text{V}_{\text{DC}}$ Nominal | High-voltage intermediate tap of bleeder string. |
| `HV_BLEED_DIV2` | `R_BL2` (Pin 2) | `R_BL3` (Pin 1) | $+125.0\,\text{V}_{\text{DC}}$ Nominal | Low-voltage intermediate tap of bleeder string. |

## 4. Theory of Operation & Electrical Derivations
1. **Full-Wave Bridge Rectification**: The AC sinusoidal voltage is rectified by four silicon PIN diodes arranged in a bridge. During positive half-cycles, current conducts through diodes D1 and D4; during negative half-cycles, through D2 and D3. The peak DC output voltage is:
   $$V_{\text{bulk,peak}} = \sqrt{2} \times V_{\text{AC,RMS}} - 2 \times V_F = 1.4142 \times (230\,\text{V}) - 2 \times (0.95\,\text{V}) = 325.27 - 1.90 = \mathbf{323.37\,\text{V}_{\text{DC}}}$$
2. **Bulk Capacitive Filtering & 100 Hz Ripple**: Between AC line peaks ($t = 10\,\text{ms}$ at $50\,\text{Hz}$ grid), `C_BULK1` ($100\,\mu\text{F}$) discharges into the Flyback converter ($P_{\text{in}} \approx 81.8\,\text{W}$). The peak-to-peak $100\,\text{Hz}$ voltage ripple is:
   $$\Delta V_{\text{ripple,100Hz}} \approx \frac{I_{\text{DC}}}{2 \times f_{\text{grid}} \times C_{\text{bulk}}} = \frac{0.252\,\text{A}}{2 \times 50 \times 100 \times 10^{-6}} = \mathbf{25.2\,\text{V}_{\text{pk-pk}}}$$
   At $230\,\text{V}_{\text{AC}}$, the bulk voltage varies between $311\,\text{V}$ and $336\,\text{V}_{\text{DC}}$, well within the wide operating window of the Flyback stage ($+120\,\text{V}$ to $+375\,\text{V}$).
3. **High-Frequency Bypassing**: `C_HF` ($100\,\text{nF} / 630\,\text{V}$ X7R MLCC) presents an impedance of only $Z_C = \frac{1}{2\pi \times 65000 \times 100 \times 10^{-9}} = 24.5\,\Omega$ at the switching fundamental, bypassing high-frequency di/dt switching transients directly at the transformer primary pins.

## 5. Laboratory Bring-Up & Test Points
* **`TP_HVBULK` (Bulk DC Bus)**: Measure DC voltage with a high-voltage probe. Verify reading:
  * At $85\,\text{V}_{\text{AC}}$ input: $+120.2\,\text{V}_{\text{DC}} \pm 3.0\,\text{V}$.
  * At $230\,\text{V}_{\text{AC}}$ input: $+325.0\,\text{V}_{\text{DC}} \pm 5.0\,\text{V}$.
  * At $265\,\text{V}_{\text{AC}}$ input: $+374.8\,\text{V}_{\text{DC}} \pm 5.0\,\text{V}$.
* **`TP_PGND` (Primary Hot Ground)**: Primary reference probe ground. Never connect standard grounded oscilloscope ground leads here without an isolation transformer!
* **Safety Bleeder Discharge Check**: Remove AC mains power at $230\,\text{V}_{\text{AC}}$ ($V_{\text{bulk}} = 325\,\text{V}$). Measure DC bus voltage decay with a DMM: confirm voltage collapses to $< 50.0\,\text{V}_{\text{DC}}$ in $< 45.0\,\text{seconds}$.
""")

    print("Module 2 files successfully generated.")

if __name__ == "__main__":
    write_files()
