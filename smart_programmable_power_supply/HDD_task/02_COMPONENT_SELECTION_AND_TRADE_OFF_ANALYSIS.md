# SPPS Hardware Design Document (HDD) — Component Selection & Trade-Off Analysis

---

### Document Control Information
* **Document Identifier**: `VVDN_SPPS_2026_HDD_SEL_V1.0`
* **Parent Document**: [PRD Final SPPS (`prd_final_spps.docx`)](file:///home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/PRD_task/reference_docs/prd_final_spps.docx)
* **Corporate Standard**: VVDN TP013 V1.1 Hardware Design Document Template
* **Project Code**: `VVDN_SPPS_2026`
* **Project Name**: Smart Programmable Voltage Supply Module (85–265 V AC In, 5–20 V / 3.0 A DC Out)
* **Author / Design Owner**: Hardware Engineering Team / Power Electronics Trainee
* **Review Level**: Level 1 Internal Technical Review / BU SME Review
* **Status**: **Component Selection Baseline (Pre-Monolithic HDD Sign-off)**
* **Date**: 21st October 2026

---

## 1. Scope & Selection Methodology

This document establishes the formal engineering justifications, parametric selections, and multi-source component trade-off studies for all four power conversion stages and mixed-signal supervisory circuits of the **Smart Programmable Power Supply (SPPS)** module (`VVDN_SPPS_2026`).

Every selected component is evaluated against four non-negotiable engineering criteria:
1. **Compliance with PRD Baseline (`prd_final_spps.docx`)**: Electrical ratings, voltage isolation withstand, and efficiency targets.
2. **Stress Derating Margin**: Voltage stress $\le 75\%$, current stress $\le 70\%$, and power dissipation $\le 60\%$ under worst-case thermal and line conditions ($265\,\text{V}_{\text{AC}}$, $50^\circ\text{C}$ ambient) in accordance with VVDN corporate reliability rules.
3. **Availability & Multi-Sourcing**: Prioritizing components with at least two qualified second-source pin-compatible alternates to mitigate supply chain obsolescence.
4. **Thermal Feasibility**: Natural convection cooling without external fans, requiring minimum package thermal resistance and optimal copper heatsinking.

---

## 2. Stage 1: Mains AC Input Protection & EMI Filtering Component Selections

```
   [AC MAINS INLET]
    IEC 320-C14
         │
         ├──[ F1: Ceramic Fuse 2A/250V (Littelfuse 0218002.MXP) ]
         │
         ├──[ NTC1: Inrush Limiter (EPCOS B57236S0100M000 / B57236S0150M000) ]
         │
         ├──[ MOV1: Surge Clamp 300V RMS (Bourns MOV-14D471K) ]
         │
         └──[ 2-Stage EMI Filter: L_CM1 (15mH), L_CM2 (4.7mH), C_X1/2 (0.22µF), C_Y1/2 (2.2nF) ]
```

### 2.1 AC Mains Inlet & Cartridge Fuse ($F_1$)
* **Design Requirement (PR-01)**: $2.0\,\text{A}$ Ceramic Fuse for AC mains short-circuit and cataclysmic fault protection.
* **Primary Selection**: **Littelfuse `0218002.MXP`**
  * *Parameters*: $2.0\,\text{A}$ rated current, $250\,\text{V}$ AC RMS, $5 \times 20\,\text{mm}$ cylindrical ceramic body, Time-Lag (Slow-Blow).
  * *Interrupting Rating*: $1500\,\text{A} @ 250\,\text{V}$ AC (Category IEC 60127-2 Sheet 5).
  * *Nominal Melting Energy ($I^2t$)*: $19.6\,\text{A}^2\text{s}$.
  * *Justification*: The ceramic body prevents catastrophic rupture during a high-energy short circuit. The time-lag characteristic and high $I^2t$ rating ensure zero nuisance tripping during cold-start capacitive inrush ($I^2t_{\text{inrush}} \approx 2.1\,\text{A}^2\text{s} \ll 19.6\,\text{A}^2\text{s}$).
  * *Second Source*: Schurter `0001.2507` (Series FST, $2.0\,\text{A}$, $250\,\text{V}$, $I^2t = 22.0\,\text{A}^2\text{s}$).

### 2.2 Inrush Current Limiting Thermistor ($\text{NTC}_1$) — Trade-Off Analysis
* **Design Requirement (PR-02)**: Input inrush current limited to $< 25.0\,\text{A}$ peak at cold start ($265\,\text{V}_{\text{AC RMS}}$).
* **Trade-Off Study: $10.0\,\Omega$ vs $15.0\,\Omega$ Cold Resistance**:

| Parameter | Option A: $10.0\,\Omega$ NTC (PRD Baseline) | Option B: $15.0\,\Omega$ NTC (Recommended Enhancement) | Trade-Off Comparison |
| :--- | :--- | :--- | :--- |
| **Manufacturer & Part Number** | TDK / EPCOS `B57236S0100M000` | TDK / EPCOS `B57236S0150M000` | Direct drop-in pin-compatible series (S236 footprint, 13mm disc). |
| **Cold Resistance ($R_{25}$)** | $10.0\,\Omega \pm 20\%$ | $15.0\,\Omega \pm 20\%$ | Option B provides 50% more cold damping. |
| **Peak Inrush Current (Zero Grid $Z$)** | $I_{\text{pk}} = \frac{374.8\,\text{V}}{10.0\,\Omega} = 37.48\,\text{A}$ | $I_{\text{pk}} = \frac{374.8\,\text{V}}{15.0\,\Omega} = \mathbf{24.98\,\text{A}}$ | Option B strictly guarantees $< 25\,\text{A}$ even on a zero-impedance industrial test bus! |
| **Peak Inrush Current ($5.0\,\Omega$ Grid $Z$)**| $I_{\text{pk}} = \frac{374.8\,\text{V}}{15.0\,\Omega} = 24.98\,\text{A}$ | $I_{\text{pk}} = \frac{374.8\,\text{V}}{20.0\,\Omega} = 18.74\,\text{A}$ | Option A requires at least $5.0\,\Omega$ external grid loop impedance to pass $< 25\,\text{A}$. |
| **Max Continuous Current Rating** | $3.2\,\text{A}_{\text{RMS}}$ | $2.9\,\text{A}_{\text{RMS}}$ | Both exceed max operating AC current ($1.60\,\text{A}_{\text{RMS}}$) by $> 80\%$. |
| **Steady-State Hot Resistance ($R_{\text{hot}}$)**| $\approx 0.35\,\Omega$ | $\approx 0.48\,\Omega$ | Option B dissipates an extra $0.20\,\text{W}$ at full load. |
| **Full Load Dissipation ($I_{\text{RMS}} = 0.55\text{A} @ 230\text{V}$)**| $P = (0.55)^2 \times 0.35 = 0.106\,\text{W}$ | $P = (0.55)^2 \times 0.48 = 0.145\,\text{W}$ | Negligible impact on overall efficiency ($< 0.05\%$). |
| **Engineering Decision** | Baseline PRD reference part. | **Recommended for Rev A1_001** to guarantee unconditional pass of PR-02 compliance. |

### 2.3 Metal Oxide Varistor Surge Suppressor ($\text{MOV}_1$)
* **Design Requirement (PR-04 / PR-05)**: Line-to-neutral transient voltage suppression compliant with IEC 61000-4-5 Level 3 ($1.0\,\text{kV}$ line-to-line surge).
* **Primary Selection**: **Bourns `MOV-14D471K`**
  * *Parameters*: $300\,\text{V}$ AC RMS continuous operating voltage, $385\,\text{V}$ DC continuous, Varistor Voltage $V_N = 470\,\text{V} \pm 10\% @ 1\,\text{mA}$, Clamping Voltage $V_C = 775\,\text{V} @ 50\,\text{A}$, Peak Surge Current: $4500\,\text{A}$ ($8/20\,\mu\text{s}$ wave), Energy Absorption: $125\,\text{J}$.
  * *Justification*: The $300\,\text{V}_{\text{RMS}}$ rating leaves a safe $13.2\%$ headroom above the highest line voltage ($265\,\text{V}_{\text{AC RMS}}$), preventing MOV degradation from nominal utility grid swells while clamping fast transient spikes before the bridge rectifier.
  * *Second Source*: Littelfuse `V300LA20AP` (14mm disc, $300\,\text{V}_{\text{RMS}}$, $4500\,\text{A}$).

### 2.4 Common-Mode Chokes & Safety Capacitors
* **Common-Mode Chokes ($L_{\text{CM1}}, L_{\text{CM2}}$)**:
  * $L_{\text{CM1}}$: Wurth Elektronik `744823215` ($15.0\,\text{mH} \pm 30\%$, $1.1\,\text{A}_{\text{RMS}}$, toroid through-hole, rated for low-frequency $150\,\text{kHz} - 2\,\text{MHz}$ attenuation). Second source: KEMET `SC-10-10J`.
  * $L_{\text{CM2}}$: Wurth Elektronik `744822472` ($4.7\,\text{mH} \pm 30\%$, $1.6\,\text{A}_{\text{RMS}}$, high-permeability core, rated for $2\,\text{MHz} - 30\,\text{MHz}$ attenuation). Second source: Bourns `7355-V-RC`.
* **Class X2 Across-The-Line Film Capacitors ($C_{X1}, C_{X2}$)**:
  * KEMET `R46KI32200001M` ($0.22\,\mu\text{F} \pm 20\%$, $310\,\text{V}$ AC RMS, Metallized Polypropylene, Pitch $15.0\,\text{mm}$). Second source: Vishay `B32922C3224M`.
* **Class Y1 Line-To-Earth Ceramic Capacitors ($C_{Y1}, C_{Y2}$)**:
  * KEMET `PHE850` / Murata `DE1E3KX222MA4BP01F` ($2.2\,\text{nF} \pm 20\%$, $400\,\text{V}$ AC RMS, Double Reinforced Insulation). Second source: TDK `CD45-E2GA222M-NKA`.

---

## 3. Stage 2: Bridge Rectifier & High-Voltage Bulk DC Link Selections

### 3.1 Single-Phase Bridge Rectifier ($\text{BR}_1$)
* **Design Requirement**: Full-wave rectification of $85\,\text{V} - 265\,\text{V}_{\text{AC}}$ with low conduction loss and high surge withstand.
* **Primary Selection**: **Diodes Incorporated `GBU606`**
  * *Parameters*: Peak Repetitive Reverse Voltage $V_{\text{RRM}} = 600\,\text{V}$, Average Forward Current $I_{\text{F(AV)}} = 6.0\,\text{A}$ (with heatsink) / $3.8\,\text{A}$ (free air), Forward Voltage Drop $V_F = 1.0\,\text{V} @ 3.0\,\text{A}$, Non-Repetitive Peak Forward Surge $I_{\text{FSM}} = 175\,\text{A}$ ($8.3\,\text{ms}$ single half-sine wave).
  * *Stress Analysis*:
    * Max Peak Reverse Voltage: $V_{\text{peak}} = 265\,\text{V} \times \sqrt{2} = 374.8\,\text{V}$. Voltage derating: $\frac{374.8\,\text{V}}{600\,\text{V}} = \mathbf{62.5\%}$ (strictly compliant with $\le 75\%$ guideline).
    * Max Operating RMS Current: $1.60\,\text{A}$. Current derating: $\frac{1.60\,\text{A}}{6.0\,\text{A}} = \mathbf{26.7\%}$ (exceptionally conservative).
    * Inrush Surge Withstand: Peak cold inrush ($25\,\text{A}$) is only $14.3\%$ of $I_{\text{FSM}} = 175\,\text{A}$.
  * *Second Source*: Vishay `GBU6J` ($600\,\text{V}$, $6.0\,\text{A}$, GBU package) or `GBU8K` ($800\,\text{V}$, $8.0\,\text{A}$).

### 3.2 High-Voltage Bulk Electrolytic Capacitor ($C_{\text{BULK1}}$)
* **Design Requirement (FR-01 / Holdup)**: Minimum $10.0\,\text{ms}$ holdup time across line dropouts with low 100/120 Hz ripple voltage.
* **Primary Selection**: **Nichicon `LGW2W101MELZ25`** (Series GW)
  * *Parameters*: Capacitance $100\,\mu\text{F} \pm 20\%$, Working Voltage $450\,\text{V}$ DC, Surge Voltage $500\,\text{V}$ DC, Snap-In Terminal Mounting, Case Dimensions $\varnothing 22 \times 25\,\text{mm}$, Operating Temperature $-25^\circ\text{C}$ to $+105^\circ\text{C}$, Load Life $3000\,\text{hours} @ 105^\circ\text{C}$.
  * *Rated Ripple Current*: $0.78\,\text{A}_{\text{RMS}} @ 120\,\text{Hz} / 105^\circ\text{C}$; Multiplier at high frequency ($10\,\text{kHz} - 100\,\text{kHz}$) is $1.50 \times \longrightarrow 1.17\,\text{A}_{\text{RMS}}$.
  * *Stress Analysis*: Max bulk DC voltage is $374.8\,\text{V}$ DC. Voltage derating: $\frac{374.8\,\text{V}}{450\,\text{V}} = \mathbf{83.3\%}$ of continuous rating ($74.9\%$ of $500\,\text{V}$ surge). Under nominal grid ($230\,\text{V}_{\text{AC}}$, $V_{\text{bulk}} = 325\,\text{V}$), derating is $\mathbf{72.2\%}$.
  * *Holdup Time Verification*: $t_{\text{holdup}} = \frac{C (V_{\text{nom}}^2 - V_{\text{min}}^2)}{2 P_{\text{in}}} = \frac{100\,\mu\text{F} \times (325^2 - 120^2)}{2 \times 81.82\,\text{W}} = \mathbf{55.8\,\text{ms}} \gg 10.0\,\text{ms}$!
  * *Second Source*: Panasonic `EEU-ED2W101` ($100\,\mu\text{F}$, $450\,\text{V}$, $105^\circ\text{C}$, Snap-in) or Rubycon `450BXW100MEFR18X30`.

### 3.3 High-Frequency Decoupling Capacitor & Bleeder Resistors
* **High-Frequency Ceramic Capacitor ($C_{\text{HF}}$)**:
  * Murata `GA342QR7GD102KW01L` ($100\,\text{nF} \pm 10\%$, $630\,\text{V}$ DC, X7R dielectric, 1812 SMD footprint). Bypasses high-frequency switching ringing directly across the primary FET and transformer loop.
* **Safety Bleeder Resistors ($R_{\text{BL1}}, R_{\text{BL2}}, R_{\text{BL3}}$)**:
  * Three $100\,\text{k}\Omega \pm 1\%$ resistors in series (Total $300\,\text{k}\Omega$, $0.75\,\text{W}$ capability). Vishay Dale `CRCW1206100KFKEA` ($1206$ SMD, $0.25\,\text{W}$, $200\,\text{V}$ element limit).
  * Voltage per resistor at $375\,\text{V}$: $125\,\text{V}$ ($62.5\%$ derating). Discharges $100\,\mu\text{F}$ cap to $< 50\,\text{V}$ in $\approx 35\,\text{seconds}$.

---

## 4. Stage 3: Isolated Flyback Converter Component Selections & Trade-Offs

### 4.1 Primary Flyback Controller Selection Trade-Off Study: UCC28740 vs UCC28C43 / UC3843
The PRD mentions both **TI UCC28740** (REF-003, Dependencies, Standby $< 150\,\text{mW}$) and **UC3843 / UCC28C43** (Step 2 uniform 65 kHz clock). A detailed trade-off analysis is conducted below:

| Feature / Metric | Option A: Texas Instruments UCC28740 | Option B: Texas Instruments UCC28C43 / UC3843 | Architectural Trade-Off Analysis |
| :--- | :--- | :--- | :--- |
| **Control Topology** | Quasi-Resonant (QR) Valley Switching with Frequency Foldback & AM/FM Modulation. | Fixed-Frequency Uniform Clock Peak Current Mode PWM ($65.0\,\text{kHz}$). | UCC28740 switches at zero-voltage valley points, minimizing capacitive turn-on losses ($P_{\text{sw}} \propto C_{\text{oss}} V^2 f_{\text{sw}}$). UCC28C43 switches at rigid uniform clock. |
| **Primary Efficiency @ 230V Full Load** | **$> 91.5\%$** (Exceeds FR-05 requirement $> 90.0\%$). | **$\approx 88.5\% - 89.5\%$** (Marginal against $> 90.0\%$ target with passive Schottky diode). | UCC28740 provides $+2.0\%$ higher stage efficiency due to valley switching and elimination of fixed-frequency hard turn-on spikes. |
| **Standby No-Load Power Consumption** | **$< 30\,\text{mW}$** (Easily satisfies FR-08 $< 150\,\text{mW}$ target). | **$\approx 180\,\text{mW} - 250\,\text{mW}$** (Fails $< 150\,\text{mW}$ unless auxiliary burst circuit added). | UCC28740 incorporates native burst-mode operation at light loads, reducing standby quiescent current to $< 35\,\mu\text{A}$. |
| **Switching Noise & EMI Profile** | Variable switching frequency spreads EMI energy across spectrum, lowering peak conducted emissions by $6\,\text{dB}-10\,\text{dB}$. | Fixed $65\,\text{kHz}$ concentrates harmonic spurs at $65\,\text{kHz}, 130\,\text{kHz}, 195\,\text{kHz}$, requiring larger EMI filter chokes. | UCC28740 significantly reduces differential-mode filter size and cost. |
| **Complexity & Pin Count** | 7-pin SOIC (`SOIC-7`), minimal external passives, direct optocoupler interface. | 8-pin SOIC (`SOIC-8`), requires external timing components ($R_T, C_T$) and slope compensation. | UCC28740 reduces PCBA component count by 6 passives. |
| **Transformer Compatibility** | Fully compatible with PQ26/20 ($L_p = 220\,\mu\text{H}$, $N_p=36$, $N_s=6$). | Fully compatible with PQ26/20 ($L_p = 220\,\mu\text{H}$, $N_p=36$, $N_s=6$). | Identical magnetic core, windings, and footprint for both options! |
| **Hardware Recommendation** | **RECOMMENDED PRIMARY CHOICE**: TI `UCC28740DR` is chosen as the baseline for Rev A1_001 due to unconditional compliance with PRD FR-05 ($>90\%$ eff) and FR-08 ($<150\text{mW}$ standby). | **VALIDATED ALTERNATE**: TI `UCC28C43DR` (BiCMOS low-power version of UC3843, $I_q = 0.5\,\text{mA}$) retained as drop-in alternate layout option if customer mandates fixed clock. |

### 4.2 Flyback Power Transformer Magnetics ($\text{TX}_1$)
* **Design Requirement (FR-02 / FR-06)**: Galvanically isolated power transfer delivering $+24.0\,\text{V} \pm 1.0\%$ @ $3.0\,\text{A}$ ($72\,\text{W}$ continuous), withstand $3000\,\text{V}$ AC RMS ($1\,\text{min}$).
* **Core & Bobbin Selection**:
  * Core: **PQ26/20 Ferrite Core**, Material Grade **Ferroxcube `3C95`** or **TDK `PC40`** ($B_{\text{sat}} = 0.38\,\text{T} @ 100^\circ\text{C}$).
  * Effective Magnetic Cross-Section ($A_e$): $122.0\,\text{mm}^2$. Effective Core Volume ($V_e$): $5490\,\text{mm}^3$.
  * Bobbin: 12-pin Through-Hole Horizontal Bobbin with physical primary-to-secondary pin pitch separation $\ge 8.0\,\text{mm}$.
* **Magnetic Parameters**:
  * Primary Inductance ($L_p$): $\mathbf{220.0\,\mu\text{H} \pm 10\%}$.
  * Primary Turns ($N_p$): **$36\,\text{turns}$** (2x strands 0.35 mm Grade 2 Polyurethane-enamelled copper wire).
  * Secondary Turns ($N_s$): **$6\,\text{turns}$** (**Furukawa `TEX-E` Triple-Insulated Wire**, $0.80\,\text{mm}$ conductor diameter, $3000\,\text{V}_{\text{RMS}}$ dielectric proof rating).
  * Auxiliary Bias Turns ($N_{\text{aux}}$): **$4\,\text{turns}$** ($0.25\,\text{mm}$ enamel wire, delivering $+14.0\,\text{V}$ DC aux bias).
  * Peak Operating Flux Density ($B_{\text{max}}$): **$0.151\,\text{Tesla}$** ($< 40\%$ of $B_{\text{sat}} = 0.38\,\text{T}$), guaranteeing zero core saturation even during instantaneous load steps or startup transients.

### 4.3 Primary Switching MOSFET ($Q_1$)
* **Design Requirement**: High-voltage switching up to $375\,\text{V}_{\text{bulk}}$ plus reflected flyback voltage ($V_R = 144\,\text{V}$) with low switching and conduction losses.
* **Primary Selection**: **Infineon `IPB80R290P7`** (CoolMOS P7 Technology)
  * *Parameters*: Drain-Source Breakdown $V_{\text{(BR)DSS}} = 800\,\text{V}$, Continuous Drain Current $I_D = 17.0\,\text{A} @ 25^\circ\text{C}$ / $11.0\,\text{A} @ 100^\circ\text{C}$, On-Resistance $R_{\text{DS(on)}} = 0.290\,\Omega$ max, Gate Charge $Q_g = 24\,\text{nC}$, Package: D2PAK (TO-263-3).
  * *Stress Derating*:
    * Peak Drain Voltage: $V_{\text{DS,max}} = V_{\text{bulk,max}} + V_R + V_{\text{spike}} = 375\,\text{V} + 144\,\text{V} + 80\,\text{V} = \mathbf{599.0\,\text{V}}$.
    * Voltage Derating: $\frac{599.0\,\text{V}}{800.0\,\text{V}} = \mathbf{74.88\%}$ (strictly within corporate $\le 75\%$ guideline).
    * Conduction Loss at full load: $P_{\text{cond}} = (1.17\,\text{A}_{\text{RMS}})^2 \times (0.29\,\Omega \times 1.5) = \mathbf{0.595\,\text{W}}$.
    * Thermal Rise: Mounted on $300\,\text{mm}^2$ 2oz copper pad ($R_{\theta\text{JA}} = 40^\circ\text{C/W}$), $\Delta T = 0.85\,\text{W} \times 40 = 34^\circ\text{C} \longrightarrow T_j \approx 84^\circ\text{C} @ 50^\circ\text{C}$ ambient.
  * *Second Source*: STMicroelectronics `STP10NK80Z` ($800\,\text{V}$, $9.0\,\text{A}$, $0.78\,\Omega$, TO-220) or Infineon `IPD80R360P7` (TO-252 DPAK).

### 4.4 Secondary Schottky Rectifier Diode ($D_{\text{SEC}}$)
* **Design Requirement**: Robust passive rectification of $24.0\,\text{V} / 3.0\,\text{A}$ output with low forward drop and fast switching.
* **Primary Selection**: **ON Semiconductor `MBR10100G`**
  * *Parameters*: Peak Repetitive Reverse Voltage $V_{\text{RRM}} = 100\,\text{V}$, Average Rectified Current $I_{\text{O}} = 10.0\,\text{A} @ T_C = 133^\circ\text{C}$, Forward Voltage $V_F = 0.60\,\text{V} @ 3.0\,\text{A} / 100^\circ\text{C}$, Package: TO-220-2.
  * *Stress Analysis*:
    * Reverse Voltage: $V_{\text{rev}} = V_{\text{OUT}} + \frac{V_{\text{bulk,max}}}{n} = 24.0\,\text{V} + \frac{374.8\,\text{V}}{6.0} = 86.47\,\text{V}$.
    * Clamped Peak Reverse Voltage: Snubber network clamps reverse inductive ring to $\le 90.0\,\text{V}$.
    * Current Derating: $\frac{3.0\,\text{A}}{10.0\,\text{A}} = \mathbf{30.0\%}$ (exceptionally conservative).
    * Conduction Dissipation: $P_{\text{diode}} = I_{\text{avg}} \times V_F = 3.0\,\text{A} \times 0.60\,\text{V} = \mathbf{1.80\,\text{W}}$. Mounted to a small stamped aluminum heatsink ($15^\circ\text{C/W}$), junction temperature reaches $T_j \approx 50^\circ\text{C} + (1.8\,\text{W} \times 17^\circ\text{C/W}) = \mathbf{80.6^\circ\text{C}} \ll 150^\circ\text{C}$.
  * *Second Source*: STMicroelectronics `STPS10H100D` ($100\,\text{V}$, $10\,\text{A}$, $V_F = 0.57\,\text{V}$) or Vishay `V10150C` ($150\,\text{V}$, $10\,\text{A}$ for even higher voltage margin: $\frac{90\,\text{V}}{150\,\text{V}} = 60\%$ derating).

---

## 5. Stage 4: 4-Switch Synchronous Buck-Boost Post-Regulator Selections

```
   +24V Intermediate Bus
            │
            ├──[ Ceramic Filter Bank (4x 10µF/50V MLCC) + 2x 470µF/35V Low-ESR ]
            │
         ┌──┴──┐
         │ QA  │ (High-Side Buck)
         └──┬──┘
            ├──[ L1: 10µH Flat-Wire Power Inductor (WE 7443321000) ]──┐
         ┌──┴──┐                                                      │
         │ QB  │ (Low-Side Buck)                                   ┌──┴──┐
         └──┬──┘                                                   │ QC  │ (Low-Side Boost)
            │                                                      └──┬──┘
          PGND                                                        │
                                                                   ┌──┴──┐
                                                                   │ QD  │ (High-Side Boost)
                                                                   └──┬──┘
                                                                      │
                                                [ 10mΩ Metal Shunt CSS2H-2512R ]
                                                                      │
                                                [ Output Filter: 4x 22µF Ceramic + 100µF Polymer ]
                                                                      │
                                                                   VOUT (5V-20V / 3A)
```

### 5.1 4-Switch Buck-Boost Controller ($U_3$)
* **Design Requirement (BB-01 to BB-07)**: Wide-input 4-switch synchronous buck-boost controller with seamless buck-to-boost mode transitions, fixed $300\,\text{kHz}$ clock, and cycle-by-cycle hardware peak overcurrent limiting via CSP/CSN.
* **Primary Selection**: **Texas Instruments `LM5176PWPR`**
  * *Parameters*: Input Voltage Range $4.2\,\text{V}$ to $55\,\text{V}$, Output Voltage $0.8\,\text{V}$ to $55\,\text{V}$, Integrated High-Side & Low-Side Gate Drivers ($2.0\,\text{A}$ sink / $1.0\,\text{A}$ source peak), Programmable Switching Frequency ($100\,\text{kHz} - 600\,\text{kHz}$), Package: HTSSOP-28 with exposed thermal pad.
  * *Key Justifications*:
    1. **Seamless Mode Transition**: Patented current-mode control smoothly transitions between pure Buck mode ($V_{\text{OUT}} = 5\,\text{V} - 18\,\text{V}$), 4-switch Buck-Boost mode ($V_{\text{OUT}} \approx 20\,\text{V}$), and pure Boost mode with zero subharmonic oscillation or output step glitches.
    2. **Native Built-in Cycle-by-Cycle Peak OCP**: Features dedicated differential current sense pins (`CSP` and `CSN`) with an internal $35\,\text{mV}$ peak threshold. Connected directly to our $10.0\,\text{m}\Omega$ output shunt, it natively clamps inductor current on every single $300\,\text{kHz}$ cycle at $3.50\,\text{A}$ without requiring external op-amps, comparators, or MCU intervention (PR-03 / CT-02).
    3. **Precision Enable / UVLO**: Pin 6 (`ENABLE`) allows both hardware input under-voltage lockout and high-speed supervisory shutdown from the STM32G474 MCU (CT-03).
    4. **Integrated Thermal Shutdown**: Shuts down internal drivers at $T_j \ge 165^\circ\text{C}$ with automatic recovery at $145^\circ\text{C}$ (PR-04).
  * *Second Source*: Analog Devices `LTC3789EGN#PBF` / `LTC3780EUH` (Pinout requires adapter board, LM5176 is primary sole-source designator for VVDN SPPS).

### 5.2 4-Switch Synchronous Power MOSFETs ($Q_A, Q_B, Q_C, Q_D$)
* **Design Requirement**: Synchronous rectification across all four positions with ultra-low on-resistance and low gate charge to minimize both conduction and high-frequency switching losses.
* **Primary Selection**: **Infineon `BSC034N04LS`** (OptiMOS 3 Technology)
  * *Parameters*: Drain-Source Breakdown $V_{\text{DSS}} = 40.0\,\text{V}$, Continuous Drain Current $I_D = 100\,\text{A} @ 25^\circ\text{C}$ / $70\,\text{A} @ 100^\circ\text{C}$, On-Resistance $R_{\text{DS(on)}} = 3.4\,\text{m}\Omega$ max ($@ V_{\text{GS}} = 10\,\text{V}$), Gate Charge $Q_g = 22\,\text{nC}$, Package: TDSON-8 / SuperSO8 ($5 \times 6\,\text{mm}$).
  * *Stress Derating*:
    * Max Voltage Stress: Occurs across buck switches at $+24\,\text{V}$ intermediate bus and boost switches at $+20\,\text{V}$ output rail.
    * Derating: $\frac{24.0\,\text{V}}{40.0\,\text{V}} = \mathbf{60.0\%}$ (comfortably within corporate $\le 75\%$ guideline).
    * Current Derating: Continuous output is $3.0\,\text{A}$; inductor peak current is $3.8\,\text{A}$. Derating against $70\,\text{A} @ 100^\circ\text{C}$ rating is $\mathbf{5.4\%}$ (negligible thermal stress).
    * Power Dissipation: Total worst-case power dissipation per MOSFET (conduction + switching) is strictly $< 0.35\,\text{W}$. With 2oz copper thermal polygons, junction temperature rise is $< 15^\circ\text{C}$ above ambient ($T_j \le 65^\circ\text{C} @ 50^\circ\text{C}$ ambient).
  * *Second Source*: Texas Instruments `CSD18534Q5A` ($40\,\text{V}$, $3.5\,\text{m}\Omega$, SON-8) or Nexperia `PSMN4R0-40YS` ($40\,\text{V}$, $4.0\,\text{m}\Omega$, LFPAK56).

### 5.3 Flat-Wire High-Current Power Inductor ($L_1$)
* **Design Requirement (BB-06)**: Fixed $300\,\text{kHz}$ operation, low DCR, high saturation margin ($I_{\text{sat}} \gg I_{\text{pk}}$) to prevent core saturation during overcurrent trip events.
* **Primary Selection**: **Wurth Elektronik `7443321000`** (Series WE-HCC)
  * *Parameters*: Inductance $L = 10.0\,\mu\text{H} \pm 20\%$, Rated RMS Current $I_{\text{RMS}} = 8.5\,\text{A}$ ($\Delta T = 40^\circ\text{C}$), Saturation Current $I_{\text{sat}} = 11.5\,\text{A}$ ($\Delta L/L = 30\%$), DC Resistance $R_{\text{DC}} = 13.5\,\text{m}\Omega$ max, Footprint: SMD $12.5 \times 12.5 \times 10.5\,\text{mm}$.
  * *Stress Analysis*:
    * Max Operating Inductor Current: $3.66\,\text{A}_{\text{pk}}$ in Buck mode at 5V; $3.55\,\text{A}_{\text{pk}}$ in Buck-Boost at 20V.
    * Saturation Safety Headroom: The hardware current limit trips at $3.50\,\text{A}$. The inductor saturation threshold is $11.5\,\text{A}$. Safety margin: $\frac{11.5\,\text{A} - 3.5\,\text{A}}{11.5\,\text{A}} = \mathbf{69.6\%}$ headroom! Core saturation is impossible under any electrical condition.
    * Copper Dissipation: $P_{\text{cu}} = I_{\text{RMS}}^2 \times R_{\text{DC}} = (3.0\,\text{A})^2 \times 0.0135\,\Omega = \mathbf{0.122\,\text{W}}$. Core loss at $300\,\text{kHz}$ is $\approx 0.15\,\text{W}$. Total inductor dissipation $< 0.28\,\text{W}$.
  * *Second Source*: Coilcraft `SER2915L-103KL` ($10.0\,\mu\text{H}$, $I_{\text{sat}} = 15.0\,\text{A}$, $R_{\text{DC}} = 8.6\,\text{m}\Omega$).

### 5.4 Precision Current Sense Shunt Resistor ($R_{\text{shunt}}$) — Trade-Off Analysis
* **Design Requirement (CT-02 / PR-03)**: Precision output current sensing and native cycle-by-cycle hardware overcurrent limiting.
* **Trade-Off Study: $10.0\,\text{m}\Omega$ vs $5.0\,\text{m}\Omega$ Metal Shunt**:

| Parameter | Option A: $10.0\,\text{m}\Omega$ Shunt (PRD Baseline) | Option B: $5.0\,\text{m}\Omega$ Shunt (Alternative) | Engineering Evaluation |
| :--- | :--- | :--- | :--- |
| **Manufacturer & Part Number** | Bourns `CSS2H-2512R-L010F` | Bourns `CSS2H-2512R-L005F` | Direct footprint drop-in (2512 SMD metal alloy). |
| **Resistance & Tolerance** | $10.0\,\text{m}\Omega \pm 1.0\%$ (or $\pm 0.1\%$ Option F) | $5.0\,\text{m}\Omega \pm 1.0\%$ | Both offer TCR $< 50\,\text{ppm}/^\circ\text{C}$. |
| **Power Rating** | $3.0\,\text{W} @ 70^\circ\text{C}$ | $3.0\,\text{W} @ 70^\circ\text{C}$ | Heavy-duty EBW metal element construction. |
| **Dissipation @ 3.0A Full Load** | $P = (3.0)^2 \times 0.010 = \mathbf{0.090\,\text{W}}$ | $P = (3.0)^2 \times 0.005 = \mathbf{0.045\,\text{W}}$ | Power dissipation in both is $< 3\%$ of the 3W package rating! Thermal drift is negligible for both. |
| **LM5176 CSP/CSN Differential Voltage Drop**| At $3.0\,\text{A}$: $\Delta V = 30.0\,\text{mV}$<br/>At $3.5\,\text{A}$: $\Delta V = \mathbf{35.0\,\text{mV}}$ | At $3.0\,\text{A}$: $\Delta V = 15.0\,\text{mV}$<br/>At $3.5\,\text{A}$: $\Delta V = 17.5\,\text{mV}$ | **CRITICAL DECISION FACTOR**: LM5176 has an internal fixed peak threshold of $V_{\text{CS(th)}} = 35.0\,\text{mV}$ typical! |
| **Native Current Limit Compatibility** | **$10.0\,\text{m}\Omega$ provides EXACT MATCH**: $\frac{35\,\text{mV}}{10\,\text{m}\Omega} = \mathbf{3.50\,\text{A}}$ hardware trip limit! | $5.0\,\text{m}\Omega$ would result in a $7.0\,\text{A}$ trip limit, requiring external op-amp level shifting! | Option A enables completely autonomous built-in hardware protection without external components. |
| **INA226 Telemetry Resolution** | At $10\,\text{m}\Omega$, INA226 $2.5\,\mu\text{V}$ LSB corresponds to $0.25\,\text{mA}$ current resolution. | At $5\,\text{m}\Omega$, INA226 $2.5\,\mu\text{V}$ LSB corresponds to $0.50\,\text{mA}$ current resolution. | Option A provides $2\times$ higher current measurement precision! |
| **Engineering Decision** | **SELECTED UNANIMOUSLY**: $10.0\,\text{m}\Omega$ satisfies PRD CT-02, perfectly matches LM5176 native $35\,\text{mV}$ clamp, and eliminates all discrete comparator pull-downs. | Rejected due to mismatch with LM5176 native internal trip threshold. |

### 5.5 Output Ceramic Bank & Polymer Filter Capacitors
* **Design Requirement (BB-04)**: Peak-to-peak output ripple voltage $< 25\,\text{mV}$ across full $5.0\,\text{V} - 20.0\,\text{V}$ range at $3.0\,\text{A}$ load.
* **Component Bank Architecture**:
  * **Ceramic MLCC Bank ($C_{\text{OUT\_CER}}$)**: $4\times$ Murata `GRM32ER71E226KE15L` ($22.0\,\mu\text{F} \pm 10\%$, $25\,\text{V}$ DC rating, X7R dielectric, 1210 SMD).
    * Effective capacitance under $20\,\text{V}$ DC bias is $\approx 10.5\,\mu\text{F}$ per cap $\longrightarrow C_{\text{eff,cer}} \approx 42.0\,\mu\text{F}$.
    * Total ESR of 4 parallel MLCCs at $300\,\text{kHz}$ is $< 1.5\,\text{m}\Omega$.
  * **Solid Aluminum Polymer Capacitor ($C_{\text{POLY}}$)**: $1\times$ Panasonic `25SVPF100M` (Series OS-CON SVPF).
    * Capacitance: $100.0\,\mu\text{F} \pm 20\%$, $25\,\text{V}$ DC working voltage, Ultra-low ESR: $12.0\,\text{m}\Omega$ max ($100\,\text{kHz} - 300\,\text{kHz}$), Rated Ripple Current: $3.22\,\text{A}_{\text{RMS}} @ 105^\circ\text{C}$, SMD Radial Can $8 \times 10\,\text{mm}$.
    * Provides deep bulk energy storage during $0\,\text{A} \to 3\,\text{A}$ load transients while MLCCs bypass $300\,\text{kHz}$ switching ripple.
  * *Second Source*: KEMET `A750KK107M1EAAE015` ($100\,\mu\text{F}$, $25\,\text{V}$, $15\,\text{m}\Omega$).

---

## 6. Mixed-Signal Control, Telemetry & User Interface Selections

### 6.1 System Supervisory Microcontroller ($U_5$)
* **Design Requirement**: Coordinates telemetry sampling, closed-loop DAC voltage steering, I2C OLED dashboard, and supervisory protection.
* **Primary Selection**: **STMicroelectronics `STM32G474RET6`**
  * *Parameters*: Arm Cortex-M4 32-bit RISC core with FPU and DSP instructions, operating up to $170\,\text{MHz}$, 512 kB Flash memory with dual-bank read-while-write, 128 kB SRAM with parity check, High-Resolution Timer (HRTIM with $184\,\text{ps}$ resolution), Package: LQFP-64 ($10 \times 10\,\text{mm}$).
  * *On-Chip Analog Peripherals*:
    * 2x 12-bit DAC channels with integrated output buffer amplifier (used for monotonic voltage steering).
    * 5x 12-bit fast ADCs ($4.0\,\text{MSPS}$ interleaved rate) with hardware oversampling up to 16-bit resolution.
    * 7x high-speed rail-to-rail analog comparators ($16.7\,\text{ns}$ response time).
  * *Justification*: The STM32G474 is ST's flagship mixed-signal microcontroller specifically engineered for digital power conversion and smart instrumentation. The internal buffered 12-bit DAC directly drives our summing network with zero external op-amp buffers required.
  * *Second Source*: STMicroelectronics `STM32G473RET6` (identical pinout and peripherals minus HRTIM) or `STM32G484RET6` (adds crypto accelerator).

### 6.2 Secondary Telemetry Power Monitor ($U_6$)
* **Design Requirement (Table 6 #1)**: 16-bit high-precision I2C monitor measuring secondary output voltage, load current, and power at 10 Hz rate.
* **Primary Selection**: **Texas Instruments `INA226AIDGSR`**
  * *Parameters*: Operating Bus Voltage $0.0\,\text{V}$ to $36.0\,\text{V}$ DC, Full-Scale Shunt Differential Voltage $\pm 81.92\,\text{mV}$, 16-bit ADC resolution ($2.5\,\mu\text{V}$ LSB), High-Side or Low-Side sensing, $I^2\text{C}$ / SMBus interface up to $3.4\,\text{MHz}$, Package: VSSOP-10.
  * *Accuracy*: Max Gain Error $\le 0.1\%$, Max Offset Voltage $\le 10\,\mu\text{V}$.
  * *Integration with $10\,\text{m}\Omega$ Shunt*:
    * Full current span: $\pm 81.92\,\text{mV} / 10.0\,\text{m}\Omega = \pm 8.192\,\text{A}$.
    * Current LSB: $\frac{8.192\,\text{A}}{32768} = \mathbf{0.25\,\text{mA}}$ per LSB.
    * Bus Voltage LSB: $1.25\,\text{mV}$ per LSB.
  * *Second Source*: Microchip `PAC1934` (4-channel I2C power monitor) or TI `INA238` ($48\,\text{V}$, 16-bit).

### 6.3 Galvanically Isolated AC Mains Voltage Sensor ($U_4$)
* **Design Requirement (TM-01 / TM-04)**: Galvanically isolated sampling of AC mains voltage ($85\,\text{V} - 265\,\text{V}_{\text{AC}}$) with $3000\,\text{V}_{\text{RMS}}$ safety withstand.
* **Primary Selection**: **Texas Instruments `AMC1311BDWVR`**
  * *Parameters*: Galvanically isolated delta-sigma amplifier, Linear Input Range $0.0\,\text{V}$ to $2.0\,\text{V}$ DC (optimally paired with high-voltage resistive divider), Fixed Gain $A_v = 1.000 \pm 0.3\%$, Working Isolation Voltage $V_{\text{IOWM}} = 1500\,\text{V}_{\text{RMS}}$, Dielectric Withstand $V_{\text{ISO}} = 7000\,\text{V}_{\text{peak}} / 5000\,\text{V}_{\text{RMS}} (1\,\text{min})$, High CMTI $> 75\,\text{kV}/\mu\text{s}$, Package: SOIC-8 Wide ($5.85\,\text{mm}$ creepage / $8.0\,\text{mm}$ clearance).
  * *Input Network*: A $1.5\,\text{M}\Omega$ high-voltage precision divider chain steps down $375\,\text{V}_{\text{peak}}$ AC to $1.875\,\text{V}$ at the AMC1311 input pin. The isolated differential output is referenced to secondary `AGND_SEC` and sampled by STM32 ADC Channel 1.
  * *Second Source*: Silicon Labs `Si8920` (isolated analog amplifier) or Broadcom `ACPL-C79B`.

### 6.4 AC Mains Current Transformer ($\text{CT}_1$)
* **Design Requirement (TM-02)**: Galvanically isolated sampling of primary AC line current ($0.1\,\text{A} - 2.0\,\text{A}_{\text{RMS}}$).
* **Primary Selection**: **Talema `AC1010`** / **CR Magnetics `CR8410-1000`**
  * *Parameters*: Turns Ratio $1000:1$, Nominal Primary Current $10.0\,\text{A}_{\text{RMS}}$, Frequency Range $50\,\text{Hz} - 400\,\text{Hz}$, Dielectric Strength $4000\,\text{V}$ AC RMS, Encapsulated PCB Through-Hole.
  * *Burden Resistor ($R_{\text{burden}}$)*: A precision $100.0\,\Omega \pm 0.1\%$ burden resistor converts the $1.60\,\text{mA}$ secondary current (at $1.60\,\text{A}_{\text{RMS}}$ primary) to $160\,\text{mV}_{\text{RMS}}$ ($452\,\text{mV}_{\text{pk-pk}}$), centered around $+1.65\,\text{V}$ DC bias for unipolar STM32 ADC sampling.

### 6.5 User Interface Dashboard & Controls
* **OLED Display Panel**:
  * $1.3\text{-inch}$ Monochrome Graphic OLED Display, $128 \times 64$ pixels, Solomon Systech `SSD1306` controller, I2C serial interface, 3.3V operating voltage, White pixel emission.
* **Dual Rotary Encoders**:
  * Bourns `PEC11R-4220F-S0024` (24 pulses per revolution, incremental quadrature 2-bit Gray code output, integrated momentary push-button switch, $20\,\text{mm}$ slotted metal shaft, through-hole bracket).
* **Front-Panel Status Indicators**:
  * 3x Kingbright surface-mount LEDs ($0805$ SMD):
    * Green LED: Constant Voltage (CV) Regulating State.
    * Amber LED: Hardware Current Limiting State ($I_{\text{OUT}} \ge 3.5\,\text{A}$).
    * Red LED: Hardware / Supervisory Fault Shutdown State.

### 6.6 Auxiliary Bias Power Supply Tree
To supply low-voltage bias to controllers, gate drivers, and digital circuits without cross-loading the main regulator, an integrated auxiliary power tree is designed:

```
+24.0V Flyback Intermediate Rail
        │
        ├──[ TI LM5164 Buck / L78L12ACUTR ] ──> +12.0V DC (LM5176 VCC Gate Bias)
        │
        └──[ STMicroelectronics L78L05ABUTR ] ──> +5.0V DC (OLED Display VCC)
                │
                └──[ Diodes Inc AP2114H-3.3TRG1 LDO ] ──> +3.3V DC (STM32 MCU VDD, INA226, OLED Logic)
```

| Rail | Nominal Voltage | Max Current | Source Topology | Primary Part Number | Package |
| :---: | :---: | :---: | :--- | :--- | :--- |
| **`+14V_PRI`** | $+14.0\,\text{V}$ DC | $50\,\text{mA}$ | Flyback Primary Aux Winding ($N_{\text{aux}}$) + 1N4148 | Passive rectified winding | PCB Winding |
| **`+12V_SEC`** | $+12.0\,\text{V}$ DC | $100\,\text{mA}$ | Linear Regulator from $+24\,\text{V}$ bus | STMicro `L78L12ACUTR` | SOT-89 |
| **`+5V_SEC`** | $+5.0\,\text{V}$ DC | $150\,\text{mA}$ | Linear Regulator from $+12\,\text{V}$ rail | STMicro `L78L05ABUTR` | SOT-89 |
| **`+3.3V_SEC`**| $+3.3\,\text{V}$ DC | $250\,\text{mA}$ | Low-Dropout Linear Regulator (LDO) from $+5\,\text{V}$ | Diodes Inc `AP2114H-3.3TRG1` | SOT-223 |

---

## 7. Multi-Source Component Qualification Matrix

To guarantee manufacturability and prevent production line stoppages, all critical-path components are matched with pre-qualified second sources:

| Ref Des | Component Description | Primary Manufacturer | Primary MPN | Alternate Manufacturer | Alternate MPN | Pinout Match? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **$F_1$** | Ceramic Fuse 2A 250V Time-Lag | Littelfuse | `0218002.MXP` | Schurter | `0001.2507` | 100% Drop-in |
| **$\text{NTC}_1$** | Inrush Current Thermistor (10Ω/15Ω) | TDK / EPCOS | `B57236S0150M000` | Amphenol Ametherm | `SL15 15003` | 100% Drop-in |
| **$\text{MOV}_1$** | Metal Oxide Varistor 300V RMS | Bourns | `MOV-14D471K` | Littelfuse | `V300LA20AP` | 100% Drop-in |
| **$\text{BR}_1$** | 600V 6A Bridge Rectifier | Diodes Inc. | `GBU606` | Vishay | `GBU6J` | 100% Drop-in |
| **$C_{\text{BULK1}}$** | 100µF 450V 105°C Electrolytic | Nichicon | `LGW2W101MELZ25` | Panasonic | `EEU-ED2W101` | Snap-in 22x25mm |
| **$Q_1$** | 800V CoolMOS P7 Power Switch | Infineon | `IPB80R290P7` | STMicroelectronics | `STP10NK80Z` | D2PAK / TO-220 |
| **$U_1$** | QR Flyback PWM Controller | Texas Instruments| `UCC28740DR` | Texas Instruments | `UCC28C43DR` (fixed) | Alternate Layout |
| **$D_{\text{SEC}}$**| 100V 10A Schottky Rectifier | ON Semi | `MBR10100G` | STMicroelectronics | `STPS10H100D` | 100% Drop-in |
| **$U_3$** | 4-Switch Synchronous Buck-Boost | Texas Instruments| `LM5176PWPR` | Analog Devices | `LTC3789EGN#PBF` | Schematic Alt |
| **$Q_A..Q_D$** | 40V 3.4mΩ N-MOSFETs (4x) | Infineon | `BSC034N04LS` | Texas Instruments | `CSD18534Q5A` | 100% Drop-in |
| **$L_1$** | 10µH 8.5A Flat-Wire Inductor | Wurth Elektronik | `7443321000` | Coilcraft | `SER2915L-103KL` | 100% Drop-in |
| **$R_{\text{shunt}}$**| 10mΩ 3W 0.1% Metal Shunt | Bourns | `CSS2H-2512R-L010F`| Vishay Dale | `WSLP2512R0100FEA`| 100% Drop-in |
| **$C_{\text{OUT}}$**| 22µF 25V X7R 1210 MLCC (4x) | Murata | `GRM32ER71E226KE15L`| TDK | `C3225X7R1E226M250AC`| 100% Drop-in |
| **$C_{\text{POLY}}$**| 100µF 25V 12mΩ Polymer Cap | Panasonic | `25SVPF100M` | KEMET | `A750KK107M1EAAE015` | Radial SMD 8x10 |
| **$U_5$** | 170MHz Mixed-Signal MCU | STMicroelectronics| `STM32G474RET6` | STMicroelectronics | `STM32G473RET6` | 100% Drop-in |
| **$U_6$** | 16-bit I2C Power Monitor | Texas Instruments| `INA226AIDGSR` | Texas Instruments | `INA238AIDGSR` | 100% Drop-in |
| **$U_4$** | Isolated Voltage Sense Amp | Texas Instruments| `AMC1311BDWVR` | Silicon Labs | `Si8920BD-IS` | SOIC-8 Wide |

---
*End of Component Selection & Trade-Off Analysis Document. Companion documents:*
- [01_HDD_DETAILED_IMPLEMENTATION_PLANNING.md](file:///home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/01_HDD_DETAILED_IMPLEMENTATION_PLANNING.md)
- [03_MATHEMATICAL_CALCULATIONS_AND_DERIVATIONS.md](file:///home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/03_MATHEMATICAL_CALCULATIONS_AND_DERIVATIONS.md)
- [04_CLASS_A_BILL_OF_MATERIALS_BOM.md](file:///home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/04_CLASS_A_BILL_OF_MATERIALS_BOM.md)
- [HDD_TRACKING_AND_DESIGN_REVIEW.md](file:///home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/HDD_TRACKING_AND_DESIGN_REVIEW.md)
