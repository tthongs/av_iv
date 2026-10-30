# Module 2: Bridge Rectifier & High-Voltage Bulk DC — Equivalent Electronic Circuit

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
