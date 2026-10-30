# Component Schematic Specification: R_T (LM5176 Frequency Program Resistor)

## 1. Component Metadata
* **Reference Designator**: `R_T`
* **Component Type**: Precision Thick-Film SMD Resistor (1% Tolerance)
* **Manufacturer**: Vishay Dale
* **Primary MPN**: `CRCW060324K9FKEA`
* **Alternate Manufacturer**: Panasonic Electronic Components
* **Alternate MPN**: `ERJ-3EKF2492V` (24.9 kΩ, 1%, 0603)
* **Package / Footprint**: SMD 0603 Metric ($1.6 \times 0.8\,\text{mm}$)
* **Subsystem**: Stage 4 (LM5176 Timing & Clock Generator)

## 2. Electrical Ratings & Constraints
* **Resistance Value ($R$)**: $24.9\,\text{k}\Omega \pm 1.0\%$
* **Power Rating ($P_{\text{rated}}$)**: $0.10\,\text{W}$ ($100\,\text{mW}$)
* **Programmed Switching Frequency ($f_{\text{sw}}$)**:
  According to the LM5176 datasheet programming equation:
  $$f_{\text{sw}} [\text{kHz}] = \frac{7450}{R_T [\text{k}\Omega]} + 1 \approx \frac{7450}{24.9} = \mathbf{299.2\,\text{kHz}} \approx \mathbf{300.0\,\text{kHz}}$$
* **Frequency Accuracy**: $\pm 5.0\%$ across $-40^\circ\text{C}$ to $+125^\circ\text{C}$ operating range.
* **Pin Voltage**: $V_{\text{RT}} \approx 1.20\,\text{V}_{\text{DC}}$ generated internally by LM5176.
  * Operating current: $I_{\text{RT}} = \frac{1.20\,\text{V}}{24.9\,\text{k}\Omega} = 48.2\,\mu\text{A}$
  * Power dissipation: $P_{\text{RT}} = (48.2\,\mu\text{A})^2 \times 24.9\,\text{k}\Omega = \mathbf{57.8\,\mu\text{W}}$ (Practically zero dissipation).

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Schematic Net Name | Connected To | Trace & Solder Requirements |
| :---: | :--- | :--- | :--- |
| **1** | `LM5176_RT` | `U3` Pin 8 (`RT`) | Direct trace $< 2.0\,\text{mm}$ length. |
| **2** | `AGND_SEC` | `U3` Pin 11 (`AGND`) | Direct connection to quiet analog ground. |

## 4. Schematic Symbol Representation
```
                    [ R_T: 24.9 kΩ ±1% FREQUENCY PROGRAM ]
                               ┌─────────────┐
        Net: LM5176_RT  ───────┤1   24.9k   2├─────── Net: AGND_SEC
                               └─────────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Clock Jitter Suppression**: Place `R_T` directly against Pin 8 of `U3`. Never route noisy clock, switch node, or gate drive signals underneath or adjacent to the `LM5176_RT` trace, as stray capacitive coupling will modulate the PWM oscillator and cause phase jitter.
