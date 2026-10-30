# Module 1: Mains AC Input Protection & EMI Filter — Equivalent Electronic Circuit

## 1. Subsystem Architectural Overview
Module 1 serves as the frontline power interface connecting the single-phase commercial utility AC mains ($85\,	ext{V} - 265\,	ext{V}_{	ext{AC RMS}}$, $47 - 63\,	ext{Hz}$) to the power supply PCBA. It incorporates multi-layered hardware protection against catastrophic short circuits, inrush transients, and lightning surges, while attenuating conducted electromagnetic emissions to meet **CISPR 32 / EN 55032 Class B** standards.

## 2. Full Schematic-Level Equivalent Electronic Circuit Diagram

```
                              [ MODULE 1: MAINS AC INPUT & 2-STAGE EMI FILTER ]
=============================================================================================================================

          J1: IEC C14
         ┌───────────┐         F1: 2.0A Slow-Blow
Live     │ Terminal L│─────────[=== 5x20mm ===]─────────┬──────────────┬──────────────●═══════════════════╗ L_CM1: 15mH
85-265V  │           │      Littelfuse 0218002.MXP      │              │              ║   Winding 1       ║
         │           │       (Melting I²t=19.6A²s)    ┌─┴─┐          ┌─┴─┐            ║                   ║
         │           │                                │   │          │   │ C_X1       ╚═══════════════════●
         │           │                                │   │ MOV1     │   │ 0.22µF X2            │
         │           │                                │   │ 300V     │   │ KEMET R46            ├─── Net: AC_LINE_CM1
         │           │                                └─┬─┘ 4.5kA    └─┬─┘ 310V AC              │
         │           │                                  │              │                      ┌─┴─┐
         │           │                                  │              │                      │   │ C_Y1: 2.2nF Y1
         │           │                                  │              │                      │   │ KEMET PHE850
         │           │         NTC1: 15.0Ω Cold         │              │                      └─┬─┘ 400V AC
Neutral  │ Terminal N│─────────[───/\/\/\/\───]─────────┴──────────────┴──────────────●           │
0V Nom   │           │      EPCOS B57236S0150M                                        ║           ├───── Net: EARTH_GND
         │           │     (Inrush < 24.98A peak)                                     ║ L_CM1     │      (Chassis Earth Stud)
         │           │                                                                ║ Winding 2 ├─────┐
Earth    │ Terminal E│────────────────────────────────────────────────────────────────────────────┘   ┌─┴─┐
         └───────────┘                                                                                │   │ C_Y2: 2.2nF Y1
                                                                                      ╚═══════════════●   │ KEMET PHE850
                                                                                                │     └─┬─┘ 400V AC
                                                                                                │       │
                                                                                 Net: AC_NEUT_CM1───────┘

  (Continuation into Stage 2 Common Mode Choke L_CM2 & Post-Filter C_X2)
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

 Net: AC_LINE_CM1
 ────────────────────────●═══════════════════╗ L_CM2: 4.7mH
                         ║   Winding 1       ║
                         ║                   ║
                         ╚═══════════════════●──────┬───────────────────────────────────────────> Net: AC_LINE_FILT
                                                    │                                             (To Bridge BR1 Pin 2)
                                                  ┌─┴─┐
                                                  │   │ C_X2
                                                  │   │ 0.22µF X2
                                                  │   │ KEMET R46
                                                  └─┬─┘ 310V AC
                         ╔═══════════════════●      │
                         ║                   ║      │
                         ║   Winding 2       ║      │
 ────────────────────────●═══════════════════╝──────┴───────────────────────────────────────────> Net: AC_NEUTRAL_FILT
 Net: AC_NEUT_CM1        L_CM2: 4.7mH                                                             (To Bridge BR1 Pin 3)

=============================================================================================================================
```

## 3. Subsystem Netlist & Interconnect Table
| Net Name | Origin Pin | Destination Pins | Nominal Voltage / Current | Functional Description |
| :--- | :--- | :--- | :---: | :--- |
| `AC_LINE_IN` | `J1` (Pin L) | `F1` (Input Clip `FC1`) | $85 - 265\,	ext{V}_{	ext{AC}}$ / $1.60\,	ext{A}_{	ext{RMS}}$ | Raw grid live entry from IEC socket. |
| `AC_NEUTRAL_IN` | `J1` (Pin N) | `NTC1` (Input Lead) | $0\,	ext{V}_{	ext{AC}}$ Nominal / $1.60\,	ext{A}_{	ext{RMS}}$ | Raw grid neutral entry. |
| `EARTH_GND` | `J1` (Pin E) | `C_Y1` (Pin 2), `C_Y2` (Pin 2), Chassis | $0\,	ext{V}$ (Chassis Reference) | Protective Earth safety drainage path. |
| `AC_LINE_FUSED` | `F1` (Output Clip `FC2`) | `MOV1` (Pin 1), `C_X1` (Pin 1), `L_CM1` (Pin 1) | $85 - 265\,	ext{V}_{	ext{AC}}$ / $1.60\,	ext{A}_{	ext{RMS}}$ | Fused live bus distributing power to surge and filter. |
| `AC_NEUTRAL_PROT` | `NTC1` (Output Lead) | `MOV1` (Pin 2), `C_X1` (Pin 2), `L_CM1` (Pin 4) | $0\,	ext{V}_{	ext{AC}}$ Nominal / $1.60\,	ext{A}_{	ext{RMS}}$ | Damped neutral bus feeding surge and filter. |
| `AC_LINE_CM1` | `L_CM1` (Pin 2) | `C_Y1` (Pin 1), `L_CM2` (Pin 1) | $85 - 265\,	ext{V}_{	ext{AC}}$ / $1.60\,	ext{A}_{	ext{RMS}}$ | Intermediate stage 1 filtered live bus. |
| `AC_NEUTRAL_CM1` | `L_CM1` (Pin 3) | `C_Y2` (Pin 1), `L_CM2` (Pin 4) | $0\,	ext{V}_{	ext{AC}}$ Nominal / $1.60\,	ext{A}_{	ext{RMS}}$ | Intermediate stage 1 filtered neutral bus. |
| `AC_LINE_FILT` | `L_CM2` (Pin 2) | `C_X2` (Pin 1), `BR1` (Pin 2 AC) | $85 - 265\,	ext{V}_{	ext{AC}}$ / $1.60\,	ext{A}_{	ext{RMS}}$ | Fully filtered, EMC-compliant live output to bridge. |
| `AC_NEUTRAL_FILT` | `L_CM2` (Pin 3) | `C_X2` (Pin 2), `BR1` (Pin 3 AC) | $0\,	ext{V}_{	ext{AC}}$ Nominal / $1.60\,	ext{A}_{	ext{RMS}}$ | Fully filtered, EMC-compliant neutral output to bridge. |

## 4. Theory of Operation & Filtering Transfer Functions
1. **Inrush Current Suppression**: When energized at peak AC line ($265\,	ext{V}_{	ext{RMS}} 	imes \sqrt{2} = 374.8\,	ext{V}_{	ext{peak}}$), the uncharged bulk capacitor presents an instantaneous dead short. `NTC1` ($15.0\,\Omega$ cold resistance) acts as an instantaneous series impedance:
   $$I_{	ext{inrush,max}} = rac{374.77\,	ext{V}}{15.0\,\Omega} = \mathbf{24.98\,	ext{A}_{	ext{peak}}}$$
   As steady-state current flows, the thermistor self-heats to $pprox 100^\circ	ext{C}$, dropping resistance to $0.48\,\Omega$ and wasting only $0.145\,	ext{W}$.
2. **Surge Voltage Clamping**: During an overvoltage surge (e.g. $1000\,	ext{V}$ combination spike per IEC 61000-4-5), `MOV1` transitions from high-impedance ($> 10\,	ext{M}\Omega$) to conducting mode within $< 25\,	ext{ns}$, clamping line voltage below $775\,	ext{V}$ and absorbing up to $125\,	ext{Joules}$.
3. **Differential Mode Noise Attenuation**: The leakage inductances of `L_CM1` ($L_{	ext{lk1}} pprox 225\,\mu	ext{H}$) and `L_CM2` ($L_{	ext{lk2}} pprox 70\,\mu	ext{H}$) combine with `C_X1` and `C_X2` ($0.22\,\mu	ext{F}$ each) to form a second-order low-pass filter with corner frequency:
   $$f_{c,	ext{DM}} = rac{1}{2\pi \sqrt{L_{	ext{lk}} 	imes C_X}} = rac{1}{2\pi \sqrt{225\,\mu	ext{H} 	imes 0.22\,\mu	ext{F}}} pprox \mathbf{22.6\,	ext{kHz}}$$
   Provides $> 18\,	ext{dB}$ attenuation at the $65\,	ext{kHz}$ Flyback switching fundamental.
4. **Common Mode Noise Attenuation**: Formed by $L_{	ext{CM1}} = 15.0\,	ext{mH}$ and $C_Y = 2 	imes 2.2\,	ext{nF} = 4.4\,	ext{nF}$:
   $$f_{c,	ext{CM}} = rac{1}{2\pi \sqrt{15\,	ext{mH} 	imes 4.4\,	ext{nF}}} pprox \mathbf{19.6\,	ext{kHz}}$$
   Provides $> 35.4\,	ext{dB}$ attenuation at $150\,	ext{kHz}$ (the start of CISPR 32 Class B conducted limits).

## 5. Laboratory Bring-Up & Test Points
* **`TP_AC1` (Live Input)**: Located on output of `F1`. Verify pure sinusoidal AC voltage ($85 - 265\,	ext{V}_{	ext{AC RMS}}$) referenced to Neutral.
* **`TP_AC2` (Filtered Live)**: Located on pin 2 of `BR1`. Inspect with an oscilloscope (high-voltage differential probe); confirm clean sine wave with switching ripple $< 100\,	ext{mV}_{	ext{pk-pk}}$.
* **`TP_EARTH` (Chassis Earth)**: Verify zero potential difference ($< 0.1\,	ext{V}$) to utility earth. Measure leakage current using an earth leakage meter: confirm reading is $pprox 0.36\,	ext{mA} < 0.75\,	ext{mA}$.
