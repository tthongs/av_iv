#!/usr/bin/env python3
"""
Generate internal sub-block diagrams for each of the 4 stages of the Smart Programmable Power Supply:
1. Stage 1: Mains Supply Subsystem (AC Inlet, Fuse, NTC, MOV, 2-Stage EMI Filter)
2. Stage 2: Rectifier & Bulk Stage Subsystem (GBU606 Bridge, 100µF/450V Bulk, Bleeder, Decoupling)
3. Stage 3: Converter DC-DC (Uniform-Frequency Isolated Flyback) Subsystem (Fixed 65kHz UC3843, 800V FET, PQ26/20 3kV Iso, Schottky Rec, +24V Bus)
4. Stage 4: Final Stage (Buck-Boost Post-Regulator & Output) Subsystem (LM5176, 4-Switch H-Bridge, 10µH Inductor, DAC Steering, <5µs CC Clamp)
"""

import subprocess
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

diagrams = {
    "diagram_inside_stage1_mains": r"""
digraph InsideStage1Mains {
    graph [
        rankdir=LR,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.40,
        ranksep=0.60,
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
        penwidth=2.0,
        arrowsize=0.8
    ];

    subgraph cluster_mains_subsystem {
        label = "INTERNAL ARCHITECTURE: STAGE 1 - MAINS AC INPUT & PROTECTION SUBSYSTEM";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#37474F";
        penwidth = 1.8;

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
                <tr><td align="left">• Restricts I_inrush &lt; 30A</td></tr>
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

        x_cap1 [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>X2 CAPACITOR 1</b></td></tr>
                <tr><td><font color="#1565C0">C_X1: 0.22µF 310V</font></td></tr>
                <hr/>
                <tr><td align="left">• Safety Class X2 Film</td></tr>
                <tr><td align="left">• Across L &amp; N lines</td></tr>
                <tr><td align="left">• Attenuates diff noise</td></tr>
            </table>>,
            fillcolor = "#E3F2FD",
            color = "#1565C0"
        ];

        cm_choke1 [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>CM CHOKE 1</b></td></tr>
                <tr><td><font color="#2E7D32">L_CM1: 15mH / 1.1A</font></td></tr>
                <hr/>
                <tr><td align="left">• Wurth 744823215</td></tr>
                <tr><td align="left">• Toroidal Ferrite Core</td></tr>
                <tr><td align="left">• Attenuates 150k-2MHz</td></tr>
            </table>>,
            fillcolor = "#E8F5E9",
            color = "#2E7D32"
        ];

        cm_choke2 [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>CM CHOKE 2</b></td></tr>
                <tr><td><font color="#2E7D32">L_CM2: 4.7mH / 1.6A</font></td></tr>
                <hr/>
                <tr><td align="left">• Wurth 744822472</td></tr>
                <tr><td align="left">• High-frequency choke</td></tr>
                <tr><td align="left">• Attenuates 2MHz-30MHz</td></tr>
            </table>>,
            fillcolor = "#E8F5E9",
            color = "#2E7D32"
        ];

        y_caps [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>Y1 SAFETY CAPS</b></td></tr>
                <tr><td><font color="#6A1B9A">C_Y1, C_Y2: 2.2nF</font></td></tr>
                <hr/>
                <tr><td align="left">• 400V AC Y1 Ceramic</td></tr>
                <tr><td align="left">• Shunts L &amp; N to Earth</td></tr>
                <tr><td align="left">• CISPR 32 Class B Pass</td></tr>
            </table>>,
            fillcolor = "#F3E5F5",
            color = "#6A1B9A"
        ];

        output_clean [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>FILTERED AC OUT</b></td></tr>
                <tr><td><font color="#1B5E20">To Rectifier Stage</font></td></tr>
                <hr/>
                <tr><td align="left">• L_FILT &amp; N_FILT lines</td></tr>
                <tr><td align="left">• Surge &amp; EMI Cleared</td></tr>
                <tr><td align="left">• Feeds GBU606 Bridge</td></tr>
            </table>>,
            fillcolor = "#C8E6C9",
            color = "#1B5E20"
        ];
    }

    inlet -> fuse [label="Line AC"];
    fuse -> ntc [label="Protected Line"];
    ntc -> mov [label="Inrush Limited"];
    inlet -> mov [label="Neutral AC", style=dashed, color="#78909C"];
    mov -> x_cap1 [label="Clamped AC"];
    x_cap1 -> cm_choke1 [label="Diff Filtered"];
    cm_choke1 -> cm_choke2 [label="Stage 1 CM"];
    cm_choke2 -> y_caps [label="Stage 2 CM"];
    y_caps -> output_clean [label="Clean AC", color="#2E7D32", penwidth=2.4];
}
""",

    "diagram_inside_stage2_rectifier": r"""
digraph InsideStage2Rectifier {
    graph [
        rankdir=LR,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.42,
        ranksep=0.65,
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
        penwidth=2.0,
        arrowsize=0.8
    ];

    subgraph cluster_rectifier_subsystem {
        label = "INTERNAL ARCHITECTURE: STAGE 2 - BRIDGE RECTIFIER & HIGH-VOLTAGE BULK STAGE";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#E65100";
        penwidth = 1.8;

        ac_in [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>FILTERED AC IN</b></td></tr>
                <tr><td><font color="#455A64">From Stage 1 Filter</font></td></tr>
                <hr/>
                <tr><td align="left">• 85V – 265V AC RMS</td></tr>
                <tr><td align="left">• 50Hz / 60Hz Sinusoid</td></tr>
                <tr><td align="left">• Clean Conductors</td></tr>
            </table>>,
            fillcolor = "#ECEFF1",
            color = "#37474F"
        ];

        bridge [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>BRIDGE RECTIFIER</b></td></tr>
                <tr><td><font color="#BF360C">GBU606 (Glass Pass.)</font></td></tr>
                <hr/>
                <tr><td align="left">• 4x Silicon Diodes</td></tr>
                <tr><td align="left">• 600V Breakdown VRRM</td></tr>
                <tr><td align="left">• 6.0A Average Current</td></tr>
                <tr><td align="left">• Full-Wave Rectification</td></tr>
            </table>>,
            fillcolor = "#FFE0B2",
            color = "#E65100"
        ];

        dc_raw [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>PULSED DC BUS</b></td></tr>
                <tr><td><font color="#D84315">100Hz / 120Hz Pulses</font></td></tr>
                <hr/>
                <tr><td align="left">• Peak: 120V – 375V pk</td></tr>
                <tr><td align="left">• 2x Mains Frequency</td></tr>
                <tr><td align="left">• Unfiltered DC</td></tr>
            </table>>,
            fillcolor = "#FFCCBC",
            color = "#D84315"
        ];

        bulk_cap [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>BULK ELECTROLYTIC</b></td></tr>
                <tr><td><font color="#C2185B">C_BULK1: 100µF / 450V</font></td></tr>
                <hr/>
                <tr><td align="left">• Nichicon 105°C Snap-in</td></tr>
                <tr><td align="left">• Energy: E = ½ C V² (7.0J)</td></tr>
                <tr><td align="left">• Holds V_bulk &gt; 90V @ 10ms</td></tr>
                <tr><td align="left">• Ripple &lt; 18V pk-pk @ 72W</td></tr>
            </table>>,
            fillcolor = "#FCE4EC",
            color = "#C2185B"
        ];

        hf_decoupling [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>HF CERAMIC DECOUPLING</b></td></tr>
                <tr><td><font color="#1565C0">C_HF: 100nF / 630V</font></td></tr>
                <hr/>
                <tr><td align="left">• High-Voltage X7R Ceramic</td></tr>
                <tr><td align="left">• Low ESR &amp; ESL</td></tr>
                <tr><td align="left">• Bypasses 80kHz switching spikes</td></tr>
            </table>>,
            fillcolor = "#E3F2FD",
            color = "#1565C0"
        ];

        bleeder [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>SAFETY BLEEDER STRING</b></td></tr>
                <tr><td><font color="#455A64">R_BLEED: 3x 330kΩ (1MΩ)</font></td></tr>
                <hr/>
                <tr><td align="left">• Vishay Dale 1206 SMD</td></tr>
                <tr><td align="left">• Discharges cap &lt; 50V in 60s</td></tr>
                <tr><td align="left">• IEC 62368-1 Shock Safety</td></tr>
            </table>>,
            fillcolor = "#CFD8DC",
            color = "#455A64"
        ];

        hvdc_out [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>HIGH-VOLTAGE DC OUT</b></td></tr>
                <tr><td><font color="#B71C1C">+120V to +375V DC Bus</font></td></tr>
                <hr/>
                <tr><td align="left">• Stable High-Voltage Rail</td></tr>
                <tr><td align="left">• Low-impedance supply</td></tr>
                <tr><td align="left">• Feeds Flyback Primary</td></tr>
            </table>>,
            fillcolor = "#FFCDD2",
            color = "#B71C1C"
        ];
    }

    ac_in -> bridge [label="AC Line & Neutral", color="#37474F"];
    bridge -> dc_raw [label="Rectified Pulses", color="#E65100"];
    dc_raw -> bulk_cap [label="Filter Charge"];
    bulk_cap -> hf_decoupling [label="Smoothed DC"];
    bulk_cap -> bleeder [label="Safety Bleed", style=dotted, color="#78909C"];
    hf_decoupling -> hvdc_out [label="+HVDC Bus", color="#B71C1C", penwidth=2.4];
}
""",

    "diagram_inside_stage3_flyback": r"""
digraph InsideStage3Flyback {
    graph [
        rankdir=LR,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.40,
        ranksep=0.65,
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
        penwidth=2.0,
        arrowsize=0.8
    ];

    subgraph cluster_pri_flyback {
        label = "PRIMARY HOT DOMAIN (High-Voltage Switching)";
        style = "filled,rounded";
        fillcolor = "#FFF8E1";
        color = "#F57F17";
        penwidth = 1.6;

        hvdc_in [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>+HVDC BUS IN</b></td></tr>
                <tr><td><font color="#BF360C">+120V to +375V DC</font></td></tr>
                <hr/>
                <tr><td align="left">• From Stage 2 Bulk Cap</td></tr>
            </table>>,
            fillcolor = "#FFE0B2",
            color = "#E65100"
        ];

        rcd_snubber [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>RCD SNUBBER CLAMP</b></td></tr>
                <tr><td><font color="#B71C1C">D_snub + R_snub + C_snub</font></td></tr>
                <hr/>
                <tr><td align="left">• US1M Ultra-Fast Diode</td></tr>
                <tr><td align="left">• 1nF 1kV + 68kΩ 2W</td></tr>
                <tr><td align="left">• Clamps leakage &lt; 650V</td></tr>
            </table>>,
            fillcolor = "#FFCDD2",
            color = "#B71C1C"
        ];

        pri_winding [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>TX1 PRIMARY (36T)</b></td></tr>
                <tr><td><font color="#E65100">PQ26/20 (3C95 Ferrite)</font></td></tr>
                <hr/>
                <tr><td align="left">• Primary Inductance: <b>220µH</b></td></tr>
                <tr><td align="left">• Peak Current: <b>I_pk = 2.96A</b></td></tr>
                <tr><td align="left">• Peak Flux: <b>B_max = 0.28T</b></td></tr>
            </table>>,
            fillcolor = "#FFE082",
            color = "#F57F17"
        ];

        pri_mosfet [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>PRIMARY MOSFET (Q1)</b></td></tr>
                <tr><td><font color="#1565C0">STP10NK80Z / IPB80R290P7</font></td></tr>
                <hr/>
                <tr><td align="left">• 800V, N-Channel Power FET</td></tr>
                <tr><td align="left">• R_DS(on) = 0.29Ω (D2PAK / TO-220)</td></tr>
                <tr><td align="left">• Uniform 65kHz PWM Gate Drive</td></tr>
            </table>>,
            fillcolor = "#BBDEFB",
            color = "#1565C0"
        ];

        pwm_controller [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>UNIFORM-FREQ PWM IC (U1)</b></td></tr>
                <tr><td><font color="#2E7D32">UC3843 / UCC28C43 (8-Pin)</font></td></tr>
                <hr/>
                <tr><td align="left">• Uniform 65kHz Fixed Clock</td></tr>
                <tr><td align="left">• RT = 10kΩ, CT = 2.2nF Timing</td></tr>
                <tr><td align="left">• Cycle-by-cycle Current Limit</td></tr>
                <tr><td align="left">• Direct Totem-Pole Gate Out</td></tr>
            </table>>,
            fillcolor = "#C8E6C9",
            color = "#2E7D32"
        ];

        aux_winding [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>AUX WINDING (TX1_AUX)</b></td></tr>
                <tr><td><font color="#6A1B9A">+14.0V Bias Supply (5T)</font></td></tr>
                <hr/>
                <tr><td align="left">• UF4004 Diode + 47µF Cap</td></tr>
                <tr><td align="left">• Powers UC3843 VCC pin</td></tr>
            </table>>,
            fillcolor = "#E1BEE7",
            color = "#6A1B9A"
        ];
    }

    subgraph cluster_sec_flyback {
        label = "SECONDARY COLD DOMAIN (Touch-Safe SELV)";
        style = "filled,rounded";
        fillcolor = "#E8F5E9";
        color = "#2E7D32";
        penwidth = 1.6;

        sec_winding [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>TX1 SECONDARY (6T)</b></td></tr>
                <tr><td><font color="#1B5E20">Furukawa TEX-E Wire</font></td></tr>
                <hr/>
                <tr><td align="left">• Triple-insulated wire</td></tr>
                <tr><td align="left">• Turns ratio Np:Ns = 6:1</td></tr>
                <tr><td align="left">• ⚡ 3000V RMS Proof</td></tr>
            </table>>,
            fillcolor = "#A5D6A7",
            color = "#1B5E20"
        ];

        schottky_rectifier [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>SCHOTTKY RECTIFIER (D_SEC)</b></td></tr>
                <tr><td><font color="#00695C">MBR10100 / MBR20100CT</font></td></tr>
                <hr/>
                <tr><td align="left">• 100V, 10A Schottky Diode</td></tr>
                <tr><td align="left">• Simple passive rectification</td></tr>
                <tr><td align="left">• Robust, no complex driver IC</td></tr>
            </table>>,
            fillcolor = "#B2DFDB",
            color = "#00695C"
        ];

        sec_filter [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>OUTPUT LC FILTER</b></td></tr>
                <tr><td><font color="#1565C0">470µF / 35V Low-ESR + 2.2µH</font></td></tr>
                <hr/>
                <tr><td align="left">• Smooths 65kHz ripple</td></tr>
                <tr><td align="left">• Attenuates HF switching spikes</td></tr>
                <tr><td align="left">• Bus ripple &lt; 50mV pk-pk</td></tr>
            </table>>,
            fillcolor = "#E3F2FD",
            color = "#1565C0"
        ];

        tl431_opto [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>ISOLATED FEEDBACK</b></td></tr>
                <tr><td><font color="#4E342E">TL431 + Opto PC817 / EL817</font></td></tr>
                <hr/>
                <tr><td align="left">• Precision 2.495V shunt</td></tr>
                <tr><td align="left">• 5000V RMS Optocoupler</td></tr>
                <tr><td align="left">• Pulls down UC3843 COMP pin</td></tr>
                <tr><td align="left">• Regulates +24.0V ± 1.0%</td></tr>
            </table>>,
            fillcolor = "#D7CCC8",
            color = "#4E342E"
        ];

        bus_24v [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>INTERMEDIATE BUS OUT</b></td></tr>
                <tr><td><font color="#004D40"><b>+24.0V DC (72W Continuous)</b></font></td></tr>
                <hr/>
                <tr><td align="left">• Ripple &lt; 50mV pk-pk</td></tr>
                <tr><td align="left">• Feeds Stage 4 Buck-Boost</td></tr>
            </table>>,
            fillcolor = "#80CBC4",
            color = "#004D40"
        ];
    }

    hvdc_in -> pri_winding [label="HVDC Supply"];
    pri_winding -> rcd_snubber [label="Snubber Clamp", style=dashed, color="#B71C1C"];
    pri_winding -> pri_mosfet [label="Switch Drain"];
    pwm_controller -> pri_mosfet [label="65kHz PWM Gate"];
    aux_winding -> pwm_controller [label="+14V VCC"];

    pri_winding -> sec_winding [label="⚡ 3000V Isolation Barrier", penwidth=3.0, color="#D32F2F", style=bold];
    sec_winding -> schottky_rectifier [label="65kHz AC Pulses"];
    schottky_rectifier -> sec_filter [label="Rectified DC"];
    sec_filter -> bus_24v [label="+24V Rail", color="#004D40", penwidth=2.4];
    bus_24v -> tl431_opto [label="Sense +24V"];
    tl431_opto -> pwm_controller [label="Isolated Feedback (COMP)", style=dashed, color="#6A1B9A"];
}
""",

    "diagram_inside_stage4_final_stage": r"""
digraph InsideStage4FinalStage {
    graph [
        rankdir=LR,
        bgcolor="#FFFFFF",
        compound=true,
        fontname="Helvetica, Arial, sans-serif",
        fontsize=12,
        nodesep=0.40,
        ranksep=0.65,
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
        penwidth=2.0,
        arrowsize=0.8
    ];

    subgraph cluster_post_regulator {
        label = "INTERNAL ARCHITECTURE: STAGE 4 - 4-SWITCH BUCK-BOOST, DAC STEERING & PROTECTION";
        style = "filled,rounded";
        fillcolor = "#FAFAFA";
        color = "#00838F";
        penwidth = 1.8;

        bus_in [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>+24.0V DC BUS IN</b></td></tr>
                <tr><td><font color="#00695C">From Stage 3 Flyback</font></td></tr>
                <hr/>
                <tr><td align="left">• Fixed 24.0V ± 1.0%</td></tr>
                <tr><td align="left">• 72W Power Headroom</td></tr>
            </table>>,
            fillcolor = "#B2DFDB",
            color = "#00695C"
        ];

        h_bridge [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>4-SWITCH H-BRIDGE</b></td></tr>
                <tr><td><font color="#00838F">4x Infineon BSC034N04LS</font></td></tr>
                <hr/>
                <tr><td align="left">• 40V, 3.4mΩ Logic-Level</td></tr>
                <tr><td align="left">• QA/QB: Buck Leg</td></tr>
                <tr><td align="left">• QC/QD: Boost Leg</td></tr>
                <tr><td align="left">• Seamless transition modes</td></tr>
            </table>>,
            fillcolor = "#B2EBF2",
            color = "#00838F"
        ];

        inductor [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>FLAT-WIRE INDUCTOR</b></td></tr>
                <tr><td><font color="#E65100">Wurth 7443321000</font></td></tr>
                <hr/>
                <tr><td align="left">• <b>10.0µH Flat Copper</b></td></tr>
                <tr><td align="left">• 8.5A RMS, 11.5A Saturation</td></tr>
                <tr><td align="left">• High-Q, low AC skin loss</td></tr>
            </table>>,
            fillcolor = "#FFE0B2",
            color = "#E65100"
        ];

        bb_controller [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>BUCK-BOOST IC (U3)</b></td></tr>
                <tr><td><font color="#00838F">TI LM5176 (HTSSOP-28)</font></td></tr>
                <hr/>
                <tr><td align="left">• 300kHz Fixed PWM</td></tr>
                <tr><td align="left">• Buck, Buck-Boost, Boost</td></tr>
                <tr><td align="left">• V_FB = 1.20V Bandgap</td></tr>
                <tr><td align="left">• COMP analog control pin</td></tr>
            </table>>,
            fillcolor = "#E0F7FA",
            color = "#00838F"
        ];

        dac_steering [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>DAC STEERING NETWORK</b></td></tr>
                <tr><td><font color="#6A1B9A">Resistor Summing Junction</font></td></tr>
                <hr/>
                <tr><td align="left">• R_top=49.9k, R_DAC=11k, R_bot=3.65k</td></tr>
                <tr><td align="left">• 12-bit DAC: 0V → 20V Out</td></tr>
                <tr><td align="left">• 12-bit DAC: 3.3V → 5V Out</td></tr>
                <tr><td align="left">• <b>10.0 mV Digital Step Size</b></td></tr>
            </table>>,
            fillcolor = "#EDE7F6",
            color = "#6A1B9A"
        ];

        output_filter [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>OUTPUT FILTER BANK</b></td></tr>
                <tr><td><font color="#1565C0">MLCC + Solid Polymer</font></td></tr>
                <hr/>
                <tr><td align="left">• 4x 22µF 25V X7R 1210</td></tr>
                <tr><td align="left">• 100µF 25V OS-CON (12mΩ)</td></tr>
                <tr><td align="left">• <b>Ripple &lt; 25mV pk-pk</b></td></tr>
            </table>>,
            fillcolor = "#E3F2FD",
            color = "#1565C0"
        ];

        shunt_sense [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>CURRENT SHUNT RESISTOR</b></td></tr>
                <tr><td><font color="#B71C1C">10mΩ Metal Shunt (CSP/CSN)</font></td></tr>
                <hr/>
                <tr><td align="left">• 10mΩ 3W 0.1% Metal Shunt</td></tr>
                <tr><td align="left">• Kelvin sense to LM5176 pins</td></tr>
                <tr><td align="left">• Cycle-by-cycle peak limit</td></tr>
            </table>>,
            fillcolor = "#FFCDD2",
            color = "#B71C1C"
        ];

        binding_posts [
            label = <<table border="0" cellborder="0" cellspacing="2">
                <tr><td><b>4mm BINDING POSTS</b></td></tr>
                <tr><td><font color="#4A148C"><b>OUTPUT TO DEVICE (DUT)</b></font></td></tr>
                <hr/>
                <tr><td align="left">• Voltage: <b>5.0V – 20.0V DC</b></td></tr>
                <tr><td align="left">• Current: <b>0.1A – 3.0A DC</b></td></tr>
                <tr><td align="left">• Power: <b>60.0W Max Continuous</b></td></tr>
                <tr><td align="left">• Protected &amp; Low-Ripple</td></tr>
            </table>>,
            fillcolor = "#E1BEE7",
            color = "#4A148C"
        ];
    }

    bus_in -> h_bridge [label="+24V Rail"];
    bb_controller -> h_bridge [label="4x Gate PWM", color="#00838F"];
    h_bridge -> inductor [label="SW1 Node"];
    inductor -> h_bridge [label="SW2 Node"];
    h_bridge -> output_filter [label="Power Flow"];
    output_filter -> shunt_sense [label="Filtered DC"];
    shunt_sense -> binding_posts [label="Regulated DC", color="#4A148C", penwidth=2.4];

    output_filter -> dac_steering [label="V_OUT Sense", style=dotted];
    dac_steering -> bb_controller [label="FB Node Steering", color="#6A1B9A"];

    shunt_sense -> bb_controller [label="CSP/CSN Current Sense", color="#C62828", penwidth=2.0];
}
"""
}

def generate_sub_diagrams():
    print(f"Building 4 internal sub-block diagrams into {SCRIPT_DIR}...")
    for name, code in diagrams.items():
        dot_path = os.path.join(SCRIPT_DIR, f"{name}.dot")
        png_path = os.path.join(SCRIPT_DIR, f"{name}.png")
        svg_path = os.path.join(SCRIPT_DIR, f"{name}.svg")

        with open(dot_path, "w", encoding="utf-8") as f:
            f.write(code.strip())

        cmd_png = ["dot", "-Tpng", "-Gdpi=300", dot_path, "-o", png_path]
        subprocess.run(cmd_png, check=True)

        cmd_svg = ["dot", "-Tsvg", dot_path, "-o", svg_path]
        subprocess.run(cmd_svg, check=True)

        print(f"  ✓ Generated: {name}.png ({os.path.getsize(png_path):,} bytes) & {name}.svg")

    print("All 4 internal sub-block diagrams built successfully!")

if __name__ == "__main__":
    generate_sub_diagrams()
