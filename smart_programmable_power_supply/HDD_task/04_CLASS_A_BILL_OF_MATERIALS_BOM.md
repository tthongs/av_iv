# SPPS Hardware Design Document (HDD) — Class A Engineering Bill of Materials (BOM)

---

### Document Control Information
* **Document Identifier**: `VVDN_SPPS_2026_HDD_BOM_V1.0`
* **Parent Document**: [PRD Final SPPS (`prd_final_spps.docx`)](file:///home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/PRD_task/reference_docs/prd_final_spps.docx)
* **Corporate Standard**: VVDN TP013 V1.1 Hardware Design Document Template (Section 18)
* **Project Code**: `VVDN_SPPS_2026`
* **Project Name**: Smart Programmable Voltage Supply Module (85–265 V AC In, 5–20 V / 3.0 A DC Out)
* **Author / Design Owner**: Hardware Engineering Team / Power Electronics Trainee
* **Review Level**: Level 1 Internal Technical Review / BU SME Review
* **Status**: **Class A Engineering BOM Baseline (Pre-Monolithic HDD Sign-off)**
* **Date**: 21st October 2026

---

## 1. Class A Engineering Bill of Materials Overview

This document presents the complete **Class A Engineering Bill of Materials (BOM)** for the **Smart Programmable Power Supply (SPPS)** module (`VVDN_SPPS_2026`).

Every component is defined with its exact reference designator, comprehensive electrical parameter description, standard footprint, tolerance rating, primary manufacturer part number (MPN), qualified second-source alternate MPN, and subsystem engineering justification.

---

## 2. Master Class A Bill of Materials (BOM) Table

| Item # | Subsystem / Stage | Ref Des | Description | Value / Rating | Tol | Footprint | Primary Mfg | Primary MPN | Alternate Mfg | Alternate MPN | Engineering Justification |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Stage 1: Mains Protection | J_1 | AC Mains Power Inlet | 10 A, 250 V AC | — | IEC 320-C14 Panel | Schurter | `6100.3300` | TE Connectivity | `1-6609987-1` | Earth grounded AC power entry socket. |
| **2** | Stage 1: Mains Protection | F_1 | Ceramic Time-Lag Cartridge Fuse | 2.0 A, 250 V AC, I^2t = 19.6 A^2s | — | 5 × 20 mm Cartridge | Littelfuse | `0218002.MXP` | Schurter | `0001.2507` | Primary short-circuit protection (PR-01). |
| **3** | Stage 1: Mains Protection | FC_1, FC_2| PCB Fuse Clips | For 5 × 20 mm fuse, 10 A | — | Through-Hole | Keystone Electronics | `3515` | Littelfuse | `01110501Z` | Heavy-duty tin-plated phosphor bronze clips. |
| **4** | Stage 1: Mains Protection | NTC_1| Inrush Current Limiting Thermistor | 15.0 Ω Cold, 2.9 A_RMS | ± 20% | Disc varnothing 13 mm Radial | TDK / EPCOS | `B57236S0150M000` | Amphenol Ametherm | `SL15 15003` | Limits cold-start inrush to < 25.0 A (PR-02). |
| **5** | Stage 1: Mains Protection | MOV_1| Metal Oxide Varistor Surge Suppressor| 300 V_RMS, 4.5 kA, 125 J | ± 10% | Disc varnothing 14 mm Radial | Bourns | `MOV-14D471K` | Littelfuse | `V300LA20AP` | IEC 61000-4-5 Level 3 surge clamp. |
| **6** | Stage 1: EMI Filter | L_CM1| Common-Mode Inductor Stage 1 | 15.0 mH, 1.1 A_RMS | ± 30% | Toroid Through-Hole | Wurth Elektronik | `744823215` | KEMET | `SC-10-10J` | Low-frequency 150 kHz - 2 MHz CM EMI attenuation. |
| **7** | Stage 1: EMI Filter | L_CM2| Common-Mode Inductor Stage 2 | 4.7 mH, 1.6 A_RMS | ± 30% | Toroid Through-Hole | Wurth Elektronik | `744822472` | Bourns | `7355-V-RC` | High-frequency 2 MHz - 30 MHz CM EMI attenuation. |
| **8** | Stage 1: EMI Filter | C_X1, C_X2| Safety Class X2 Film Capacitors | 0.22 µF, 310 V AC RMS | ± 20% | Radial Pitch 15.0 mm| KEMET | `R46KI32200001M` | Vishay | `B32922C3224M` | Line-to-neutral differential mode noise filter. |
| **9** | Stage 1: EMI Filter | C_Y1, C_Y2| Safety Class Y1 Ceramic Capacitors | 2.2 nF, 400 V AC RMS | ± 20% | Disc Radial | KEMET | `PHE850ED6220MD15R06L2`| Murata | `DE1E3KX222MA4BP01F`| Line/Neutral to Earth common mode bypass. |
| **10**| Stage 2: Rectifier & Bulk Link| BR_1 | Single-Phase Bridge Rectifier | 600 V, 6.0 A, V_F = 1.0 V | — | GBU Through-Hole | Diodes Incorporated | `GBU606` | Vishay | `GBU6J` | AC full-wave rectification. |
| **11**| Stage 2: Rectifier & Bulk Link| C_BULK1| High-Voltage Bulk Electrolytic Cap | 100 µF, 450 V, 105°C, 3000h | ± 20% | Snap-In varnothing 22 × 25 mm | Nichicon | `LGW2W101MELZ25` | Panasonic | `EEU-ED2W101` | Guarantees > 50 ms holdup at 230 V (> 10 ms req). |
| **12**| Stage 2: Rectifier & Bulk Link| C_HF | High-Voltage Decoupling Ceramic Cap | 100 nF, 630 V DC, X7R | ± 10% | SMD 1812 | Murata | `GA342QR7GD102KW01L`| TDK | `C4532X7R2J104K230KA`| Bypasses primary switching frequency ringing. |
| **13**| Stage 2: Rectifier & Bulk Link| R_BL1..R_BL3| High-Voltage Bleeder Resistors (3x) | 100 kΩ, 0.25 W, 200 V | ± 1% | SMD 1206 | Vishay Dale | `CRCW1206100KFKEA` | Panasonic | `ERJ-8ENF1003V` | Safely discharges bulk cap to < 50 V in < 45 s. |
| **14**| Stage 3: Flyback Subsystem | U_1 | Quasi-Resonant Flyback Controller | Low Standby, Valley Switching | — | SOIC-7 | Texas Instruments | `UCC28740DR` | Texas Instruments | `UCC28C43DR` (Fixed PWM)| Primary Flyback PWM control engine (FR-05 / FR-08). |
| **15**| Stage 3: Flyback Subsystem | TX_1 | Isolated Power Transformer | PQ26/20, L_p = 220 µH ± 10% | — | PQ26/20 Through-Hole | Ferroxcube / Custom | `3C95-PQ2620-72W` | TDK / Epcos | `B66358W0387K187` | 3000V RMS isolated step-down to +24V DC. |
| **16**| Stage 3: Flyback Subsystem | Q_1 | Superjunction CoolMOS P7 N-FET | 800 V, 17.0 A, 0.290 Ω | — | D2PAK (TO-263-3) | Infineon | `IPB80R290P7` | STMicroelectronics | `STP10NK80Z` | Primary high-voltage switching transistor. |
| **17**| Stage 3: Flyback Subsystem | R_CS1, R_CS2| Primary Current Sense Resistors (2x)| 0.50 Ω, 1.0 W (Parallel = 0.25Ω) | ± 1% | SMD 1206 | Vishay Dale | `WSL1206R5000FEA` | Bourns | `CRA2512-FZ-R500ELF` | Senses primary peak current for cycle-by-cycle limit. |
| **18**| Stage 3: Flyback Subsystem | D_snub | Ultra-Fast RCD Snubber Diode | 1000 V, 1.0 A, t_rr < 50 ns | — | DO-214AC (SMA) | STMicroelectronics | `STTH110A` | Vishay | `ES1J` | Clamps primary transformer leakage spike. |
| **19**| Stage 3: Flyback Subsystem | R_snub1..R_snub3| Snubber Resistors (3x in parallel) | 68.0 kΩ, 1.0 W (Net = 22.67kΩ) | ± 1% | SMD 2512 | Panasonic | `ERJ-1TYJ683U` | Vishay Dale | `CRCW251268K0FKEG` | Dissipates leakage inductance energy (P ≈ 2.4 W). |
| **20**| Stage 3: Flyback Subsystem | C_snub1, C_snub2| Snubber Capacitors (2x in parallel) | 3.3 nF, 1000 V DC, X7R | ± 10% | SMD 1206 | Murata | `GRM31BR73A332KW01L`| TDK | `C3216X7R2J332K115AA`| Absorbs primary drain voltage clamp ring. |
| **21**| Stage 3: Flyback Subsystem | D_SEC| Secondary Schottky Barrier Rectifier | 100 V, 10.0 A, V_F = 0.60 V | — | TO-220-2 Through-Hole| ON Semiconductor | `MBR10100G` | STMicroelectronics | `STPS10H100D` | Robust passive secondary rectification to +24V bus. |
| **22**| Stage 3: Flyback Subsystem | HS_1 | Stamped Aluminum Heatsink for D_SEC | 15.0°C/W Thermal Resistance | — | TO-220 Clip Mount | Aavid / Boyd | `577002B00000G` | Ohmite | `FA-T220-38E` | Natural convection cooling for Schottky rectifier. |
| **23**| Stage 3: Flyback Subsystem | C_SEC1, C_SEC2| Secondary Low-ESR Filter Caps (2x) | 470 µF, 35 V, 105°C, 35 mΩ | ± 20% | Radial Can varnothing 10 × 20 mm| Panasonic | `EEU-FC1V471` | Rubycon | `35ZLJ470M10X16` | Intermediate +24V bus bulk filtering. |
| **24**| Stage 3: Flyback Subsystem | L_post| Secondary LC Post-Filter Choke | 2.2 µH, 5.0 A, 18 mΩ | ± 20% | Toroid Through-Hole | Bourns | `2100LL-2R2-H-RC` | Wurth Elektronik | `7447022` | Post-LC ripple attenuation filter (f_c ≈ 3.5 kHz). |
| **25**| Stage 3: Flyback Subsystem | C_SEC_CER| Secondary Decoupling MLCCs (2x) | 10.0 µF, 50 V, X7R | ± 10% | SMD 1210 | Murata | `GRM32ER71H106KA12L`| TDK | `C3225X7R1H106K250AB`| High-frequency bypass for intermediate 24V rail. |
| **26**| Stage 3: Flyback Subsystem | U_2 | Precision Programmable Shunt Ref | 2.495 V ± 0.5%, 100 mA | ± 0.5% | SOT-23-3 | Texas Instruments | `TL431ACDBZR` | ON Semiconductor | `TL431ACDMR2G` | Secondary voltage reference for 24V regulation. |
| **27**| Stage 3: Flyback Subsystem | OPTO_1| Optocoupler Galvanic Isolator | 5000 V_RMS Isolation, CTR 100-200% | — | SMD-4 Gull-Wing | Everlight | `EL817(S)(TA)` | Broadcom | `LTV-817S-TA` | Closed-loop isolated secondary feedback. |
| **28**| Stage 4: Buck-Boost Subsystem | U_3 | 4-Switch Synchronous Buck-Boost Ctrl | 4.2 V - 55 V In, 300 kHz PWM | — | HTSSOP-28 (PowerPAD)| Texas Instruments | `LM5176PWPR` | Analog Devices | `LTC3789EGN#PBF` | Core 4-switch post-regulator controller (BB-01..07). |
| **29**| Stage 4: Buck-Boost Subsystem | Q_A..Q_D| Synchronous Power N-MOSFETs (4x) | 40.0 V, 70 A, R_DS(on) = 3.4 mΩ | — | TDSON-8 (SuperSO8) | Infineon | `BSC034N04LS` | Texas Instruments | `CSD18534Q5A` | Ultra-low loss H-bridge switching bridge. |
| **30**| Stage 4: Buck-Boost Subsystem | L_1 | Flat-Wire High-Current Inductor | 10.0 µH, I_sat = 11.5 A, 13.5 mΩ | ± 20% | SMD 12.5 × 12.5 mm | Wurth Elektronik | `7443321000` | Coilcraft | `SER2915L-103KL` | Energy transfer inductor (> 65% saturation margin). |
| **31**| Stage 4: Buck-Boost Subsystem | R_shunt| Precision Metal Current Sense Shunt | 10.0 mΩ, 3.0 W, TCR < 50 ppm | ± 0.1% | SMD 2512 | Bourns | `CSS2H-2512R-L010F` | Vishay Dale | `WSLP2512R0100FEA` | Native cycle-by-cycle CSP/CSN current limit (PR-03).|
| **32**| Stage 4: Buck-Boost Subsystem | C_OUT1..C_OUT4| Ceramic Output Filter Bank (4x) | 22.0 µF, 25 V DC, X7R | ± 10% | SMD 1210 | Murata | `GRM32ER71E226KE15L`| TDK | `C3225X7R1E226M250AC`| Low ESR switching ripple suppression (< 25 mV). |
| **33**| Stage 4: Buck-Boost Subsystem | C_POLY1| Solid Aluminum Polymer Capacitor | 100.0 µF, 25 V, 12.0 mΩ ESR | ± 20% | Radial SMD 8 × 10 mm| Panasonic | `25SVPF100M` | KEMET | `A750KK107M1EAAE015` | Transient step load reservoir capacitor. |
| **34**| Stage 4: Buck-Boost Subsystem | R_top| Voltage Steering Top Feedback Resistor| 49.9 kΩ, 0.125 W | ± 0.1% | SMD 0805 | Vishay Dale | `TNPW080549K9BEEA` | Panasonic | `ERA-6AEB4992V` | Top divider leg for LM5176 FB node (CT-01). |
| **35**| Stage 4: Buck-Boost Subsystem | R_bot| Voltage Steering Ground Resistor | 4.48 kΩ, 0.125 W | ± 0.1% | SMD 0805 | Vishay Dale | `TNPW08054K48BEEA` | Panasonic | `ERA-6AEB4481V` | Ground leg setting 20.0 V baseline setpoint. |
| **36**| Stage 4: Buck-Boost Subsystem | R_DAC| Voltage Steering DAC Injection Resistor| 11.0 kΩ, 0.125 W | ± 0.1% | SMD 0805 | Vishay Dale | `TNPW080511K0BEEA` | Panasonic | `ERA-6AEB1102V` | Steers V_OUT from 5.0 V to 20.0 V via DAC. |
| **37**| Stage 4: Buck-Boost Subsystem | R_comp, C_comp, C_comp2| Loop Compensation Passive Network | 12.4 kΩ, 82.0 nF, 15.0 pF | ± 1% | SMD 0603 | Vishay / Murata | Standard C0G/X7R | Yageo / TDK | Standard Series | Sets 25 kHz crossover with 65° phase margin. |
| **38**| Stage 4: Buck-Boost Subsystem | R_T | LM5176 Frequency Program Resistor | 24.9 kΩ, 0.1 W | ± 1% | SMD 0603 | Vishay Dale | `CRCW060324K9FKEA` | Panasonic | `ERJ-3EKF2492V` | Sets fixed 300 kHz PWM frequency (BB-06). |
| **39**| Supervisory Brain & UI | U_5 | Mixed-Signal ARM Microcontroller | Cortex-M4 @ 170 MHz, 512kB, 128kB | — | LQFP-64 (10 × 10 mm)| STMicroelectronics | `STM32G474RET6` | STMicroelectronics | `STM32G473RET6` | Coordinates telemetry, DAC steering & OLED UI. |
| **40**| Supervisory Brain & UI | Y_1 | High-Speed External Crystal (HSE) | 24.000 MHz, ± 10 ppm, 18 pF | — | SMD 3.2 × 2.5 mm | Abracon | `ABM8G-24.000MHZ-18-D2Y-T`| TXC Corp | `7M-24.000MAAJ-T` | Primary PLL reference oscillator for STM32. |
| **41**| Supervisory Brain & UI | Y_2 | Low-Speed Real-Time Crystal (LSE) | 32.768 kHz, ± 20 ppm, 12.5 pF| — | SMD 3.2 × 1.5 mm | Abracon | `ABS07-32.768KHZ-T` | Citizen | `CM7V-T1A-32.768KHZ` | Precision 100ms telemetry loop timekeeping. |
| **42**| Supervisory Brain & UI | U_6 | Secondary I2C Power Monitor IC | 16-bit ADC, 0.1% Gain Error, 36 V Bus | — | VSSOP-10 | Texas Instruments | `INA226AIDGSR` | Texas Instruments | `INA238AIDGSR` | Samples secondary V, I, P at 10 Hz rate. |
| **43**| Supervisory Brain & UI | U_4 | Galvanically Isolated Sensing Amp | 3000 V_RMS Isolation, 0-2 V Input | — | SOIC-8 Wide (5.85mm)| Texas Instruments | `AMC1311BDWVR` | Silicon Labs | `Si8920BD-IS` | Samples isolated primary AC mains voltage (TM-01).|
| **44**| Supervisory Brain & UI | CT_1| AC Mains Current Transformer | 1000:1 Ratio, 10 A_RMS, 4000 V_ISO | — | Through-Hole Encapsulated | Talema | `AC1010` | CR Magnetics | `CR8410-1000` | Galvanically senses primary AC line current (TM-02). |
| **45**| Supervisory Brain & UI | R_burden| Precision CT Burden Resistor | 100.0 Ω, 0.25 W | ± 0.1% | SMD 0805 | Vishay Dale | `TNPW0805100RBEEA` | Panasonic | `ERA-6AEB1000V` | Converts 1.6 mA secondary current to voltage. |
| **46**| Supervisory Brain & UI | DISP_1| 1.3" Monochrome OLED Display Module | 128 × 64 Dots, SSD1306, I2C, 3.3V | — | 4-Pin Header / Cable | Solomon / Generic | `OLED-1.3-12864-I2C` | Adafruit | `938` | Local graphical telemetry dashboard. |
| **47**| Supervisory Brain & UI | ENC_1, ENC_2| Incremental Rotary Encoders (2x) | 24 Pulses/Rev, Push Switch, Slotted | — | Through-Hole Bracket | Bourns | `PEC11R-4220F-S0024`| Alps Alpine | `EC11E2424407` | Fine/coarse voltage adjustment and output enable. |
| **48**| Supervisory Brain & UI | LED_1..LED_3| Front-Panel Status Indicators (3x) | Green (CV), Amber (CC), Red (Fault) | — | SMD 0805 | Kingbright | `APT2012SGC / SEC / SRC` | Lite-On | `LTST-C170 Series` | Clear local visual indication of operating state. |
| **49**| Auxiliary Power Tree | U_7 | Linear Regulator +12V Gate Bias | +12.0 V_DC, 100 mA, 35 V_IN | ± 4% | SOT-89 | STMicroelectronics | `L78L12ACUTR` | ON Semiconductor | `MC78L12ABPRPG` | Steps down +24V bus to LM5176 VCC gate bias rail. |
| **50**| Auxiliary Power Tree | U_8 | Linear Regulator +5V OLED Bias | +5.0 V_DC, 100 mA, 30 V_IN | ± 4% | SOT-89 | STMicroelectronics | `L78L05ABUTR` | Texas Instruments | `LM78L05ACMX/NOPB` | Powers 1.3" OLED display logic and analog rails. |
| **51**| Auxiliary Power Tree | U_9 | Low-Dropout Linear Regulator (LDO) | +3.30 V_DC, 1.0 A, Dropout 240 mV| ± 1% | SOT-223 | Diodes Incorporated | `AP2114H-3.3TRG1` | Texas Instruments | `TLV1117-33IDCYR` | Clean, low-noise supply for STM32, INA226, & DAC. |
| **52**| Connectors & Terminals | J_2, J_3| Heavy-Duty 4mm Output Binding Posts | Red (+), Black (-), 30 A, 1000 V | — | 4mm Gold-Plated Panel | Pomona Electronics | `3770-2 (Red) / 3770-0 (Blk)`| Mueller Electric | `BU-P3770-2 / BU-P3770-0` | Standard laboratory 19.05mm spaced binding posts.|
| **53**| Connectors & Terminals | J_4 | SWD Firmware Debug Header | 4-Pin, 2.54 mm Pitch, Shrouded | — | SMD / THT Header | Molex | `22-28-4040` | Samtec | `TSW-104-07-G-S` | Microcontroller programming and real-time debug. |
| **54**| Connectors & Terminals | J_5 | UART Serial Telemetry Header | 3-Pin, 2.54 mm Pitch, Pin Strip | — | Through-Hole Strip | Molex | `22-28-4030` | Samtec | `TSW-103-07-G-S` | Connects TX/RX/GND for 10 Hz external telemetry log.|

---
*End of Class A Engineering Bill of Materials Document. Companion documents:*
- [01_HDD_DETAILED_IMPLEMENTATION_PLANNING.md](file:///home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/01_HDD_DETAILED_IMPLEMENTATION_PLANNING.md)
- [02_COMPONENT_SELECTION_AND_TRADE_OFF_ANALYSIS.md](file:///home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/02_COMPONENT_SELECTION_AND_TRADE_OFF_ANALYSIS.md)
- [03_MATHEMATICAL_CALCULATIONS_AND_DERIVATIONS.md](file:///home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/03_MATHEMATICAL_CALCULATIONS_AND_DERIVATIONS.md)
- [HDD_TRACKING_AND_DESIGN_REVIEW.md](file:///home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/HDD_TRACKING_AND_DESIGN_REVIEW.md)

