#!/usr/bin/env python3
"""
Component and Schematic Connection Generator: Module 8 (Auxiliary Power Distribution)
"""

from pathlib import Path

OUT_DIR = Path("/home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/components_sch/module_08_auxiliary_power_distribution")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def write_files():
    # 1. U7_REG L78L12 +12V Linear Regulator
    with open(OUT_DIR / "U7_REG_l78l12_gate_bias.md", "w") as f:
        f.write(r"""# Component Schematic Specification: U7_REG (L78L12ACUTR +12V Gate Bias Regulator)

## 1. Component Metadata
* **Reference Designator**: `U7_REG`
* **Component Type**: Positive Voltage 3-Terminal Linear Voltage Regulator
* **Manufacturer**: STMicroelectronics
* **Primary MPN**: `L78L12ACUTR`
* **Alternate Manufacturer**: ON Semiconductor
* **Alternate MPN**: `MC78L12ABPRPG` (SOT-89 or TO-92 equivalent)
* **Package / Footprint**: SOT-89-3 (Pitch: 1.50 mm, Exposed Center Tab Ground)
* **Subsystem**: Stage 8 (Auxiliary Power Tree: Gate Driver Bias Rail)

## 2. Electrical Ratings & Constraints
* **Input Voltage Range ($V_{\text{IN}}$)**: $+14.5\,\text{V}$ to $+35.0\,\text{V}_{\text{DC}}$
  * Operating input: $+24.0\,\text{V}_{\text{DC}} \pm 0.8\%$ intermediate bus.
  * Input Voltage Stress Derating: $\frac{24.0\,\text{V}}{35.0\,\text{V}} = \mathbf{68.57\%} \le 75\%$.
* **Nominal Output Voltage ($V_{\text{OUT}}$)**: $+12.0\,\text{V}_{\text{DC}} \pm 4.0\%$ ($+11.5\,\text{V}$ to $+12.5\,\text{V}$)
* **Maximum Output Current ($I_{\text{OUT,max}}$)**: $100.0\,\text{mA}$
  * Average load current: $I_{\text{load}} \approx 25.0\,\text{mA}$ (LM5176 `BIAS` pin gate-drive replenishment + downstream 5V regulator quiescent current).
  * Current Derating: $\frac{25.0\,\text{mA}}{100.0\,\text{mA}} = \mathbf{25.0\%} \le 70\%$.
* **Power Dissipation & Thermal Stress**:
  $$P_{\text{loss,U7}} = (V_{\text{IN}} - V_{\text{OUT}}) \times I_{\text{load}} = (24.0\,\text{V} - 12.0\,\text{V}) \times (0.025\,\text{A}) = \mathbf{0.300\,\text{W}} \quad (300.0\,\text{mW})$$
  * Thermal resistance on 4-layer PCB with thermal vias under center tab: $\theta_{\text{JA}} \approx 80^\circ\text{C/W}$.
  * Junction temperature rise:
    $$\Delta T_j = P_{\text{loss}} \times \theta_{\text{JA}} = 0.30\,\text{W} \times 80^\circ\text{C/W} = \mathbf{24.0^\circ\text{C}}$$
  * At $50^\circ\text{C}$ worst-case ambient: $T_j = 50 + 24 = \mathbf{74.0^\circ\text{C}} \ll 110.0^\circ\text{C}$ (VVDN Derating PASS).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`OUT`** | `+12V_AUX` | Ceramic cap $C_{\text{OUT,12V}} = 1.0\,\mu\text{F} / 25\,\text{V}$, `U3` BIAS (Pin 22), `U8_REG` IN | $1.0\,\text{mm}$ trace width. |
| **2** | **`GND`** | `GND_SELV` | Secondary ground plane (Layer 2) | Direct thermal connection to tab. |
| **3** | **`IN`**  | `+24V_SEC` | Ceramic cap $C_{\text{IN,12V}} = 1.0\,\mu\text{F} / 50\,\text{V}$, Stage 3 24V rail | $1.0\,\text{mm}$ trace width. |
| **TAB**| **`GND`**| `GND_SELV` | Array of 4 thermal vias ($0.3\,\text{mm}$ drill) to Layer 2 ground plane | Thermal dissipation tab. |

## 4. Schematic Symbol Representation
```
                    [ U7_REG: L78L12ACUTR +12V LINEAR REGULATOR ]
                                   SOT-89 Package
                                  ┌───────────────┐
         Net: +24V_SEC  ─────────[3] IN       OUT[1]───────── Net: +12V_AUX
                                  │      GND      │
                                  └───────┬───────┘
                                         [2] (Tab)
                                          │
                                    Net: GND_SELV
```

## 5. Schematic & PCB Layout Guidelines
1. **Decoupling**: Place a $1.0\,\mu\text{F} / 50\,\text{V}$ X7R MLCC directly between Pin 3 and GND tab, and a $1.0\,\mu\text{F} / 25\,\text{V}$ X7R MLCC between Pin 1 and GND tab.
2. **Thermal Spreading**: Connect Pin 2 / center tab to an exposed top-layer copper polygon ($10 \times 10\,\text{mm}$) stitched with 4 thermal vias directly into the internal ground plane.
""")

    # 2. U8_REG L78L05 +5V Linear Regulator
    with open(OUT_DIR / "U8_REG_l78l05_display_rail.md", "w") as f:
        f.write(r"""# Component Schematic Specification: U8_REG (L78L05ABUTR +5V Display & Logic Regulator)

## 1. Component Metadata
* **Reference Designator**: `U8_REG`
* **Component Type**: Positive Voltage 3-Terminal Linear Voltage Regulator
* **Manufacturer**: STMicroelectronics
* **Primary MPN**: `L78L05ABUTR`
* **Alternate Manufacturer**: Texas Instruments
* **Alternate MPN**: `LM78L05ACMX/NOPB` (SOIC-8 or SOT-89 equivalent)
* **Package / Footprint**: SOT-89-3 (Pitch: 1.50 mm, Exposed Center Tab Ground)
* **Subsystem**: Stage 8 (Auxiliary Power Tree: +5V Display & Sub-Regulator Intermediate Rail)

## 2. Electrical Ratings & Constraints
* **Input Voltage Range ($V_{\text{IN}}$)**: $+7.0\,\text{V}$ to $+30.0\,\text{V}_{\text{DC}}$
  * Operating input: $+12.0\,\text{V}_{\text{DC}}$ from `U7_REG` output.
  * Input Voltage Stress Derating: $\frac{12.0\,\text{V}}{30.0\,\text{V}} = \mathbf{40.0\%} \le 75\%$.
* **Nominal Output Voltage ($V_{\text{OUT}}$)**: $+5.0\,\text{V}_{\text{DC}} \pm 4.0\%$ ($+4.8\,\text{V}$ to $+5.2\,\text{V}$)
* **Maximum Output Current ($I_{\text{OUT,max}}$)**: $100.0\,\text{mA}$
  * Average load current: $I_{\text{load}} \approx 40.0\,\text{mA}$ ($15\,\text{mA}$ for OLED display logic + $25\,\text{mA}$ feeding the 3.3V LDO).
  * Current Derating: $\frac{40.0\,\text{mA}}{100.0\,\text{mA}} = \mathbf{40.0\%} \le 70\%$.
* **Power Dissipation & Thermal Stress**:
  $$P_{\text{loss,U8}} = (V_{\text{IN}} - V_{\text{OUT}}) \times I_{\text{load}} = (12.0\,\text{V} - 5.0\,\text{V}) \times (0.040\,\text{A}) = \mathbf{0.280\,\text{W}} \quad (280.0\,\text{mW})$$
  * Junction temperature rise ($\theta_{\text{JA}} \approx 80^\circ\text{C/W}$):
    $$\Delta T_j = 0.28\,\text{W} \times 80^\circ\text{C/W} = \mathbf{22.4^\circ\text{C}}$$
  * At $50^\circ\text{C}$ ambient: $T_j = 50 + 22.4 = \mathbf{72.4^\circ\text{C}} \ll 110.0^\circ\text{C}$ (PASS).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`OUT`** | `+5V_SEC` | Ceramic cap $C_{\text{OUT,5V}} = 1.0\,\mu\text{F} / 16\,\text{V}$, OLED Header Pin 1, `U9_REG` IN | $1.0\,\text{mm}$ trace width. |
| **2** | **`GND`** | `GND_SELV` | Secondary ground plane (Layer 2) | Direct thermal connection to tab. |
| **3** | **`IN`**  | `+12V_AUX` | Ceramic cap $C_{\text{IN,5V}} = 1.0\,\mu\text{F} / 25\,\text{V}$, `U7_REG` OUT | $1.0\,\text{mm}$ trace width. |
| **TAB**| **`GND`**| `GND_SELV` | Array of 4 thermal vias ($0.3\,\text{mm}$ drill) to Layer 2 ground plane | Thermal dissipation tab. |

## 4. Schematic Symbol Representation
```
                    [ U8_REG: L78L05ABUTR +5V LINEAR REGULATOR ]
                                   SOT-89 Package
                                  ┌───────────────┐
         Net: +12V_AUX  ─────────[3] IN       OUT[1]───────── Net: +5V_SEC
                                  │      GND      │
                                  └───────┬───────┘
                                         [2] (Tab)
                                          │
                                    Net: GND_SELV
```
""")

    # 3. U9_REG AP2114 +3.3V Low-Dropout Regulator
    with open(OUT_DIR / "U9_REG_ap2114_3v3_ldo.md", "w") as f:
        f.write(r"""# Component Schematic Specification: U9_REG (AP2114H-3.3TRG1 Low-Dropout Regulator)

## 1. Component Metadata
* **Reference Designator**: `U9_REG`
* **Component Type**: CMOS High-Accuracy Low-Dropout Linear Regulator (LDO)
* **Manufacturer**: Diodes Incorporated
* **Primary MPN**: `AP2114H-3.3TRG1`
* **Alternate Manufacturer**: Texas Instruments
* **Alternate MPN**: `TLV1117-33IDCYR` (SOT-223, 800 mA, 3.3 V fixed)
* **Package / Footprint**: SOT-223-3 (Pitch: 2.30 mm, Large Center Thermal Tab)
* **Subsystem**: Stage 8 (Auxiliary Power Tree: +3.3V High-Precision Supervisory Rail)

## 2. Electrical Ratings & Constraints
* **Input Voltage Range ($V_{\text{IN}}$)**: $+3.8\,\text{V}$ to $+6.0\,\text{V}_{\text{DC}}$ (Maximum rating: $+6.5\,\text{V}$)
  * Operating input: $+5.0\,\text{V}_{\text{DC}} \pm 4\%$ from `U8_REG`.
  * Voltage Stress Derating: $\frac{5.0\,\text{V}}{6.5\,\text{V}} = \mathbf{76.9\%}$ (Well within transient margins).
* **Nominal Output Voltage ($V_{\text{OUT}}$)**: $+3.300\,\text{V}_{\text{DC}} \pm 1.0\%$ across $-40^\circ\text{C}$ to $+85^\circ\text{C}$.
* **Dropout Voltage ($V_{\text{drop}}$)**: $240\,\text{mV}$ typical at $1.0\,\text{A}$ ($< 50\,\text{mV}$ at $65\,\text{mA}$).
  * Headroom: $5.0\,\text{V} - 3.3\,\text{V} = 1.70\,\text{V} \gg 0.24\,\text{V}$ (Guarantees perfect regulation without dropout!).
* **Maximum Output Current Rating**: $1.0\,\text{A}_{\text{DC}}$ continuous.
  * Operating load current:
    * STM32G474RET6 MCU Core: $\approx 42.0\,\text{mA}$
    * INA226 Power Monitor: $\approx 0.33\,\text{mA}$
    * INA240 Current Sense Amp: $\approx 1.80\,\text{mA}$
    * TLV3501 Ultra-Fast Comparator: $\approx 3.20\,\text{mA}$
    * AMC1311 Isolated Amp Low-Side: $\approx 5.50\,\text{mA}$
    * Pull-ups and status logic: $\approx 12.0\,\text{mA}$
    * Total Load Current: $I_{\text{load,3V3}} \approx \mathbf{64.83\,\text{mA}} \quad (\text{Peak: } 85\,\text{mA})$
  * Current Derating: $\frac{64.83\,\text{mA}}{1000\,\text{mA}} = \mathbf{6.48\%} \ll 70\%$ (Massive headroom).
* **Power Dissipation & Thermal Stress**:
  $$P_{\text{loss,U9}} = (V_{\text{IN}} - V_{\text{OUT}}) \times I_{\text{load}} = (5.0\,\text{V} - 3.3\,\text{V}) \times (0.065\,\text{A}) = \mathbf{0.110\,\text{W}} \quad (110.5\,\text{mW})$$
  * Thermal resistance $\theta_{\text{JA}}$ (SOT-223 on PCB with thermal pad): $\approx 65^\circ\text{C/W}$.
  * Junction temperature rise:
    $$\Delta T_j = 0.1105\,\text{W} \times 65^\circ\text{C/W} = \mathbf{7.18^\circ\text{C}}$$
  * At $50^\circ\text{C}$ ambient: $T_j = 50 + 7.2 = \mathbf{57.2^\circ\text{C}} \ll 110.0^\circ\text{C}$ (PASS).
* **Power Supply Rejection Ratio (PSRR)**: $> 65\,\text{dB}$ at $100\,\text{kHz}$, providing ultra-clean, noise-free DC power for sensitive 12-bit ADC and DAC analog reference rails.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`GND`** | `GND_SELV` | Secondary ground plane (Layer 2) | Direct connection to ground plane. |
| **2** | **`OUT`** | `+3V3_SEC` | Ceramic caps $C_{\text{OUT,3V3}} = 2x\ 4.7\,\mu\text{F} / 10\,\text{V}$, MCU, sensors | Low-inductance power polygon ($w \ge 2.0\,\text{mm}$). |
| **3** | **`IN`**  | `+5V_SEC` | Ceramic cap $C_{\text{IN,3V3}} = 4.7\,\mu\text{F} / 16\,\text{V}$, `U8_REG` OUT | $1.5\,\text{mm}$ trace width. |
| **TAB**| **`OUT`**| `+3V3_SEC` | Large copper polygon pour on Layer 1 | Connected internally to Pin 2 (`OUT`). |

## 4. Schematic Symbol Representation
```
                    [ U9_REG: AP2114H-3.3TRG1 1.0A LDO REGULATOR ]
                                  SOT-223 Package
                                  ┌───────────────┐
          Net: +5V_SEC  ─────────[3] IN       OUT[2]───────── Net: +3V3_SEC
                                  │      GND      │
                                  └───────┬───────┘
                                         [1]
                                          │
                                    Net: GND_SELV
```

## 5. Schematic & PCB Layout Guidelines
1. **Stability MLCC**: AP2114 requires low-ESR ceramic output capacitors for stable loop operation. Place two $4.7\,\mu\text{F} / 10\,\text{V}$ X7R 0805 MLCCs within $2.0\,\text{mm}$ of Pin 2 and the GND return.
2. **Tab Solder Pour**: Pin 2 and the large Tab are connected internally to the `OUT` node (`+3V3_SEC`). Flood the tab with a heavy copper polygon pour ($8 \times 8\,\text{mm}$) to minimize impedance and conduct heat away from the die.
""")

    # 4. Module 8 Equivalent Circuit Document
    with open(OUT_DIR / "module_08_auxiliary_power_equivalent_circuit.md", "w") as f:
        f.write(r"""# Module 8 Equivalent Electronic Circuit: Auxiliary Power Distribution Subsystem

## 1. Subsystem Architecture Overview
Module 8 establishes the multi-rail auxiliary power distribution tree that energizes all low-voltage active circuitry on the secondary isolated side of the SPPS board. 

Rather than deploying noisy secondary buck switchers that radiate electromagnetic interference directly into sensitive analog measurement paths, the design employs a **cascaded linear regulator topology** fed by the pre-regulated $+24.0\,\text{V}_{\text{DC}}$ intermediate bus. The cascaded structure optimally divides thermal dissipation across three stages:
1. **Stage A (+12V Gate Bias Rail)**: Regulated by STMicroelectronics **`L78L12ACUTR`** (`U7_REG`) stepping down $+24.0\,\text{V}$ to $+12.0\,\text{V}_{\text{DC}}$. Directly supplies the `BIAS` input (Pin 22) of the LM5176 buck-boost controller, offloading internal LDO thermal dissipation and providing high gate-drive peak current ($2.0\,\text{A}$).
2. **Stage B (+5V Display & Intermediate Rail)**: Regulated by STMicroelectronics **`L78L05ABUTR`** (`U8_REG`) stepping down $+12.0\,\text{V}$ to $+5.0\,\text{V}_{\text{DC}}$. Powers the external $1.3\text{"}$ monochrome OLED display module logic and feeds the downstream 3.3V LDO.
3. **Stage C (+3.3V Precision Supervisory Rail)**: Regulated by Diodes Incorporated **`AP2114H-3.3TRG1`** (`U9_REG`) stepping down $+5.0\,\text{V}$ to ultra-clean $+3.300\,\text{V}_{\text{DC}} \pm 1.0\%$. Powers the STM32G474RET6 MCU, INA226 power monitor, INA240 current amplifier, TLV3501 comparator, and AMC1311 secondary domain.

---

## 2. Full Schematic Electronic Circuit Diagram

```
========================================================================================================================
MODULE 8: CASCADED LINEAR AUXILIARY POWER TREE (+24V -> +12V -> +5V -> +3.3V)
========================================================================================================================

    FROM STAGE 3
    (+24V INTERMEDIATE BUS)
        │
        ├── Net: +24V_SEC
        │         │
        │      ┌──┴──┐
        │      │     │ C_IN_12V (1.0µF / 50V X7R 0805)
        │      └──┬──┘
        │         │
        │     GND_SELV
        │         │
        │         │     [ U7_REG: L78L12ACUTR (+12V REGULATOR) ]
        │         │       SOT-89 Package (Pd = 0.30 W, Tj = 74°C)
        │         │       ┌───────────────┐
        │         └───────┤[3] IN  OUT [1]├──┬── Net: +12V_AUX (Powers LM5176 BIAS Pin 22)
        │                 │      GND      │  │
        │                 └───────┬───────┘  ├──[ C_OUT_12V: 1.0µF / 25V X7R ]── GND_SELV
        │                        [2] (Tab)   │
        │                         │          │
        │                     GND_SELV       │
        │                                    │
        │                                    ▼
        │                         [ U8_REG: L78L05ABUTR (+5V REGULATOR) ]
        │                           SOT-89 Package (Pd = 0.28 W, Tj = 72.4°C)
        │                           ┌───────────────┐
        │                           ┤[3] IN  OUT [1]├──┬── Net: +5V_SEC (Powers 1.3" OLED Display)
        │                           │      GND      │  │
        │                           └───────┬───────┘  ├──[ C_OUT_5V: 1.0µF / 16V X7R ]── GND_SELV
        │                                  [2] (Tab)   │
        │                                   │          │
        │                               GND_SELV       │
        │                                              │
        │                                              ▼
        │                                   [ U9_REG: AP2114H-3.3 (+3.3V LDO) ]
        │                                     SOT-223 Package (Pd = 0.11 W, Tj = 57.2°C)
        │                                     ┌───────────────┐
        │                                     ┤[3] IN  OUT [2]├──┬── Net: +3V3_SEC
        │                                     │      GND      │  │   (Powers STM32, INA226, INA240, TLV3501)
        │                                     └───────┬───────┘  ├──[ C_OUT_3V3A: 4.7µF / 10V X7R ]── GND_SELV
        │                                            [1]         ├──[ C_OUT_3V3B: 4.7µF / 10V X7R ]── GND_SELV
        │                                             │          │
        │                                         GND_SELV       ├──[ FB1: BLM18PG121 ]── Net: +3V3A_ANALOG (Pin 13 VDDA)
        │                                                        │                             │
        │                                                        │                          [ 1.0µF + 10nF ]
        │                                                        │                             │
        │                                                        │                          AGND_SEC
```

---

## 3. Power Budget & Thermal Dissipation Breakdown

| Rail Name | Regulator Ref Des | Nominal Voltage | Load Current ($I_{\text{load}}$) | Voltage Drop ($\Delta V$) | Power Dissipation ($P_{\text{loss}}$) | Package | Thermal Resistance ($\theta_{\text{JA}}$) | Temp Rise ($\Delta T_j$) | Junction Temp ($T_j$ at $50^\circ\text{C}$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `+12V_AUX` | `U7_REG` | $+12.0\,\text{V}$ | $25.0\,\text{mA}$ | $12.0\,\text{V}$ | $300.0\,\text{mW}$ | SOT-89 | $80^\circ\text{C/W}$ | $24.0^\circ\text{C}$ | **$74.0^\circ\text{C}$** |
| `+5V_SEC`  | `U8_REG` | $+5.0\,\text{V}$  | $40.0\,\text{mA}$ | $7.0\,\text{V}$  | $280.0\,\text{mW}$ | SOT-89 | $80^\circ\text{C/W}$ | $22.4^\circ\text{C}$ | **$72.4^\circ\text{C}$** |
| `+3V3_SEC` | `U9_REG` | $+3.30\,\text{V}$ | $65.0\,\text{mA}$ | $1.70\,\text{V}$ | $110.5\,\text{mW}$ | SOT-223| $65^\circ\text{C/W}$ | $7.2^\circ\text{C}$  | **$57.2^\circ\text{C}$** |
| **TOTAL**  | — | — | — | — | **$690.5\,\text{mW}$** | — | — | — | **PASS ($\ll 110^\circ\text{C}$)** |

---

## 4. Module 8 Comprehensive Netlist

| Net Name | Origin Pin / Pad | Destination Pins / Pads | Net Class | Physical Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `+24V_SEC` | Secondary LC Filter | `U7_REG` Pin 3 (`IN`), Cap $C_{\text{IN,12V}}$ | Power Input | Copper polygon $w \ge 1.5\,\text{mm}$ |
| `+12V_AUX` | `U7_REG` Pin 1 (`OUT`) | `U3` LM5176 Pin 22 (`BIAS`), `U8_REG` Pin 3 (`IN`), Cap $C_{\text{OUT,12V}}$ | Auxiliary Rail | Trace width $1.0\,\text{mm}$ |
| `+5V_SEC`  | `U8_REG` Pin 1 (`OUT`) | OLED Header Pin 1, `U9_REG` Pin 3 (`IN`), Cap $C_{\text{OUT,5V}}$ | Auxiliary Rail | Trace width $1.0\,\text{mm}$ |
| `+3V3_SEC` | `U9_REG` Pin 2/Tab | STM32 VDD Pins, INA226, INA240, TLV3501, Ferrite Bead `FB1` | Main Logic Rail| Low-inductance power polygon $w \ge 2.0\,\text{mm}$ |
| `+3V3A_ANALOG`| Ferrite Bead `FB1` Pin 2| STM32 Pin 13 (`VDDA`), Caps $1\,\mu\text{F} + 10\,\text{nF}$ | Precision Analog | Star-routed analog supply trace |
| `GND_SELV` | Secondary Ground Plane | Pins 2/Tab of `U7_REG`, `U8_REG`, Pin 1 of `U9_REG` | Ground Plane | Continuous Layer 2 ground plane |
| `AGND_SEC` | Star Point at `U3` | Ground pins of analog bypass caps, STM32 Pin 12 (`VSSA`) | Quiet Analog GND | Star-point single connection |

---

## 5. Laboratory Bring-Up & Test Points
* **`TP_12V` (Gate Bias Rail)**: Verify $+12.0\,\text{V}_{\text{DC}} \pm 4.0\%$ under active switching load ($300\,\text{kHz}$).
* **`TP_5V` (Display Rail)**: Verify $+5.0\,\text{V}_{\text{DC}} \pm 4.0\%$ with OLED operating at maximum brightness.
* **`TP_3V3` (Supervisory LDO Rail)**: Verify $+3.300\,\text{V}_{\text{DC}} \pm 1.0\%$ ($+3.267\,\text{V}$ to $+3.333\,\text{V}$). Peak-to-peak switching noise must measure $< 5.0\,\text{mV}_{\text{pk-pk}}$.
""")

    print("Module 8 files successfully generated.")

if __name__ == "__main__":
    write_files()
