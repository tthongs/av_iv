# Component Schematic Specification: U3 (LM5176PWPR Buck-Boost Controller)

## 1. Component Metadata
* **Reference Designator**: `U3`
* **Component Type**: 4-Switch Synchronous Buck-Boost Controller IC
* **Manufacturer**: Texas Instruments
* **Primary MPN**: `LM5176PWPR`
* **Alternate Manufacturer**: Analog Devices
* **Alternate MPN**: `LTC3789EGN#PBF` (functional discrete architecture equivalent)
* **Package / Footprint**: HTSSOP-28 with Exposed Thermal Pad (PowerPAD, Pitch: 0.65 mm, Body: 9.7 × 4.4 mm)
* **Subsystem**: Stage 4 (Synchronous Buck-Boost Post-Regulator)

## 2. Electrical Ratings & Constraints
* **Input Voltage Range ($V_{\text{IN}}$)**: $4.2\,\text{V}$ to $55.0\,\text{V}_{\text{DC}}$ (Continuous maximum rating: $60.0\,\text{V}$)
  * Operating input: $+24.0\,\text{V}_{\text{DC}} \pm 0.8\%$ from isolated Flyback Stage 3.
  * Voltage Derating: $\frac{24.0\,\text{V}}{60.0\,\text{V}} = \mathbf{40.0\%}$ (Well below 75% VVDN maximum limit).
* **Output Voltage Regulation Range**: $5.0\,\text{V}$ to $20.0\,\text{V}_{\text{DC}}$ at $3.0\,\text{A}_{\text{DC}}$ continuous ($60.0\,\text{W}$).
* **Switching Frequency ($f_{\text{sw}}$)**: $300.0\,\text{kHz} \pm 10\%$ programmed via $R_T = 24.9\,\text{k}\Omega \pm 1\%$ to AGND.
* **Internal Reference Voltage ($V_{\text{REF}}$)**: $0.800\,\text{V} \pm 1.0\%$ across full $-40^\circ\text{C}$ to $+125^\circ\text{C}$ temperature span.
* **Gate Drive Capability**:
  * $2.0\,\text{A}$ peak source / $3.0\,\text{A}$ peak sink current.
  * Drives high-side buck FET `QA`, low-side buck sync FET `QB`, low-side boost FET `QC`, and high-side boost sync FET `QD`.
* **Internal Bias Supply ($V_{\text{CC}}$)**: $+7.3\,\text{V}_{\text{DC}}$ typical regulated internal LDO.
  * Supplemented by external $+12.0\,\text{V}_{\text{DC}}$ rail via `BIAS` pin (Pin 28) to bypass internal LDO dissipation and maximize gate-drive slew rates.
* **Operating Modes**:
  * Smooth, automatic transition between Buck mode ($V_{\text{IN}} > V_{\text{OUT}}$: $24\text{V} \to 5\text{V}..19\text{V}$), Buck-Boost boundary mode ($V_{\text{IN}} \approx V_{\text{OUT}} \approx 20\text{V}$), and Boost mode.

## 3. Schematic Pin Connections & Net Mapping
| Pin # | Pin Name | Schematic Net Name | Connected To | Description & Trace Requirements |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **`VISNS`** | `+24V_SEC` | Input ceramic decoupling `C_IN_CER` | Input voltage sense / feedforward; direct Kelvin trace to input rail. |
| **2** | **`EN/UVLO`** | `BUCK_BOOST_EN` | Resistor divider `R_UV1`/`R_UV2` & `Q_EN` collector | Enable & UVLO threshold ($1.22\,\text{V}$). MCU PB0 pulls LOW to shutdown. |
| **3** | **`VOSNS`** | `+V_OUT` | Output filter rail `+V_OUT` | Output voltage sense for mode transitions and OVP. |
| **4** | **`VOUT`** | `+V_OUT` | Output capacitor bank | Internal bias feedback and sense reference. |
| **5** | **`FB`** | `LM5176_FB` | DAC summing junction (`R_top`, `R_bot`, `R_DAC`) | Error amplifier inverting input ($V_{\text{FB}} = 0.800\,\text{V}$). Keep trace $< 5\,\text{mm}$. |
| **6** | **`COMP`** | `LM5176_COMP` | Type-II network (`R_comp`, `C_comp`, `C_comp2`), `Q_CLAMP` | Error amplifier compensation output. Clamped to GND for fast shutdown. |
| **7** | **`SS`** | `LM5176_SS` | Soft-start capacitor $C_{\text{SS}} = 33\,\text{nF}$ | Sets smooth monotonic startup ramp ($t_{\text{ss}} \approx 3.3\,\text{ms}$). |
| **8** | **`RT`** | `LM5176_RT` | Frequency resistor $R_T = 24.9\,\text{k}\Omega$ to `AGND_SEC` | Programs $300\,\text{kHz}$ PWM clock. Short trace to quiet analog ground. |
| **9** | **`MODE`** | `LM5176_MODE`| Pulled to `AGND_SEC` | Sets Forced Continuous Conduction Mode (FCCM) for continuous ripple control. |
| **10**| **`SLOPE`** | `LM5176_SLOPE`| Resistor $R_{\text{SLOPE}} = 100\,\text{k}\Omega$ to `AGND_SEC` | Programs internal slope compensation ramp to eliminate subharmonic oscillation. |
| **11**| **`AGND`** | `AGND_SEC` | Star connection to `GND_SELV` | Quiet analog ground reference; isolate from high $\frac{di}{dt}$ switching loops. |
| **12**| **`CS`** | `LM5176_CS` | Resistor $R_{\text{CS_IN}} = 100\,\Omega$ from Inductor sense | Current sense loop node. |
| **13**| **`CSN`** | `LM5176_CSN` | Shunt resistor `R_shunt` Kelvin Negative pad | Negative input for cycle-by-cycle peak/average current limit. |
| **14**| **`CSP`** | `LM5176_CSP` | Shunt resistor `R_shunt` Kelvin Positive pad | Positive input for current limit (trip threshold = $50\,\text{mV} \to 5.0\,\text{A}$). |
| **15**| **`ILIM`** | `LM5176_ILIM`| Divider from $V_{\text{CC}}$ setting $1.2\,\text{V}$ | Programs internal current limit threshold ($3.50\,\text{A}$ nominal clamp). |
| **16**| **`LDRV2`** | `GATE_QC` | Gate of low-side boost FET `QC` | Low-side boost gate drive pulse ($2.0\,\text{A}$ peak); wide $1.0\,\text{mm}$ trace. |
| **17**| **`PGND`** | `PGND_SEC` | Source of `QB`, `QC`, PowerPAD | Heavy power ground return carrying full inductor circulating currents. |
| **18**| **`HDRV2`** | `GATE_QD` | Gate of high-side boost sync FET `QD` | Floating high-side boost drive pulse; pair with `SW2`. |
| **19**| **`SW2`** | `SW2_NODE` | Switch node 2 (Drain `QC`, Source `QD`, `L1` Pin 2) | High $\frac{dv}{dt}$ switching node ($0\,\text{V}$ to $+20\,\text{V}$). Keep copper area compact. |
| **20**| **`BST2`** | `BST2_NODE` | Bootstrap cap $C_{\text{BST2}} = 100\,\text{nF}$ to `SW2` | High-side boost driver floating supply rail ($V_{\text{SW2}} + 7.3\,\text{V}$). |
| **21**| **`VCC`** | `+7V3_VCC` | Decoupling cap $C_{\text{VCC}} = 4.7\,\mu\text{F} / 16\,\text{V}$ X7R | Internal gate-drive LDO bypass; low ESL ceramic direct to `PGND`. |
| **22**| **`BIAS`** | `+12V_AUX` | Linear regulator `U7` output (+12V rail) | Overdrives internal LDO to supply gate drivers from auxiliary 12V bus. |
| **23**| **`BST1`** | `BST1_NODE` | Bootstrap cap $C_{\text{BST1}} = 100\,\text{nF}$ to `SW1` | High-side buck driver floating supply rail ($V_{\text{SW1}} + 7.3\,\text{V}$). |
| **24**| **`HDRV1`** | `GATE_QA` | Gate of high-side buck FET `QA` | Floating high-side buck drive pulse; pair with `SW1`. |
| **25**| **`SW1`** | `SW1_NODE` | Switch node 1 (Source `QA`, Drain `QB`, `L1` Pin 1) | High $\frac{dv}{dt}$ switching node ($0\,\text{V}$ to $+24\,\text{V}$). Minimize loop area. |
| **26**| **`LDRV1`** | `GATE_QB` | Gate of low-side buck sync FET `QB` | Low-side buck gate drive pulse ($2.0\,\text{A}$ peak); wide $1.0\,\text{mm}$ trace. |
| **27**| **`PGOOD`** | `MCU_PGOOD` | STM32 GPIO `PB1` (with $10\,\text{k}\Omega$ pull-up to 3.3V) | Open-drain Power Good indicator; goes HIGH when $V_{\text{OUT}}$ within $\pm 7\%$. |
| **28**| **`SYNC/EXT`**| `AGND_SEC` | Tied to `AGND_SEC` | Operates on internal free-running $300\,\text{kHz}$ oscillator. |
| **PAD**| **`PowerPAD`**| `PGND_SEC` | Thermal vias to Layer 2 & Layer 4 ground plane | Solder pad ($4.2 \times 2.8\,\text{mm}$) for electrical ground and heat sinking. |

## 4. Schematic Symbol Representation
```
                         [ U3: LM5176PWPR BUCK-BOOST CONTROLLER ]
                                  ┌────────────────────┐
        Net: +24V_SEC  ──────────[1] VISNS             [28] SYNC/EXT  ─── Net: AGND_SEC
    Net: BUCK_BOOST_EN ──────────[2] EN/UVLO           [27] PGOOD     ─── Net: MCU_PGOOD
        Net: +V_OUT    ──────────[3] VOSNS             [26] LDRV1     ─── Net: GATE_QB
        Net: +V_OUT    ──────────[4] VOUT              [25] SW1       ─── Net: SW1_NODE
        Net: LM5176_FB ──────────[5] FB                [24] HDRV1     ─── Net: GATE_QA
      Net: LM5176_COMP ──────────[6] COMP              [23] BST1      ─── Net: BST1_NODE
        Net: LM5176_SS ──────────[7] SS                [22] BIAS      ─── Net: +12V_AUX
        Net: LM5176_RT ──────────[8] RT                [21] VCC       ─── Net: +7V3_VCC
      Net: LM5176_MODE ──────────[9] MODE              [20] BST2      ─── Net: BST2_NODE
     Net: LM5176_SLOPE ──────────[10] SLOPE            [19] SW2       ─── Net: SW2_NODE
        Net: AGND_SEC  ──────────[11] AGND             [18] HDRV2     ─── Net: GATE_QD
        Net: LM5176_CS ──────────[12] CS               [17] PGND      ─── Net: PGND_SEC
       Net: LM5176_CSN ──────────[13] CSN              [16] LDRV2     ─── Net: GATE_QC
       Net: LM5176_CSP ──────────[14] CSP              [15] ILIM      ─── Net: LM5176_ILIM
                                  │                    │
                                  │    [ PowerPAD ]    │
                                  └──────────┬─────────┘
                                             │
                                     Net: PGND_SEC
```

## 5. Schematic & PCB Layout Guidelines
1. **Gate Drive Loop Minimization**: Keep `HDRV1`/`SW1`, `LDRV1`/`PGND`, `HDRV2`/`SW2`, and `LDRV2`/`PGND` traces routed as tight differential pairs on Layer 1 with trace widths $\ge 0.8\,\text{mm}$ to minimize parasitic gate loop inductance ($L_{\text{trace}} < 3\,\text{nH}$).
2. **Kelvin Shunt Routing**: Route `CSP` and `CSN` as a tightly shielded differential pair from the inside Kelvin pads of `R_shunt` directly to Pins 13 and 14 of `U3`. Avoid routing near high $\frac{dv}{dt}$ switch nodes `SW1` and `SW2`.
3. **PowerPAD Soldering**: Place an array of at least 12 thermal vias ($0.3\,\text{mm}$ drill, $0.6\,\text{mm}$ pad) inside the exposed pad area connecting directly to the Layer 2 solid ground plane for effective heat spreading ($\theta_{\text{JA}} \approx 28.5^\circ\text{C/W}$).
4. **Analog Ground Isolation**: Connect `AGND` (Pin 11) to `PGND` (Pin 17) at a single quiet star-point immediately beneath the IC. Decoupling capacitors for `VCC`, `SS`, and `RT` must return directly to `AGND`.
