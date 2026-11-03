# Component Schematic Specification: COMP_NET (Type-II Loop Compensation Network)

## 1. Component Metadata
* **Reference Designators**: `R_comp`, `C_comp`, `C_comp2`
* **Component Type**: Precision Type-II Analog Loop Compensation Network
* **Values**:
 * `R_comp`: 12.4 kΩ ± 1%, 0603 SMD, Vishay Dale `CRCW060312K4FKEA`
 * `C_comp`: 82.0 nF ± 5%, 50 V, X7R, 0603 SMD, Murata `GRM188R71H823JA93D`
 * `C_comp2`: 15.0 pF ± 5%, 50 V, C0G/NP0, 0603 SMD, Murata `GRM1885C1H150JA01D`
* **Subsystem**: Stage 4 (LM5176 Closed-Loop Stability & Transient Response Engine)

## 2. Electrical Ratings & Constraints
* **Transconductance of Error Amplifier (g_m)**: 1200 µS (1.2 mA/V)
* **Target Loop Crossover Frequency (f_c)**: 25.0 kHz (f_c ≈ (f_sw / 12)
* **Target Phase Margin**: 65.0° across entire 5.0 V to 20.0 V output span under 0.0 A to 3.0 A load.
* **Gain Margin**: ≥ 14.5 dB at 150 kHz Nyquist frequency.
* **Pole-Zero Placement**:
 * **Zero 1 (f_z1)**: Placed to cancel output capacitor dominant load pole at lowest load:
 f_z1 = (1 / 2π × R_comp × C_comp) = (1 / 2π × (12.4 kΩ) × (82 nF) = 156.5 Hz
 * **High-Frequency Pole 2 (f_p2)**: Cancels output capacitor ESR zero and suppresses high-frequency switching ripple injection into the PWM comparator:
 f_p2 = (1 / 2π × R_comp × C_comp2) = (1 / 2π × (12.4 kΩ) × (15 pF) = 855.6 kHz

## 3. Schematic Pin Connections & Net Mapping
| Component | Pin 1 Net | Pin 2 Net | Description & Connection |
| :---: | :--- | :--- | :--- |
| **`R_comp`** | `LM5176_COMP` | `COMP_SERIES_MID` | In series with `C_comp` between Pin 6 and `AGND_SEC`. |
| **`C_comp`** | `COMP_SERIES_MID` | `AGND_SEC` | In series with `R_comp` to set zero f_z1. |
| **`C_comp2`** | `LM5176_COMP` | `AGND_SEC` | Connected directly from Pin 6 to `AGND_SEC` to set pole f_p2. |

## 4. Schematic Symbol Representation
```
 [ LM5176 TYPE-II LOOP COMPENSATION NETWORK ]
 Net: LM5176_COMP (Pin 6)
 ├───┬────────────────┐
 │ │ │
 ┌─┴─┐ │ ┌─┴─┐
 R_comp (12.4 kΩ) │ │ │ C_comp2 │ │ Q_CLAMP
 └─┬─┘ │ (15 pF) │ │ (MMBT3904)
 │ │ └─┬─┘
 ┌─┴─┐ │ │
 C_comp (82 nF) │ │ │ │
 └──┬┘ │ │
 ├──┴────────────────┘
 │
 Net: AGND_SEC
```

## 5. Schematic & PCB Layout Guidelines
1. **Proximity**: Keep all three compensation components within 4.0 mm of `U3` Pin 6 (`COMP`).
2. **Ground Return**: Return the ground pins of `C_comp` and `C_comp2` directly to the `AGND` pin (Pin 11) of `U3` before connecting to the main secondary ground plane.
