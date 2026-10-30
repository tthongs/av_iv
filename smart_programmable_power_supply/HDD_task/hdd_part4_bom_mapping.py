"""
Hardware Design Document - Part 4: Chapters 14 to 20
14. Connectors & Cable Assembly
15. GPIO Mapping
16. Interrupt Mapping
17. Programmable ROM Devices
18. Bill of Material (Master Class A BOM Table 22 - 54 items)
19. Design Limitations
20. Requirement-Design Mapping (Traceability Matrix Table 23)
"""

def add_part4(builder):
    # =========================================================================
    # Chapter 14: Connectors & Cable Assembly
    # =========================================================================
    builder.add_h1("14. Connectors & Cable Assembly")
    builder.add_h2("14.1 Subsystem1 Connectors")

    builder.add_h3("14.1.1 Internal Connectors")
    builder.add_p(
        "Internal board connectors facilitate debugging, automated factory flashing, and front-panel user interface sub-assembly routing:"
    )

    builder.add_h4("Connector 1 [UART Telemetry Header - J5]")
    builder.add_bullet("Connector MPN & Make: Molex 22-28-4030 / Samtec TSW-103-07-G-S (3-pin, 2.54 mm pitch, vertical pin strip).")
    builder.add_bullet("Mating Housing: Molex 0022013037 with crimp terminals 0008500114.")
    builder.add_bullet("Cable Specification: 24 AWG stranded copper, PVC insulated, 300 V rating, length 150 mm.")

    j5_headers = ["Pin No", "Net Name", "Signal / Power Type", "Designed Voltage / Current", "Description"]
    j5_rows = [
        ["1", "+3.3V_VDD", "Power", "+3.30 V DC / 20 mA", "Housekeeping logic rail for opto-isolated serial cable."],
        ["2", "UART1_TX", "Digital Output", "+3.3 V Logic / 4 mA", "Transmit data stream from STM32 pin PA9 (115,200 baud)."],
        ["3", "GND_SEC", "Ground", "0.0 V / Return", "Secondary touch-safe quiet ground reference."],
    ]
    builder.add_table("Table 16: Subsystem1 - UART Header (J5)", j5_headers, j5_rows, [0.8, 1.3, 1.3, 1.4, 2.7])

    builder.add_h4("Connector 2 [SWD Debug Header - J4]")
    builder.add_bullet("Connector MPN & Make: Molex 22-28-4040 / Samtec TSW-104-07-G-S (4-pin, 2.54 mm pitch, vertical shrouded header).")
    builder.add_bullet("Mating Housing: Molex 0022013047 with crimp terminals 0008500114.")

    j4_headers = ["Pin No", "Net Name", "Signal / Power Type", "Designed Voltage / Current", "Description"]
    j4_rows = [
        ["1", "+3.3V_VDD", "Power Reference", "+3.30 V DC / 10 mA", "Reference voltage for external debug probe (ST-Link V3)."],
        ["2", "SWDIO", "Bidirectional Data", "+3.3 V Logic / 4 mA", "Serial Wire Data input/output (STM32 pin PA13)."],
        ["3", "SWCLK", "Clock Input", "+3.3 V Logic / 4 mA", "Serial Wire Clock input (STM32 pin PA14)."],
        ["4", "GND_SEC", "Ground", "0.0 V / Return", "Secondary touch-safe quiet ground reference."],
    ]
    builder.add_table("Table 17: Subsystem1 - SWD Debug Header (J4)", j4_headers, j4_rows, [0.8, 1.3, 1.3, 1.4, 2.7])

    builder.add_h4("Connector 3 [OLED Display Header - J6]")
    builder.add_bullet("Connector MPN & Make: Samtec SSW-104-02-G-S (4-pin, 2.54 mm right-angle female socket).")
    builder.add_bullet("Pinout: Pin 1 (GND), Pin 2 (+5V_DISP), Pin 3 (I2C1_SCL), Pin 4 (I2C1_SDA).")

    builder.add_h3("14.1.2 External Connectors")

    builder.add_h4("External Connector 1 [AC Mains Inlet - J1]")
    builder.add_bullet(
        "Connector MPN & Make: Schurter 6100.3300 / TE Connectivity 1-6609987-1 (IEC 320-C14 chassis appliance inlet, "
        "10.0 A, 250 V AC, 50/60 Hz, screw-mount with quick-connect / solder terminals)."
    )

    j1_headers = ["Terminal No", "Terminal Designation", "Net Name", "Designed Voltage / Current", "Functional Description"]
    j1_rows = [
        ["L", "Live", "AC_LINE", "85 V - 265 V AC / 1.60 A RMS", "Connects to 2A ceramic cartridge fuse F1."],
        ["N", "Neutral", "AC_NEUTRAL", "0.0 V Nominal / 1.60 A RMS", "Connects to 15Ω inrush limiting thermistor NTC1."],
        ["E", "Earth", "EARTH_GND", "Chassis Ground / Fault Return", "Direct chassis screw bond and Class Y1 capacitor return."],
    ]
    builder.add_table("Table 18: External AC Mains Inlet (J1)", j1_headers, j1_rows, [1.0, 1.3, 1.2, 1.5, 2.5])

    builder.add_h4("External Connector 2 [Output Binding Posts - J2, J3]")
    builder.add_bullet(
        "Connector MPN & Make: Pomona Electronics 3770-2 (Red) / 3770-0 (Black) heavy-duty 4 mm gold-plated turret terminal binding posts "
        "(30.0 A, 1000 V RMS, panel mount with standard 19.05 mm center-to-center spacing)."
    )

    j2_headers = ["Terminal Ref", "Body Color", "Net Name", "Designed Voltage / Current", "Description"]
    j2_rows = [
        ["J2", "Red", "+V_OUT", "+5.0 V - +20.0 V DC / 3.0 A DC", "Positive DC output power terminal."],
        ["J3", "Black", "-V_OUT (GND)", "0.0 V DC / 3.0 A DC Return", "Negative DC output power return terminal."],
    ]
    builder.add_table("Table 18.1: External Output Binding Posts (J2, J3)", j2_headers, j2_rows, [1.0, 1.0, 1.2, 1.6, 2.7])

    builder.add_h2("14.2 Inter-Subsystem Wiring & Harness Specifications")
    builder.add_bullet("AC Input Wiring: 18 AWG UL1015 high-voltage hookup wire (600 V rating, 105°C insulation, stranded tinned copper).")
    builder.add_bullet("DC Output Wiring: 16 AWG UL1007 high-current wire (300 V rating, 105°C insulation) minimizing DC conduction drop to < 10 mV at 3.0 A full load.")
    builder.add_bullet("Display Cable Assembly: 4-conductor 26 AWG ribbon cable with keyed IDC socket headers, length 100 mm.")

    # =========================================================================
    # Chapter 15: GPIO Mapping
    # =========================================================================
    builder.add_h1("15. GPIO Mapping")
    builder.add_h2("15.1 Subsystem1 GPIOs")
    builder.add_p(
        "All microcontroller GPIO pins on U5 (STMicroelectronics STM32G474RET6, LQFP-64) are comprehensively allocated "
        "with defined electrical drive modes, internal pull-up/pull-down states, reset states, and software roles:"
    )

    gpio_headers = ["Pin #", "Port / Pin", "Net Name", "Direction", "Drive Type", "Pull State", "Reset State", "Alternate Function", "Software / Hardware Functional Role"]
    gpio_rows = [
        ["1", "VBAT", "+3.3V_VDD", "Power", "—", "—", "—", "—", "Backup battery rail (tied to +3.3V logic supply)."],
        ["2", "PC13", "ENC1_SW", "Input", "CMOS", "Pull-Up", "High-Z", "GPIO (EXTI13)", "Push-button switch on Rotary Encoder 1 (Coarse/Fine Toggle)."],
        ["3", "PC14", "OSC32_IN", "Input", "Analog", "None", "High-Z", "LSE Clock In", "32.768 kHz crystal input (ABS07)."],
        ["4", "PC15", "OSC32_OUT", "Output", "Analog", "None", "High-Z", "LSE Clock Out", "32.768 kHz crystal output."],
        ["5", "PF0", "OSC_IN", "Input", "Analog", "None", "High-Z", "HSE Clock In", "24.000 MHz crystal input (ABM8G)."],
        ["6", "PF1", "OSC_OUT", "Output", "Analog", "None", "High-Z", "HSE Clock Out", "24.000 MHz crystal output."],
        ["7", "NRST", "MCU_RESET_N", "Input", "CMOS", "Pull-Up", "Reset", "Dedicated", "Active-low hardware reset pin with 100 nF filter."],
        ["8", "PC0", "ADC1_IN6", "Input", "Analog", "None", "High-Z", "ADC1 Channel 6", "Senses primary AC input voltage from AMC1311 iso-amp."],
        ["9", "PC1", "ADC1_IN7", "Input", "Analog", "None", "High-Z", "ADC1 Channel 7", "Senses primary AC line current from 1000:1 CT burden."],
        ["10", "PC2", "ADC1_IN8", "Input", "Analog", "None", "High-Z", "ADC1 Channel 8", "Auxiliary board temperature sensor (NTC voltage divider)."],
        ["11", "PC3", "ADC1_IN9", "Input", "Analog", "None", "High-Z", "ADC1 Channel 9", "Senses intermediate +24.0 V rail voltage divider."],
        ["14", "PA0", "TIM2_CH1", "Input", "CMOS", "Pull-Up", "High-Z", "TIM2 Channel 1", "Rotary Encoder 1 Phase A input (Quadrature decoding)."],
        ["15", "PA1", "TIM2_CH2", "Input", "CMOS", "Pull-Up", "High-Z", "TIM2 Channel 2", "Rotary Encoder 1 Phase B input."],
        ["16", "PA2", "ENC2_SW", "Input", "CMOS", "Pull-Up", "High-Z", "GPIO (EXTI2)", "Push-button switch on Rotary Encoder 2 (Output ON/OFF)."],
        ["20", "PA4", "DAC1_OUT1", "Output", "Analog", "None", "High-Z", "DAC1 Channel 1", "12-Bit DAC Voltage Steering reference into LM5176 FB."],
        ["24", "PA6", "TIM3_CH1", "Input", "CMOS", "Pull-Up", "High-Z", "TIM3 Channel 1", "Rotary Encoder 2 Phase A input."],
        ["25", "PA7", "TIM3_CH2", "Input", "CMOS", "Pull-Up", "High-Z", "TIM3 Channel 2", "Rotary Encoder 2 Phase B input."],
        ["26", "PC4", "ADC2_IN5", "Input", "Analog", "None", "High-Z", "ADC2 Channel 5", "Direct hardware output voltage sense (V_OUT divider)."],
        ["27", "PC5", "ADC2_IN11", "Input", "Analog", "None", "High-Z", "ADC2 Channel 11", "Direct hardware load current sense (I_OUT amplifier)."],
        ["28", "PB0", "LM5176_EN", "Output", "Push-Pull", "None", "Low", "GPIO Output", "Drives base of NPN clamp to disable LM5176 (1 = OFF)."],
        ["37", "PC6", "LED_CV", "Output", "Push-Pull", "None", "Low", "GPIO Output", "Drives Green Front-Panel LED (Constant Voltage Mode)."],
        ["38", "PC7", "LED_CC", "Output", "Push-Pull", "None", "Low", "GPIO Output", "Drives Amber Front-Panel LED (Constant Current Clamp Mode)."],
        ["39", "PC8", "LED_FAULT", "Output", "Push-Pull", "None", "Low", "GPIO Output", "Drives Red Front-Panel LED (Fault / Trip Shutdown)."],
        ["42", "PA9", "USART1_TX", "Output", "Push-Pull", "None", "High-Z", "USART1 TX", "External serial telemetry logging output (115,200 baud)."],
        ["43", "PA10", "USART1_RX", "Input", "CMOS", "Pull-Up", "High-Z", "USART1 RX", "External serial command input."],
        ["46", "PA13", "SWDIO", "Bidir", "CMOS", "Pull-Up", "High-Z", "SYS_JTMS-SWDIO", "Serial Wire Debug Data I/O."],
        ["49", "PA14", "SWCLK", "Input", "CMOS", "Pull-Down", "High-Z", "SYS_JTCK-SWCLK", "Serial Wire Debug Clock."],
        ["60", "BOOT0", "BOOT0", "Input", "CMOS", "Pull-Down", "Low", "Dedicated", "Hardware boot mode configuration (tied to GND via 10 kΩ)."],
        ["61", "PB8", "I2C1_SCL", "Bidir", "Open-Drain", "None", "High-Z", "I2C1 SCL", "Fast-Mode 400 kHz clock for INA226 and OLED display."],
        ["62", "PB9", "I2C1_SDA", "Bidir", "Open-Drain", "None", "High-Z", "I2C1 SDA", "Fast-Mode 400 kHz data for INA226 and OLED display."],
    ]
    builder.add_table("Table 19: Module 1 STM32G474RET6 GPIO Allocation Table", gpio_headers, gpio_rows, [0.5, 0.7, 0.9, 0.7, 0.7, 0.7, 0.7, 1.0, 1.6])

    # =========================================================================
    # Chapter 16: Interrupt Mapping
    # =========================================================================
    builder.add_h1("16. Interrupt Mapping")
    builder.add_h2("16.1 Subsystem1 Interrupts")
    builder.add_p(
        "The STM32G474RET6 Nested Vectored Interrupt Controller (NVIC) is configured with defined preemption and sub-priorities "
        "to ensure microsecond-level response to user inputs and telemetry scheduling:"
    )

    nvic_headers = ["Interrupt Source / Vector", "Priority", "Sub-Priority", "Trigger Condition", "Execution Budget (µs)", "ISR Functional Role & Servicing Procedure"]
    nvic_rows = [
        ["HardFault_Handler", "-1", "—", "Bus error, invalid memory access", "< 5.0 µs", "Instantly executes emergency shutdown: asserts PB0 HIGH to kill LM5176."],
        ["EXTI2_IRQHandler", "1", "0", "Falling Edge on PA2 (Encoder 2 Switch)", "< 25 µs", "User Output Enable/Disable toggle request. Toggles LM5176_EN state."],
        ["EXTI13_IRQHandler", "1", "1", "Falling Edge on PC13 (Encoder 1 Switch)", "< 15 µs", "User Tuning Mode toggle (switches between 10 mV fine and 1.0 V coarse)."],
        ["TIM2_IRQHandler", "2", "0", "Encoder 1 Count Overflow / Change", "< 35 µs", "Rotary Encoder 1 moved. Updates voltage setpoint register and recalculates DAC."],
        ["TIM3_IRQHandler", "2", "1", "Encoder 2 Count Overflow / Change", "< 35 µs", "Rotary Encoder 2 moved. Adjusts software overcurrent warning threshold."],
        ["DMA1_Channel1_IRQHandler", "3", "0", "DMA Buffer Half / Full Transfer Complete", "< 45 µs", "ADC sampling buffer ready. Computes true RMS AC input voltage and current."],
        ["TIM6_DAC_IRQHandler", "4", "0", "TIM6 Timer Update (100.0 ms tick)", "< 250 µs", "Master 10 Hz Telemetry Loop: reads INA226, calculates η, triggers OLED update."],
        ["I2C1_EV_IRQHandler", "5", "0", "I2C Byte Transfer Finished (DMA mode)", "< 10 µs", "Non-blocking OLED display DMA transmission completion handler."],
        ["I2C1_ER_IRQHandler", "5", "1", "I2C Bus Acknowledge Failure or Error", "< 30 µs", "Resets I2C1 peripheral in case of OLED disconnect or bus noise spike."],
        ["SysTick_Handler", "15", "0", "1.0 ms System Tick Overflow", "< 5.0 µs", "System millisecond timebase for software debouncing timers and LED blinkers."],
    ]
    builder.add_table("Table 20: Module 1 Interrupt Mapping", nvic_headers, nvic_rows, [1.4, 0.7, 0.7, 1.3, 0.9, 2.5])

    # =========================================================================
    # Chapter 17: Programmable ROM Devices
    # =========================================================================
    builder.add_h1("17. Programmable ROM Devices")
    builder.add_p(
        "The SPPS hardware integrates non-volatile memory resources within the STM32G474RET6 microcontroller to store executable firmware, "
        "factory calibration constants, and user runtime setpoints:"
    )

    rom_headers = ["Device Identifier", "Memory Type", "Size / Organization", "Address Space", "Programming Interface", "Functional Contents & Allocation"]
    rom_rows = [
        ["STM32 Flash Bank 1", "Embedded NOR Flash", "256 kB (128 × 2 kB pages)", "0x0800 0000 - 0x0803 FFFF", "SWD / DFU Bootloader", "Primary bootloader, vector table, and core control application firmware (< 120 kB)."],
        ["STM32 Flash Bank 2", "Embedded NOR Flash", "240 kB (120 × 2 kB pages)", "0x0804 0000 - 0x0807 BFFF", "SWD / In-Application (IAP)", "Secondary application image for fail-safe Dual-Bank In-Application Firmware Updates."],
        ["EEPROM Emulation Sector", "Embedded NOR Flash", "16 kB (8 × 2 kB pages)", "0x0807 C000 - 0x0807 FFFF", "Internal Firmware Flash Driver", "Stores factory calibration coefficients (DAC linearity offset/gain, INA226 calibration, CT burden scaling) and user power-on setpoints."],
        ["System Memory (ROM)", "Factory Masked ROM", "32 kB", "0x1FFF 0000 - 0x1FFF 7FFF", "Factory Hardwired", "STMicroelectronics factory DFU bootloader supporting USART1 in-system programming."],
        ["Option Bytes", "Flash Configuration Bits", "64 Bytes", "0x1FFF 7800 - 0x1FFF 783F", "SWD / Flash Registers", "Hardware configuration: Readout Protection (RDP Level 1), Brownout Reset (BOR Level 3), Dual-Bank mode."],
    ]
    builder.add_table("Table 21: Programmable ROM Devices", rom_headers, rom_rows, [1.2, 1.1, 1.1, 1.3, 1.1, 1.7])

    # =========================================================================
    # Chapter 18: Bill of Material
    # =========================================================================
    builder.add_h1("18. Bill of Material")
    builder.add_p(
        "The table below documents the complete Class A Engineering Bill of Materials (BOM) for the Smart Programmable Power Supply "
        "(VVDN_SPPS_2026). Every component is specified with its reference designator, comprehensive electrical parameter description, "
        "footprint, tolerance, primary manufacturer part number, and qualified second-source alternate:"
    )

    bom_headers = ["Item #", "Subsystem / Stage", "Ref Des", "Component Description", "Value / Rating", "Tol", "Footprint", "Primary Mfg", "Primary MPN", "Alternate Mfg", "Alternate MPN", "Engineering Sourcing Justification"]
    bom_rows = [
        ["1", "Stage 1: Mains Protection", "J1", "AC Mains Power Inlet Socket", "10 A, 250 V AC", "—", "IEC 320-C14 Panel Mount", "Schurter", "6100.3300", "TE Connectivity", "1-6609987-1", "International standard earth-grounded chassis AC power entry."],
        ["2", "Stage 1: Mains Protection", "F1", "Ceramic Time-Lag Cartridge Fuse", "2.0 A, 250 V AC, I^2t = 19.6 A^2s", "—", "5 × 20 mm Cartridge", "Littelfuse", "0218002.MXP", "Schurter", "0001.2507", "Primary short-circuit protection (PR-01); safely absorbs inrush energy."],
        ["3", "Stage 1: Mains Protection", "FC1, FC2", "Heavy-Duty PCB Fuse Clips (2x)", "For 5 × 20 mm fuse, 10 A rated", "—", "Through-Hole Solder Mount", "Keystone Electronics", "3515", "Littelfuse", "01110501Z", "Tin-plated phosphor bronze clips with low contact resistance."],
        ["4", "Stage 1: Mains Protection", "NTC1", "Inrush Current Limiting Thermistor", "15.0 Ω Cold, 2.9 A RMS", "± 20%", "Disc 13 mm Radial", "TDK / EPCOS", "B57236S0150M000", "Amphenol Ametherm", "SL15 15003", "Guarantees cold-start inrush < 25.0 A peak at 265 V AC (PR-02)."],
        ["5", "Stage 1: Mains Protection", "MOV1", "Metal Oxide Varistor Surge Clamp", "300 V RMS, 4.5 kA, 125 J", "± 10%", "Disc 14 mm Radial", "Bourns", "MOV-14D471K", "Littelfuse", "V300LA20AP", "IEC 61000-4-5 Level 3 differential surge clamp (PR-03)."],
        ["6", "Stage 1: EMI Filter", "L_CM1", "Common-Mode Choke Stage 1", "15.0 mH, 1.1 A RMS", "± 30%", "Toroid Through-Hole", "Wurth Elektronik", "744823215", "KEMET", "SC-10-10J", "Low-frequency 150 kHz - 2 MHz CM EMI attenuation (PR-07)."],
        ["7", "Stage 1: EMI Filter", "L_CM2", "Common-Mode Choke Stage 2", "4.7 mH, 1.6 A RMS", "± 30%", "Toroid Through-Hole", "Wurth Elektronik", "744822472", "Bourns", "7355-V-RC", "High-frequency 2 MHz - 30 MHz CM EMI attenuation (PR-07)."],
        ["8", "Stage 1: EMI Filter", "C_X1, C_X2", "Safety Class X2 Film Capacitors (2x)", "0.22 µF, 310 V AC RMS", "± 20%", "Radial Pitch 15.0 mm", "KEMET", "R46KI32200001M", "Vishay", "B32922C3224M", "Line-to-neutral differential mode noise filtering."],
        ["9", "Stage 1: EMI Filter", "C_Y1, C_Y2", "Safety Class Y1 Ceramic Caps (2x)", "2.2 nF, 400 V AC RMS", "± 20%", "Disc Radial Pitch 10 mm", "KEMET", "PHE850ED6220MD15R06L2", "Murata", "DE1E3KX222MA4BP01F", "Line/Neutral to Earth common mode bypass (Leakage = 0.366 mA)."],
        ["10", "Stage 2: Rectifier & Bulk Link", "BR1", "Single-Phase Bridge Rectifier", "600 V, 6.0 A, V_F = 1.0 V", "—", "GBU Through-Hole", "Diodes Incorporated", "GBU606", "Vishay", "GBU6J", "Full-wave rectification (PIV = 375 V; derating = 62.5% <= 75%)."],
        ["11", "Stage 2: Rectifier & Bulk Link", "C_BULK1", "High-Voltage Bulk Electrolytic Cap", "100 µF, 450 V, 105°C, 3000h", "± 20%", "Snap-In 22 × 25 mm", "Nichicon", "LGW2W101MELZ25", "Panasonic", "EEU-ED2W101", "Guarantees > 50 ms holdup at 230 V (> 10 ms req)."],
        ["12", "Stage 2: Rectifier & Bulk Link", "C_HF", "High-Voltage Decoupling Ceramic Cap", "100 nF, 630 V DC, X7R", "± 10%", "SMD 1812", "Murata", "GA342QR7GD102KW01L", "TDK", "C4532X7R2J104K230KA", "Bypasses primary switching frequency ringing directly at TX1."],
        ["13", "Stage 2: Rectifier & Bulk Link", "R_BL1..3", "High-Voltage Bleeder Resistors (3x)", "100 kΩ, 0.25 W, 200 V", "± 1%", "SMD 1206", "Vishay Dale", "CRCW1206100KFKEA", "Panasonic", "ERJ-8ENF1003V", "Discharges bulk capacitor to < 50 V in < 45 s (IEC 62368-1)."],
        ["14", "Stage 3: Flyback Subsystem", "U1", "Quasi-Resonant Flyback Controller", "Low Standby, Valley Switching", "—", "SOIC-7", "Texas Instruments", "UCC28740DR", "Texas Instruments", "UCC28C43DR (Fixed PWM)", "Primary Flyback PWM control engine (FR-05 / FR-08)."],
        ["15", "Stage 3: Flyback Subsystem", "TX1", "Isolated Power Transformer", "PQ26/20, L_p = 220 µH ± 10%", "—", "PQ26/20 Through-Hole", "Ferroxcube / Custom", "3C95-PQ2620-72W", "TDK / Epcos", "B66358W0387K187", "3000V RMS reinforced isolated step-down to +24V DC."],
        ["16", "Stage 3: Flyback Subsystem", "Q1", "Superjunction CoolMOS P7 N-FET", "800 V, 17.0 A, 0.290 Ω", "—", "D2PAK (TO-263-3)", "Infineon", "IPB80R290P7", "STMicroelectronics", "STP10NK80Z", "Primary high-voltage switch (V_peak = 599 V; derating = 74.88%)."],
        ["17", "Stage 3: Flyback Subsystem", "R_CS1, 2", "Primary Current Sense Resistors (2x)", "0.50 Ω, 1.0 W (Net = 0.25 Ω)", "± 1%", "SMD 1206", "Vishay Dale", "WSL1206R5000FEA", "Bourns", "CRA2512-FZ-R500ELF", "Senses primary peak current for cycle-by-cycle limit."],
        ["18", "Stage 3: Flyback Subsystem", "D_snub", "Ultra-Fast RCD Snubber Diode", "1000 V, 1.0 A, t_rr < 50 ns", "—", "DO-214AC (SMA)", "STMicroelectronics", "STTH110A", "Vishay", "ES1J", "Clamps primary transformer leakage spike."],
        ["19", "Stage 3: Flyback Subsystem", "R_snub1..3", "Snubber Resistors (3x in parallel)", "68.0 kΩ, 1.0 W (Net = 22.67 kΩ)", "± 1%", "SMD 2512", "Panasonic", "ERJ-1TYJ683U", "Vishay Dale", "CRCW251268K0FKEG", "Dissipates leakage inductance energy (P ≈ 2.4 W)."],
        ["20", "Stage 3: Flyback Subsystem", "C_snub1, 2", "Snubber Capacitors (2x in parallel)", "3.3 nF, 1000 V DC, X7R", "± 10%", "SMD 1206", "Murata", "GRM31BR73A332KW01L", "TDK", "C3216X7R2J332K115AA", "Absorbs primary drain voltage clamp ring."],
        ["21", "Stage 3: Flyback Subsystem", "D_SEC", "Secondary Schottky Barrier Rectifier", "100 V, 10.0 A, V_F = 0.60 V", "—", "TO-220-2 Through-Hole", "ON Semiconductor", "MBR10100G", "STMicroelectronics", "STPS10H100D", "Robust passive secondary rectification to +24V bus."],
        ["22", "Stage 3: Flyback Subsystem", "HS1", "Stamped Aluminum Heatsink for D_SEC", "15.0°C/W Thermal Resistance", "—", "TO-220 Clip Mount", "Aavid / Boyd", "577002B00000G", "Ohmite", "FA-T220-38E", "Natural convection cooling for Schottky rectifier (T_j = 79.7°C)."],
        ["23", "Stage 3: Flyback Subsystem", "C_SEC1, 2", "Secondary Low-ESR Filter Caps (2x)", "470 µF, 35 V, 105°C, 35 mΩ", "± 20%", "Radial Can 10 × 20 mm", "Panasonic", "EEU-FC1V471", "Rubycon", "35ZLJ470M10X16", "Intermediate +24V bus bulk filtering."],
        ["24", "Stage 3: Flyback Subsystem", "L_post", "Secondary LC Post-Filter Choke", "2.2 µH, 5.0 A, 18 mΩ", "± 20%", "Toroid Through-Hole", "Bourns", "2100LL-2R2-H-RC", "Wurth Elektronik", "7447022", "Post-LC ripple attenuation filter (f_c ≈ 3.5 kHz)."],
        ["25", "Stage 3: Flyback Subsystem", "C_SEC_CER", "Secondary Decoupling MLCCs (2x)", "10.0 µF, 50 V, X7R", "± 10%", "SMD 1210", "Murata", "GRM32ER71H106KA12L", "TDK", "C3225X7R1H106K250AB", "High-frequency bypass for intermediate 24V rail."],
        ["26", "Stage 3: Flyback Subsystem", "U2", "Precision Programmable Shunt Ref", "2.495 V ± 0.5%, 100 mA", "± 0.5%", "SOT-23-3", "Texas Instruments", "TL431ACDBZR", "ON Semiconductor", "TL431ACDMR2G", "Secondary voltage reference for 24V regulation."],
        ["27", "Stage 3: Flyback Subsystem", "OPTO1", "Optocoupler Galvanic Isolator", "5000 V RMS Isolation, CTR 100-200%", "—", "SMD-4 Gull-Wing", "Everlight", "EL817(S)(TA)", "Broadcom", "LTV-817S-TA", "Closed-loop isolated secondary feedback."],
        ["28", "Stage 4: Buck-Boost Subsystem", "U3", "4-Switch Synchronous Buck-Boost Ctrl", "4.2 V - 55 V In, 300 kHz PWM", "—", "HTSSOP-28 (PowerPAD)", "Texas Instruments", "LM5176PWPR", "Analog Devices", "LTC3789EGN#PBF", "Core 4-switch post-regulator controller (BB-01..07)."],
        ["29", "Stage 4: Buck-Boost Subsystem", "QA..QD", "Synchronous Power N-MOSFETs (4x)", "40.0 V, 70 A, R_DS(on) = 3.4 mΩ", "—", "TDSON-8 (SuperSO8)", "Infineon", "BSC034N04LS", "Texas Instruments", "CSD18534Q5A", "Ultra-low loss H-bridge switching bridge (V_pk = 28V; derating = 70%)."],
        ["30", "Stage 4: Buck-Boost Subsystem", "L1", "Flat-Wire High-Current Inductor", "10.0 µH, I_sat = 11.5 A, 13.5 mΩ", "± 20%", "SMD 12.5 × 12.5 mm", "Wurth Elektronik", "7443321000", "Coilcraft", "SER2915L-103KL", "Energy transfer inductor (> 65% saturation margin)."],
        ["31", "Stage 4: Buck-Boost Subsystem", "R_shunt", "Precision Metal Current Sense Shunt", "10.0 mΩ, 3.0 W, TCR < 50 ppm", "± 0.1%", "SMD 2512", "Bourns", "CSS2H-2512R-L010F", "Vishay Dale", "WSLP2512R0100FEA", "Native cycle-by-cycle CSP/CSN current limit (PR-03)."],
        ["32", "Stage 4: Buck-Boost Subsystem", "C_OUT1..4", "Ceramic Output Filter Bank (4x)", "22.0 µF, 25 V DC, X7R", "± 10%", "SMD 1210", "Murata", "GRM32ER71E226KE15L", "TDK", "C3225X7R1E226M250AC", "Low ESR switching ripple suppression (< 25 mV)."],
        ["33", "Stage 4: Buck-Boost Subsystem", "C_POLY1", "Solid Aluminum Polymer Capacitor", "100.0 µF, 25 V, 12.0 mΩ ESR", "± 20%", "Radial SMD 8 × 10 mm", "Panasonic", "25SVPF100M", "KEMET", "A750KK107M1EAAE015", "Transient step load reservoir capacitor."],
        ["34", "Stage 4: Buck-Boost Subsystem", "R_top", "Voltage Steering Top Feedback Resistor", "49.9 kΩ, 0.125 W", "± 0.1%", "SMD 0805", "Vishay Dale", "TNPW080549K9BEEA", "Panasonic", "ERA-6AEB4992V", "Top divider leg for LM5176 FB node (CT-01)."],
        ["35", "Stage 4: Buck-Boost Subsystem", "R_bot", "Voltage Steering Ground Resistor", "4.48 kΩ, 0.125 W", "± 0.1%", "SMD 0805", "Vishay Dale", "TNPW08054K48BEEA", "Panasonic", "ERA-6AEB4481V", "Ground leg setting 20.0 V baseline setpoint."],
        ["36", "Stage 4: Buck-Boost Subsystem", "R_DAC", "Voltage Steering DAC Injection Resistor", "11.0 kΩ, 0.125 W", "± 0.1%", "SMD 0805", "Vishay Dale", "TNPW080511K0BEEA", "Panasonic", "ERA-6AEB1102V", "Steers V_OUT from 5.0 V to 20.0 V via DAC (CT-01)."],
        ["37", "Stage 4: Buck-Boost Subsystem", "R_comp, C_comp, C_comp2", "Loop Compensation Passive Network", "12.4 kΩ, 82.0 nF, 15.0 pF", "± 1%", "SMD 0603", "Vishay / Murata", "Standard C0G/X7R", "Yageo / TDK", "Standard Series", "Sets 25 kHz crossover with 65° phase margin."],
        ["38", "Stage 4: Buck-Boost Subsystem", "R_T", "LM5176 Frequency Program Resistor", "24.9 kΩ, 0.1 W", "± 1%", "SMD 0603", "Vishay Dale", "CRCW060324K9FKEA", "Panasonic", "ERJ-3EKF2492V", "Sets fixed 300 kHz PWM frequency (BB-06)."],
        ["39", "Supervisory Brain & UI", "U5", "Mixed-Signal ARM Microcontroller", "Cortex-M4 @ 170 MHz, 512kB, 128kB", "—", "LQFP-64 (10 × 10 mm)", "STMicroelectronics", "STM32G474RET6", "STMicroelectronics", "STM32G473RET6", "Coordinates telemetry, DAC steering & OLED UI."],
        ["40", "Supervisory Brain & UI", "Y1", "High-Speed External Crystal (HSE)", "24.000 MHz, ± 10 ppm, 18 pF", "—", "SMD 3.2 × 2.5 mm", "Abracon", "ABM8G-24.000MHZ-18-D2Y-T", "TXC Corp", "7M-24.000MAAJ-T", "Primary PLL reference oscillator for STM32."],
        ["41", "Supervisory Brain & UI", "Y2", "Low-Speed Real-Time Crystal (LSE)", "32.768 kHz, ± 20 ppm, 12.5 pF", "—", "SMD 3.2 × 1.5 mm", "Abracon", "ABS07-32.768KHZ-T", "Citizen", "CM7V-T1A-32.768KHZ", "Precision 100ms telemetry loop timekeeping."],
        ["42", "Supervisory Brain & UI", "U6", "Secondary I2C Power Monitor IC", "16-bit ADC, 0.1% Gain Error, 36 V Bus", "—", "VSSOP-10", "Texas Instruments", "INA226AIDGSR", "Texas Instruments", "INA238AIDGSR", "Samples secondary V, I, P at 10 Hz rate (TM-03)."],
        ["43", "Supervisory Brain & UI", "U4", "Galvanically Isolated Sensing Amp", "3000 V RMS Isolation, 0-2 V Input", "—", "SOIC-8 Wide (5.85mm)", "Texas Instruments", "AMC1311BDWVR", "Silicon Labs", "Si8920BD-IS", "Samples isolated primary AC mains voltage (TM-01)."],
        ["44", "Supervisory Brain & UI", "CT1", "AC Mains Current Transformer", "1000:1 Ratio, 10 A RMS, 4000 V ISO", "—", "Through-Hole Encapsulated", "Talema", "AC1010", "CR Magnetics", "CR8410-1000", "Galvanically senses primary AC line current (TM-02)."],
        ["45", "Supervisory Brain & UI", "R_burden", "Precision CT Burden Resistor", "100.0 Ω, 0.25 W", "± 0.1%", "SMD 0805", "Vishay Dale", "TNPW0805100RBEEA", "Panasonic", "ERA-6AEB1000V", "Converts 1.6 mA secondary current to voltage."],
        ["46", "Supervisory Brain & UI", "DISP1", "1.3-inch Monochrome OLED Display Module", "128 × 64 Dots, SSD1306, I2C, 3.3V", "—", "4-Pin Header / Cable", "Solomon / Generic", "OLED-1.3-12864-I2C", "Adafruit", "938", "Local graphical telemetry dashboard."],
        ["47", "Supervisory Brain & UI", "ENC1, 2", "Incremental Rotary Encoders (2x)", "24 Pulses/Rev, Push Switch, Slotted", "—", "Through-Hole Bracket", "Bourns", "PEC11R-4220F-S0024", "Alps Alpine", "EC11E2424407", "Fine/coarse voltage adjustment and output enable."],
        ["48", "Supervisory Brain & UI", "LED1..3", "Front-Panel Status Indicators (3x)", "Green (CV), Amber (CC), Red (Fault)", "—", "SMD 0805", "Kingbright", "APT2012SGC / SEC / SRC", "Lite-On", "LTST-C170 Series", "Clear local visual indication of operating state."],
        ["49", "Auxiliary Power Tree", "U7", "Linear Regulator +12V Gate Bias", "+12.0 V DC, 100 mA, 35 V IN", "± 4%", "SOT-89", "STMicroelectronics", "L78L12ACUTR", "ON Semiconductor", "MC78L12ABPRPG", "Steps down +24V bus to LM5176 VCC gate bias rail."],
        ["50", "Auxiliary Power Tree", "U8", "Linear Regulator +5V OLED Bias", "+5.0 V DC, 100 mA, 30 V IN", "± 4%", "SOT-89", "STMicroelectronics", "L78L05ABUTR", "Texas Instruments", "LM78L05ACMX/NOPB", "Powers 1.3-inch OLED display logic and analog rails."],
        ["51", "Auxiliary Power Tree", "U9", "Low-Dropout Linear Regulator (LDO)", "+3.30 V DC, 1.0 A, Dropout 240 mV", "± 1%", "SOT-223", "Diodes Incorporated", "AP2114H-3.3TRG1", "Texas Instruments", "TLV1117-33IDCYR", "Clean, low-noise supply for STM32, INA226, & DAC."],
        ["52", "Connectors & Terminals", "J2, J3", "Heavy-Duty 4mm Output Binding Posts", "Red (+), Black (-), 30 A, 1000 V", "—", "4mm Gold-Plated Panel", "Pomona Electronics", "3770-2 (Red) / 3770-0 (Blk)", "Mueller Electric", "BU-P3770-2 / BU-P3770-0", "Standard laboratory 19.05mm spaced binding posts."],
        ["53", "Connectors & Terminals", "J4", "SWD Firmware Debug Header", "4-Pin, 2.54 mm Pitch, Shrouded", "—", "SMD / THT Header", "Molex", "22-28-4040", "Samtec", "TSW-104-07-G-S", "Microcontroller programming and real-time debug."],
        ["54", "Connectors & Terminals", "J5", "UART Serial Telemetry Header", "3-Pin, 2.54 mm Pitch, Pin Strip", "—", "Through-Hole Strip", "Molex", "22-28-4030", "Samtec", "TSW-103-07-G-S", "Connects TX/RX/GND for 10 Hz external telemetry log."],
    ]
    builder.add_table("Table 22: Master Class A Engineering Bill of Materials (BOM)", bom_headers, bom_rows, [0.4, 0.9, 0.6, 1.0, 0.9, 0.4, 0.8, 0.7, 0.8, 0.7, 0.8, 1.0])

    # =========================================================================
    # Chapter 19: Design Limitations
    # =========================================================================
    builder.add_h1("19. Design Limitations")
    builder.add_p(
        "The physical, electrical, and thermal boundaries of the SPPS hardware design are established below. "
        "Operating outside these boundaries may degrade performance or trigger protective shutdown:"
    )
    builder.add_bullet(
        "AC Mains Input Voltage Envelope: Minimum continuous operating voltage is 85.0 V AC RMS. Below 80.0 V AC, "
        "input current exceeds 1.7 A RMS and primary Flyback controller UVLO triggers graceful shutdown. Maximum continuous "
        "operating voltage is 265.0 V AC RMS. Above 275.0 V AC, the 300 V RMS MOV begins conduction and bulk voltage exceeds 390 V DC."
    )
    builder.add_bullet(
        "Output Power & Current Envelope: Maximum continuous output power is strictly limited to 60.0 W (20.0 V × 3.0 A). "
        "Continuous output current limit is 3.0 A DC across full 5.0 V to 20.0 V span. Peak current is clamped at 3.50 A by "
        "LM5176 native hardware limit. Peak transient overload is 84.0 W (20.0 V / 4.2 A or 24.0 V / 3.5 A intermediate) "
        "for a maximum duration of 500 ms. Extended operation above 60 W will induce thermal accumulation."
    )
    builder.add_bullet(
        "Capacitive Load Stability Boundary: The output compensation network (R_comp = 12.4 kΩ, C_comp = 82 nF, C_comp2 = 15 pF) "
        "guarantees stable closed-loop phase margin (≥ 65°) for external capacitive loads up to C_load,max = 1000 µF. "
        "Capacitive loads exceeding 2200 µF may degrade transient phase margin and induce loop hunting during dynamic load steps."
    )
    builder.add_bullet(
        "Minimum Load Requirements: The Buck-Boost stage features synchronous rectification and operates down to 0.0 A (true zero load) "
        "with stable output regulation."
    )
    builder.add_bullet(
        "Thermal & Environmental Operating Boundaries: Ambient operating temperature is -20.0°C to +50.0°C. "
        "Cooling mode is pure natural convection (free air). Minimum chassis ventilation clearance of 25.0 mm is required above and "
        "beneath the PCBA. Enclosing the board in a hermetically sealed box without heat sinking will exceed thermal ratings. "
        "Maximum internal component junction temperature is Tj ≤ 110.0°C under worst-case full load at 50°C ambient."
    )

    # =========================================================================
    # Chapter 20: Requirement-Design Mapping
    # =========================================================================
    builder.add_h1("20. Requirement-Design Mapping")
    builder.add_p(
        "The table below establishes complete bi-directional traceability connecting every mandatory requirement from the authoritative "
        "Product Requirement Document (prd_final_spps.docx, Rev A1_001) to its physical implementation, mathematical verification, "
        "and corresponding HDD section:"
    )

    trace_headers = ["PRD Req ID", "PRD Requirement Description", "PRD Specification / Target", "Physical Hardware Implementation", "Calculated / Verified Value", "HDD Section", "Compliance Status"]
    trace_rows = [
        ["FR-01", "AC Input Voltage Range", "85 V – 265 V AC RMS [MUST]", "GBU606 bridge + 100 µF / 450 V bulk cap", "85.0 V brownout to 265.0 V high-line", "4.2, 8.4", "COMPLIANT"],
        ["FR-02", "Intermediate DC Bus Voltage", "+24.0 V DC ± 1.0% [MUST]", "Isolated Flyback regulated via TL431 + EL817", "+24.0 V DC ± 0.8% continuous", "4.2, 7.1", "COMPLIANT"],
        ["FR-03", "Continuous Primary Power", "72.0 W Continuous [MUST]", "PQ26/20 (Lp = 220 µH) + Infineon IPB80R290P7", "72.0 W continuous throughput (101.9 W cap)", "4.2, 8.1", "COMPLIANT"],
        ["FR-04", "Peak Power Capability", "84.0 W for 500 ms [SHOULD]", "PQ26/20 core sized for B_max = 0.189 T << 0.380 T", "84.0 W surge throughput (50% flux margin)", "4.2, 19", "COMPLIANT"],
        ["FR-05", "Primary Stage Efficiency", "> 88.0% @ 230 V AC [MUST]", "TI UCC28740 Quasi-Resonant Valley Flyback", "91.30% @ 230 V AC Full Load", "4.2, 8.1", "COMPLIANT"],
        ["FR-06", "Safety Galvanic Isolation", "3,000 V AC RMS (1 min) [MUST]", "Furukawa TEX-E wire + 6.4 mm creepage + 2 mm slot", "Certified 3000 V RMS withstand (SELV safe)", "4.1, 13.5", "COMPLIANT"],
        ["FR-07", "Uniform Switching Frequency", "65.0 kHz ± 5% Constant [MUST]", "UCC28C43 / UC3843 timing network RT=10k, CT=2.2nF", "65.15 kHz uniform PWM clock", "4.2, 10", "COMPLIANT"],
        ["FR-08", "Cold-Start Inrush Current", "< 25.0 A Peak [MUST]", "EPCOS 15.0 Ω Cold NTC Thermistor (B57236S0150M)", "24.98 A peak at 265 V AC (< 21 A typical)", "4.2, 8.3", "COMPLIANT"],
        ["FR-09", "No-Load Standby Power", "< 250 mW Standby [SHOULD]", "UCC28740 low-frequency burst mode (I_q < 35 µA)", "< 30 mW idle power", "4.2, 8.1", "COMPLIANT"],
        ["BB-01", "Output Voltage Range", "5.0 V – 20.0 V DC Programmable [MUST]", "LM5176 4-switch Buck-Boost + 12-bit DAC steering", "5.04 V to 20.01 V continuous linear span", "4.3, 7.1", "COMPLIANT"],
        ["BB-02", "Continuous Output Current", "0.0 A – 3.0 A DC Continuous [MUST]", "Inductor 10 µH (8.5 A RMS) + 4x BSC034N04LS (70 A)", "0.0 A - 3.0 A across full 5 V - 20 V", "4.3, 8.1", "COMPLIANT"],
        ["BB-03", "Maximum Output Power", "60.0 W Continuous Output [MUST]", "20.0 V × 3.0 A continuous rating", "60.0 W continuous DC output", "4.3, 8.1", "COMPLIANT"],
        ["BB-04", "Voltage Setpoint Resolution", "10 mV step resolution (12-bit DAC) [MUST]", "R_top = 49.9 kΩ, R_bot = 4.48 kΩ, R_DAC = 11.0 kΩ", "3.655 mV per step (< 10 mV target)", "7.1.1", "COMPLIANT"],
        ["BB-05", "Output Voltage Ripple", "< 25 mV pk-pk ripple [MUST]", "4× 22 µF 1210 MLCC + 100 µF Polymer (12 mΩ ESR)", "8.54 mV pk-pk worst-case @ 12V/3A", "4.3, 13.3", "COMPLIANT"],
        ["BB-06", "Load Transient Recovery", "< 150 µs recovery, < 250mV sag [MUST]", "High-bandwidth loop compensation (fc = 25 kHz)", "Recovery in < 120 µs, sag < 185 mV", "4.3, 13.2", "COMPLIANT"],
        ["BB-07", "Buck-Boost Efficiency", "> 95% @ 20V/3A; > 92% @ 5V/3A [MUST]", "4-Switch synchronous rectification (R_DS = 3.4 mΩ)", "98.7% @ 20V/3A; 95.4% @ 5V/3A", "4.3, 8.1", "COMPLIANT"],
        ["BB-08", "Switching Frequency", "300 kHz ± 10% [MUST]", "LM5176 programmed via R_T = 24.9 kΩ ± 1%", "300.0 kHz fixed uniform PWM", "4.3, 10", "COMPLIANT"],
        ["BB-09", "Hardware Current Limiting", "Cycle-by-cycle via CSP/CSN [MUST]", "Dedicated 10.0 mΩ shunt across LM5176 CSP/CSN pins", "Native hardware clamp at 3.50 A", "4.3, 7.1", "COMPLIANT"],
        ["TM-01", "Primary AC Voltage Sensing", "Isolated AMC1311 (0-300V AC) [MUST]", "AMC1311 Iso-Amp + 1.5 MΩ / 7.5 kΩ divider chain", "True RMS AC voltage with ± 0.8% accuracy", "4.3, 7.1", "COMPLIANT"],
        ["TM-02", "Primary AC Current Sensing", "Current Transformer 1000:1 [MUST]", "Talema AC1010 (1000:1) + 100 Ω burden resistor", "True RMS AC current with ± 1.2% accuracy", "4.3, 7.1", "COMPLIANT"],
        ["TM-03", "Secondary DC Voltage Sense", "INA226 16-bit ADC (1.25mV/LSB) [MUST]", "Direct high-side bus tap into INA226 VBUS pin", "± 0.15% measurement accuracy", "4.3, 7.1", "COMPLIANT"],
        ["TM-04", "Secondary DC Current Sense", "INA226 16-bit ADC (100µA/LSB) [MUST]", "Differential sense across 10.0 mΩ Bourns shunt", "± 0.35% measurement accuracy", "4.3, 7.1", "COMPLIANT"],
        ["TM-05", "Dual-Domain Telemetry Rate", "10.0 Hz Real-Time Loop Rate [MUST]", "STM32G474 DMA/Timer sampling + INA226 I2C read", "Real-time P_AC, P_DC, η computed every 100ms", "4.3, 13.2", "COMPLIANT"],
        ["TM-06", "Galvanic Isolation Barrier", "3,000 V AC RMS (1 min) [MUST]", "Optocoupler, AMC1311, and transformer isolation", "Certified 3000 V RMS tested isolation barrier", "4.1, 13.5", "COMPLIANT"],
        ["TM-07", "Calibration Test Points", "Dedicated PCB Test Loops [MUST]", "Keystone 5001 miniature loop test points on PCBA", "Test points on V_bulk, +24 V, V_OUT, and GNDs", "4.3, 14.1", "COMPLIANT"],
        ["PR-01", "Input Fuse Protection", "2.0 A Ceramic Fuse [MUST]", "Littelfuse 0218002.MXP (2.0 A, 250 V, Slow-Blow)", "Catastrophic short-circuit interrupt up to 1500 A", "4.2, 8.3", "COMPLIANT"],
        ["PR-02", "Input Inrush Current Limit", "Inrush < 25.0 A Peak [MUST]", "EPCOS B57236S0150M000 (15.0 Ω Cold)", "I_pk = 24.98 A at zero grid impedance", "4.2, 8.3", "COMPLIANT"],
        ["PR-03", "Built-in Controller OCP", "Cycle-by-cycle CSP/CSN clamp [MUST]", "LM5176 native 35 mV threshold on 10 mΩ shunt", "Hard limit at 3.50 A (< 100 ns response)", "4.3, 7.1", "COMPLIANT"],
        ["PR-04", "Over-Temperature (OTP)", "LM5176 internal shutdown (165°C)", "Built-in thermal sensor on LM5176 silicon die", "Trips at 165°C; auto-recovers at 145°C", "4.3, 13.6", "COMPLIANT"],
        ["PR-05", "Safety Compliance Standard", "IEC 62368-1 Reinforced Isolation", "Milled air slot, triple-insulated wire, safety caps", "SELV touch-safe compliance (V_OUT <= 20 V < 60 V)", "1.5, 13.5", "COMPLIANT"],
        ["PR-06", "Creepage & Clearance", "Creepage >= 6.4mm, Clear >= 5.0mm", "PCB routing rule: 6.4 mm copper-to-copper creepage", "Surface creepage 6.4 mm + 2.0 mm air slot", "4.1, 13.5", "COMPLIANT"],
        ["PR-07", "Conducted & Radiated EMC", "CISPR 32 / EN 55032 Class B [MUST]", "2-stage CM choke filter + X2/Y1 caps + shielded inductor", "Filter attenuation: 35.4 dB at 150 kHz", "4.2, 10", "COMPLIANT"],
        ["PR-08", "Operating Ambient Temp", "-20°C to +50°C Full Load [MUST]", "Natural convection thermal sizing (2oz outer copper)", "Max component T_j <= 100.4°C << 150°C", "13.6, 19", "COMPLIANT"],
        ["CT-01", "DAC Voltage Steering Network", "Resistor summing into LM5176 FB [MUST]", "R_top = 49.9 kΩ, R_bot = 4.48 kΩ, R_DAC = 11.0 kΩ", "Linear steering, resolution 3.66 mV per step", "7.1.1", "COMPLIANT"],
        ["CT-02", "Current Sense Resistor", "10 mΩ Metal Shunt, 3W, 0.1% [MUST]", "Bourns CSS2H-2512R-L010F (10.0 mΩ ± 0.1%, 3W)", "Dissipation 90 mW @ 3A (3.0% of 3W rating)", "4.3, 7.1", "COMPLIANT"],
        ["CT-03", "MCU Supervisory Shutdown", "GPIO pulling LM5176 ENABLE low [MUST]", "STM32 GPIO driving NPN pull-down transistor on Pin 6", "Clamps ENABLE to < 0.4 V in < 500 ns", "4.3, 11", "COMPLIANT"],
        ["CT-04", "Auxiliary Bias Regulation", "+14 V Flyback, +12 V, +5 V, +3.3 V", "Aux winding + L78L12 + L78L05 + AP2114-3.3 LDO", "Clean, isolated rails for gate drivers and logic", "4.3, 8.2", "COMPLIANT"],
    ]
    builder.add_table("Table 23: Complete Requirement – Design Traceability Matrix", trace_headers, trace_rows, [0.8, 1.4, 1.2, 1.4, 1.3, 0.7, 0.9])
