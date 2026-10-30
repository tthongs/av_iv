# Smart Programmable Power Supply (SPPS) — Schematic Component & Equivalent Circuit Library

Welcome to the **`components_sch`** engineering repository for the **Smart Programmable Power Supply** (`VVDN_SPPS_2026`). 

This directory contains individual component schematic specification files, pinout-to-net mappings, footprint references, electrical stress ratings, and complete equivalent electronic circuits for each of the 9 functional modules of the SPPS hardware architecture.

---

## 1. Directory Structure & Module Index

```
components_sch/
├── README.md                                         <-- Master Navigation Index (This Document)
├── module_01_mains_input_and_emi_filter/             <-- Stage 1: AC Mains Entry, Surge & 2-Stage CM Filter
├── module_02_bridge_rectifier_and_bulk_dc/           <-- Stage 2: 600V Full-Wave Rectifier & Bulk Link
├── module_03_isolated_flyback_converter/             <-- Stage 3: 65 kHz Isolated Flyback (+24V Intermediate)
├── module_04_buck_boost_post_regulator/              <-- Stage 4: 300 kHz Synchronous 4-Switch Buck-Boost (5-20V / 3A)
├── module_05_fast_hardware_cc_protection/            <-- Stage 5: Sub-5µs Autonomous Analog Hardware Current Clamp
├── module_06_supervisory_mcu_core/                   <-- Stage 6: STM32G474 Mixed-Signal ARM Cortex-M4 Supervisory Core
├── module_07_dual_domain_telemetry/                  <-- Stage 7: Isolated AC Mains & Secondary DC Power Telemetry
├── module_08_auxiliary_power_distribution/           <-- Stage 8: Cascaded Auxiliary Linear Power Tree (+12V/+5V/+3.3V)
└── module_09_user_interface_and_connectors/          <-- Stage 9: 1.3" OLED, Encoders, LEDs, Binding Posts & Headers
```

---

## 2. Master Module & Circuit Map

| Module # | Module Directory | Subsystem Role | Equivalent Circuit Document | Total Components |
| :---: | :--- | :--- | :--- | :---: |
| **01** | [`module_01_mains_input_and_emi_filter`](module_01_mains_input_and_emi_filter/) | Stage 1: Mains Entry & Surge Filter | [`module_01_mains_emi_equivalent_circuit.md`](module_01_mains_input_and_emi_filter/module_01_mains_emi_equivalent_circuit.md) | 6 Files |
| **02** | [`module_02_bridge_rectifier_and_bulk_dc`](module_02_bridge_rectifier_and_bulk_dc/) | Stage 2: Rectification & Bulk Link | [`module_02_bridge_rectifier_bulk_equivalent_circuit.md`](module_02_bridge_rectifier_and_bulk_dc/module_02_bridge_rectifier_bulk_equivalent_circuit.md) | 4 Files |
| **03** | [`module_03_isolated_flyback_converter`](module_03_isolated_flyback_converter/) | Stage 3: Isolated Flyback Converter | [`module_03_isolated_flyback_equivalent_circuit.md`](module_03_isolated_flyback_converter/module_03_isolated_flyback_equivalent_circuit.md) | 7 Files |
| **04** | [`module_04_buck_boost_post_regulator`](module_04_buck_boost_post_regulator/) | Stage 4: Synchronous Buck-Boost | [`module_04_buck_boost_equivalent_circuit.md`](module_04_buck_boost_post_regulator/module_04_buck_boost_equivalent_circuit.md) | 9 Files |
| **05** | [`module_05_fast_hardware_cc_protection`](module_05_fast_hardware_cc_protection/) | Stage 5: Autonomous Current Clamp | [`module_05_fast_cc_protection_equivalent_circuit.md`](module_05_fast_hardware_cc_protection/module_05_fast_cc_protection_equivalent_circuit.md) | 3 Files |
| **06** | [`module_06_supervisory_mcu_core`](module_06_supervisory_mcu_core/) | Stage 6: Supervisory MCU Core | [`module_06_supervisory_mcu_equivalent_circuit.md`](module_06_supervisory_mcu_core/module_06_supervisory_mcu_equivalent_circuit.md) | 5 Files |
| **07** | [`module_07_dual_domain_telemetry`](module_07_dual_domain_telemetry/) | Stage 7: Dual-Domain Telemetry | [`module_07_dual_domain_telemetry_equivalent_circuit.md`](module_07_dual_domain_telemetry/module_07_dual_domain_telemetry_equivalent_circuit.md) | 5 Files |
| **08** | [`module_08_auxiliary_power_distribution`](module_08_auxiliary_power_distribution/) | Stage 8: Auxiliary Power Tree | [`module_08_auxiliary_power_equivalent_circuit.md`](module_08_auxiliary_power_distribution/module_08_auxiliary_power_equivalent_circuit.md) | 3 Files |
| **09** | [`module_09_user_interface_and_connectors`](module_09_user_interface_and_connectors/) | Stage 9: UI, Controls & Headers | [`module_09_user_interface_connectors_equivalent_circuit.md`](module_09_user_interface_and_connectors/module_09_user_interface_connectors_equivalent_circuit.md) | 6 Files |

---

## 3. Comprehensive Component Specification Directory

### Module 01: Mains Input & EMI Filter
* [`J1_iec_c14_inlet.md`](module_01_mains_input_and_emi_filter/J1_iec_c14_inlet.md): Schurter `6100.3300` 10A/250V AC C14 Panel Inlet.
* [`F1_cartridge_fuse.md`](module_01_mains_input_and_emi_filter/F1_cartridge_fuse.md): Littelfuse `0218002.MXP` 2.0A Time-Lag Ceramic Fuse ($I^2t = 19.6\,\text{A}^2\text{s}$) with Keystone 3515 clips.
* [`NTC1_inrush_thermistor.md`](module_01_mains_input_and_emi_filter/NTC1_inrush_thermistor.md): TDK `B57236S0150M000` 15Ω cold thermistor (Limits inrush to $24.98\,\text{A} < 25.0\,\text{A}$).
* [`MOV1_surge_varistor.md`](module_01_mains_input_and_emi_filter/MOV1_surge_varistor.md): Bourns `MOV-14D471K` 300V RMS, 4.5 kA surge clamp (IEC 61000-4-5 Level 3).
* [`L_CM1_L_CM2_common_mode_chokes.md`](module_01_mains_input_and_emi_filter/L_CM1_L_CM2_common_mode_chokes.md): Wurth `744823215` (15 mH) & `744822472` (4.7 mH) 2-stage CM filter.
* [`C_X_C_Y_safety_capacitors.md`](module_01_mains_input_and_emi_filter/C_X_C_Y_safety_capacitors.md): KEMET `R46` Class X2 ($0.22\,\mu\text{F}$) & `PHE850` Class Y1 ($2.2\,\text{nF}$, earth leakage $0.366\,\text{mA}$).
* [`module_01_mains_emi_equivalent_circuit.md`](module_01_mains_input_and_emi_filter/module_01_mains_emi_equivalent_circuit.md): Complete Stage 1 equivalent schematic, attenuation models, and netlist.

### Module 02: Bridge Rectifier & High-Voltage Bulk DC
* [`BR1_gbu606_bridge_rectifier.md`](module_02_bridge_rectifier_and_bulk_dc/BR1_gbu606_bridge_rectifier.md): Diodes Inc. `GBU606` 600V/6A bridge (PIV $375\,\text{V}$, derating $62.5\%$).
* [`C_BULK1_nichicon_bulk_electrolytic.md`](module_02_bridge_rectifier_and_bulk_dc/C_BULK1_nichicon_bulk_electrolytic.md): Nichicon `LGW2W101MELZ25` $100\,\mu\text{F} / 450\,\text{V}$ (Holdup $55.86\,\text{ms}$ at 230V, $12.55\,\text{ms}$ at 85V).
* [`C_HF_murata_high_voltage_ceramic.md`](module_02_bridge_rectifier_and_bulk_dc/C_HF_murata_high_voltage_ceramic.md): Murata `GA342QR7GD102KW01L` $100\,\text{nF} / 630\,\text{V}$ 1812 MLCC high-frequency link bypass.
* [`R_BL1_3_safety_bleeder_resistors.md`](module_02_bridge_rectifier_and_bulk_dc/R_BL1_3_safety_bleeder_resistors.md): Vishay 3x $100\,\text{k}\Omega$ 1206 in series ($300\,\text{k}\Omega$, discharges bulk to $< 50\,\text{V}$ in $44.8\,\text{s}$).
* [`module_02_bridge_rectifier_bulk_equivalent_circuit.md`](module_02_bridge_rectifier_and_bulk_dc/module_02_bridge_rectifier_bulk_equivalent_circuit.md): Complete Stage 2 equivalent schematic, holdup math, and netlist.

### Module 03: Isolated Flyback Converter
* [`U1_flyback_controller.md`](module_03_isolated_flyback_converter/U1_flyback_controller.md): Texas Instruments `UCC28740DR` / `UCC28C43DR` 65 kHz Flyback PWM controller.
* [`TX1_pq2620_flyback_transformer.md`](module_03_isolated_flyback_converter/TX1_pq2620_flyback_transformer.md): Custom PQ26/20 3C95 transformer ($L_p = 220\,\mu\text{H}$, $N_p=36\text{T}$, $N_s=6\text{T}$ TIW, $B_{\text{max}} = 0.152\,\text{T}$).
* [`Q1_ipb80r290p7_coolmos_switch.md`](module_03_isolated_flyback_converter/Q1_ipb80r290p7_coolmos_switch.md): Infineon `IPB80R290P7` 800V/17A CoolMOS ($V_{\text{DS,peak}} = 599\,\text{V}$, derating $74.88\%$).
* [`R_CS1_2_primary_current_sense_shunt.md`](module_03_isolated_flyback_converter/R_CS1_2_primary_current_sense_shunt.md): 2x $0.50\,\Omega$ parallel ($0.25\,\Omega / 2\,\text{W}$) primary current sense shunt.
* [`RCD_snubber_network.md`](module_03_isolated_flyback_converter/RCD_snubber_network.md): `STTH110A` ultrafast diode + 3x $68\,\text{k}\Omega$ parallel ($22.67\,\text{k}\Omega / 3\,\text{W}$) + 2x $3.3\,\text{nF} / 1\,\text{kV}$.
* [`D_SEC_mbr10100g_schottky_rectifier.md`](module_03_isolated_flyback_converter/D_SEC_mbr10100g_schottky_rectifier.md): ON Semi `MBR10100G` 100V/10A Schottky with Aavid 577002 heatsink ($T_j = 79.7^\circ\text{C}$).
* [`secondary_lc_filter_and_tl431_feedback.md`](module_03_isolated_flyback_converter/secondary_lc_filter_and_tl431_feedback.md): 2x $470\,\mu\text{F} / 35\,\text{V}$ + $2.2\,\mu\text{H}$ choke + `TL431ACDBZR` + `EL817` optocoupler.
* [`module_03_isolated_flyback_equivalent_circuit.md`](module_03_isolated_flyback_converter/module_03_isolated_flyback_equivalent_circuit.md): Complete Stage 3 equivalent schematic, magnetics derivations, and netlist.

### Module 04: Buck-Boost Post-Regulator
* [`U3_lm5176_controller.md`](module_04_buck_boost_post_regulator/U3_lm5176_controller.md): Texas Instruments `LM5176PWPR` 4-Switch synchronous controller (HTSSOP-28 PowerPAD).
* [`QA_QD_bsc034n04ls_power_mosfets.md`](module_04_buck_boost_post_regulator/QA_QD_bsc034n04ls_power_mosfets.md): 4x Infineon `BSC034N04LS` (40V, $3.4\,\text{m}\Omega$, $V_{\text{peak}} = 28\,\text{V}$, derating $70.0\%$).
* [`L1_wurth_10uH_flatwire_inductor.md`](module_04_buck_boost_post_regulator/L1_wurth_10uH_flatwire_inductor.md): Wurth `7443321000` $10\,\mu\text{H}$ flat-wire ($I_{\text{sat}} = 11.5\,\text{A}$, $65.2\%$ saturation headroom).
* [`R_shunt_bourns_css2h_10mohm.md`](module_04_buck_boost_post_regulator/R_shunt_bourns_css2h_10mohm.md): Bourns `CSS2H-2512R-L010F` $10.0\,\text{m}\Omega \pm 0.1\%$ 3W metal shunt (4-wire Kelvin taps).
* [`C_OUT_output_filter_bank.md`](module_04_buck_boost_post_regulator/C_OUT_output_filter_bank.md): 4x Murata `GRM32ER71E226K` $22\,\mu\text{F} / 25\,\text{V}$ 1210 MLCCs (Ripple $8.54\,\text{mV}_{\text{pk-pk}} \ll 25\,\text{mV}$).
* [`C_POLY1_panasonic_polymer_cap.md`](module_04_buck_boost_post_regulator/C_POLY1_panasonic_polymer_cap.md): Panasonic `25SVPF100M` $100\,\mu\text{F} / 25\,\text{V}$ solid polymer ($12\,\text{m}\Omega$ ESR, step droop $< 75\,\text{mV}$).
* [`R_STEER_voltage_steering_network.md`](module_04_buck_boost_post_regulator/R_STEER_voltage_steering_network.md): $49.9\,\text{k}\Omega / 4.48\,\text{k}\Omega / 11.0\,\text{k}\Omega \pm 0.1\%$ network ($3.655\,\text{mV}$ DAC step resolution).
* [`COMP_NET_loop_compensation.md`](module_04_buck_boost_post_regulator/COMP_NET_loop_compensation.md): Type-II network ($12.4\,\text{k}\Omega + 82\,\text{nF} + 15\,\text{pF}$) setting $25\,\text{kHz}$ crossover, $65^\circ$ phase margin.
* [`R_T_frequency_setting_resistor.md`](module_04_buck_boost_post_regulator/R_T_frequency_setting_resistor.md): $24.9\,\text{k}\Omega \pm 1\%$ setting fixed $300.0\,\text{kHz}$ PWM frequency.
* [`module_04_buck_boost_equivalent_circuit.md`](module_04_buck_boost_post_regulator/module_04_buck_boost_equivalent_circuit.md): Complete Stage 4 equivalent schematic, 4-switch modes, and netlist.

### Module 05: Fast Hardware CC Protection
* [`U7_FAST_CC_ina240a2_current_amp.md`](module_05_fast_hardware_cc_protection/U7_FAST_CC_ina240a2_current_amp.md): TI `INA240A2EDCKR` ($A_v = 50.0\,\text{V/V}$, $400\,\text{kHz}$, PWM rejection, $0.500\,\text{V/A}$).
* [`U8_FAST_CC_tlv3501_comparator.md`](module_05_fast_hardware_cc_protection/U8_FAST_CC_tlv3501_comparator.md): TI `TLV3501AIDBVR` ($4.5\,\text{ns}$ push-pull comparator with $1.602\,\text{V}$ reference divider).
* [`Q_CLAMP_mmbt3904_transistor.md`](module_05_fast_hardware_cc_protection/Q_CLAMP_mmbt3904_transistor.md): Diodes Inc. `MMBT3904` NPN clamp transistor (Discharges LM5176 `COMP` in $< 250\,\text{ns}$).
* [`module_05_fast_cc_protection_equivalent_circuit.md`](module_05_fast_hardware_cc_protection/module_05_fast_cc_protection_equivalent_circuit.md): Complete Stage 5 equivalent schematic, timing waveform, and total $2.25\,\mu\text{s}$ latency analysis.

### Module 06: Supervisory MCU Core
* [`U5_stm32g474ret6_mcu.md`](module_06_supervisory_mcu_core/U5_stm32g474ret6_mcu.md): STMicroelectronics `STM32G474RET6` 170 MHz Cortex-M4 MCU (64-pin pinout mapping).
* [`Y1_abm8g_24mhz_crystal.md`](module_06_supervisory_mcu_core/Y1_abm8g_24mhz_crystal.md): Abracon `ABM8G` 24.000 MHz crystal ($C_{L1,2} = 27\,\text{pF}$, $R_{\text{damp}} = 47\,\Omega$).
* [`Y2_abs07_32khz_crystal.md`](module_06_supervisory_mcu_core/Y2_abs07_32khz_crystal.md): Abracon `ABS07` 32.768 kHz RTC crystal ($C_{L3,4} = 18\,\text{pF}$).
* [`MCU_DECOUPLING_filters.md`](module_06_supervisory_mcu_core/MCU_DECOUPLING_filters.md): Power supply bypass array ($4x\ 100\,\text{nF} + 4.7\,\mu\text{F}$ bulk) and VDDA pi-filter.
* [`MCU_RESET_CIRCUIT.md`](module_06_supervisory_mcu_core/MCU_RESET_CIRCUIT.md): NRST supervisory RC filter ($10\,\text{k}\Omega + 100\,\text{nF}$, $\tau = 1.0\,\text{ms}$) with manual reset button.
* [`module_06_supervisory_mcu_equivalent_circuit.md`](module_06_supervisory_mcu_core/module_06_supervisory_mcu_equivalent_circuit.md): Complete Stage 6 equivalent schematic, firmware timing loop, and netlist.

### Module 07: Dual-Domain Telemetry
* [`U4_amc1311_isolated_amp.md`](module_07_dual_domain_telemetry/U4_amc1311_isolated_amp.md): TI `AMC1311BDWVR` ($3000\,\text{V}_{\text{RMS}}$ reinforced isolated amplifier, $0-2\,\text{V}$ linear input).
* [`R_DIV_HV_mains_divider.md`](module_07_dual_domain_telemetry/R_DIV_HV_mains_divider.md): High-voltage divider ($3x\ 500\,\text{k}\Omega / 1206 + 7.50\,\text{k}\Omega \pm 0.1\%$, ratio $1:201.0$).
* [`CT1_talema_current_transformer.md`](module_07_dual_domain_telemetry/CT1_talema_current_transformer.md): Talema `AC1010` 1000:1 current transformer ($4000\,\text{V}_{\text{RMS}}$ isolation).
* [`R_burden_resistor.md`](module_07_dual_domain_telemetry/R_burden_resistor.md): Vishay `TNPW0805100R` $100.0\,\Omega \pm 0.1\%$ burden + $1.650\,\text{V}_{\text{DC}}$ midpoint bias divider.
* [`U6_ina226_power_monitor.md`](module_07_dual_domain_telemetry/U6_ina226_power_monitor.md): TI `INA226AIDGSR` 16-bit I2C power monitor ($0.25\,\text{mA}$ current LSB, $1.25\,\text{mV}$ bus LSB).
* [`module_07_dual_domain_telemetry_equivalent_circuit.md`](module_07_dual_domain_telemetry/module_07_dual_domain_telemetry_equivalent_circuit.md): Complete Stage 7 equivalent schematic, RMS/efficiency math models, and netlist.

### Module 08: Auxiliary Power Distribution
* [`U7_REG_l78l12_gate_bias.md`](module_08_auxiliary_power_distribution/U7_REG_l78l12_gate_bias.md): ST `L78L12ACUTR` +12V linear regulator (Powers LM5176 BIAS pin, $T_j = 74.0^\circ\text{C}$).
* [`U8_REG_l78l05_display_rail.md`](module_08_auxiliary_power_distribution/U8_REG_l78l05_display_rail.md): ST `L78L05ABUTR` +5V linear regulator (Powers OLED display logic, $T_j = 72.4^\circ\text{C}$).
* [`U9_REG_ap2114_3v3_ldo.md`](module_08_auxiliary_power_distribution/U9_REG_ap2114_3v3_ldo.md): Diodes Inc. `AP2114H-3.3TRG1` 1.0A LDO (Powers MCU & analog circuitry, $T_j = 57.2^\circ\text{C}$).
* [`module_08_auxiliary_power_equivalent_circuit.md`](module_08_auxiliary_power_distribution/module_08_auxiliary_power_equivalent_circuit.md): Complete Stage 8 equivalent schematic, power dissipation budget, and netlist.

### Module 09: User Interface & Connectors
* [`DISP1_ssd1306_oled.md`](module_09_user_interface_and_connectors/DISP1_ssd1306_oled.md): 1.3" Monochrome I2C OLED ($128 \times 64$, SSD1306 controller at `0x3C`).
* [`ENC1_2_rotary_encoders.md`](module_09_user_interface_and_connectors/ENC1_2_rotary_encoders.md): 2x Bourns `PEC11R-4220F-S0024` rotary encoders with RC debouncing filters.
* [`LED1_3_status_leds.md`](module_09_user_interface_and_connectors/LED1_3_status_leds.md): 3x Kingbright `APT2012` SMD LEDs (Green CV, Amber CC, Red Fault).
* [`J2_J3_binding_posts.md`](module_09_user_interface_and_connectors/J2_J3_binding_posts.md): Pomona `3770-2` (Red) & `3770-0` (Black) $4\,\text{mm}$ safety binding posts ($30\,\text{A} / 1000\,\text{V}$).
* [`J4_swd_header.md`](module_09_user_interface_and_connectors/J4_swd_header.md): Molex `22-28-4040` 4-pin $2.54\,\text{mm}$ shrouded SWD firmware debug header.
* [`J5_uart_header.md`](module_09_user_interface_and_connectors/J5_uart_header.md): Molex `22-28-4030` 3-pin $2.54\,\text{mm}$ UART serial telemetry streaming header.
* [`module_09_user_interface_connectors_equivalent_circuit.md`](module_09_user_interface_and_connectors/module_09_user_interface_connectors_equivalent_circuit.md): Complete Stage 9 equivalent schematic, UI state machine, and netlist.

---

## 4. EDA / Altium Designer Schematic Capture Guidelines

When capturing these circuits into Altium Designer or any professional EDA tool:

1. **Multi-Sheet Hierarchical Architecture**:
   Create a top-level sheet symbol for each of the 9 modules. Use standard hierarchical ports to route power buses (`+HV_BULK`, `+24V_SEC`, `+12V_AUX`, `+5V_SEC`, `+3V3_SEC`, `+V_OUT`) and digital telemetry buses (`I2C1`, `USART1`, `SWD`).
2. **Ground Plane Separation**:
   Strictly isolate the two primary grounding domains:
   * **`PGND_HOT`**: Primary high-voltage hot ground (contains bridge rectifier return, primary flyback FET source, and primary bulk capacitor).
   * **`GND_SELV`**: Secondary isolated safety extra-low voltage ground (contains secondary flyback output, buck-boost power stage, MCU, and binding post negative terminal).
   * Never connect `PGND_HOT` and `GND_SELV` on any copper layer. Maintain $\ge 6.5\,\text{mm}$ physical clearance (IEC 62368-1).
3. **Dedicated Analog Ground Star Point (`AGND_SEC`)**:
   Establish a single-point connection between `AGND_SEC` and `GND_SELV` directly beneath the `LM5176` PowerPAD. All sensitive analog feedback dividers (`R_top`, `R_bot`, `R_DAC`), compensation capacitors, and MCU `VSSA` must return to `AGND_SEC`.
4. **True 4-Wire Kelvin Shunt Routing**:
   Always route `SHUNT_SENSE_P` and `SHUNT_SENSE_N` as a differential pair from the dedicated inside Kelvin pads of Bourns `R_shunt`. Never route load current through the sensing traces.
5. **Net Classes for PCB Layout**:
   * **`HV_POWER`** (`+HV_BULK`, `DRAIN_Q1`): Clearance $\ge 3.0\,\text{mm}$, Trace width $\ge 2.5\,\text{mm}$.
   * **`SEC_POWER`** (`+24V_SEC`, `+V_OUT`, `SW1_NODE`, `SW2_NODE`): 2oz copper polygon pours, $w \ge 4.0\,\text{mm}$.
   * **`GATE_DRIVE`** (`GATE_QA`..`GATE_QD`): Trace width $\ge 0.8\,\text{mm}$, length-matched, routed as tight pairs with switch nodes / power ground.
   * **`PRECISION_ANALOG`** (`LM5176_FB`, `FAST_CC_SENSE`, `MCU_DAC1_OUT1`): Guarded by ground, keep away from high $\frac{dv}{dt}$ switch nodes.
