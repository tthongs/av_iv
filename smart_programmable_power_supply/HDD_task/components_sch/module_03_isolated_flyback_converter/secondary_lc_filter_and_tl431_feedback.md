# Component Schematic Specification: Secondary Filter & Closed-Loop Feedback (C_SEC, L_post, TL431, OPTO1)

## 1. Component Metadata
* **Reference Designators**:
 * `C_SEC1, 2`: Secondary Bulk Electrolytic Capacitors (Panasonic `EEU-FC1V471`, 2x 470 µF / 35 V, 35 mΩ ESR, 105°C)
 * `L_post`: Secondary LC Post-Filter Choke (Bourns `2100LL-2R2-H-RC`, 2.20 µH ± 20%, 5.0 A_RMS, 18 mΩ DCR)
 * `C_SEC_CER`: Secondary Decoupling MLCCs (Murata `GRM32ER71H106K`, 2x 10.0 µF / 50 V X7R 1210)
 * `U2`: Precision Shunt Reference (Texas Instruments `TL431ACDBZR`, 2.495 V ± 0.5%, SOT-23-3)
 * `OPTO1`: Reinforced Galvanic Optocoupler (Everlight `EL817(S)(TA)`, 5000 V_RMS isolation, CTR 100% - 200%, SMD-4)
* **Subsystem**: Stage 3 (Isolated Flyback Subsystem)

## 2. Electrical Ratings & Constraints
* **Intermediate Rail Output**: +24.0 V_DC ± 1.0% continuous (72.0 W rated throughput)
* **Output LC Filter Ripple Attenuation**:
 * Corner Frequency: f_c = (1 / 2π sqrt{L_post × C_cer}) = (1 / 2π √(2.2 µH × 20 µF) ≈ 24.0 kHz
 * Output voltage ripple on +24 V bus is attenuated to < 35.0 mV_pk-pk.
* **TL431 Feedback Voltage Divider Sizing**:
 * Reference Bandgap: V_REF = 2.495 V_DC
 * Top Resistor: R_FB1 = 86.6 kΩ ± 0.1%
 * Bottom Resistor: R_FB2 = 10.0 kΩ ± 0.1%
 * Regulated Output Voltage:
 V_bus = V_REF × (1 + (R_FB1 / R_FB2) = 2.495 V × (1 + (86.6 kΩ / 10.0 kΩ) = 2.495 × 9.66 = mathbf{24.10 V_DC ± 0.8%}

## 3. Schematic Pin Connections & Net Mapping
```
 Net: +24V_UNFILT L_post: 2.2µH Net: +24V_BUS
 ───────────────────┬──────────────●═══[ 2.2µH ]═══─────────┬───────────────────────────────> To Stage 4
 │ │
 ┌─┴─┐ C_SEC1/2 ┌─┴─┐ C_SEC_CER
 │ + │ 2x 470µF/35V │ │ 2x 10µF/50V
 └───┘ Panasonic FC └─┬─┘ Murata 1210
 │ │
 ───────────────────┴───────────────────────────────────────┴───────────────────────────────> Net: PGND_SEC
 │
 ┌─┴─┐ R_LED: 1.5kΩ
 │ │
 └─┬─┘
 │
 [1] Anode [4] Collector ─── Net: FLY_COMP (To U1 Pin 1)
 ┌───────────────┐
 │ OPTO1: EL817 │ Reinforced Galvanic Isolation (5000 V RMS)
 │ [2] Cathode │ [3] Emitter ─── Net: PGND_HOT (Primary Hot Ground)
 └───────┬───────┘
 │
 ├─── Net: TL431_CATHODE
 │
 ┌─┴─┐
 │ │ Cathode
 │ │ TL431ACDBZR
 │ │ Ref [1] ─── Net: TL431_REF (From 86.6k / 10k divider)
 └─┬─┘
 │ Anode [2]
 │
 Net: PGND_SEC
```

| Ref Des | Pin # | Pin Name | Schematic Net Name | Connected To | Functional Role |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **`OPTO1`** | **1** | Anode | `OPTO_ANODE` | +24 V rail via 1.5 kΩ bias resistor | Infrared emitter input. |
| **`OPTO1`** | **2** | Cathode | `TL431_CATHODE` | `U2` TL431 Cathode (Pin 3) | Modulated by error amplifier. |
| **`OPTO1`** | **3** | Emitter | `PGND_HOT` | Primary hot power ground plane | Phototransistor return. |
| **`OPTO1`** | **4** | Collector | `FLY_COMP` | `U1` Flyback controller `COMP` (Pin 1) | Pulls COMP down on overvoltage. |
| **`U2`** | **1** | Reference | `TL431_REF` | Divider node of 86.6 kΩ / 10.0 kΩ | 2.495 V reference comparison. |
| **`U2`** | **2** | Anode | `PGND_SEC` | Secondary touch-safe ground plane | Shunt regulator ground reference. |
| **`U2`** | **3** | Cathode | `TL431_CATHODE` | Optocoupler `OPTO1` Cathode (Pin 2) | Sinks current when bus > 24.0 V. |

## 4. Schematic & PCB Layout Guidelines
1. **Milled Slot Beneath Optocoupler**: Ensure the 2.0 mm milled PCB air slot passes directly beneath `OPTO1` between primary pins (3-4) and secondary pins (1-2) to maintain ≥ 6.4 mm creepage.
