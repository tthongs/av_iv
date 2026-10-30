"""
Hardware Design Document - Part 2: Chapters 5 to 8
5. Digital Interface Design
6. RF Design
7. Analog Design
8. Power Design
"""

def add_part2(builder):
    # =========================================================================
    # Chapter 5: Digital Interface Design
    # =========================================================================
    builder.add_h1("5. Digital Interface Design")
    builder.add_h2("5.1 Subsystem1 [Main Board]")
    builder.add_h3("5.1.1 Module1: STM32G474RET6 Microcontroller")
    builder.add_p(
        "The STMicroelectronics STM32G474RET6 mixed-signal microcontroller serves as the supervisory intelligence of the SPPS board. "
        "It coordinates the user interface, executes the 10.0 Hz telemetry loop, computes real-time conversion efficiency, commands "
        "the 12-bit DAC steering network, and provides supervisor-level fault protection."
    )

    builder.add_h4("Boot Strapping")
    builder.add_p(
        "The STM32G474RET6 boot configuration is determined by the logic state of the BOOT0 pin and internal Flash option bytes. "
        "To ensure deterministic startup in electrically noisy switching environments, BOOT0 is tied to ground through a dedicated "
        "10 kΩ pull-down resistor:"
    )

    boot_headers = ["BOOT0 Pin State", "nBOOT1 Option Bit", "Boot Mode Selected", "Target Memory Space", "Engineering Implementation / Selection"]
    boot_rows = [
        ["0 (GND)", "X", "Main Flash Memory", "Bank 1 (0x0800 0000)", "DEFAULT HARDWARE BASELINE: 10 kΩ pull-down to GND. Deterministically boots primary application firmware."],
        ["1 (VDD)", "1", "System Memory", "System ROM (0x1FFF 0000)", "Factory bootloader mode (DFU via USART1). Accessible via 3-pin configuration header JP3."],
        ["1 (VDD)", "0", "Embedded SRAM", "SRAM1 (0x2000 0000)", "Debug SRAM execution. Reserved for factory diagnostics; not used in production."],
    ]
    builder.add_table("Table 4: Boot Strapping Pin Table", boot_headers, boot_rows, [1.0, 1.0, 1.3, 1.4, 2.3])

    builder.add_h4("Memory Interface")
    builder.add_p("The STM32G474RET6 integrates high-speed internal memories with zero wait-state read capability via the ST ART Accelerator:")
    builder.add_bullet("Flash Memory: 512 kB organized as dual banks of 256 kB each (2 kB page size, 10,000 write/erase endurance cycles, > 20 years data retention at 85°C). Bank 1 hosts the core application firmware (< 120 kB footprint). The upper 16 kB sector of Bank 2 is reserved for EEPROM emulation to persist user setpoints, voltage calibration offsets, and fault history logs.")
    builder.add_bullet("Embedded SRAM: 128 kB total internal SRAM partitioned into 80 kB SRAM1, 16 kB SRAM2, and 32 kB CCM (Core Coupled Memory) data RAM with hardware parity check. Critical ADC sampling ISRs and mathematical routines execute out of CCM RAM with zero bus arbitration latency.")

    mem_headers = ["Memory Block", "Base Address", "End Address", "Size", "Wait States @ 170 MHz", "Functional Allocation"]
    mem_rows = [
        ["Flash Bank 1", "0x0800 0000", "0x0803 FFFF", "256 kB", "4 WS (0 WS w/ ART)", "Core supervisory firmware, RTOS kernel, interrupt vectors."],
        ["Flash Bank 2", "0x0804 0000", "0x0807 BFFF", "240 kB", "4 WS (0 WS w/ ART)", "Dual-bank live firmware update image."],
        ["EEPROM Emulation", "0x0807 C000", "0x0807 FFFF", "16 kB", "4 WS", "Persistent calibration offsets, runtime setpoints, fault history logs."],
        ["CCM Data RAM", "0x1000 0000", "0x1000 7FFF", "32 kB", "0 WS (Direct Core)", "High-speed ADC circular buffers, DMA ISR scratchpad, math engine."],
        ["SRAM1", "0x2000 0000", "0x2001 3FFF", "80 kB", "0 WS", "General application heap, OLED frame buffer (1024 B), RTOS stacks."],
        ["SRAM2", "0x2001 4000", "0x2001 7FFF", "16 kB", "0 WS", "Peripheral DMA communication buffers (I2C, USART)."],
    ]
    builder.add_table("Table 5: Microcontroller Internal Memory Map", mem_headers, mem_rows, [1.3, 1.0, 1.0, 0.8, 1.1, 1.8])

    builder.add_h4("Programming Interface")
    builder.add_p(
        "The PCBA provides an onboard 4-pin shrouded 2.54 mm Serial Wire Debug (SWD) header (J4) for production firmware flashing "
        "and real-time in-circuit emulation:"
    )
    builder.add_bullet("Pin 1: +3.3V_VDD (Target reference supply)")
    builder.add_bullet("Pin 2: SWDIO (PA13, internal pull-up)")
    builder.add_bullet("Pin 3: SWCLK (PA14, internal pull-down, external 100 kΩ pull-down to GND)")
    builder.add_bullet("Pin 4: GND (Secondary touch-safe SELV ground)")
    builder.add_bullet("The active-low reset signal (NRST) is supervised by an external RC filter (10 kΩ pull-up to +3.3 V, 100 nF ceramic capacitor to ground).")

    builder.add_h4("Peripheral Interface")
    builder.add_p("The microcontroller interfaces with on-board telemetry and display peripherals via the following digital buses:")
    builder.add_bullet(
        "I2C1 Bus Interface (Fast-Mode 400 kHz): Connects STM32 PB8 (I2C1_SCL) and PB9 (I2C1_SDA) to the INA226AIDGSR secondary power monitor "
        "(7-bit address 0x40) and the 1.3-inch OLED display controller SSD1306 (7-bit address 0x3C). Total bus capacitance is estimated at "
        "C_bus ≈ 35 pF (PCB trace capacitance ≈ 15 pF, pin input capacitance ≈ 20 pF). Pull-up resistors R_p = 2.2 kΩ ± 1% (R_PU1, R_PU2) "
        "are tied to +3.3 V. Bus rise time: t_r = 0.8473 × R_p × C_bus = 0.8473 × 2200 Ω × 35 × 10^-12 F = 65.2 ns, well within the I2C "
        "Fast-Mode maximum limit (t_r,max = 300 ns). High-level noise margin exceeds 0.825 V (V_IH,min = 2.31 V)."
    )
    builder.add_bullet(
        "USART1 Serial Telemetry Interface: Pins PA9 (USART1_TX) and PA10 (USART1_RX) route to a dedicated 3-pin 2.54 mm header (J5) "
        "operating at 115,200 baud, 8 data bits, no parity, 1 stop bit (8N1). Emits an ASCII telemetry string once every 100 ms (10.0 Hz) "
        "containing V_AC, I_AC, P_AC, V_OUT, I_OUT, P_DC, and efficiency η."
    )

    builder.add_h4("GPIO Interface")
    builder.add_bullet(
        "LM5176 Supervisory Enable: STM32 pin PB0 drives the base of an NPN transistor (MMBT3904) through a 4.7 kΩ series resistor. "
        "When PB0 is driven HIGH, the NPN pulls the LM5176 ENABLE pin (Pin 6) below 0.2 V within 500 ns, instantly inhibiting gate drive pulses."
    )
    builder.add_bullet(
        "Rotary Encoders: Pins PA0/PA1 (Encoder 1) and PA6/PA7 (Encoder 2) connect to external Bourns mechanical encoders with onboard "
        "10 kΩ pull-ups and 10 nF ceramic RC low-pass debouncing filters (τ = 100 µs), feeding hardware timer quadrature decoder inputs (TIM2 and TIM3)."
    )
    builder.add_bullet(
        "Front-Panel Status LEDs: Pins PC6 (Green - CV Mode), PC7 (Amber - CC Clamped Mode), and PC8 (Red - Fault / Trip) drive low-current "
        "SMD LEDs through 1.0 kΩ current-limiting resistors (I_LED ≈ 1.5 mA)."
    )

    # =========================================================================
    # Chapter 6: RF Design
    # =========================================================================
    builder.add_h1("6. RF Design")
    builder.add_h2("6.1 Subsystem1 [Main Board]")
    builder.add_callout(
        "Engineering Status: NOT APPLICABLE (Out of Scope per PRD Rev A1_001 Section 10). "
        "The Smart Programmable Power Supply (VVDN_SPPS_2026) is a wired benchtop and ATE power supply. Wireless radios (Wi-Fi, Bluetooth, "
        "BLE, Zigbee, Cellular, LoRa) are intentionally excluded from the architecture.",
        "NOTE"
    )
    builder.add_p(
        "Although intentional RF transmitters are excluded, unintentional radiated RF emissions generated by high dv/dt and di/dt switching cells "
        "(65.0 kHz Flyback primary switch and 300.0 kHz Buck-Boost H-bridge) are rigorously controlled to comply with CISPR 32 / EN 55032 "
        "Class B commercial radiated emission limits through the following layout rules:"
    )
    builder.add_bullet("Four-Layer Balanced Stackup: Layer 2 serves as a continuous, low-impedance ground plane directly beneath all high-current power switching loops on Layer 1, providing mirror image return paths that cancel radiated magnetic dipole loops.")
    builder.add_bullet("Switching Loop Area Minimization: The high-frequency commutation loop areas for the Flyback primary (C_BULK1 → TX1 → Q1 → GND) and Buck-Boost bridge (C_IN → QA → QB → GND and C_OUT → QC → QD → GND) are physically constrained to < 1.5 cm^2.")
    builder.add_bullet("Magnetic Field Shielding: Wurth Elektronik 7443321000 flat-wire power inductor features a fully closed magnetic shielding structure with negligible leakage flux. The PQ26/20 transformer core uses an outer copper foil flux band tied to primary quiet ground.")
    builder.add_bullet("Snubber Damping: Primary RCD clamp (STTH110A + 22.67 kΩ / 3 W + 6.6 nF) suppresses drain ringing to < 10% overshoot. Buck-Boost gate drive resistors (4.7 Ω) control MOSFET turn-on switching edges to approximately 12 ns.")

    # =========================================================================
    # Chapter 7: Analog Design
    # =========================================================================
    builder.add_h1("7. Analog Design")
    builder.add_h2("7.1 Subsystem1 [Main Board]")

    builder.add_h3("7.1.1 Module1: 12-Bit DAC Precision Voltage Steering Network")
    builder.add_p(
        "The LM5176 regulates output voltage by modulating its 4-switch H-bridge to maintain its feedback pin (FB, Pin 24) at an internal "
        "bandgap reference voltage of V_REF = 1.200 V DC. Rather than altering the internal reference, an active resistive summing junction "
        "is implemented at the FB node. The STM32G474 internal 12-bit DAC channel (DAC1_OUT1, Pin PA4) injects or extracts current into the "
        "summing junction through resistor R_DAC, steering the regulated output voltage V_OUT smoothly from 5.0 V to 20.0 V DC:"
    )

    builder.add_p("Resistive Summing Topology Schematic:")
    builder.add_p(
        "                  V_OUT\n"
        "                    │\n"
        "                  ┌─┴─┐\n"
        "                  │R_top│  (49.9 kΩ, 0.1%)\n"
        "                  └─┬─┘\n"
        "                    │\n"
        "                    ├─── FB Node (LM5176 Pin 24, V_REF = 1.200 V)\n"
        "                    │\n"
        "         ┌──────────┼──────────┐\n"
        "         │          │          │\n"
        "       ┌─┴─┐      ┌─┴─┐      ┌─┴─┐\n"
        "       │R_bot│    │R_DAC│    │C_ff│  (15 pF Feedforward)\n"
        "       └─┬─┘      └─┬─┘      └─┬─┘\n"
        "         │          │          │\n"
        "        GND       V_DAC       GND\n"
        "               (0 V - 3.3 V)\n"
    )

    builder.add_h4("Governing Nodal Equations")
    builder.add_p("Applying Kirchhoff's Current Law (KCL) at the LM5176 FB summing junction:")
    builder.add_p("(V_OUT - V_REF) / R_top = (V_REF / R_bot) + (V_REF - V_DAC) / R_DAC")
    builder.add_p("Solving explicitly for the output voltage V_OUT:")
    builder.add_p("V_OUT = V_REF × [ 1 + (R_top / R_bot) + (R_top / R_DAC) ] - V_DAC × (R_top / R_DAC)")

    builder.add_h4("Component Sizing and Parameter Table")
    dac_headers = ["Parameter / Component", "Reference Designator", "Nominal Value", "Tolerance", "Tempco (TCR)", "Manufacturer & MPN"]
    dac_rows = [
        ["Top Divider Resistor", "R_top", "49.9 kΩ", "± 0.1%", "< 25 ppm/°C", "Vishay Dale TNPW080549K9BEEA"],
        ["Bottom Ground Resistor", "R_bot", "4.48 kΩ", "± 0.1%", "< 25 ppm/°C", "Vishay Dale TNPW08054K48BEEA"],
        ["DAC Injection Resistor", "R_DAC", "11.0 kΩ", "± 0.1%", "< 25 ppm/°C", "Vishay Dale TNPW080511K0BEEA"],
        ["Feedforward Capacitor", "C_ff", "15.0 pF", "± 5%", "C0G / NP0", "Murata GRM1885C1H150JA01D"],
        ["LM5176 Internal V_REF", "U3 (Pin 24)", "1.200 V DC", "± 1.0%", "Internal Bandgap", "Texas Instruments LM5176PWPR"],
        ["DAC Steering Span", "U5 (PA4)", "0.0 V - 3.30 V", "12-bit (4096 steps)", "Internal STM32", "STMicroelectronics STM32G474RET6"],
    ]
    builder.add_table("Table 6: Voltage Steering Resistor Sizing and Precision Parameters", dac_headers, dac_rows, [1.5, 0.9, 1.0, 0.8, 1.1, 1.7])

    builder.add_h4("Mathematical Verification Across Operating Envelope")
    builder.add_p("1. Maximum Voltage Setpoint (V_OUT = 20.0 V): Commanded DAC output V_DAC = 0.000 V:")
    builder.add_p("   V_OUT = 1.200 × [ 1 + (49.9 / 4.48) + (49.9 / 11.0) ] - 0.000")
    builder.add_p("   V_OUT = 1.200 × [ 1 + 11.1384 + 4.5364 ] = 1.200 × 16.6748 = 20.01 V DC")
    builder.add_p("2. Mid-Scale Setpoint (V_OUT = 12.5 V): Commanded DAC output V_DAC = 1.650 V:")
    builder.add_p("   V_OUT = 20.01 - 1.650 × (49.9 / 11.0) = 20.01 - 1.650 × 4.5364 = 20.01 - 7.485 = 12.525 V DC")
    builder.add_p("3. Minimum Voltage Setpoint (V_OUT = 5.0 V): Commanded DAC output V_DAC = 3.300 V:")
    builder.add_p("   V_OUT = 20.01 - 3.300 × (4.5364) = 20.01 - 14.970 = 5.04 V DC")

    builder.add_h4("Monotonic Digital Resolution")
    builder.add_p(
        "The STM32G474 12-bit DAC features 2^12 = 4096 quantization codes spanning 0.0 V to +3.30 V (V_LSB = 3.30 V / 4096 = 805.7 µV). "
        "The resulting output voltage tuning resolution is:"
    )
    builder.add_p("Δ V_OUT,step = V_LSB × (R_top / R_DAC) = (805.7 µV) × (49.9 kΩ / 11.0 kΩ) = 3.655 mV per step")
    builder.add_p("This guarantees smooth, monotonic voltage tuning that exceeds the PRD requirement (≤ 10.0 mV step resolution) by nearly 3x.")

    builder.add_h3("7.1.2 Module2: Sub-5µs Fast Hardware Current Limit Clamping")
    builder.add_p(
        "To protect the BSC034N04LS switching MOSFETs from destructive avalanche breakdown during sudden dead short circuits, "
        "an autonomous analog hardware current clamp is implemented directly on the PCBA, operating completely independent of firmware:"
    )
    builder.add_bullet("Precision Metal Current Sense Shunt (R_shunt): Bourns CSS2H-2512R-L010F (10.0 mΩ ± 0.1%, 3.0 W, 2512 package, TCR < 50 ppm/°C). Senses total load current directly in the negative return path.")
    builder.add_bullet(
        "Current Sense Amplifier (U7): Texas Instruments INA240A2EDCKR (enhanced PWM common-mode rejection, fixed gain Av = 50.0 V/V, bandwidth 400 kHz):\n"
        "   V_CS,out = I_OUT × R_shunt × Av = I_OUT × (0.010 Ω) × 50.0 = I_OUT × 0.500 V/A\n"
        "   - At I_OUT = 3.0 A (Full Load): V_CS,out = 1.500 V.\n"
        "   - At I_OUT = 3.20 A (Hardware Trip Setpoint): V_CS,out = 1.600 V."
    )
    builder.add_bullet("High-Speed Analog Comparator (U8): Texas Instruments TLV3501AIDBVR (push-pull rail-to-rail output, propagation delay t_pd = 4.5 ns). The inverting input is biased to 1.600 V via a precision divider from +3.3 V.")
    builder.add_bullet("COMP Pin Pull-Down Transistor: Diodes Inc. MMBT3904 NPN transistor connected from LM5176 COMP (Pin 25) to quiet analog ground.")
    builder.add_bullet(
        "Total Autonomous Clamping Latency Breakdown:\n"
        "   - Current trip threshold exceeded (I_OUT > 3.2 A): t = 0\n"
        "   - INA240 amplifier output slew to 1.60 V (400 kHz BW): 1.20 µs\n"
        "   - TLV3501 comparator trip and transition: 4.5 ns\n"
        "   - MMBT3904 base turn-on and collector saturation: 250 ns\n"
        "   - LM5176 internal error amplifier compensation discharge, duty cycle truncation: 800 ns\n"
        "   - Total Response Time: 2.25 µs << 5.0 µs (Guaranteed safe envelope!)."
    )

    builder.add_h3("7.1.3 Module3: Primary Isolated AC Voltage & Current Telemetry")
    builder.add_p("To measure primary AC power (P_AC) while maintaining certified 3000 V RMS reinforced galvanic isolation:")
    builder.add_bullet(
        "Isolated Primary Voltage Sensing (U4): Texas Instruments AMC1311BDWVR (SOIC-8 Wide, 5.85 mm creepage, 7000 V peak reinforced isolation, "
        "differential 2.0 V input range). A high-voltage divider (1.5 MΩ string of three 500 kΩ 1206 resistors in series, and a 7.5 kΩ bottom resistor) "
        "scales full-scale 375 V peak down to 1.86 V, feeding the AMC1311 input. The isolated differential output is low-pass filtered and sampled by STM32 ADC channels."
    )
    builder.add_bullet(
        "Primary Current Sensing (CT1): Talema AC1010 encapsulated current transformer (1000:1 turns ratio, 10.0 A RMS rating, 4000 V RMS isolation). "
        "Senses AC mains Live current. Secondary current (I_sec = I_pri / 1000 = 1.60 mA at 1.60 A RMS) flows through a precision 100.0 Ω ± 0.1% "
        "thin-film burden resistor (R_burden, Vishay Dale TNPW0805100R), generating an AC signal of 160.0 mV RMS biased at +1.65 V DC midpoint, "
        "sampled by the STM32 ADC."
    )

    builder.add_h3("7.1.4 Module4: Secondary DC Power Telemetry")
    builder.add_bullet("Texas Instruments INA226AIDGSR (16-bit I2C power monitor, VSSOP-10) is placed on the secondary side to sample load telemetry.")
    builder.add_bullet("Connected differentially across the 10.0 mΩ Bourns shunt resistor R_shunt.")
    builder.add_bullet("Shunt voltage LSB: 2.5 µV, yielding current measurement resolution of 250 µA (0.25 mA).")
    builder.add_bullet("Bus voltage LSB: 1.25 mV, full-scale measurement range 36.0 V.")
    builder.add_bullet("Programmed via I2C for 16-sample averaging (1.1 ms conversion time per channel). Emits calibrated voltage, current, and computed DC load power (P_DC) at 10.0 Hz rate.")

    # =========================================================================
    # Chapter 8: Power Design
    # =========================================================================
    builder.add_h1("8. Power Design")
    builder.add_h2("8.1 Subsystem1 Power Architecture")
    builder.add_p("The SPPS power architecture comprises a four-stage conversion topology feeding secondary post-regulation and auxiliary housekeeping rails:")

    builder.add_p(
        "Universal AC Mains (85 V - 265 V AC RMS)\n"
        "       │\n"
        "       ▼\n"
        "[Stage 1: Input Protection & EMI Filter]  (Fuse 2A, NTC 15Ω, MOV 300V, 2-Stage CM Choke)\n"
        "       │\n"
        "       ▼\n"
        "[Stage 2: Rectification & Bulk Link]      (GBU606 Bridge + 100 µF / 450 V Bulk Electrolytic)\n"
        "       │\n"
        "       ├─── High-Voltage DC Link (+120 V to +375 V DC)\n"
        "       ▼\n"
        "[Stage 3: Galvanically Isolated Flyback]   (PQ26/20 Core, IPB80R290P7 CoolMOS, MBR10100 Diode)\n"
        "       │\n"
        "       ├─── Intermediate Bus (+24.0 V DC ± 1.0%, 72 W Continuous / 84 W Peak)\n"
        "       │\n"
        "       ├──► [L78L12 Linear Regulator]  ──► +12.0 V DC (LM5176 Gate Drive Bias)\n"
        "       ├──► [L78L05 Linear Regulator]  ──► +5.0 V DC  (OLED Display & Sensors)\n"
        "       │           │\n"
        "       │           └──► [AP2114 LDO]   ──► +3.30 V DC (STM32 MCU, ADC Ref, INA226)\n"
        "       │\n"
        "       ▼\n"
        "[Stage 4: Synchronous Buck-Boost]         (LM5176 Controller + 4x BSC034N04LS Power MOSFETs)\n"
        "       │\n"
        "       ▼\n"
        "Regulated DC Output Terminals (5.0 V - 20.0 V DC @ 3.0 A Continuous, 60 W Max)\n"
    )

    builder.add_h3("8.1.1 Power Sequencing")
    builder.add_h4("Power Up Sequence")
    builder.add_p(
        "To prevent inductive inrush stress, output overshoot, and MCU race conditions, the hardware enforces a deterministic "
        "5-phase startup sequence:"
    )

    seq_headers = ["Time (ms)", "Operational State / Event", "Circuit Behavior & Hardware Control", "Output Voltage State"]
    seq_rows = [
        ["0.0 ms", "AC Mains Applied", "85 V - 265 V AC RMS energizes circuit. 15 Ω NTC limits inrush charging current to < 25 A peak. Bridge rectifier charges bulk capacitor.", "0.0 V"],
        ["15.0 ms", "Bulk DC Bus Stabilized", "Bulk DC rail reaches > 120 V DC. High-voltage trickle resistor charges Flyback controller VCC capacitor to startup threshold (14.5 V).", "0.0 V"],
        ["25.0 ms", "Flyback Stage Starts", "Controller initiates 65 kHz PWM. Auxiliary winding takes over controller bias. Secondary Schottky rectifies pulses.", "+24.0 V ramp begins"],
        ["40.0 ms", "+24.0 V Rail Stabilized", "+24.0 V ± 1.0% intermediate bus stabilizes. Housekeeping regulators power up: +12 V gate bias, +5 V display, +3.3 V MCU rail.", "+24.0 V stable"],
        ["50.0 ms", "MCU Boot & Init", "STM32 POR releases at +3.3 V. DAC output set to +3.30 V (defaulting output command to safe minimum 5.0 V). LM5176 ENABLE held LOW by NPN clamp. OLED initializes.", "0.0 V (Output Disabled)"],
        ["70.0 ms", "System Standby Ready", "Idle power < 150 mW. System awaits user enable command.", "0.0 V (Standby)"],
        ["User Run", "Output Enable Toggle", "MCU releases ENABLE clamp. LM5176 executes internal 5 ms soft-start ramp to commanded setpoint (5.0 V to 20.0 V) with zero overshoot (< 1.0%).", "Commanded setpoint reached"],
    ]
    builder.add_table("Table 7: Power Sequencing", seq_headers, seq_rows, [1.0, 1.5, 3.2, 1.3])

    builder.add_h4("Power Down Sequence")
    builder.add_bullet(
        "User Commanded Output Disable: STM32 drives pin PB0 HIGH, turning on NPN clamp to ground LM5176 ENABLE. "
        "Buck-boost gate drivers immediately turn OFF all four MOSFETs. Active output bleeder resistor discharges output filter capacitors "
        "to < 0.8 V within 250 ms."
    )
    builder.add_bullet(
        "AC Mains Grid Dropout: AMC1311 detects AC input line falling below 70 V RMS. Bulk capacitor sustains continuous operation for "
        "> 50 ms (at 230 V AC). MCU captures current setpoint and calibration data to Flash EEPROM emulation sector within 2.0 ms. "
        "As bulk rail collapses below Flyback UVLO, PWM switching stops. Safety bleeder resistors (300 kΩ) safely discharge bulk electrolytic "
        "capacitor from 375 V to < 50 V within 44.8 seconds."
    )

    builder.add_h3("8.1.2 Power Consumption")
    builder.add_p("The table below details current consumption across all operational voltage rails in Standby and Full Load states:")

    pwr_headers = ["Rail Name", "Nominal Voltage", "Standby Current", "5V / 3A Load (15W)", "12V / 3A Load (36W)", "20V / 3A Load (60W)", "Subsystem Loads Served"]
    pwr_rows = [
        ["High-Voltage Bulk", "+325 V DC", "0.85 mA", "58.2 mA", "134.1 mA", "215.8 mA", "Primary Flyback switching stage, snubber, primary bleeders."],
        ["+24.0V Inter Rail", "+24.0 V DC", "12.0 mA", "685 mA", "1580 mA", "2605 mA", "LM5176 power stage, +12 V gate bias, +5 V display rail."],
        ["+12.0V Gate Bias", "+12.0 V DC", "2.5 mA", "18.5 mA", "18.5 mA", "18.5 mA", "LM5176 VCC supply, internal MOSFET gate charge drive circuits."],
        ["+5.0V OLED Rail", "+5.0 V DC", "1.2 mA", "15.0 mA", "15.0 mA", "15.0 mA", "1.3-inch OLED display controller, display logic, AP2114 LDO."],
        ["+3.3V Logic Rail", "+3.30 V DC", "22.0 mA", "38.5 mA", "38.5 mA", "38.5 mA", "STM32G474 MCU (170 MHz), INA226 monitor, DAC reference, LEDs."],
        ["Net Input Power", "230 V AC", "< 120 mW", "18.4 W", "42.8 W", "70.14 W", "Total System Grid Power Consumption"],
    ]
    builder.add_table("Table 8: Subsystem1 – Power Consumption", pwr_headers, pwr_rows, [1.1, 1.0, 0.9, 1.0, 1.0, 1.0, 1.0])

    builder.add_h3("8.1.3 Power Dissipation & Thermal Losses")
    builder.add_p(
        "The table below documents the stage-by-stage power loss analysis under maximum continuous full load "
        "(20.0 V / 3.0 A = 60.0 W DC output at 230 V AC RMS):"
    )

    diss_headers = ["Circuit Stage / Component", "Component Ref Des", "Calculated Loss (W)", "Primary Loss Mechanism", "Thermal Mitigation / Heat Sinking"]
    diss_rows = [
        ["Mains Input & EMI Filter", "F1, NTC1, L_CM1/2", "0.38 W", "I^2 R copper winding resistance and fuse element loss.", "Natural convection, through-hole thermal conduction."],
        ["Bridge Rectifier", "BR1 (GBU606)", "1.62 W", "Conduction loss: 2 × V_F × I_avg = 2 × 0.95 V × 0.85 A.", "Through-hole leads to 2oz copper polygon pour."],
        ["High-Voltage Bulk Cap", "C_BULK1 (100µF/450V)", "0.15 W", "I_RMS^2 × ESR = (0.95 A)^2 × 0.165 Ω.", "Large aluminum snap-in can, 105°C rated."],
        ["Primary CoolMOS Switch", "Q1 (IPB80R290P7)", "0.85 W", "Conduction loss (0.59 W) + switching capacitive loss (0.26 W).", "D2PAK tab soldered to 2oz copper plane (400 mm^2)."],
        ["Primary RCD Snubber", "R_snub1..3", "2.40 W", "Dissipation of leakage inductance energy (E_lk = 20.2 µJ).", "Three 2512 SMD resistors in parallel (3.0 W total rating)."],
        ["Flyback Transformer", "TX1 (PQ26/20 3C95)", "1.85 W", "Core hysteresis/eddy loss (0.95 W) + copper loss (0.90 W).", "Ferrite core natural convection (R_th ≈ 18°C/W)."],
        ["Secondary Schottky Diode", "D_SEC (MBR10100G)", "1.80 W", "Conduction forward loss: V_F × I_OUT = 0.60 V × 3.0 A.", "TO-220 mounted on stamped aluminum heatsink (15°C/W)."],
        ["Buck-Boost Power MOSFETs", "QA..QD (BSC034N04LS)", "0.42 W", "Conduction loss (0.08 W) + gate drive & switching (0.34 W).", "SuperSO8 package with thermal vias to bottom copper plane."],
        ["Power Inductor", "L1 (Wurth 7443321000)", "0.15 W", "Copper loss (I^2 × DCR = 9 × 0.0105 Ω) + core loss.", "Flat-wire coil, direct surface thermal dissipation."],
        ["Current Sense Shunt", "R_shunt (Bourns 10mΩ)", "0.09 W", "I^2 R = (3.0 A)^2 × 0.010 Ω = 0.090 W (3.0% of 3W).", "Metal alloy element, negligible heating (< 5°C rise)."],
        ["Auxiliary Regulators & MCU", "U5, U7..U9, DISP1", "0.43 W", "LDO voltage drop and microcontroller dynamic power.", "SOT-89 / SOT-223 PCB copper heatsinking tabs."],
        ["Total System Dissipation", "All Stages Combined", "10.14 W", "Total internal heat generated at 60.0W full DC output", "Full-Load System Efficiency: η = 85.54% @ 230V AC"],
    ]
    builder.add_table("Table 9: Subsystem1 – Power Dissipation", diss_headers, diss_rows, [1.5, 1.2, 0.9, 1.9, 1.5])

    builder.add_h2("8.2 Subsystem2 Power Architecture")
    builder.add_p("The secondary SELV subsystem distributes regulated bias power generated from the +24.0 V DC intermediate rail:")
    builder.add_bullet("+12.0 V DC Gate Drive Bias Rail: Regulated by STMicroelectronics L78L12ACUTR (SOT-89, 100 mA capacity) stepping down +24 V to provide a quiet, stable bias for the LM5176 internal gate charge pumps and gate driver circuitry.")
    builder.add_bullet("+5.0 V DC Display & Sensor Rail: Regulated by STMicroelectronics L78L05ABUTR (SOT-89, 100 mA capacity) powering the 1.3-inch OLED display module logic and input supply of the +3.3 V LDO.")
    builder.add_bullet("+3.30 V DC Ultra-Quiet MCU & Analog Rail: Regulated by Diodes Inc. AP2114H-3.3TRG1 (SOT-223, 1.0 A capacity, low dropout voltage 240 mV, high PSRR of 65 dB @ 1 kHz). Decoupled with a 10 µF X7R ceramic capacitor and individual 100 nF bypass capacitors on every microcontroller VDD/VDDA pin pair.")

    builder.add_h2("8.3 Power Input Protection")
    builder.add_bullet("Overcurrent Protection (F1): Littelfuse 0218002.MXP (2.0 A, 250 V AC, 5 x 20 mm Time-Lag Ceramic Cartridge Fuse). Melting I^2 t = 19.6 A^2 s safely absorbs repetitive capacitive inrush pulses (0.468 A^2 s) while opening safely during short-circuit conditions up to 1500 A interrupting rating.")
    builder.add_bullet("Inrush Current Suppression (NTC1): EPCOS B57236S0150M000 (15.0 Ω cold resistance at 25°C, 2.9 A RMS steady-state current). Clamps maximum cold-start inrush current at 265 V AC RMS (374.8 V peak) to strictly 24.98 A peak even with zero external line impedance, satisfying PRD requirement PR-02 (< 25.0 A peak).")
    builder.add_bullet("Surge Voltage Clamp (MOV1): Bourns MOV-14D471K (14 mm disc, 300 V RMS continuous voltage, clamping voltage 775 V @ 50 A, peak surge current 4500 A for 8/20 µs transient, energy absorption 125 J). Protects against IEC 61000-4-5 Level 3 differential line surges (1.0 kV).")

    builder.add_h2("8.4 System Power Source")
    builder.add_p("The SPPS module operates from commercial single-phase AC utility grids worldwide:")
    builder.add_bullet("Nominal Voltage: 100 V - 240 V AC RMS")
    builder.add_bullet("Operating Voltage Tolerance: Universal 85.0 V to 265.0 V AC RMS continuous")
    builder.add_bullet("Nominal Frequency: 50 Hz / 60 Hz (Operating frequency range: 47 Hz - 63 Hz)")
    builder.add_bullet("Maximum Steady-State Input Current: 1.604 A RMS at 85.0 V AC RMS under full 60.0 W DC load.")
