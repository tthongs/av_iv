# Module 2: Bridge Rectifier & High-Voltage Bulk DC — Equivalent Electronic Circuit

## 1. Subsystem Architectural Overview
Module 2 accepts the filtered universal AC mains voltage (85 V - 265 V_AC RMS) from Module 1, performs full-wave bridge rectification, and filters the pulsating sinusoidal waveform into an unregulated high-voltage DC bus link spanning **+120.0 V to +375.0 V_DC**. It guarantees continuous power holdup (> 50 ms) across grid dropouts and incorporates an autonomous safety bleeder discharge network.

## 2. Full Schematic-Level Equivalent Electronic Circuit Diagram

```
 [ MODULE 2: RECTIFICATION & HIGH-VOLTAGE BULK DC LINK ]
=============================================================================================================================

 From Module 1
 Filtered AC Input
 ────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │
 Net: AC_LINE_FILT ─────────────────────────────────┐ │
 (From L_CM2 Pin 2) │ │
 ┌─────────┴─────────┐ │
 │ BR1: GBU606 │ │
 │ 600V, 6.0A │ │
 │ [2] ~ + [1]├──────────────────────┬───────────┬───────────┴──────────┐
 │ │ │ │ │
 Net: AC_NEUTRAL_FILT ────────────────────┤ [3] ~ - [4]├──────────┐ │ │ │
 (From L_CM2 Pin 3) └─────────┬─────────┘ │ ┌─┴─┐ ┌─┴─┐ ┌─┴─┐
 │ │ │ + │ │ │ C_HF │ │ R_BL1
 ▼ │ │ │ │ │ 100nF / 630V │ │ 100kΩ
 Internal Diodes │ │ │ │ │ Murata 1812 └─┬─┘ 1206
 Full-Wave Bridge │ │ │ └─┬─┘ (High-Freq Bypass) │
 │ │ │ C_BULK1 │ ┌─┴─┐
 │ │ │ 100µF │ │ │ R_BL2
 │ │ │ 450V DC │ │ │ 100kΩ
 │ │ │ Nichicon│ └─┬─┘ 1206
 │ │ - │ Snap-In │ │
 │ └─┬─┘ │ ┌─┴─┐
 │ │ │ │ │ R_BL3
 │ │ │ │ │ 100kΩ
 │ │ │ └─┬─┘ 1206
 │ │ │ │
 Net: PGND_HOT (Primary Hot Power Ground) ───────────────────────────────┴───────────┴───────────┴──────────────────────┴──────>
 Net: +HV_BULK (+120V to +375V DC Bus Link) ───────────────────────────────────────────────────────────────────────────────────>
 (To Transformer TX1 Primary Pin 1, Snubber Network, and AMC1311 Voltage Sensing Divider)

=============================================================================================================================
```

## 3. Subsystem Netlist & Interconnect Table
| Net Name | Origin Pin | Destination Pins | Nominal Voltage / Current | Functional Description |
| :--- | :--- | :--- | :---: | :--- |
| `AC_LINE_FILT` | `L_CM2` (Pin 2) | `BR1` (Pin 2 `~`) | 85 - 265 V_AC / 1.60 A_RMS | Filtered AC mains Live feed. |
| `AC_NEUTRAL_FILT`| `L_CM2` (Pin 3) | `BR1` (Pin 3 `~`) | 0 V_AC Nominal / 1.60 A_RMS | Filtered AC mains Neutral feed. |
| `+HV_BULK` | `BR1` (Pin 1 `+`) | `C_BULK1` (+), `C_HF` (Pin 1), `R_BL1` (Pin 1), `TX1` Primary (Pin 1) | +120.0 V - +375.0 V_DC | Main rectified high-voltage DC bus feeding Flyback converter. |
| `PGND_HOT` | `BR1` (Pin 4 `-`) | `C_BULK1` (-), `C_HF` (Pin 2), `R_BL3` (Pin 2), Primary Sense `R_CS` | 0.0 V (Hot Reference) | Primary power ground return, floating at mains rectified potential. |
| `HV_BLEED_DIV1` | `R_BL1` (Pin 2) | `R_BL2` (Pin 1) | +250.0 V_DC Nominal | High-voltage intermediate tap of bleeder string. |
| `HV_BLEED_DIV2` | `R_BL2` (Pin 2) | `R_BL3` (Pin 1) | +125.0 V_DC Nominal | Low-voltage intermediate tap of bleeder string. |

## 4. Theory of Operation & Electrical Derivations
1. **Full-Wave Bridge Rectification**: The AC sinusoidal voltage is rectified by four silicon PIN diodes arranged in a bridge. During positive half-cycles, current conducts through diodes D1 and D4; during negative half-cycles, through D2 and D3. The peak DC output voltage is:
 V_bulk,peak = √(2) × V_AC,RMS - 2 × V_F = 1.4142 × (230 V) - 2 × (0.95 V) = 325.27 - 1.90 = mathbf{323.37 V_DC}
2. **Bulk Capacitive Filtering & 100 Hz Ripple**: Between AC line peaks (t = 10 ms at 50 Hz grid), `C_BULK1` (100 µF) discharges into the Flyback converter (P_in ≈ 81.8 W). The peak-to-peak 100 Hz voltage ripple is:
 Δ V_ripple,100Hz ≈ (I_DC / 2 × f_grid × C_bulk) = (0.252 A / 2 × 50 × 100 × 10^-6) = mathbf{25.2 V_pk-pk}
 At 230 V_AC, the bulk voltage varies between 311 V and 336 V_DC, well within the wide operating window of the Flyback stage (+120 V to +375 V).
3. **High-Frequency Bypassing**: `C_HF` (100 nF / 630 V X7R MLCC) presents an impedance of only Z_C = (1 / 2π × 65000 × 100 × 10^-9) = 24.5 Ω at the switching fundamental, bypassing high-frequency di/dt switching transients directly at the transformer primary pins.

## 5. Laboratory Bring-Up & Test Points
* **`TP_HVBULK` (Bulk DC Bus)**: Measure DC voltage with a high-voltage probe. Verify reading:
 * At 85 V_AC input: +120.2 V_DC ± 3.0 V.
 * At 230 V_AC input: +325.0 V_DC ± 5.0 V.
 * At 265 V_AC input: +374.8 V_DC ± 5.0 V.
* **`TP_PGND` (Primary Hot Ground)**: Primary reference probe ground. Never connect standard grounded oscilloscope ground leads here without an isolation transformer!
* **Safety Bleeder Discharge Check**: Remove AC mains power at 230 V_AC (V_bulk = 325 V). Measure DC bus voltage decay with a DMM: confirm voltage collapses to < 50.0 V_DC in < 45.0 seconds.
