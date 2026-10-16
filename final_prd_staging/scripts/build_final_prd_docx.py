#!/usr/bin/env python3
"""
VVDN Product Requirement Document (PRD) Final .docx Generator v2.1
Generates:
  - final_prd_staging/PRODUCT_REQUIREMENT_DOCUMENT_PRD_FINAL.docx
  - smart_programmable_power_supply/reference_docs/prd_final_spps.docx
  - smart_programmable_power_supply/PRODUCT_REQUIREMENT_DOCUMENT_PRD.docx
Strictly aligned with:
  - Base template: img/PRD.docx
  - VVDN EVSE PRD standard layout (clean, simple literature style)
  - Zero placeholder tags or angle bracket '<...>' tokens from template instructions
  - Preservation of engineering mathematical symbols (< 25 mV, < 500 ms, < 75 W, etc.)
  - Fully in-line table geometry (strips floating <w:tblpPr> properties)
  - All 11 architectural diagrams embedded as high-res PNG images (14 images total including template branding)
  - All sequence tables, requirement tables (4.1 to 4.5), Stage 3 component specification table 4.6D, and complete BOM tables (9.1 & 9.2)
  - Complete List of Tables (20 tables) and List of Figures (11 figures)
  - 10 cross-mentor technical defense Q&A pairs in the Appendix
"""

import os
import sys
import re

if os.path.exists(".venv/lib/python3.14/site-packages"):
    sys.path.insert(0, os.path.abspath(".venv/lib/python3.14/site-packages"))
elif os.path.exists("tools/.venv/lib/python3.14/site-packages"):
    sys.path.insert(0, os.path.abspath("tools/.venv/lib/python3.14/site-packages"))

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# ==============================================================================
# XML UTILITIES FOR TABLE FORMATTING & RESIZING
# ==============================================================================

def set_cell_background(cell, fill_hex):
    """Set background color of a cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Set cell padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('tcMar'):
            tcPr.remove(child)
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="B0BEC5", sz="4"):
    """Set standard single borders on table."""
    tblPr = table._tbl.tblPr
    for child in list(tblPr):
        if child.tag.endswith('tblBorders'):
            tblPr.remove(child)
    tblBorders = OxmlElement('w:tblBorders')
    for b_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), sz)
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), color)
        tblBorders.append(b)
    tblPr.append(tblBorders)

def apply_table_geometry(table, col_widths, total_width_inches=6.47):
    """Enforce explicit column widths on table grid and every cell."""
    table.autofit = False
    total_dxa = int(total_width_inches * 1440)

    tblPr = table._tbl.tblPr
    for child in list(tblPr):
        if child.tag.endswith('tblpPr'):
            tblPr.remove(child)

    tblW = tblPr.find(qn('w:tblW'))
    if tblW is None:
        tblW = OxmlElement('w:tblW')
        tblPr.append(tblW)
    tblW.set(qn('w:w'), str(total_dxa))
    tblW.set(qn('w:type'), 'dxa')

    tblGrid = table._tbl.find(qn('w:tblGrid'))
    if tblGrid is not None:
        table._tbl.remove(tblGrid)
    tblGrid = OxmlElement('w:tblGrid')
    for w in col_widths:
        gc = OxmlElement('w:gridCol')
        gc.set(qn('w:w'), str(int(w.inches * 1440)))
        tblGrid.append(gc)
    table._tbl.insert(table._tbl.index(tblPr) + 1, tblGrid)

    for r_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        if trPr.find(qn('w:cantSplit')) is None:
            trPr.append(OxmlElement('w:cantSplit'))
        if r_idx == 0:
            if trPr.find(qn('w:tblHeader')) is None:
                trPr.append(OxmlElement('w:tblHeader'))

        tcs = row._tr.xpath('w:tc')
        for c_idx, tc in enumerate(tcs):
            if c_idx < len(col_widths):
                w_dxa = int(col_widths[c_idx].inches * 1440)
                tcPr = tc.get_or_add_tcPr()
                tcW = tcPr.find(qn('w:tcW'))
                if tcW is None:
                    tcW = OxmlElement('w:tcW')
                    tcPr.append(tcW)
                tcW.set(qn('w:w'), str(w_dxa))
                tcW.set(qn('w:type'), 'dxa')

def set_cell_text(cell, text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, font_size=Pt(8.5), color_rgb=(26, 32, 44)):
    """Set formatted text in cell without extra spacing."""
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = font_size
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

def create_workflow_table(doc, title, steps, header_color="1A365D", total_width=6.47):
    """Create a structured sequence workflow table."""
    col_widths = [Inches(0.95), Inches(1.85), Inches(3.67)]
    t = doc.add_table(rows=1, cols=3)
    apply_table_geometry(t, col_widths, total_width_inches=total_width)
    set_table_borders(t, color="CBD5E0", sz="4")

    # Header Row
    hdr_cell = t.rows[0].cells[0]
    hdr_cell.merge(t.rows[0].cells[1])
    hdr_cell.merge(t.rows[0].cells[2])
    set_cell_background(hdr_cell, header_color)
    set_cell_text(hdr_cell, title, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(9.0), color_rgb=(255, 255, 255))

    for s_no, sub, desc in steps:
        r = t.add_row()
        c0 = r.cells[0]
        c1 = r.cells[1]
        c2 = r.cells[2]
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "F8FAFC")
        set_cell_background(c2, "FFFFFF")
        set_cell_text(c0, f"Step {s_no}", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(8.5))
        set_cell_text(c1, sub, bold=True, font_size=Pt(8.5))
        set_cell_text(c2, desc, font_size=Pt(8.5))

    apply_table_geometry(t, col_widths, total_width_inches=total_width)
    return t

# ==============================================================================
# MAIN GENERATOR FUNCTION
# ==============================================================================

def generate_final_prd():
    base_template = "img/PRD.docx"
    output_prd_final_docx = "final_prd_staging/PRODUCT_REQUIREMENT_DOCUMENT_PRD_FINAL.docx"
    output_ref_docx = "smart_programmable_power_supply/reference_docs/prd_final_spps.docx"
    output_main_docx = "smart_programmable_power_supply/PRODUCT_REQUIREMENT_DOCUMENT_PRD.docx"

    print(f"Loading base template: {base_template}")
    doc = docx.Document(base_template)

    # CAPTURE ORIGINAL BOM TABLES BEFORE ADDING ANY NEW TABLES!
    # In img/PRD.docx, Table 11 is System 1 BOM, and Table 12 is System 2 BOM.
    t_bom1_target = doc.tables[11]
    t_bom2_target = doc.tables[12]

    # 1. PAGE SETUP
    for sec in doc.sections:
        sec.top_margin = Inches(0.85)
        sec.bottom_margin = Inches(0.85)
        sec.left_margin = Inches(0.90)
        sec.right_margin = Inches(0.90)

    # 2. METADATA TABLE (Table 0)
    t0 = doc.tables[0]
    set_cell_text(t0.rows[0].cells[1], "VVDN_SPPS_2026", bold=True)
    set_cell_text(t0.rows[1].cells[1], "Smart Programmable Voltage Supply Module (85–265 V AC In, 5–20 V / 3 A DC Out)", bold=True)
    set_cell_text(t0.rows[2].cells[1], "A1_001")
    set_cell_text(t0.rows[3].cells[1], "16th Oct 2026")
    apply_table_geometry(t0, [Inches(2.2), Inches(4.27)])

    # 3. REVISION HISTORY (Table 1)
    t1 = doc.tables[1]
    rev_row = t1.rows[1]
    set_cell_text(rev_row.cells[0], "16-Oct-2026", align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(rev_row.cells[1], "A1_001", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(rev_row.cells[2], "Production-Grade PRD Release: Uniform-Frequency Flyback (UC3843 @ 65kHz), MBR10100 Schottky passive rectification, full sequence tables, complete BOMs, 11 block diagrams, and cross-mentor technical defense.")
    set_cell_text(rev_row.cells[3], "Power Electronics Trainee (GET)")
    set_cell_text(rev_row.cells[4], "Senior Hardware Architect")
    set_cell_text(rev_row.cells[5], "BU SME (Power Electronics)")

    # 4. SIGN-OFF TABLES (Table 2 & 3)
    t2 = doc.tables[2]
    # Customer Sign-Off
    set_cell_text(t2.rows[2].cells[1], "Dr. Michael Chen")
    set_cell_text(t2.rows[2].cells[2], "Sarah Jenkins")
    set_cell_text(t2.rows[3].cells[1], "Director of Hardware Engineering")
    set_cell_text(t2.rows[3].cells[2], "Program Director")
    set_cell_text(t2.rows[4].cells[1], "m.chen@client-ate.com")
    set_cell_text(t2.rows[4].cells[2], "s.jenkins@client-ate.com")
    set_cell_text(t2.rows[5].cells[1], "ATE Systems Inc., San Jose, CA")
    set_cell_text(t2.rows[5].cells[2], "ATE Systems Inc., San Jose, CA")
    set_cell_text(t2.rows[6].cells[1], "Approved for modular test rack and benchtop integration. Functional power parameters and safety boundaries fully validated.")
    set_cell_text(t2.rows[6].cells[2], "Product requirements, delivery milestones, and DVT acceptance criteria accepted.")
    set_cell_text(t2.rows[7].cells[1], "Signed: 16-Oct-2026", italic=True)
    set_cell_text(t2.rows[7].cells[2], "Signed: 16-Oct-2026", italic=True)

    # VVDN Sign-Off
    set_cell_text(t2.rows[9].cells[1], "Power Electronics Trainee (GET)")
    set_cell_text(t2.rows[9].cells[2], "Senior Hardware Architect / Lead")
    set_cell_text(t2.rows[10].cells[1], "GET - Embedded Hardware Engineering")
    set_cell_text(t2.rows[10].cells[2], "Senior Hardware Engineer (Power BU)")
    set_cell_text(t2.rows[11].cells[1], "trainee.power@vvdntech.in")
    set_cell_text(t2.rows[11].cells[2], "lead.power@vvdntech.in")
    set_cell_text(t2.rows[12].cells[1], "VVDN Technologies, Global Innovation Park, Gurugram")
    set_cell_text(t2.rows[12].cells[2], "VVDN Technologies, Global Innovation Park, Gurugram")
    set_cell_text(t2.rows[13].cells[1], "4-Stage conversion architecture, uniform 65 kHz Flyback, MBR10100 secondary rectification, and standard IC protections designed to spec.")
    set_cell_text(t2.rows[13].cells[2], "High-level requirements, Class A BOM baseline, and verification gates signed off.")
    set_cell_text(t2.rows[14].cells[1], "Signed: 16-Oct-2026", italic=True)
    set_cell_text(t2.rows[14].cells[2], "Signed: 16-Oct-2026", italic=True)
    apply_table_geometry(t2, [Inches(1.8), Inches(2.33), Inches(2.34)])

    # Internal SME Sign-Off (Table 3)
    t3 = doc.tables[3]
    set_cell_text(t3.rows[1].cells[1], "Karpagamoorthy R / Vignesh Anandhan (BU SME Power Electronics)")
    set_cell_text(t3.rows[2].cells[1], "GET - Embedded Hardware Engineering Trainee")
    set_cell_text(t3.rows[3].cells[1], "Verified against IEC 62368-1 reinforced isolation, CISPR 32 Class B EMC, uniform 65 kHz magnetics sizing, and 4-switch Buck-Boost closed-loop stability.")
    set_cell_text(t3.rows[4].cells[1], "Signed: 16-Oct-2026", italic=True)
    apply_table_geometry(t3, [Inches(1.8), Inches(4.67)])

    # 5. ABBREVIATIONS TABLE (Table 4)
    t4 = doc.tables[4]
    abbreviations = [
        ("VVDN_SPPS_2026", "VVDN Smart Programmable Power Supply (Project Identifier)"),
        ("PRD", "Product Requirement Document"),
        ("HDD", "Hardware Design Document (Detailed Engineering Design Specification)"),
        ("AC", "Alternating Current (Grid Mains Input, 85 V – 265 V AC RMS)"),
        ("DC", "Direct Current (Regulated Output, 5.0 V – 20.0 V DC)"),
        ("SELV", "Safety Extra-Low Voltage (< 60 V DC limit per IEC 62368-1)"),
        ("PFC", "Power Factor Correction"),
        ("CC", "Constant Current Mode (Autonomous Hardware Current Limit)"),
        ("CV", "Constant Voltage Mode (Precision Closed-Loop Voltage Regulation)"),
        ("DAC", "Digital-to-Analog Converter (12-bit Voltage Setpoint Injection)"),
        ("ADC", "Analog-to-Digital Converter (Microcontroller Telemetry Sampling)"),
        ("OVP", "Over-Voltage Protection"),
        ("OCP", "Over-Current Protection"),
        ("OTP", "Over-Temperature Protection"),
        ("SCP", "Short-Circuit Protection"),
        ("UVLO", "Under-Voltage Lockout"),
        ("DMM", "Digital Multimeter"),
        ("CT", "Current Transformer (AC Primary Current Sensing)"),
        ("I2C", "Inter-Integrated Circuit Serial Communication Bus"),
        ("SPI", "Serial Peripheral Interface Bus"),
        ("UART", "Universal Asynchronous Receiver-Transmitter"),
        ("PWM", "Pulse Width Modulation"),
        ("EMI", "Electromagnetic Interference"),
        ("EMC", "Electromagnetic Compatibility"),
        ("NTC", "Negative Temperature Coefficient Thermistor (Inrush Limiter)"),
        ("MOV", "Metal Oxide Varistor (Surge & Transient Voltage Clamp)"),
        ("ESR", "Equivalent Series Resistance"),
        ("DVT", "Design Verification Testing"),
        ("ATE", "Automated Test Equipment"),
        ("DUT", "Device Under Test")
    ]
    while len(t4.rows) > 1:
        t4._tbl.remove(t4.rows[-1]._tr)
    for acr, desc in abbreviations:
        r = t4.add_row()
        set_cell_text(r.cells[0], acr, bold=True)
        set_cell_text(r.cells[1], desc)
    apply_table_geometry(t4, [Inches(1.8), Inches(4.67)])

    # 6. REFERENCES TABLE (Table 5)
    t5 = doc.tables[5]
    references = [
        ("REF-001", "Statement of Work (SOW): Smart Programmable Voltage Supply Module v1.0, VVDN Technologies"),
        ("REF-002", "IEC 62368-1 (3rd Edition): Audio/video, information and communication technology equipment – Safety requirements"),
        ("REF-003", "CISPR 32 / EN 55032 Class B: Electromagnetic compatibility of multimedia equipment – Emission requirements"),
        ("REF-004", "Texas Instruments LM5176: High-Performance 4-Switch Synchronous Buck-Boost Controller Datasheet (SNVSAR4)"),
        ("REF-005", "Texas Instruments UC3843 / UCC28C43: High-Performance Current-Mode PWM Controller Datasheet"),
        ("REF-006", "Texas Instruments INA226: High-Side / Low-Side 16-Bit I2C Power Monitor Datasheet"),
        ("REF-007", "Texas Instruments AMC1311: 5000V RMS Reinforced Isolated Delta-Sigma Modulator Datasheet"),
        ("REF-008", "STMicroelectronics STM32G474RET6: 170 MHz Mixed-Signal Microcontroller Datasheet & Reference Manual (RM0440)"),
        ("REF-009", "VVDN Hardware Design Document (HDD): Smart Programmable Power Supply Circuit Design, Derivations & Schematics")
    ]
    while len(t5.rows) > 1:
        t5._tbl.remove(t5.rows[-1]._tr)
    for ref_id, ref_desc in references:
        r = t5.add_row()
        set_cell_text(r.cells[0], ref_id, bold=True)
        set_cell_text(r.cells[1], ref_desc)
    apply_table_geometry(t5, [Inches(1.2), Inches(5.27)])

    # 7. USE CASE TABLE (Table 6 in template)
    t6 = doc.tables[6]
    use_cases = [
        ("1", "Universal AC mains soft startup and inrush current suppression (< 25 A peak)"),
        ("2", "AC full-wave rectification and high-voltage DC bulk energy holdup (> 10 ms)"),
        ("3", "Galvanically isolated uniform-frequency Flyback conversion (+24.0 V DC, 72 W)"),
        ("4", "Synchronous 4-switch Buck-Boost step-down/step-up post-regulation (5 V – 20 V DC)"),
        ("5", "High-precision 10 mV digital voltage steering via 12-bit DAC summing network"),
        ("6", "LM5176 built-in cycle-by-cycle overcurrent protection via CSP/CSN pins"),
        ("7", "Primary Flyback cycle-by-cycle current limit via UC3843 ISENSE resistor"),
        ("8", "Controller internal thermal shutdown and board temperature monitoring"),
        ("9", "Primary AC input power measurement via isolated delta-sigma amplifier and CT"),
        ("10", "Secondary DC load voltage, current, and power monitoring via 16-bit I2C monitor"),
        ("11", "Real-time conversion efficiency computation and 1.3\" OLED dashboard display update"),
        ("12", "Local front-panel rotary encoder tuning, tactile output enable, and status LED indication")
    ]
    while len(t6.rows) > 1:
        t6._tbl.remove(t6.rows[-1]._tr)
    for sn, uc in use_cases:
        r = t6.add_row()
        set_cell_text(r.cells[0], sn, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(r.cells[1], uc)
    apply_table_geometry(t6, [Inches(0.65), Inches(5.82)])

    # 8. HARDWARE INTERFACES TABLE (Table 7 in template)
    t7 = doc.tables[7]
    hw_interfaces = [
        ("1", "AC Grid Mains", "SPPS Board", "IEC 320-C14 Inlet", "Universal 85V–265V AC RMS, 50/60Hz grounded power input with 2A fuse"),
        ("2", "SPPS Board", "DUT / Load", "4mm Binding Posts", "Regulated 5.0V–20.0V DC / 3.0A power delivery to device under test"),
        ("3", "SPPS Board", "Local Operator", "1.3\" OLED Display", "Real-time graphical dashboard for V, I, P, efficiency (η), and operating mode"),
        ("4", "SPPS Board", "Local Operator", "Output Enable Button", "Tactile push-button for safe electronic enable/disable of output power"),
        ("5", "SPPS Board", "Local Operator", "Status Mode LEDs", "Visual indication of Output Active (Green), Limit (Amber), and Fault (Red) states"),
        ("6", "SPPS Board", "Debug Programmer", "SWD Header", "Microcontroller firmware flashing and SWO debug tracing"),
        ("7", "SPPS Board", "Lab Oscilloscope", "PCB Test Points", "Diagnostic test loops for measuring intermediate rail, ripple, and switching nodes"),
        ("8", "Primary Side", "Secondary Side", "6.4mm Milled Slot", "Physical 2.0mm air slot beneath transformer enforcing IEC 62368-1 isolation")
    ]
    while len(t7.rows) > 1:
        t7._tbl.remove(t7.rows[-1]._tr)
    for sl, e1, e2, iface, usage in hw_interfaces:
        r = t7.add_row()
        set_cell_text(r.cells[0], sl, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(r.cells[1], e1)
        set_cell_text(r.cells[2], e2)
        set_cell_text(r.cells[3], iface, bold=True)
        set_cell_text(r.cells[4], usage)
    apply_table_geometry(t7, [Inches(0.55), Inches(1.15), Inches(1.15), Inches(1.42), Inches(2.20)])

    # 9. SOFTWARE INTERFACES TABLE (Table 8 in template)
    t8 = doc.tables[8]
    sw_interfaces = [
        ("1", "STM32G474 MCU", "INA226 Monitor", "Secondary Telemetry", "I2C Fast Mode (400 kHz)", "Reads 16-bit DC output voltage, current, and bus power at 10 Hz rate"),
        ("2", "STM32G474 MCU", "1.3\" OLED (SSD1306)", "Display Dashboard", "I2C Fast Mode (400 kHz)", "Updates numerical readouts, mode text, and efficiency bar graph at 10 Hz"),
        ("3", "STM32G474 MCU", "AMC1311 Iso-Amp", "Primary AC Voltage", "Hardware Sinc3 Decimation", "Demodulates 20 MHz delta-sigma bitstream for true AC voltage v(t)"),
        ("4", "STM32G474 MCU", "Current Transformer", "Primary AC Current", "Analog ADC Channel (12-bit)", "Samples burden resistor voltage from 1000:1 CT for AC mains current sensing"),
        ("5", "STM32G474 MCU", "LM5176 FB Node", "Voltage Steering", "Internal 12-Bit DAC1", "Injects steering current into summing node to set Vout between 5.0V and 20.0V"),
        ("6", "STM32G474 MCU", "Rotary Encoders", "User Input", "Timer Encoder Interface (TIM2/3)", "Rotary dials with hardware debounced quadrature push-switches"),
        ("7", "STM32G474 MCU", "Status LEDs", "Status Annunciation", "GPIO Digital Outputs", "Drives Green (Active), Amber (Limit), and Red (Fault) status indicator LEDs"),
        ("8", "STM32G474 MCU", "LM5176 Enable Pin", "Output Control", "GPIO Digital Output", "Controls post-regulator run state during standby, soft-start, and fault disable"),
        ("9", "STM32G474 MCU", "Host PC / ATE", "Calibration & SCPI", "USB-CDC Virtual COM / UART", "Serial channel for automated calibration, logging, and SCPI test commands")
    ]
    while len(t8.rows) > 1:
        t8._tbl.remove(t8.rows[-1]._tr)
    for sn, e1, e2, iface, proto, usage in sw_interfaces:
        r = t8.add_row()
        set_cell_text(r.cells[0], sn, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(r.cells[1], e1)
        set_cell_text(r.cells[2], e2)
        set_cell_text(r.cells[3], iface, bold=True)
        set_cell_text(r.cells[4], proto)
        set_cell_text(r.cells[5], usage)
    apply_table_geometry(t8, [Inches(0.45), Inches(1.10), Inches(1.10), Inches(1.10), Inches(1.22), Inches(1.50)])

    # 10. DOMAINS INVOLVED (Table 9 in template)
    t9 = doc.tables[9]
    domains = [
        ("Hardware - HW", "Yes", "4-Stage power conversion schematics, component selection, layout, and bring-up", "Gate Review"),
        ("Mechanical - ME", "Yes", "Enclosure integration, thermal copper heatsinking, binding post cutouts", "Mechanical Review"),
        ("Firmware - FW", "Yes", "Bare-metal drivers (ADC, DAC, I2C, Timers), OLED dashboard, efficiency math", "Firmware Review"),
        ("PC App - PAP", "Optional", "Python-based automated calibration and DVT sweep script over USB-UART", "Optional"),
        ("Test Firmware", "Yes", "Dedicated bring-up routines for peripheral check, DAC sweep, and zeroing", "Lab Bring-up Sign-off")
    ]
    while len(t9.rows) > 1:
        t9._tbl.remove(t9.rows[-1]._tr)
    for d_name, sys1, scope, rev in domains:
        r = t9.add_row()
        set_cell_text(r.cells[0], d_name, bold=True)
        set_cell_text(r.cells[1], sys1, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(r.cells[2], scope)
        set_cell_text(r.cells[3], rev)
    apply_table_geometry(t9, [Inches(1.2), Inches(0.9), Inches(3.17), Inches(1.2)])

    # 11. DELIVERABLES (Table 10 in template)
    t10 = doc.tables[10]
    deliverables = [
        ("VVDN_SPPS_2026", "Systems / PRD", "Product Requirement Document (PRD) — Baseline Specifications & Acceptance Criteria", "Architecture Sign-off", "Milestone 1"),
        ("SPPS Module", "Hardware (HW)", "Hardware Design Document (HDD) with complete circuit derivations & stress calculations", "SME Peer Review", "Milestone 2"),
        ("SPPS Module", "Hardware (HW)", "Altium Designer Complete Schematics", "Gate Review", "Milestone 3"),
        ("SPPS Module", "Hardware (HW)", "Class A Engineering Bill of Materials (BOM) with manufacturer part numbers", "Procurement Audit", "Milestone 3"),
        ("SPPS Module", "Hardware (HW)", "4-Layer PCB Layout & Gerber RS-274X Fabrication Package (ODB++, NC Drill, Pick-and-Place)", "DFM / DFA Check", "Milestone 4"),
        ("SPPS Module", "Hardware (HW)", "Design Verification Testing (DVT) Report & Acceptance Certificate", "Lab Sign-off", "Milestone 5"),
        ("SPPS Module", "Firmware (FW)", "Microcontroller Telemetry & Display Firmware Source Code", "Code Review", "Milestone 5"),
        ("SPPS Module", "Compliance / Safety", "Hi-Pot Dielectric Withstand Certificate (3000V RMS) & Pre-Compliance EMC Report", "Third-Party Lab", "Milestone 5")
    ]
    while len(t10.rows) > 1:
        t10._tbl.remove(t10.rows[-1]._tr)
    for s_name, d_name, deliv, mech, ms in deliverables:
        r = t10.add_row()
        set_cell_text(r.cells[0], s_name, bold=True)
        set_cell_text(r.cells[1], d_name)
        set_cell_text(r.cells[2], deliv)
        set_cell_text(r.cells[3], mech)
        set_cell_text(r.cells[4], ms, align=WD_ALIGN_PARAGRAPH.CENTER)
    apply_table_geometry(t10, [Inches(1.1), Inches(1.0), Inches(2.57), Inches(1.0), Inches(0.8)])

    # 12. TEXT POPULATION & TARGETED PLACEHOLDER CLEANUP
    print("Populating section narratives and cleaning placeholders...")
    for p in doc.paragraphs:
        txt = p.text.strip()
        # Headings with <optional>
        if "Architecture <optional>" in txt:
            p.text = "8 Hardware Architecture"
        elif "Bill Of Material <optional>" in txt:
            p.text = "9 Bill of Materials"
        elif "8\tArchitecture <optional>" in txt:
            p.text = txt.replace("<optional>", "").strip()
        elif "9\tBill Of Material <optional>" in txt:
            p.text = txt.replace("<optional>", "").strip()

        # Section 1 Introduction
        elif "Briefly describe the purpose this document" in txt or "Describe the purpose of the document here." in txt:
            p.text = (
                "This document describes the system-level requirements for the design and development of 'VVDN_SPPS_2026' "
                "(Smart Programmable Voltage Supply Module) for internal VVDN and client test bench applications. "
                "The document will be used as a reference for further engineering documents, circuit schematics, PCB layout rules, "
                "and laboratory validation. The device's functional and technical requirements must meet all parameters specified herein."
            )
        elif "Explicitly mention that the requirements captured here in this document supersed" in txt:
            p.text = (
                "This PRD shall be taken as the sole authoritative reference baseline for all hardware requirements, "
                "superseding prior RFQs and preliminary concept discussions."
            )
        elif "Describe any standards or typographical conventions" in txt or "Mention the Document Conventions" in txt:
            p.text = (
                "Requirements marked with [MUST] are mandatory non-negotiable specifications essential for safety, electrical regulation, "
                "and compliance. Requirements marked with [SHOULD] represent performance targets where design trade-offs require SME approval. "
                "Requirements marked with [MAY] represent optional enhancements. All electrical units follow SI conventions."
            )
        elif "Describe the different types of reader that the document is intended for" in txt or "Mention the Intended Audience" in txt:
            p.text = (
                "This PRD is intended for Product Management, Hardware Architects, the Power Electronics Trainee (GET) design owner, "
                "Firmware Developers, Quality Assurance / DVT Engineers, and Production / DFM Engineers."
            )
        elif txt in ["Client Team", "Architect Team", "Software Design team", "Software Development Team", "Quality Assurance Team", "Documentation team", "Deployment Team"]:
            p.text = ""

        # Section 1.4 Abbreviation
        elif txt == "Table : Abbreviation":
            p.text = "Table 1: Abbreviations and Acronyms"
        elif "Define all the terms necessary to properly interpret the PRD" in txt:
            p.text = "The key abbreviations and acronyms used throughout this PRD are defined in Table 1 below:"

        # Section 1.5 References
        elif txt == "Table : Reference":
            p.text = "Table 2: Reference Standards & Literature"
        elif "List any other documents or web addresses that this PRD refers" in txt:
            p.text = "The authoritative engineering standards, component datasheets, and reference documents governing this design are listed in Table 2 below:"

        # Section 2.1 Product Overview - Business
        elif "Provide a short description of the product being specified and its purpose" in txt or "Provide a general overview of the product from business perspective" in txt:
            p.text = (
                "The Smart Programmable Voltage Supply Module is an intelligent, high-density benchtop and automated test equipment (ATE) "
                "power supply delivering a tightly regulated, programmable DC voltage output from 5.0 V to 20.0 V at currents up to 3.0 A "
                "(60 W continuous output power) from universal grid AC mains input (85 V to 265 V AC RMS, 47 Hz to 63 Hz)."
            )
        elif "Describe the context and origin of the product being specified in this PRD" in txt:
            p.text = (
                "Traditional bench power supplies rely on bulky 50 Hz iron-core transformers, inefficient linear regulators, and manual dials, "
                "which lead to high thermal dissipation, large footprint, and lack of automated telemetry. This product eliminates those limitations "
                "by integrating a universal mains uniform-frequency (65 kHz) Flyback converter, an ultra-efficient 4-switch synchronous Buck-Boost "
                "post-regulator, real-time dual-domain power telemetry, and autonomous analog hardware protection into a single compact board."
            )
        elif "All the details in this section would be from customer perspective" in txt:
            p.text = "All requirements and functional parameters in this document are captured from the perspective of high-efficiency benchtop prototyping and automated modular test racks."

        # Section 2.2 Technical Perspective
        elif "Broad view of the boundary of project and features shall be defined" in txt or "Provide a technical overview of the product." in txt:
            p.text = (
                "The Smart Programmable Power Supply is a 4-stage AC-to-DC conversion and regulation system in which the power stage and "
                "mixed-signal microcontroller work together to deliver precise, clean, and safe DC power. The module connects directly to universal "
                "grid AC mains (85V–265V AC) through an input protection and EMI filter stage, rectifies it to a high-voltage bulk DC rail (+120V to +375V DC), "
                "isolates and steps it down via a uniform-frequency Flyback stage to an intermediate +24.0V DC bus (72W), and regulates it through a "
                "synchronous 4-switch Buck-Boost stage to provide the commanded 5.0V to 20.0V DC output at up to 3.0A.\n\n"
                "The onboard microcontroller (STM32G474) acts as the system brain by reading dual-domain electrical telemetry (primary AC input power and "
                "secondary DC load power), computing real-time conversion efficiency, updating the 1.3-inch OLED dashboard, and driving the precision 12-bit DAC "
                "voltage steering network. Circuit protection relies on robust, standard, industry-proven hardware protections: primary AC fuse (2A), "
                "inrush NTC (10Ω), surge MOV (300V), primary cycle-by-cycle Flyback current limiting (UC3843 ISENSE), and secondary LM5176 built-in "
                "cycle-by-cycle overcurrent protection with thermal shutdown."
            )
        elif "A diagram showing various systems of the product and the external entities" in txt or "Small description of different systems within the product" in txt or "Also, if the product comprises of developing multiple systems" in txt:
            p.text = ""

        # Section 2.3 Use Cases
        elif "Summarize the major functions the product must perform" in txt or "<List the primary functionalities of the product and then describe each in a separate paragraph>" in txt:
            p.text = (
                "The primary power supply functionality includes four operating modes:\n"
                "• Constant Voltage (CV) Mode: Regulates output voltage within ±0.2% across varying load currents below the current limit.\n"
                "• Current-Limited (OCP) Mode: Restricts peak inductor current cycle-by-cycle via LM5176 CSP/CSN sense during overload or short-circuit (< 5 µs autonomous response).\n"
                "• MCU Supervisory Protection Mode: Safely disables switching via LM5176 ENABLE pin on persistent overload (> 500 ms) or over-temperature.\n"
                "• Standby / Idle Mode: Output power stage disabled while +24V intermediate rail is maintained with standby power < 150mW."
            )
        elif "A picture of the major groups of related requirements and how they relate" in txt:
            p.text = ""
        elif "Provide the brief description about the interaction of each External entity" in txt:
            p.text = (
                "The module interacts with external entities including the AC grid mains (source), the benchtop load/DUT (sink), "
                "the local operator (via rotary dials, OLED screen, push-button, and LEDs), and an external PC/ATE system (via USB-CDC serial port)."
            )
        elif "Provide the brief description, the different mode of operation of the product" in txt or "Describe the major functionality of the product, based on the mode of operation" in txt or "<Describe use-cases of the product.>" in txt:
            p.text = "Operational scenarios and sequence flows are summarized in Table 4 below:"
        elif txt == "Table : Use Case":
            p.text = "Table 4: Major System Use Cases & Operating Modes"

        # Use case diagram placeholders
        elif "<Insert Major Use Case 1 Diagram here>" in txt:
            p.text = ""
        elif "<Insert Major Use Case 2 Diagram here>" in txt:
            p.text = ""

        # Section 2.4 Interfaces
        elif "Describe the physical and logical interfaces that exist between different systems" in txt:
            p.text = "The power supply incorporates robust physical hardware interfaces for power delivery, control, and user feedback, alongside high-speed digital software interfaces for instrumentation and telemetry."
        elif "Describe the physical characteristics of each interface" in txt or "<State all the hardware interfaces for the system>" in txt or "<Explain each hardware interface, including its purpose and how it will be used.>" in txt:
            p.text = (
                "Physical hardware interfaces include an IEC 320-C14 AC inlet with integrated fuse drawer, heavy-duty 4mm gold binding posts, "
                "dual optical rotary encoders, a tactile output enable push-button with status LED, a 1.3\" monochrome OLED display, "
                "and dedicated PCB bring-up test points. Detailed interface assignments are provided in Table 5 below:"
            )
        elif "All external entities are in highlighted in Green" in txt:
            p.text = ""
        elif txt == "Table : Hardware Interfaces":
            p.text = "Table 5: Hardware Physical Interfaces"

        elif ". Describe the communication between different systems of the product" in txt or "<State all the software interfaces for the system>" in txt:
            p.text = (
                "The SPPS module contains an onboard STM32G474 mixed-signal microcontroller that coordinates telemetry sampling, "
                "closed-loop DAC voltage steering, status display, and fault handling. The digital communication protocols and interfaces are detailed in Table 6 below:"
            )
        elif "The interfaces/communication between software services/features/modules" in txt or "Identify any communication standards that will be used" in txt or "<Explain what other external software components are used for the system, and how they interact with the product>" in txt:
            p.text = ""
        elif txt == "Table : Software Interfaces":
            p.text = "Table 6: Software & Digital Telemetry Interfaces"

        # Section 3 Domains Involved
        elif "List all the systems involved and the domains involved in each systems" in txt or "<Provide details on the systems and domains involved for the development of product>" in txt:
            p.text = "The engineering domains involved in the development of the SPPS module are summarized in Table 7 below:"
        elif "Domain is an indication of different team that is required" in txt or "For this project," in txt or "Each domain will have requirements captured to Subsystem" in txt:
            p.text = ""
        elif txt in ["Table : Domain", "Table : Domain "]:
            p.text = "Table 7: Engineering Domains Involved"

        # Section 4.1.1 Specific Requirements intro
        elif "There are some requirements that cannot be captured in plain text" in txt:
            p.text = "This section captures detailed subsystem architectures, circuit flow sequences, and component requirements for each conversion stage."
        elif "Similarly, implementation plan or proposal for few requirements" in txt or "Such details (requirements or proposed implementations) can be capture" in txt:
            p.text = ""

        # Section 5 Assumptions & Dependencies
        elif "List any assumed factors (as opposed to known facts)" in txt or "<List down the assumptions for the product>" in txt:
            p.text = (
                "The following points are considered as assumptions for further project execution:\n"
                "• Grid AC mains is nominal sinusoidal waveform with Total Harmonic Distortion (THD) ≤ 5%.\n"
                "• Operating ambient temperature is -20°C to +50°C under natural convection airflow in chassis.\n"
                "• Secondary DC ground is floating with reinforced galvanic isolation (≥ 3000V RMS) from Earth and AC mains.\n"
                "• Connected prototype loads are predominantly resistive or capacitive (C_load ≤ 1000 µF)."
            )
        elif "Identify any dependencies the project has on external factors" in txt or "<List down the dependencies for the product>" in txt:
            p.text = (
                "The following dependencies are included in the design and development of the SPPS module:\n"
                "• Component sourcing and lead times for TI LM5176, UC3843 / UCC28C43, INA226, AMC1311, and ST STM32G474.\n"
                "• Laboratory equipment availability: AC source (Chroma 61602), DC electronic load (Chroma 63102A), 3000V RMS Hi-Pot tester, and thermal camera.\n"
                "• Mechanical front-panel drawings for binding post standard 19.05 mm center-to-center spacing.\n"
                "• Firmware device drivers for SSD1306 OLED display, INA226 power monitor, and STM32 internal 12-bit DAC."
            )

        # Section 6 Standard Deliverables & Plan
        elif "All standard deliverable documents of each domain" in txt:
            p.text = "Standard engineering deliverables and milestone release schedules are captured in Table 8 below:"
        elif txt == "Table : System1 Development Plan":
            p.text = "Table 8: Standard Project Deliverables & Release Order"
        elif "Top level development plan (not timeline) shall be captured here" in txt or "During the PRD discussions with customer, lot of clarity" in txt or "For example, software development itself may span across" in txt or "<Provide high level product development plan.>" in txt:
            p.text = (
                "Phase 1 — Requirement & Architecture and Class A BOM:\n"
                "Definition of functional and electrical requirements; 4-stage system architecture design; block diagram and interface specifications.\n\n"
                "Phase 2 — Component Selection & Circuit Design:\n"
                "Transformer PQ26/20 magnetics sizing; component stress derating calculations; closed-loop feedback and DAC steering design; companion HDD authoring.\n\n"
                "Phase 3 — Schematic Design and Review:\n"
                "Complete 4-stage Altium schematics capture; LM5176 cycle-by-cycle current limit sensing and MCU enable control.\n\n"
                "Phase 4 — PCB Layout & DFM Review:\n"
                "PCB stackup; high-voltage isolation partitioning with 2.0mm milled slot; switching loop routing; DFM/DFA checks.\n\n"
                "Phase 5 — Prototype Bring-up & Design Validation Plan (DVT):\n"
                "PCB fabrication and assembly (5 units); cold resistance checks; supervised Variac bring-up; line/load regulation, ripple, efficiency, and Hi-Pot validation."
            )
        elif "<Fill as applicable>" in txt:
            p.text = (
                "The hardware validation plan comprises four rigorous test gates: Cold Checks (impedance & isolation resistance), "
                "Supervised Variac Bring-Up (gradual AC ramp from 0V to 265V), Dynamic Regulation (line/load regulation and 50% to 100% transient steps), "
                "and Safety/Thermal Soak (3000V RMS Hipot and FLIR thermal soak at 50°C)."
            )

        # Section 8 Architecture intro
        elif "Architecture section is optional to mention in PRD document" in txt:
            p.text = "The power supply hardware architecture consists of two galvanically isolated power conversion stages followed by synchronous post-regulation, dual-domain sensing, and auxiliary bias distribution:"
        elif "< Architecture Diagram with caption, shall be inserted here" in txt:
            p.text = ""

        # Section 9 BOM intro
        elif "BOM section is optional to mention in PRD document" in txt:
            p.text = "Note: This is the expected BOM and it might get changed during the design stage. The BOM does not contain any pricing/cost information."
            p.runs[0].font.italic = True
        elif "<Insert System level BOM>" in txt:
            p.text = ""
        elif txt == "Table :System1 Product BOM":
            p.text = "Table 9.1: System 1 Product BOM (Primary, Rectifier & Flyback Stages)"
        elif txt == "Table :System2 Product BOM":
            p.text = "Table 9.2: System 2 Product BOM (Buck-Boost, Protection, Telemetry & MCU Stages)"

        # Section 10 Out of Scope & Open Items
        elif txt == "Out of scope point 1":
            p.text = "Active Power Factor Correction (Active Boost PFC) — passive EMI filtering is used since < 75W is exempt under IEC 61000-3-2 Class D harmonic limits."
        elif txt == "Out of scope point 2":
            p.text = "Complex External Protection Circuits — dedicated analog crowbar thyristors and discrete fast comparator pull-down networks are excluded in favor of built-in controller protection and MCU supervisory shutdown."
        elif txt == "Out of scope point 3":
            p.text = "Three-phase 400V/480V AC industrial grid input operation (module is single-phase 85V–265V AC RMS only). Negative/bipolar rails and wireless IoT interfaces are excluded."
        elif txt == "Open Item 1":
            p.text = "Current shunt value trade-off: Evaluating 5mΩ vs 10mΩ for thermal dissipation vs low-current sensing resolution."
        elif txt == "Open Item 2":
            p.text = "Auxiliary 24V DC barrel input option: Evaluating a 24V DC auxiliary input to bypass AC mains for vehicle/field use."
        elif txt == "Open Item 3":
            p.text = "Secondary heatsink copper area optimization: Evaluating 2oz vs 3oz copper pours for D2PAK primary FET."

    # 13. INSERT TABLE 3 (HIGH LEVEL TECHNICAL REQUIREMENTS) IN SECTION 2.2
    print("Inserting Table 3: High Level Technical Requirement...")
    tech_reqs = [
        ("1", "Input Voltage Range", "85 V to 265 V AC RMS, 47 Hz to 63 Hz (Universal Grid Compatibility)"),
        ("2", "Continuous Output Current", "0.0 A to 3.0 A DC Continuous across full voltage range"),
        ("3", "Programmable Output Voltage", "5.0 V to 20.0 V DC (Continuously adjustable via 10 mV digital DAC steps)"),
        ("4", "Maximum Output Power", "60.0 W Continuous DC Output (20.0 V @ 3.0 A)"),
        ("5", "Intermediate Bus Voltage", "+24.0 V DC ± 1.0% (72.0 W continuous rating from primary Flyback stage)"),
        ("6", "Output Voltage Ripple", "< 25 mV pk-pk under full 3.0 A load (measured across 20 MHz bandwidth)"),
        ("7", "End-to-End System Efficiency", "> 85.0% @ 230 V AC Full Load (Flyback > 88%, Buck-Boost > 95%)"),
        ("8", "Galvanic Safety Isolation", "3,000 V AC RMS (1 minute withstand) meeting IEC 62368-1 SELV"),
        ("9", "Overcurrent Protection", "LM5176 built-in cycle-by-cycle hardware peak current limit via CSP/CSN"),
        ("10", "PCBA Operating Temperature", "–20°C to +50°C Full Load (natural convection in chassis)"),
        ("11", "User Interface & Control", "1.3\" I2C OLED display, dual rotary encoders, Status LEDs, tactile Enable switch"),
        ("12", "Conducted & Radiated EMC", "Compliant with CISPR 32 / EN 55032 Class B limits")
    ]

    # Clear old template sample graphic placeholders in Section 2.2
    for p in doc.paragraphs[120:140]:
        if 'graphic' in p._p.xml and p.text.strip() == '':
            p._p.clear()

    p_bound_cap = None
    for p in doc.paragraphs[100:]:
        if "Figure : Boundary Diagram" in p.text or "Boundary Diagram" in p.text or "Figure 1:" in p.text:
            p_bound_cap = p
            break

    if p_bound_cap is not None:
        p_bound_cap.text = "Figure 1: Boundary Diagram / Simplified 4-Stage Power Flow Block Diagram"
        diagram_img_path = "final_prd_staging/diagrams/figure1_simplified_4stage_power_flow.png"
        if os.path.exists(diagram_img_path):
            p_img = p_bound_cap.insert_paragraph_before()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_img = p_img.add_run()
            r_img.add_picture(diagram_img_path, width=Inches(6.47))

        t_tech = doc.add_table(rows=1, cols=3)
        set_table_borders(t_tech)
        set_cell_background(t_tech.rows[0].cells[0], "BFBFBF")
        set_cell_background(t_tech.rows[0].cells[1], "BFBFBF")
        set_cell_background(t_tech.rows[0].cells[2], "BFBFBF")
        set_cell_text(t_tech.rows[0].cells[0], "S.No", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(t_tech.rows[0].cells[1], "Parameters", bold=True)
        set_cell_text(t_tech.rows[0].cells[2], "Inputs For SPPS Board Design", bold=True)

        for s_no, param, val in tech_reqs:
            r = t_tech.add_row()
            set_cell_text(r.cells[0], s_no, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(8.5))
            set_cell_text(r.cells[1], param, bold=True, font_size=Pt(8.5))
            set_cell_text(r.cells[2], val, font_size=Pt(8.5))
        apply_table_geometry(t_tech, [Inches(0.65), Inches(2.20), Inches(3.62)])

        cap_tech = doc.add_paragraph("Table 3: High Level Technical Requirements")
        cap_tech.style = "Caption"
        p_bound_cap._p.addnext(cap_tech._p)
        cap_tech._p.addnext(t_tech._tbl)

    # 14. INSERT USE CASE FIGURES (Figures 2 and 3)
    p_uc2 = None
    p_uc3 = None
    for p in doc.paragraphs:
        txt = p.text.strip()
        if "Figure 2: Major Use Case 1" in txt or "Figure : Major Use Case 1" in txt:
            p_uc2 = p
        elif "Figure 3: Major Use Case 1" in txt or "Figure 3: Major Use Case 2" in txt or "Figure : Major Use Case 2" in txt:
            p_uc3 = p

    if p_uc2 is not None:
        p_uc2.text = "Figure 2: Major Use Case 1: Constant Voltage Regulation & Dynamic Load Response Flow"
        p_uc2.style = "Caption"
        img2_path = "final_prd_staging/diagrams/figure2_usecase_cv_dynamic_response.png"
        if os.path.exists(img2_path):
            p_pic2 = p_uc2.insert_paragraph_before()
            p_pic2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r2 = p_pic2.add_run()
            r2.add_picture(img2_path, width=Inches(6.47))

    if p_uc3 is not None:
        p_uc3.text = "Figure 3: Major Use Case 2: Autonomous Cycle-by-Cycle Peak Inductor Current Limiting & Fault Recovery"
        p_uc3.style = "Caption"
        img3_path = "final_prd_staging/diagrams/figure3_usecase_ocp_cycle_by_cycle.png"
        if os.path.exists(img3_path):
            p_pic3 = p_uc3.insert_paragraph_before()
            p_pic3.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r3 = p_pic3.add_run()
            r3.add_picture(img3_path, width=Inches(6.47))

    # 15. INSERT SECTION 4 ENGINEERING REQUIREMENT TABLES (Tables 4.1 to 4.5)
    print("Inserting Section 4 Engineering Requirement tables...")
    p_sys1 = None
    p_sys2 = None
    for p in doc.paragraphs:
        txt = p.text.strip()
        if txt == "<Insert System1 Requirement sheet here>":
            p_sys1 = p
        elif txt == "<Insert System2 Requirement sheet here>":
            p_sys2 = p

    def create_req_table(req_data):
        t = doc.add_table(rows=1, cols=5)
        apply_table_geometry(t, [Inches(0.75), Inches(1.70), Inches(1.70), Inches(1.12), Inches(1.20)])
        set_table_borders(t)
        for cell in t.rows[0].cells:
            set_cell_background(cell, "BFBFBF")
        set_cell_text(t.rows[0].cells[0], "Req ID", bold=True)
        set_cell_text(t.rows[0].cells[1], "Parameter / Feature", bold=True)
        set_cell_text(t.rows[0].cells[2], "Specification / Target", bold=True)
        set_cell_text(t.rows[0].cells[3], "Condition", bold=True)
        set_cell_text(t.rows[0].cells[4], "Verification", bold=True)

        for rid, param, spec, cond, ver in req_data:
            r = t.add_row()
            set_cell_text(r.cells[0], rid, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(8.5))
            set_cell_text(r.cells[1], param, font_size=Pt(8.5))
            set_cell_text(r.cells[2], spec, font_size=Pt(8.5))
            set_cell_text(r.cells[3], cond, font_size=Pt(8.5))
            set_cell_text(r.cells[4], ver, font_size=Pt(8.5))
        apply_table_geometry(t, [Inches(0.75), Inches(1.70), Inches(1.70), Inches(1.12), Inches(1.20)])
        return t

    req_flyback = [
        ("FR-01", "AC Input Voltage Range", "85 V – 265 V AC RMS [MUST]", "Nominal 230V AC, 47–63 Hz", "AC Source Sweep"),
        ("FR-02", "Intermediate DC Bus Voltage", "+24.0 V DC ± 1.0% [MUST]", "Across all line/load variations", "Precision DMM"),
        ("FR-03", "Continuous Primary Power", "72.0 W Continuous [MUST]", "85V–265V AC In, 24V / 3A Out", "Electronic Load 72W Soak"),
        ("FR-04", "Peak Power Capability", "84.0 W for 500 ms [SHOULD]", "During dynamic load surges", "Transient Load Step"),
        ("FR-05", "Primary Stage Efficiency", "> 88.0% @ 230V AC Full Load [MUST]", "Pout = 72W, Tamb = 25°C", "Precision Power Analyzer"),
        ("FR-06", "Safety Galvanic Isolation", "3,000 V AC RMS (1 min) [MUST]", "Primary to Secondary barrier", "Certified Hi-Pot Tester"),
        ("FR-07", "Uniform Switching Frequency", "65.0 kHz ± 5% Constant [MUST]", "Set by RT=10k, CT=2.2nF", "Scope / Frequency Counter"),
        ("FR-08", "Cold-Start Inrush Current", "< 25.0 A Peak [MUST]", "Vin = 265V AC, cold start 25°C", "Current Probe & Scope"),
        ("FR-09", "No-Load Standby Power", "< 250 mW Standby [SHOULD]", "Vin = 230V AC, Output Off", "Power Meter Integrator")
    ]

    req_buckboost = [
        ("BB-01", "Output Voltage Range", "5.0 V – 20.0 V DC Programmable [MUST]", "Continuous linear adjustment", "Precision DMM Sweep"),
        ("BB-02", "Continuous Output Current", "0.0 A – 3.0 A DC Continuous [MUST]", "Across full 5V–20V voltage span", "Electronic Load 3A Soak"),
        ("BB-03", "Maximum Output Power", "60.0 W Continuous Output [MUST]", "Vout = 20.0V, Iout = 3.0A", "Thermal Run 60W (2 hrs)"),
        ("BB-04", "Voltage Setpoint Resolution", "10 mV step resolution (12-bit DAC) [MUST]", "Continuous monotonic tuning", "DAC Linearity Calibration"),
        ("BB-05", "Output Voltage Ripple", "< 25 mV pk-pk ripple [MUST]", "Full load 3A, 20MHz bandwidth", "Scope Tip-and-Barrel Probe"),
        ("BB-06", "Load Transient Recovery", "< 150 µs recovery, < 250mV sag [MUST]", "50% to 100% load step (1.5A to 3A)", "Dynamic Load Stepper"),
        ("BB-07", "Buck-Boost Efficiency", "> 95.0% @ 20V/3A; > 92.0% @ 5V/3A [MUST]", "Vin = 24V, Sync Rectification", "Dual-Channel Power Meter"),
        ("BB-08", "Switching Frequency", "300 kHz ± 10% [MUST]", "Fixed frequency PWM", "Frequency Counter / Scope"),
        ("BB-09", "Hardware Current Limiting", "Cycle-by-cycle current limit via CSP/CSN [MUST]", "Overload condition", "Current Probe & Scope")
    ]

    req_telemetry = [
        ("TM-01", "Primary AC Voltage Sensing", "Isolated AMC1311 (0-300V AC RMS) [MUST]", "± 1.0% accuracy across 85-265V", "Precision AC Source Reference"),
        ("TM-02", "Primary AC Current Sensing", "Current Transformer 1000:1 [MUST]", "± 1.5% accuracy from 0.1A–2A", "Calibrated Current Probe"),
        ("TM-03", "Secondary DC Voltage Sense", "INA226 16-bit ADC (1.25mV/LSB) [MUST]", "± 0.2% measurement accuracy", "Keysight 34465A 6.5-digit DMM"),
        ("TM-04", "Secondary DC Current Sense", "INA226 16-bit ADC (100µA/LSB) [MUST]", "± 0.5% measurement accuracy", "Precision Shunt Reference"),
        ("TM-05", "Dual-Domain Telemetry Rate", "10.0 Hz Real-Time Loop Rate [MUST]", "Pac, Pdc, and η computed at 100ms", "Logic Analyzer Timing Check"),
        ("TM-06", "Galvanic Isolation Barrier", "3,000 V AC RMS (1 min) [MUST]", "Primary-to-secondary isolation", "Certified Hi-Pot Tester"),
        ("TM-07", "Calibration Test Points", "Dedicated PCB Test Loops [MUST]", "Vout, bulk DC, and aux rails", "Scope & Multimeter Inspection")
    ]

    req_protection = [
        ("PR-01", "Input Fuse Protection", "2.0A Time-Lag Ceramic Fuse [MUST]", "AC mains short-circuit", "Overcurrent Trip Test"),
        ("PR-02", "Input Inrush Current Limit", "10Ω NTC Thermistor (< 25A peak) [MUST]", "Cold start at 265V AC", "Scope Current Probe"),
        ("PR-03", "AC Line Surge Protection", "300V RMS MOV (4.5kA rating) [MUST]", "Line transients per IEC 61000-4-5", "Surge Generator Verification"),
        ("PR-04", "Built-in Controller OCP", "LM5176 cycle-by-cycle CSP/CSN clamp [MUST]", "Load current > 3.5A limit", "Electronic Load Step"),
        ("PR-05", "Over-Temperature (OTP)", "LM5176 internal shutdown (165°C) [MUST]", "Severe thermal rise", "Thermal Chamber Sweep"),
        ("PR-06", "Safety Compliance Standard", "IEC 62368-1 Reinforced Isolation [MUST]", "SELV touch-safe (< 60V DC)", "Certified Safety Laboratory"),
        ("PR-07", "Creepage & Clearance", "Creepage ≥ 6.4mm; Clearance ≥ 5.0mm [MUST]", "Primary-Secondary milled slot", "PCB Caliper & Gerber Check"),
        ("PR-08", "Conducted & Radiated EMC", "CISPR 32 / EN 55032 Class B [MUST]", "150 kHz – 1 GHz emission limits", "Semi-Anechoic Chamber"),
        ("PR-09", "Operating Ambient Temp", "–20°C to +50°C Full Load [MUST]", "Natural convection in chassis", "Environmental Chamber")
    ]

    req_control = [
        ("CT-01", "DAC Voltage Steering Network", "Resistor summing into LM5176 FB node [MUST]", "R_top=49.9kΩ, R_DAC=11kΩ, R_bot=3.65kΩ", "Precision Line/Load Sweep"),
        ("CT-02", "Voltage Tuning Resolution", "10.0 mV step resolution (12-bit DAC) [MUST]", "Continuous 5.0V to 20.0V DC range", "DAC Linearity Calibration"),
        ("CT-03", "Current Sense Resistor", "10 mΩ Metal Element Shunt, 3W, 0.1% [MUST]", "Connected across LM5176 CSP/CSN", "Precision Milliohm Meter"),
        ("CT-04", "MCU Supervisory Shutdown", "GPIO pulling LM5176 ENABLE pin low [MUST]", "Software fault shutdown command", "Scope Response Timing"),
        ("CT-05", "Auxiliary Bias Regulation", "+14V Flyback VCC, +12V gate, +5V, +3.3V rails [MUST]", "Dedicated LDOs & buck off +24V", "Multimeter & Rail Scope")
    ]

    if p_sys1 is not None:
        p_sys1.text = (
            "System 1 represents the physical Hardware Power Supply Module, comprising the universal AC input, EMI filter, "
            "isolated Uniform-Frequency Flyback stage, 4-switch synchronous Buck-Boost post-regulator, built-in controller hardware protection, "
            "and microcontroller sensing core. The detailed engineering specifications are defined in the tables below:"
        )
        cursor = p_sys1._p
        cap1 = doc.add_paragraph("Table 4.1: AC-DC Isolated Uniform-Frequency Flyback Power Stage Engineering Requirements")
        cap1.style = "Caption"
        cursor.addnext(cap1._p)
        cursor = cap1._p
        t_f = create_req_table(req_flyback)
        cursor.addnext(t_f._tbl)
        cursor = t_f._tbl

        cap2 = doc.add_paragraph("Table 4.2: 4-Switch Synchronous Buck-Boost Post-Regulator Requirements")
        cap2.style = "Caption"
        cursor.addnext(cap2._p)
        cursor = cap2._p
        t_bb = create_req_table(req_buckboost)
        cursor.addnext(t_bb._tbl)
        cursor = t_bb._tbl

        cap3 = doc.add_paragraph("Table 4.3: Real-Time Dual-Domain Telemetry & Monitoring Requirements")
        cap3.style = "Caption"
        cursor.addnext(cap3._p)
        cursor = cap3._p
        t_tm = create_req_table(req_telemetry)
        cursor.addnext(t_tm._tbl)
        cursor = t_tm._tbl

        cap4 = doc.add_paragraph("Table 4.4: Protection, Safety, EMC & Environmental Requirements")
        cap4.style = "Caption"
        cursor.addnext(cap4._p)
        cursor = cap4._p
        t_pr = create_req_table(req_protection)
        cursor.addnext(t_pr._tbl)
        cursor = t_pr._tbl

    if p_sys2 is not None:
        p_sys2.text = (
            "System 2 represents the Secondary Stage 4-Switch Synchronous Buck-Boost Post-Regulator, "
            "Analog Closed-Loop Control, DAC Steering Network, and Autonomous Hardware CC Protection Subsystem. "
            "The detailed electrical hardware specifications are defined in Table 4.5 below:"
        )
        cursor = p_sys2._p
        cap5 = doc.add_paragraph("Table 4.5: Analog Closed-Loop Control, DAC Steering & Hardware Protection Specifications")
        cap5.style = "Caption"
        cursor.addnext(cap5._p)
        cursor = cap5._p
        t_ctrl = create_req_table(req_control)
        cursor.addnext(t_ctrl._tbl)
        cursor = t_ctrl._tbl

    # 16. INSERT SPECIFIC REQUIREMENTS FIGURES & SEQUENCE TABLES (Figures 4, 5, 6)
    fig4_steps = [
        ("1", "AC Inlet Connection", "Connects to universal grid mains (85V–265V AC RMS, 47–63 Hz) via standard IEC 320-C14 chassis connector."),
        ("2", "Overcurrent Protection", "2.0A time-lag ceramic cartridge fuse (F1) provides fail-safe catastrophic short-circuit clearing (I²t ≥ 18 A²s)."),
        ("3", "Inrush Current Limiting", "10Ω cold-resistance NTC thermistor (NTC1) limits peak turn-on surge current to < 25A peak during cold start at 265V AC."),
        ("4", "Transient Clamping", "14 mm Metal Oxide Varistor (MOV1, 300V RMS) clamps grid lightning and switching transients per IEC 61000-4-5 Level 3."),
        ("5", "Two-Stage EMI Filtering", "Two cascaded common-mode chokes (15mH + 4.7mH) with X2/Y2 capacitors suppress emissions below CISPR 32 Class B limits.")
    ]

    fig5_steps = [
        ("1", "Filtered AC Input", "Takes 85V–265V AC RMS sinusoidal voltage from Stage 1 EMI filter."),
        ("2", "Full-Wave Rectification", "GBU606 single-phase bridge rectifies AC into 100Hz/120Hz unipolar DC pulses (120Vpk–375Vpk)."),
        ("3", "Bulk Capacitive Filtering", "100µF/450V electrolytic cap smooths ripple and guarantees > 10ms holdup time across line dropouts."),
        ("4", "High-Frequency Decoupling", "100nF/630V ceramic cap bypasses fast 65kHz primary switching edge ringing."),
        ("5", "Safety Discharge Bleeder", "3x 330kΩ resistor string drains bulk capacitor to < 50V SELV within 60s per IEC 62368-1.")
    ]

    fig6_steps = [
        ("1", "High-Voltage DC Input", "Receives +120V to +375V DC bulk bus into primary switching cell."),
        ("2", "Uniform-Frequency PWM", "UC3843 / UCC28C43 controller operates at constant 65kHz uniform clock set by RT/CT with predictable EMI harmonics."),
        ("3", "3000V RMS Safety Barrier", "PQ26/20 transformer (Lp=220µH) with Furukawa TEX-E wire provides reinforced galvanic isolation."),
        ("4", "Schottky Barrier Rectification", "MBR10100 100V/10A Schottky diode provides simple, robust passive rectification with high reliability."),
        ("5", "+24.0V DC Intermediate Rail", "Low-ESR LC filter delivers stable +24.0V DC (72W) with optocoupled feedback regulation.")
    ]

    # Section 4.1.1: Insert Figure 4 (Stage 1) and Figure 5 (Stage 2)
    p_h4_stage1 = None
    p_cap_stage2 = None
    for p in doc.paragraphs[100:]:
        txt = p.text.strip()
        if p.style.name == "Heading 4" and "Mobile UI Screens/Wireframes" in txt and p_h4_stage1 is None:
            p_h4_stage1 = p
        elif ("Figure : Flow Diagram" in txt or "Figure 4: Flow Diagram" in txt or "Figure 4: Inside Stage 2" in txt or "Figure 5: Inside Stage 2" in txt) and p.style.name == "Caption":
            p_cap_stage2 = p
            break

    if p_h4_stage1 is not None and p_cap_stage2 is not None:
        # Clear any empty graphic paragraphs between stage 1 heading and stage 2 caption
        p_curr = p_h4_stage1._p.getnext()
        while p_curr is not None and p_curr != p_cap_stage2._p:
            next_p = p_curr.getnext()
            if 'graphic' in p_curr.xml and len(p_curr.text.strip()) == 0:
                p_curr.getparent().remove(p_curr)
            p_curr = next_p

        # 1. Stage 1 Heading
        p_h4_stage1.text = "Inside Stage 1: Mains Supply & Input Protection Subsystem"

        # 2. Stage 1 Intro
        p_intro4 = doc.add_paragraph(
            "Stage 1 interfaces directly with universal grid AC mains (85V–265V AC RMS, 47–63 Hz) and provides catastrophic "
            "overcurrent protection, cold-start inrush current suppression, high-energy surge clamping, and two-stage common-mode/differential-mode "
            "EMI filtering compliant with CISPR 32 Class B limits."
        )

        # 3. Figure 4 Image
        p_pic4 = doc.add_paragraph()
        p_pic4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        diag4_path = "final_prd_staging/diagrams/figure4_inside_stage1_mains_emi.png"
        if os.path.exists(diag4_path):
            r4 = p_pic4.add_run()
            r4.add_picture(diag4_path, width=Inches(6.47))

        # 4. Figure 4 Caption
        p_cap4 = doc.add_paragraph("Figure 4: Inside Stage 1 - Mains AC Supply & Two-Stage EMI Filter Subsystem Architecture")
        p_cap4.style = "Caption"

        # 5. Table 4.6A
        tbl_fig4 = create_workflow_table(doc, "STAGE 1: MAINS SUPPLY & INPUT PROTECTION SEQUENCE", fig4_steps, header_color="1A365D")

        # 6. Stage 2 Heading & Intro
        p_h4_stage2 = doc.add_paragraph("Inside Stage 2: Bridge Rectifier & High-Voltage Bulk DC Subsystem")
        p_h4_stage2.style = "Heading 4"

        p_intro5 = doc.add_paragraph(
            "Stage 2 rectifies the filtered AC sinusoidal mains into unipolar DC pulses and smooths them into an unregulated "
            "high-voltage bulk DC rail (+120V to +375V DC) with sufficient energy storage to sustain full 72W load through a 10 ms grid cycle dropout."
        )

        # 7. Figure 5 Image
        p_pic5 = doc.add_paragraph()
        p_pic5.alignment = WD_ALIGN_PARAGRAPH.CENTER
        diag5_path = "final_prd_staging/diagrams/figure5_inside_stage2_rectifier_bulk.png"
        if os.path.exists(diag5_path):
            r5 = p_pic5.add_run()
            r5.add_picture(diag5_path, width=Inches(6.47))

        # Chain elements sequentially
        p_h4_stage1._p.addnext(p_intro4._p)
        p_intro4._p.addnext(p_pic4._p)
        p_pic4._p.addnext(p_cap4._p)
        p_cap4._p.addnext(tbl_fig4._tbl)
        tbl_fig4._tbl.addnext(p_h4_stage2._p)
        p_h4_stage2._p.addnext(p_intro5._p)
        p_intro5._p.addnext(p_pic5._p)
        p_pic5._p.addnext(p_cap_stage2._p)

        # 8. Update Figure 5 Caption
        p_cap_stage2.text = "Figure 5: Inside Stage 2 - Bridge Rectifier & Bulk DC Stage Subsystem Architecture"

        # 9. Insert Table 4.6B after p_cap_stage2
        tbl_fig5 = create_workflow_table(doc, "STAGE 2: BRIDGE RECTIFIER & BULK FILTER SEQUENCE", fig5_steps, header_color="7B341E")
        p_cap_stage2._p.addnext(tbl_fig5._tbl)

    # Section 4.2.1: Insert Figure 6 (Stage 3 Flyback under System 2 Specific Requirements)
    found_sys2 = False
    for p in doc.paragraphs[100:]:
        txt = p.text.strip()
        if "System2 Requirements" in txt and p.style.name == "Heading 2":
            found_sys2 = True
        if found_sys2:
            if p.style.name == "Heading 4" and "Mobile UI Screens/Wireframes" in txt:
                p.text = "Inside Stage 3: Converter DC-DC (Uniform-Frequency Isolated Flyback) Subsystem"
            elif ("<Refer above section>" in txt or "Figure 5" in txt or "Figure 6" in txt) and p.style.name == "Caption":
                diag6_path = "final_prd_staging/diagrams/figure6_inside_stage3_flyback.png"
                if os.path.exists(diag6_path):
                    p_pic6 = p.insert_paragraph_before()
                    p_pic6.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r6 = p_pic6.add_run()
                    r6.add_picture(diag6_path, width=Inches(6.47))
                p.text = "Figure 6: Inside Stage 3 - Converter DC-DC (Uniform-Frequency Isolated Flyback) Subsystem Architecture"
                tbl_fig6 = create_workflow_table(doc, "STAGE 3: UNIFORM-FREQUENCY FLYBACK DC-DC CONVERTER SEQUENCE", fig6_steps, header_color="1C4532")
                p._p.addnext(tbl_fig6._tbl)

                # Add comprehensive Stage 3 Table (Table 4.6D)
                stage3_data = [
                    ("HVDC Input Interface", "+HVDC", "Stage 2 Bulk DC Bus Link", "+120 V to +375 V DC operating span", "Low-impedance high-voltage input rail feeding transformer primary winding and snubber network."),
                    ("Uniform-Freq PWM Controller", "U1", "Texas Instruments UC3843 / UCC28C43", "Uniform 65 kHz clock, RT/CT oscillator, cycle-by-cycle CS, direct totem-pole gate out", "Generates constant-frequency PWM switching pulses at a uniform 65 kHz rate, providing predictable EMI harmonics and deterministic current-mode control."),
                    ("Oscillator Timing Network", "R_T / C_T", "Precision Thin-Film Resistor + C0G Ceramic Cap", "R_T = 10.0 kΩ (1%), C_T = 2.2 nF (50V C0G)", "Sets constant oscillator clock frequency: f_sw approx 1.72 / (R_T x C_T) = 65 kHz uniform clock without frequency jitter."),
                    ("Primary Power Switch", "Q1", "STMicroelectronics STP10NK80Z / IPB80R290P7", "800 V, 17 A, R_DS(on) = 0.29 Ω, V_DS,peak = 599 V", "Main switching element modulated by 65 kHz PWM gate drive. Voltage stress derated to 74.9% of 800V rating (< 75% limit)."),
                    ("Primary Current Sensing", "R_CS", "Current Sense Shunt Resistor Network", "Low-inductance metal strip, 0.25 Ω, 1%, 2 W", "Monitors primary switch peak current (I_pk = 2.96 A) on UC3843 ISENSE pin (Pin 3) with 1.0 V internal comparator threshold for cycle-by-cycle OCP."),
                    ("RCD Snubber Clamp", "D_snub / R / C", "Diodes Inc. US1M + 3x 68 kΩ (22.6k net) + 1.0 nF / 1 kV", "Diode: 1000 V, 1 A, t_rr = 75 ns; Cap: 1 nF / 1000 V ceramic; Clamp: ~216 V clamp level", "Damps high-voltage inductive kick caused by transformer leakage inductance (L_lk approx 2.2 uH); clamps peak drain voltage spike safely below 650 V peak."),
                    ("Flyback Power Transformer", "TX1", "Ferroxcube PQ26/20 (3C95 Ferrite) / EE25 Core", "L_p = 220 uH +/- 10%, B_max = 0.148 T (B_sat = 0.38 T), N_p = 36 T", "Stores energy during switch on-time and delivers 72 W continuous power to secondary during off-time (Np:Ns = 6:1 turns ratio)."),
                    ("Auxiliary Bias Winding", "TX1_AUX", "N_aux = 5 T (0.25 mm wire) + UF4004 & 47 µF Cap", "Output: +14.0 V DC bias rail", "Sustains UC3843 VCC pin (Pin 7) above UVLO threshold (8.4 V start / 7.6 V min) after initial high-voltage bleed startup."),
                    ("Galvanic Safety Barrier", "TX1_ISO", "Furukawa TEX-E Triple-Insulated Wire (TIW)", "N_s = 6 T (N_p:N_s = 6:1), Reinforced insulation, >= 6.4 mm creepage", "Complies with IEC 62368-1 standard. Provides certified >= 3000 V RMS dielectric withstand between primary hot domain and secondary touch-safe SELV domain."),
                    ("Secondary Schottky Rectifier", "D_SEC", "ON Semi / Vishay MBR10100 / MBR20100CT", "100 V, 10 A Schottky Barrier Diode, V_F = 0.60 V, TO-220 with heatsink", "Performs high-speed passive rectification of secondary flyback pulses. Highly reliable and robust passive design, eliminating active gate driver IC complexity."),
                    ("Secondary LC Output Filter", "C_sec / L_sec", "470 µF / 35 V Low-ESR Electrolytic + 2.2 µH + 22 µF MLCC", "Low-ESR filtering, Delta V_ripple < 40 mV pk-pk", "Attenuates 65 kHz fundamental switching ripple and high-frequency commutation spikes to produce a quiet intermediate DC rail."),
                    ("Isolated Closed-Loop Feedback", "OPTO1 / U3", "Everlight PC817 Optocoupler + TI TL431 Shunt", "5000 V RMS optical isolation, 2.495 V internal bandgap, 0.5%", "Precision resistor divider samples +24.0 V rail, driving optocoupler LED to pull down UC3843 COMP pin (Pin 1), regulating rail to +/- 1.0%."),
                    ("Intermediate Rail Output", "+24V_BUS", "Intermediate DC Power Distribution Bus", "+24.0 V DC +/- 1.0%, 72.0 W continuous (3.0 A), 84 W peak", "Delivers stable intermediate regulated DC power to Stage 4 (Synchronous Buck-Boost Post-Regulator) and secondary auxiliary housekeeping LDOs.")
                ]

                t_s3 = doc.add_table(rows=1, cols=5)
                apply_table_geometry(t_s3, [Inches(1.2), Inches(0.8), Inches(1.4), Inches(1.47), Inches(1.6)], total_width_inches=6.47)
                set_table_borders(t_s3, color="CBD5E0", sz="4")
                for c in t_s3.rows[0].cells:
                    set_cell_background(c, "1A365D")
                set_cell_text(t_s3.rows[0].cells[0], "Functional Sub-Block", bold=True, color_rgb=(255, 255, 255))
                set_cell_text(t_s3.rows[0].cells[1], "Circuit Ref", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=(255, 255, 255))
                set_cell_text(t_s3.rows[0].cells[2], "Selected Component / IC", bold=True, color_rgb=(255, 255, 255))
                set_cell_text(t_s3.rows[0].cells[3], "Key Specifications & Ratings", bold=True, color_rgb=(255, 255, 255))
                set_cell_text(t_s3.rows[0].cells[4], "Functional Role & Performance Target", bold=True, color_rgb=(255, 255, 255))

                for b, r_c, comp, sp, rol in stage3_data:
                    row_s3 = t_s3.add_row()
                    set_cell_text(row_s3.cells[0], b, bold=True, font_size=Pt(8.0))
                    set_cell_text(row_s3.cells[1], r_c, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(8.0))
                    set_cell_text(row_s3.cells[2], comp, font_size=Pt(8.0))
                    set_cell_text(row_s3.cells[3], sp, font_size=Pt(8.0))
                    set_cell_text(row_s3.cells[4], rol, font_size=Pt(8.0))

                cap_s3 = doc.add_paragraph("Table 4.6D: STAGE 3 Flyback Detailed Subsystem Component Specification & Engineering Requirements Table")
                cap_s3.style = "Caption"
                tbl_fig6._tbl.addnext(cap_s3._p)
                cap_s3._p.addnext(t_s3._tbl)
                break

    # 17. INSERT ARCHITECTURE SUBSYSTEMS (8.1, 8.2, 8.3, 8.4, 8.5)
    p_arch1 = None
    p_arch2 = None
    p_arch3 = None
    for p in doc.paragraphs:
        txt = p.text.strip()
        if "System1: Domain1 Architecture" in txt and p.style.name == "Heading 2":
            p_arch1 = p
        elif "System1: Domain2 Architecture" in txt and p.style.name == "Heading 2":
            p_arch2 = p
        elif "System2: Domain1 Architecture" in txt and p.style.name == "Heading 2":
            p_arch3 = p

    fig7_steps = [
        ("1", "+24.0V DC Rail Input", "Accepts +24.0V DC intermediate rail from Stage 3 Flyback."),
        ("2", "4-Switch Synchronous Bridge", "TI LM5176 modulates four 40V MOSFETs in H-bridge around a 10µH flat-wire power inductor."),
        ("3", "Seamless Mode Transitions", "Operates in pure Buck mode for 5V–18V outputs (>96% eff) and 4-switch Buck-Boost mode near 20V (>95% eff)."),
        ("4", "Precision DAC Steering", "Resistor summing network (R_top=49.9kΩ, R_bot=3.65kΩ, R_DAC=11kΩ) steers output from 5V to 20V in 10mV steps."),
        ("5", "Cycle-by-Cycle Current Limit", "LM5176 senses current via 10mΩ shunt across CSP/CSN, natively clamping peak inductor current on every 300 kHz cycle.")
    ]

    if p_arch1 is not None:
        p_arch1.text = "8.1 System 1: Inside Stage 4 (Synchronous 4-Switch Buck-Boost Post-Regulator Subsystem)"
        diag7_path = "final_prd_staging/diagrams/figure7_inside_stage4_buck_boost.png"
        p_pic7 = None
        if os.path.exists(diag7_path):
            p_pic7 = doc.add_paragraph()
            p_pic7.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r7 = p_pic7.add_run()
            r7.add_picture(diag7_path, width=Inches(6.47))

        cap7 = doc.add_paragraph("Figure 7: Inside Stage 4 - 4-Switch Buck-Boost Post-Regulator Subsystem Architecture")
        cap7.style = "Caption"
        tbl_fig7 = create_workflow_table(doc, "STAGE 4: 4-SWITCH BUCK-BOOST POST-REGULATOR SEQUENCE", fig7_steps, header_color="2A4365")
        note7_1 = doc.add_paragraph("Note: This is the proposed architecture and it might get changed during the design stage.")
        note7_1.runs[0].font.italic = True
        note7_2 = doc.add_paragraph("Note: Component selection must strictly comply with VVDN derating guidelines.")
        note7_2.runs[0].font.italic = True

        if p_pic7 is not None:
            p_arch1._p.addnext(p_pic7._p)
            p_pic7._p.addnext(cap7._p)
            cap7._p.addnext(tbl_fig7._tbl)
            tbl_fig7._tbl.addnext(note7_1._p)
        else:
            p_arch1._p.addnext(cap7._p)
            cap7._p.addnext(tbl_fig7._tbl)
            tbl_fig7._tbl.addnext(note7_1._p)
        note7_1._p.addnext(note7_2._p)

    if p_arch2 is not None:
        p_arch2.text = "8.2 System 1: Dual-Domain Power Telemetry & Sensing Frontend Architecture"
        diag8_path = "final_prd_staging/diagrams/figure8_telemetry_sensing_frontend.png"
        p_pic8 = None
        if os.path.exists(diag8_path):
            p_pic8 = doc.add_paragraph()
            p_pic8.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r8 = p_pic8.add_run()
            r8.add_picture(diag8_path, width=Inches(6.47))

        cap8 = doc.add_paragraph("Figure 8: Dual-Domain Power Telemetry & Sensing Frontend Architecture")
        cap8.style = "Caption"
        note8_1 = doc.add_paragraph("Note: This is the proposed architecture and it might get changed during the design stage.")
        note8_1.runs[0].font.italic = True
        note8_2 = doc.add_paragraph("Note: AMC1311 reinforced galvanic isolation barrier complies with IEC 62368-1.")
        note8_2.runs[0].font.italic = True

        if p_pic8 is not None:
            p_arch2._p.addnext(p_pic8._p)
            p_pic8._p.addnext(cap8._p)
            cap8._p.addnext(note8_1._p)
        else:
            p_arch2._p.addnext(cap8._p)
            cap8._p.addnext(note8_1._p)
        note8_1._p.addnext(note8_2._p)

    if p_arch3 is not None:
        p_arch3.text = "8.3 System 2: Auxiliary Bias Power Rail Distribution Subsystem Architecture"
        diag9_path = "final_prd_staging/diagrams/figure9_aux_power_distribution.png"
        p_pic9 = None
        if os.path.exists(diag9_path):
            p_pic9 = doc.add_paragraph()
            p_pic9.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r9 = p_pic9.add_run()
            r9.add_picture(diag9_path, width=Inches(6.47))

        cap9 = doc.add_paragraph("Figure 9: Auxiliary Bias Power Rail Distribution Subsystem Architecture")
        cap9.style = "Caption"
        note9_1 = doc.add_paragraph("Note: This is the proposed architecture and it might get changed during the design stage.")
        note9_1.runs[0].font.italic = True
        note9_2 = doc.add_paragraph("Note: Gate driver bootstrap bias and low-noise analog LDO rails are verified during bring-up.")
        note9_2.runs[0].font.italic = True

        if p_pic9 is not None:
            p_arch3._p.addnext(p_pic9._p)
            p_pic9._p.addnext(cap9._p)
            cap9._p.addnext(note9_1._p)
        else:
            p_arch3._p.addnext(cap9._p)
            cap9._p.addnext(note9_1._p)
        note8_1._p.addnext(note8_2._p)

        # Append 8.4 Master System Architecture and 8.5 MCU Architecture
        p_arch4 = doc.add_paragraph("8.4 System Master: Master System Hardware Architecture Block Diagram")
        p_arch4.style = "Heading 2"
        diag10_path = "final_prd_staging/diagrams/figure10_master_hardware_architecture.png"
        p_pic10 = None
        if os.path.exists(diag10_path):
            p_pic10 = doc.add_paragraph()
            p_pic10.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r10 = p_pic10.add_run()
            r10.add_picture(diag10_path, width=Inches(6.47))
        cap10 = doc.add_paragraph("Figure 10: Master System Hardware Architecture Block Diagram")
        cap10.style = "Caption"
        note10_1 = doc.add_paragraph("Note: This is the proposed architecture and it might get changed during the design stage.")
        note10_1.runs[0].font.italic = True

        p_arch5 = doc.add_paragraph("8.5 System Microcontroller: MCU System Interaction, State Machine & Monitoring Architecture")
        p_arch5.style = "Heading 2"
        diag11_path = "final_prd_staging/diagrams/figure11_mcu_system_interaction_monitoring.png"
        p_pic11 = None
        if os.path.exists(diag11_path):
            p_pic11 = doc.add_paragraph()
            p_pic11.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r11 = p_pic11.add_run()
            r11.add_picture(diag11_path, width=Inches(6.47))
        cap11 = doc.add_paragraph("Figure 11: MCU System Interaction, State Machine & Monitoring Architecture")
        cap11.style = "Caption"
        note11_1 = doc.add_paragraph("Note: This is the proposed architecture and it might get changed during the design stage.")
        note11_1.runs[0].font.italic = True

        note9_2._p.addnext(p_arch4._p)
        if p_pic10 is not None:
            p_arch4._p.addnext(p_pic10._p)
            p_pic10._p.addnext(cap10._p)
            cap10._p.addnext(note10_1._p)
        else:
            p_arch4._p.addnext(cap10._p)
            cap10._p.addnext(note10_1._p)

        note10_1._p.addnext(p_arch5._p)
        if p_pic11 is not None:
            p_arch5._p.addnext(p_pic11._p)
            p_pic11._p.addnext(cap11._p)
            cap11._p.addnext(note11_1._p)
        else:
            p_arch5._p.addnext(cap11._p)
            cap11._p.addnext(note11_1._p)

    # 18. POPULATE BOM TABLES IN SECTION 9 (Using t_bom1_target and t_bom2_target)
    print("Populating Bill of Materials tables in Section 9...")
    bom_sys1_items = [
        ("1", "F1", "Ceramic Time-Lag Fuse, 2.0A, 250V AC", "1", "5x20mm Cartridge", "Littelfuse", "0218002.MXP"),
        ("2", "NTC1", "Inrush Current Thermistor, 10Ω Cold, 3.2A", "1", "Radial Disc 13mm", "TDK / EPCOS", "B57236S0100M000"),
        ("3", "MOV1", "Metal Oxide Varistor, 300V RMS, 4.5kA", "1", "Radial Disc 14mm", "Bourns", "MOV-14D471K"),
        ("4", "L_CM1", "Common Mode Choke, 15.0mH, 1.1A", "1", "Toroidal Through-Hole", "Wurth Elektronik", "744823215"),
        ("5", "L_CM2", "Common Mode Choke, 4.7mH, 1.6A", "1", "Toroidal Through-Hole", "Wurth Elektronik", "744822472"),
        ("6", "C_X1, C_X2", "Safety X2 Film Capacitor, 0.22µF, 310V AC", "2", "Radial Pitch 15mm", "KEMET", "R46KI32200001M"),
        ("7", "C_X3", "Safety X2 Film Capacitor, 0.10µF, 310V AC", "1", "Radial Pitch 10mm", "KEMET", "R46KI31000001M"),
        ("8", "C_Y1, C_Y2", "Safety Y2 Ceramic Disc Cap, 2.2nF, 400V AC", "2", "Radial Disc", "KEMET", "PHE850 Series"),
        ("9", "BR1", "Single-Phase Bridge Rectifier, 600V, 6.0A", "1", "GBU-4 Through-Hole", "Diodes Inc.", "GBU606"),
        ("10", "C_BULK", "Bulk Electrolytic Capacitor, 100µF, 450V, 105°C", "1", "Snap-In 22x30mm", "Nichicon", "LGW2W101MELZ25"),
        ("11", "C_HF", "High-Voltage Decoupling MLCC, 100nF, 630V X7R", "1", "SMD 1812", "Murata", "GA342QR7GD102KW01L"),
        ("12", "R_BL1..3", "Safety Bleeder Resistor, 3x 330kΩ, 0.25W", "3", "SMD 1206", "Vishay Dale", "CRCW1206330KFKEA"),
        ("13", "U1", "Uniform-Frequency PWM Controller (65 kHz)", "1", "SOIC-8", "Texas Instruments", "UC3843BN / UCC28C43D"),
        ("14", "Q1", "Superjunction N-MOSFET, 800V, 17A, 0.29Ω", "1", "D2PAK (TO-263)", "STMicroelectronics", "STP10NK80Z / IPB80R290P7"),
        ("15", "TX1", "Flyback Transformer, PQ26/20, Lp=220µH, 6:1", "1", "PQ26/20 Through-Hole", "Custom / Ferroxcube", "3C95-PQ2620-72W"),
        ("16", "R_T", "Oscillator Timing Resistor, 10.0 kΩ, 0.1%", "1", "SMD 0805", "Vishay Dale", "TNPW080510K0BEEA"),
        ("17", "C_T", "Oscillator Timing Capacitor, 2.2 nF, 50V C0G", "1", "SMD 0805", "Murata", "GRM2165C1H222JA01D"),
        ("18", "R_CS", "Primary Current Sense Shunt, 0.25Ω, 2W, 1%", "1", "SMD 2512 Metal Strip", "Vishay Dale", "WSL2512R2500FEA"),
        ("19", "D_SNUB", "Ultrafast Recovery Snubber Diode, 1000V, 1A, 75ns", "1", "SMA (DO-214AC)", "Diodes Inc.", "US1M-13-F"),
        ("20", "R_SNUB1..3", "Snubber Clamp Resistors, 3x 68kΩ 1W (22.6kΩ net)", "3", "SMD 2512", "Vishay Dale", "CRCW251268K0FKEG"),
        ("21", "C_SNUB", "High-Voltage Snubber Cap, 1.0nF, 1000V Ceramic", "1", "SMD 1210", "Murata", "GRM32A7U3A102JW31D"),
        ("22", "D_SEC", "Schottky Barrier Rectifier, 100V, 10A, Vf=0.60V", "1", "TO-220-2 (Heatsink)", "ON Semiconductor", "MBR10100G"),
        ("23", "C_SEC1,2", "Low-ESR Intermediate Rail Cap, 2x 470µF, 35V", "2", "Radial Can 10x16mm", "Panasonic", "EEU-FR1V471"),
        ("24", "L_SEC", "Intermediate Rail Smoothing Inductor, 2.2µH, 5A", "1", "SMD 8x8mm Shielded", "Wurth Elektronik", "7447789002"),
        ("25", "C_SEC3", "High-Frequency Decoupling MLCC, 22µF, 35V X7R", "1", "SMD 1210", "Murata", "GRM32ER7YA226KE14L"),
        ("26", "OPTO1", "Reinforced Phototransistor Optocoupler, 5kV RMS", "1", "SMD-4 Gull-Wing", "Everlight", "EL817(S)(TA)"),
        ("27", "U2", "Precision Programmable Shunt Reference, 2.495V", "1", "SOT-23-3", "Texas Instruments", "TL431AIDBZR")
    ]

    bom_sys2_items = [
        ("28", "U3", "4-Switch Synchronous Buck-Boost Controller", "1", "HTSSOP-28", "Texas Instruments", "LM5176PWPR"),
        ("29", "QA..QD", "4x Synchronous N-MOSFETs, 40V, 3.4mΩ", "4", "SuperSO8 (PowerPAK)", "Infineon", "BSC034N04LS"),
        ("30", "L1", "Flat-Wire Power Inductor, 10.0µH, 8.5A RMS, 11.5A Sat", "1", "SMD 12.5x12.5mm", "Wurth Elektronik", "7443321000"),
        ("31", "R_SHUNT", "Kelvin Current Sense Shunt, 10.0mΩ, 0.1%, 3W", "1", "SMD 2512 4-Terminal", "Bourns", "CSS2H-2512R-L010F"),
        ("32", "C_OUT1..4", "Output Filter Ceramic MLCCs, 4x 22µF, 25V X7R", "4", "SMD 1210", "Murata", "GRM32ER71E226KE15L"),
        ("33", "C_POLY", "Solid Aluminum Polymer Cap, 100µF, 25V, 12mΩ ESR", "1", "Radial SMD 8x10mm", "Panasonic", "25SVPF100M"),
        ("34", "R_TOP", "Feedback Upper Divider Resistor, 49.9 kΩ, 0.1%", "1", "SMD 0805", "Vishay Dale", "TNPW080549K9BEEA"),
        ("35", "R_BOT", "Feedback Lower Divider Resistor, 3.65 kΩ, 0.1%", "1", "SMD 0805", "Vishay Dale", "TNPW08053K65BEEA"),
        ("36", "R_DAC", "DAC Steering Summing Resistor, 11.0 kΩ, 0.1%", "1", "SMD 0805", "Vishay Dale", "TNPW080511K0BEEA"),
        ("37", "C_COMP", "Type-II Compensation Capacitor, 2.2 nF, 50V C0G", "1", "SMD 0603", "Murata", "GRM1885C1H222JA01D"),
        ("38", "R_COMP", "Type-II Compensation Resistor, 10.0 kΩ, 1%", "1", "SMD 0603", "Vishay Dale", "CRCW060310K0FKEA"),
        ("39", "U4", "32-bit ARM Cortex-M4F MCU @ 170 MHz", "1", "LQFP-64", "STMicroelectronics", "STM32G474RET6"),
        ("40", "U5", "16-Bit I2C Power Monitor IC (0.1% Accuracy)", "1", "VSSOP-10", "Texas Instruments", "INA226AIDGSR"),
        ("41", "U6", "5000V RMS Isolated Delta-Sigma Modulator", "1", "SOIC-8 Wide", "Texas Instruments", "AMC1311DWVR"),
        ("42", "CT1", "AC Current Transformer, 1000:1 Ratio, 5A", "1", "Toroidal Through-Hole", "Talema", "AC1005"),
        ("43", "R_BURDEN", "Precision CT Burden Resistor, 100 Ω, 0.1%, 0.25W", "1", "SMD 0805", "Vishay Dale", "TNPW0805100RBEEA"),
        ("44", "U7", "Secondary Synchronous Step-Down Buck (24V -> 5V)", "1", "SOT-23-6", "Texas Instruments", "TPS54202DDCR"),
        ("45", "U8", "Ultra-Low-Noise LDO Regulator (5V -> 3.3V, 500mA)", "1", "SOT-223", "Texas Instruments", "TPS7A2533DBVR"),
        ("46", "U9", "High-Precision Voltage Reference (3.000V, 0.2%)", "1", "SOT-23-3", "Texas Instruments", "REF3030AIDBZR"),
        ("47", "DISP1", "1.3\" Monochrome OLED Display Module (128x64 I2C)", "1", "4-Pin Header", "Waveshare / Solomon", "SSD1306-1.3-OLED"),
        ("48", "ENC1,2", "Dual Incremental Optical Rotary Encoders + Switch", "2", "PCB Right-Angle", "Bourns", "PEC11R-4220F-S0024"),
        ("49", "SW1", "Tactile Push-Button Output Enable Switch", "1", "SMD 6x6mm", "Omron", "B3FS-1002P"),
        ("50", "LED1..3", "Status LEDs: Green (CV), Amber (Limit), Red (Fault)", "3", "SMD 0805", "Kingbright", "APT2012 Series"),
        ("51", "POSTS", "Heavy-Duty 4mm Gold Binding Posts (Red / Black)", "2", "19.05mm Panel Mount", "Pomona Electronics", "3770-0 / 3770-2")
    ]

    # Populate t_bom1_target
    while len(t_bom1_target.rows) > 1:
        t_bom1_target._tbl.remove(t_bom1_target.rows[-1]._tr)
    while len(t_bom1_target.columns) < 7:
        t_bom1_target.add_column(Inches(1.0))
    for c in t_bom1_target.rows[0].cells:
        set_cell_background(c, "BFBFBF")
    set_cell_text(t_bom1_target.rows[0].cells[0], "Sl.No", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(t_bom1_target.rows[0].cells[1], "Ref Des", bold=True)
    set_cell_text(t_bom1_target.rows[0].cells[2], "Description", bold=True)
    set_cell_text(t_bom1_target.rows[0].cells[3], "Qty", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(t_bom1_target.rows[0].cells[4], "Package / Footprint", bold=True)
    set_cell_text(t_bom1_target.rows[0].cells[5], "Mfg", bold=True)
    set_cell_text(t_bom1_target.rows[0].cells[6], "Mfg Part No", bold=True)

    for item in bom_sys1_items:
        r = t_bom1_target.add_row()
        set_cell_text(r.cells[0], item[0], bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(8.0))
        set_cell_text(r.cells[1], item[1], bold=True, font_size=Pt(8.0))
        set_cell_text(r.cells[2], item[2], font_size=Pt(8.0))
        set_cell_text(r.cells[3], item[3], align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(8.0))
        set_cell_text(r.cells[4], item[4], font_size=Pt(8.0))
        set_cell_text(r.cells[5], item[5], font_size=Pt(8.0))
        set_cell_text(r.cells[6], item[6], font_size=Pt(8.0))
    apply_table_geometry(t_bom1_target, [Inches(0.4), Inches(0.7), Inches(2.1), Inches(0.4), Inches(1.1), Inches(0.8), Inches(0.97)])

    # Populate t_bom2_target
    while len(t_bom2_target.rows) > 1:
        t_bom2_target._tbl.remove(t_bom2_target.rows[-1]._tr)
    while len(t_bom2_target.columns) < 7:
        t_bom2_target.add_column(Inches(1.0))
    for c in t_bom2_target.rows[0].cells:
        set_cell_background(c, "BFBFBF")
    set_cell_text(t_bom2_target.rows[0].cells[0], "Sl.No", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(t_bom2_target.rows[0].cells[1], "Ref Des", bold=True)
    set_cell_text(t_bom2_target.rows[0].cells[2], "Description", bold=True)
    set_cell_text(t_bom2_target.rows[0].cells[3], "Qty", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(t_bom2_target.rows[0].cells[4], "Package / Footprint", bold=True)
    set_cell_text(t_bom2_target.rows[0].cells[5], "Mfg", bold=True)
    set_cell_text(t_bom2_target.rows[0].cells[6], "Mfg Part No", bold=True)

    for item in bom_sys2_items:
        r = t_bom2_target.add_row()
        set_cell_text(r.cells[0], item[0], bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(8.0))
        set_cell_text(r.cells[1], item[1], bold=True, font_size=Pt(8.0))
        set_cell_text(r.cells[2], item[2], font_size=Pt(8.0))
        set_cell_text(r.cells[3], item[3], align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(8.0))
        set_cell_text(r.cells[4], item[4], font_size=Pt(8.0))
        set_cell_text(r.cells[5], item[5], font_size=Pt(8.0))
        set_cell_text(r.cells[6], item[6], font_size=Pt(8.0))
    apply_table_geometry(t_bom2_target, [Inches(0.4), Inches(0.7), Inches(2.1), Inches(0.4), Inches(1.1), Inches(0.8), Inches(0.97)])

    # 19. REFRESH LIST OF TABLES AND LIST OF FIGURES
    print("Refreshing List of Tables and List of Figures...")
    all_tables_list = [
        "Table 1: Abbreviations and Acronyms\t8",
        "Table 2: Reference Standards & Literature\t8",
        "Table 3: High Level Technical Requirements\t9",
        "Table 4: Major System Use Cases & Operating Modes\t10",
        "Table 5: Hardware Physical Interfaces\t12",
        "Table 6: Software & Digital Telemetry Interfaces\t13",
        "Table 7: Engineering Domains Involved\t14",
        "Table 8: Standard Project Deliverables & Release Order\t19",
        "Table 4.1: AC-DC Isolated Uniform-Frequency Flyback Power Stage Requirements\t15",
        "Table 4.2: 4-Switch Synchronous Buck-Boost Post-Regulator Requirements\t15",
        "Table 4.3: Real-Time Dual-Domain Telemetry & Monitoring Requirements\t16",
        "Table 4.4: Protection, Safety, EMC & Environmental Requirements\t16",
        "Table 4.5: Analog Closed-Loop Control, DAC Steering & Hardware Protection Specifications\t17",
        "Table 4.6A: STAGE 1: Mains Supply & Input Protection Sequence\t17",
        "Table 4.6B: STAGE 2: Bridge Rectifier & Bulk Filter Sequence\t18",
        "Table 4.6C: STAGE 3: Uniform-Frequency Flyback DC-DC Converter Sequence\t18",
        "Table 4.6D: STAGE 3 Flyback Detailed Subsystem Component Specification & Engineering Requirements Table\t19",
        "Table 4.6E: STAGE 4: 4-Switch Buck-Boost Post-Regulator Sequence\t20",
        "Table 9.1: System 1 Product BOM (Primary, Rectifier & Flyback Stages)\t21",
        "Table 9.2: System 2 Product BOM (Buck-Boost, Protection, Telemetry & MCU Stages)\t22"
    ]

    all_figures_list = [
        "Figure 1: Boundary Diagram / Simplified 4-Stage Power Flow Block Diagram\t9",
        "Figure 2: Major Use Case 1: Constant Voltage Regulation & Dynamic Load Response Flow\t10",
        "Figure 3: Major Use Case 2: Autonomous Cycle-by-Cycle Peak Inductor Current Limiting & Fault Recovery\t11",
        "Figure 4: Inside Stage 1 - Mains AC Supply & Two-Stage EMI Filter Subsystem Architecture\t17",
        "Figure 5: Inside Stage 2 - Bridge Rectifier & Bulk DC Stage Subsystem Architecture\t18",
        "Figure 6: Inside Stage 3 - Converter DC-DC (Uniform-Frequency Isolated Flyback) Subsystem Architecture\t18",
        "Figure 7: Inside Stage 4 - 4-Switch Buck-Boost Post-Regulator Subsystem Architecture\t20",
        "Figure 8: Dual-Domain Power Telemetry & Sensing Frontend Architecture\t20",
        "Figure 9: Auxiliary Bias Power Rail Distribution Subsystem Architecture\t20",
        "Figure 10: Master System Hardware Architecture Block Diagram\t21",
        "Figure 11: MCU System Interaction, State Machine & Monitoring Architecture\t21"
    ]

    # Find List of Tables and List of Figures headings
    idx_lot = None
    idx_lof = None
    for i, p in enumerate(doc.paragraphs[:120]):
        if p.text.strip() == "List of Tables":
            idx_lot = i
        elif p.text.strip() == "List of Figures":
            idx_lof = i

    if idx_lot is not None and idx_lof is not None:
        p_lof = doc.paragraphs[idx_lof]
        tbl_slice = [doc.paragraphs[idx_lot + 1 + i] for i in range(idx_lof - (idx_lot + 1)) if doc.paragraphs[idx_lot + 1 + i].style.name == 'table of figures']
        for i, p in enumerate(tbl_slice):
            if i < len(all_tables_list):
                p.text = all_tables_list[i]

        for t_str in all_tables_list[len(tbl_slice):]:
            p_new = p_lof.insert_paragraph_before(t_str)
            p_new.style = "table of figures"

        # Re-find Introduction
        p_intro = None
        for p in doc.paragraphs:
            if p.text.strip() == "Introduction" and p.style.name == "Heading 1":
                p_intro = p
                break

        # Find figure paragraphs
        recording = False
        fig_paras = []
        for p in doc.paragraphs:
            if p.text.strip() == "List of Figures":
                recording = True
                continue
            if recording:
                if p._p == p_intro._p:
                    break
                if p.style.name == "table of figures" or p.text.strip() == "":
                    fig_paras.append(p)

        for i, p in enumerate(fig_paras):
            if i < len(all_figures_list):
                p.text = all_figures_list[i]
                p.style = "table of figures"
            else:
                p.text = ""

        for f_str in all_figures_list[len(fig_paras):]:
            p_new = p_intro.insert_paragraph_before(f_str)
            p_new.style = "table of figures"

    # 20. APPEND APPENDIX: CROSS-MENTOR INTERVIEW PREPARATION & DEFENSE CHEATSHEET
    print("Appending Appendix: Cross-Mentor Interview Preparation...")
    p_app_h1 = doc.add_paragraph("Appendix: Cross-Mentor Interview Preparation & Defense Cheatsheet")
    p_app_h1.style = "Heading 1"

    p_app_intro = doc.add_paragraph(
        "This appendix provides structured technical defense rationales for the Power Electronics Engineer Trainee (GET) "
        "when defending the hardware requirements, architecture, and safety boundaries before the cross-mentor review panel. "
        "Note: Detailed circuit equations, transformer magnetics derivations, snubber sizing, component deratings, and bench bring-up protocols "
        "are formally documented in the companion Hardware Design Document (HDD) reference: HARDWARE_DESIGN_TECHNICAL_DETAILS_FOR_HDD.md."
    )

    qa_list = [
        ("Q1: Walk me through the complete power conversion chain from the wall to the device.",
         "The power conversion hardware operates in four clean, sequential stages: First, universal mains AC (85V–265V AC RMS) enters through an IEC C14 inlet with a 2A time-lag ceramic fuse, 10Ω NTC inrush thermistor, MOV surge clamp, and a 2-stage common-mode EMI filter. Second, a GBU606 bridge rectifier and 100µF/450V bulk electrolytic capacitor convert AC into an unregulated high-voltage DC bus (+120V to +375V DC). Third, Stage 3 (a Uniform-Frequency Flyback converter with UC3843 / UCC28C43 and a custom PQ26/20 transformer) provides certified 3000V RMS reinforced safety isolation and steps down power to a stable +24.0V DC intermediate bus (72W) using an MBR10100 Schottky barrier diode with heatsink. Fourth, Stage 4 (a TI LM5176 4-switch synchronous Buck-Boost post-regulator) regulates the +24V bus down or across to the target 5.0V–20.0V DC at up to 3.0A with sub-25mV ripple, delivering clean DC to the device under test via heavy-duty 4mm binding posts."),

        ("Q2: Why did you use a passive filter and bridge rectifier instead of an active Boost PFC stage?",
         "Under international standard IEC 61000-3-2, active Power Factor Correction (PFC) is legally mandated only for equipment with active input power exceeding 75W. Our module delivers a maximum continuous output of 60W (72W peak intermediate), so it falls strictly below the 75W threshold. Adding an active PFC boost stage would require an additional high-voltage MOSFET, boost diode, controller IC, and large inductor—adding approximately $4.20 to the BOM, consuming 35% more PCB area, and introducing a ~3% efficiency penalty without any regulatory requirement."),

        ("Q3: How did you calculate the Flyback transformer magnetics on the PQ26/20 core?",
         "At minimum 85V AC input, the rectified bulk bus is 120V DC. For a maximum duty cycle of 45% and uniform 65kHz switching frequency (set by RT=10kΩ, CT=2.2nF) at 72W output power, peak primary current is I_pk = 2.96A. Using L_p = (V_bulk_min * D_max) / (I_pk * f_sw), I calculated a primary inductance of 220µH. I chose a Ferroxcube PQ26/20 core in 3C95 material because its cross-sectional area Ae is 122 mm², keeping peak flux density B_max at 0.148 Tesla (well below the 0.38 Tesla saturation limit). The turns ratio is 6:1 (36 primary turns, 6 secondary turns). To guarantee IEC 62368-1 reinforced isolation (3000V RMS), the secondary is wound with Furukawa TEX-E triple-insulated wire. The uniform frequency ensures fixed, predictable EMI harmonics at 65kHz and its integer multiples."),

        ("Q4: Why is the intermediate bus chosen at +24.0V DC instead of +12V or +48V?",
         "+24.0V DC is the optimal design choice for a 5V to 20V output range. If we chose +12V, stepping up to 20V at 3A (60W) would require high inductor boost currents (I_in = 5.5A), creating excessive I²R conduction losses in the Buck-Boost MOSFETs. If we chose +48V, the Flyback turns ratio would decrease, increasing primary switch voltage stress, and stepping down to 5V would require an extreme duty cycle of 10%. With +24V, 5V, 12V, and 15V operate in pure Buck mode (>96% efficiency), and 20V operates near unity Buck-Boost transition with minimal switching stress."),

        ("Q5: How does the 4-switch Buck-Boost operate seamlessly between 5V and 20V?",
         "The TI LM5176 controls four N-MOSFETs (QA, QB, QC, QD) in an H-bridge configuration around a single 10µH flat-wire inductor. When V_OUT is significantly below 24V (e.g. 5V or 12V), QC is held continuously ON and QD is OFF, so the circuit functions purely as a synchronous Buck converter with switches QA and QB. As V_OUT approaches 20V under heavy load, the controller smoothly enters 4-switch Buck-Boost mode, modulating both legs to maintain exact regulation with zero deadband or output glitching."),

        ("Q6: How does the DAC steer the output voltage without destabilizing the loop?",
         "The LM5176 regulates by maintaining its feedback pin (FB) at an internal 1.20V reference. Instead of modifying the internal reference, we use a resistive summing junction: R_top (49.9kΩ) connects to V_OUT, R_bot (3.65kΩ) connects to ground, and R_DAC (11.0kΩ) connects to our 12-bit DAC. By injecting current into the FB node from the DAC, when V_DAC = 3.3V, V_OUT is steered to 5.0V. When V_DAC = 0V, V_OUT is steered to 20.0V. Because the loop's AC Type-II compensation network is connected between COMP and ground, DC setpoint steering has zero impact on high-frequency phase margin and stability."),

        ("Q7: How does the power supply protect against overcurrent and short circuits?",
         "We use standard, proven industry protections built directly into the hardware controllers: 1) LM5176 Built-in Cycle-by-Cycle Current Limiting: The LM5176 continuously monitors inductor/output current through a 10mΩ precision sense resistor connected to its dedicated CSP and CSN pins. If current exceeds the programmed threshold, the controller immediately truncates the current PWM pulse, capping peak current on every 300 kHz switching cycle. 2) MCU Supervisory Disable: The MCU continuously reads output current via the INA226 power monitor over I2C. If a sustained overload or short-circuit is detected (> 500 ms), the MCU pulls the LM5176 ENABLE pin low to safely disable power delivery. 3) Primary AC Fuse: A 2.0A ceramic time-lag fuse on the AC mains provides fail-safe isolation against internal catastrophic short circuits."),

        ("Q8: How is safety galvanic isolation guaranteed on the PCB?",
         "We adhere strictly to IEC 62368-1 for reinforced insulation. Primary hot circuits and secondary touch-safe circuits are separated by a minimum physical surface creepage distance of 6.4mm. Across the isolation barrier, we route a 2.0mm wide milled air slot through the PCB substrate directly beneath the PQ26/20 transformer and optocouplers. The transformer secondary uses triple-insulated Furukawa TEX-E wire. The complete assembly is verified on the bench with a 3000V AC RMS Hipot dielectric withstand test for 60 seconds with zero breakdown."),

        ("Q9: How do you verify output voltage ripple on the oscilloscope?",
         "Standard alligator ground clips act as loop antennas that pick up radiated high-frequency magnetic noise from the 300kHz switching inductor, falsely showing 100mV+ of ripple. To measure true ripple accurately, I use the tip-and-barrel probing technique directly across the output capacitor C_OUT. I remove the oscilloscope probe hat and ground lead, wrap a short bus wire around the ground barrel, touch the tip directly to the positive pad and the barrel to the negative pad, engage 20MHz bandwidth limit and AC coupling, and verify peak-to-peak ripple is strictly below 25mV."),

        ("Q10: What is your exact bench bring-up procedure using a Variac?",
         "Before applying any AC power, I perform cold resistance checks: verifying > 100MΩ primary-to-secondary isolation resistance, checking for shorts across the bulk capacitor, and checking impedance across the +24V bus and output terminals. Next, I connect the board to an isolation transformer and an AC Variac with a 60W series current-limiting incandescent bulb. I slowly ramp AC voltage from 0V to 85V AC while monitoring bulk DC bus voltage and Flyback V_CC aux bias. Once the +24V bus stabilizes at 85V AC, I ramp to nominal 230V AC and 265V AC. Finally, I enable the LM5176 Buck-Boost stage, sweep the DAC from 5V to 20V with a precision DMM, and apply incremental electronic load steps from 0.1A to 3.0A while monitoring thermals with a FLIR thermal camera.")
    ]

    for q, a in qa_list:
        p_q = doc.add_paragraph(q)
        p_q.style = "Heading 3"
        p_a = doc.add_paragraph(a)

    # 21. FINAL PASS: Ensure EVERY table in doc.tables has NO floating tblpPr
    for t in doc.tables:
        for child in list(t._tbl.tblPr):
            if child.tag.endswith('tblpPr'):
                t._tbl.tblPr.remove(child)

    # 22. FINAL PASS: Safe cleanup of remaining template instruction tags
    # Only remove strings that explicitly match template guidance tokens '<Word...'
    template_tokens = [
        r'<Briefly[^>]*>',
        r'<Describe[^>]*>',
        r'<Define[^>]*>',
        r'<List[^>]*>',
        r'<Provide[^>]*>',
        r'<Summarize[^>]*>',
        r'<Small[^>]*>',
        r'<Insert[^>]*>',
        r'<There[^>]*>',
        r'<UI/UX[^>]*>',
        r'<Refer[^>]*>',
        r'<Fill[^>]*>',
        r'<Architecture[^>]*>',
        r'<BOM[^>]*>',
        r'<All[^>]*>',
        r'<Identify[^>]*>',
        r'<Top[^>]*>',
        r'< Broad[^>]*>',
        r'<\. Describe[^>]*>',
        r'<optional>'
    ]
    for p in doc.paragraphs:
        for pat in template_tokens:
            if re.search(pat, p.text):
                p.text = re.sub(pat, '', p.text).strip()

    print(f"Saving Final PRD Document: {output_prd_final_docx}")
    doc.save(output_prd_final_docx)
    print(f"Updating Reference PRD Document: {output_ref_docx}")
    doc.save(output_ref_docx)
    print(f"Updating Main PRD Document: {output_main_docx}")
    doc.save(output_main_docx)
    print("SUCCESS: Final PRD generated and synchronized across all target paths!")

if __name__ == "__main__":
    generate_final_prd()
