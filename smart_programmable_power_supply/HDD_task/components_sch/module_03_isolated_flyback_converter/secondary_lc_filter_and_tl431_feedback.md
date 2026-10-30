# Component Schematic Specification: Secondary Filter & Closed-Loop Feedback (C_SEC, L_post, TL431, OPTO1)

## 1. Component Metadata
* **Reference Designators**:
  * `C_SEC1, 2`: Secondary Bulk Electrolytic Capacitors (Panasonic `EEU-FC1V471`, 2x $470\,\mu\text{F} / 35\,\text{V}$, $35\,\text{m}\Omega$ ESR, $105^\circ\text{C}$)
  * `L_post`: Secondary LC Post-Filter Choke (Bourns `2100LL-2R2-H-RC`, $2.20\,\mu\text{H} \pm 20\%$, $5.0\,\text{A}_{\text{RMS}}$, $18\,\text{m}\Omega$ DCR)
  * `C_SEC_CER`: Secondary Decoupling MLCCs (Murata `GRM32ER71H106K`, 2x $10.0\,\mu\text{F} / 50\,\text{V}$ X7R 1210)
  * `U2`: Precision Shunt Reference (Texas Instruments `TL431ACDBZR`, $2.495\,\text{V} \pm 0.5\%$, SOT-23-3)
  * `OPTO1`: Reinforced Galvanic Optocoupler (Everlight `EL817(S)(TA)`, $5000\,\text{V}_{\text{RMS}}$ isolation, CTR $100\% - 200\%$, SMD-4)
* **Subsystem**: Stage 3 (Isolated Flyback Subsystem)

## 2. Electrical Ratings & Constraints
* **Intermediate Rail Output**: $+24.0\,\text{V}_{\text{DC}} \pm 1.0\%$ continuous ($72.0\,\text{W}$ rated throughput)
* **Output LC Filter Ripple Attenuation**:
  * Corner Frequency: $f_c = \frac{1}{2\pi \sqrt{L_{\text{post}} \times C_{\text{cer}}}} = \frac{1}{2\pi \sqrt{2.2\,\mu\text{H} \times 20\,\mu\text{F}}} \approx \mathbf{24.0\,\text{kHz}}$
  * Output voltage ripple on $+24\,\text{V}$ bus is attenuated to $< 35.0\,\text{mV}_{\text{pk-pk}}$.
* **TL431 Feedback Voltage Divider Sizing**:
  * Reference Bandgap: $V_{\text{REF}} = 2.495\,\text{V}_{\text{DC}}$
  * Top Resistor: $R_{\text{FB1}} = 86.6\,\text{k}\Omega \pm 0.1\%$
  * Bottom Resistor: $R_{\text{FB2}} = 10.0\,\text{k}\Omega \pm 0.1\%$
  * Regulated Output Voltage:
    $$V_{\text{bus}} = V_{\text{REF}} \times \left( 1 + \frac{R_{\text{FB1}}}{R_{\text{FB2}}} \right) = 2.495\,\text{V} \times \left( 1 + \frac{86.6\,\text{k}\Omega}{10.0\,\text{k}\Omega} \right) = 2.495 \times 9.66 = \mathbf{24.10\,\text{V}_{\text{DC}} \pm 0.8\%}$$

## 3. Schematic Pin Connections & Net Mapping
```
   Net: +24V_UNFILT                 L_post: 2.2µH                 Net: +24V_BUS
  ───────────────────┬──────────────●═══[ 2.2µH ]═══─────────┬───────────────────────────────> To Stage 4
                     │                                       │
                   ┌─┴─┐ C_SEC1/2                          ┌─┴─┐ C_SEC_CER
                   │ + │ 2x 470µF/35V                      │   │ 2x 10µF/50V
                   └───┘ Panasonic FC                      └─┬─┘ Murata 1210
                     │                                       │
  ───────────────────┴───────────────────────────────────────┴───────────────────────────────> Net: PGND_SEC
                     │
                   ┌─┴─┐ R_LED: 1.5kΩ
                   │   │
                   └─┬─┘
                     │
                    [1] Anode        [4] Collector ─── Net: FLY_COMP (To U1 Pin 1)
                   ┌───────────────┐
                   │  OPTO1: EL817 │   Reinforced Galvanic Isolation (5000 V RMS)
                   │  [2] Cathode  │ [3] Emitter   ─── Net: PGND_HOT (Primary Hot Ground)
                   └───────┬───────┘
                           │
                           ├─── Net: TL431_CATHODE
                           │
                         ┌─┴─┐
                         │   │ Cathode
                         │   │ TL431ACDBZR
                         │   │ Ref [1] ─── Net: TL431_REF (From 86.6k / 10k divider)
                         └─┬─┘
                           │ Anode [2]
                           │
                   Net: PGND_SEC
```

| Ref Des | Pin # | Pin Name | Schematic Net Name | Connected To | Functional Role |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **`OPTO1`** | **1** | Anode | `OPTO_ANODE` | $+24\,\text{V}$ rail via $1.5\,\text{k}\Omega$ bias resistor | Infrared emitter input. |
| **`OPTO1`** | **2** | Cathode | `TL431_CATHODE` | `U2` TL431 Cathode (Pin 3) | Modulated by error amplifier. |
| **`OPTO1`** | **3** | Emitter | `PGND_HOT` | Primary hot power ground plane | Phototransistor return. |
| **`OPTO1`** | **4** | Collector | `FLY_COMP` | `U1` Flyback controller `COMP` (Pin 1) | Pulls COMP down on overvoltage. |
| **`U2`** | **1** | Reference | `TL431_REF` | Divider node of $86.6\,\text{k}\Omega$ / $10.0\,\text{k}\Omega$ | $2.495\,\text{V}$ reference comparison. |
| **`U2`** | **2** | Anode | `PGND_SEC` | Secondary touch-safe ground plane | Shunt regulator ground reference. |
| **`U2`** | **3** | Cathode | `TL431_CATHODE` | Optocoupler `OPTO1` Cathode (Pin 2) | Sinks current when bus $> 24.0\,\text{V}$. |

## 4. Schematic & PCB Layout Guidelines
1. **Milled Slot Beneath Optocoupler**: Ensure the $2.0\,\text{mm}$ milled PCB air slot passes directly beneath `OPTO1` between primary pins (3-4) and secondary pins (1-2) to maintain $\ge 6.4\,\text{mm}$ creepage.
