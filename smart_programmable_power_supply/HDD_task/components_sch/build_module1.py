#!/usr/bin/env python3
"""
Component and Schematic Connection Generator: Module 1 (Mains AC Input & EMI Filter)
"""

import os
from pathlib import Path

OUT_DIR = Path("smart_programmable_power_supply/HDD_task/components_sch/module_01_mains_input_and_emi_filter")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def write_files():
    # 1. J1 IEC C14 Inlet
    with open(OUT_DIR / "J1_iec_c14_inlet.md", "w") as f:
        f.write("""# Component Schematic Specification: J1 (AC Mains Inlet Socket)

## 1. Component Metadata
* **Reference Designator**: `J1`
* **Component Type**: AC Chassis Appliance Inlet
* **Manufacturer**: Schurter Inc.
* **Primary MPN**: `6100.3300`
* **Alternate Manufacturer**: TE Connectivity / Corcom
* **Alternate MPN**: `1-6609987-1`
* **Package / Footprint**: IEC 60320-1 C14 Panel Mount with Solder / Faston Terminals
* **Subsystem**: Stage 1 (Mains AC Input & Protection)

## 2. Electrical Ratings & Constraints
* **Rated Voltage**: $250\,\text{V}_{\text{AC RMS}}$ (Operating span: $85\,\text{V} - 265\,\text{V}_{\text{AC}}$)
* **Rated Current**: $10.0\,\text{A}_{\text{RMS}}$ (Max system operating current: $1.604\,\text{A}_{\text{RMS}}$ at $85\,\text{V}_{\text{AC}}$)
* **Dielectric Withstand**: $> 2000\,\text{V}_{\text{AC}}$ Line-to-Earth (1 min)
* **Insulation Resistance**: $> 100\,\text{M}\Omega$ @ $500\,\text{V}_{\text{DC}}$
* **Flammability Rating**: UL 94V-0 thermoplastic housing

## 3. Schematic Pin Connections & Net Mapping
| Pin / Terminal # | Terminal Name | Schematic Net Name | Connected To | Wire / Trace Requirement |
| :---: | :--- | :--- | :--- | :--- |
| **L** | **Live** | `AC_LINE_IN` | Fuse `F1` (Input terminal of fuse clip `FC1`) | Direct heavy-gauge chassis wire ($18\,\text{AWG}$) or $\ge 2.5\,\text{mm}$ PCB trace (2oz Cu). |
| **N** | **Neutral** | `AC_NEUTRAL_IN` | Inrush Thermistor `NTC1` (Input terminal) | Direct heavy-gauge chassis wire ($18\,\text{AWG}$) or $\ge 2.5\,\text{mm}$ PCB trace (2oz Cu). |
| **E** | **Earth** | `EARTH_GND` | Chassis metal enclosure stud and Class Y1 ground return (`C_Y1`, `C_Y2`) | Direct chassis mechanical screw bond with star lock washer. Safety earth track. |

## 4. Schematic Symbol Representation
```
       [ J1: IEC 320-C14 INLET ]
             ┌─────────┐
    Line  [L]│─────────│─── Net: AC_LINE_IN ──────> To Fuse F1
             │         │
 Neutral  [N]│─────────│─── Net: AC_NEUTRAL_IN ───> To NTC1
             │         │
   Earth  [E]│─────────│─── Net: EARTH_GND ───────> Chassis Earth & Y-Caps
             └─────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Creepage & Clearance**: Maintain $\ge 3.0\,\text{mm}$ clearance between Live and Neutral terminals, and $\ge 4.0\,\text{mm}$ between Live/Neutral and Earth chassis ground.
2. **Safety Marking**: Clearly silkscreen High-Voltage warning symbols `[!] CAUTION: HIGH VOLTAGE 85-265V AC` directly adjacent to `J1`.
3. **Chassis Earth Bonding**: Earth terminal must be mechanically bonded to the metal chassis using an M4 screw with a star washer to guarantee $< 0.1\,\Omega$ ground bond resistance.
""")

    # 2. F1 Cartridge Fuse
    with open(OUT_DIR / "F1_cartridge_fuse.md", "w") as f:
        f.write("""# Component Schematic Specification: F1 (AC Mains Input Cartridge Fuse)

## 1. Component Metadata
* **Reference Designator**: `F1` (Mounted in PCB clips `FC1`, `FC2`)
* **Component Type**: Time-Lag (Slow-Blow) Ceramic Cartridge Fuse
* **Manufacturer**: Littelfuse Inc.
* **Primary MPN**: `0218002.MXP`
* **Alternate Manufacturer**: Schurter
* **Alternate MPN**: `0001.2507`
* **Package / Footprint**: $5 \times 20\,\text{mm}$ Cylindrical Cartridge (Clips: Keystone Electronics `3515`)
* **Subsystem**: Stage 1 (Mains AC Input & Protection)

## 2. Electrical Ratings & Constraints
* **Rated Current ($I_n$)**: $2.0\,\text{A}_{\text{RMS}}$
* **Rated Voltage**: $250\,\text{V}_{\text{AC RMS}}$
* **Melting Energy ($I^2t$)**: $19.6\,\text{A}^2\text{s}$ (Safely absorbs inrush $I^2t \approx 0.468\,\text{A}^2\text{s} \ll 19.6\,\text{A}^2\text{s}$)
* **Interrupting Rating**: $1500\,\text{A}$ @ $250\,\text{V}_{\text{AC}}$ (IEC 60127-2 Sheet 5)
* **Maximum Continuous Load Current**: $1.604\,\text{A}_{\text{RMS}}$ at $85\,\text{V}_{\text{AC}}$ ($80.2\%$ loading $\le 85\%$)

## 3. Schematic Pin Connections & Net Mapping
| Pin / Clip # | Clip Designation | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `FC1` (Input) | `AC_LINE_IN` | `J1` Terminal L | $2.5\,\text{mm}$ width on Layer 1 (2oz Cu), reinforced with bottom trace. |
| **2** | `FC2` (Output) | `AC_LINE_FUSED`| `MOV1` (Terminal 1), `C_X1` (Terminal 1), `L_CM1` (Pin 1) | $2.5\,\text{mm}$ width on Layer 1 (2oz Cu). Low-impedance bus. |

## 4. Schematic Symbol Representation
```
     Net: AC_LINE_IN                       Net: AC_LINE_FUSED
    ───────────────────[  F1: 2.0A TIME-LAG  ]───────────────────> To MOV1, CX1, LCM1
                          5x20mm Ceramic
```

## 5. Schematic & PCB Layout Guidelines
1. **Fuse Proximity**: Place `F1` immediately adjacent to AC inlet `J1` Live pin ($< 15\,\text{mm}$ trace length).
2. **No Polygon Copper Underneath**: Strip all copper polygon pours on all layers directly beneath the fuse body ($5 \times 20\,\text{mm}$ keepout) to prevent arcing during catastrophic rupture.
3. **Fuse Clips**: Use heavy-duty tin-plated phosphor bronze clips (`Keystone 3515`) to ensure low contact resistance and prevent thermal oxidation.
""")

    # 3. NTC1 Inrush Thermistor
    with open(OUT_DIR / "NTC1_inrush_thermistor.md", "w") as f:
        f.write("""# Component Schematic Specification: NTC1 (Inrush Current Limiter)

## 1. Component Metadata
* **Reference Designator**: `NTC1`
* **Component Type**: Negative Temperature Coefficient (NTC) Power Thermistor
* **Manufacturer**: TDK / EPCOS
* **Primary MPN**: `B57236S0150M000`
* **Alternate Manufacturer**: Amphenol Ametherm
* **Alternate MPN**: `SL15 15003`
* **Package / Footprint**: Radial Disc (Body diameter: $13.0\,\text{mm}$, Lead spacing: $7.5\,\text{mm}$)
* **Subsystem**: Stage 1 (Mains AC Input & Protection)

## 2. Electrical Ratings & Constraints
* **Cold Resistance ($R_{25}$)**: $15.0\,\Omega \pm 20\%$
* **Maximum Continuous Current**: $2.90\,\text{A}_{\text{RMS}}$ (Derating margin: $1.604\,\text{A} / 2.90\,\text{A} = 55.3\% \le 70\%$)
* **Maximum Cold-Start Inrush Current**: $I_{\text{pk}} = (265\,\text{V} \times \sqrt{2}) / 15.0\,\Omega = \mathbf{24.98\,\text{A}_{\text{peak}}}$ (Guaranteed $< 25.0\,\text{A}$)
* **Hot Steady-State Resistance ($R_{\text{hot}}$)**: $\approx 0.48\,\Omega$ @ $100^\circ\text{C}$
* **Full-Load Power Dissipation**: $P = (0.55\,\text{A})^2 \times 0.48\,\Omega = \mathbf{0.145\,\text{W}}$ (Negligible loss)

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Thermal Requirements |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Input Lead | `AC_NEUTRAL_IN` | `J1` Terminal N | $2.5\,\text{mm}$ width on Layer 1 (2oz Cu). |
| **2** | Output Lead | `AC_NEUTRAL_PROT`| `MOV1` (Terminal 2), `C_X1` (Terminal 2), `L_CM1` (Pin 2) | $2.5\,\text{mm}$ width on Layer 1 (2oz Cu). |

## 4. Schematic Symbol Representation
```
     Net: AC_NEUTRAL_IN                   Net: AC_NEUTRAL_PROT
    ──────────────────────[ NTC1: 15.0Ω ]───────────────────────> To MOV1, CX1, LCM1
                           B57236S0150M
```

## 5. Schematic & PCB Layout Guidelines
1. **Thermal Separation**: NTC thermistors operate hot ($\approx 80^\circ\text{C} - 110^\circ\text{C}$ under full load). Maintain at least $10.0\,\text{mm}$ physical spacing from temperature-sensitive electrolytic capacitors (`C_BULK1`).
2. **Elevated Mounting**: In through-hole assembly, mount `NTC1` with $3\,\text{mm} - 5\,\text{mm}$ standoff height above the PCB to promote airflow and prevent localized board scorching.
""")

    # 4. MOV1 Surge Varistor
    with open(OUT_DIR / "MOV1_surge_varistor.md", "w") as f:
        f.write("""# Component Schematic Specification: MOV1 (Line Surge Varistor)

## 1. Component Metadata
* **Reference Designator**: `MOV1`
* **Component Type**: Metal Oxide Varistor (MOV) Transient Surge Suppressor
* **Manufacturer**: Bourns Inc.
* **Primary MPN**: `MOV-14D471K`
* **Alternate Manufacturer**: Littelfuse
* **Alternate MPN**: `V300LA20AP`
* **Package / Footprint**: Radial Disc (Body diameter: $14.0\,\text{mm}$, Lead spacing: $7.5\,\text{mm}$)
* **Subsystem**: Stage 1 (Mains AC Input & Protection)

## 2. Electrical Ratings & Constraints
* **Max Continuous Operating Voltage**: $300\,\text{V}_{\text{AC RMS}}$ / $385\,\text{V}_{\text{DC}}$ ($13.2\%$ safety margin above $265\,\text{V}_{\text{AC}}$)
* **Nominal Varistor Voltage ($V_N$)**: $470\,\text{V} \pm 10\%$ @ $1\,\text{mA}_{\text{DC}}$
* **Maximum Clamping Voltage ($V_C$)**: $775\,\text{V}$ @ $50.0\,\text{A}$ ($8/20\,\mu\text{s}$ surge)
* **Peak Surge Current ($I_{\text{max}}$)**: $4500\,\text{A}$ ($8/20\,\mu\text{s}$ single wave)
* **Energy Absorption Capacity**: $125.0\,\text{Joules}$
* **Compliance**: IEC 61000-4-5 Level 3 ($1.0\,\text{kV}$ line-to-line surge test, derating $3.1\% \ll 60\%$)

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Terminal 1 | `AC_LINE_FUSED` | Fuse `F1` output, `C_X1` Pin 1, `L_CM1` Pin 1 | $2.5\,\text{mm}$ width (2oz Cu). Solder directly across line bus. |
| **2** | Terminal 2 | `AC_NEUTRAL_PROT`| `NTC1` output, `C_X1` Pin 2, `L_CM1` Pin 2 | $2.5\,\text{mm}$ width (2oz Cu). Solder directly across line bus. |

## 4. Schematic Symbol Representation
```
                     Net: AC_LINE_FUSED
                             │
                           ┌─┴─┐
                           │   │  MOV1: 300V RMS / 470V
                           │   │  Bourns MOV-14D471K
                           └─┬─┘
                             │
                   Net: AC_NEUTRAL_PROT
```

## 5. Schematic & PCB Layout Guidelines
1. **Parallel Placement**: Solder `MOV1` directly between `AC_LINE_FUSED` and `AC_NEUTRAL_PROT` immediately downstream of `F1` and `NTC1`. If the MOV degrades into a thermal short, `F1` opens instantly without fire hazard.
2. **Clearance**: Maintain $\ge 3.0\,\text{mm}$ copper clearance around `MOV1` terminals.
""")

    # 5. LCM1 & LCM2 Common Mode Chokes
    with open(OUT_DIR / "L_CM1_L_CM2_common_mode_chokes.md", "w") as f:
        f.write("""# Component Schematic Specification: L_CM1 & L_CM2 (Common-Mode EMI Chokes)

## 1. Component Metadata
* **Reference Designators**: `L_CM1` (Stage 1 LF Choke), `L_CM2` (Stage 2 HF Choke)
* **Component Type**: Two-Winding Common-Mode Inductors
* **Manufacturer**: Wurth Elektronik
* **Primary MPNs**:
  * `L_CM1`: `744823215` ($15.0\,\text{mH} \pm 30\%$, $1.10\,\text{A}_{\text{RMS}}$, Toroid Core)
  * `L_CM2`: `744822472` ($4.70\,\text{mH} \pm 30\%$, $1.60\,\text{A}_{\text{RMS}}$, Sectional Winding Core)
* **Alternate Manufacturers**: KEMET (`SC-10-10J`) / Bourns (`7355-V-RC`)
* **Package / Footprint**: 4-Pin Through-Hole Toroidal Header (Pitch $15.0 \times 10.0\,\text{mm}$)
* **Subsystem**: Stage 1 (Mains AC Input & EMI Filter)

## 2. Electrical Ratings & Constraints
* **Operating Voltage**: $250\,\text{V}_{\text{AC RMS}}$ continuous ($500\,\text{V}$ dielectric test withstand between windings)
* **Current Rating**: $1.10\,\text{A}$ (`L_CM1`) / $1.60\,\text{A}$ (`L_CM2`) (Operating RMS: $0.55\,\text{A}$ @ $230\,\text{V}$, $1.60\,\text{A}$ @ $85\,\text{V}$)
* **Frequency Coverage**:
  * `L_CM1` ($15\,\text{mH}$): Sized for $150\,\text{kHz} - 2.0\,\text{MHz}$ low-frequency attenuation.
  * `L_CM2` ($4.7\,\text{mH}$): Sized for $2.0\,\text{MHz} - 30.0\,\text{MHz}$ high-frequency attenuation.
* **Combined CM Attenuation**: $> 35.4\,\text{dB}$ at $150\,\text{kHz}$, ensuring CISPR 32 Class B compliance.

## 3. Schematic Pin Connections & Net Mapping
### L_CM1 (Stage 1 Choke)
| Pin # | Winding | Net Name (In/Out) | Connected To | Phase Dot |
| :---: | :---: | :--- | :--- | :---: |
| **1** | W1 (Line) In | `AC_LINE_FUSED` | Fuse `F1`, `MOV1`, `C_X1` Pin 1 | [Dot] |
| **2** | W1 (Line) Out | `AC_LINE_CM1` | `L_CM2` Pin 1, `C_Y1` Pin 1 | — |
| **3** | W2 (Neut) Out | `AC_NEUTRAL_CM1` | `L_CM2` Pin 2, `C_Y2` Pin 1 | — |
| **4** | W2 (Neut) In | `AC_NEUTRAL_PROT` | `NTC1`, `MOV1`, `C_X1` Pin 2 | [Dot] |

### L_CM2 (Stage 2 Choke)
| Pin # | Winding | Net Name (In/Out) | Connected To | Phase Dot |
| :---: | :---: | :--- | :--- | :---: |
| **1** | W1 (Line) In | `AC_LINE_CM1` | `L_CM1` Pin 2, `C_Y1` Pin 1 | [Dot] |
| **2** | W1 (Line) Out | `AC_LINE_FILT` | `C_X2` Pin 1, Bridge Rectifier `BR1` Pin 2 (AC) | — |
| **3** | W2 (Neut) Out | `AC_NEUTRAL_FILT`| `C_X2` Pin 2, Bridge Rectifier `BR1` Pin 3 (AC) | — |
| **4** | W2 (Neut) In | `AC_NEUTRAL_CM1` | `L_CM1` Pin 3, `C_Y2` Pin 1 | [Dot] |

## 4. Schematic Symbol Representation
```
     Net: AC_LINE_FUSED             L_CM1                   Net: AC_LINE_CM1            L_CM2                   Net: AC_LINE_FILT
    ──────────────────────●═══[ W1: 15mH ]═══───────────────●═══[ W1: 4.7mH ]═══────────────> To BR1 Pin 2
                               ║║                                        ║║
    ──────────────────────●═══[ W2: 15mH ]═══───────────────●═══[ W2: 4.7mH ]═══────────────> To BR1 Pin 3
     Net: AC_NEUTRAL_PROT                           Net: AC_NEUTRAL_CM1         Net: AC_NEUTRAL_FILT
```

## 5. Schematic & PCB Layout Guidelines
1. **Winding Phasing**: Strict adherence to winding phase dots is essential. If one winding is reversed, common-mode impedance collapses to near zero.
2. **Symmetric Routing**: Keep Live and Neutral traces perfectly parallel and identical in length through both chokes.
3. **No Cross-Talk**: Route input traces and output traces on opposite sides of the choke body to prevent capacitive bypass coupling.
""")

    # 6. CX and CY Safety Capacitors
    with open(OUT_DIR / "C_X_C_Y_safety_capacitors.md", "w") as f:
        f.write("""# Component Schematic Specification: C_X1, C_X2 & C_Y1, C_Y2 (Safety Capacitors)

## 1. Component Metadata
* **Reference Designators**:
  * `C_X1`, `C_X2`: Class X2 Across-The-Line Metallized Polypropylene Film Capacitors
  * `C_Y1`, `C_Y2`: Class Y1 Line-To-Earth Double Reinforced Ceramic Capacitors
* **Manufacturers**: KEMET (`R46` Series for X2, `PHE850` Series for Y1) / Murata (`DE1E3KX222M`)
* **Primary MPNs**:
  * `C_X1, C_X2`: `R46KI32200001M` ($0.22\,\mu\text{F} \pm 20\%$, $310\,\text{V}_{\text{AC RMS}}$, Pitch $15.0\,\text{mm}$)
  * `C_Y1, C_Y2`: `PHE850ED6220MD15R06L2` ($2.2\,\text{nF} \pm 20\%$, $400\,\text{V}_{\text{AC RMS}}$, Pitch $10.0\,\text{mm}$)
* **Subsystem**: Stage 1 (Mains AC Input & EMI Filter)

## 2. Electrical Ratings & Safety Limits
* **Class X2 Capacitors**:
  * Rated AC Voltage: $310\,\text{V}_{\text{AC RMS}}$ (Continuous line-to-line operation)
  * Self-healing metallized polypropylene dielectric.
  * Role: Attenuates differential-mode switching noise.
* **Class Y1 Capacitors**:
  * Rated AC Voltage: $400\,\text{V}_{\text{AC RMS}}$ (Reinforced line-to-earth insulation)
  * Proof withstand voltage: $> 4000\,\text{V}_{\text{AC}}$ for $60\,\text{seconds}$.
  * Earth Leakage Current Calculation:
    $$I_{\text{leak}} = 2\pi \times f \times V_{\text{IN,max}} \times (C_{\text{Y1}} + C_{\text{Y2}}) = 2\pi \times 50\,\text{Hz} \times 265\,\text{V} \times 4.4\,\text{nF} = \mathbf{0.366\,\text{mA}}$$
    Strictly complies with the IEC 62368-1 allowable touch-current limit of $< 0.75\,\text{mA}$.

## 3. Schematic Pin Connections & Net Mapping
| Ref Des | Pin 1 Net Name | Connected To | Pin 2 Net Name | Connected To | Safety Role |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **`C_X1`** | `AC_LINE_FUSED` | Fuse `F1`, `MOV1`, `L_CM1` Pin 1 | `AC_NEUTRAL_PROT` | `NTC1`, `MOV1`, `L_CM1` Pin 4 | Pre-filter differential noise bypass. |
| **`C_X2`** | `AC_LINE_FILT` | `L_CM2` Pin 2, Bridge `BR1` Pin 2 | `AC_NEUTRAL_FILT` | `L_CM2` Pin 3, Bridge `BR1` Pin 3 | Post-filter differential noise bypass. |
| **`C_Y1`** | `AC_LINE_CM1` | Node between `L_CM1` & `L_CM2` | `EARTH_GND` | Chassis Earth Stud / Earth Pin of J1 | Line-to-Earth common mode noise drain. |
| **`C_Y2`** | `AC_NEUTRAL_CM1`| Node between `L_CM1` & `L_CM2` | `EARTH_GND` | Chassis Earth Stud / Earth Pin of J1 | Neutral-to-Earth common mode noise drain. |

## 4. Schematic Symbol Representation
```
     Net: AC_LINE_FUSED                                           Net: AC_LINE_FILT
    ───────────────┬───────────────────[ L_CM1/2 ]───────────────────────┬──────────> To Bridge
                   │                                                     │
                 ┌─┴─┐                                                 ┌─┴─┐
                 │CX1│ (0.22µF X2)                                     │CX2│ (0.22µF X2)
                 └─┬─┘                                                 └─┬─┘
                   │             Net: AC_LINE_CM1                        │
    ───────────────┼───────────────┬───────────                    ──────┼──────────> To Bridge
                   │             ┌─┴─┐                             │     │
                   │             │CY1│ (2.2nF Y1)                  │   Net: AC_NEUTRAL_FILT
                   │             └─┬─┘                             │
                   │               │                               │
                   │               └─── Net: EARTH_GND ────────────┤
                   │               ┌───                            │
                   │             ┌─┴─┐                             │
                   │             │CY2│ (2.2nF Y1)                  │
                   │             └─┬─┘                             │
                   │             Net: AC_NEUTRAL_CM1               │
                   │               │                               │
    ───────────────┴───────────────┴───────────────────────────────┴──────────> To Bridge
     Net: AC_NEUTRAL_PROT
```

## 5. Schematic & PCB Layout Guidelines
1. **Low-Inductive Ground Return**: The ground pin of `C_Y1` and `C_Y2` must return to the chassis earth terminal via a short, wide copper pour ($> 2.0\,\text{mm}$ width).
2. **Creepage**: Maintain $\ge 6.4\,\text{mm}$ creepage distance between the AC line pins of the Y-capacitors and secondary ground planes.
""")

    # 7. Module 1 Equivalent Circuit
    with open(OUT_DIR / "module_01_mains_emi_equivalent_circuit.md", "w") as f:
        f.write("""# Module 1: Mains AC Input Protection & EMI Filter — Equivalent Electronic Circuit

## 1. Subsystem Architectural Overview
Module 1 serves as the frontline power interface connecting the single-phase commercial utility AC mains ($85\,\text{V} - 265\,\text{V}_{\text{AC RMS}}$, $47 - 63\,\text{Hz}$) to the power supply PCBA. It incorporates multi-layered hardware protection against catastrophic short circuits, inrush transients, and lightning surges, while attenuating conducted electromagnetic emissions to meet **CISPR 32 / EN 55032 Class B** standards.

## 2. Full Schematic-Level Equivalent Electronic Circuit Diagram

```
                              [ MODULE 1: MAINS AC INPUT & 2-STAGE EMI FILTER ]
=============================================================================================================================

          J1: IEC C14
         ┌───────────┐         F1: 2.0A Slow-Blow
Live     │ Terminal L│─────────[=== 5x20mm ===]─────────┬──────────────┬──────────────●═══════════════════╗ L_CM1: 15mH
85-265V  │           │      Littelfuse 0218002.MXP      │              │              ║   Winding 1       ║
         │           │       (Melting I²t=19.6A²s)    ┌─┴─┐          ┌─┴─┐            ║                   ║
         │           │                                │   │          │   │ C_X1       ╚═══════════════════●
         │           │                                │   │ MOV1     │   │ 0.22µF X2            │
         │           │                                │   │ 300V     │   │ KEMET R46            ├─── Net: AC_LINE_CM1
         │           │                                └─┬─┘ 4.5kA    └─┬─┘ 310V AC              │
         │           │                                  │              │                      ┌─┴─┐
         │           │                                  │              │                      │   │ C_Y1: 2.2nF Y1
         │           │                                  │              │                      │   │ KEMET PHE850
         │           │         NTC1: 15.0Ω Cold         │              │                      └─┬─┘ 400V AC
Neutral  │ Terminal N│─────────[───/\/\/\/\───]─────────┴──────────────┴──────────────●           │
0V Nom   │           │      EPCOS B57236S0150M                                        ║           ├───── Net: EARTH_GND
         │           │     (Inrush < 24.98A peak)                                     ║ L_CM1     │      (Chassis Earth Stud)
         │           │                                                                ║ Winding 2 ├─────┐
Earth    │ Terminal E│────────────────────────────────────────────────────────────────────────────┘   ┌─┴─┐
         └───────────┘                                                                                │   │ C_Y2: 2.2nF Y1
                                                                                      ╚═══════════════●   │ KEMET PHE850
                                                                                                │     └─┬─┘ 400V AC
                                                                                                │       │
                                                                                 Net: AC_NEUT_CM1───────┘

  (Continuation into Stage 2 Common Mode Choke L_CM2 & Post-Filter C_X2)
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

 Net: AC_LINE_CM1
 ────────────────────────●═══════════════════╗ L_CM2: 4.7mH
                         ║   Winding 1       ║
                         ║                   ║
                         ╚═══════════════════●──────┬───────────────────────────────────────────> Net: AC_LINE_FILT
                                                    │                                             (To Bridge BR1 Pin 2)
                                                  ┌─┴─┐
                                                  │   │ C_X2
                                                  │   │ 0.22µF X2
                                                  │   │ KEMET R46
                                                  └─┬─┘ 310V AC
                         ╔═══════════════════●      │
                         ║                   ║      │
                         ║   Winding 2       ║      │
 ────────────────────────●═══════════════════╝──────┴───────────────────────────────────────────> Net: AC_NEUTRAL_FILT
 Net: AC_NEUT_CM1        L_CM2: 4.7mH                                                             (To Bridge BR1 Pin 3)

=============================================================================================================================
```

## 3. Subsystem Netlist & Interconnect Table
| Net Name | Origin Pin | Destination Pins | Nominal Voltage / Current | Functional Description |
| :--- | :--- | :--- | :---: | :--- |
| `AC_LINE_IN` | `J1` (Pin L) | `F1` (Input Clip `FC1`) | $85 - 265\,\text{V}_{\text{AC}}$ / $1.60\,\text{A}_{\text{RMS}}$ | Raw grid live entry from IEC socket. |
| `AC_NEUTRAL_IN` | `J1` (Pin N) | `NTC1` (Input Lead) | $0\,\text{V}_{\text{AC}}$ Nominal / $1.60\,\text{A}_{\text{RMS}}$ | Raw grid neutral entry. |
| `EARTH_GND` | `J1` (Pin E) | `C_Y1` (Pin 2), `C_Y2` (Pin 2), Chassis | $0\,\text{V}$ (Chassis Reference) | Protective Earth safety drainage path. |
| `AC_LINE_FUSED` | `F1` (Output Clip `FC2`) | `MOV1` (Pin 1), `C_X1` (Pin 1), `L_CM1` (Pin 1) | $85 - 265\,\text{V}_{\text{AC}}$ / $1.60\,\text{A}_{\text{RMS}}$ | Fused live bus distributing power to surge and filter. |
| `AC_NEUTRAL_PROT` | `NTC1` (Output Lead) | `MOV1` (Pin 2), `C_X1` (Pin 2), `L_CM1` (Pin 4) | $0\,\text{V}_{\text{AC}}$ Nominal / $1.60\,\text{A}_{\text{RMS}}$ | Damped neutral bus feeding surge and filter. |
| `AC_LINE_CM1` | `L_CM1` (Pin 2) | `C_Y1` (Pin 1), `L_CM2` (Pin 1) | $85 - 265\,\text{V}_{\text{AC}}$ / $1.60\,\text{A}_{\text{RMS}}$ | Intermediate stage 1 filtered live bus. |
| `AC_NEUTRAL_CM1` | `L_CM1` (Pin 3) | `C_Y2` (Pin 1), `L_CM2` (Pin 4) | $0\,\text{V}_{\text{AC}}$ Nominal / $1.60\,\text{A}_{\text{RMS}}$ | Intermediate stage 1 filtered neutral bus. |
| `AC_LINE_FILT` | `L_CM2` (Pin 2) | `C_X2` (Pin 1), `BR1` (Pin 2 AC) | $85 - 265\,\text{V}_{\text{AC}}$ / $1.60\,\text{A}_{\text{RMS}}$ | Fully filtered, EMC-compliant live output to bridge. |
| `AC_NEUTRAL_FILT` | `L_CM2` (Pin 3) | `C_X2` (Pin 2), `BR1` (Pin 3 AC) | $0\,\text{V}_{\text{AC}}$ Nominal / $1.60\,\text{A}_{\text{RMS}}$ | Fully filtered, EMC-compliant neutral output to bridge. |

## 4. Theory of Operation & Filtering Transfer Functions
1. **Inrush Current Suppression**: When energized at peak AC line ($265\,\text{V}_{\text{RMS}} \times \sqrt{2} = 374.8\,\text{V}_{\text{peak}}$), the uncharged bulk capacitor presents an instantaneous dead short. `NTC1` ($15.0\,\Omega$ cold resistance) acts as an instantaneous series impedance:
   $$I_{\text{inrush,max}} = \frac{374.77\,\text{V}}{15.0\,\Omega} = \mathbf{24.98\,\text{A}_{\text{peak}}}$$
   As steady-state current flows, the thermistor self-heats to $\approx 100^\circ\text{C}$, dropping resistance to $0.48\,\Omega$ and wasting only $0.145\,\text{W}$.
2. **Surge Voltage Clamping**: During an overvoltage surge (e.g. $1000\,\text{V}$ combination spike per IEC 61000-4-5), `MOV1` transitions from high-impedance ($> 10\,\text{M}\Omega$) to conducting mode within $< 25\,\text{ns}$, clamping line voltage below $775\,\text{V}$ and absorbing up to $125\,\text{Joules}$.
3. **Differential Mode Noise Attenuation**: The leakage inductances of `L_CM1` ($L_{\text{lk1}} \approx 225\,\mu\text{H}$) and `L_CM2` ($L_{\text{lk2}} \approx 70\,\mu\text{H}$) combine with `C_X1` and `C_X2` ($0.22\,\mu\text{F}$ each) to form a second-order low-pass filter with corner frequency:
   $$f_{c,\text{DM}} = \frac{1}{2\pi \sqrt{L_{\text{lk}} \times C_X}} = \frac{1}{2\pi \sqrt{225\,\mu\text{H} \times 0.22\,\mu\text{F}}} \approx \mathbf{22.6\,\text{kHz}}$$
   Provides $> 18\,\text{dB}$ attenuation at the $65\,\text{kHz}$ Flyback switching fundamental.
4. **Common Mode Noise Attenuation**: Formed by $L_{\text{CM1}} = 15.0\,\text{mH}$ and $C_Y = 2 \times 2.2\,\text{nF} = 4.4\,\text{nF}$:
   $$f_{c,\text{CM}} = \frac{1}{2\pi \sqrt{15\,\text{mH} \times 4.4\,\text{nF}}} \approx \mathbf{19.6\,\text{kHz}}$$
   Provides $> 35.4\,\text{dB}$ attenuation at $150\,\text{kHz}$ (the start of CISPR 32 Class B conducted limits).

## 5. Laboratory Bring-Up & Test Points
* **`TP_AC1` (Live Input)**: Located on output of `F1`. Verify pure sinusoidal AC voltage ($85 - 265\,\text{V}_{\text{AC RMS}}$) referenced to Neutral.
* **`TP_AC2` (Filtered Live)**: Located on pin 2 of `BR1`. Inspect with an oscilloscope (high-voltage differential probe); confirm clean sine wave with switching ripple $< 100\,\text{mV}_{\text{pk-pk}}$.
* **`TP_EARTH` (Chassis Earth)**: Verify zero potential difference ($< 0.1\,\text{V}$) to utility earth. Measure leakage current using an earth leakage meter: confirm reading is $\approx 0.36\,\text{mA} < 0.75\,\text{mA}$.
""")

    print("Module 1 files successfully generated.")

if __name__ == "__main__":
    write_files()
