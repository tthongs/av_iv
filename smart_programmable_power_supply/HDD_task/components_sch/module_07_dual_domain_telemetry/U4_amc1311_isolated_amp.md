# Component Schematic Specification: U4 (AMC1311BDWVR Reinforced Isolated Amplifier)

## 1. Component Metadata
* **Reference Designator**: `U4`
* **Component Type**: High-Impedance 2-V Input Reinforced Galvanically Isolated Amplifier
* **Manufacturer**: Texas Instruments
* **Primary MPN**: `AMC1311BDWVR`
* **Alternate Manufacturer**: Silicon Laboratories
* **Alternate MPN**: `Si8920BD-IS` (Wide SOIC-8, reinforced isolated amplifier)
* **Package / Footprint**: SOIC-8 Wide-Body (Pitch: 1.27 mm, Body: 5.85 mm creepage, Clearance: 8.0 mm)
* **Subsystem**: Stage 7 (Primary AC Mains Isolated Voltage Telemetry)

## 2. Electrical Ratings & Constraints
* **Galvanic Isolation Rating**:
  * Reinforced Working Insulation: $V_{\text{IOWM}} = 1500\,\text{V}_{\text{RMS}}$ ($2121\,\text{V}_{\text{peak}}$).
  * Reinforced Withstand Voltage ($V_{\text{ISO}}$): $\mathbf{7000\,\text{V}_{\text{peak}}} / \mathbf{5000\,\text{V}_{\text{RMS}}}$ for 1 minute (IEC 62368-1).
  * Common-Mode Transient Immunity (CMTI): $> 75.0\,\text{kV}/\mu\text{s}$ (immune to flyback and buck-boost switching noise).
* **Linear Input Voltage Range ($V_{\text{IN}}$)**: $0.0\,\text{V}$ to $+2.000\,\text{V}_{\text{DC}}$ (Unipolar input, optimized for divided DC bulk / rectified AC).
* **Input Impedance ($R_{\text{IN}}$)**: $> 1.0\,\text{G}\Omega$ (negligible loading on high-voltage divider).
* **Voltage Gain ($A_v$)**: $\mathbf{1.000\,\text{V/V}} \pm 0.20\%$ maximum gain error.
* **Nonlinearity**: $< 0.03\%$ full scale.
* **Bandwidth ($-3\,\text{dB}$)**: $220.0\,\text{kHz}$.
* **High-Side Supply ($V_{\text{DD1}}$)**: $+3.0\,\text{V}$ to $+5.5\,\text{V}_{\text{DC}}$ (Powered from isolated Flyback aux bias rail).
* **Low-Side Supply ($V_{\text{DD2}}$)**: $+3.0\,\text{V}$ to $+5.5\,\text{V}_{\text{DC}}$ (Powered from secondary $+3.30\,\text{V}_{\text{DC}}$ LDO rail).
* **Differential Output Stage**:
  * Emits differential signal $V_{\text{OUTP}} - V_{\text{OUTN}}$ with DC common-mode midpoint $V_{\text{CM,out}} = 1.44\,\text{V}_{\text{DC}}$.
  * A single-supply low-pass differential-to-single-ended operational amplifier circuit scales and filters the signal to feed STM32 ADC input `PC0`.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Isolation Domain | Description & Connection |
| :---: | :---: | :--- | :---: | :--- |
| **1** | **`VDD1`** | `+5V_HOT_ISO` | Primary (HOT) | High-side isolated supply rail; $100\,\text{nF}$ bypass cap. |
| **2** | **`INP`**  | `MAINS_DIV_SENSE` | Primary (HOT) | Tapped from high-voltage divider $1.5\,\text{M}\Omega / 7.5\,\text{k}\Omega$. |
| **3** | **`INN`**  | `PGND_HOT` | Primary (HOT) | Negative differential input tied directly to primary hot ground. |
| **4** | **`GND1`** | `PGND_HOT` | Primary (HOT) | High-side power ground reference. |
| **5** | **`GND2`** | `AGND_SEC` | Secondary (SELV)| Low-side secondary quiet analog ground plane. |
| **6** | **`OUTN`** | `AMC_OUT_N` | Secondary (SELV)| Differential negative analog output to differential filter. |
| **7** | **`OUTP`** | `AMC_OUT_P` | Secondary (SELV)| Differential positive analog output to differential filter. |
| **8** | **`VDD2`** | `+3V3_SEC` | Secondary (SELV)| Low-side secondary supply; $100\,\text{nF}$ bypass cap to `AGND_SEC`. |

## 4. Schematic Symbol Representation
```
                    [ U4: AMC1311BDWVR REINFORCED ISOLATED AMP ]
                      PRIMARY DOMAIN (HOT)  │  SECONDARY DOMAIN (SELV)
                                            │
                                ┌───────────┴───────────┐
     Net: +5V_HOT_ISO ─────────[1] VDD1             VDD2[8]───────── Net: +3V3_SEC
   Net: MAINS_DIV_SENSE ───────[2] INP              OUTP[7]───────── Net: AMC_OUT_P
     Net: PGND_HOT    ─────────[3] INN              OUTN[6]───────── Net: AMC_OUT_N
     Net: PGND_HOT    ─────────[4] GND1             GND2[5]───────── Net: AGND_SEC
                                └───────────────────────┘
                                     SOIC-8 Wide-Body
                                (>= 8.0 mm Creepage Across)
```

## 5. Schematic & PCB Layout Guidelines
1. **Creepage Barrier Keepout**: The PCB layout under `U4` must maintain a strict copper keepout zone of $\ge 8.0\,\text{mm}$ across all internal and external copper layers between Primary Hot Ground (`PGND_HOT`) and Secondary SELV Ground (`AGND_SEC`).
2. **Differential Output Filtering**: Route `AMC_OUT_P` and `AMC_OUT_N` as a balanced differential pair to a second-order active Sallen-Key low-pass filter ($f_c = 10.0\,\text{kHz}$) placed on the secondary side before feeding STM32 pin `PC0`.
