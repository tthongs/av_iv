#!/usr/bin/env python3
"""
Generate comprehensive hardware component connections block diagram for the
Smart Programmable Power Supply (VVDN_SPPS_2026).
Completely eliminates voltage steering; standardizes on Direct PWM Duty Cycle Voltage Control.
Outputs:
  - Mermaid code (.mmd) into final_prd_staging/mermaid/ and smart_programmable_power_supply/mermaid/
  - Graphviz source (.dot) into final_prd_staging/diagrams/
  - Rendered high-res vector graphics (.svg) and raster images (.png) into final_prd_staging/diagrams/
"""

import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIAG_DIR = os.path.join(BASE_DIR, "diagrams")
MMD_DIR = os.path.join(BASE_DIR, "mermaid")
REPO_MMD_DIR = os.path.join(os.path.dirname(BASE_DIR), "smart_programmable_power_supply", "mermaid")

os.makedirs(DIAG_DIR, exist_ok=True)
os.makedirs(MMD_DIR, exist_ok=True)
os.makedirs(REPO_MMD_DIR, exist_ok=True)

# ==============================================================================
# MERMAID SOURCE: COMPONENT CONNECTIONS BLOCK DIAGRAM (NO VOLTAGE STEERING)
# ==============================================================================

mmd_content = """flowchart TD
    %% Domain Styles
    classDef acStyle fill:#ECEFF1,stroke:#37474F,stroke-width:2px,color:#263238
    classDef priPwr fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#BF360C
    classDef isoBarrier fill:#FFEBEE,stroke:#C62828,stroke-width:2px,stroke-dasharray: 5 5,color:#B71C1C
    classDef secPwr fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20
    classDef bbPwr fill:#E0F7FA,stroke:#00838F,stroke-width:2px,color:#004D40
    classDef fbStyle fill:#EDE7F6,stroke:#512DA8,stroke-width:2px,color:#311B92
    classDef auxStyle fill:#FFF8E1,stroke:#FFA000,stroke-width:2px,color:#FF6F00
    classDef tlmStyle fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px,color:#4A148C
    classDef mcuStyle fill:#E1F5FE,stroke:#0277BD,stroke-width:2px,color:#01579B
    classDef outStyle fill:#E8EAF6,stroke:#283593,stroke-width:2px,color:#1A237E

    subgraph STAGE1 ["STAGE 1: MAINS AC INPUT & EMI FILTERING (HOT DOMAIN)"]
        J1["AC Mains Inlet J1<br/>IEC 320-C14<br/>• Pin L (Line 85-265V)<br/>• Pin N (Neutral)<br/>• Pin PE (Earth)"]:::acStyle
        F1["Fuse F1<br/>2.0A / 250V AC<br/>Time-Lag 5x20mm"]:::acStyle
        NTC1["Inrush NTC1<br/>10Ω Cold, 3.2A<br/>Disc 13mm"]:::acStyle
        MOV1["Surge MOV1<br/>14D471K (300V RMS)<br/>4.5kA Clamp"]:::acStyle
        CX1["X2 Cap CX1<br/>0.22µF / 275V AC<br/>+ Bleeder R_DIS1"]:::acStyle
        L_CM1["CM Choke L_CM1<br/>15.0mH, 1.1A RMS<br/>Toroidal Through-Hole"]:::acStyle
        CY1_2["Y2 Caps CY1/CY2<br/>2x 2.2nF / 300V AC<br/>L/N to Earth PE"]:::acStyle
        CX2["X2 Cap CX2<br/>0.22µF / 275V AC<br/>+ Bleeder R_DIS2"]:::acStyle
        L_CM2["CM Choke L_CM2<br/>4.7mH, 1.6A RMS<br/>High-Freq Choke"]:::acStyle
        CY3_4["Y2 Caps CY3/CY4<br/>2x 2.2nF / 300V AC<br/>L/N to Earth PE"]:::acStyle

        J1 -->|"Line (L)"| F1
        F1 --> NTC1
        J1 -->|"Neutral (N)"| CX1
        NTC1 --> MOV1
        MOV1 --> CX1
        CX1 --> L_CM1
        L_CM1 --> CY1_2
        CY1_2 --> CX2
        CX2 --> L_CM2
        L_CM2 --> CY3_4
    end

    subgraph STAGE2 ["STAGE 2: BRIDGE RECTIFIER & BULK DC BUS (HOT DOMAIN)"]
        BR1["Bridge Rectifier BR1<br/>GBU606 (600V, 6A)<br/>Pins: AC1, AC2, +, -"]:::priPwr
        C_BULK["Bulk Cap C_BULK<br/>100µF / 450V Elect.<br/>+ C_HF 0.1µF Film"]:::priPwr
        R_BLEED["Bleeder Resistor<br/>R_BLEED 330kΩ, 2W<br/>Safety Discharge"]:::priPwr

        CY3_4 -->|"AC1, AC2"| BR1
        BR1 -->|"(+) DC Bus"| C_BULK
        BR1 -->|"(-) GND_PRI"| C_BULK
        C_BULK --- R_BLEED
    end

    subgraph STAGE3_PRIMARY ["STAGE 3: 65 kHz FLYBACK PRIMARY & CONTROLLER (GND_PRI)"]
        TX1_PRI["Flyback Trans TX1 Pri<br/>PQ26/20 (3C95 Ferrite)<br/>Pin 1 (+HVDC) -> Pin 3<br/>Lp=220µH, Np=36T"]:::priPwr
        Q1_FET["Primary MOSFET Q1<br/>STP10NK80Z (800V, 17A)<br/>Pins: Drain, Gate, Source"]:::priPwr
        RCD_CLAMP["RCD Snubber Clamp<br/>• US1M Diode (1000V, 1A)<br/>• C_SNUB 1nF / 1kV<br/>• R_SNUB 22.6kΩ (3x 68k)"]:::priPwr
        R_CS["CS Shunt Resistor R_CS<br/>0.25Ω / 1%, 2W Metal<br/>Pin: ISENSE to GND_PRI"]:::priPwr
        U1_PWM["PWM Controller U1<br/>TI UC3843 / UCC28C43<br/>• Pin 7: VCC (+14V Aux)<br/>• Pin 8: VREF (5.0V)<br/>• Pin 4: RT/CT (65kHz)<br/>• Pin 3: ISENSE (1.0V OCP)<br/>• Pin 6: OUT (Gate Drive)<br/>• Pin 1: COMP / Pin 2: FB<br/>• Pin 5: GND_PRI"]:::priPwr
        TX1_AUX["TX1 Aux Winding<br/>Pins 4, 5 (Naux=5T)<br/>+ UF4004 & 47µF Cap"]:::priPwr

        C_BULK -->|"+HVDC (+120V to +375V)"| TX1_PRI
        TX1_PRI -->|"Pin 3 (Drain)"| Q1_FET
        TX1_PRI -.->|"Snubber Loop"| RCD_CLAMP
        Q1_FET -->|"Pin Source"| R_CS
        R_CS -->|"GND_PRI"| BR1
        U1_PWM -->|"Pin 6 (OUT) via 10Ω"| Q1_FET
        R_CS -->|"Filtered ISENSE"| U1_PWM
        TX1_AUX -->|"VCC Rail (+14V)"| U1_PWM
    end

    subgraph ISOLATION_BARRIER ["⚡ REINFORCED ISOLATION BARRIER (IEC 62368-1 / 3000V RMS / 6.4mm Creepage)"]
        ISO_TX1["TX1 Secondary Winding<br/>Furukawa TEX-E TIW (Ns=6T)<br/>3000V RMS Dielectric Barrier"]:::isoBarrier
        ISO_OPTO["Optocoupler OPTO1<br/>PC817 (5000V RMS)<br/>Voltage Loop Feedback"]:::isoBarrier
        ISO_AMC["Isolated Modulator U5<br/>TI AMC1311 (5000V RMS)<br/>VINP/N (Pri) to VOUTP/N (Sec)"]:::isoBarrier
        ISO_CT1["Current Transformer CT1<br/>Talema AC1005 (1000:1)<br/>Isolated AC Line Current"]:::isoBarrier
        ISO_DC_DC["Isolated DC-DC U9<br/>Mornsun B0505S-1WR3<br/>+5V System -> +5V_ISO (Pri)"]:::isoBarrier
    end

    subgraph STAGE3_SECONDARY ["STAGE 3: SCHOTTKY RECTIFICATION & +24V BUS (SELV DOMAIN)"]
        D_SEC["Schottky Diode D_SEC<br/>ON Semi MBR10100 (100V, 10A)<br/>Pins: Anode -> Cathode<br/>TO-220 with Stamped Heatsink"]:::secPwr
        C_SEC["Secondary LC Filter<br/>• C_SEC1: 470µF / 35V Low-ESR<br/>• L_SEC: 2.2µH Choke<br/>• C_SEC2: 22µF Ceramic MLCC"]:::secPwr
        BUS_24V["Intermediate Rail<br/>+24.0V DC Bus (72W)<br/>Ripple < 40mV pk-pk"]:::secPwr
        U2_TL431["Shunt Regulator U2<br/>TI TL431 (2.495V Ref)<br/>+ Divider 21.5kΩ / 2.49kΩ"]:::secPwr

        TX1_PRI -.->|"Magnetic Coupling"| ISO_TX1
        ISO_TX1 -->|"Pin 7 (Anode)"| D_SEC
        ISO_TX1 -->|"Pin 9 (GND_SEC)"| C_SEC
        D_SEC -->|"Cathode"| C_SEC
        C_SEC --> BUS_24V
        BUS_24V -->|"Feedback Divider"| U2_TL431
        U2_TL431 -->|"Drives Photodiode"| ISO_OPTO
        ISO_OPTO -->|"Phototransistor"| U1_PWM
    end

    subgraph STAGE4_BUCK_BOOST ["STAGE 4: 4-SWITCH SYNCHRONOUS BUCK-BOOST (DIRECT PWM CONTROL)"]
        GATE_DRV["Dual Synchronous Gate Drivers<br/>TI UCC27211A / LM5106 (120V, 4A)<br/>• High/Low Side Drivers<br/>• Hardware Dead-Time Generation<br/>• Bootstrap Diodes & Caps"]:::bbPwr
        H_BRIDGE["4-Switch H-Bridge MOSFETs<br/>Infineon BSC034N04LS (40V, 3.4mΩ)<br/>• QA (Buck High) / QB (Buck Low)<br/>• QC (Boost High) / QD (Boost Low)"]:::bbPwr
        L1_IND["Power Inductor L1<br/>Wurth 7443321000 (10.0µH)<br/>Flat-Wire 8.5A RMS / 11.5A Sat"]:::bbPwr
        R_SHUNT["Kelvin Shunt R_SHUNT<br/>Bourns 10.0mΩ, 0.1%, 3W<br/>2512 4-Terminal Metal Strip"]:::bbPwr
        C_OUT["Output Filter Caps<br/>• 4x 22µF / 25V X7R MLCC<br/>• 1x 220µF / 25V Polymer Cap"]:::bbPwr

        BUS_24V -->|"Power In (+24V)"| H_BRIDGE
        GATE_DRV -->|"Gate Drive Lines (QA..QD)"| H_BRIDGE
        H_BRIDGE -->|"SW1, SW2 Nodes"| L1_IND
        H_BRIDGE -->|"Regulated Output"| R_SHUNT
        R_SHUNT --> C_OUT
    end

    subgraph VOLTAGE_FEEDBACK ["PASSIVE VOLTAGE SENSING ATTENUATOR"]
        R_FB1["R_FB1: 49.9kΩ (0.1%)<br/>VOUT Tap Resistor"]:::fbStyle
        R_FB2["R_FB2: 3.65kΩ (0.1%)<br/>Ground Sense Resistor"]:::fbStyle
        ADC_VOUT_NODE["V_SENSE Node (0 - 1.36V)<br/>Direct Attenuation to MCU ADC<br/>NO Voltage Steering / NO DAC Injection"]:::fbStyle

        C_OUT -->|"VOUT+ (5V - 20V)"| R_FB1
        R_FB1 --> ADC_VOUT_NODE
        R_FB2 -->|"GND_SEC"| ADC_VOUT_NODE
    end

    subgraph TELEMETRY_FRONTEND ["DUAL-DOMAIN SENSING & TELEMETRY FRONTEND"]
        U4_INA226["DC Power Monitor U4<br/>TI INA226 (I2C @ 0x40)<br/>• IN+ / IN- across R_SHUNT<br/>• VBUS connected to VOUT+<br/>• ALERT: Fast OCP Interrupt"]:::tlmStyle
        U5_AMC1311["AC Voltage Sensing U5<br/>TI AMC1311 (Reinforced)<br/>• VINP/N from 1MΩ Divider<br/>• VOUTP/N Diff to MCU ADC"]:::tlmStyle
        CT1_BURDEN["AC Current Sensing CT1<br/>Talema AC1005 (1000:1)<br/>• 100Ω Burden Resistor<br/>• Clamping Diodes to ADC"]:::tlmStyle

        R_SHUNT -->|"Kelvin V_SENSE"| U4_INA226
        C_OUT -->|"VBUS"| U4_INA226
        STAGE1 -.->|"AC Line Voltage"| U5_AMC1311
        STAGE1 -.->|"Line Wire Passage"| CT1_BURDEN
        U5_AMC1311 --- ISO_AMC
        CT1_BURDEN --- ISO_CT1
    end

    subgraph AUX_SUPPLY ["AUXILIARY BIAS POWER RAIL NETWORK"]
        U7_BUCK["Aux Buck Converter U7<br/>TI LMR33630 (36V -> 5.0V)<br/>Output: +5.0V DC System Rail"]:::auxStyle
        U8_LDO["Ultra-Low-Noise LDO U8<br/>TI TPS7A4700 (5.0V -> 3.3V)<br/>Output: +3.3V DC Quiet Rail"]:::auxStyle
        U9_ISODC["Isolated DC-DC U9<br/>Mornsun B0505S-1WR3<br/>Output: +5V_ISO (Hot Domain)"]:::auxStyle

        BUS_24V -->|"+24V Input"| U7_BUCK
        U7_BUCK -->|"+5.0V System Rail"| U8_LDO
        U7_BUCK -->|"+5.0V Supply"| U9_ISODC
        U9_ISODC -->|"+5V_ISO"| ISO_DC_DC
        ISO_DC_DC -->|"VDD1_ISO"| U5_AMC1311
    end

    subgraph HOST_MCU ["HOST MCU & DIGITAL PWM CONTROLLER"]
        U6_MCU["Host Controller U6<br/>STM32G474 Mixed-Signal MCU<br/>• HRTIM: Direct PWM Duty Cycle (D)<br/>  - D = 20.8% (5V) to 83.3% (20V)<br/>• ADC1_IN4 <- V_SENSE (Direct Voltage)<br/>• COMP1 <- R_SHUNT (<30ns Hardware Trip)<br/>• I2C1 (SCL/SDA) Bus<br/>• ADC1 (VAC_P/N, IAC) Line Channels<br/>• VDD / VREF: +3.3V Quiet Rail"]:::mcuStyle
        DISP_OLED["1.3 inch OLED Display<br/>SSD1306 (128x64 I2C @ 0x3C)<br/>Telemetry & Status (10Hz)"]:::mcuStyle
        ROT_ENC["Rotary Encoder EC11<br/>Dual-Phase Quadrature<br/>+ Push-Button (Vset / Ilimit)"]:::mcuStyle
        BTN_ONOFF["Output Enable Button<br/>Front-Panel Illuminated Switch"]:::mcuStyle
        STATUS_LEDS["Status LEDs<br/>• Green: Standby / Power<br/>• Blue: Output Active<br/>• Red: Fault / Trip"]:::mcuStyle
        USB_UART["USB-C / UART Bridge<br/>CP2102 / CH340G<br/>PC Telemetry & SCPI Control"]:::mcuStyle

        U8_LDO -->|"+3.3V Quiet Rail"| U6_MCU
        U7_BUCK -->|"+5.0V Display Rail"| DISP_OLED
        U7_BUCK -->|"+5.0V Driver Bias"| GATE_DRV
        U6_MCU -->|"Direct PWM (D=20.8%-83.3%)"| GATE_DRV
        ADC_VOUT_NODE -->|"V_SENSE Analog In"| U6_MCU
        R_SHUNT -.->|"Fast Shunt Tap (<30ns)"| U6_MCU
        U4_INA226 -->|"I2C Bus + ALERT"| U6_MCU
        U5_AMC1311 -->|"Diff Analog VAC"| U6_MCU
        CT1_BURDEN -->|"Analog IAC"| U6_MCU
        U6_MCU <-->|"I2C Bus"| DISP_OLED
        ROT_ENC -->|"Pins A, B, SW"| U6_MCU
        BTN_ONOFF -->|"Active Low"| U6_MCU
        U6_MCU -->|"GPIO Drives"| STATUS_LEDS
        U6_MCU <-->|"UART TX / RX"| USB_UART
    end

    subgraph OUTPUT_STAGE ["OUTPUT POWER TERMINALS & LOAD (TOUCH-SAFE SELV)"]
        J2_OUT["Output Terminals J2<br/>Heavy-Duty 4mm Binding Posts<br/>• Red: VOUT+ (5.0V to 20.0V DC)<br/>• Black: VOUT- (GND_SEC Return)<br/>• Green: Chassis Earth PE"]:::outStyle
        LOAD_DUT["Device Under Test (DUT)<br/>Max Continuous: 60W (3.0A)<br/>Peak Ripple < 25mV pk-pk"]:::outStyle

        C_OUT -->|"Power Out+" | J2_OUT
        R_FB2 -->|"GND_SEC"| J2_OUT
        J2_OUT -->|"DC Power Cable"| LOAD_DUT
    end
"""

# ==============================================================================
# GRAPHVIZ SOURCE: COMPONENT CONNECTIONS BLOCK DIAGRAM (NO VOLTAGE STEERING)
# ==============================================================================

dot_content = r"""digraph ComponentConnectionsDiagram {
    graph [
        rankdir=TB,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=13,
        nodesep=0.40,
        ranksep=0.60,
        pad="0.30,0.30",
        splines=true
    ];

    node [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=9.0,
        shape=box,
        style="filled,rounded",
        penwidth=1.5,
        margin="0.15,0.10"
    ];

    edge [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=8.0,
        penwidth=1.4,
        color="#37474F",
        arrowsize=0.75
    ];

    // ==========================================
    // STAGE 1: MAINS AC & PROTECTION
    // ==========================================
    subgraph cluster_stage1 {
        label="STAGE 1: MAINS AC INPUT & EMI FILTERING (HOT DOMAIN)";
        fontcolor="#263238";
        fontsize=11;
        fillcolor="#ECEFF1";
        style="filled,rounded";
        color="#90A4AE";

        J1 [label="AC Mains Inlet J1\nIEC 320-C14 (85-265V AC)\nPins: L, N, PE", fillcolor="#FFFFFF", color="#455A64"];
        F1 [label="Cartridge Fuse F1\n2.0A / 250V AC Time-Lag\n5x20mm Ceramic", fillcolor="#FFFFFF", color="#455A64"];
        NTC1 [label="Inrush Thermistor NTC1\n10Ω Cold, 3.2A RMS\nRadial Disc 13mm", fillcolor="#FFFFFF", color="#455A64"];
        MOV1 [label="Surge Varistor MOV1\n14D471K (300V RMS, 4.5kA)\nPhase-to-Neutral Clamp", fillcolor="#FFFFFF", color="#455A64"];
        CX1 [label="X2 Safety Cap CX1\n0.22µF / 275V AC Film\n+ Bleeder R_DIS1 (1MΩ)", fillcolor="#FFFFFF", color="#455A64"];
        L_CM1 [label="CM Choke L_CM1\n15.0mH, 1.1A RMS\nToroidal Core", fillcolor="#FFFFFF", color="#455A64"];
        CY1_2 [label="Y2 Safety Caps CY1/2\n2x 2.2nF / 300V AC\nLine/Neut to Chassis PE", fillcolor="#FFFFFF", color="#455A64"];
        CX2 [label="X2 Safety Cap CX2\n0.22µF / 275V AC Film\n+ Bleeder R_DIS2 (1MΩ)", fillcolor="#FFFFFF", color="#455A64"];
        L_CM2 [label="CM Choke L_CM2\n4.7mH, 1.6A RMS\nHigh-Frequency Stage", fillcolor="#FFFFFF", color="#455A64"];
        CY3_4 [label="Y2 Safety Caps CY3/4\n2x 2.2nF / 300V AC\nLine/Neut to Chassis PE", fillcolor="#FFFFFF", color="#455A64"];

        J1 -> F1 [label="Line"];
        F1 -> NTC1;
        NTC1 -> MOV1;
        J1 -> CX1 [label="Neutral"];
        MOV1 -> CX1;
        CX1 -> L_CM1;
        L_CM1 -> CY1_2;
        CY1_2 -> CX2;
        CX2 -> L_CM2;
        L_CM2 -> CY3_4;
    }

    // ==========================================
    // STAGE 2: RECTIFIER & BULK DC
    // ==========================================
    subgraph cluster_stage2 {
        label="STAGE 2: BRIDGE RECTIFIER & BULK DC BUS (HOT DOMAIN)";
        fontcolor="#BF360C";
        fontsize=11;
        fillcolor="#FFF3E0";
        style="filled,rounded";
        color="#FFB74D";

        BR1 [label="Bridge Rectifier BR1\nGBU606 (600V, 6A)\nPins: AC1, AC2, (+), (-)", fillcolor="#FFFFFF", color="#E65100"];
        C_BULK [label="Bulk Cap C_BULK\n100µF / 450V Electrolytic\n+ C_HF 0.1µF Film", fillcolor="#FFFFFF", color="#E65100"];
        R_BLEED [label="Bleeder Resistor\n330kΩ, 2W Metal Oxide\nDischarge Safety", fillcolor="#FFFFFF", color="#E65100"];

        CY3_4 -> BR1 [label="Filtered AC"];
        BR1 -> C_BULK [label="+HVDC / GND_PRI"];
        C_BULK -> R_BLEED [style=dashed, arrowhead=none];
    }

    // ==========================================
    // STAGE 3: FLYBACK PRIMARY & CONTROLLER
    // ==========================================
    subgraph cluster_stage3_pri {
        label="STAGE 3: 65 kHz FLYBACK PRIMARY & PWM CONTROLLER (GND_PRI)";
        fontcolor="#BF360C";
        fontsize=11;
        fillcolor="#FBE9E7";
        style="filled,rounded";
        color="#FF8A65";

        TX1_PRI [label="Transformer TX1 Primary\nPQ26/20 (3C95 Ferrite)\nLp=220µH, Np=36T\nPins 1 (+HVDC) -> 3 (Drain)", fillcolor="#FFFFFF", color="#D84315"];
        Q1_FET [label="Primary MOSFET Q1\nSTP10NK80Z (800V, 17A, 0.29Ω)\nPins: Drain, Gate, Source", fillcolor="#FFFFFF", color="#D84315"];
        RCD_CLAMP [label="RCD Snubber Network\n• US1M Diode (1000V, 1A)\n• 1nF / 1kV + 22.6kΩ Net", fillcolor="#FFFFFF", color="#D84315"];
        R_CS [label="CS Shunt R_CS\n0.25Ω / 1%, 2W Metal\nSource to GND_PRI", fillcolor="#FFFFFF", color="#D84315"];
        U1_PWM [label="PWM Controller U1\nTI UC3843 / UCC28C43 (65 kHz)\n• Pin 7: VCC (+14V Aux)\n• Pin 4: RT/CT (10kΩ / 2.2nF)\n• Pin 3: ISENSE (1.0V OCP)\n• Pin 6: OUT (Gate Drive)\n• Pin 1: COMP / Pin 2: FB", fillcolor="#FFFFFF", color="#D84315"];
        TX1_AUX [label="TX1 Aux Winding\nNaux=5T (Pins 4, 5)\n+ UF4004 & 47µF Cap", fillcolor="#FFFFFF", color="#D84315"];

        C_BULK -> TX1_PRI [label="+HVDC Rail"];
        TX1_PRI -> Q1_FET [label="Pin 3"];
        TX1_PRI -> RCD_CLAMP [style=dotted];
        Q1_FET -> R_CS [label="Source"];
        U1_PWM -> Q1_FET [label="OUT (Pin 6)"];
        R_CS -> U1_PWM [label="ISENSE (Pin 3)"];
        TX1_AUX -> U1_PWM [label="VCC (+14V)"];
    }

    // ==========================================
    // REINFORCED ISOLATION BARRIER
    // ==========================================
    subgraph cluster_isolation {
        label="⚡ REINFORCED ISOLATION BARRIER (IEC 62368-1 / 3000V RMS / 6.4mm Creepage)";
        fontcolor="#C62828";
        fontsize=11;
        fillcolor="#FFEBEE";
        style="filled,rounded";
        color="#EF5350";

        ISO_TX1 [label="TX1 Secondary Winding\nFurukawa TEX-E TIW (Ns=6T)\n3000V RMS Isolation", fillcolor="#FFFFFF", color="#C62828"];
        ISO_OPTO [label="Optocoupler OPTO1\nPC817 (5000V RMS)\nVoltage Loop Feedback", fillcolor="#FFFFFF", color="#C62828"];
        ISO_AMC [label="TI AMC1311 Modulator\n5000V RMS Reinforced\nIsolated AC Voltage Sense", fillcolor="#FFFFFF", color="#C62828"];
        ISO_CT1 [label="Talema AC1005 (1000:1)\nGalvanic Current Transformer\nIsolated AC Line Current", fillcolor="#FFFFFF", color="#C62828"];
        ISO_DC_DC [label="Isolated DC-DC U9\nMornsun B0505S-1WR3 (1W)\nHot-Side +5V_ISO Bias", fillcolor="#FFFFFF", color="#C62828"];
    }

    // ==========================================
    // STAGE 3: SCHOTTKY RECTIFIER & +24V BUS
    // ==========================================
    subgraph cluster_stage3_sec {
        label="STAGE 3: SCHOTTKY RECTIFICATION & +24V INTERMEDIATE BUS (SELV)";
        fontcolor="#1B5E20";
        fontsize=11;
        fillcolor="#E8F5E9";
        style="filled,rounded";
        color="#81C784";

        D_SEC [label="Schottky Diode D_SEC\nON Semi MBR10100 (100V, 10A)\nPassive Rectifier + Heatsink", fillcolor="#FFFFFF", color="#2E7D32"];
        C_SEC [label="Secondary LC Filter\n470µF/35V + 2.2µH + 22µF\nRipple < 40mV pk-pk", fillcolor="#FFFFFF", color="#2E7D32"];
        BUS_24V [label="+24.0V DC Rail\nStable 72W DC Bus\n(±1.0% Regulated)", fillcolor="#FFFFFF", color="#2E7D32"];
        U2_TL431 [label="Shunt Regulator U2\nTI TL431 (2.495V Ref)\n+ Divider 21.5k / 2.49k", fillcolor="#FFFFFF", color="#2E7D32"];

        TX1_PRI -> ISO_TX1 [style=dotted, label="Core Coupling"];
        ISO_TX1 -> D_SEC [label="Flyback Pulses"];
        D_SEC -> C_SEC;
        C_SEC -> BUS_24V [label="+24V Rail"];
        BUS_24V -> U2_TL431 [label="Sense Divider"];
        U2_TL431 -> ISO_OPTO [label="LED Drive"];
        ISO_OPTO -> U1_PWM [label="COMP Pin 1"];
    }

    // ==========================================
    // STAGE 4: BUCK-BOOST POST-REGULATOR (DIRECT PWM)
    // ==========================================
    subgraph cluster_stage4 {
        label="STAGE 4: 4-SWITCH SYNCHRONOUS BUCK-BOOST (DIRECT PWM DUTY CYCLE CONTROL)";
        fontcolor="#004D40";
        fontsize=11;
        fillcolor="#E0F7FA";
        style="filled,rounded";
        color="#4DD0E1";

        GATE_DRV [label="Dual Synchronous Gate Drivers\nTI UCC27211A / LM5106 (120V, 4A)\n• Dual Half-Bridge Gate Drivers\n• Bootstrap Diodes & Caps\n• Hardware Dead-Time", fillcolor="#FFFFFF", color="#00838F"];
        H_BRIDGE [label="4-Switch H-Bridge FETs\n4x Infineon BSC034N04LS (40V)\nQA (Buck High), QB (Buck Low)\nQC (Boost High), QD (Boost Low)", fillcolor="#FFFFFF", color="#00838F"];
        L1_IND [label="Power Inductor L1\nWurth 7443321000 (10.0µH)\nFlat-Wire 8.5A RMS / 11.5A Sat", fillcolor="#FFFFFF", color="#00838F"];
        R_SHUNT [label="Kelvin Shunt R_SHUNT\nBourns 10.0mΩ, 0.1%, 3W\n2512 4-Terminal Metal Strip", fillcolor="#FFFFFF", color="#00838F"];
        C_OUT [label="Output Capacitor Bank\n• 4x 22µF / 25V X7R MLCC\n• 1x 220µF Polymer Cap", fillcolor="#FFFFFF", color="#00838F"];

        BUS_24V -> H_BRIDGE [label="Power Flow (+24V)"];
        GATE_DRV -> H_BRIDGE [label="Gate Drives (QA..QD)"];
        H_BRIDGE -> L1_IND [label="SW1, SW2"];
        H_BRIDGE -> R_SHUNT [label="Output Current"];
        R_SHUNT -> C_OUT [label="VOUT Rail (5V-20V)"];
    }

    // ==========================================
    // PASSIVE VOLTAGE FEEDBACK ATTENUATOR
    // ==========================================
    subgraph cluster_feedback {
        label="PASSIVE VOLTAGE SENSING ATTENUATOR";
        fontcolor="#311B92";
        fontsize=11;
        fillcolor="#EDE7F6";
        style="filled,rounded";
        color="#B39DDB";

        R_FB1 [label="R_FB1: 49.9kΩ (0.1%)\nVOUT Sense Attenuator", fillcolor="#FFFFFF", color="#512DA8"];
        R_FB2 [label="R_FB2: 3.65kΩ (0.1%)\nGround Sense Resistor", fillcolor="#FFFFFF", color="#512DA8"];
        V_SENSE_NODE [label="V_SENSE Node (0 - 1.36V)\nDirect to MCU ADC Channel\nNO Steering Resistors / NO DAC Injection", fillcolor="#FFFFFF", color="#512DA8"];

        C_OUT -> R_FB1 [label="VOUT+"];
        R_FB1 -> V_SENSE_NODE;
        R_FB2 -> V_SENSE_NODE;
    }

    // ==========================================
    // SENSING & TELEMETRY FRONTEND
    // ==========================================
    subgraph cluster_telemetry {
        label="DUAL-DOMAIN SENSING & TELEMETRY FRONTEND";
        fontcolor="#4A148C";
        fontsize=11;
        fillcolor="#F3E5F5";
        style="filled,rounded";
        color="#CE93D8";

        U4_INA226 [label="DC Power Monitor U4\nTI INA226 (I2C @ 0x40)\n• IN+/IN- Kelvin across R_SHUNT\n• VBUS connected to VOUT+\n• ALERT: Fast OCP Interrupt", fillcolor="#FFFFFF", color="#7B1FA2"];
        U5_AMC1311 [label="AC Voltage Sense U5\nTI AMC1311 Modulator\n• 1MΩ Precision Divider\n• Differential VOUT to MCU", fillcolor="#FFFFFF", color="#7B1FA2"];
        CT1_BURDEN [label="AC Current Sense CT1\nTalema AC1005 (1000:1)\n• 100Ω Burden Resistor\n• Clamping Diodes to ADC", fillcolor="#FFFFFF", color="#7B1FA2"];

        R_SHUNT -> U4_INA226 [label="V_SHUNT"];
        C_OUT -> U4_INA226 [label="VBUS"];
        J1 -> U5_AMC1311 [style=dashed, label="Line Tap"];
        J1 -> CT1_BURDEN [style=dashed, label="Line Wire"];
        U5_AMC1311 -> ISO_AMC [style=dotted];
        CT1_BURDEN -> ISO_CT1 [style=dotted];
    }

    // ==========================================
    // AUXILIARY BIAS DISTRIBUTION
    // ==========================================
    subgraph cluster_aux {
        label="AUXILIARY BIAS POWER RAIL NETWORK";
        fontcolor="#FF6F00";
        fontsize=11;
        fillcolor="#FFF8E1";
        style="filled,rounded";
        color="#FFE082";

        U7_BUCK [label="Aux Buck Converter U7\nTI LMR33630 (36V -> 5.0V)\n+5.0V DC System Rail (2.5A)", fillcolor="#FFFFFF", color="#FFA000"];
        U8_LDO [label="Ultra-Low-Noise LDO U8\nTI TPS7A4700 / AP7365\n+3.3V DC Quiet Rail (<4.2µV)", fillcolor="#FFFFFF", color="#FFA000"];
        U9_ISODC [label="Isolated DC-DC U9\nMornsun B0505S-1WR3 (1W)\n+5V_ISO Hot Domain Rail", fillcolor="#FFFFFF", color="#FFA000"];

        BUS_24V -> U7_BUCK [label="+24V In"];
        U7_BUCK -> U8_LDO [label="+5.0V System"];
        U7_BUCK -> U9_ISODC [label="+5.0V Supply"];
        U9_ISODC -> ISO_DC_DC [style=dotted];
        ISO_DC_DC -> U5_AMC1311 [label="VDD1_ISO"];
    }

    // ==========================================
    // HOST MCU & DIGITAL PWM CONTROLLER
    // ==========================================
    subgraph cluster_mcu {
        label="HOST MCU & DIGITAL PWM CONTROLLER";
        fontcolor="#01579B";
        fontsize=11;
        fillcolor="#E1F5FE";
        style="filled,rounded";
        color="#81D4FA";

        U6_MCU [label="Host Microcontroller U6\nSTM32G474 Mixed-Signal MCU\n• High-Resolution PWM Timer (HRTIM)\n  Direct Duty Cycle Modulation (D=20.8%-83.3%)\n• ADC1_IN4: V_SENSE Direct Voltage Sense\n• COMP1: Ultra-Fast Hardware OCP (<30ns)\n• I2C1 (SCL/SDA) Bus\n• ADC1 (VAC_P/N, IAC)\n• VDD/VREF: +3.3V Quiet Rail", fillcolor="#FFFFFF", color="#0277BD"];
        DISP_OLED [label="1.3 inch OLED Display\nSSD1306 (128x64 I2C @ 0x3C)\n10Hz Real-Time Telemetry", fillcolor="#FFFFFF", color="#0277BD"];
        ROT_ENC [label="Rotary Encoder EC11\nDual-Phase Quadrature\n+ Push-Button (Vset / Ilimit)", fillcolor="#FFFFFF", color="#0277BD"];
        BTN_ONOFF [label="Output Enable Button\nFront-Panel Illuminated Switch\nHardware Debounced", fillcolor="#FFFFFF", color="#0277BD"];
        STATUS_LEDS [label="Status LEDs\n• Green: Power On\n• Blue: Output Active\n• Red: Overcurrent Fault", fillcolor="#FFFFFF", color="#0277BD"];
        USB_UART [label="USB-C / UART Interface\nCP2102 / CH340G\nPC GUI & SCPI Control", fillcolor="#FFFFFF", color="#0277BD"];

        U8_LDO -> U6_MCU [label="+3.3V Quiet"];
        U7_BUCK -> DISP_OLED [label="+5.0V Supply"];
        U7_BUCK -> GATE_DRV [label="+5V Driver Bias"];
        U6_MCU -> GATE_DRV [label="Direct PWM Drive (D)"];
        V_SENSE_NODE -> U6_MCU [label="V_SENSE to ADC"];
        R_SHUNT -> U6_MCU [style=dashed, label="Fast Shunt Tap (<30ns)"];
        U4_INA226 -> U6_MCU [label="I2C / ALERT"];
        U5_AMC1311 -> U6_MCU [label="Diff VAC ADC"];
        CT1_BURDEN -> U6_MCU [label="Analog IAC ADC"];
        U6_MCU -> DISP_OLED [label="I2C SCL/SDA"];
        ROT_ENC -> U6_MCU [label="Pins A, B, SW"];
        BTN_ONOFF -> U6_MCU [label="Active Low"];
        U6_MCU -> STATUS_LEDS [label="GPIO Drivers"];
        U6_MCU -> USB_UART [dir=both, label="UART TX/RX"];
    }

    // ==========================================
    // OUTPUT STAGE & LOAD
    // ==========================================
    subgraph cluster_output {
        label="OUTPUT POWER TERMINALS & LOAD (TOUCH-SAFE SELV)";
        fontcolor="#1A237E";
        fontsize=11;
        fillcolor="#E8EAF6";
        style="filled,rounded";
        color="#9FA8DA";

        J2_OUT [label="Output Binding Posts J2\n4mm Heavy-Duty Terminals\n• Red: VOUT+ (5-20V DC)\n• Black: VOUT- (GND_SEC)\n• Green: Chassis Earth PE", fillcolor="#FFFFFF", color="#283593"];
        LOAD_DUT [label="Target Load (DUT)\n5.0V - 20.0V DC @ 0 - 3.0A (60W)\nRipple < 25mV pk-pk", fillcolor="#FFFFFF", color="#283593"];

        C_OUT -> J2_OUT [label="VOUT+ / GND_SEC"];
        J2_OUT -> LOAD_DUT [label="DC Power Cable"];
    }
}
"""

def main():
    print("Writing Mermaid source files...")
    # Staging path
    mmd_path1 = os.path.join(MMD_DIR, "figure12_detailed_component_connections_block_diagram.mmd")
    with open(mmd_path1, "w", encoding="utf-8") as f:
        f.write(mmd_content)
    print(f"  Created: {mmd_path1}")

    # Synchronize to smart_programmable_power_supply/mermaid/
    mmd_path2 = os.path.join(REPO_MMD_DIR, "figure12_detailed_component_connections_block_diagram.mmd")
    with open(mmd_path2, "w", encoding="utf-8") as f:
        f.write(mmd_content)
    print(f"  Created: {mmd_path2}")

    mmd_path3 = os.path.join(REPO_MMD_DIR, "component_connections_block_diagram.mmd")
    with open(mmd_path3, "w", encoding="utf-8") as f:
        f.write(mmd_content)
    print(f"  Created: {mmd_path3}")

    print("Writing Graphviz DOT source...")
    dot_path = os.path.join(DIAG_DIR, "figure12_detailed_component_connections_block_diagram.dot")
    with open(dot_path, "w", encoding="utf-8") as f:
        f.write(dot_content)
    print(f"  Created: {dot_path}")

    # Also synchronize DOT to smart_programmable_power_supply/
    repo_dot_path = os.path.join(os.path.dirname(BASE_DIR), "smart_programmable_power_supply", "figure12_detailed_component_connections_block_diagram.dot")
    with open(repo_dot_path, "w", encoding="utf-8") as f:
        f.write(dot_content)

    print("Rendering SVG and PNG using Graphviz dot...")
    svg_path = os.path.join(DIAG_DIR, "figure12_detailed_component_connections_block_diagram.svg")
    png_path = os.path.join(DIAG_DIR, "figure12_detailed_component_connections_block_diagram.png")
    
    repo_svg_path = os.path.join(os.path.dirname(BASE_DIR), "smart_programmable_power_supply", "figure12_detailed_component_connections_block_diagram.svg")
    repo_png_path = os.path.join(os.path.dirname(BASE_DIR), "smart_programmable_power_supply", "figure12_detailed_component_connections_block_diagram.png")

    cmd_svg = ["dot", "-Tsvg", dot_path, "-o", svg_path]
    cmd_png = ["dot", "-Tpng", "-Gdpi=150", dot_path, "-o", png_path]

    subprocess.run(cmd_svg, check=True)
    subprocess.run(cmd_png, check=True)
    print(f"  Rendered: {svg_path}")
    print(f"  Rendered: {png_path}")

    # Copy to repo folder as well
    subprocess.run(["cp", svg_path, repo_svg_path], check=True)
    subprocess.run(["cp", png_path, repo_png_path], check=True)
    print(f"  Synchronized: {repo_svg_path}")
    print(f"  Synchronized: {repo_png_path}")

    print("SUCCESS: Component connections block diagram generated in Mermaid, DOT, SVG, and PNG without voltage steering!")

if __name__ == "__main__":
    main()
