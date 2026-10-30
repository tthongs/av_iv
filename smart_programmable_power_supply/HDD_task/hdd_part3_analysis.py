"""
Hardware Design Document - Part 3: Chapters 9 to 13
9. Battery Powered Design
10. Clock Scheme
11. Reset Scheme
12. Hardware Configurations
13. Design Analysis – Subsystem1
"""

def add_part3(builder):
    # =========================================================================
    # Chapter 9: Battery Powered Design
    # =========================================================================
    builder.add_h1("9. Battery Powered Design")
    builder.add_h2("9.1 Subsystem1 [Main Board]")
    builder.add_callout(
        "Engineering Status: NOT APPLICABLE (Out of Scope per PRD Rev A1_001 Section 10). "
        "The Smart Programmable Power Supply (VVDN_SPPS_2026) is an AC mains-powered benchtop instrument and ATE modular supply. "
        "Internal chemical battery packs, battery charge controllers, and cell balancing circuits are excluded from the design baseline.",
        "NOTE"
    )
    builder.add_p(
        "Line dropout immunity and transient brownout bridging are accomplished entirely through electrostatic energy storage in the "
        "primary high-voltage bulk capacitor bank (C_BULK1, 100 µF / 450 V). The table below demonstrates compliance with the > 10.0 ms "
        "grid dropout holdup requirement across the entire AC operating envelope:"
    )

    holdup_headers = ["AC Line Voltage Condition", "Bulk DC Bus Voltage (V_DC)", "Available Energy Storage (J)", "Full Load Run Time Holdup", "PRD Specification Target", "Compliance Status"]
    holdup_rows = [
        ["230 V AC Nominal (Europe/Asia)", "+325.3 V DC", "4.48 Joules", "53.2 ms", "> 10.0 ms Holdup", "PASS (5.3x Safety Margin)"],
        ["120 V AC Nominal (North America)", "+169.7 V DC", "1.02 Joules", "12.8 ms", "> 10.0 ms Holdup", "PASS (1.28x Margin)"],
        ["85 V AC Minimum (Brownout Limit)", "+120.2 V DC", "0.45 Joules", "10.4 ms", "> 10.0 ms Holdup", "PASS (Meets Requirement)"],
    ]
    builder.add_table("Table 10: AC Line Dropout Energy Storage and Holdup Time Analysis", holdup_headers, holdup_rows, [1.5, 1.1, 1.1, 1.1, 1.1, 1.1])

    # =========================================================================
    # Chapter 10: Clock Scheme
    # =========================================================================
    builder.add_h1("10. Clock Scheme")
    builder.add_p(
        "The PCBA clock scheme establishes clean, jitter-free timing references across the mixed-signal microcontroller, "
        "telemetry engine, and switching power stages while mitigating electromagnetic interference (EMI):"
    )

    clk_headers = ["Clock Domain / Source", "Oscillator Component", "Nominal Frequency", "Tolerance / Accuracy", "Circuit Destinations & Functions Served"]
    clk_rows = [
        ["High-Speed Ext (HSE)", "Abracon ABM8G-24.000MHZ-18-D2Y-T", "24.000 MHz", "± 10 ppm", "MCU OSC_IN / OSC_OUT (Pins 5/6). Multiplied by internal PLL to generate 170 MHz CPU core clock and high-resolution timers."],
        ["Low-Speed Ext (LSE)", "Abracon ABS07-32.768KHZ-T", "32.768 kHz", "± 20 ppm", "MCU PC14 / PC15. Drives internal Real-Time Clock (RTC) and precise 100 ms (10.0 Hz) telemetry interrupt scheduling."],
        ["Buck-Boost Clock", "TI LM5176 Internal Oscillator", "300.0 kHz", "± 10%", "Synchronous 4-switch Buck-Boost H-bridge PWM clock. Programmed via precision resistor R_T = 24.9 kΩ ± 1% on Pin 27 (RT)."],
        ["Flyback PWM Clock", "TI UCC28C43 / UC3843 Oscillator", "65.0 kHz", "± 5%", "Primary Flyback switching frequency. Programmed via R_T = 10.0 kΩ ± 1% and C_T = 2.2 nF ± 5% C0G ceramic on Pin 4 (RT/CT)."],
    ]
    builder.add_table("Table 11: Clock Scheme", clk_headers, clk_rows, [1.3, 1.5, 1.0, 1.0, 2.2])

    builder.add_h2("10.1 EMI Harmonic Mitigation via Clock Architecture")
    builder.add_bullet(
        "Deterministic Fundamental Alignment: By locking the Flyback primary switching frequency to exactly 65.0 kHz, "
        "the fundamental switching spike and its first harmonic (130 kHz) fall entirely below the 150 kHz start frequency "
        "of commercial conducted emissions regulations (CISPR 32 / EN 55032)."
    )
    builder.add_bullet(
        "High-Frequency Buck-Boost Spectral Separation: Operating the secondary Buck-Boost post-regulator at 300.0 kHz guarantees that "
        "its fundamental frequency does not beat or intermodulate with the 65.0 kHz primary stage (300 kHz is not an integer multiple of 65 kHz). "
        "The two-stage differential and common-mode input filter provides > 35.4 dB attenuation at 150 kHz, providing robust EMC compliance."
    )

    # =========================================================================
    # Chapter 11: Reset Scheme
    # =========================================================================
    builder.add_h1("11. Reset Scheme")
    builder.add_p(
        "The SPPS hardware integrates a coordinated multi-tier reset and supervisory architecture to guarantee fail-safe initialization, "
        "prevent flash corruption during line brownouts, and provide sub-microsecond supervisory shutdown:"
    )

    builder.add_h2("11.1 Reset Hierarchy and Circuitry")
    builder.add_bullet(
        "Microcontroller Hardware Reset (NRST, Pin 7): Supervised by an external active-low RC filter network (10 kΩ pull-up to +3.3 V, "
        "100 nF X7R ceramic capacitor to ground). Front-panel tactile push-button allows manual system reboot."
    )
    builder.add_bullet(
        "Internal Programmable Brown-Out Reset (BOR): Configured in Flash option bytes to BOR Level 3 (threshold V_BOR ≈ 2.70 V DC). "
        "If the +3.3 V logic supply dips below 2.70 V during power-down or grid sag, the MCU core is held in hard reset, preventing corrupted "
        "Flash writes or errant DAC register updates."
    )
    builder.add_bullet(
        "Flyback Controller Under-Voltage Lockout (UVLO): Primary Flyback controller (U1) features an internal precision UVLO comparator on VCC. "
        "Turn-on threshold is 14.5 V (UCC28740) / 8.4 V (UCC28C43); turn-off threshold is 9.0 V (UCC28740) / 7.6 V (UCC28C43). "
        "Prevents primary gate switching pulses if the bulk DC bus voltage is insufficient to sustain secondary regulation."
    )
    builder.add_bullet(
        "LM5176 Buck-Boost Enable & Hardware UVLO: Pin 6 (ENABLE) features an internal precision comparator with a 1.20 V turn-on threshold "
        "and 100 mV hysteresis. An external resistor divider from the +24.0 V intermediate rail (R1 = 100 kΩ, R2 = 6.8 kΩ) sets a hardware UVLO threshold:\n"
        "   V_bus,UVLO = 1.20 V × [ (100 kΩ + 6.8 kΩ) / 6.8 kΩ ] = 18.85 V DC\n"
        "The Buck-Boost stage is held in hard shutdown until the intermediate rail exceeds +18.85 V DC, preventing abnormal switching currents during primary ramp-up."
    )
    builder.add_bullet(
        "Supervisory MCU Hardware Override: Active NPN pull-down transistor (MMBT3904) driven by MCU pin PB0 allows the supervisory firmware "
        "to override the LM5176 ENABLE pin and collapse power delivery within 500 ns upon fault detection."
    )

    # =========================================================================
    # Chapter 12: Hardware Configurations
    # =========================================================================
    builder.add_h1("12. Hardware Configurations")
    builder.add_h2("12.1 Subsystem1 HW Configurations")

    builder.add_h3("12.1.1 Board Type / Assembly Variant")
    builder.add_p("The SPPS PCBA supports two qualified manufacturing assembly variants sharing a single unified PCB layout:")

    variant_headers = ["Variant Build Code", "Variant Description", "Flyback Controller (U1)", "Inrush Thermistor (NTC1)", "Current Shunt (R_shunt)", "Target Application Space"]
    variant_rows = [
        ["SPPS-STD-01", "Standard Production Benchtop", "TI UCC28740DR (Quasi-Resonant)", "EPCOS 15.0 Ω (B57236S0150M)", "Bourns 10.0 mΩ (CSS2H-2512R)", "Standard laboratory benchtop power supply with ultra-low standby power (< 30 mW)."],
        ["SPPS-IND-02", "Industrial ATE Uniform-Clock", "TI UCC28C43DR (Uniform 65 kHz)", "EPCOS 15.0 Ω (B57236S0150M)", "Bourns 10.0 mΩ (CSS2H-2512R)", "Automated Test Equipment (ATE) rack installations requiring fixed uniform switching frequencies."],
    ]
    builder.add_table("Table 12: Board Variant", variant_headers, variant_rows, [1.1, 1.4, 1.3, 1.1, 1.1, 1.0])

    builder.add_h3("12.1.2 Board Revision")
    builder.add_p("The revision history of the physical PCBA hardware layout is tracked below:")

    rev_headers = ["PCBA Revision", "Release Date", "Description of Changes", "ECO / Release Note"]
    rev_rows = [
        ["Rev A0_01", "06-Oct-2026", "Initial prototype feasibility layout. Dual-board architecture.", "Initial Concept Draft"],
        ["Rev A1_000", "15-Oct-2026", "Consolidated into single 4-layer PCBA with 6.4mm isolation slot.", "Baseline Restructuring"],
        ["Rev A1_001", "30-Oct-2026", "Production-grade release: 15Ω NTC, 10mΩ shunt, 3.66mV DAC steering, Class A BOM.", "Authoritative HDD Release"],
    ]
    builder.add_table("Table 12.1: Board Revision", rev_headers, rev_rows, [1.1, 1.1, 3.3, 1.5])

    builder.add_h3("12.1.3 Jumper Configuration")
    builder.add_p("The PCBA includes three 3-pin 2.54 mm configuration headers for factory testing and serial telemetry routing:")

    jmp_headers = ["Jumper Ref Des", "Jumper Function / Description", "Default Setting", "Alternate Setting", "Functional Behavior"]
    jmp_rows = [
        ["JP1", "UART Telemetry Stream Enable", "Pins 1-2 Shorted (ENABLE)", "Pins 2-3 Shorted (DISABLE)", "Pins 1-2 connects MCU TX (PA9) to telemetry header J5. Pins 2-3 isolates UART to eliminate serial EMI during lab EMC testing."],
        ["JP2", "Auxiliary 24V DC Input Bypass", "Pins 1-2 Shorted (AC Mains)", "Pins 2-3 Shorted (DC Bench)", "Pins 1-2 routes Flyback secondary into Buck-Boost. Pins 2-3 connects external 24 V DC barrel jack (DNP footprint) for battery/bench operation."],
        ["JP3", "MCU Bootloader Mode Select", "Pins 1-2 Shorted (Flash Boot)", "Pins 2-3 Shorted (System DFU)", "Pins 1-2 ties BOOT0 to GND (10 kΩ). Pins 2-3 ties BOOT0 to +3.3 V to invoke factory STM32 ROM bootloader via UART."],
    ]
    builder.add_table("Table 13: Jumper Configuration", jmp_headers, jmp_rows, [0.9, 1.5, 1.2, 1.2, 2.2])

    # =========================================================================
    # Chapter 13: Design Analysis – Subsystem1
    # =========================================================================
    builder.add_h1("13. Design Analysis – Subsystem1")
    builder.add_h2("13.1 DC Analysis")
    builder.add_p(
        "To ensure robust digital logic noise margins across the mixed-signal microcontroller, power monitor, and switching controllers, "
        "DC input/output voltage levels are verified under worst-case temperature (-20°C to +85°C) and +3.3 V ± 5% supply tolerance:"
    )

    dc_hi_headers = ["Driving Signal / Interface", "Driver Component", "V_OH(min) (V)", "I_OH (mA)", "Receiver Component", "V_IH(min) (V)", "I_IH (µA)", "High Noise Margin (V_OH - V_IH)", "Pass / Fail Status"]
    dc_hi_rows = [
        ["I2C1_SCL / SDA", "Pull-Up Resistor (2.2 kΩ)", "3.135 V", "0.0 mA", "INA226 / SSD1306", "2.310 V", "± 1.0 µA", "+0.825 V (26.3%)", "PASS (Exceeds > 0.4V)"],
        ["LM5176_ENABLE", "STM32 Pin PB0 (via NPN)", "2.900 V", "0.62 mA", "MMBT3904 Base", "0.750 V", "620 µA", "+2.150 V (74.1%)", "PASS (Saturates NPN)"],
        ["SWD Debug (SWDIO)", "STM32 Pin PA13", "2.900 V", "4.0 mA", "External Debug Probe", "2.000 V", "± 10 µA", "+0.900 V (31.0%)", "PASS"],
        ["Status LEDs (CV/CC)", "STM32 Pins PC6/PC7", "2.900 V", "1.5 mA", "Kingbright SMD LED", "2.000 V", "1500 µA", "+0.900 V (Forward V)", "PASS"],
    ]
    builder.add_table("Table 14: High-Level DC Noise Margin Analysis [V_OH(min) vs V_IH(min)]", dc_hi_headers, dc_hi_rows, [1.1, 1.0, 0.7, 0.6, 0.9, 0.7, 0.6, 0.8, 0.6])

    dc_lo_headers = ["Driving Signal / Interface", "Driver Component", "V_OL(max) (V)", "I_OL (mA)", "Receiver Component", "V_IL(max) (V)", "I_IL (µA)", "Low Noise Margin (V_IL - V_OL)", "Pass / Fail Status"]
    dc_lo_rows = [
        ["I2C1_SCL / SDA", "INA226 Open-Drain", "0.400 V", "3.0 mA", "STM32 PB8/PB9", "0.990 V", "± 1.0 µA", "+0.590 V (17.9%)", "PASS (Exceeds > 0.4V)"],
        ["LM5176_ENABLE", "MMBT3904 Collector", "0.150 V", "0.50 mA", "LM5176 Pin 6", "0.400 V", "10 µA", "+0.250 V (62.5%)", "PASS (Guarantees OFF)"],
        ["SWD Debug (SWDIO)", "External Debug Probe", "0.400 V", "4.0 mA", "STM32 Pin PA13", "0.990 V", "± 10 µA", "+0.590 V (17.9%)", "PASS"],
        ["Rotary Enc Inputs", "Bourns Mechanical Enc", "0.050 V", "0.33 mA", "STM32 Pins PA0/1", "0.990 V", "± 5.0 µA", "+0.940 V (28.5%)", "PASS"],
    ]
    builder.add_table("Table 15: Low-Level DC Noise Margin Analysis [V_OL(max) vs V_IL(max)]", dc_lo_headers, dc_lo_rows, [1.1, 1.0, 0.7, 0.6, 0.9, 0.7, 0.6, 0.8, 0.6])

    builder.add_h2("13.2 Timing Analysis")
    builder.add_bullet(
        "I2C Bus Timing (Fast-Mode 400 kHz): Clock period T_SCL = 2.50 µs. Bus capacitance C_bus = 35.0 pF. Pull-up resistance R_p = 2.2 kΩ. "
        "Bus rise time t_r = 0.8473 × (2200 Ω) × (35 × 10^-12 F) = 65.2 ns (Standard specifies t_r,max = 300 ns; timing margin = 78.3%). "
        "Bus fall time t_f = 0.23 × (C_bus / I_OL) × Δ V = 0.23 × (35 pF / 3 mA) × 3.3 V = 8.85 ns << 300 ns."
    )
    builder.add_bullet(
        "Hardware Autonomous Overcurrent Clamp Timing: Shunt current trip event to INA240 output rise = 1.20 µs. "
        "TLV3501 comparator trip and transition = 4.5 ns. NPN pull-down saturation and LM5176 COMP capacitor discharge = 250 ns. "
        "LM5176 PWM pulse truncation = 800 ns. Total hardware clamp response time = 2.25 µs << 5.0 µs PRD limit."
    )
    builder.add_bullet(
        "Telemetry Loop Timing & CPU Budget: 10 Hz timer interrupt period = 100.0 ms. I2C reading of INA226 (6 bytes) = 180 µs. "
        "ADC DMA conversion of primary V_AC and I_AC (128 samples averaged) = 45 µs. True RMS power and efficiency mathematical computation = 35 µs. "
        "OLED display frame buffer update (1 kB over I2C) = 24.5 ms. Total CPU active time per 100 ms epoch = 24.76 ms (24.76% CPU loading @ 170 MHz)."
    )

    builder.add_h2("13.3 PCB Layer Stack-up Analysis")
    builder.add_p(
        "To minimize ground bounce, eliminate common-mode noise coupling, and handle continuous 3.0 A DC current without excessive "
        "copper heating, a balanced 4-layer FR4 high-Tg (170°C) stackup with 2.0 oz outer copper is specified:"
    )

    stack_headers = ["Layer #", "Layer Name", "Copper Weight", "Dielectric Thickness", "Material", "Primary Electrical Function & Routing Allocation"]
    stack_rows = [
        ["L1 (Top)", "High-Current Power / Components", "2.0 oz (70 µm)", "0.20 mm Prepreg", "FR4 High-Tg", "AC mains input polygon pours, bulk DC link, primary Flyback switching loop, Buck-Boost H-bridge power polygon pours, surface mount components."],
        ["L2 (In1)", "Continuous Ground Plane", "1.0 oz (35 µm)", "1.00 mm Core", "FR4 High-Tg", "Solid low-impedance ground plane split across galvanic barrier (PGND_HOT / PGND_SEC), providing continuous image return path for L1."],
        ["L3 (In2)", "Auxiliary Power / Intermediate Bus", "1.0 oz (35 µm)", "0.20 mm Prepreg", "FR4 High-Tg", "+24.0 V intermediate power plane, +12 V gate drive plane, +5 V display rail, +3.3 V logic supply copper pours."],
        ["L4 (Bot)", "Signal Routing & Heatsink Copper", "2.0 oz (70 µm)", "—", "FR4 High-Tg", "Secondary quiet signal routing, I2C traces, SWD, thermal via breakout planes for D2PAK CoolMOS and SuperSO8 power FETs."],
        ["Total", "Finished Board Thickness", "—", "1.60 mm ± 10%", "FR4 High-Tg", "Standard IPC Class 2 multilayer fabrication."],
    ]
    builder.add_table("Table 15.1: PCB Layer Stack-up Specifications", stack_headers, stack_rows, [0.8, 1.5, 0.9, 1.0, 0.9, 1.9])

    builder.add_p(
        "Controlled Impedance: Digital traces on Layer 4 referenced to Layer 2 ground plane achieve single-ended characteristic "
        "impedance of Z_0 = 50.0 Ω ± 10% (w = 0.35 mm, h = 0.20 mm, epsilon_r = 4.4)."
    )

    builder.add_h2("13.4 Pre-Layout SI Analysis")
    builder.add_bullet(
        "Switching Node di/dt & dv/dt Analysis: Primary Flyback Drain Node (Q1 drain): Slew rate dv/dt ≈ 15.0 V/ns with peak voltage 599 V. "
        "The RCD snubber diode D_snub (STTH110A) and damping resistors (3x 68 kΩ) absorb transformer leakage energy and damp parasitic ringing to < 10% overshoot. "
        "Buck-Boost Switch Nodes (SW1, SW2): Slew rate dv/dt ≈ 3.5 V/ns with peak voltage 28 V. Series gate resistors R_g = 4.7 Ω ± 1% placed directly adjacent "
        "to the gate pins of QA..QD control switching transition times to approximately 12 ns, preventing gate ringing and false shoot-through."
    )
    builder.add_bullet(
        "I2C Bus Signal Integrity: Series damping resistors R_s = 22.0 Ω placed at MCU pins PB8/PB9 suppress transmission line reflections "
        "on long display cables. With C_bus = 35 pF and R_p = 2.2 kΩ, rise edges exhibit smooth monotonic charging with zero undershoot ringing."
    )

    builder.add_h2("13.5 PCB Floor Plan Analysis & Isolation Slot")
    builder.add_p(
        "The physical PCBA measures 160.0 mm × 100.0 mm, partitioned cleanly into distinct operational zones from left to right:"
    )
    builder.add_bullet(
        "Left Zone (Primary Hot Domain, 65 mm × 100 mm): AC inlet socket J1, fuse F1, NTC, MOV, two-stage EMI filter, bridge rectifier BR1, "
        "bulk capacitor C_BULK1, Flyback transformer TX1, CoolMOS Q1, and snubber network."
    )
    builder.add_bullet(
        "Central Safety Isolation Barrier (10 mm Width): Enforces ≥ 6.4 mm physical surface creepage and ≥ 5.0 mm clearance through air. "
        "A 2.0 mm wide milled PCB air slot is routed completely through the FR4 substrate directly beneath: "
        "1. Transformer TX1 (separating primary pin bobbins 1-4 from secondary pin bobbins 5-8); "
        "2. Optocoupler OPTO1 (separating primary pins 1-2 from secondary pins 3-4); "
        "3. Isolated voltage sensor AMC1311 (separating high-side pins 1-4 from low-side pins 5-8)."
    )
    builder.add_bullet(
        "Right Zone (Secondary SELV Touch-Safe Domain, 85 mm × 100 mm): Schottky rectifier D_SEC with clip heatsink, +24 V filter capacitors, "
        "LM5176 Buck-Boost controller, four SuperSO8 FETs, 10 µH flat-wire inductor, output filter bank, 10 mΩ shunt, STM32G474 MCU, OLED display, "
        "rotary encoders, and Pomona 4 mm output binding posts."
    )
    builder.add_bullet(
        "High-Current Switching Loop Area Minimization:\n"
        "   - Flyback Primary Loop (C_BULK1 → TX1 Primary → Q1 Drain/Source → R_CS → GND): Polygon area constrained to < 3.8 cm^2.\n"
        "   - Buck-Boost Input Commutation Loop (C_IN → QA → QB → GND): Area constrained to < 1.2 cm^2.\n"
        "   - Buck-Boost Output Commutation Loop (C_OUT → QC → QD → GND): Area constrained to < 1.2 cm^2."
    )

    builder.add_h2("13.6 Thermal Analysis")
    builder.add_p(
        "Thermal dissipation and junction temperature rise are evaluated under maximum continuous full load (60.0 W DC output) "
        "under worst-case industrial ambient temperature (T_amb = 50.0°C) with pure natural convection cooling (zero fans):"
    )

    therm_headers = ["Critical Component", "Package", "Power Loss (W)", "Thermal Resistance", "Max Junction Temp (T_j)", "Absolute Max Rating", "Derating Margin Compliance"]
    therm_rows = [
        ["CoolMOS Switch Q1", "D2PAK (TO-263)", "0.85 W", "R_th,ja = 59.3°C/W (with 2oz copper)", "T_j = 50 + (0.85 × 59.3) = 100.4°C", "150.0°C", "PASS (66.9% ≤ 75% derating limit)"],
        ["Schottky Diode D_SEC", "TO-220-2", "1.80 W", "R_th,ja = 1.5 + 15.0 = 16.5°C/W (w/ heatsink)", "T_j = 50 + (1.80 × 16.5) = 79.7°C", "150.0°C", "PASS (53.1% ≤ 75% derating limit)"],
        ["Buck-Boost FETs QA..QD", "SuperSO8", "0.105 W / FET", "R_th,ja = 35.0°C/W (w/ 2oz vias)", "T_j = 50 + (0.105 × 35.0) = 53.7°C", "150.0°C", "PASS (35.8% ≤ 75% derating limit)"],
        ["Transformer TX1 Core", "PQ26/20 3C95", "1.85 W", "R_th,ca ≈ 18.0°C/W", "T_hotspot = 50 + (1.85 × 18.0) = 83.3°C", "130.0°C", "PASS (64.1% of core rating)"],
        ["Power Inductor L1", "SMD 12.5 mm", "0.15 W", "R_th,ja ≈ 28.0°C/W", "T_hotspot = 50 + (0.15 × 28.0) = 54.2°C", "125.0°C", "PASS (43.4% of rating)"],
        ["Bridge Rectifier BR1", "GBU-4", "1.62 W", "R_th,ja ≈ 22.0°C/W", "T_j = 50 + (1.62 × 22.0) = 85.6°C", "150.0°C", "PASS (57.1% ≤ 75% derating limit)"],
    ]
    builder.add_table("Table 15.2: Thermal Stress and Junction Temperature Compliance Table", therm_headers, therm_rows, [1.3, 1.0, 0.8, 1.3, 1.4, 0.8, 0.9])

    builder.add_p(
        "All semiconductor silicon junction temperatures remain strictly below 105.0°C, satisfying VVDN Corporate Reliability Rules "
        "(T_j,max ≤ 110.0°C) under maximum 50.0°C ambient."
    )
