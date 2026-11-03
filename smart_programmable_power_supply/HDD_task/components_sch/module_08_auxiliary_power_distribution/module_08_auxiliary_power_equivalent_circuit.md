# Module 8 Equivalent Electronic Circuit: Auxiliary Power Distribution Subsystem

## 1. Subsystem Architecture Overview
Module 8 establishes the multi-rail auxiliary power distribution tree that energizes all low-voltage active circuitry on the secondary isolated side of the SPPS board. 

Rather than deploying noisy secondary buck switchers that radiate electromagnetic interference directly into sensitive analog measurement paths, the design employs a **cascaded linear regulator topology** fed by the pre-regulated +24.0 V_DC intermediate bus. The cascaded structure optimally divides thermal dissipation across three stages:
1. **Stage A (+12V Gate Bias Rail)**: Regulated by STMicroelectronics **`L78L12ACUTR`** (`U7_REG`) stepping down +24.0 V to +12.0 V_DC. Directly supplies the `BIAS` input (Pin 22) of the LM5176 buck-boost controller, offloading internal LDO thermal dissipation and providing high gate-drive peak current (2.0 A).
2. **Stage B (+5V Display & Intermediate Rail)**: Regulated by STMicroelectronics **`L78L05ABUTR`** (`U8_REG`) stepping down +12.0 V to +5.0 V_DC. Powers the external 1.3" monochrome OLED display module logic and feeds the downstream 3.3V LDO.
3. **Stage C (+3.3V Precision Supervisory Rail)**: Regulated by Diodes Incorporated **`AP2114H-3.3TRG1`** (`U9_REG`) stepping down +5.0 V to ultra-clean +3.300 V_DC ± 1.0%. Powers the STM32G474RET6 MCU, INA226 power monitor, INA240 current amplifier, TLV3501 comparator, and AMC1311 secondary domain.

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
 │ │
 │ ┌──┴──┐
 │ │ │ C_IN_12V (1.0µF / 50V X7R 0805)
 │ └──┬──┘
 │ │
 │ GND_SELV
 │ │
 │ │ [ U7_REG: L78L12ACUTR (+12V REGULATOR) ]
 │ │ SOT-89 Package (Pd = 0.30 W, Tj = 74°C)
 │ │ ┌───────────────┐
 │ └───────┤[3] IN OUT [1]├──┬── Net: +12V_AUX (Powers LM5176 BIAS Pin 22)
 │ │ GND │ │
 │ └───────┬───────┘ ├──[ C_OUT_12V: 1.0µF / 25V X7R ]── GND_SELV
 │ [2] (Tab) │
 │ │ │
 │ GND_SELV │
 │ │
 │ ▼
 │ [ U8_REG: L78L05ABUTR (+5V REGULATOR) ]
 │ SOT-89 Package (Pd = 0.28 W, Tj = 72.4°C)
 │ ┌───────────────┐
 │ ┤[3] IN OUT [1]├──┬── Net: +5V_SEC (Powers 1.3" OLED Display)
 │ │ GND │ │
 │ └───────┬───────┘ ├──[ C_OUT_5V: 1.0µF / 16V X7R ]── GND_SELV
 │ [2] (Tab) │
 │ │ │
 │ GND_SELV │
 │ │
 │ ▼
 │ [ U9_REG: AP2114H-3.3 (+3.3V LDO) ]
 │ SOT-223 Package (Pd = 0.11 W, Tj = 57.2°C)
 │ ┌───────────────┐
 │ ┤[3] IN OUT [2]├──┬── Net: +3V3_SEC
 │ │ GND │ │ (Powers STM32, INA226, INA240, TLV3501)
 │ └───────┬───────┘ ├──[ C_OUT_3V3A: 4.7µF / 10V X7R ]── GND_SELV
 │ [1] ├──[ C_OUT_3V3B: 4.7µF / 10V X7R ]── GND_SELV
 │ │ │
 │ GND_SELV ├──[ FB1: BLM18PG121 ]── Net: +3V3A_ANALOG (Pin 13 VDDA)
 │ │ │
 │ │ [ 1.0µF + 10nF ]
 │ │ │
 │ │ AGND_SEC
```

---

## 3. Power Budget & Thermal Dissipation Breakdown

| Rail Name | Regulator Ref Des | Nominal Voltage | Load Current (I_load) | Voltage Drop (Δ V) | Power Dissipation (P_loss) | Package | Thermal Resistance (θ_JA) | Temp Rise (Δ T_j) | Junction Temp (T_j at 50°C) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `+12V_AUX` | `U7_REG` | +12.0 V | 25.0 mA | 12.0 V | 300.0 mW | SOT-89 | 80°C/W | 24.0°C | **74.0°C** |
| `+5V_SEC` | `U8_REG` | +5.0 V | 40.0 mA | 7.0 V | 280.0 mW | SOT-89 | 80°C/W | 22.4°C | **72.4°C** |
| `+3V3_SEC` | `U9_REG` | +3.30 V | 65.0 mA | 1.70 V | 110.5 mW | SOT-223| 65°C/W | 7.2°C | **57.2°C** |
| **TOTAL** | — | — | — | — | **690.5 mW** | — | — | — | **PASS (<< 110°C)** |

---

## 4. Module 8 Comprehensive Netlist

| Net Name | Origin Pin / Pad | Destination Pins / Pads | Net Class | Physical Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `+24V_SEC` | Secondary LC Filter | `U7_REG` Pin 3 (`IN`), Cap C_IN,12V | Power Input | Copper polygon w ≥ 1.5 mm |
| `+12V_AUX` | `U7_REG` Pin 1 (`OUT`) | `U3` LM5176 Pin 22 (`BIAS`), `U8_REG` Pin 3 (`IN`), Cap C_OUT,12V | Auxiliary Rail | Trace width 1.0 mm |
| `+5V_SEC` | `U8_REG` Pin 1 (`OUT`) | OLED Header Pin 1, `U9_REG` Pin 3 (`IN`), Cap C_OUT,5V | Auxiliary Rail | Trace width 1.0 mm |
| `+3V3_SEC` | `U9_REG` Pin 2/Tab | STM32 VDD Pins, INA226, INA240, TLV3501, Ferrite Bead `FB1` | Main Logic Rail| Low-inductance power polygon w ≥ 2.0 mm |
| `+3V3A_ANALOG`| Ferrite Bead `FB1` Pin 2| STM32 Pin 13 (`VDDA`), Caps 1 µF + 10 nF | Precision Analog | Star-routed analog supply trace |
| `GND_SELV` | Secondary Ground Plane | Pins 2/Tab of `U7_REG`, `U8_REG`, Pin 1 of `U9_REG` | Ground Plane | Continuous Layer 2 ground plane |
| `AGND_SEC` | Star Point at `U3` | Ground pins of analog bypass caps, STM32 Pin 12 (`VSSA`) | Quiet Analog GND | Star-point single connection |

---

## 5. Laboratory Bring-Up & Test Points
* **`TP_12V` (Gate Bias Rail)**: Verify +12.0 V_DC ± 4.0% under active switching load (300 kHz).
* **`TP_5V` (Display Rail)**: Verify +5.0 V_DC ± 4.0% with OLED operating at maximum brightness.
* **`TP_3V3` (Supervisory LDO Rail)**: Verify +3.300 V_DC ± 1.0% (+3.267 V to +3.333 V). Peak-to-peak switching noise must measure < 5.0 mV_pk-pk.
