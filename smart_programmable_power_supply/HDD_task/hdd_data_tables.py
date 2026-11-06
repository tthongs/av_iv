"""
Data tables for VVDN TP013 V1.1 HDD - Smart Programmable Power Supply (VVDN_SPPS_2026).
Matches exact template table schemas.
"""

# Table 0: Amendment History
T0_AMENDMENT = [
    ["29-AUG-19", "V1.0", "First Release", "Perumal S, Sumit Ranjan, Vignesh Babu, Shekhar Saini, Abhishek Kumar Singh, Chetan Singh Rajput"],
    ["28-MAY-20", "V1.1", "Removed CoE reference & Included SME Reference in Signoff Section", "Somnath Shenoy"],
    ["30-OCT-2026", "V1.0", "Initial Production Hardware Design Document release for Smart Programmable Power Supply (SPPS). Conforms strictly to VVDN TP013 V1.1 corporate standard.", "Power Electronics Trainee (GET)"],
    ["06-NOV-2026", "V1.1", "Subsystem enhancement release: Restored isolated AMC1311 + Talema CT dual-domain telemetry, added autonomous MicroSD FAT32 data logging, reconciled 12-bit DAC steering, and updated 58-item Class A BOM.", "Power Electronics Trainee (GET)"]
]

# Table 1: Project Metadata
T1_PROJECT_METADATA = [
    ["Project Code", "VVDN_SPPS_2026"],
    ["Project Name", "Design and Development of a Smart Programmable Voltage Supply Module with 230 V AC Nominal Input (85–265 V AC) and 5–20 V, 3 A Programmable DC Output"],
    ["Revision", "V1.1"],
    ["Date", "06-NOV-2026"]
]

# Table 2: Revision History
T2_REVISION_HISTORY = [
    ["06-NOV-2026", "V1.1", "Production Alignment Release: Restored primary isolated AC mains voltage sense (AMC1311) and current sense (Talema AC1010 CT) for live conversion efficiency computation (eta = P_DC / P_AC); inserted autonomous MicroSD FAT32 continuous data logging subsystem (SPI2 bus, push-push socket J6, Bourns TVS ESD array); verified active 12-bit DAC voltage steering into LM5176 FB node; updated to 1.30-inch OLED display; and expanded Class A BOM to 58 items with 100% RoHS compliance.", "Power Electronics Trainee (GET)", "Senior Hardware Architect", "BU Head (Power Electronics)"],
    ["30-OCT-2026", "V1.0", "Initial Production Hardware Design Document release conforming strictly to VVDN TP013 V1.1 corporate standard. Fully captures 4-stage AC-DC architecture, uniform 65 kHz Flyback, LM5176 synchronous 4-switch Buck-Boost, STM32G474 mixed-signal supervisory core, and preliminary Class A BOM.", "Power Electronics Trainee (GET)", "Senior Hardware Architect", "BU Head (Power Electronics)"],
    ["21-OCT-2026", "V0.9", "Baseline implementation planning, component selection trade-off studies, mathematical derivations, and preliminary Class A BOM.", "Power Electronics Trainee (GET)", "Senior Hardware Architect", "BU SME (Power Electronics)"]
]

# Table 1: Abbreviations (Docx Table 5)
T1_ABBREVIATIONS = [
    ["AC", "Alternating Current"],
    ["ADC", "Analog-to-Digital Converter"],
    ["ANSI", "American National Standards Institute"],
    ["ART", "Adaptive Real-Time Accelerator (STM32 Flash Controller)"],
    ["BOM", "Bill of Materials"],
    ["BOR", "Brown-Out Reset"],
    ["CC", "Constant Current Mode"],
    ["CCM", "Continuous Conduction Mode"],
    ["CISPR", "Comité International Spécial des Perturbations Radioélectriques"],
    ["CMC", "Common-Mode Choke"],
    ["CSV", "Comma-Separated Values Data Format"],
    ["CT", "Current Transformer"],
    ["CV", "Constant Voltage Mode"],
    ["DAC", "Digital-to-Analog Converter"],
    ["DC", "Direct Current"],
    ["DCM", "Discontinuous Conduction Mode"],
    ["DFA", "Design for Assembly"],
    ["DFM", "Design for Manufacturing"],
    ["DVT", "Design Verification Test"],
    ["EMI", "Electromagnetic Interference"],
    ["ESR", "Equivalent Series Resistance"],
    ["FAT32", "32-bit File Allocation Table File System"],
    ["FCC", "Federal Communications Commission"],
    ["FRU", "Field Replaceable Unit"],
    ["HSE", "High-Speed External Clock (Crystal Oscillator)"],
    ["HRTIM", "High-Resolution Timer (STM32 Mixed-Signal Peripheral)"],
    ["I2C", "Inter-Integrated Circuit Serial Bus"],
    ["IAP", "In-Application Programming"],
    ["IEC", "International Electrotechnical Commission"],
    ["ISO", "International Organization for Standardization"],
    ["ISR", "Interrupt Service Routine"],
    ["LDO", "Low-Dropout Linear Regulator"],
    ["LSE", "Low-Speed External Clock (32.768 kHz RTC Crystal)"],
    ["LSB", "Least Significant Bit"],
    ["MLCC", "Multilayer Ceramic Capacitor"],
    ["MOSFET", "Metal-Oxide-Semiconductor Field-Effect Transistor"],
    ["MOV", "Metal Oxide Varistor"],
    ["NTC", "Negative Temperature Coefficient Thermistor"],
    ["OCP", "Over-Current Protection"],
    ["OLED", "Organic Light Emitting Diode Display"],
    ["OTP", "Over-Temperature Protection"],
    ["OVP", "Over-Voltage Protection"],
    ["PCBA", "Printed Circuit Board Assembly"],
    ["PID", "Proportional-Integral-Derivative Digital Controller"],
    ["POR", "Power-On Reset"],
    ["PWM", "Pulse Width Modulation"],
    ["QR", "Quasi-Resonant Switching Mode"],
    ["RDP", "Readout Protection (Flash Security)"],
    ["RMS", "Root Mean Square"],
    ["RoHS", "Restriction of Hazardous Substances"],
    ["SCPI", "Standard Commands for Programmable Instruments"],
    ["SCR", "Silicon-Controlled Rectifier (Crowbar Thyristor)"],
    ["SD", "Secure Digital Memory Card"],
    ["SDIO", "Secure Digital Input Output Interface"],
    ["SELV", "Safety Extra-Low Voltage (< 60 V DC touch-safe domain)"],
    ["SI", "Signal Integrity"],
    ["SMD", "Surface-Mount Device"],
    ["SPI", "Serial Peripheral Interface"],
    ["SPPS", "Smart Programmable Power Supply"],
    ["SRAM", "Static Random-Access Memory"],
    ["SWD", "Serial Wire Debug"],
    ["TUE", "Total Unadjusted Error (ADC Accuracy Metric)"],
    ["TVS", "Transient Voltage Suppressor"],
    ["UART", "Universal Asynchronous Receiver-Transmitter"],
    ["USART", "Universal Synchronous/Asynchronous Receiver-Transmitter"],
    ["UVLO", "Under-Voltage Lockout"],
    ["VVDN", "VVDN Technologies Pvt. Ltd."]
]

# Table 2: References (Docx Table 6)
T2_REFERENCES = [
    ["PRD_SPPS_A1_001", "Product Requirement Document - Smart Programmable Power Supply Module, Rev A1_001, VVDN Technologies, CA / India, Oct 2026."],
    ["VVDN_TP013_V1.1", "Hardware Design Document Template & Standard, TP013 Rev V1.1, VVDN Corporate Quality Management System, May 2020."],
    ["IEC_62368_1_ED3", "Audio/video, information and communication technology equipment - Part 1: Safety requirements, International Electrotechnical Commission, 3rd Edition, 2018."],
    ["CISPR_32_CLASS_B", "Electromagnetic compatibility of multimedia equipment - Emission requirements, CISPR 32 Edition 2.1, 2019."],
    ["FCC_PART_15_B", "Title 47 CFR Part 15 Subpart B - Unintentional Radiators, Class B Digital Device Standards, Federal Communications Commission."],
    ["TI_UCC28740_DS", "UCC28740 Constant-Voltage Constant-Current Flyback Controller with Optocoupled Feedback, Texas Instruments, Rev F, 2020."],
    ["TI_UCC28C43_DS", "UCC28C43 High-Performance BiCMOS Current-Mode PWM Controller, Texas Instruments, Rev F, 2021."],
    ["TI_LM5176_DS", "LM5176 Wide VIN 4-Switch Synchronous Buck-Boost Controller, Texas Instruments, Rev B, 2021."],
    ["ST_STM32G474_DS", "STM32G474xE Arm Cortex-M4 32-bit MCU+FPU, 170 MHz, 512 KB Flash, High-Resolution Timer, STMicroelectronics, Rev 4, 2023."],
    ["TI_AMC1311_DS", "AMC1311 Reinforced Isolated Amplifier with High-Impedance Input for Voltage Sensing, Texas Instruments, Rev C, 2021."],
    ["TALEMA_AC1010_DS", "AC1010 1000:1 Toroidal Current Transformer 4000Vrms Reinforced Isolation, Talema Group, 2020."],
    ["TI_INA226_DS", "INA226 High-Side or Low-Side Measurement, Bi-Directional Current and Power Monitor with I2C, Texas Instruments, Rev A, 2015."],
    ["SD_SPEC_V3", "SD Specifications Part 1 Physical Layer Simplified Specification, Version 3.01, SD Association."],
    ["ELM_FATFS", "FatFs - Generic FAT Filesystem Module for Embedded Systems, ChaN, R0.15, 2023."],
    ["IPC_2221B", "Generic Standard on Printed Board Design, IPC Standard, Rev B, 2012."]
]

# Table 3: Implementation Plan Matrix
T3_IMPLEMENTATION = [
    ["Universal AC Line Input", "85 - 265 V AC RMS (230 V AC Nominal), 47 - 63 Hz operation with integrated surge/inrush protection.", "Stage 1: F1 (2A Time-Lag), RV1 (300V MOV / 4.5kA), RT1 (10Ω NTC inrush). Two-stage CM/DM filter.", "Functional Variac AC sweep (85V to 265V RMS) and surge injection test (1 kV DM / 2 kV CM)."],
    ["Galvanic Safety Isolation", "Reinforced safety isolation >= 3.0 kV AC RMS per IEC 62368-1.", "Stage 3: PQ26/20 transformer TX1 (triple-insulated wire, 6.4 mm physical creepage barrier). Optocouplers U2/U3.", "Hi-Pot dielectric withstand test (3000 V AC for 60 s, leakage < 2 mA)."],
    ["Intermediate DC Bus", "Regulated 24.0 V DC +/- 2.5% intermediate rail (65 W capable).", "Stage 3: UCC28740 quasi-resonant flyback controller (UCC28C43 fixed-PWM alternate), STP10NK80Z MOSFET, 24V secondary output.", "Load step response and efficiency verification over 120V to 375V DC bulk rail."],
    ["Wide Programmable DC Out", "5.0 V to 20.0 V DC continuously adjustable output @ 3.0 A continuous.", "Stage 4: LM5176 synchronous 4-switch buck-boost controller @ 300 kHz with Active 12-bit DAC Voltage Steering (R_DAC = 30.1 kΩ).", "Continuous dynamic sweep from 5.0V to 20.0V DC across 0 to 3.0 A resistive and electronic loads."],
    ["Maximum Output Power", "60.0 W continuous delivery across 5.0 - 20.0 V envelope.", "LM5176 wide VIN/VOUT power stage with Coilcraft SER2918-682KL (6.8 µH / 18A inductor) and solid thermal dissipation.", "Thermal chamber soak at 50°C ambient, 60 W continuous output for 4 hours."],
    ["Low Output Voltage Ripple", "Output voltage peak-to-peak ripple <= 50 mVpp at full 60 W load.", "Stage 4: Low-ESR aluminum polymer capacitors (2x 220 µF / 25V, ESR = 12 mΩ) + secondary ceramic filter (3x 22 µF).", "High-bandwidth oscilloscope measurement with 20 MHz bandwidth limit and tip-and-barrel probe."],
    ["High Conversion Efficiency", "Overall AC-to-DC conversion efficiency >= 85% at nominal load; peak >= 88%.", "Two-stage cascaded architecture: QR Flyback (94.2% eff) + 4-switch Buck-Boost (95.4% eff) -> 88.1% full load.", "Precision power analyzer measurement (Yokogawa WT310E) at 115V AC and 230V AC across load."],
    ["Fast Constant-Current Clamp", "Fast hardware cycle-by-cycle CC clamping response < 5 µs upon short circuit.", "Stage 5: High-speed analog comparator TLV3201 (40 ns) + 10 mΩ Kelvin shunt pulling LM5176 COMP low (< 4.2 µs).", "Dead-short electronic load step with Rogowski current probe verifying clamping in < 4.2 µs."],
    ["Dual-Domain Telemetry & Live Efficiency", "Primary AC voltage/current sensing + secondary DC power monitoring with real-time conversion efficiency computation (eta = P_DC / P_AC) at 10 Hz.", "Stage 7: Isolated AMC1311 (201:1 divider) + Talema AC1010 CT (100Ω burden) + secondary INA226 (10mΩ shunt).", "Multi-point precision calibration against 6.5-digit multimeter (Keysight 34465A) and WT310E power analyzer."],
    ["Autonomous Data Logging", "Continuous time-stamped CSV telemetry logging to FAT32 MicroSD card up to 32 GB.", "Stage 10: Dedicated SPI2 bus to push-push MicroSD socket J6 with Bourns TVS ESD array; FreeRTOS circular ring buffer.", "FAT32 file system verification, continuous 24-hour endurance logging, and SCPI command data retrieval."],
    ["Supervisory Intelligence & Local UI", "ARM Cortex-M4 supervisory core with 12-bit DAC steering and 1.30-inch OLED dashboard.", "Stage 6: STM32G474RET6 (170 MHz, 512KB Flash) driving DAC1, 1.30-inch OLED display (SSD1306/SH1106), and USB-C/UART SCPI.", "Firmware verification of 10 Hz telemetry loop, DAC linearity, OLED frame rate, and SCPI command parsing."],
    ["Multi-Protection Mechanism", "Comprehensive OVP, OCP, OTP, and Mains UVLO protection with latch/auto-restart.", "Hardware comparator OVP crowbar, fast CC clamp, Murata NTC thermal sense, and LM5176 UVLO.", "Fault injection testing across overvoltage, overtemperature, short-circuit, and AC brown-out."],
    ["Conducted & Radiated EMI", "Compliance with CISPR 32 / FCC Part 15 Class B limits.", "Stage 1: Two-stage line filter (FL1 15mH, FL2 4.7mH, X2 caps 220nF/100nF, Y caps 2x 2.2nF) + PCB guard rings.", "LISN conducted emissions scan from 150 kHz to 30 MHz in certified semi-anechoic EMC chamber."]
]

# Table 4: Boot Strapping Pin Table
T4_BOOT_STRAPPING = [
    ["BOOT0", "Pin 60 (PB8/BOOT0)", "Weak Internal Pull-Down (40 kΩ)", "Ground (GND_SEC)", "0 (Logic Low)", "Boot from Main User Flash Memory (0x08000000). Standard production operational mode."],
    ["nBOOT0", "Option Byte (FLASH_OPTR[27])", "Internal Non-Volatile Flash", "Factory Default = 1", "1 (Logic High)", "Forces nBOOT0 active. Ensures processor always boots from internal user Flash on power-on reset."],
    ["nSWBOOT0", "Option Byte (FLASH_OPTR[26])", "Internal Non-Volatile Flash", "Factory Default = 1", "1 (Logic High)", "Selects hardware BOOT0 pin over software bit for deterministic reset state decoding."]
]

# Table 5: RF Radiated Performance (Docx Table 8)
T5_RF_RADIATED = [
    ["30 MHz - 230 MHz", "30.0 dBµV/m (Quasi-Peak @ 10 m)", "23.4 dBµV/m", "+6.6 dB", "Pass (Compliant)"],
    ["230 MHz - 1.0 GHz", "37.0 dBµV/m (Quasi-Peak @ 10 m)", "28.1 dBµV/m", "+8.9 dB", "Pass (Compliant)"],
    ["1.0 GHz - 3.0 GHz", "50.0 dBµV/m (Average @ 3 m)", "36.5 dBµV/m", "+13.5 dB", "Pass (Compliant)"],
    ["3.0 GHz - 6.0 GHz", "54.0 dBµV/m (Average @ 3 m)", "39.2 dBµV/m", "+14.8 dB", "Pass (Compliant)"]
]

# Table 6: Power Sequencing (Docx Table 7)
T6_POWER_SEQUENCING = [
    ["1", "Mains AC Application (85-265V RMS)", "Inrush NTC limits initial current surge <= 16 A peak. Bulk capacitor charges to +120V to +375V DC in <= 15 ms.", "Bulk voltage collapses safely below 50 V DC via discharge bleeder resistors in <= 12.0 s."],
    ["2", "Flyback Controller VCC UVLO Release", "Tertiary winding charges VCC capacitor above 21.0 V UVLO turn-on threshold (soft-start begins).", "Controller terminates switching when VCC falls below 8.1 V UVLO shutdown threshold."],
    ["3", "Intermediate DC Bus Stabilization", "Flyback secondary ramps +24.0 V DC intermediate rail up in 8.0 ms (+/- 2.5% regulation).", "Intermediate rail discharged safely via Buck-Boost bleeder network."],
    ["4", "Secondary Auxiliary Regulators", "TPS7A4700 and AZ1117 LDOs establish quiet +5.0 V and +3.3 V rails in <= 2.0 ms.", "LDO rails decay monotonically without reverse bias or latch-up."],
    ["5", "Supervisory MCU Initialization", "STM32G474 exits POR, configures internal clocks (170 MHz), and reads calibration from EEPROM.", "MCU asserts emergency shutdown pins and saves state to Flash before core voltage decays."],
    ["6", "Active Voltage & Current Steering", "MCU DAC1 outputs commanded setpoint (0-2.45V) into LM5176 FB node; sets current threshold.", "DAC outputs float or reset to safe minimum ground state."],
    ["7", "Buck-Boost Output Power Delivery", "MCU asserts LM5176_ENABLE HIGH; VOUT soft-starts to programmed 5.0 - 20.0 V in <= 5.0 ms.", "LM5176_ENABLE pulled LOW instantly (< 50 ns); discharge FET engages to bleed output."]
]

# Table 7: Subsystem 1 Power Consumption (Docx Table 8)
T7_POWER_CONSUMPTION = [
    ["1", "High-Voltage DC Bulk Bus (+HV_BULK)", "120.0", "325.0", "375.0", "0.22", "0.08"],
    ["2", "Intermediate Flyback Bus (+24V_INT)", "23.4", "24.0", "24.6", "2.71", "0.05"],
    ["3", "Programmable Output Bus (+V_OUT)", "5.0", "12.0", "20.0", "3.00", "0.00"],
    ["4", "Primary Flyback Auxiliary Rail (+14V_PRI)", "12.5", "14.0", "16.0", "0.025", "0.015"],
    ["5", "Secondary Auxiliary Bias (+12V_SEC)", "11.2", "12.0", "12.8", "0.065", "0.020"],
    ["6", "Clean Analog & Core Rail (+3.3V_SEC)", "3.27", "3.30", "3.33", "0.085", "0.012"],
    ["7", "Digital Display Rail (+5V_AUX)", "4.85", "5.00", "5.15", "0.045", "0.005"],
    ["8", "MicroSD Card Logging Rail (+3.3V_SD)", "3.25", "3.30", "3.35", "0.050", "0.001"]
]

# Table 8: Subsystem 1 Power Dissipation (Docx Table 9)
T8_POWER_DISSIPATION = [
    ["1", "Mains EMI Filter & GBU4J Bridge", "230.0", "325.0", "0.32", "97.8", "1.45", "68.06"],
    ["2", "UCC28740 Flyback Stage (TX1, Q1, D2)", "325.0", "24.0", "2.71", "94.2", "3.65", "66.61"],
    ["3", "LM5176 Buck-Boost Stage (L1, Q2-Q5)", "24.0", "20.0", "3.00", "95.4", "2.78", "62.96"],
    ["4", "Auxiliary LDO Regulators (TPS7A, AZ1117)", "24.0", "3.3 / 5.0", "0.12", "68.5", "0.18", "0.57"],
    ["5", "Total Cascaded Power System", "230.0", "20.0", "3.00", "88.1", "8.06", "68.06"]
]

# Table 9: Battery Capacity Calculation (Docx Table 10)
T9_BATTERY_CAPACITY = [
    ["1", "Continuous AC Mains Operation", "60.0 W", "0.0 W (Direct Line)", "Infinite (Continuous AC Line)", "N/A (No Battery Required)"]
]

# Table 10: Power Modes (Docx Table 11)
T10_POWER_MODES = [
    ["1", "Standby / Idle Mode", "AC Line connected; Flyback active (24V rail present); LM5176 disabled; MCU running @ 24 MHz with OLED active.", "0.08 A", "0.14 W", "European CoC Tier 2 / US DoE Level VI Compliant (< 0.15 W)"],
    ["2", "Active CV Regulation Mode", "LM5176 actively regulating output from 5.0 V to 20.0 V DC at load currents up to 3.0 A continuous.", "0.32 A", "68.06 W", "Full-load conversion efficiency = 88.1% (peak = 88.8%)"],
    ["3", "Active Fast CC Clamping Mode", "Output short-circuit or load current > 3.45 A. TLV3201 clamps LM5176 COMP low (< 4.2 µs response).", "0.09 A", "4.20 W", "Safe foldback protection without thermal runaway"],
    ["4", "Fault Latch / Shutdown Mode", "Hardware OVP crowbar fire, sustained overtemperature (> 95°C), or primary brownout. All outputs isolated.", "0.06 A", "0.11 W", "System locks out switching until manual user power reset"],
    ["5", "Telemetry Logging Mode", "Continuous 10 Hz dual-domain AC/DC sampling with FatFs CSV streaming to MicroSD card and SCPI console.", "0.33 A", "68.25 W", "Non-blocking FreeRTOS circular ring buffer operation"]
]

# Table 11: Subsystem 1 Assembly Variants (Docx Table 12)
T11_ASSEMBLY_VARIANTS = [
    ["SPPS-STD-01", "Standard Production Benchtop", "TI UCC28740DR (Quasi-Resonant)", "EPCOS 10.0 Ω (SL10 10003)", "Vishay 10.0 mΩ (WSL2512)", "Standard laboratory benchtop power supply with ultra-low standby power (< 30 mW) and MicroSD logging."],
    ["SPPS-ATE-02", "Automated Test Rack (ATE)", "TI UCC28C43DR (Fixed 65 kHz PWM)", "EPCOS 10.0 Ω (SL10 10003)", "Vishay 10.0 mΩ (WSL2512)", "Optimized for automated multi-channel ATE test racks requiring rigid uniform switching harmonics."],
    ["SPPS-IND-03", "Industrial Extended Temp", "TI UCC28740DR (Quasi-Resonant)", "Ametherm 15.0 Ω (SL15 15002)", "Bourns 10.0 mΩ (CSS2H-2512)", "Harsh industrial environment variant with extended -40°C to +85°C operating thermal boundary."],
    ["SPPS-LOW-04", "Ultra-Low Standby Commercial", "TI UCC28740DR (Quasi-Resonant)", "EPCOS 10.0 Ω (SL10 10003)", "Vishay 10.0 mΩ (WSL2512)", "Energy-star certified model with deep burst-mode sleep capability (< 20 mW idle consumption)."]
]

# Table 12: Subsystem 1 Board Revisions (Docx Table 13)
T12_BOARD_REVISIONS = [
    ["V0.9", "21-OCT-2026", "Preliminary Engineering Prototype", "Proof-of-concept verification of 4-stage cascaded architecture, magnetics, and firmware control loops."],
    ["V1.0", "30-OCT-2026", "Initial Production Release", "Full compliance with VVDN TP013 V1.1 corporate standard. Incorporated monolithic 4-layer PCBA floorplan."],
    ["V1.1", "06-NOV-2026", "Production Telemetry & Storage Alignment", "Restored isolated AMC1311 + Talema CT dual-domain telemetry frontend; integrated MicroSD FAT32 logging; updated to 1.30-inch OLED; finalized 58-item Class A BOM."],
    ["V2.0", "Pending DVT", "Mass Production Tooling Release", "Tooling sign-off incorporating DVT environmental, vibration, and HALT stress testing refinements."]
]

# Table 13: DC Analysis High (Docx Table 14)
T13_DC_HIGH = [
    ["1", "STM32G474RET6 (PA0/EN)", "2.90 V", "8.0 mA", "LM5176 (EN Pin)", "2.00 V", "0.001 mA", "+0.90 V (Adequate Margin)"],
    ["2", "STM32G474RET6 (I2C1/SCL)", "2.90 V", "4.0 mA", "INA226 (SCL Pin)", "2.31 V", "0.005 mA", "+0.59 V (Adequate Margin)"],
    ["3", "STM32G474RET6 (SPI2/SCK)", "3.10 V", "8.0 mA", "MicroSD Socket J6 (CLK)", "2.00 V", "0.010 mA", "+1.10 V (Adequate Margin)"],
    ["4", "STM32G474RET6 (DAC1_OUT1)", "2.45 V", "1.0 mA", "LM5176 (FB Node via R_DAC)", "1.20 V", "0.002 mA", "+1.25 V (Linear Steering)"]
]

# Table 13: DC Analysis Low (Docx Table 15)
T13_DC_LOW = [
    ["1", "STM32G474RET6 (PA0/EN)", "0.40 V", "8.0 mA", "LM5176 (EN Pin)", "0.80 V", "0.001 mA", "+0.40 V (Adequate Margin)"],
    ["2", "STM32G474RET6 (I2C1/SCL)", "0.40 V", "4.0 mA", "INA226 (SCL Pin)", "0.99 V", "0.005 mA", "+0.59 V (Adequate Margin)"],
    ["3", "STM32G474RET6 (SPI2/SCK)", "0.20 V", "8.0 mA", "MicroSD Socket J6 (CLK)", "0.80 V", "0.010 mA", "+0.60 V (Adequate Margin)"],
    ["4", "STM32G474RET6 (DAC1_OUT1)", "0.00 V", "1.0 mA", "LM5176 (FB Node via R_DAC)", "1.20 V", "0.002 mA", "+1.20 V (Zero Offset Sink)"]
]

# Table 14: UART Header J3 (Docx Table 16)
T14_UART_HEADER = [
    ["1", "+3.3V_ISO", "Power", "0.05 A", "1.5 A"],
    ["2", "MCU_TX_DEBUG", "Signal", "115.2 kHz", "10.0 MHz"],
    ["3", "MCU_RX_DEBUG", "Signal", "115.2 kHz", "10.0 MHz"],
    ["4", "GND_ISO", "Power", "0.05 A", "1.5 A"]
]

# Table 15: UART Header Mating (Docx Table 17)
T15_UART_MATING = [
    ["1", "+3.3V_ISO", "Power", "0.05 A", "1.5 A"],
    ["2", "MCU_TX_DEBUG", "Signal", "115.2 kHz", "10.0 MHz"],
    ["3", "MCU_RX_DEBUG", "Signal", "115.2 kHz", "10.0 MHz"],
    ["4", "GND_ISO", "Power", "0.05 A", "1.5 A"]
]

# Table 16: UART Header Cable (Docx Table 18)
T16_UART_CABLE = [
    ["1", "0.05 A", "26 AWG / 0.14 mm^2", "1", "0.05 A"],
    ["2", "115.2 kHz", "26 AWG / 0.14 mm^2", "2", "115.2 kHz"],
    ["3", "115.2 kHz", "26 AWG / 0.14 mm^2", "3", "115.2 kHz"],
    ["4", "0.05 A", "26 AWG / 0.14 mm^2", "4", "0.05 A"]
]

# Table 17: Inter-Subsystem / Expansion Header J4 (Docx Table 19)
T17_EXPANSION_HEADER = [
    ["+5V_AUX", "Power", "0.20 A", "1", "1.5 A", "1", "1.5 A"],
    ["I2C1_SDA", "Signal", "400 kHz", "2", "10.0 MHz", "2", "10.0 MHz"],
    ["I2C1_SCL", "Signal", "400 kHz", "3", "10.0 MHz", "3", "10.0 MHz"],
    ["REMOTE_SENSE+", "Signal", "DC", "4", "1.0 A", "4", "1.0 A"],
    ["REMOTE_SENSE-", "Signal", "DC", "5", "1.0 A", "5", "1.0 A"],
    ["GND_SEC", "Power", "0.20 A", "6", "1.5 A", "6", "1.5 A"]
]

# Table 18: Expansion Header Cable (Docx Table 20)
T18_EXPANSION_CABLE = [
    ["1", "0.20 A", "28 AWG Ribbon", "1", "0.20 A"],
    ["2", "400 kHz", "28 AWG Ribbon", "2", "400 kHz"],
    ["3", "400 kHz", "28 AWG Ribbon", "3", "400 kHz"],
    ["4", "DC Sense", "28 AWG Ribbon", "4", "DC Sense"],
    ["5", "DC Sense", "28 AWG Ribbon", "5", "DC Sense"],
    ["6", "0.20 A", "28 AWG Ribbon", "6", "0.20 A"]
]

# Table 19: Module 1 GPIOs (Docx Table 21) - Sequential 1 to 24 with zero gaps
T19_MODULE1_GPIOS = [
    ["1", "LM5176_ENABLE", "PA0", "Pin 14", "3.3V", "Push-Pull", "3.3V", "Pull-Down (10k)", "0", "0: Buck-Boost Disabled, 1: Buck-Boost Enabled"],
    ["2", "LM5176_PGOOD", "PA1", "Pin 15", "3.3V", "Floating", "3.3V", "Pull-Up (10k)", "0", "0: VOUT Out of Regulation, 1: VOUT In Regulation"],
    ["3", "DISCHARGE_GATE", "PA2", "Pin 16", "3.3V", "Push-Pull", "3.3V", "Pull-Down (100k)", "0", "1: Active Output Capacitor Bleeder FET Turn-on"],
    ["4", "FAST_CC_TRIP", "PA3", "Pin 17", "3.3V", "Floating", "3.3V", "Pull-Down (10k)", "0", "1: Hardware CC Comparator Overcurrent Event (< 5 µs trip)"],
    ["5", "MCU_DAC1_OUT1", "PA4", "Pin 20", "3.3V", "Analog Out", "3.3V", "None", "0.0V", "12-bit Active DAC Voltage Steering into LM5176 FB Node (0-2.45V)"],
    ["6", "ALERT_N", "PA5", "Pin 21", "3.3V", "Floating", "3.3V", "Pull-Up (4.7k)", "1", "0: INA226 Secondary Telemetry Threshold Alert Interrupt"],
    ["7", "STATUS_LED_G", "PB0", "Pin 26", "3.3V", "Push-Pull", "3.3V", "Series Resistor", "0", "1: Green Normal CV Operation LED Illumination"],
    ["8", "STATUS_LED_R", "PB1", "Pin 27", "3.3V", "Push-Pull", "3.3V", "Series Resistor", "0", "1: Red Fault / Warning LED Illumination"],
    ["9", "OLED_RST", "PB2", "Pin 28", "3.3V", "Push-Pull", "3.3V", "Pull-Up (10k)", "1", "0: Hardware Reset Pulse to 1.30-inch OLED Controller"],
    ["10", "SD_CS_N", "PB12", "Pin 33", "3.3V", "Push-Pull", "3.3V", "Pull-Up (100k)", "1", "0: MicroSD Card Select Active Low (SPI2 bus)"],
    ["11", "SD_SCK", "PB13", "Pin 34", "3.3V", "Push-Pull", "3.3V", "Pull-Down (100k)", "0", "SPI2 Serial Clock up to 20 MHz to MicroSD Card J6"],
    ["12", "SD_MISO", "PB14", "Pin 35", "3.3V", "Input", "3.3V", "Pull-Up (47k)", "1", "SPI2 Master-In Slave-Out Data from MicroSD Card J6"],
    ["13", "SD_MOSI", "PB15", "Pin 36", "3.3V", "Push-Pull", "3.3V", "None", "1", "SPI2 Master-Out Slave-In Data to MicroSD Card J6"],
    ["14", "SD_CD_N", "PC6", "Pin 37", "3.3V", "Input", "3.3V", "Pull-Up (10k)", "1", "0: MicroSD Card Detected in Socket J6"],
    ["15", "AMC1311_ADC_IN", "PC0", "Pin 8", "3.3V", "Analog In", "3.3V", "None", "0.0V", "Primary AC Mains Isolated Voltage Telemetry Input (AMC1311 filter)"],
    ["16", "CT_ADC_IN", "PC1", "Pin 9", "3.3V", "Analog In", "3.3V", "None", "1.65V", "Primary AC Mains Current Telemetry Input (Talema AC1010 CT burden)"],
    ["17", "I2C1_SCL", "PB8", "Pin 61", "3.3V", "Open-Drain", "3.3V", "Pull-Up (2.2k)", "1", "Fast-Mode 400 kHz Clock to INA226 & 1.30-inch OLED Display"],
    ["18", "I2C1_SDA", "PB9", "Pin 62", "3.3V", "Open-Drain", "3.3V", "Pull-Up (2.2k)", "1", "Fast-Mode 400 kHz Bidirectional Data to INA226 & OLED"],
    ["19", "USART1_TX", "PA9", "Pin 42", "3.3V", "Push-Pull", "3.3V", "None", "1", "115.2 kbps Serial Console / SCPI Telemetry Output to Header J3"],
    ["20", "USART1_RX", "PA10", "Pin 43", "3.3V", "Input", "3.3V", "Pull-Up (10k)", "1", "115.2 kbps Serial Console / SCPI Command Input from Header J3"],
    ["21", "OVP_LATCH", "PC7", "Pin 38", "3.3V", "Input", "3.3V", "Pull-Down (10k)", "0", "1: Hardware Crowbar SCR Fire (Latched Shutdown Alert)"],
    ["22", "USER_BTN", "PC13", "Pin 2", "3.3V", "Input", "3.3V", "Pull-Up (10k)", "1", "0: Output Enable / Standby Toggle Pushbutton Active"],
    ["23", "SWDIO", "PA13", "Pin 46", "3.3V", "Input", "3.3V", "Pull-Up (100k)", "1", "ARM Serial Wire Debug Data to SWD Programming Header J5"],
    ["24", "SWCLK", "PA14", "Pin 49", "3.3V", "Input", "3.3V", "Pull-Down (100k)", "0", "ARM Serial Wire Debug Clock from SWD Programming Header J5"]
]

# Table 20: Module 1 Interrupts (Docx Table 22) - Sequential 1 to 11 with zero gaps
T20_MODULE1_INTERRUPTS = [
    ["1", "FAST_CC_TRIP", "PA3", "EXTI3_IRQn", "3.3V", "Floating", "3.3V", "Pull-Down (10k)", "Rising Edge", "Hardware CC Comparator Overcurrent Trip (< 5 µs shutdown)"],
    ["2", "OVP_LATCH", "PC7", "EXTI9_5_IRQn", "3.3V", "Floating", "3.3V", "Pull-Down (10k)", "Rising Edge", "Hardware Crowbar SCR Fire (Immediate Latched Off)"],
    ["3", "ALERT_N", "PA5", "EXTI9_5_IRQn", "3.3V", "Floating", "3.3V", "Pull-Up (4.7k)", "Falling Edge", "INA226 Telemetry Alert: Overpower (62.0 W) / Overvoltage"],
    ["4", "PGOOD_EDGE", "PA1", "EXTI1_IRQn", "3.3V", "Floating", "3.3V", "Pull-Up (10k)", "Both Edges", "LM5176 Power Good Status Change ISR"],
    ["5", "USART1_RXNE", "PA10", "USART1_IRQn", "3.3V", "Floating", "3.3V", "Pull-Up (10k)", "Data Ready", "Serial SCPI Telemetry Command Interpreter"],
    ["6", "I2C1_EV", "PB8/9", "I2C1_EV_IRQn", "3.3V", "Open-Drain", "3.3V", "Pull-Up (2.2k)", "Bus Event", "I2C DMA Buffer Transfer Complete (INA226 / OLED)"],
    ["7", "SPI2_DMA_TC", "PB13-15", "DMA1_CH3_IRQn", "3.3V", "Internal", "3.3V", "None", "Transfer Complete", "MicroSD 512-Byte Sector Buffer Write Complete ISR"],
    ["8", "SD_CD_EXTI", "PC6", "EXTI9_5_IRQn", "3.3V", "Floating", "3.3V", "Pull-Up (10k)", "Both Edges", "MicroSD Card Insertion / Removal Detection ISR"],
    ["9", "ADC1_DMA_TC", "PC0/PC1", "DMA1_CH1_IRQn", "3.3V", "Internal", "3.3V", "None", "Half/Full Complete", "Dual-Domain AC Telemetry Sampling Buffer Ready (10 Hz RMS Engine)"],
    ["10", "TIM1_UP", "Internal", "TIM1_UP_IRQn", "3.3V", "Internal", "3.3V", "Internal", "Periodic", "Supervisory Control Loop: 100 kHz PID Fine Trimming"],
    ["11", "SYSTICK", "Internal", "SysTick_IRQn", "3.3V", "Internal", "3.3V", "Internal", "1 ms Tick", "FreeRTOS Kernel Tick & Periodic Telemetry State Machine"]
]

# Table 21: Programmable ROM (Docx Table 23)
T21_PROGRAMMABLE_ROM = [
    ["Subsystem 1 (Main PCBA)", "STM32G474RET6 Internal Flash (512 KB)", "Stores master firmware executable, FreeRTOS kernel, USB/UART SCPI protocol stack, FatFs middleware, and telemetry math algorithms. Dual-bank layout allows robust In-Application Programming (IAP)."],
    ["Subsystem 1 (Main PCBA)", "STM32G474RET6 System Memory ROM (32 KB)", "Factory programmed by STMicroelectronics with standard DFU bootloader supporting UART, I2C, and USB in-system programming."],
    ["Subsystem 1 (Main PCBA)", "Emulated EEPROM (Sector 7, 16 KB)", "Non-volatile storage for factory calibration constants (voltage divider gain/offset, shunt calibration trim, serial number, FRU data, fault logs)."],
    ["Subsystem 1 (Main PCBA)", "Option Bytes Flash Register (1 KB)", "Non-volatile hardware security fuses: Readout Protection (RDP Level 1), hardware watchdog enable, and BOOT0 hardware strapping selection."],
    ["Subsystem 1 (Main PCBA)", "MicroSD Removable Flash Card (4 GB - 32 GB)", "External non-volatile storage for continuous time-stamped CSV telemetry logging (Timestamp, V_AC, I_AC, P_AC, PF, V_OUT, I_OUT, P_OUT, efficiency, temperature, mode, fault flags) formatted with FAT32."]
]

# Table 22: Class A BOM (Docx Table 24) - Sequential 1 to 58 with zero gaps
T22_CLASS_A_BOM = [
    ["1", "Fuse Time-Lag 2.0A 250V Ceramic SMD", "1", "Littelfuse", "0477002.MXEP", "C", "Yes", "-55°C to +125°C"],
    ["2", "MOV Metal Oxide Varistor 300V RMS 4.5kA", "1", "EPCOS / TDK", "B72210S0301K101", "C", "Yes", "-40°C to +105°C"],
    ["3", "NTC Thermistor Inrush Limiter 10 Ohm 3.2A", "1", "Ametherm", "SL10 10003", "C", "Yes", "-40°C to +125°C"],
    ["4", "Film Capacitor X2 Safety 220nF 310VAC 10%", "1", "KEMET", "R46KR422000M1M", "C", "Yes", "-40°C to +110°C"],
    ["5", "Common-Mode Choke 2x 15mH 1.8A Nanocrystalline", "1", "Wurth Elektronik", "744824150", "C", "Yes", "-40°C to +125°C"],
    ["6", "Film Capacitor X2 Safety 100nF 310VAC 10%", "1", "KEMET", "R46KR410000M1M", "C", "Yes", "-40°C to +110°C"],
    ["7", "Common-Mode Choke 2x 4.7mH 2.2A Ferrite", "1", "Wurth Elektronik", "744823247", "C", "Yes", "-40°C to +125°C"],
    ["8", "Safety Capacitor Y1/Y2 Ceramic 2.2nF 250VAC", "2", "Murata", "DE1E3KX222MA4BP01F", "C", "Yes", "-40°C to +125°C"],
    ["9", "Glass Passivated Bridge Rectifier 600V 4A GBU", "1", "Diodes Inc.", "GBU4J", "C", "Yes", "-55°C to +150°C"],
    ["10", "Aluminum Electrolytic Capacitor 82uF 450V 105C", "1", "Nichicon", "LGX2W820MELA30", "C", "Yes", "-40°C to +105°C"],
    ["11", "Constant-Voltage QR Flyback Controller SOIC-7", "1", "Texas Instruments", "UCC28740DR", "I", "Yes", "-40°C to +125°C"],
    ["12", "N-Channel Power MOSFET 800V 9A TO-220", "1", "STMicroelectronics", "STP10NK80Z", "C", "Yes", "-55°C to +150°C"],
    ["13", "Flyback Transformer PQ26/20 220uH Custom", "1", "Wurth Elektronik / Custom", "WE-750316821", "C", "Yes", "-40°C to +125°C"],
    ["14", "Ultrafast Recovery Diode 1000V 1A SMA", "1", "Vishay", "ES1J-E3/61T", "C", "Yes", "-55°C to +150°C"],
    ["15", "TVS Diode Transient Suppressor 180V 600W SMB", "1", "Littelfuse", "SMBJ180A", "C", "Yes", "-55°C to +150°C"],
    ["16", "Optocoupler Transistor Output 5000Vrms 4-SMD", "2", "Broadcom", "ACPL-217-500E", "C", "Yes", "-55°C to +110°C"],
    ["17", "Schottky Barrier Diode 100V 20A Dual TO-220AB", "1", "Diodes Inc.", "MBR20100CT", "C", "Yes", "-65°C to +175°C"],
    ["18", "Aluminum Electrolytic Capacitor 470uF 35V Low-ESR", "2", "Panasonic", "EEU-FR1V471", "C", "Yes", "-40°C to +105°C"],
    ["19", "Multilayer Ceramic Capacitor 10uF 50V X7R 1210", "4", "TDK", "C3225X7R1H106K250AC", "C", "Yes", "-55°C to +125°C"],
    ["20", "Wide VIN 4-Switch Buck-Boost Controller HTSSOP-28", "1", "Texas Instruments", "LM5176PWPR", "I", "Yes", "-40°C to +125°C"],
    ["21", "N-Channel MOSFET 100V 100A SuperSO8 BSC", "4", "Infineon", "BSC035N10NS5", "C", "Yes", "-55°C to +150°C"],
    ["22", "High-Current Power Inductor 6.8uH 18A SMD", "1", "Coilcraft", "SER2918-682KL", "C", "Yes", "-40°C to +125°C"],
    ["23", "Current Sense Resistor 10 mOhm 3W 1% 2512", "1", "Vishay Dale", "WSL2512R0100FEA", "C", "Yes", "-65°C to +170°C"],
    ["24", "Aluminum Polymer Capacitor 220uF 25V 12mOhm SMD", "2", "KEMET", "A750KK227M1EAAE012", "C", "Yes", "-55°C to +105°C"],
    ["25", "Multilayer Ceramic Capacitor 22uF 25V X7R 1210", "3", "Murata", "GRM32ER71E226KE15L", "C", "Yes", "-55°C to +125°C"],
    ["26", "High-Speed Analog Comparator 40ns SOT-23-5", "1", "Texas Instruments", "TLV3201AIDBVR", "C", "Yes", "-40°C to +125°C"],
    ["27", "N-Channel MOSFET Small-Signal 60V 300mA SOT-23", "2", "Diodes Inc.", "2N7002K", "C", "Yes", "-55°C to +150°C"],
    ["28", "Bipolar Power Transistor Disconnector 30V 5A SOT-223", "1", "Diodes Inc.", "FZT851TA", "C", "Yes", "-55°C to +150°C"],
    ["29", "ARM Cortex-M4 Mixed-Signal MCU 170MHz LQFP-64", "1", "STMicroelectronics", "STM32G474RET6", "I", "Yes", "-40°C to +85°C"],
    ["30", "Quartz Crystal Resonator 24.000MHz 18pF SMD", "1", "Abracon", "ABM8G-24.000MHZ-B4Y-T", "C", "Yes", "-40°C to +85°C"],
    ["31", "Ceramic Load Capacitor 18pF 50V C0G 0603", "2", "Murata", "GRM1885C1H180JA01D", "C", "Yes", "-55°C to +125°C"],
    ["32", "High-Side/Low-Side Power Monitor I2C VSSOP-10", "1", "Texas Instruments", "INA226AIDGSR", "I", "Yes", "-40°C to +125°C"],
    ["33", "Precision Isolated Amplifier 7000Vpk SOIC-8", "1", "Texas Instruments", "AMC1311BDWVR", "I", "Yes", "-40°C to +125°C"],
    ["34", "Toroidal Current Transformer 1000:1 4000Vrms PCB", "1", "Talema", "AC1010", "C", "Yes", "-40°C to +120°C"],
    ["35", "Precision Metal Film Resistor 100 Ohm 0.1% 0805", "1", "Vishay Beyschlag", "MBB02070C1000FCT00", "C", "Yes", "-55°C to +125°C"],
    ["36", "High-Voltage Thick Film Resistor 500 kOhm 0.1% 1206", "3", "Vishay Techno", "CRCW1206500KFKEAHP", "C", "Yes", "-55°C to +155°C"],
    ["37", "Precision Divider Resistor 7.50 kOhm 0.1% 0805", "1", "Vishay Beyschlag", "MBB02070C7501FCT00", "C", "Yes", "-55°C to +125°C"],
    ["38", "Push-Push MicroSD Card Socket SMD 8-Pin", "1", "Amphenol ICC", "10100303-68211LF", "C", "Yes", "-40°C to +85°C"],
    ["39", "4-Channel Low-Capacitance TVS Diode Array DFN-10", "1", "Bourns", "CDDFN10-0524P", "C", "Yes", "-55°C to +85°C"],
    ["40", "Ultra-Low-Noise LDO Regulator 3.3V 1A QFN-20", "1", "Texas Instruments", "TPS7A4700QRGWRQ1", "A", "Yes", "-40°C to +125°C"],
    ["41", "Positive Voltage Regulator LDO 5.0V 1A SOT-223", "1", "Diodes Inc.", "AZ1117EH-5.0TRG1", "C", "Yes", "-40°C to +125°C"],
    ["42", "Precision Resistor 30.1 kOhm 0.1% 0805 (DAC Injection)", "1", "Vishay Beyschlag", "MBB02070C3012FCT00", "C", "Yes", "-55°C to +125°C"],
    ["43", "Precision Feedback Resistor 19.1 kOhm 0.1% 0805", "1", "Vishay Beyschlag", "MBB02070C1912FCT00", "C", "Yes", "-55°C to +125°C"],
    ["44", "Precision Ground Resistor 1.21 kOhm 0.1% 0805", "1", "Vishay Beyschlag", "MBB02070C1211FCT00", "C", "Yes", "-55°C to +125°C"],
    ["45", "NTC Thermistor Sensor 10 kOhm 1% 0603", "1", "Murata", "NCP18XH103F03RB", "C", "Yes", "-40°C to +125°C"],
    ["46", "1.30-inch Monochrome OLED Display Module 128x64 I2C", "1", "Waveshare / Solomon Systech", "SH1106-1.30-I2C", "C", "Yes", "-40°C to +85°C"],
    ["47", "AC Mains Terminal Block 3-Pos 5.08mm Rising Cage", "1", "Phoenix Contact", "1757255", "C", "Yes", "-40°C to +105°C"],
    ["48", "DC Output Binding Posts Dual Heavy-Duty Banana", "1", "Pomona Electronics", "6883", "C", "Yes", "-55°C to +115°C"],
    ["49", "Isolated Debug Header 4-Pin 2.54mm Friction Lock", "1", "Molex", "0022013047", "C", "Yes", "-40°C to +105°C"],
    ["50", "SWD Programming Header 5-Pin 1.27mm Micro-Pitch", "1", "Samtec", "FTSH-105-01-L-DV", "C", "Yes", "-55°C to +125°C"],
    ["51", "Ceramic Bypass Capacitor 100nF 50V X7R 0603", "24", "TDK", "C1608X7R1H104K080AA", "C", "Yes", "-55°C to +125°C"],
    ["52", "Ceramic Decoupling Capacitor 1uF 25V X7R 0805", "8", "Murata", "GRM21BR71E105KA99L", "C", "Yes", "-55°C to +125°C"],
    ["53", "Standard Chip Resistor 10 kOhm 1% 0603", "14", "Yageo", "RC0603FR-0710KL", "C", "Yes", "-55°C to +125°C"],
    ["54", "Standard Chip Resistor 4.7 kOhm 1% 0603", "6", "Yageo", "RC0603FR-074K7L", "C", "Yes", "-55°C to +125°C"],
    ["55", "Gate Drive Damping Resistor 4.7 Ohm 1% 0805", "4", "Panasonic", "ERJ-6GEYJ4R7V", "C", "Yes", "-55°C to +125°C"],
    ["56", "Green Status LED 565nm 20mA 0805 SMD", "1", "Lite-On", "LTST-C170GKT", "C", "Yes", "-55°C to +105°C"],
    ["57", "Red Fault LED 630nm 20mA 0805 SMD", "1", "Lite-On", "LTST-C170CKT", "C", "Yes", "-55°C to +105°C"],
    ["58", "Silicon Power SCR Crowbar Thyristor 400V 8A DPAK", "1", "STMicroelectronics", "TN805-600B-TR", "C", "Yes", "-40°C to +125°C"]
]

# Table 23: Requirement - Design Mapping (Docx Table 25)
T23_REQ_MAPPING = [
    ["CR-PWR-001", "HW-PWR-001", "Section 2, Section 8.3 (Mains Input Stage & Protection)"],
    ["CR-PWR-002", "HW-PWR-002", "Section 4.1, Section 8.4 (AC Mains Power Factor & Voltage Envelope)"],
    ["CR-PWR-003", "HW-PWR-003", "Section 4.2, Section 5.1.2, Section 8.1 (LM5176 Buck-Boost Output Range)"],
    ["CR-PWR-004", "HW-PWR-004", "Section 4.2, Section 8.1.2 (Continuous Output Power & Current Envelope)"],
    ["CR-PWR-005", "HW-PWR-005", "Section 4.2, Section 8.1.3 (Output Voltage Ripple & Low-ESR Polymer Filter)"],
    ["CR-PWR-006", "HW-PWR-006", "Section 8.1.3, Section 13.6 (System Efficiency & Thermal Loss Budget)"],
    ["CR-PROT-001", "HW-PROT-001", "Section 7.1.1, Section 8.3 (Hardware OVP Crowbar & Latch Circuit)"],
    ["CR-PROT-002", "HW-PROT-002", "Section 7.1.2, Section 8.3, Section 16.1 (Fast Hardware CC Comparator Clamping)"],
    ["CR-PROT-003", "HW-PROT-003", "Section 7.1.3, Section 8.3 (NTC Thermal Sensing & Overtemp Protection)"],
    ["CR-PROT-004", "HW-PROT-004", "Section 8.3 (Primary Line Under-Voltage Lockout UVLO)"],
    ["CR-ISO-001", "HW-ISO-001", "Section 2, Section 4.1, Section 13.5 (Reinforced Safety Isolation Barrier)"],
    ["CR-TEL-001", "HW-TEL-001", "Section 4.2, Section 7.1.4 (Dual-Domain Telemetry: Isolated AMC1311, Talema CT1, and Secondary INA226)"],
    ["CR-TEL-002", "HW-TEL-002", "Section 5.1.1, Section 13.1.2 (10 Hz Telemetry Update Rate & Fast-Mode I2C)"],
    ["CR-TEL-003", "HW-TEL-003", "Section 4.2, Section 7.1.4, Section 8.1.3 (Real-Time Live Efficiency Monitoring Engine eta = P_DC / P_AC)"],
    ["CR-LOG-001", "HW-LOG-001", "Section 4.2, Section 5.1.3, Section 14.1.6, Section 17 (Autonomous MicroSD FAT32 Data Logging & CSV Record Engine)"],
    ["CR-CTL-001", "HW-CTL-001", "Section 5.1.1, Section 7.1.2 (12-bit Active DAC Voltage/Current Steering into FB Node)"],
    ["CR-UI-001", "HW-UI-001", "Section 4.2, Section 5.1.1 (1.30-inch OLED Interface & Status LEDs)"],
    ["CR-DBG-001", "HW-DBG-001", "Section 5.1.1, Section 14.1.1 (SWD Debug Header & Isolated UART J3)"],
    ["CR-EMC-001", "HW-EMC-001", "Section 6.1.1, Section 13.4 (Conducted EMI Attenuation & 2-Stage Filter)"],
    ["CR-EMC-002", "HW-EMC-002", "Section 6.1.1, Section 13.5 (Radiated Emissions Shielding & Layout Isolation)"],
    ["CR-ENV-001", "HW-ENV-001", "Section 1.2, Section 13.6 (Operating Ambient Temperature -10°C to +50°C)"],
    ["CR-ENV-002", "HW-ENV-002", "Section 13.6 (Passive Natural Convection Cooling Without Fan)"],
    ["CR-MECH-001", "HW-MECH-001", "Section 4.1, Section 13.5 (140 mm x 90 mm PCB Enclosure Envelope)"],
    ["CR-REL-001", "HW-REL-001", "Section 1.2, Section 13.6, Section 18 (VVDN Component Derating Guidelines)"]
]
