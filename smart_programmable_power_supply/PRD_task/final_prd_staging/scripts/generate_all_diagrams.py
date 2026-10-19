#!/usr/bin/env python3
"""
Generate all 11 architectural block diagrams and flowcharts for the
VVDN Smart Programmable Power Supply (VVDN_SPPS_2026) PRD.
Outputs:
  - Mermaid code (.mmd) into final_prd_staging/mermaid/
  - Graphviz source (.dot) into final_prd_staging/diagrams/
  - Rendered vector graphics (.svg) into final_prd_staging/diagrams/
  - High-resolution raster images (.png, 150 DPI) into final_prd_staging/diagrams/
"""

import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIAG_DIR = os.path.join(BASE_DIR, "diagrams")
MMD_DIR = os.path.join(BASE_DIR, "mermaid")

os.makedirs(DIAG_DIR, exist_ok=True)
os.makedirs(MMD_DIR, exist_ok=True)

# ==============================================================================
# 1. FIGURE 1: BOUNDARY DIAGRAM / SIMPLIFIED 4-STAGE POWER FLOW
# ==============================================================================
fig1_mmd = r"""flowchart LR
    %% Domain Styles
    classDef acStyle fill:#ECEFF1,stroke:#37474F,stroke-width:2px,color:#263238
    classDef rectStyle fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#BF360C
    classDef isoStyle fill:#C8E6C9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20
    classDef bbStyle fill:#B2EBF2,stroke:#00838F,stroke-width:2px,color:#004D40
    classDef dutStyle fill:#E1BEE7,stroke:#6A1B9A,stroke-width:2px,color:#4A148C

    subgraph HOT_DOMAIN ["PRIMARY HOT DOMAIN (High Voltage)"]
        S1["<b>Stage 1: MAINS SUPPLY & EMI</b><br/>• 85V - 265V AC RMS, 47-63Hz<br/>• 2A Fuse, 10Ω NTC, 300V MOV<br/>• 2-Stage Common-Mode Filter"]:::acStyle
        S2["<b>Stage 2: RECTIFIER & BULK DC</b><br/>• GBU606 Bridge (600V, 6A)<br/>• 100µF / 450V Bulk Cap<br/>• +120V to +375V DC Bus"]:::rectStyle
        S1 -->|"Filtered AC"| S2
    end

    subgraph COLD_DOMAIN ["SECONDARY COLD DOMAIN (Touch-Safe SELV)"]
        S3["<b>Stage 3: CONVERTER DC-DC</b><br/>• Uniform-Freq Flyback (UC3843 @ 65kHz)<br/>• PQ26/20 Core (Lp = 220µH, 6:1 turns)<br/>• MBR10100 Schottky Diode + Heatsink<br/>• +24.0V DC Intermediate Rail (72W)"]:::isoStyle
        S4["<b>Stage 4: POST-REGULATOR</b><br/>• 4-Switch Buck-Boost (TI LM5176 @ 300kHz)<br/>• 4x 40V Low-Rds MOSFETs + 10µH Inductor<br/>• Direct PWM Duty Cycle Control (D = 20.8% - 83.3%)<br/>• Built-in CSP/CSN Peak Current Limit<br/>• 5.0V - 20.0V DC / 3.0A (60W)"]:::bbStyle
        S3 -->|"+24.0V DC Rail"| S4
    end

    subgraph LOAD_DOMAIN ["APPLICATION / LOAD"]
        S5["<b>5. TARGET DEVICE (DUT)</b><br/>• 4mm Gold Binding Posts<br/>• Clean DC: Ripple < 25mV pk-pk<br/>• Touch-Safe SELV Compliant"]:::dutStyle
    end

    S2 ==>|"⚡ 3000V RMS Galvanic Barrier<br/>(IEC 62368-1 Reinforced, 6.4mm Creepage)"| S3
    S4 -->|"Regulated DC Power"| S5
"""

fig1_dot = r"""digraph Figure1PowerFlow {
    graph [
        rankdir=LR,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.45,
        ranksep=0.70,
        pad="0.25,0.25",
        splines=true
    ];

    node [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=9.5,
        shape=box,
        style="filled,rounded",
        margin="0.16,0.12",
        penwidth=1.6
    ];

    edge [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=8.5,
        penwidth=2.2,
        arrowsize=0.8
    ];

    subgraph cluster_hot_domain {
        label = "PRIMARY HOT DOMAIN (High Voltage Grid)";
        style = "filled,rounded,dashed";
        fillcolor = "#F5F5F5";
        color = "#B71C1C";
        penwidth = 1.8;

        s1 [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>STAGE 1: MAINS &amp; EMI</b></td></tr>
                <tr><td><font color="#455A64">AC Protection &amp; Filtering</font></td></tr>
                <hr/>
                <tr><td align="left">• 85V – 265V AC RMS, 47–63 Hz</td></tr>
                <tr><td align="left">• 2A Time-Lag Ceramic Fuse</td></tr>
                <tr><td align="left">• 10Ω NTC Inrush Limiter</td></tr>
                <tr><td align="left">• 300V RMS MOV Surge Clamp</td></tr>
                <tr><td align="left">• 2-Stage Common-Mode Choke</td></tr>
            </table>>,
            fillcolor = "#ECEFF1",
            color = "#37474F"
        ];

        s2 [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>STAGE 2: RECTIFIER &amp; BULK</b></td></tr>
                <tr><td><font color="#E65100">AC to Unregulated HVDC</font></td></tr>
                <hr/>
                <tr><td align="left">• GBU606 Bridge (600V, 6A)</td></tr>
                <tr><td align="left">• 100µF / 450V Bulk Electrolytic</td></tr>
                <tr><td align="left">• Holdup Time &gt; 10 ms</td></tr>
                <tr><td align="left">• Bleeder Discharge String</td></tr>
                <tr><td align="left">• Bus: +120V to +375V DC</td></tr>
            </table>>,
            fillcolor = "#FFF3E0",
            color = "#E65100"
        ];

        s1 -> s2 [label=" Filtered AC", color="#37474F"];
    }

    subgraph cluster_cold_domain {
        label = "SECONDARY TOUCH-SAFE SELV DOMAIN";
        style = "filled,rounded,dashed";
        fillcolor = "#F1F8E9";
        color = "#2E7D32";
        penwidth = 1.8;

        s3 [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>STAGE 3: CONVERTER DC-DC</b></td></tr>
                <tr><td><font color="#2E7D32">Uniform-Frequency Flyback</font></td></tr>
                <hr/>
                <tr><td align="left">• UC3843 PWM @ Uniform 65 kHz</td></tr>
                <tr><td align="left">• PQ26/20 Core (Lp = 220µH, 6:1)</td></tr>
                <tr><td align="left">• 800V Superjunction MOSFET</td></tr>
                <tr><td align="left">• MBR10100 Schottky Diode</td></tr>
                <tr><td align="left">• Rail: +24.0V DC / 72W (3A)</td></tr>
            </table>>,
            fillcolor = "#E8F5E9",
            color = "#2E7D32"
        ];

        s4 [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>STAGE 4: POST-REGULATOR</b></td></tr>
                <tr><td><font color="#00838F">Synchronous 4-Switch Buck-Boost</font></td></tr>
                <hr/>
                <tr><td align="left">• TI LM5176 Controller @ 300 kHz</td></tr>
                <tr><td align="left">• 4x 40V MOSFETs + 10µH Inductor</td></tr>
                <tr><td align="left">• Direct PWM Duty Cycle Control</td></tr>
                <tr><td align="left">• Cycle-by-Cycle CSP/CSN Clamp</td></tr>
                <tr><td align="left">• Output: 5.0V – 20.0V DC / 3.0A</td></tr>
            </table>>,
            fillcolor = "#E0F7FA",
            color = "#00838F"
        ];

        s3 -> s4 [label=" +24.0V DC Rail\n(72W continuous)", color="#2E7D32"];
    }

    s5 [
        label = <<table border="0" cellborder="0" cellspacing="2">
            <tr><td><b>DEVICE UNDER TEST (DUT)</b></td></tr>
            <tr><td><font color="#6A1B9A">Benchtop / ATE Load</font></td></tr>
            <hr/>
            <tr><td align="left">• 4mm Gold Binding Posts</td></tr>
            <tr><td align="left">• Clean DC: Ripple &lt; 25mV pk-pk</td></tr>
            <tr><td align="left">• Output Power: Up to 60W</td></tr>
            <tr><td align="left">• Touch-Safe SELV Protected</td></tr>
        </table>>,
        fillcolor = "#F3E5F5",
        color = "#6A1B9A"
    ];

    s2 -> s3 [
        label = "⚡ 3000V RMS Reinforced Galvanic Barrier\n(IEC 62368-1 SELV, 6.4mm Creepage, 2.0mm Milled Slot)",
        color = "#C62828",
        style = "bold",
        penwidth = 3.0
    ];

    s4 -> s5 [label=" Regulated DC Output\n(5.0V - 20.0V / 3A)", color="#00838F", penwidth=2.5];
}
"""

# ==============================================================================
# 2. FIGURE 2: USE CASE 1 - CV REGULATION & PWM DUTY CYCLE MODULATION
# ==============================================================================
fig2_mmd = r"""sequenceDiagram
    autonumber
    actor User as Operator / ATE Host
    participant UI as Front Panel / SCPI
    participant MCU as STM32G474 Brain
    participant DAC as Internal 12-Bit DAC
    participant Sum as Resistor Summing Network
    participant LM as LM5176 Buck-Boost
    participant Out as 4mm Output Terminals
    participant INA as INA226 Telemetry

    User->>UI: Select Setpoint (e.g. 12.00 V, 3.00 A)
    UI->>MCU: Forward Target via Encoder / SCPI
    MCU->>MCU: Compute PWM Duty Cycle: D = V_target / 24.0V
    MCU->>LM: Output 300 kHz High-Resolution PWM (D = 20.8% to 83.3%)
    LM->>LM: Modulate 4-Switch Synchronous H-Bridge
    LM->>Out: Slew Output Rail (dV/dt Controlled Soft Step)
    Out-->>INA: Sensed V_OUT, I_LOAD across 10mΩ Shunt
    INA->>MCU: Stream 16-Bit Voltage & Current via I2C (10 Hz)
    MCU->>UI: Update 1.3" OLED Dashboard & Mode LEDs (CV Active)
    Note over Out,LM: Load step applied: 0.1A -> 3.0A<br/>Recovery < 150 µs, Sag < 250 mV
"""

fig2_dot = r"""digraph Figure2UseCaseCV {
    graph [
        rankdir=TB,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.35,
        ranksep=0.45,
        pad="0.25,0.25"
    ];

    node [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=9.5,
        shape=box,
        style="filled,rounded",
        margin="0.14,0.10",
        penwidth=1.5
    ];

    edge [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=8.5,
        penwidth=1.8,
        arrowsize=0.8
    ];

    user [label="Operator Input / Host ATE\n• Dual Rotary Encoders\n• USB-CDC SCPI Command", fillcolor="#ECEFF1", color="#37474F"];
    mcu [label="STM32G474 MCU Controller\n• Setpoint Validation (5.0V - 20.0V)\n• Linear DAC Voltage Calculation", fillcolor="#E1F5FE", color="#0277BD"];
    dac [label="12-Bit Monotonic DAC Channel\n• V_DAC Output: 0.00V to 3.30V\n• 10 mV Fine Resolution", fillcolor="#E8EAF6", color="#283593"];
    sum [label="Summing Network (R_top, R_DAC, R_bot)\n• Injects steering current into FB\n• Keeps FB at 1.20V Precision Ref", fillcolor="#F3E5F5", color="#6A1B9A"];
    lm5176 [label="TI LM5176 Controller\n• 300 kHz Synchronous PWM\n• Buck Mode (5-18V) / Buck-Boost (18-20V)", fillcolor="#E0F7FA", color="#00838F"];
    power_stage [label="4-Switch Synchronous Bridge & Inductor\n• 4x 40V BSC034N04LS MOSFETs\n• 10µH Flat-Wire Power Inductor", fillcolor="#B2EBF2", color="#00695C"];
    out_rail [label="DC Output Rail (5.0V - 20.0V / 3A)\n• Output Filter (4x 22µF MLCC + 100µF Poly)\n• Dynamic Recovery < 150µs, Sag < 250mV", fillcolor="#C8E6C9", color="#1B5E20"];
    telemetry [label="Dual Telemetry Verification\n• INA226 16-Bit I2C Power Monitor\n• 1.3\" OLED Dashboard Live Metering", fillcolor="#FFFDE7", color="#F57F17"];

    user -> mcu [label=" Setpoint Target"];
    mcu -> pwm_gen [label=" Duty Cycle Command"];
    pwm_gen -> lm5176 [label=" 300 kHz PWM Drive"];
    lm5176 -> power_stage [label=" 4x Gate Drives"];
    power_stage -> out_rail [label=" Regulated DC"];
    out_rail -> telemetry [label=" Kelvin Sensing"];
    telemetry -> mcu [label=" 10 Hz Telemetry Loop"];
    out_rail -> v_sense [label=" V_OUT Attenuation", style="dashed", color="#6A1B9A"];
    v_sense -> mcu [label=" ADC V_SENSE"];
}
"""

# ==============================================================================
# 3. FIGURE 3: USE CASE 2 - AUTONOMOUS CYCLE-BY-CYCLE CURRENT LIMITING
# ==============================================================================
fig3_mmd = r"""flowchart TD
    classDef startStyle fill:#ECEFF1,stroke:#37474F,stroke-width:2px,color:#263238
    classDef warnStyle fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#BF360C
    classDef faultStyle fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#B71C1C
    classDef safeStyle fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20
    classDef mcuStyle fill:#E1F5FE,stroke:#0277BD,stroke-width:2px,color:#01579B

    A["<b>NORMAL OPERATION</b><br/>• Output: 5V - 20V DC<br/>• Load Current: I_load ≤ 3.0A<br/>• Mode: Constant Voltage (CV)"]:::safeStyle
    B["<b>OVERLOAD / SHORT CIRCUIT EVENT</b><br/>• Heavy Load Step or Direct Short<br/>• Current surges past 3.5A limit"]:::warnStyle
    C{"<b>LM5176 CSP/CSN COMPARATOR</b><br/>Is V_shunt > 35mV across 10mΩ?<br/>(Peak Inductor Current Sense)"}:::faultStyle
    D["<b>CYCLE-BY-CYCLE HARDWARE CLAMP</b><br/>• LM5176 truncates active PWM pulse<br/>• Clamps peak inductor current immediately<br/>• Output voltage folds back to sustain limit<br/>• Response Time: &lt; 5 µs autonomous"]:::faultStyle
    E{"<b>IS OVERLOAD TRANSIENT OR PERSISTENT?</b><br/>Evaluated by MCU Telemetry Task (INA226)"}:::mcuStyle
    F["<b>TRANSIENT CLEARED (&lt; 500 ms)</b><br/>• Inductor current drops below 3.0A<br/>• LM5176 resumes normal PWM duty<br/>• Seamless return to CV Regulation"]:::safeStyle
    G["<b>PERSISTENT FAULT (&gt; 500 ms)</b><br/>• MCU detects thermal stress or dead short<br/>• MCU asserts GPIO low to LM5176 ENABLE pin<br/>• Synchronous bridge shut down safely<br/>• Amber / Red Mode LED latched on front panel"]:::faultStyle
    H["<b>SUPERVISED AUTO-RECOVERY</b><br/>• Operator clears short or presses Enable<br/>• MCU soft-starts LM5176 back to setpoint"]:::safeStyle

    A --> B
    B --> C
    C -- "YES" --> D
    D --> E
    E -- "Clears Quickly" --> F
    F --> A
    E -- "Sustained Overload" --> G
    G --> H
    H --> A
"""

fig3_dot = r"""digraph Figure3UseCaseOCP {
    graph [
        rankdir=TB,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.40,
        ranksep=0.45,
        pad="0.25,0.25"
    ];

    node [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=9.5,
        shape=box,
        style="filled,rounded",
        margin="0.14,0.10",
        penwidth=1.5
    ];

    edge [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=8.5,
        penwidth=1.8,
        arrowsize=0.8
    ];

    norm [label="NORMAL OPERATION\n• Output: 5.0V - 20.0V DC\n• Load Current: ≤ 3.0A\n• CV Mode (Green LED)", fillcolor="#E8F5E9", color="#2E7D32"];
    overload [label="OVERLOAD / SHORT CIRCUIT EVENT\n• Sudden heavy load step or terminal short\n• Current surges above 3.5A trip threshold", fillcolor="#FFF3E0", color="#E65100"];
    sense [label="LM5176 CSP/CSN COMPARATOR\n• 10mΩ Kelvin shunt senses peak current\n• V_sense exceeds internal current limit threshold", fillcolor="#FFEBEE", color="#C62828"];
    clamp [label="AUTONOMOUS HARDWARE CLAMP\n• Truncates current PWM pulse within cycle\n• Clamps peak inductor current (< 5µs response)\n• V_OUT drops proportionally to maintain limit", fillcolor="#FFCDD2", color="#B71C1C", penwidth=2.0];
    eval [label="MCU SUPERVISORY EVALUATION\n• INA226 samples continuous overload\n• Telemetry timer runs for 500 ms window", fillcolor="#E1F5FE", color="#0277BD"];
    recov [label="TRANSIENT RECOVERY\n• Short circuit cleared within 500 ms\n• LM5176 resumes full PWM duty\n• Output voltage restores smoothly to setpoint", fillcolor="#C8E6C9", color="#1B5E20"];
    shutdown [label="PERSISTENT FAULT SUPERVISORY SHUTDOWN\n• Overload persists > 500 ms\n• MCU pulls LM5176 ENABLE pin LOW\n• Synchronous switches disabled, Red Fault LED lit", fillcolor="#FFCDD2", color="#B71C1C"];
    manual_reset [label="SAFE RESTART & BRING-UP\n• Operator removes overload / presses Enable\n• MCU executes soft-start ramp to programmed setpoint", fillcolor="#ECEFF1", color="#37474F"];

    norm -> overload [label=" Overload Applied"];
    overload -> sense [label=" I_peak > 3.5A"];
    sense -> clamp [label=" Hardware Trip (< 5µs)"];
    clamp -> eval [label=" Cycle-by-cycle Limiting"];
    eval -> recov [label=" Overload Removed (< 500ms)", color="#2E7D32"];
    recov -> norm [label=" Normal CV Mode", color="#2E7D32"];
    eval -> shutdown [label=" Overload Persists (> 500ms)", color="#C62828"];
    shutdown -> manual_reset [label=" Push Button Reset / Clear Short"];
    manual_reset -> norm [label=" Soft-Start Ramp", color="#2E7D32"];
}
"""

# ==============================================================================
# 4. FIGURE 4: STAGE 1 - MAINS SUPPLY & INPUT PROTECTION SUBSYSTEM
# ==============================================================================
fig4_mmd = r"""flowchart LR
    classDef acStyle fill:#ECEFF1,stroke:#37474F,stroke-width:2px,color:#263238
    classDef protStyle fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#B71C1C
    classDef ntcStyle fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#BF360C
    classDef emiStyle fill:#E8EAF6,stroke:#283593,stroke-width:2px,color:#1A237E

    subgraph STAGE1_MAINS ["STAGE 1: AC MAINS SUPPLY & INPUT PROTECTION SUBSYSTEM"]
        INLET["<b>AC INLET</b><br/>IEC 320-C14<br/>• 85V - 265V AC RMS<br/>• 47Hz - 63Hz Grid<br/>• Line, Neutral, Earth"]:::acStyle
        FUSE["<b>OVERCURRENT FUSE</b><br/>F1: 2.0A / 250V AC<br/>• Time-Lag Ceramic Cartridge<br/>• 5x20mm Standard Holder<br/>• I²t ≥ 18 A²s Surge Rating"]:::protStyle
        NTC["<b>INRUSH LIMITER</b><br/>NTC1: 10Ω Cold Resistance<br/>• TDK Epcos B57236S<br/>• Limits Inrush &lt; 25A Peak<br/>• Drops to &lt; 0.4Ω Running"]:::ntcStyle
        MOV["<b>SURGE CLAMP</b><br/>MOV1: 14D471K Varistor<br/>• 300V RMS Clamping Level<br/>• 4.5kA (8/20µs) Peak Surge<br/>• IEC 61000-4-5 Level 3"]:::protStyle
        
        subgraph EMI_FILTER ["2-STAGE COMMON-MODE & DIFFERENTIAL EMI FILTER"]
            X1["<b>X2 FILM CAP 1</b><br/>220nF / 305V AC<br/>Differential DM Filter"]:::emiStyle
            CMC1["<b>COMMON-MODE CHOKE 1</b><br/>L_CM1: 15.0 mH Toroidal<br/>Suppresses 150kHz-2MHz"]:::emiStyle
            X2["<b>X2 FILM CAP 2</b><br/>100nF / 305V AC<br/>High-Freq DM Filter"]:::emiStyle
            CMC2["<b>COMMON-MODE CHOKE 2</b><br/>L_CM2: 4.7 mH High-Band<br/>Suppresses 2MHz-30MHz"]:::emiStyle
            YCAPS["<b>Y2 SAFETY CAPS</b><br/>2x 2.2nF / 400V AC<br/>Line/Neutral to Earth"]:::emiStyle
        end

        OUT_AC["<b>FILTERED AC OUTPUT</b><br/>Clean 85V - 265V AC<br/>Feeds Stage 2 Bridge Rectifier<br/>Meets CISPR 32 Class B"]:::acStyle

        INLET -->|L, N, PE| FUSE
        FUSE -->|Fused Line| NTC
        NTC -->|Inrush Clamped| MOV
        MOV -->|Protected AC| X1
        X1 --> CMC1
        CMC1 --> X2
        X2 --> CMC2
        CMC2 --> YCAPS
        YCAPS --> OUT_AC
    end
"""

fig4_dot = r"""digraph Figure4Stage1Mains {
    graph [
        rankdir=LR,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.35,
        ranksep=0.55,
        pad="0.25,0.25",
        splines=true
    ];

    node [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=9,
        shape=box,
        style="filled,rounded",
        margin="0.14,0.10",
        penwidth=1.5
    ];

    edge [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=8,
        penwidth=1.8,
        arrowsize=0.8
    ];

    subgraph cluster_mains {
        label = "STAGE 1: AC MAINS SUPPLY & INPUT PROTECTION SUBSYSTEM (HOT DOMAIN)";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#37474F";
        penwidth = 1.6;

        inlet [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>AC INLET</b></td></tr>
                <tr><td><font color="#455A64">IEC 320-C14</font></td></tr>
                <hr/>
                <tr><td align="left">• 85V – 265V AC RMS</td></tr>
                <tr><td align="left">• 47Hz – 63Hz Grid</td></tr>
                <tr><td align="left">• Line, Neutral, Earth</td></tr>
            </table>>,
            fillcolor = "#ECEFF1",
            color = "#37474F"
        ];

        fuse [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>OVERCURRENT</b></td></tr>
                <tr><td><font color="#D32F2F">F1: 2.0A / 250V AC</font></td></tr>
                <hr/>
                <tr><td align="left">• Time-Lag Ceramic</td></tr>
                <tr><td align="left">• 5x20mm Cartridge</td></tr>
                <tr><td align="left">• I²t ≥ 18 A²s Surge</td></tr>
            </table>>,
            fillcolor = "#FFEBEE",
            color = "#C62828"
        ];

        ntc [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>INRUSH LIMITER</b></td></tr>
                <tr><td><font color="#E65100">NTC1: 10Ω Cold</font></td></tr>
                <hr/>
                <tr><td align="left">• TDK B57236S</td></tr>
                <tr><td align="left">• Restricts I_inrush &lt; 25A</td></tr>
                <tr><td align="left">• Drops to &lt; 0.4Ω hot</td></tr>
            </table>>,
            fillcolor = "#FFF3E0",
            color = "#EF6C00"
        ];

        mov [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>SURGE CLAMP</b></td></tr>
                <tr><td><font color="#B71C1C">MOV1: 14D471K</font></td></tr>
                <hr/>
                <tr><td align="left">• 300V RMS Clamping</td></tr>
                <tr><td align="left">• 4.5kA (8/20µs) Peak</td></tr>
                <tr><td align="left">• IEC 61000-4-5 Level 3</td></tr>
            </table>>,
            fillcolor = "#FFCDD2",
            color = "#B71C1C"
        ];

        subgraph cluster_emi {
            label = "2-STAGE EMI FILTER (CISPR 32 CLASS B)";
            style = "filled,rounded";
            fillcolor = "#FFFFFF";
            color = "#283593";
            penwidth = 1.4;

            x1 [label="X2 Cap 1\n220nF / 305V", fillcolor="#E8EAF6", color="#283593"];
            cmc1 [label="CM Choke 1\nL_CM1: 15mH", fillcolor="#C5CAE9", color="#1A237E"];
            x2 [label="X2 Cap 2\n100nF / 305V", fillcolor="#E8EAF6", color="#283593"];
            cmc2 [label="CM Choke 2\nL_CM2: 4.7mH", fillcolor="#C5CAE9", color="#1A237E"];
            ycaps [label="Y2 Safety Caps\n2x 2.2nF / 400V", fillcolor="#E8EAF6", color="#283593"];

            x1 -> cmc1 [label=" DM Atten"];
            cmc1 -> x2;
            x2 -> cmc2 [label=" Stage 2"];
            cmc2 -> ycaps [label=" CM to Earth"];
        }

        out_ac [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>FILTERED AC BUS</b></td></tr>
                <tr><td><font color="#1B5E20">To Stage 2 Rectifier</font></td></tr>
                <hr/>
                <tr><td align="left">• Clean AC Mains</td></tr>
                <tr><td align="left">• Low Conducted Noise</td></tr>
                <tr><td align="left">• CISPR 32 Class B Pass</td></tr>
            </table>>,
            fillcolor = "#E8F5E9",
            color = "#2E7D32"
        ];

        inlet -> fuse [label=" L, N, PE"];
        fuse -> ntc [label=" Fused Line"];
        ntc -> mov [label=" Inrush Clamped"];
        mov -> x1 [label=" Protected AC"];
        ycaps -> out_ac [label=" Filtered AC Output"];
    }
}
"""

# ==============================================================================
# 5. FIGURE 5: STAGE 2 - BRIDGE RECTIFIER & BULK DC SUBSYSTEM
# ==============================================================================
fig5_mmd = r"""flowchart LR
    classDef acStyle fill:#ECEFF1,stroke:#37474F,stroke-width:2px,color:#263238
    classDef brStyle fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#BF360C
    classDef capStyle fill:#E1F5FE,stroke:#0277BD,stroke-width:2px,color:#01579B
    classDef bleederStyle fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#B71C1C
    classDef outStyle fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20

    subgraph STAGE2_RECTIFIER ["STAGE 2: BRIDGE RECTIFIER & HIGH-VOLTAGE BULK DC SUBSYSTEM"]
        IN_AC["<b>FILTERED AC INPUT</b><br/>From Stage 1 EMI Filter<br/>85V - 265V AC RMS"]:::acStyle
        GBU["<b>PASSIVE BRIDGE RECTIFIER</b><br/>BR1: Diodes Inc. GBU606<br/>• 600V PIV, 6.0A Rating<br/>• Full-Wave 100Hz/120Hz<br/>• Forward Drop: 2x 0.95V"]:::brStyle
        BULK_CAP["<b>BULK CAPACITOR BANK</b><br/>C_BULK: Nichicon 100µF / 450V<br/>• 105°C Long-Life Electrolytic<br/>• ESR &lt; 0.45Ω @ 100kHz<br/>• Holdup Time: &gt; 10 ms (Dropouts)"]:::capStyle
        HF_CAP["<b>HF CERAMIC BYPASS</b><br/>C_HF: 100nF / 630V X7R<br/>• Damps 65kHz Commutation Spikes<br/>• Low ESL / Ultra-Low ESR"]:::capStyle
        BLEEDER["<b>SAFETY BLEEDER STRING</b><br/>R_BLEED: 3x 330kΩ (1206) in Series<br/>• Total: 990 kΩ / 0.75W<br/>• Drains bulk cap to &lt; 50V SELV<br/>in &lt; 60s per IEC 62368-1"]:::bleederStyle
        HVDC_RAIL["<b>HIGH-VOLTAGE DC BUS</b><br/>+120V to +375V DC Bulk Rail<br/>Feeds Stage 3 Flyback Primary<br/>Ripple: &lt; 20V pk-pk @ full 72W"]:::outStyle

        IN_AC -->|Sinusoidal AC| GBU
        GBU -->|Rectified DC Pulses| BULK_CAP
        BULK_CAP --> HF_CAP
        BULK_CAP -.->|Parallel Discharge| BLEEDER
        HF_CAP --> HVDC_RAIL
    end
"""

fig5_dot = r"""digraph Figure5Stage2Rectifier {
    graph [
        rankdir=LR,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.35,
        ranksep=0.55,
        pad="0.25,0.25",
        splines=true
    ];

    node [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=9,
        shape=box,
        style="filled,rounded",
        margin="0.14,0.10",
        penwidth=1.5
    ];

    edge [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=8,
        penwidth=1.8,
        arrowsize=0.8
    ];

    subgraph cluster_rectifier {
        label = "STAGE 2: BRIDGE RECTIFIER & HIGH-VOLTAGE BULK DC SUBSYSTEM (HOT DOMAIN)";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#E65100";
        penwidth = 1.6;

        in_ac [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>FILTERED AC INPUT</b></td></tr>
                <tr><td><font color="#455A64">From Stage 1 EMI Filter</font></td></tr>
                <hr/>
                <tr><td align="left">• 85V – 265V AC RMS</td></tr>
                <tr><td align="left">• 47Hz – 63Hz Sinusoidal</td></tr>
            </table>>,
            fillcolor = "#ECEFF1",
            color = "#37474F"
        ];

        gbu [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>BRIDGE RECTIFIER</b></td></tr>
                <tr><td><font color="#D84315">BR1: GBU606</font></td></tr>
                <hr/>
                <tr><td align="left">• 600V PIV, 6.0A DC</td></tr>
                <tr><td align="left">• Glass Passivated</td></tr>
                <tr><td align="left">• Unipolar 100/120Hz DC</td></tr>
            </table>>,
            fillcolor = "#FFF3E0",
            color = "#E65100"
        ];

        bulk_cap [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>BULK CAPACITOR</b></td></tr>
                <tr><td><font color="#0277BD">C_BULK: 100µF / 450V</font></td></tr>
                <hr/>
                <tr><td align="left">• Nichicon 105°C Long-Life</td></tr>
                <tr><td align="left">• ESR &lt; 0.45Ω @ 100kHz</td></tr>
                <tr><td align="left">• Holdup Time &gt; 10 ms</td></tr>
            </table>>,
            fillcolor = "#E1F5FE",
            color = "#0277BD"
        ];

        hf_cap [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>HF DECOUPLING</b></td></tr>
                <tr><td><font color="#0277BD">100nF / 630V X7R</font></td></tr>
                <hr/>
                <tr><td align="left">• Shunts 65kHz edges</td></tr>
                <tr><td align="left">• Ultra-low ESL</td></tr>
            </table>>,
            fillcolor = "#E1F5FE",
            color = "#0277BD"
        ];

        bleeder [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>SAFETY BLEEDER</b></td></tr>
                <tr><td><font color="#B71C1C">3x 330kΩ Series (990kΩ)</font></td></tr>
                <hr/>
                <tr><td align="left">• Drains cap &lt; 50V in 60s</td></tr>
                <tr><td align="left">• IEC 62368-1 Compliant</td></tr>
                <tr><td align="left">• Total Power: 0.14W</td></tr>
            </table>>,
            fillcolor = "#FFEBEE",
            color = "#C62828"
        ];

        hvdc_out [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>HIGH-VOLTAGE DC RAIL</b></td></tr>
                <tr><td><font color="#1B5E20">+120V to +375V DC</font></td></tr>
                <hr/>
                <tr><td align="left">• Supplies Stage 3 Flyback</td></tr>
                <tr><td align="left">• Ripple &lt; 20V pk-pk</td></tr>
                <tr><td align="left">• 72W Peak Power Handling</td></tr>
            </table>>,
            fillcolor = "#E8F5E9",
            color = "#2E7D32"
        ];

        in_ac -> gbu [label=" Filtered AC"];
        gbu -> bulk_cap [label=" Rectified DC"];
        bulk_cap -> hf_cap;
        bulk_cap -> bleeder [label=" Parallel Bleed", style="dashed", color="#C62828"];
        hf_cap -> hvdc_out [label=" +HVDC Bus", color="#D84315", penwidth=2.2];
    }
}
"""

# ==============================================================================
# 6. FIGURE 6: STAGE 3 - UNIFORM-FREQUENCY ISOLATED FLYBACK SUBSYSTEM
# ==============================================================================
fig6_mmd = r"""flowchart LR
    classDef hvdcStyle fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#BF360C
    classDef ctrlStyle fill:#E1F5FE,stroke:#0277BD,stroke-width:2px,color:#01579B
    classDef fetStyle fill:#FFE0B2,stroke:#F57C00,stroke-width:2px,color:#E65100
    classDef isoStyle fill:#FFEBEE,stroke:#C62828,stroke-width:2px,stroke-dasharray: 5 5,color:#B71C1C
    classDef secStyle fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20
    classDef railStyle fill:#A5D6A7,stroke:#1B5E20,stroke-width:2px,color:#1B5E20

    subgraph STAGE3_FLYBACK ["STAGE 3: CONVERTER DC-DC (UNIFORM-FREQUENCY ISOLATED FLYBACK) SUBSYSTEM"]
        HVDC_IN["<b>+HVDC BUS IN</b><br/>+120V to +375V DC<br/>From Stage 2 Bulk Cap"]:::hvdcStyle
        
        subgraph PRIMARY_CIRCUIT ["PRIMARY CONTROL & SWITCHING CELL (GND_PRI)"]
            UC3843["<b>PWM CONTROLLER</b><br/>TI UC3843 / UCC28C43<br/>• Uniform 65 kHz Clock<br/>• RT=10kΩ, CT=2.2nF<br/>• Totem-Pole Gate Out<br/>• Cycle-by-Cycle ISENSE"]:::ctrlStyle
            Q1["<b>PRIMARY MOSFET</b><br/>STP10NK80Z / IPB80R290P7<br/>• 800V Superjunction N-FET<br/>• R_DS(on) = 0.29Ω<br/>• V_DS,peak = 599V (< 75% derated)"]:::fetStyle
            SNUBBER["<b>RCD CLAMP SNUBBER</b><br/>US1M (1kV, 75ns) +<br/>22.6kΩ (3W) + 1nF / 1kV<br/>• Clamps Leakage Spike &lt; 650V"]:::fetStyle
            R_SENSE["<b>PRIMARY CURRENT SHUNT</b><br/>R_CS: 0.25Ω / 2W Non-Inductive<br/>• Monitored at ISENSE Pin<br/>• Limits Peak Current to 2.96A"]:::fetStyle
            AUX_WIND["<b>AUXILIARY BIAS WINDING</b><br/>N_aux = 5T (0.25mm) + UF4004<br/>• Generates +14.0V DC Rail<br/>• Powers UC3843 VCC Pin"]:::ctrlStyle
        end

        subgraph TRANSFORMER_BARRIER ["⚡ REINFORCED ISOLATION BARRIER (IEC 62368-1)"]
            TX_PRI["<b>PRIMARY WINDING</b><br/>PQ26/20 Core (3C95 Ferrite)<br/>Np = 36T, Lp = 220µH ±10%<br/>B_max = 0.148T (B_sat=0.38T)"]:::isoStyle
            TX_SEC["<b>SECONDARY WINDING</b><br/>Ns = 6T (Furukawa TEX-E TIW)<br/>Turns Ratio Np:Ns = 6:1<br/>Certified 3000V RMS Withstand"]:::isoStyle
            OPTO["<b>FEEDBACK OPTOCOUPLER</b><br/>PC817 / EL817 Optocoupler<br/>5000V RMS Isolation Barrier"]:::isoStyle
        end

        subgraph SECONDARY_RECT ["SECONDARY RECTIFICATION & REGULATION (GND_SEC)"]
            SCHOTTKY["<b>SCHOTTKY RECTIFIER</b><br/>MBR10100 / MBR20100CT<br/>• 100V, 10A Barrier Diode<br/>• V_F = 0.60V @ 3A<br/>• Robust Passive Heatsink"]:::secStyle
            LC_FILT["<b>OUTPUT LC FILTER</b><br/>• 470µF / 35V Low-ESR Poly<br/>• 2.2µH Shielded Inductor<br/>• 22µF X7R MLCC Bypass<br/>• Ripple: &lt; 40mV pk-pk"]:::secStyle
            TL431["<b>CLOSED-LOOP REGULATION</b><br/>TI TL431 Precision Reference<br/>• 2.495V Internal Bandgap<br/>• Type-II Compensation Loop<br/>• Holds Bus within ±1.0%"]:::secStyle
        end

        BUS_24V["<b>+24.0V DC INTERMEDIATE BUS</b><br/>• +24.0V DC ± 1.0% Regulated<br/>• 72W Continuous Power (3.0A)<br/>• Supplies Stage 4 Buck-Boost"]:::railStyle

        HVDC_IN --> TX_PRI
        TX_PRI -->|Drain| Q1
        Q1 -.->|Leakage Clamp| SNUBBER
        Q1 -->|Source| R_SENSE
        R_SENSE -.->|ISENSE Pin| UC3843
        UC3843 -->|65kHz PWM Gate| Q1
        AUX_WIND -->|+14V VCC| UC3843

        TX_PRI ==>|Magnetic Coupling| TX_SEC
        TX_SEC -->|Switched AC Pulses| SCHOTTKY
        SCHOTTKY -->|Rectified DC| LC_FILT
        LC_FILT --> BUS_24V
        BUS_24V -->|Voltage Sense| TL431
        TL431 -->|Opto LED Drive| OPTO
        OPTO -.->|COMP Pin Pull-Down| UC3843
    end
"""

fig6_dot = r"""digraph Figure6Stage3Flyback {
    graph [
        rankdir=LR,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.35,
        ranksep=0.55,
        pad="0.25,0.25",
        splines=true
    ];

    node [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=9,
        shape=box,
        style="filled,rounded",
        margin="0.14,0.10",
        penwidth=1.5
    ];

    edge [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=8,
        penwidth=1.8,
        arrowsize=0.8
    ];

    hvdc_in [
        label = <<table border="0" cellborder="0" cellspacing="2">
            <tr><td><b>+HVDC BUS IN</b></td></tr>
            <tr><td><font color="#E65100">+120V to +375V DC</font></td></tr>
            <hr/>
            <tr><td align="left">• From Stage 2 Bulk Cap</td></tr>
            <tr><td align="left">• Feeds Primary Cell</td></tr>
        </table>>,
        fillcolor = "#FFF3E0",
        color = "#E65100"
    ];

    subgraph cluster_pri_flyback {
        label = "PRIMARY CONTROL & SWITCHING CELL (GND_PRI)";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#E65100";
        penwidth = 1.6;

        uc3843 [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>PWM CONTROLLER</b></td></tr>
                <tr><td><font color="#0277BD">UC3843 / UCC28C43</font></td></tr>
                <hr/>
                <tr><td align="left">• Uniform 65 kHz Clock</td></tr>
                <tr><td align="left">• RT = 10kΩ, CT = 2.2nF</td></tr>
                <tr><td align="left">• Totem-Pole Gate Out</td></tr>
                <tr><td align="left">• Cycle-by-cycle ISENSE</td></tr>
            </table>>,
            fillcolor = "#E1F5FE",
            color = "#0277BD"
        ];

        q1 [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>PRIMARY MOSFET</b></td></tr>
                <tr><td><font color="#E65100">STP10NK80Z / 800V</font></td></tr>
                <hr/>
                <tr><td align="left">• 800V Superjunction N-FET</td></tr>
                <tr><td align="left">• R_DS(on) = 0.29Ω</td></tr>
                <tr><td align="left">• V_DS,pk = 599V (&lt; 75%)</td></tr>
            </table>>,
            fillcolor = "#FFE0B2",
            color = "#E65100"
        ];

        snub [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>RCD SNUBBER CLAMP</b></td></tr>
                <tr><td><font color="#E65100">US1M + 22.6kΩ + 1nF</font></td></tr>
                <hr/>
                <tr><td align="left">• Clamps leakage spike</td></tr>
                <tr><td align="left">• V_clamp safely &lt; 650V</td></tr>
            </table>>,
            fillcolor = "#FFE0B2",
            color = "#E65100"
        ];

        rcs [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>CURRENT SHUNT</b></td></tr>
                <tr><td><font color="#E65100">R_CS: 0.25Ω / 2W</font></td></tr>
                <hr/>
                <tr><td align="left">• Peak current sense</td></tr>
                <tr><td align="left">• Limit = 2.96A peak</td></tr>
            </table>>,
            fillcolor = "#FFE0B2",
            color = "#E65100"
        ];

        aux [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>AUX BIAS WINDING</b></td></tr>
                <tr><td><font color="#0277BD">N_aux = 5T (+14V DC)</font></td></tr>
                <hr/>
                <tr><td align="left">• Sustains UC3843 VCC</td></tr>
                <tr><td align="left">• High-rel bootstrap</td></tr>
            </table>>,
            fillcolor = "#E1F5FE",
            color = "#0277BD"
        ];
    }

    subgraph cluster_trans_barrier {
        label = "⚡ REINFORCED ISOLATION BARRIER (IEC 62368-1)\n3000V RMS Dielectric Withstand | 6.4mm Creepage | 2.0mm Milled Slot";
        style = "filled,rounded,dashed";
        fillcolor = "#FFEBEE";
        color = "#C62828";
        penwidth = 1.8;

        tx_pri [label="Primary Winding\nPQ26/20 Core (3C95)\nNp=36T, Lp=220µH", fillcolor="#FFFFFF", color="#C62828"];
        tx_sec [label="Secondary Winding\nNs=6T (TEX-E TIW)\nTurns Ratio = 6:1", fillcolor="#FFFFFF", color="#C62828"];
        opto [label="Feedback Optocoupler\nPC817 / EL817 (5kV RMS)", fillcolor="#FFFFFF", color="#C62828"];
    }

    subgraph cluster_sec_flyback {
        label = "SECONDARY SCHOTTKY RECTIFICATION (GND_SEC)";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#2E7D32";
        penwidth = 1.6;

        mbr [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>SCHOTTKY RECTIFIER</b></td></tr>
                <tr><td><font color="#2E7D32">MBR10100 / 100V 10A</font></td></tr>
                <hr/>
                <tr><td align="left">• V_F = 0.60V @ 3A</td></tr>
                <tr><td align="left">• High-rel passive diode</td></tr>
                <tr><td align="left">• Heatsink mounted</td></tr>
            </table>>,
            fillcolor = "#E8F5E9",
            color = "#2E7D32"
        ];

        lc [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>LC OUTPUT FILTER</b></td></tr>
                <tr><td><font color="#2E7D32">470µF Poly + 2.2µH</font></td></tr>
                <hr/>
                <tr><td align="left">• Low ESR &lt; 15mΩ</td></tr>
                <tr><td align="left">• Attenuates 65kHz ripple</td></tr>
                <tr><td align="left">• Ripple &lt; 40mV pk-pk</td></tr>
            </table>>,
            fillcolor = "#E8F5E9",
            color = "#2E7D32"
        ];

        tl431 [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>SHUNT REGULATOR</b></td></tr>
                <tr><td><font color="#2E7D32">TI TL431 + Type-II Loop</font></td></tr>
                <hr/>
                <tr><td align="left">• 2.495V Reference</td></tr>
                <tr><td align="left">• 0.5% Accuracy</td></tr>
                <tr><td align="left">• Drives Opto Diode</td></tr>
            </table>>,
            fillcolor = "#E8F5E9",
            color = "#2E7D32"
        ];
    }

    bus_24v [
        label = <<table border="0" cellborder="0" cellspacing="2">
            <tr><td><b>+24.0V DC BUS</b></td></tr>
            <tr><td><font color="#1B5E20">Intermediate Rail (72W)</font></td></tr>
            <hr/>
            <tr><td align="left">• +24.0V DC ± 1.0%</td></tr>
            <tr><td align="left">• 3.0A Continuous (72W)</td></tr>
            <tr><td align="left">• Feeds Stage 4 Post-Reg</td></tr>
        </table>>,
        fillcolor = "#A5D6A7",
        color = "#1B5E20",
        penwidth = 2.0
    ];

    hvdc_in -> tx_pri [color="#E65100", penwidth=2.2];
    tx_pri -> q1 [label=" Drain", color="#E65100"];
    q1 -> snub [dir=both, style=dashed, color="#E65100"];
    q1 -> rcs [label=" Source", color="#E65100"];
    rcs -> uc3843 [label=" ISENSE", style=dashed, color="#0277BD"];
    uc3843 -> q1 [label=" 65kHz Gate", color="#0277BD"];
    aux -> uc3843 [label=" +14V VCC", color="#0277BD"];

    tx_pri -> tx_sec [label=" 6:1 Ratio", color="#C62828", style=bold];
    tx_sec -> mbr [label=" Secondary AC", color="#2E7D32", penwidth=2.0];
    mbr -> lc [label=" Rectified DC", color="#2E7D32", penwidth=2.0];
    lc -> bus_24v [label=" +24V Rail", color="#1B5E20", penwidth=2.2];
    bus_24v -> tl431 [label=" Sense", color="#2E7D32"];
    tl431 -> opto [label=" LED Drive", color="#C62828"];
    opto -> uc3843 [label=" COMP Pull-Down", color="#C62828"];
}
"""

# ==============================================================================
# 7. FIGURE 7: STAGE 4 - SYNCHRONOUS BUCK-BOOST POST-REGULATOR SUBSYSTEM
# ==============================================================================
fig7_mmd = r"""flowchart LR
    classDef inStyle fill:#A5D6A7,stroke:#1B5E20,stroke-width:2px,color:#1B5E20
    classDef ctrlStyle fill:#E0F7FA,stroke:#00838F,stroke-width:2px,color:#004D40
    classDef bridgeStyle fill:#B2EBF2,stroke:#00695C,stroke-width:2px,color:#004D40
    classDef dacStyle fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px,color:#4A148C
    classDef outStyle fill:#C8E6C9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20

    subgraph STAGE4_BUCKBOOST ["STAGE 4: 4-SWITCH SYNCHRONOUS BUCK-BOOST POST-REGULATOR SUBSYSTEM"]
        BUS_IN["<b>+24.0V DC BUS IN</b><br/>From Stage 3 Flyback Rail<br/>Stable 72W DC Power Source"]:::inStyle

        subgraph CONTROLLER_CELL ["CONTROLLER & GATE DRIVE ENGINE"]
            LM5176["<b>TI LM5176 CONTROLLER</b><br/>• 300 kHz Synchronous PWM<br/>• Integrated 4x Gate Drivers<br/>• Pure Buck Mode (5V - 18V)<br/>• Buck-Boost Mode (18V - 20V)<br/>• Built-in CSP/CSN Current Limit"]:::ctrlStyle
            COMP_NET["<b>TYPE-II COMPENSATION</b><br/>C_comp = 2.2nF, R_comp = 10kΩ<br/>Maintains 55° Phase Margin"]:::ctrlStyle
        end

        subgraph SWITCHING_H_BRIDGE ["SYNCHRONOUS 4-SWITCH H-BRIDGE & INDUCTOR"]
            QA_QB["<b>BUCK LEG (SW1)</b><br/>• QA: High-Side Buck FET<br/>• QB: Low-Side Buck Sync FET<br/>Infineon BSC034N04LS (40V, 3.4mΩ)"]:::bridgeStyle
            L_IND["<b>POWER INDUCTOR</b><br/>Wurth 7443321000 (WE-HCC)<br/>• 10.0 µH, 8.5A RMS, 11.5A Sat<br/>• Flat-Wire Low-Loss Core<br/>• DCR = 11.8 mΩ"]:::bridgeStyle
            QC_QD["<b>BOOST LEG (SW2)</b><br/>• QC: Low-Side Boost Sync FET<br/>• QD: High-Side Boost FET<br/>Infineon BSC034N04LS (40V, 3.4mΩ)"]:::bridgeStyle
        end

        subgraph OUTPUT_BANK ["OUTPUT FILTERING & HARDWARE PROTECTION"]
            OUT_CAPS["<b>OUTPUT CAPACITOR BANK</b><br/>• 4x 22µF / 25V X7R MLCCs<br/>• 1x 100µF / 25V OS-CON Poly<br/>• ESR &lt; 2.5 mΩ (Sub-25mV Ripple)"]:::outStyle
            SHUNT["<b>10mΩ KELVIN SENSE SHUNT</b><br/>Bourns CSS2H-2512R-L010F<br/>• 3W Metal Element, 0.1% Tol<br/>• Directly feeds LM5176 CSP/CSN<br/>• Cycle-by-cycle limit at 3.5A"]:::outStyle
        end

        subgraph PWM_VOLTAGE_CONTROL ["DIRECT PWM DUTY CYCLE VOLTAGE CONTROL"]
            PWM_IN["<b>DIRECT PWM MODULATION (D)</b><br/>STM32G474 HRTIM Engine<br/>Duty Cycle: D = V_OUT / 24V<br/>20.8% (5V) to 83.3% (20V)"]:::dacStyle
            RES_SUM["<b>PASSIVE VOLTAGE ATTENUATOR</b><br/>• R_FB1 = 49.9 kΩ (0.1%)<br/>• R_FB2 = 3.65 kΩ (0.1%)<br/>• Direct to MCU 12-Bit ADC<br/>• NO Voltage Steering / NO DAC Injection"]:::dacStyle
        end

        OUT_POSTS["<b>PROGRAMMABLE DC OUTPUT</b><br/>• 5.0V to 20.0V DC Programmable<br/>• 0.0A to 3.0A Continuous (60W)<br/>• Gold 4mm Binding Posts<br/>• Ripple: &lt; 25mV pk-pk @ 20MHz"]:::outStyle

        BUS_IN --> QA_QB
        LM5176 -->|Gate Drives SW1| QA_QB
        QA_QB --> L_IND
        L_IND --> QC_QD
        LM5176 -->|Gate Drives SW2| QC_QD
        QC_QD --> OUT_CAPS
        OUT_CAPS --> SHUNT
        SHUNT --> OUT_POSTS

        SHUNT -.->|CSP / CSN Kelvin Sense| LM5176
        OUT_POSTS -.->|V_OUT Sense| RES_SUM
        PWM_IN --> LM5176
        RES_SUM -->|V_SENSE to ADC| PWM_IN
        COMP_NET --- LM5176
    end
"""

fig7_dot = r"""digraph Figure7Stage4BuckBoost {
    graph [
        rankdir=LR,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.35,
        ranksep=0.55,
        pad="0.25,0.25",
        splines=true
    ];

    node [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=9,
        shape=box,
        style="filled,rounded",
        margin="0.14,0.10",
        penwidth=1.5
    ];

    edge [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=8,
        penwidth=1.8,
        arrowsize=0.8
    ];

    bus_in [
        label = <<table border="0" cellborder="0" cellspacing="2">
            <tr><td><b>+24.0V DC BUS IN</b></td></tr>
            <tr><td><font color="#1B5E20">From Stage 3 Flyback</font></td></tr>
            <hr/>
            <tr><td align="left">• +24.0V DC ± 1.0%</td></tr>
            <tr><td align="left">• 72W Power Source</td></tr>
        </table>>,
        fillcolor = "#A5D6A7",
        color = "#1B5E20"
    ];

    subgraph cluster_ctrl {
        label = "CONTROLLER & COMP (300 kHz)";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#00838F";
        penwidth = 1.6;

        lm5176 [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>TI LM5176 CONTROLLER</b></td></tr>
                <tr><td><font color="#00838F">4-Switch Synchronous PWM</font></td></tr>
                <hr/>
                <tr><td align="left">• Buck &amp; Buck-Boost</td></tr>
                <tr><td align="left">• 4x Integrated Drivers</td></tr>
                <tr><td align="left">• CSP/CSN OCP Clamp</td></tr>
            </table>>,
            fillcolor = "#E0F7FA",
            color = "#00838F"
        ];
    }

    subgraph cluster_hbridge {
        label = "4-SWITCH SYNCHRONOUS H-BRIDGE & INDUCTOR";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#00695C";
        penwidth = 1.6;

        qa_qb [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>BUCK LEG (SW1)</b></td></tr>
                <tr><td><font color="#004D40">QA (HS) &amp; QB (LS)</font></td></tr>
                <hr/>
                <tr><td align="left">• BSC034N04LS (40V)</td></tr>
                <tr><td align="left">• R_DS = 3.4mΩ</td></tr>
            </table>>,
            fillcolor = "#B2EBF2",
            color = "#00695C"
        ];

        ind [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>POWER INDUCTOR</b></td></tr>
                <tr><td><font color="#004D40">10.0 µH Flat-Wire</font></td></tr>
                <hr/>
                <tr><td align="left">• Wurth 7443321000</td></tr>
                <tr><td align="left">• I_sat = 11.5A, 8.5A RMS</td></tr>
                <tr><td align="left">• DCR = 11.8 mΩ</td></tr>
            </table>>,
            fillcolor = "#B2EBF2",
            color = "#00695C"
        ];

        qc_qd [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>BOOST LEG (SW2)</b></td></tr>
                <tr><td><font color="#004D40">QC (LS) &amp; QD (HS)</font></td></tr>
                <hr/>
                <tr><td align="left">• BSC034N04LS (40V)</td></tr>
                <tr><td align="left">• R_DS = 3.4mΩ</td></tr>
            </table>>,
            fillcolor = "#B2EBF2",
            color = "#00695C"
        ];
    }

    subgraph cluster_out_bank {
        label = "OUTPUT FILTER & CURRENT SENSING";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#2E7D32";
        penwidth = 1.6;

        out_caps [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>OUTPUT FILTER</b></td></tr>
                <tr><td><font color="#2E7D32">4x 22µF MLCC + 100µF Poly</font></td></tr>
                <hr/>
                <tr><td align="left">• ESR &lt; 2.5 mΩ</td></tr>
                <tr><td align="left">• Ripple &lt; 25mV pk-pk</td></tr>
            </table>>,
            fillcolor = "#C8E6C9",
            color = "#2E7D32"
        ];

        shunt [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>10mΩ KELVIN SHUNT</b></td></tr>
                <tr><td><font color="#B71C1C">Bourns CSS2H (3W, 0.1%)</font></td></tr>
                <hr/>
                <tr><td align="left">• Peak current sense</td></tr>
                <tr><td align="left">• Cycle-by-cycle trip</td></tr>
            </table>>,
            fillcolor = "#FFCDD2",
            color = "#B71C1C"
        ];
    }

    subgraph cluster_dac_sum {
        label = "DIRECT PWM DUTY CYCLE CONTROL";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#6A1B9A";
        penwidth = 1.6;

        dac_sum [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>DIRECT PWM VOLTAGE CONTROL</b></td></tr>
                <tr><td><font color="#6A1B9A">D = V_OUT / 24.0V (Duty Cycle)</font></td></tr>
                <hr/>
                <tr><td align="left">• 5.0V: D = 20.8%</td></tr>
                <tr><td align="left">• 12.0V: D = 50.0%</td></tr>
                <tr><td align="left">• 20.0V: D = 83.3%</td></tr>
                <tr><td align="left">• Passive divider R1/R2 to ADC</td></tr>
            </table>>,
            fillcolor = "#F3E5F5",
            color = "#6A1B9A"
        ];
    }

    out_rail [
        label = <<table border="0" cellborder="0" cellspacing="2">
            <tr><td><b>PROGRAMMABLE DC TERMINALS</b></td></tr>
            <tr><td><font color="#1B5E20">5.0V to 20.0V DC / 3.0A (60W)</font></td></tr>
            <hr/>
            <tr><td align="left">• Heavy-duty 4mm binding posts</td></tr>
            <tr><td align="left">• Sub-25mV ripple @ 20MHz</td></tr>
            <tr><td align="left">• Dynamic settling &lt; 150µs</td></tr>
        </table>>,
        fillcolor = "#A5D6A7",
        color = "#1B5E20",
        penwidth = 2.0
    ];

    bus_in -> qa_qb [color="#00695C", penwidth=2.2];
    lm5176 -> qa_qb [label=" SW1 Gates", color="#00838F"];
    qa_qb -> ind [label=" SW1 Node", color="#00695C", penwidth=2.2];
    ind -> qc_qd [label=" SW2 Node", color="#00695C", penwidth=2.2];
    lm5176 -> qc_qd [label=" SW2 Gates", color="#00838F"];
    qc_qd -> out_caps [label=" Filtered DC", color="#00695C", penwidth=2.2];
    out_caps -> shunt [color="#00695C", penwidth=2.2];
    shunt -> out_rail [color="#1B5E20", penwidth=2.5];

    shunt -> lm5176 [label=" CSP / CSN Kelvin Sense\n(Cycle-by-Cycle Peak OCP)", style="dashed", color="#B71C1C", penwidth=1.8];
    out_rail -> dac_sum [label=" V_OUT Sense", style="dashed", color="#6A1B9A"];
    dac_sum -> lm5176 [label=" V_FB (1.20V)", color="#6A1B9A"];
}
"""

# ==============================================================================
# 8. FIGURE 8: DUAL-DOMAIN POWER TELEMETRY & SENSING FRONTEND
# ==============================================================================
fig8_mmd = r"""flowchart TB
    classDef acStyle fill:#ECEFF1,stroke:#37474F,stroke-width:2px,color:#263238
    classDef isoStyle fill:#FFEBEE,stroke:#C62828,stroke-width:2px,stroke-dasharray: 5 5,color:#B71C1C
    classDef dcStyle fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20
    classDef mcuStyle fill:#E1F5FE,stroke:#0277BD,stroke-width:2px,color:#01579B
    classDef effStyle fill:#FFFDE7,stroke:#F57F17,stroke-width:2px,color:#E65100

    subgraph PRIMARY_AC_DOMAIN ["PRIMARY HIGH-VOLTAGE AC DOMAIN (HOT)"]
        AC_LINE["AC Mains Line & Neutral<br/>(85V - 265V AC RMS, 47-63 Hz)"]:::acStyle
        HV_DIV["Precision HV Resistor Divider<br/>4x 1MΩ (1206) + 2kΩ 0.1% Shunt<br/>(375Vpk → 187.5mVpk)"]:::acStyle
        CT_TOROID["Talema AC1005 Current Transformer<br/>1000:1 Ratio Toroidal Magnetic Isolation"]:::acStyle
        CT_BURDEN["Precision Burden Resistor<br/>100Ω 0.1% Metal Film (2mA → 200mV RMS)"]:::acStyle

        AC_LINE -->|Voltage Tap| HV_DIV
        AC_LINE -->|Current Primary Loop| CT_TOROID
        CT_TOROID -->|1000:1 Current| CT_BURDEN
    end

    subgraph REINFORCED_ISOLATION ["⚡ REINFORCED ISOLATION BARRIER (IEC 62368-1 / 5000V RMS)"]
        AMC1311["<b>TI AMC1311DWVR ISOLATED ΔΣ MODULATOR</b><br/>• Galvanic Isolation: 5000V RMS (1 min)<br/>• ±250mV Linear Differential Input<br/>• 20 MHz Digital Modulator Bitstream"]:::isoStyle
        HV_DIV -->|VINP, VINN| AMC1311
    end

    subgraph SECONDARY_DC_DOMAIN ["SECONDARY TOUCH-SAFE DC DOMAIN (SELV)"]
        DC_LOAD["Regulated DC Output Rail<br/>5.0V - 20.0V DC / 0.1A - 3.0A"]:::dcStyle
        INA226["<b>TI INA226 16-BIT I2C POWER MONITOR</b><br/>• 10mΩ 0.1% Low-Inductance Shunt<br/>• Shunt Voltage: 1.25µV / LSB<br/>• Bus Voltage: 1.25mV / LSB (±0.1% Acc)<br/>• Fast-Mode I2C Bus @ 400 kHz"]:::dcStyle

        DC_LOAD -->|Kelvin Sense| INA226
    end

    subgraph MCU_ENGINE ["CENTRAL MICROCONTROLLER (STM32G474RET6 @ 170 MHz)"]
        SINC3["<b>HARDWARE SINC3 DECIMATION FILTER</b><br/>Demodulates AMC1311 20MHz Bitstream<br/>Yields 16-Bit True v_ac(t) @ 20 kHz"]:::mcuStyle
        FAST_ADC["<b>12-BIT FAST ADC</b><br/>Samples CT_SIG i_ac(t) @ 10 kHz"]:::mcuStyle
        I2C_MASTER["<b>I2C MASTER PERIPHERAL</b><br/>Polls INA226 V_dc, I_dc, P_dc @ 10 Hz"]:::mcuStyle

        AMC1311 ==>|Digital Bitstream across barrier| SINC3
        CT_BURDEN -->|Analog AC Signal| FAST_ADC
        INA226 ==>|I2C Bus Data| I2C_MASTER

        subgraph EFFICIENCY_CORE ["REAL-TIME EFFICIENCY MATH ENGINE (10 Hz LOOP)"]
            PAC_CALC["<b>ACTIVE AC POWER</b><br/>P_ac = (1/N) Σ v_ac(t) · i_ac(t)<br/>True RMS Vac, Iac, Power Factor"]:::effStyle
            PDC_CALC["<b>TRUE DC POWER</b><br/>P_dc = V_out · I_out"]:::effStyle
            EFF_CALC["<b>SYSTEM EFFICIENCY (η)</b><br/>η = (P_dc / P_ac) × 100%<br/>Smoothed via 8-tap EMA Filter"]:::effStyle

            SINC3 --> PAC_CALC
            FAST_ADC --> PAC_CALC
            I2C_MASTER --> PDC_CALC
            PAC_CALC --> EFF_CALC
            PDC_CALC --> EFF_CALC
        end
    end

    EFF_CALC --> OLED["1.3\" OLED Display Dashboard<br/>Live V, I, P, ηReadouts"]:::effStyle
"""

fig8_dot = r"""digraph Figure8Telemetry {
    graph [
        rankdir=LR,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.35,
        ranksep=0.55,
        pad="0.25,0.25",
        splines=true
    ];

    node [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=9,
        shape=box,
        style="filled,rounded",
        margin="0.14,0.10",
        penwidth=1.5
    ];

    edge [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=8,
        penwidth=1.8,
        arrowsize=0.8
    ];

    subgraph cluster_pri_sense {
        label = "PRIMARY AC SENSING (HOT)";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#37474F";
        penwidth = 1.6;

        ac_line [label="AC Mains Line & Neutral\n85V - 265V AC RMS", fillcolor="#ECEFF1", color="#37474F"];
        hv_div [label="HV Resistor Divider\n4x 1MΩ + 2kΩ (0.1%)\n375Vpk -> 187.5mV", fillcolor="#ECEFF1", color="#37474F"];
        ct [label="Talema AC1005 CT\n1000:1 Toroidal Ratio", fillcolor="#ECEFF1", color="#37474F"];
        burden [label="Burden Resistor\n100Ω 0.1% (200mV RMS)", fillcolor="#ECEFF1", color="#37474F"];

        ac_line -> hv_div;
        ac_line -> ct;
        ct -> burden;
    }

    subgraph cluster_iso_sense {
        label = "⚡ REINFORCED BARRIER\n5000V RMS Withstand";
        style = "filled,rounded,dashed";
        fillcolor = "#FFEBEE";
        color = "#C62828";
        penwidth = 1.8;

        amc1311 [label="TI AMC1311 ΔΣ Modulator\n5kV RMS Galvanic Isolation\n20MHz Digital Bitstream", fillcolor="#FFFFFF", color="#C62828"];
        hv_div -> amc1311;
    }

    subgraph cluster_sec_sense {
        label = "SECONDARY DC LOAD SENSING (SELV)";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#2E7D32";
        penwidth = 1.6;

        ina226 [label="TI INA226 16-Bit Power Monitor\n10mΩ Shunt (1.25µV/LSB)\nBus Voltage (1.25mV/LSB)\nI2C Interface @ 400 kHz", fillcolor="#E8F5E9", color="#2E7D32"];
    }

    subgraph cluster_mcu_core {
        label = "STM32G474 MCU & REAL-TIME EFFICIENCY ENGINE";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#0277BD";
        penwidth = 1.6;

        sinc3 [label="Hardware Sinc3 Filter\nDemodulates v_ac(t) @ 20kHz", fillcolor="#E1F5FE", color="#0277BD"];
        fast_adc [label="Fast 12-Bit ADC\nSamples i_ac(t) @ 10kHz", fillcolor="#E1F5FE", color="#0277BD"];
        i2c_in [label="I2C Master Engine\nSamples V_dc, I_dc @ 10Hz", fillcolor="#E1F5FE", color="#0277BD"];
        eff_math [label="Efficiency Engine (10Hz)\nPac = (1/N) Σ v_ac · i_ac\nPdc = Vdc · Idc\nη = (Pdc / Pac) × 100%", fillcolor="#FFFDE7", color="#F57F17", penwidth=2.0];
        oled [label="1.3\" OLED Dashboard\nLive V, I, P, η Meters", fillcolor="#FFE0B2", color="#E65100"];

        amc1311 -> sinc3 [label=" Bitstream", color="#C62828", penwidth=2.0];
        burden -> fast_adc [label=" Analog i_ac", color="#37474F"];
        ina226 -> i2c_in [label=" I2C Data", color="#2E7D32"];

        sinc3 -> eff_math;
        fast_adc -> eff_math;
        i2c_in -> eff_math;
        eff_math -> oled [label=" 10 Hz GUI Refresh", color="#E65100"];
    }
}
"""

# ==============================================================================
# 9. FIGURE 9: AUXILIARY BIAS POWER RAIL DISTRIBUTION
# ==============================================================================
fig9_mmd = r"""flowchart TD
    classDef priStyle fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#BF360C
    classDef secBusStyle fill:#A5D6A7,stroke:#1B5E20,stroke-width:2px,color:#1B5E20
    classDef buckStyle fill:#E0F7FA,stroke:#00838F,stroke-width:2px,color:#004D40
    classDef ldoStyle fill:#E1F5FE,stroke:#0277BD,stroke-width:2px,color:#01579B
    classDef refStyle fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px,color:#4A148C

    subgraph AUX_DISTRIBUTION ["AUXILIARY BIAS POWER RAIL DISTRIBUTION SUBSYSTEM"]
        subgraph PRIMARY_HOT_AUX ["PRIMARY AUXILIARY DOMAIN (GND_PRI)"]
            TX_AUX["<b>FLYBACK AUXILIARY WINDING</b><br/>TX1_AUX: N_aux = 5T (0.25mm wire)<br/>UF4004 Fast Diode + 47µF Cap"]:::priStyle
            VCC_PRI["<b>+14.0V DC PRIMARY VCC RAIL</b><br/>Powers UC3843 PWM Controller (Pin 7)<br/>Sustained above 8.4V UVLO Threshold"]:::priStyle
            TX_AUX --> VCC_PRI
        end

        subgraph SECONDARY_COLD_AUX ["SECONDARY TOUCH-SAFE AUXILIARY DOMAIN (GND_SEC)"]
            BUS_24V["<b>+24.0V DC INTERMEDIATE RAIL</b><br/>72W Continuous Power Source<br/>Directly feeds LM5176 Controller VIN"]:::secBusStyle

            BUCK_5V["<b>SECONDARY STEP-DOWN BUCK</b><br/>TI TPS54202 Synchronous Buck<br/>• Input: +24V DC<br/>• Output: +5.0V DC ± 1.5% @ 2.0A<br/>• High Efficiency (> 92%)"]:::buckStyle

            LDO_3V3["<b>ULTRA-LOW-NOISE LOGIC LDO</b><br/>TI TPS7A25 LDO Regulator<br/>• Input: +5.0V DC<br/>• Output: +3.3V DC ± 1.0% @ 500mA<br/>• PSRR > 65 dB @ 100 kHz"]:::ldoStyle

            REF_3V0["<b>PRECISION ANALOG REFERENCE</b><br/>TI REF3030 Precision Reference<br/>• Output: +3.000V DC ± 0.2%<br/>• Drift: 20 ppm/°C<br/>• Ultra-low noise for ADC & DAC"]:::refStyle

            BUS_24V -->|Direct Rail| LM_VIN["TI LM5176 Internal Drivers<br/>Internal 7.5V LDO powers gates"]:::buckStyle
            BUS_24V -->|+24V In| BUCK_5V
            BUCK_5V -->|+5.0V Rail| OLED_PWR["1.3\" OLED Display VCC<br/>Current: ~40mA"]:::buckStyle
            BUCK_5V -->|+5.0V Rail| AMC_PWR["TI AMC1311 Secondary VDD2<br/>Current: ~15mA"]:::buckStyle
            BUCK_5V -->|+5.0V In| LDO_3V3
            LDO_3V3 -->|+3.3V Rail| MCU_PWR["STM32G474RET6 MCU Core<br/>Current: ~80mA @ 170MHz"]:::ldoStyle
            LDO_3V3 -->|+3.3V Rail| INA_PWR["TI INA226 Power Monitor VDD<br/>Current: ~1mA"]:::ldoStyle
            LDO_3V3 -->|+3.3V In| REF_3V0
            REF_3V0 -->|+3.000V VREF| VREF_MCU["STM32 VDDA / VREF+ Pins<br/>Calibrated ADC / DAC Reference"]:::refStyle
        end
    end
"""

fig9_dot = r"""digraph Figure9AuxPower {
    graph [
        rankdir=TB,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.35,
        ranksep=0.45,
        pad="0.25,0.25"
    ];

    node [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=9,
        shape=box,
        style="filled,rounded",
        margin="0.14,0.10",
        penwidth=1.5
    ];

    edge [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=8,
        penwidth=1.8,
        arrowsize=0.8
    ];

    subgraph cluster_pri_aux {
        label = "PRIMARY AUXILIARY DOMAIN (GND_PRI)";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#E65100";
        penwidth = 1.6;

        aux_wind [label="Transformer Aux Winding\nN_aux = 5T (0.25mm) + UF4004", fillcolor="#FFE0B2", color="#E65100"];
        vcc_pri [label="+14.0V DC Primary VCC Rail\nPowers UC3843 PWM Controller", fillcolor="#FFE0B2", color="#E65100"];
        aux_wind -> vcc_pri;
    }

    subgraph cluster_sec_aux {
        label = "SECONDARY TOUCH-SAFE AUXILIARY DOMAIN (GND_SEC)";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#2E7D32";
        penwidth = 1.6;

        bus_24v [label="+24.0V DC Intermediate Rail (72W)\nDirectly powers LM5176 VIN", fillcolor="#A5D6A7", color="#1B5E20", penwidth=2.0];
        buck_5v [label="TI TPS54202 Synchronous Buck\n+24V -> +5.0V DC / 2.0A (> 92% eff)", fillcolor="#E0F7FA", color="#00838F"];
        ldo_3v3 [label="TI TPS7A25 Low-Noise LDO\n+5.0V -> +3.3V DC / 500mA (PSRR > 65dB)", fillcolor="#E1F5FE", color="#0277BD"];
        ref_3v0 [label="TI REF3030 Precision Reference\n+3.000V DC ± 0.2% (20 ppm/°C)", fillcolor="#F3E5F5", color="#6A1B9A"];

        oled [label="1.3\" OLED Display VCC (+5V, 40mA)", fillcolor="#ECEFF1", color="#37474F"];
        amc [label="AMC1311 Secondary VDD2 (+5V, 15mA)", fillcolor="#ECEFF1", color="#37474F"];
        mcu [label="STM32G474RET6 MCU Core (+3.3V, 80mA)", fillcolor="#ECEFF1", color="#37474F"];
        ina [label="TI INA226 Power Monitor (+3.3V, 1mA)", fillcolor="#ECEFF1", color="#37474F"];
        vref_mcu [label="MCU VDDA / VREF+ Pins (+3.000V Calibrated)", fillcolor="#ECEFF1", color="#37474F"];

        bus_24v -> buck_5v [label=" +24V Bus"];
        buck_5v -> oled [label=" +5.0V"];
        buck_5v -> amc [label=" +5.0V"];
        buck_5v -> ldo_3v3 [label=" +5.0V"];
        ldo_3v3 -> mcu [label=" +3.3V"];
        ldo_3v3 -> ina [label=" +3.3V"];
        ldo_3v3 -> ref_3v0 [label=" +3.3V"];
        ref_3v0 -> vref_mcu [label=" +3.000V VREF"];
    }
}
"""

# ==============================================================================
# 10. FIGURE 10: MASTER SYSTEM HARDWARE ARCHITECTURE BLOCK DIAGRAM
# ==============================================================================
fig10_mmd = r"""flowchart LR
    classDef acStyle fill:#ECEFF1,stroke:#37474F,stroke-width:2px,color:#263238
    classDef priStyle fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#BF360C
    classDef isoStyle fill:#FFEBEE,stroke:#C62828,stroke-width:2px,stroke-dasharray: 5 5,color:#B71C1C
    classDef secPwrStyle fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20
    classDef bbStyle fill:#E0F7FA,stroke:#00838F,stroke-width:2px,color:#004D40
    classDef ctrlStyle fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px,color:#4A148C
    classDef mcuStyle fill:#E1F5FE,stroke:#0277BD,stroke-width:2px,color:#01579B
    classDef uiStyle fill:#FBE9E7,stroke:#D84315,stroke-width:2px,color:#BF360C

    subgraph AC_FRONTEND ["STAGE 1 & 2: MAINS FRONTEND & BULK DC (HOT DOMAIN)"]
        AC_IN["AC Mains Grid Input<br/>85V - 265V AC RMS (IEC C14)"]:::acStyle
        FUSE_NTC["Input Protection<br/>• 2A Ceramic Fuse<br/>• 10Ω NTC Limiter<br/>• 300V MOV Surge Clamp"]:::acStyle
        EMI_FILT["2-Stage EMI Filter<br/>• L_CM1: 15mH, L_CM2: 4.7mH<br/>• 3x X2 Film + 2x Y2 Caps"]:::acStyle
        RECT_BULK["Bridge & Bulk DC Bus<br/>• BR1: GBU606 (600V, 6A)<br/>• 100µF / 450V Bulk Cap<br/>Bus: +120V to +375V DC"]:::acStyle

        AC_IN --> FUSE_NTC
        FUSE_NTC --> EMI_FILT
        EMI_FILT --> RECT_BULK
    end

    subgraph STAGE3_PRIMARY ["STAGE 3: UNIFORM-FREQ FLYBACK (GND_PRI)"]
        TX_PRI["Flyback Primary<br/>PQ26/20 Core (3C95)<br/>Np=36T, Lp=220µH"]:::priStyle
        Q1_FET["Primary FET Q1<br/>STP10NK80Z (800V, 0.29Ω)"]:::priStyle
        SNUBBER["RCD Clamp Snubber<br/>US1M + 22.6kΩ + 1nF"]:::priStyle
        PWM_CTRL["UC3843 Controller<br/>Uniform 65kHz Fixed Clock<br/>Cycle-by-cycle ISENSE"]:::priStyle

        RECT_BULK --> TX_PRI
        TX_PRI --> Q1_FET
        Q1_FET -.-> SNUBBER
        PWM_CTRL --> Q1_FET
    end

    subgraph ISO_BARRIER ["⚡ REINFORCED ISOLATION BARRIER (IEC 62368-1 / 3000V RMS)"]
        ISO_TX["PQ26/20 TIW Secondary (6T)<br/>3000V RMS Galvanic Barrier"]:::isoStyle
        ISO_OPTO["PC817 Optocoupler<br/>5000V RMS Voltage Feedback"]:::isoStyle
        ISO_AMC["TI AMC1311 ΔΣ Modulator<br/>5000V RMS AC Voltage Sense"]:::isoStyle
        ISO_CT["Talema AC1005 (1000:1 CT)<br/>Galvanic AC Current Sense"]:::isoStyle
    end

    subgraph STAGE3_SECONDARY ["STAGE 3: SCHOTTKY RECTIFICATION (SELV)"]
        SCHOTTKY["Schottky Rectifier<br/>MBR10100 (100V, 10A) + Heatsink"]:::secPwrStyle
        BUS_24V["+24.0V Intermediate Bus<br/>Stable 72W DC Rail (±1.0%)"]:::secPwrStyle
        TL431["TL431 Precision Shunt<br/>2.495V Ref + Opto Drive"]:::secPwrStyle

        TX_PRI ==> ISO_TX
        ISO_TX --> SCHOTTKY
        SCHOTTKY --> BUS_24V
        BUS_24V --> TL431
        TL431 --> ISO_OPTO
        ISO_OPTO -.-> PWM_CTRL
    end

    subgraph STAGE4_BUCKBOOST ["STAGE 4: SYNCHRONOUS BUCK-BOOST POST-REGULATOR"]
        LM5176["TI LM5176 Controller<br/>300 kHz Synchronous PWM<br/>4x Gate Drivers Inside"]:::bbStyle
        H_BRIDGE["4-Switch Synchronous H-Bridge<br/>4x 40V BSC034N04LS MOSFETs<br/>+ 10µH Flat-Wire Inductor"]:::bbStyle
        OUT_STAGE["Output LC Filter Bank<br/>4x 22µF MLCC + 100µF Poly<br/>10mΩ Kelvin Sense Shunt"]:::bbStyle
        DC_OUT["Programmable DC Terminals<br/>5.0V - 20.0V DC / 3.0A (60W)<br/>Sub-25mV Ripple | 4mm Posts"]:::bbStyle

        BUS_24V --> H_BRIDGE
        LM5176 --> H_BRIDGE
        H_BRIDGE --> OUT_STAGE
        OUT_STAGE --> DC_OUT
        OUT_STAGE -.->|CSP / CSN OCP| LM5176
    end

    subgraph VOLT_SENSE ["PASSIVE VOLTAGE SENSING"]
        RES_DIV["Passive Attenuator<br/>R1: 49.9k, R2: 3.65k<br/>Direct to MCU ADC"]:::ctrlStyle
        DC_OUT -.-> RES_DIV
        RES_DIV --> STM32
    end

    subgraph MCU_CORE ["CENTRAL EMBEDDED CONTROLLER"]
        STM32["STM32G474RET6 MCU (170 MHz)<br/>• Sinc3 Demodulator (AMC1311)<br/>• Fast 12-Bit ADCs & DAC<br/>• Real-Time Efficiency Engine (10Hz)"]:::mcuStyle
        INA226["TI INA226 Power Monitor<br/>16-Bit I2C DC Bus & Shunt"]:::secPwrStyle

        ISO_AMC ==> STM32
        ISO_CT --> STM32
        OUT_STAGE -.-> INA226
        INA226 ==> STM32
        STM32 -->|Direct PWM (D)| LM5176
        STM32 -->|ENABLE Pin| LM5176
    end

    subgraph HMI_UI ["USER INTERFACE & MONITORING"]
        OLED["1.3\" I2C OLED Dashboard<br/>Live V, I, P, η Meters"]:::uiStyle
        CONTROLS["Dual Rotary Encoders<br/>Tactile Output Enable Switch"]:::uiStyle
        LEDS["Front-Panel Status LEDs<br/>Green (CV), Amber (Limit), Red (Fault)"]:::uiStyle

        STM32 ==> OLED
        CONTROLS ==> STM32
        STM32 ==> LEDS
    end
"""

# Figure 10 DOT code
fig10_dot = r"""digraph Figure10MasterArchitecture {
    graph [
        rankdir=LR,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=13,
        nodesep=0.35,
        ranksep=0.55,
        pad="0.25,0.25",
        splines=true
    ];

    node [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=8.5,
        shape=box,
        style="filled,rounded",
        margin="0.12,0.08",
        penwidth=1.4
    ];

    edge [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=7.5,
        penwidth=1.8,
        arrowsize=0.75
    ];

    subgraph cluster_mains_frontend {
        label = "STAGE 1 & 2: MAINS AC FRONTEND & BULK DC (HOT DOMAIN)";
        style = "filled,rounded";
        fillcolor = "#F0F4F8";
        color = "#37474F";
        penwidth = 1.6;

        ac_in [label="AC Grid Input\n85V - 265V AC\n47 - 63 Hz (C14)", fillcolor="#CFD8DC", color="#263238"];
        ac_prot [label="Input Protection\n2A Fuse, 10Ω NTC\n300V MOV Clamp", fillcolor="#FFFFFF", color="#455A64"];
        ac_emi [label="2-Stage EMI Filter\n15mH + 4.7mH Chokes\n3x X2 + 2x Y2 Caps", fillcolor="#FFFFFF", color="#455A64"];
        ac_rect [label="Bridge & Bulk DC\nGBU606 (600V, 6A)\n100µF/450V Bulk Cap\n+120V to +375V DC", fillcolor="#FFFFFF", color="#455A64"];

        ac_in -> ac_prot;
        ac_prot -> ac_emi;
        ac_emi -> ac_rect;
    }

    subgraph cluster_pri_flyback {
        label = "STAGE 3: UNIFORM-FREQ FLYBACK (GND_PRI)";
        style = "filled,rounded";
        fillcolor = "#FFF3E0";
        color = "#E65100";
        penwidth = 1.6;

        tx_pri [label="Transformer Primary\nPQ26/20 (3C95 Ferrite)\nNp = 36T, Lp = 220µH", fillcolor="#FFE0B2", color="#E65100"];
        snubber [label="RCD Snubber Clamp\nUS1M + 22.6kΩ + 1nF", fillcolor="#FFFFFF", color="#F57C00"];
        pri_fet [label="STP10NK80Z N-FET\n800V, 0.29Ω D2PAK", fillcolor="#FFFFFF", color="#E65100"];
        pri_ctrl [label="UC3843 PWM Controller\nUniform 65kHz Fixed Clock\nCycle-by-cycle ISENSE", fillcolor="#FFFFFF", color="#E65100"];

        ac_rect -> tx_pri [label=" +HVDC", color="#D84315", penwidth=2.2];
        tx_pri -> pri_fet [label=" Drain"];
        pri_fet -> snubber [dir=both, style=dashed];
        pri_ctrl -> pri_fet [label=" 65kHz Gate"];
    }

    subgraph cluster_barrier {
        label = "⚡ REINFORCED ISOLATION BARRIER (IEC 62368-1)\nCreepage ≥ 6.4mm | Milled Slot 2.0mm | 3000V RMS Withstand";
        style = "filled,rounded,dashed";
        fillcolor = "#FFEBEE";
        color = "#C62828";
        penwidth = 1.8;

        tx_sec [label="Secondary Winding\nNs = 6T (TEX-E TIW)\n3000V RMS Barrier", fillcolor="#FFFFFF", color="#C62828"];
        iso_opto [label="Feedback Optocoupler\nPC817 (5kV RMS)", fillcolor="#FFFFFF", color="#C62828"];
        iso_amc [label="AC Voltage Sensor\nTI AMC1311 (5kV RMS)", fillcolor="#FFFFFF", color="#C62828"];
        iso_ct [label="AC Current Sensor\nTalema CT (1000:1)", fillcolor="#FFFFFF", color="#C62828"];
    }

    subgraph cluster_sec_flyback {
        label = "STAGE 3: SCHOTTKY RECTIFICATION (SELV)";
        style = "filled,rounded";
        fillcolor = "#E8F5E9";
        color = "#2E7D32";
        penwidth = 1.6;

        mbr [label="Schottky Rectifier\nMBR10100 (100V, 10A)\nPassive TO-220 Heatsink", fillcolor="#FFFFFF", color="#2E7D32"];
        bus_24v [label="+24.0V Intermediate Bus\nRegulated 24V / 72W\nRipple < 40mV pk-pk", fillcolor="#A5D6A7", color="#1B5E20", penwidth=2.0];
        tl431 [label="TL431 Shunt Regulator\n2.495V Bandgap Ref", fillcolor="#FFFFFF", color="#2E7D32"];

        tx_sec -> mbr;
        mbr -> bus_24v [label=" +24V DC", color="#2E7D32", penwidth=2.0];
        bus_24v -> tl431;
        tl431 -> iso_opto;
        iso_opto -> pri_ctrl [label=" COMP Pull-Down", color="#C62828"];
    }

    subgraph cluster_buck_boost {
        label = "STAGE 4: SYNCHRONOUS BUCK-BOOST POST-REGULATOR";
        style = "filled,rounded";
        fillcolor = "#E0F7FA";
        color = "#00838F";
        penwidth = 1.6;

        bb_ctrl [label="TI LM5176 Controller\n300 kHz Synchronous PWM\n4x Integrated Gate Drivers", fillcolor="#FFFFFF", color="#00838F"];
        h_bridge [label="4-Switch H-Bridge\n4x 40V BSC034N04LS\n10µH Flat-Wire Inductor", fillcolor="#B2EBF2", color="#00838F"];
        dc_shunt [label="10mΩ Kelvin Shunt\nBourns CSS2H (3W, 0.1%)", fillcolor="#FFFFFF", color="#00838F"];
        dc_terminals [label="Programmable DC Output\n5.0V - 20.0V DC / 3.0A (60W)\nRipple < 25mV | 4mm Posts", fillcolor="#80CBC4", color="#004D40", penwidth=2.2];

        bus_24v -> h_bridge [label=" +24V Bus", color="#00695C", penwidth=2.0];
        bb_ctrl -> h_bridge;
        h_bridge -> dc_shunt;
        dc_shunt -> dc_terminals [color="#004D40", penwidth=2.2];
        dc_shunt -> bb_ctrl [label=" CSP/CSN OCP", color="#C62828", style=dashed];
    }

    subgraph cluster_control_dac {
        label = "DAC VOLTAGE STEERING NETWORK";
        style = "filled,rounded";
        fillcolor = "#F3E5F5";
        color = "#6A1B9A";
        penwidth = 1.6;

        dac_sum [label="Summing Junction\nR_top = 49.9k, R_bot = 3.65k\nR_DAC = 11.0k (0.1% Tol)\n10 mV Step Resolution", fillcolor="#FFFFFF", color="#6A1B9A"];
        dc_terminals -> dac_sum [label=" V_OUT Sense", style=dashed];
        dac_sum -> bb_ctrl [label=" V_FB (1.20V Ref)"];
    }

    subgraph cluster_mcu_telemetry {
        label = "CENTRAL EMBEDDED CONTROLLER & TELEMETRY";
        style = "filled,rounded";
        fillcolor = "#E1F5FE";
        color = "#0277BD";
        penwidth = 1.8;

        mcu [label="STM32G474RET6 MCU (170 MHz)\n• Hardware Sinc3 Decimation Filter\n• Fast 12-Bit DAC & ADCs\n• Real-Time Efficiency Engine (10Hz)", fillcolor="#B3E5FC", color="#01579B", penwidth=2.0];
        ina226 [label="TI INA226 Power Monitor\n16-Bit I2C ADC (10Hz)", fillcolor="#FFFFFF", color="#0277BD"];
        oled [label="1.3\" OLED Display Dashboard\nLive V, I, P, ηReadouts", fillcolor="#FFFFFF", color="#D84315"];

        iso_amc -> mcu [label=" Sinc3 Bitstream", color="#C62828"];
        iso_ct -> mcu [label=" Analog i_ac"];
        dc_shunt -> ina226;
        ina226 -> mcu [label=" I2C (400kHz)"];
        mcu -> dac_sum [label=" 12-Bit V_DAC", color="#6A1B9A", penwidth=1.8];
        mcu -> bb_ctrl [label=" ENABLE Pin", color="#00838F"];
        mcu -> oled [label=" I2C Dashboard", color="#D84315"];
    }

    ac_emi -> iso_amc [label=" AC Voltage Tap", style=dashed];
    ac_prot -> iso_ct [label=" AC Current Loop", style=dashed];
    tx_pri -> tx_sec [color="#C62828", style=bold, penwidth=2.5];
}
"""

# ==============================================================================
# 11. FIGURE 11: MCU SYSTEM INTERACTION & STATE MACHINE
# ==============================================================================
fig11_mmd = r"""flowchart TD
    classDef initStyle fill:#ECEFF1,stroke:#37474F,stroke-width:2px,color:#263238
    classDef standStyle fill:#FFFDE7,stroke:#F57F17,stroke-width:2px,color:#E65100
    classDef runStyle fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20
    classDef warnStyle fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#BF360C
    classDef faultStyle fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#B71C1C

    subgraph MCU_STATE_MACHINE ["STM32G474 FIRMWARE OPERATING STATE MACHINE"]
        STATE_INIT["<b>STATE 0: SYSTEM INITIALIZATION</b><br/>• Clock setup @ 170 MHz, Sinc3 Init<br/>• Self-test peripherals (INA226, OLED, DAC)<br/>• Read factory calibration coefficients<br/>• Set LM5176 ENABLE pin LOW"]:::initStyle

        STATE_STANDBY["<b>STATE 1: STANDBY / IDLE MODE</b><br/>• +24V Intermediate bus active<br/>• Output disabled (LM5176 ENABLE = LOW)<br/>• OLED displays 'STANDBY: Press Enable'<br/>• Standby power &lt; 150 mW<br/>• Mode LED: Amber Flashing"]:::standStyle

        STATE_RAMP["<b>STATE 2: SOFT-START VOLTAGE RAMP</b><br/>• Operator presses Enable button or SCPI :OUTP ON<br/>• MCU steps 12-bit DAC smoothly to target setpoint<br/>• Enables LM5176 post-regulator<br/>• Inrush slew controlled (dV/dt &lt; 1V/ms)"]:::runStyle

        STATE_CV["<b>STATE 3: ACTIVE REGULATION (CV MODE)</b><br/>• LM5176 regulates V_OUT within ±0.2%<br/>• Mode LED: Solid Green<br/>• 10 Hz Telemetry Loop active<br/>• OLED displays live V_out, I_load, P_out, η"]:::runStyle

        STATE_LIMIT["<b>STATE 4: AUTONOMOUS CURRENT LIMIT</b><br/>• Load current exceeds programmed limit<br/>• LM5176 cycle-by-cycle CSP/CSN clamps peak current<br/>• Output voltage folds back<br/>• Mode LED: Solid Amber (Limit Active)<br/>• MCU starts 500 ms persistent timer"]:::warnStyle

        STATE_FAULT["<b>STATE 5: SUPERVISORY FAULT SHUTDOWN</b><br/>• Triggered if overload &gt; 500ms or OTP &gt; 85°C<br/>• MCU drives LM5176 ENABLE pin LOW<br/>• Output disconnected within 2 ms<br/>• Mode LED: Solid Red (Fault)<br/>• OLED displays fault diagnostics"]:::faultStyle

        STATE_INIT -->|Self-Test Passed| STATE_STANDBY
        STATE_STANDBY -->|Enable Event| STATE_RAMP
        STATE_RAMP -->|Target Voltage Reached| STATE_CV
        STATE_CV -->|Output Disable Button / SCPI| STATE_STANDBY
        STATE_CV -->|Overload Step (I &gt; 3.0A)| STATE_LIMIT
        STATE_LIMIT -->|Overload Cleared (&lt; 500ms)| STATE_CV
        STATE_LIMIT -->|Persistent Short (&gt; 500ms)| STATE_FAULT
        STATE_CV -->|Overtemperature / OTP| STATE_FAULT
        STATE_FAULT -->|User Clears Fault / Presses Reset| STATE_STANDBY
    end
"""

fig11_dot = r"""digraph Figure11MCUStateMachine {
    graph [
        rankdir=TB,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.40,
        ranksep=0.50,
        pad="0.25,0.25"
    ];

    node [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=9.5,
        shape=box,
        style="filled,rounded",
        margin="0.16,0.12",
        penwidth=1.6
    ];

    edge [
        fontname="Helvetica, Arial, sans-serif",
        fontsize=8.5,
        penwidth=1.8,
        arrowsize=0.8
    ];

    s0 [label="STATE 0: INITIALIZATION & SELF-TEST\n• 170MHz Clock, Sinc3 & ADC setup\n• Verify I2C INA226 & OLED\n• Zero DAC, LM5176 ENABLE = LOW", fillcolor="#ECEFF1", color="#37474F"];
    s1 [label="STATE 1: STANDBY / IDLE MODE\n• +24V Intermediate rail sustained\n• LM5176 ENABLE = LOW (Output Off)\n• Standby power < 150 mW\n• Amber LED blinking", fillcolor="#FFFDE7", color="#F57F17"];
    s2 [label="STATE 2: SOFT-START VOLTAGE RAMP\n• Enable pressed / SCPI :OUTP ON\n• 12-Bit DAC slews to target\n• LM5176 ENABLE driven HIGH\n• Slew rate dV/dt < 1V/ms", fillcolor="#E1F5FE", color="#0277BD"];
    s3 [label="STATE 3: ACTIVE REGULATION (CV MODE)\n• V_OUT maintained ±0.2%\n• Solid Green LED\n• 10 Hz Telemetry Loop running\n• Live OLED Dashboard update", fillcolor="#E8F5E9", color="#2E7D32"];
    s4 [label="STATE 4: AUTONOMOUS CURRENT LIMIT\n• LM5176 CSP/CSN clamps peak current\n• Solid Amber LED (Limit active)\n• V_OUT folds back to maintain current\n• 500 ms supervisory timer runs", fillcolor="#FFF3E0", color="#E65100"];
    s5 [label="STATE 5: SUPERVISORY FAULT SHUTDOWN\n• Overload > 500ms or OTP > 85°C\n• MCU drives LM5176 ENABLE LOW\n• Solid Red Fault LED\n• OLED diagnostic alert", fillcolor="#FFEBEE", color="#C62828"];

    s0 -> s1 [label=" POST Passed"];
    s1 -> s2 [label=" Enable Command"];
    s2 -> s3 [label=" V_OUT Reached"];
    s3 -> s1 [label=" Disable Command"];
    s3 -> s4 [label=" Overload Event (I > 3A)"];
    s4 -> s3 [label=" Overload Cleared (< 500ms)", color="#2E7D32"];
    s4 -> s5 [label=" Fault Persistent (> 500ms)", color="#C62828"];
    s3 -> s5 [label=" Thermal OTP Event", color="#C62828"];
    s5 -> s1 [label=" Fault Cleared & Reset", color="#37474F"];
}
"""

all_diagrams = [
    ("figure1_simplified_4stage_power_flow", fig1_mmd, fig1_dot),
    ("figure2_usecase_cv_dynamic_response", fig2_mmd, fig2_dot),
    ("figure3_usecase_ocp_cycle_by_cycle", fig3_mmd, fig3_dot),
    ("figure4_inside_stage1_mains_emi", fig4_mmd, fig4_dot),
    ("figure5_inside_stage2_rectifier_bulk", fig5_mmd, fig5_dot),
    ("figure6_inside_stage3_flyback", fig6_mmd, fig6_dot),
    ("figure7_inside_stage4_buck_boost", fig7_mmd, fig7_dot),
    ("figure8_telemetry_sensing_frontend", fig8_mmd, fig8_dot),
    ("figure9_aux_power_distribution", fig9_mmd, fig9_dot),
    ("figure10_master_hardware_architecture", fig10_mmd, fig10_dot),
    ("figure11_mcu_system_interaction_monitoring", fig11_mmd, fig11_dot)
]

def main():
    print("=" * 70)
    print("Generating all 11 PRD Architectural Diagrams (Mermaid, DOT, PNG, SVG)")
    print("=" * 70)

    for name, mmd_code, dot_code in all_diagrams:
        mmd_path = os.path.join(MMD_DIR, f"{name}.mmd")
        with open(mmd_path, "w", encoding="utf-8") as f:
            f.write(mmd_code.strip() + "\n")
        print(f"Saved Mermaid: {mmd_path}")

        dot_path = os.path.join(DIAG_DIR, f"{name}.dot")
        with open(dot_path, "w", encoding="utf-8") as f:
            f.write(dot_code.strip() + "\n")
        print(f"Saved DOT:     {dot_path}")

        png_path = os.path.join(DIAG_DIR, f"{name}.png")
        svg_path = os.path.join(DIAG_DIR, f"{name}.svg")

        try:
            subprocess.run(["dot", "-Gdpi=150", "-Tpng", dot_path, "-o", png_path], check=True)
            subprocess.run(["dot", "-Tsvg", dot_path, "-o", svg_path], check=True)
            print(f"Rendered:      {png_path} and {svg_path}")
        except Exception as e:
            print(f"ERROR rendering {name}: {e}")

    # Generate a Mermaid README.md catalog
    readme_path = os.path.join(MMD_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# Mermaid Architectural Diagram Catalog\n\n")
        f.write("This directory contains the standalone Mermaid (`.mmd`) source files for all 11 architectural diagrams ")
        f.write("referenced in the Smart Programmable Power Supply (VVDN_SPPS_2026) PRD.\n\n")
        f.write("| Diagram File | Description | Rendered Image Link |\n")
        f.write("| :--- | :--- | :--- |\n")
        for name, _, _ in all_diagrams:
            title = name.replace("_", " ").title()
            f.write(f"| [{name}.mmd](file://{os.path.abspath(os.path.join(MMD_DIR, name + '.mmd'))}) | {title} | [PNG](file://{os.path.abspath(os.path.join(DIAG_DIR, name + '.png'))}) / [SVG](file://{os.path.abspath(os.path.join(DIAG_DIR, name + '.svg'))}) |\n")
    print(f"Saved Mermaid README catalog: {readme_path}")
    print("\nAll 11 diagrams generated successfully!")

if __name__ == "__main__":
    main()
