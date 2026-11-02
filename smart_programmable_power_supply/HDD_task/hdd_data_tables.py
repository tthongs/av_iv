"""
Data tables for VVDN TP013 V1.1 HDD - Smart Programmable Power Supply (VVDN_SPPS_2026).
Matches exact template table schemas.
"""

# Table 0: Amendment History
T0_AMENDMENT = [
    ["29-AUG-19", "V1.0", "First Release", "Perumal S, Sumit Ranjan, Vignesh Babu, Shekhar Saini, Abhishek Kumar Singh, Chetan Singh Rajput"],
    ["28-MAY-20", "V1.1", "Removed CoE reference & Included SME Reference in Signoff Section", "Somnath Shenoy"],
    ["30-OCT-2026", "V1.0", "Initial Production Hardware Design Document release for Smart Programmable Power Supply (SPPS). Conforms strictly to VVDN TP013 V1.1 corporate standard.", "Power Electronics Trainee (GET)"]
]

# Table 1: Project Metadata
T1_PROJECT_METADATA = [
    ["Project Code", "VVDN_SPPS_2026"],
    ["Project Name", "Smart Programmable Power Supply (SPPS) Module"],
    ["Revision", "V1.0"],
    ["Date", "30-OCT-2026"]
]

# Table 2: Revision History
T2_REVISION_HISTORY = [
    ["30-OCT-2026", "V1.0", "Initial Production Hardware Design Document release conforming strictly to VVDN TP013 V1.1 corporate standard. Fully captures 4-stage AC-DC architecture, uniform 65 kHz Flyback, LM5176 synchronous 4-switch Buck-Boost, STM32G474 mixed-signal supervisory core, dual-domain power telemetry, and 54-item Class A BOM.", "Power Electronics Trainee (GET)", "Senior Hardware Architect", "BU Head (Power Electronics)"],
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
    ["CV", "Constant Voltage Mode"],
    ["DAC", "Digital-to-Analog Converter"],
    ["DC", "Direct Current"],
    ["DCM", "Discontinuous Conduction Mode"],
    ["DFA", "Design for Assembly"],
    ["DFM", "Design for Manufacturing"],
    ["DVT", "Design Verification Test"],
    ["EMI", "Electromagnetic Interference"],
    ["ESR", "Equivalent Series Resistance"],
    ["FCC", "Federal Communications Commission"],
    ["FRU", "Field Replaceable Unit"],
    ["HSE", "High-Speed External Clock (Crystal Oscillator)"],
    ["I2C", "Inter-Integrated Circuit Bus"],
    ["IEC", "International Electrotechnical Commission"],
    ["IEEE", "Institute of Electrical and Electronics Engineers"],
    ["IWDG", "Independent Watchdog Timer"],
    ["LDO", "Low-Dropout Linear Regulator"],
    ["MOV", "Metal Oxide Varistor"],
    ["MPN", "Manufacturer Part Number"],
    ["NTC", "Negative Temperature Coefficient Thermistor"],
    ["OCP", "Over-Current Protection"],
    ["OLED", "Organic Light Emitting Diode Display"],
    ["OTP", "Over-Temperature Protection"],
    ["OVP", "Over-Voltage Protection"],
    ["PCB", "Printed Circuit Board"],
    ["PCBA", "Printed Circuit Board Assembly"],
    ["PFC", "Power Factor Correction"],
    ["PGOOD", "Power Good Indicator Signal"],
    ["POR", "Power-On Reset"],
    ["PWM", "Pulse Width Modulation"],
    ["QR", "Quasi-Resonant Switching Mode"],
    ["RMS", "Root Mean Square"],
    ["RoHS", "Restriction of Hazardous Substances"],
    ["SOA", "Safe Operating Area"],
    ["SPPS", "Smart Programmable Power Supply"],
    ["SR", "Synchronous Rectification"],
    ["SWD", "Serial Wire Debug Port"],
    ["THD", "Total Harmonic Distortion"],
    ["UART", "Universal Asynchronous Receiver-Transmitter"],
    ["UVLO", "Under-Voltage Lockout"],
    ["WWDG", "Window Watchdog Timer"]
]

# Table 2: References (Docx Table 6)
T2_REFERENCES = [
    ["PRD_SPPS_A1_001", "Product Requirement Document - Smart Programmable Power Supply Module, Rev A1_001, VVDN Technologies, CA / India, Oct 2026."],
    ["VVDN_TP013_V1.1", "Hardware Design Document Template & Standard, TP013 Rev V1.1, VVDN Corporate Quality Management System, May 2020."],
    ["IEC_62368_1_ED3", "Audio/video, information and communication technology equipment - Part 1: Safety requirements, International Electrotechnical Commission, 3rd Edition, 2018."],
    ["CISPR_32_CLASS_B", "Electromagnetic compatibility of multimedia equipment - Emission requirements, CISPR 32 Edition 2.1, 2019."],
    ["FCC_PART_15_B", "Title 47 CFR Part 15 Subpart B - Unintentional Radiators, Class B Digital Device Standards, Federal Communications Commission."],
    ["TI_UCC28740_DS", "UCC28740 Constant-Voltage Constant-Current Flyback Controller with Optocoupled Feedback, Texas Instruments, Rev F, 2020."],
    ["TI_LM5176_DS", "LM5176 Wide VIN 4-Switch Synchronous Buck-Boost Controller, Texas Instruments, Rev B, 2021."],
    ["ST_STM32G474_DS", "STM32G474xE Arm Cortex-M4 32-bit MCU+FPU, 170 MHz, 512 KB Flash, High-Resolution Timer, STMicroelectronics, Rev 4, 2023."],
    ["TI_INA226_DS", "INA226 High-Side or Low-Side Measurement, Bi-Directional Current and Power Monitor with I2C, Texas Instruments, Rev A, 2015."],
    ["IPC_2221B", "Generic Standard on Printed Board Design, IPC Standard, Rev B, 2012."]
]

# Table 3: Implementation Plan Matrix
T3_IMPLEMENTATION = [
    ["Universal AC Line Input", "85 - 265 V AC RMS, 47 - 63 Hz operation with integrated surge/inrush protection.", "Stage 1: F1 (2A Time-Lag), RV1 (300V MOV / 4.5kA), RT1 (10Ω NTC inrush). Two-stage CM/DM filter.", "Functional Variac AC sweep (85V to 265V RMS) and surge injection test (1 kV DM / 2 kV CM)."],
    ["Galvanic Safety Isolation", "Reinforced safety isolation >= 3.0 kV AC RMS per IEC 62368-1.", "Stage 3: PQ26/20 transformer TX1 (triple-insulated wire, 6.4 mm physical creepage barrier). Optocouplers U2/U3.", "Hi-Pot dielectric withstand test (3000 V AC for 60 s, leakage < 2 mA)."],
    ["Intermediate DC Bus", "Regulated 24.0 V DC +/- 2.5% intermediate rail (65 W capable).", "Stage 3: UCC28740 quasi-resonant flyback controller @ 65 kHz, STP10NK80Z primary MOSFET, 24V secondary output.", "Load step response and efficiency verification over 120V to 375V DC bulk rail."],
    ["Wide Programmable DC Out", "5.0 V to 20.0 V DC continuously adjustable output @ 3.0 A continuous.", "Stage 4: LM5176 synchronous 4-switch buck-boost controller @ 300 kHz with 4x BSC035N10NS5 100V MOSFETs.", "Continuous dynamic sweep from 5.0V to 20.0V DC across 0 to 3.0 A resistive and electronic loads."],
    ["Maximum Output Power", "60.0 W continuous delivery across 5.0 - 20.0 V envelope.", "LM5176 wide VIN/VOUT power stage with Coilcraft SER2918-682KL (6.8 µH / 18A inductor) and solid thermal dissipation.", "Thermal chamber soak at 50°C ambient, 60 W continuous output for 4 hours."],
    ["Low Output Voltage Ripple", "Output voltage peak-to-peak ripple <= 50 mVpp at full 60 W load.", "Stage 4: Low-ESR aluminum polymer capacitors (2x 220 µF / 25V, ESR = 12 mΩ) + secondary ceramic filter (3x 22 µF).", "High-bandwidth oscilloscope measurement with 20 MHz bandwidth limit and tip-and-barrel probe."],
    ["High Conversion Efficiency", "Overall AC-to-DC conversion efficiency >= 85% at nominal load; peak >= 88%.", "Two-stage cascaded architecture: QR Flyback (94.2% eff) + 4-switch Buck-Boost (95.4% eff) -> 88.1% full load.", "Precision power analyzer measurement (Yokogawa WT310E) at 115V AC and 230V AC across load."],
    ["Fast Constant-Current Clamp", "Fast hardware cycle-by-cycle CC clamping response < 5 µs upon short circuit.", "Stage 5: High-speed analog comparator TLV3201 (40 ns) + 10 mΩ Kelvin shunt pulling LM5176 COMP low (< 4.2 µs).", "Dead-short electronic load step with Rogowski current probe verifying clamping in < 4.2 µs."],
    ["Dual-Domain Telemetry", "Primary bulk voltage telemetry and secondary VOUT/IOUT telemetry with 10-bit accuracy.", "Stage 7: Dual Texas Instruments INA226 16-bit I2C power monitors with isolated I2C barrier (ISO1640).", "Multi-point precision calibration against 6.5-digit multimeter (Keysight 34465A)."],
    ["Supervisory Intelligence", "ARM Cortex-M4 supervisory core with 12-bit DAC steering and OLED UI.", "Stage 6: STM32G474RET6 (170 MHz, 512KB Flash) driving DAC1/DAC3 and SSD1306 0.96-inch OLED.", "Firmware verification of 10 Hz telemetry loop, DAC linearity, and user command parsing."],
    ["Multi-Protection Mechanism", "Comprehensive OVP, OCP, OTP, and Mains UVLO protection with latch/auto-restart.", "Hardware comparator OVP crowbar, fast CC clamp, Murata NTC thermal sense, and LM5176 UVLO.", "Fault injection testing across overvoltage, overtemperature, short-circuit, and AC brown-out."],
    ["Conducted & Radiated EMI", "Compliance with CISPR 32 / FCC Part 15 Class B limits.", "Stage 1: Two-stage line filter (FL1 15mH, FL2 4.7mH, X2 caps 220nF/100nF, Y caps 2x 2.2nF) + PCB guard rings.", "LISN conducted emissions scan from 150 kHz to 30 MHz in certified semi-anechoic EMC chamber."]
]

# Table 4: Boot Strapping Pin Table
T4_BOOT_STRAPPING = [
    ["BOOT0", "Pin 60 (PB8/BOOT0)", "Weak Internal Pull-Down (40 kΩ)", "Ground (GND_SEC)", "0 (Logic Low)", "Boot from Main User Flash Memory (0x08000000). Standard production operational mode."],
    ["nBOOT0", "Option Byte (FLASH_OPTR[27])", "Internal Non-Volatile Flash", "Factory Default = 1", "1 (Logic High)", "Forces nBOOT0 active. Ensures processor always boots from internal user Flash on power-on reset."],
    ["nSWBOOT0", "Option Byte (FLASH_OPTR[26])", "Internal Non-Volatile Flash", "Factory Default = 1", "1 (Logic High)", "Enables hardware BOOT0 pin detection. Prevents software corruption from redirecting boot execution."]
]

# Table 5: RF Radiated Performance (Docx Table 5 under RF Design)
T5_RF_RADIATED = [
    ["30 MHz - 88 MHz", "30.0 dBµV/m (Quasi-Peak @ 10m)", "22.4 dBµV/m", "7.6 dB Headroom", "Pass (Compliant)"],
    ["88 MHz - 216 MHz", "35.0 dBµV/m (Quasi-Peak @ 10m)", "26.8 dBµV/m", "8.2 dB Headroom", "Pass (Compliant)"],
    ["216 MHz - 960 MHz", "37.0 dBµV/m (Quasi-Peak @ 10m)", "28.5 dBµV/m", "8.5 dB Headroom", "Pass (Compliant)"],
    ["960 MHz - 1.0 GHz", "40.0 dBµV/m (Quasi-Peak @ 10m)", "31.2 dBµV/m", "8.8 dB Headroom", "Pass (Compliant)"]
]

# Table 6: Power Sequencing (Docx Table 7)
T6_POWER_SEQUENCING = [
    ["1", "AC Mains Input (J1)", "85 - 265 V AC RMS line voltage applied via power switch.", "Instantaneous line disconnect upon switch opening (< 1 ms)."],
    ["2", "Bulk DC Rail (+375V_BULK)", "Charges to 120V - 375V DC through GBU4J and NTC RT1 (t_rise = 12 ms).", "Discharges through bleeders R1-R3 in 20.8 ms during AC dropout."],
    ["3", "Flyback Primary VDD", "UCC28740 VDD charges to 21.0 V UVLO turn-on via startup bleeders.", "Collapses below 8.1 V UVLO turn-off as bulk capacitor discharges."],
    ["4", "Intermediate DC Rail (+24V_INT)", "Soft-start ramp up to 24.0 V DC +/- 2.5% in 8.0 ms.", "Discharges via Buck-Boost power stage in 15.0 ms after AC loss."],
    ["5", "Secondary Auxiliary (+5V_AUX, +3.3V)", "TPS7A4700 and LM1117 LDOs establish quiet +5V and +3.3V rails (t = 2 ms).", "Held up by secondary local bulk capacitance (100 µF) for >= 25 ms."],
    ["6", "Supervisory MCU (STM32G474)", "Boots @ 170 MHz, validates ADC rails, holds LM5176 EN low during init.", "Executes brownout ISR upon BOR trip, records telemetry to Flash."],
    ["7", "Programmable Output (VOUT)", "LM5176 ENABLE pulled HIGH; VOUT soft-starts to commanded 5-20V in 5.0 ms.", "Forced hard shutdown: LM5176 disabled and active bleeder engaged."]
]

# Table 7: Subsystem 1 Power Consumption (Docx Table 8)
T7_POWER_CONSUMPTION = [
    ["1", "STM32G474RET6 MCU Core", "72.0", "12.0", "0.0", "0.30", "0.22"],
    ["2", "LM5176 Buck-Boost Controller", "0.0", "0.0", "18.5", "0.22", "0.18"],
    ["3", "INA226 Telemetry Monitors (x2)", "1.2", "0.0", "0.0", "0.01", "0.01"],
    ["4", "UCC28740 Flyback Controller", "0.0", "0.0", "3.2", "0.05", "0.04"],
    ["5", "MOSFET Gate Drivers (LM5176/Q2-Q5)", "0.0", "0.0", "65.0", "0.78", "0.62"],
    ["6", "0.96-inch OLED Display", "28.0", "0.0", "0.0", "0.09", "0.06"],
    ["7", "Fast Hardware Comparator (TLV3201)", "0.8", "0.0", "0.0", "0.01", "0.01"],
    ["8", "Output Power Delivery (5-20V / 3A)", "0.0", "0.0", "0.0", "60.00", "45.00"]
]

# Table 8: Subsystem 1 Power Dissipation (Docx Table 9)
T8_POWER_DISSIPATION = [
    ["1", "Mains EMI Filter & GBU4J Bridge", "230.0", "325.0", "0.32", "97.8", "1.45", "68.06"],
    ["2", "UCC28740 Flyback Stage (TX1, Q1, D2)", "325.0", "24.0", "2.71", "94.2", "3.65", "66.61"],
    ["3", "LM5176 Buck-Boost Stage (L1, Q2-Q5)", "24.0", "20.0", "3.00", "95.4", "2.78", "62.96"],
    ["4", "Auxiliary LDO Regulators (TPS7A, LM1117)", "24.0", "3.3 / 5.0", "0.12", "68.5", "0.18", "0.57"],
    ["5", "Total Conversion Subsystem", "230.0", "20.0", "3.00", "88.1", "8.06", "68.06"]
]

# Table 9: Battery Capacity Calculation (Docx Table 10)
T9_BATTERY_CAPACITY = [
    ["1", "Continuous AC Mains Operation", "60.0 W", "0.0 W (Direct Line)", "Infinite (Continuous AC Line)", "N/A (No Battery Required)"]
]

# Table 10: Power Modes (Docx Table 11)
T10_POWER_MODES = [
    ["1", "Standby / Idle Mode", "0.15 W", "N/A (Line Powered)", "0.0 W", "Continuous (Line Powered)"],
    ["2", "Constant Voltage (CV) Full Load", "60.0 W", "N/A (Line Powered)", "8.06 W", "Continuous (Line Powered)"],
    ["3", "Fast CC Clamping Mode", "36.0 W", "N/A (Line Powered)", "6.80 W", "Continuous (Line Powered)"],
    ["4", "Fault / Hiccup Recovery Mode", "1.20 W", "N/A (Line Powered)", "0.45 W", "Continuous (Line Powered)"],
    ["5", "Thermal Shutdown Mode", "0.20 W", "N/A (Line Powered)", "0.12 W", "Continuous (Line Powered)"]
]

# Table 11: Subsystem 1 Assembly Variants (Docx Table 12)
T11_ASSEMBLY_VARIANTS = [
    ["1", "STM32G474RET6", "PC10 / Pin 51", "BRD_VAR0", "00: Variant 01 - Standard Industrial 60W (5-20V / 3A, Commercial Passives)"],
    ["2", "STM32G474RET6", "PC11 / Pin 52", "BRD_VAR1", "01: Variant 02 - High-Rel Conformal Coated 60W (Harsh Environment, AEC-Q200)"],
    ["3", "STM32G474RET6", "PC10 / Pin 51", "BRD_VAR0", "10: Variant 03 - Precision Lab Grade 60W (0.05% Shunt, BNC Remote Sense)"],
    ["4", "STM32G474RET6", "PC11 / Pin 52", "BRD_VAR1", "11: Reserved for Future Industrial High-Power Extension (100W USB-PD EPR)"]
]

# Table 12: Subsystem 1 Board Revisions (Docx Table 13)
T12_BOARD_REVISIONS = [
    ["1", "STM32G474RET6", "PC12 / Pin 53", "BRD_REV0", "00: Revision 0.1 - Engineering Proof-of-Concept Prototype"],
    ["2", "STM32G474RET6", "PD2 / Pin 54", "BRD_REV1", "01: Revision 0.9 - Pre-Production DVT Compliance Build"],
    ["3", "STM32G474RET6", "PC12 / Pin 53", "BRD_REV0", "10: Revision 1.0 - Mass Production Standard Release"],
    ["4", "STM32G474RET6", "PD2 / Pin 54", "BRD_REV1", "11: Reserved for Next-Generation Hardware Iteration"]
]

# Table 13: DC Analysis High (Docx Table 14)
T13_DC_HIGH = [
    ["1", "STM32G474RET6", "2.90", "8.0", "LM5176 (EN)", "2.00", "0.001", "+0.90"],
    ["2", "STM32G474RET6", "2.90", "4.0", "ISO1640 (SDA/SCL)", "2.31", "0.005", "+0.59"],
    ["3", "TLV3201 (Comparator)", "2.95", "4.0", "STM32G474 (EXTI)", "2.31", "0.001", "+0.64"],
    ["4", "MCP4725 (DAC Out)", "3.10", "1.0", "LM5176 (FB Node)", "2.00", "0.002", "+1.10"]
]

# Table 13: DC Analysis Low (Docx Table 15)
T13_DC_LOW = [
    ["1", "STM32G474RET6", "0.40", "8.0", "LM5176 (EN)", "0.80", "0.001", "+0.40"],
    ["2", "STM32G474RET6", "0.40", "4.0", "ISO1640 (SDA/SCL)", "0.99", "0.005", "+0.59"],
    ["3", "TLV3201 (Comparator)", "0.35", "4.0", "STM32G474 (EXTI)", "0.99", "0.001", "+0.64"],
    ["4", "MCP4725 (DAC Out)", "0.20", "1.0", "LM5176 (FB Node)", "0.80", "0.002", "+0.60"]
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
    ["I2C1_SDA", "Signal", "1.00 MHz", "2", "10.0 MHz", "2", "10.0 MHz"],
    ["I2C1_SCL", "Signal", "1.00 MHz", "3", "10.0 MHz", "3", "10.0 MHz"],
    ["REMOTE_SENSE+", "Signal", "DC", "4", "1.0 A", "4", "1.0 A"],
    ["REMOTE_SENSE-", "Signal", "DC", "5", "1.0 A", "5", "1.0 A"],
    ["GND_SEC", "Power", "0.20 A", "6", "1.5 A", "6", "1.5 A"]
]

# Table 18: Expansion Header Cable (Docx Table 20)
T18_EXPANSION_CABLE = [
    ["1", "0.20 A", "28 AWG Ribbon", "1", "0.20 A"],
    ["2", "1.00 MHz", "28 AWG Ribbon", "2", "1.00 MHz"],
    ["3", "1.00 MHz", "28 AWG Ribbon", "3", "1.00 MHz"],
    ["4", "DC Sense", "28 AWG Ribbon", "4", "DC Sense"],
    ["5", "DC Sense", "28 AWG Ribbon", "5", "DC Sense"],
    ["6", "0.20 A", "28 AWG Ribbon", "6", "0.20 A"]
]

# Table 19: Module 1 GPIOs (Docx Table 21)
T19_MODULE1_GPIOS = [
    ["1", "LM5176_ENABLE", "PA0", "GPIO0", "3.3V", "Push-Pull", "3.3V", "Pull-Down (10k)", "0", "0: Buck-Boost Disabled, 1: Buck-Boost Enabled"],
    ["2", "LM5176_PGOOD", "PA1", "GPIO1", "3.3V", "Floating", "3.3V", "Pull-Up (10k)", "0", "0: VOUT Out of Regulation, 1: VOUT In Regulation"],
    ["3", "DISCHARGE_GATE", "PA2", "GPIO2", "3.3V", "Push-Pull", "3.3V", "Pull-Down (100k)", "0", "1: Active Output Capacitor Bleeder FET Turn-on"],
    ["4", "FAST_CC_TRIP", "PA3", "GPIO3", "3.3V", "Floating", "3.3V", "Pull-Down (10k)", "0", "1: Hardware CC Comparator Overcurrent Event"],
    ["5", "OVP_LATCH", "PA4", "GPIO4", "3.3V", "Push-Pull", "3.3V", "Pull-Down (10k)", "0", "1: Hardware Crowbar SCR Fire (Latched Shutdown)"],
    ["6", "ALERT_N", "PA5", "GPIO5", "3.3V", "Floating", "3.3V", "Pull-Up (4.7k)", "1", "0: INA226 Telemetry Threshold Alert Interrupt"],
    ["7", "STATUS_LED_G", "PB0", "GPIO16", "3.3V", "Push-Pull", "3.3V", "Series Resistor", "0", "1: Green Normal Operation LED Illumination"],
    ["8", "STATUS_LED_R", "PB1", "GPIO17", "3.3V", "Push-Pull", "3.3V", "Series Resistor", "0", "1: Red Fault / Warning LED Illumination"],
    ["9", "OLED_RST", "PB2", "GPIO18", "3.3V", "Push-Pull", "3.3V", "Pull-Up (10k)", "1", "0: Hardware Reset Pulse to SSD1306 Display Controller"],
    ["10", "I2C1_SCL", "PB6", "GPIO22", "3.3V", "Open-Drain", "3.3V", "Pull-Up (4.7k)", "1", "Fast-Mode+ 1.0 MHz Telemetry Clock Line"],
    ["11", "I2C1_SDA", "PB7", "GPIO23", "3.3V", "Open-Drain", "3.3V", "Pull-Up (4.7k)", "1", "Fast-Mode+ 1.0 MHz Telemetry Bidirectional Data"],
    ["12", "USART1_TX", "PA9", "GPIO9", "3.3V", "Push-Pull", "3.3V", "None", "1", "115.2 kbps Serial Console Telemetry Output to J3"],
    ["13", "USART1_RX", "PA10", "GPIO10", "3.3V", "Floating", "3.3V", "Pull-Up (10k)", "1", "115.2 kbps Serial Console Command Input from J3"],
    ["14", "BRD_VAR0", "PC10", "GPIO42", "3.3V", "Floating", "3.3V", "Strapping Resistor", "0", "Hardware Assembly Variant Bit 0 Detection"],
    ["15", "BRD_VAR1", "PC11", "GPIO43", "3.3V", "Floating", "3.3V", "Strapping Resistor", "0", "Hardware Assembly Variant Bit 1 Detection"],
    ["16", "BRD_REV0", "PC12", "GPIO44", "3.3V", "Floating", "3.3V", "Strapping Resistor", "0", "Hardware Board Revision Bit 0 Detection"],
    ["17", "BRD_REV1", "PD2", "GPIO50", "3.3V", "Floating", "3.3V", "Strapping Resistor", "0", "Hardware Board Revision Bit 1 Detection"],
    ["18", "USER_BTN", "PC13", "GPIO45", "3.3V", "Floating", "3.3V", "Pull-Up (10k)", "1", "0: Pushbutton Actuation (Toggle VOUT Enable/Disable)"]
]

# Table 20: Module 1 Interrupts (Docx Table 22)
T20_MODULE1_INTERRUPTS = [
    ["1", "FAST_CC_TRIP", "PA3", "EXTI3", "3.3V", "Floating", "3.3V", "Pull-Down (10k)", "Rising Edge", "Hardware Over-Current Clamp: Halts PWM, enters CC mode (< 4.2 µs)"],
    ["2", "OVP_LATCH", "PA4", "EXTI4", "3.3V", "Floating", "3.3V", "Pull-Down (10k)", "Rising Edge", "Hardware Over-Voltage Crowbar: Immediate shutdown and fault latch"],
    ["3", "ALERT_N", "PA5", "EXTI9_5", "3.3V", "Floating", "3.3V", "Pull-Up (4.7k)", "Falling Edge", "INA226 Telemetry Alert: Overpower or overvoltage threshold exceeded"],
    ["4", "ADC1_AWD", "Internal", "ADC1_2_IRQ", "3.3V", "Internal", "3.3V", "Internal", "Level High", "ADC Analog Watchdog: Output current exceeds 3.3 A software limit"],
    ["5", "USART1_RXNE", "PA10", "USART1_IRQ", "3.3V", "Floating", "3.3V", "Pull-Up (10k)", "Data Ready", "Serial Telemetry Command: Received command packet from J3 header"],
    ["6", "I2C1_EV", "PB6/7", "I2C1_EV_IRQ", "3.3V", "Open-Drain", "3.3V", "Pull-Up (4.7k)", "Bus Event", "I2C DMA Buffer Transfer Complete: Primary/Secondary telemetry ready"],
    ["7", "TIM1_UP", "Internal", "TIM1_UP_IRQ", "3.3V", "Internal", "3.3V", "Internal", "Periodic", "High-Resolution Control Loop: 100 kHz voltage/current DAC trimming"],
    ["8", "SYSTICK", "Internal", "SysTick_IRQ", "3.3V", "Internal", "3.3V", "Internal", "1 ms Tick", "RTOS Kernel Scheduler: 10 Hz OLED display and state machine tick"]
]

# Table 21: Programmable ROM Devices (Docx Table 23)
T21_PROGRAMMABLE_ROM = [
    ["Subsystem 1 (Main PCBA)", "STM32G474RET6 Internal Flash (512 KB)", "Stores master firmware executable, RTOS kernel, USB/UART protocol stack, and mathematical control algorithms. Dual-bank layout allows robust In-Application Programming (IAP)."],
    ["Subsystem 1 (Main PCBA)", "STM32G474RET6 System Memory ROM (32 KB)", "Factory programmed by STMicroelectronics with standard DFU bootloader supporting UART, I2C, and USB in-system programming."],
    ["Subsystem 1 (Main PCBA)", "Emulated EEPROM (Sector 7, 16 KB)", "Non-volatile storage for factory calibration constants (voltage divider gain/offset, shunt calibration trim, serial number, FRU data, fault logs)."],
    ["Subsystem 1 (Main PCBA)", "Option Bytes Flash Register (1 KB)", "Non-volatile hardware security fuses: Readout Protection (RDP Level 1), hardware watchdog enable, and BOOT0 hardware strapping selection."]
]

# Table 22: Master Class A Engineering BOM (Docx Table 24)
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
    ["15", "TVS Diode Transient Suppressor 180V 600W SMB", "1", "Littelfuse", "SMBJ180A", "C", "Yes", "-65°C to +150°C"],
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
    ["26", "High-Speed Analog Comparator 40ns SOT-23-5", "1", "Texas Instruments", "TLV3201AIDBVR", "I", "Yes", "-40°C to +125°C"],
    ["27", "N-Channel MOSFET Small-Signal 60V 300mA SOT-23", "2", "Diodes Inc.", "2N7002K", "C", "Yes", "-55°C to +150°C"],
    ["28", "Bipolar Power Transistor Disconnector 30V 5A SOT-223", "1", "Diodes Inc.", "FZT851TA", "C", "Yes", "-55°C to +150°C"],
    ["29", "ARM Cortex-M4 Mixed-Signal MCU 170MHz LQFP-64", "1", "STMicroelectronics", "STM32G474RET6", "I", "Yes", "-40°C to +85°C"],
    ["30", "Quartz Crystal Resonator 24.000MHz 18pF SMD", "1", "Abracon", "ABM8G-24.000MHZ-B4Y-T", "C", "Yes", "-40°C to +85°C"],
    ["31", "Ceramic Load Capacitor 18pF 50V C0G 0603", "2", "Murata", "GRM1885C1H180JA01D", "C", "Yes", "-55°C to +125°C"],
    ["32", "High-Side/Low-Side Power Monitor I2C VSSOP-10", "2", "Texas Instruments", "INA226AIDGSR", "I", "Yes", "-40°C to +125°C"],
    ["33", "Bidirectional I2C Digital Isolator 3000Vrms SOIC-8", "1", "Texas Instruments", "ISO1640BDR", "I", "Yes", "-40°C to +125°C"],
    ["34", "Ultra-Low-Noise LDO Regulator 3.3V 1A QFN-20", "1", "Texas Instruments", "TPS7A4700QRGWRQ1", "A", "Yes", "-40°C to +125°C"],
    ["35", "Positive Voltage Regulator LDO 5.0V 1A SOT-223", "1", "Diodes Inc.", "AZ1117EH-5.0TRG1", "C", "Yes", "-40°C to +125°C"],
    ["36", "12-Bit Digital-to-Analog Converter I2C SOT-23-6", "2", "Microchip", "MCP4725A0T-E/CH", "C", "Yes", "-40°C to +125°C"],
    ["37", "Precision Resistor 30.1 kOhm 0.1% 0805 (DAC Injection)", "1", "Vishay Beyschlag", "MBB02070C3012FCT00", "C", "Yes", "-55°C to +155°C"],
    ["38", "Precision Feedback Resistor 19.1 kOhm 0.1% 0805", "1", "Vishay Beyschlag", "MBB02070C1912FCT00", "C", "Yes", "-55°C to +155°C"],
    ["39", "Precision Ground Resistor 1.21 kOhm 0.1% 0805", "1", "Vishay Beyschlag", "MBB02070C1211FCT00", "C", "Yes", "-55°C to +155°C"],
    ["40", "NTC Thermistor Sensor 10 kOhm 1% 0603", "1", "Murata", "NCP18XH103F03RB", "C", "Yes", "-40°C to +125°C"],
    ["41", "OLED Display Module 0.96-inch 128x64 White I2C", "1", "Solomon Systech / Adafruit", "SSD1306-0.96", "C", "Yes", "-40°C to +85°C"],
    ["42", "AC Mains Terminal Block 3-Pos 5.08mm Rising Cage", "1", "Phoenix Contact", "1757255", "C", "Yes", "-40°C to +105°C"],
    ["43", "DC Output Binding Posts Dual Heavy-Duty Banana", "1", "Pomona Electronics", "6883", "C", "Yes", "-55°C to +115°C"],
    ["44", "Isolated Debug Header 4-Pin 2.54mm Friction Lock", "1", "Molex", "0022013047", "C", "Yes", "-40°C to +105°C"],
    ["45", "SWD Programming Header 5-Pin 1.27mm Micro-Pitch", "1", "Samtec", "FTSH-105-01-L-DV", "C", "Yes", "-55°C to +125°C"],
    ["46", "Ceramic Bypass Capacitor 100nF 50V X7R 0603", "24", "TDK", "C1608X7R1H104K080AA", "C", "Yes", "-55°C to +125°C"],
    ["47", "Ceramic Decoupling Capacitor 1uF 25V X7R 0805", "8", "Murata", "GRM21BR71E105KA99L", "C", "Yes", "-55°C to +125°C"],
    ["48", "Standard Chip Resistor 10 kOhm 1% 0603", "14", "Yageo", "RC0603FR-0710KL", "C", "Yes", "-55°C to +155°C"],
    ["49", "Standard Chip Resistor 4.7 kOhm 1% 0603", "6", "Yageo", "RC0603FR-074K7L", "C", "Yes", "-55°C to +155°C"],
    ["50", "Gate Drive Damping Resistor 4.7 Ohm 1% 0805", "4", "Panasonic", "ERJ-6GEYJ4R7V", "C", "Yes", "-55°C to +155°C"],
    ["51", "Green Status LED 565nm 20mA 0805 SMD", "1", "Lite-On", "LTST-C170GKT", "C", "Yes", "-55°C to +85°C"],
    ["52", "Red Fault LED 630nm 20mA 0805 SMD", "1", "Lite-On", "LTST-C170CKT", "C", "Yes", "-55°C to +85°C"],
    ["53", "Tactile Pushbutton Switch SMD 6x6mm Ground Sealed", "2", "C&K", "PTS645SL43SMTR92LFS", "C", "Yes", "-20°C to +70°C"],
    ["54", "Silicon Power SCR Crowbar Thyristor 400V 8A DPAK", "1", "STMicroelectronics", "TN805-600B-TR", "C", "Yes", "-40°C to +125°C"]
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
    ["CR-TEL-001", "HW-TEL-001", "Section 5.1.1, Section 7.1.1 (Dual INA226 Telemetry & Precision Shunts)"],
    ["CR-TEL-002", "HW-TEL-002", "Section 5.1.1, Section 13.1.2 (10 Hz Telemetry Update Rate & Fast-Mode+ I2C)"],
    ["CR-CTL-001", "HW-CTL-001", "Section 5.1.1, Section 7.1.2 (12-bit Active DAC Voltage/Current Steering)"],
    ["CR-UI-001", "HW-UI-001", "Section 4.2, Section 5.1.1 (0.96-inch OLED Interface & Status LEDs)"],
    ["CR-DBG-001", "HW-DBG-001", "Section 5.1.1, Section 14.1.1 (SWD Debug Header & Isolated UART J3)"],
    ["CR-EMC-001", "HW-EMC-001", "Section 6.1.1, Section 13.4 (Conducted EMI Attenuation & 2-Stage Filter)"],
    ["CR-EMC-002", "HW-EMC-002", "Section 6.1.1, Section 13.5 (Radiated Emissions Shielding & Layout Isolation)"],
    ["CR-ENV-001", "HW-ENV-001", "Section 1.2, Section 13.6 (Operating Ambient Temperature -10°C to +50°C)"],
    ["CR-ENV-002", "HW-ENV-002", "Section 13.6 (Passive Natural Convection Cooling Without Fan)"],
    ["CR-MECH-001", "HW-MECH-001", "Section 4.1, Section 13.5 (140 mm x 90 mm PCB Enclosure Envelope)"],
    ["CR-REL-001", "HW-REL-001", "Section 1.2, Section 13.6, Section 18 (VVDN Component Derating Guidelines)"]
]
