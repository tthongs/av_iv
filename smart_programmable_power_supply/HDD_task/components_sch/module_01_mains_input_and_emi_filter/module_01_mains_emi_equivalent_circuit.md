# Module 1: Mains AC Input Protection & EMI Filter — Equivalent Electronic Circuit

## 1. Subsystem Architectural Overview
Module 1 serves as the frontline power interface connecting the single-phase commercial utility AC mains (85 V - 265 V_ AC RMS, 47 - 63 Hz) to the power supply PCBA. It incorporates multi-layered hardware protection against catastrophic short circuits, inrush transients, and lightning surges, while attenuating conducted electromagnetic emissions to meet **CISPR 32 / EN 55032 Class B** standards.

## 2. Full Schematic-Level Equivalent Electronic Circuit Diagram

```
 [ MODULE 1: MAINS AC INPUT & 2-STAGE EMI FILTER ]
=============================================================================================================================

 J1: IEC C14
 ┌───────────┐ F1: 2.0A Slow-Blow
Live │ Terminal L│─────────[=== 5x20mm ===]─────────┬──────────────┬──────────────●═══════════════════╗ L_CM1: 15mH
85-265V │ │ Littelfuse 0218002.MXP │ │ ║ Winding 1 ║
 │ │ (Melting I²t=19.6A²s) ┌─┴─┐ ┌─┴─┐ ║ ║
 │ │ │ │ │ │ C_X1 ╚═══════════════════●
 │ │ │ │ MOV1 │ │ 0.22µF X2 │
 │ │ │ │ 300V │ │ KEMET R46 ├─── Net: AC_LINE_CM1
 │ │ └─┬─┘ 4.5kA └─┬─┘ 310V AC │
 │ │ │ │ ┌─┴─┐
 │ │ │ │ │ │ C_Y1: 2.2nF Y1
 │ │ │ │ │ │ KEMET PHE850
 │ │ NTC1: 15.0Ω Cold │ │ └─┬─┘ 400V AC
Neutral │ Terminal N│─────────[───////───]─────────┴──────────────┴──────────────● │
0V Nom │ │ EPCOS B57236S0150M ║ ├───── Net: EARTH_GND
 │ │ (Inrush < 24.98A peak) ║ L_CM1 │ (Chassis Earth Stud)
 │ │ ║ Winding 2 ├─────┐
Earth │ Terminal E│────────────────────────────────────────────────────────────────────────────┘ ┌─┴─┐
 └───────────┘ │ │ C_Y2: 2.2nF Y1
 ╚═══════════════● │ KEMET PHE850
 │ └─┬─┘ 400V AC
 │ │
 Net: AC_NEUT_CM1───────┘

 (Continuation into Stage 2 Common Mode Choke L_CM2 & Post-Filter C_X2)
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

 Net: AC_LINE_CM1
 ────────────────────────●═══════════════════╗ L_CM2: 4.7mH
 ║ Winding 1 ║
 ║ ║
 ╚═══════════════════●──────┬───────────────────────────────────────────> Net: AC_LINE_FILT
 │ (To Bridge BR1 Pin 2)
 ┌─┴─┐
 │ │ C_X2
 │ │ 0.22µF X2
 │ │ KEMET R46
 └─┬─┘ 310V AC
 ╔═══════════════════● │
 ║ ║ │
 ║ Winding 2 ║ │
 ────────────────────────●═══════════════════╝──────┴───────────────────────────────────────────> Net: AC_NEUTRAL_FILT
 Net: AC_NEUT_CM1 L_CM2: 4.7mH (To Bridge BR1 Pin 3)

=============================================================================================================================
```

## 3. Subsystem Netlist & Interconnect Table
| Net Name | Origin Pin | Destination Pins | Nominal Voltage / Current | Functional Description |
| :--- | :--- | :--- | :---: | :--- |
| `AC_LINE_IN` | `J1` (Pin L) | `F1` (Input Clip `FC1`) | 85 - 265 V_ AC / 1.60 A_ RMS | Raw grid live entry from IEC socket. |
| `AC_NEUTRAL_IN` | `J1` (Pin N) | `NTC1` (Input Lead) | 0 V_ AC Nominal / 1.60 A_ RMS | Raw grid neutral entry. |
| `EARTH_GND` | `J1` (Pin E) | `C_Y1` (Pin 2), `C_Y2` (Pin 2), Chassis | 0 V (Chassis Reference) | Protective Earth safety drainage path. |
| `AC_LINE_FUSED` | `F1` (Output Clip `FC2`) | `MOV1` (Pin 1), `C_X1` (Pin 1), `L_CM1` (Pin 1) | 85 - 265 V_ AC / 1.60 A_ RMS | Fused live bus distributing power to surge and filter. |
| `AC_NEUTRAL_PROT` | `NTC1` (Output Lead) | `MOV1` (Pin 2), `C_X1` (Pin 2), `L_CM1` (Pin 4) | 0 V_ AC Nominal / 1.60 A_ RMS | Damped neutral bus feeding surge and filter. |
| `AC_LINE_CM1` | `L_CM1` (Pin 2) | `C_Y1` (Pin 1), `L_CM2` (Pin 1) | 85 - 265 V_ AC / 1.60 A_ RMS | Intermediate stage 1 filtered live bus. |
| `AC_NEUTRAL_CM1` | `L_CM1` (Pin 3) | `C_Y2` (Pin 1), `L_CM2` (Pin 4) | 0 V_ AC Nominal / 1.60 A_ RMS | Intermediate stage 1 filtered neutral bus. |
| `AC_LINE_FILT` | `L_CM2` (Pin 2) | `C_X2` (Pin 1), `BR1` (Pin 2 AC) | 85 - 265 V_ AC / 1.60 A_ RMS | Fully filtered, EMC-compliant live output to bridge. |
| `AC_NEUTRAL_FILT` | `L_CM2` (Pin 3) | `C_X2` (Pin 2), `BR1` (Pin 3 AC) | 0 V_ AC Nominal / 1.60 A_ RMS | Fully filtered, EMC-compliant neutral output to bridge. |

## 4. Theory of Operation & Filtering Transfer Functions
1. **Inrush Current Suppression**: When energized at peak AC line (265 V_ RMS imes √(2) = 374.8 V_ peak), the uncharged bulk capacitor presents an instantaneous dead short. `NTC1` (15.0 Ω cold resistance) acts as an instantaneous series impedance:
 I_ inrush,max = (374.77 V / 15.0 Ω) = mathbf{24.98 A_ peak}
 As steady-state current flows, the thermistor self-heats to approx 100°C, dropping resistance to 0.48 Ω and wasting only 0.145 W.
2. **Surge Voltage Clamping**: During an overvoltage surge (e.g. 1000 V combination spike per IEC 61000-4-5), `MOV1` transitions from high-impedance (> 10 MΩ) to conducting mode within < 25 ns, clamping line voltage below 775 V and absorbing up to 125 Joules.
3. **Differential Mode Noise Attenuation**: The leakage inductances of `L_CM1` (L_ lk1 approx 225 µ H) and `L_CM2` (L_ lk2 approx 70 µ H) combine with `C_X1` and `C_X2` (0.22 µ F each) to form a second-order low-pass filter with corner frequency:
 f_c, DM = (1 / 2π sqrt{L_ lk imes C_X}) = (1 / 2π √(225 µ H imes 0.22 µ F) approx 22.6 kHz
 Provides > 18 dB attenuation at the 65 kHz Flyback switching fundamental.
4. **Common Mode Noise Attenuation**: Formed by L_ CM1 = 15.0 mH and C_Y = 2 imes 2.2 nF = 4.4 nF:
 f_c, CM = (1 / 2π √(15 mH imes 4.4 nF) approx 19.6 kHz
 Provides > 35.4 dB attenuation at 150 kHz (the start of CISPR 32 Class B conducted limits).

## 5. Laboratory Bring-Up & Test Points
* **`TP_AC1` (Live Input)**: Located on output of `F1`. Verify pure sinusoidal AC voltage (85 - 265 V_ AC RMS) referenced to Neutral.
* **`TP_AC2` (Filtered Live)**: Located on pin 2 of `BR1`. Inspect with an oscilloscope (high-voltage differential probe); confirm clean sine wave with switching ripple < 100 mV_ pk-pk.
* **`TP_EARTH` (Chassis Earth)**: Verify zero potential difference (< 0.1 V) to utility earth. Measure leakage current using an earth leakage meter: confirm reading is approx 0.36 mA < 0.75 mA.
