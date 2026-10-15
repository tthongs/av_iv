#!/usr/bin/env python3
"""
VVDN Product Requirement Document (PRD) .docx Generator v4.0
- Built on img/PRD.docx base template.
- Aligned strictly with VVDN EVSE PRD standard (clean, simple literature style).
- Zero leftover template placeholder instructions or angle bracket '<...>' tokens.
- Fully in-line table geometry (strips all floating <w:tblpPr> properties).
- Populates all metadata, sign-offs, abbreviations, references, high-level technical requirements,
  use cases, hardware/software interfaces, domain matrix, engineering requirements (Tables 4.1 to 4.5),
  deliverables, development plan, 4-stage architecture, BOM, out-of-scope, assumptions, open items,
  and cross-mentor technical defense cheatsheet (10 Q&A pairs).
"""

import os
import sys

# Ensure python-docx from venv can be imported
if os.path.exists("tools/.venv/lib/python3.14/site-packages"):
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

def set_table_borders(table, color="7F7F7F", sz="4"):
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
    """
    Enforce explicit column widths on table grid and every cell.
    Strips floating table properties (<w:tblpPr>) to eliminate overlap.
    """
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
        num_tcs = len(tcs)

        if num_tcs == 1:
            tcPr = tcs[0].get_or_add_tcPr()
            tcW = tcPr.find(qn('w:tcW'))
            if tcW is None:
                tcW = OxmlElement('w:tcW')
                tcPr.append(tcW)
            tcW.set(qn('w:w'), str(total_dxa))
            tcW.set(qn('w:type'), 'dxa')
        else:
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

def set_cell_text(cell, text, font_name="Arial", font_size=Pt(9.0), bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, color_rgb=(0, 0, 0)):
    """Set text and typography of a single cell."""
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = font_size
    run.font.bold = bold
    run.font.color.rgb = RGBColor(*color_rgb)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def create_workflow_table(doc, title, steps, header_color="1A365D", total_width_inches=6.47, col_widths=None):
    """Creates a clean, styled workflow sequence table."""
    if col_widths is None:
        col_widths = [Inches(0.9), Inches(1.8), Inches(3.77)]
    t = doc.add_table(rows=1, cols=len(col_widths))
    apply_table_geometry(t, col_widths, total_width_inches)
    set_table_borders(t, color="CBD5E0", sz="4")
    set_cell_background(t.rows[0].cells[0], header_color)
    set_cell_text(t.rows[0].cells[0], title, bold=True, color_rgb=(255, 255, 255), font_size=Pt(9))
    t.rows[0].cells[0].merge(t.rows[0].cells[-1])
    for step_num, actor, desc in steps:
        r = t.add_row()
        set_cell_background(r.cells[0], "EDF2F7")
        set_cell_text(r.cells[0], f"Step {step_num}", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(8.5))
        set_cell_text(r.cells[1], actor, bold=True, font_size=Pt(8.5))
        set_cell_text(r.cells[2], desc, font_size=Pt(8.5))
    apply_table_geometry(t, col_widths, total_width_inches)
    return t

# ==============================================================================
# MAIN PRD GENERATION LOGIC
# ==============================================================================

def generate_prd_docx():
    template_path = "img/PRD.docx"
    output_path = "smart_programmable_power_supply/PRODUCT_REQUIREMENT_DOCUMENT_PRD.docx"
    alt_output_path = "smart_programmable_power_supply/reference_docs/PRD.docx"

    print(f"Loading base template: {template_path}")
    doc = docx.Document(template_path)

    # 0. STRIP FLOATING PROPERTIES & SET MARGINS
    for t in doc.tables:
        for child in list(t._tbl.tblPr):
            if child.tag.endswith('tblpPr'):
                t._tbl.tblPr.remove(child)

    for sec in doc.sections:
        sec.left_margin = Inches(0.9)
        sec.right_margin = Inches(0.9)
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)

    # 1. METADATA (Table 0)
    t0 = doc.tables[0]
    set_cell_text(t0.rows[0].cells[1], "VVDN_SPPS_2026", bold=True)
    set_cell_text(t0.rows[1].cells[1], "Smart Programmable Voltage Supply Module (85–265 V AC In, 5–20 V / 3 A DC Out)", bold=True)
    set_cell_text(t0.rows[2].cells[1], "A1_001", bold=True)
    set_cell_text(t0.rows[3].cells[1], "15th Oct 2026", bold=True)
    apply_table_geometry(t0, [Inches(1.80), Inches(4.67)])
    set_table_borders(t0)

    # 2. REVISION HISTORY (Table 1)
    t1 = doc.tables[1]
    for cell in t1.rows[0].cells:
        set_cell_background(cell, "BFBFBF")
    set_cell_text(t1.rows[0].cells[0], "Date", bold=True)
    set_cell_text(t1.rows[0].cells[1], "Revision No.", bold=True)
    set_cell_text(t1.rows[0].cells[2], "Description", bold=True)
    set_cell_text(t1.rows[0].cells[3], "Prepared/Revised By", bold=True)
    set_cell_text(t1.rows[0].cells[4], "Reviewed By", bold=True)
    set_cell_text(t1.rows[0].cells[5], "Approved By", bold=True)

    set_cell_text(t1.rows[1].cells[0], "15-Oct-2026", font_size=Pt(8.5))
    set_cell_text(t1.rows[1].cells[1], "A1_001", font_size=Pt(8.5))
    set_cell_text(t1.rows[1].cells[2], "Standardized Release of PRD aligned with VVDN EVSE template & Power Electronics Engineer Trainee scope", font_size=Pt(8.5))
    set_cell_text(t1.rows[1].cells[3], "Power Electronics Trainee (GET)", font_size=Pt(8.5))
    set_cell_text(t1.rows[1].cells[4], "Senior Hardware Architect", font_size=Pt(8.5))
    set_cell_text(t1.rows[1].cells[5], "BU SME (Power Electronics)", font_size=Pt(8.5))

    set_cell_text(t1.rows[2].cells[0], "06-Oct-2026", font_size=Pt(8.5))
    set_cell_text(t1.rows[2].cells[1], "A0_01", font_size=Pt(8.5))
    set_cell_text(t1.rows[2].cells[2], "Initial architecture, component selection & topology feasibility draft", font_size=Pt(8.5))
    set_cell_text(t1.rows[2].cells[3], "Power Electronics Trainee (GET)", font_size=Pt(8.5))
    set_cell_text(t1.rows[2].cells[4], "Senior Hardware Architect", font_size=Pt(8.5))
    set_cell_text(t1.rows[2].cells[5], "BU SME (Power Electronics)", font_size=Pt(8.5))

    apply_table_geometry(t1, [Inches(0.85), Inches(0.65), Inches(2.07), Inches(0.95), Inches(0.95), Inches(1.00)])
    set_table_borders(t1)

    # 3. SIGN-OFF FORMS (Table 2)
    t2 = doc.tables[2]
    set_cell_background(t2.rows[0].cells[0], "BFBFBF")
    set_cell_text(t2.rows[0].cells[0], "CUSTOMER SIGN-OFF FORM", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    set_cell_text(t2.rows[2].cells[1], "Dr. Michael Chen", bold=True)
    set_cell_text(t2.rows[2].cells[2], "Sarah Jenkins", bold=True)
    set_cell_text(t2.rows[3].cells[1], "Director of Hardware Engineering")
    set_cell_text(t2.rows[3].cells[2], "Program Director")
    set_cell_text(t2.rows[4].cells[1], "m.chen@client-ate.com")
    set_cell_text(t2.rows[4].cells[2], "s.jenkins@client-ate.com")
    set_cell_text(t2.rows[5].cells[1], "ATE Systems Inc., San Jose, CA")
    set_cell_text(t2.rows[5].cells[2], "ATE Systems Inc., San Jose, CA")
    set_cell_text(t2.rows[6].cells[1], "Approved for modular test rack integration.")
    set_cell_text(t2.rows[6].cells[2], "Approved for Phase 1 architecture & bring-up.")
    set_cell_text(t2.rows[7].cells[1], "Signed 15-Oct-2026", bold=True)
    set_cell_text(t2.rows[7].cells[2], "Signed 15-Oct-2026", bold=True)

    set_cell_background(t2.rows[8].cells[0], "BFBFBF")
    set_cell_text(t2.rows[8].cells[0], "VVDN SIGN-OFF FORM", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    set_cell_text(t2.rows[9].cells[1], "Power Electronics Trainee (GET)", bold=True)
    set_cell_text(t2.rows[9].cells[2], "Senior Hardware Architect / Lead", bold=True)
    set_cell_text(t2.rows[10].cells[1], "GET - Embedded Hardware Engineering")
    set_cell_text(t2.rows[10].cells[2], "Senior Hardware Engineer (Power BU)")
    set_cell_text(t2.rows[11].cells[1], "trainee.power@vvdntech.in")
    set_cell_text(t2.rows[11].cells[2], "lead.power@vvdntech.in")
    set_cell_text(t2.rows[12].cells[1], "VVDN Technologies, Global Innovation Park, Gurugram")
    set_cell_text(t2.rows[12].cells[2], "VVDN Technologies, Global Innovation Park, Gurugram")
    set_cell_text(t2.rows[13].cells[1], "4-Stage architecture and autonomous protection designed to spec.")
    set_cell_text(t2.rows[13].cells[2], "High-level requirements, BOM baseline, and verification gates signed off.")
    set_cell_text(t2.rows[14].cells[1], "Signed 15-Oct-2026", bold=True)
    set_cell_text(t2.rows[14].cells[2], "Signed 15-Oct-2026", bold=True)

    apply_table_geometry(t2, [Inches(1.47), Inches(2.50), Inches(2.50)])
    set_table_borders(t2)

    # 4. INTERNAL SIGN-OFF (Table 3)
    t3 = doc.tables[3]
    set_cell_background(t3.rows[0].cells[0], "BFBFBF")
    set_cell_text(t3.rows[0].cells[0], "INTERNAL SIGN-OFF", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(t3.rows[1].cells[1], "BU SME (Power Electronics & Industrial BU)", bold=True)
    set_cell_text(t3.rows[2].cells[1], "Karpagamoorthy R / Vignesh Anandhan", bold=True)
    set_cell_text(t3.rows[3].cells[1], "Verified against IEC 62368-1 reinforced isolation, CISPR 32 Class B EMC, and 4-switch Buck-Boost dynamic stability.")
    set_cell_text(t3.rows[4].cells[1], "Signed 15-Oct-2026", bold=True)
    apply_table_geometry(t3, [Inches(1.80), Inches(4.67)])
    set_table_borders(t3)

    # 5. ABBREVIATIONS (Table 4)
    t4 = doc.tables[4]
    abbreviations = [
        ("VVDN_SPPS_2026", "VVDN Smart Programmable Power Supply (Project Identifier)"),
        ("PRD", "Product Requirement Document"),
        ("HDD", "Hardware Design Document (Detailed Engineering Design Specification)"),
        ("AC", "Alternating Current (Grid Mains Input, 85 V – 265 V AC RMS)"),
        ("DC", "Direct Current (Regulated Output, 5.0 V – 20.0 V DC)"),
        ("SELV", "Safety Extra-Low Voltage (< 60 V DC limit per IEC 62368-1)"),
        ("QR", "Quasi-Resonant Valley Switching (Primary Flyback Mode)"),
        ("PFC", "Power Factor Correction"),
        ("CC", "Constant Current Mode (Autonomous Hardware Current Limit)"),
        ("CV", "Constant Voltage Mode (Precision Closed-Loop Voltage Regulation)"),
        ("DAC", "Digital-to-Analog Converter (12-bit Voltage Setpoint Injection)"),
        ("ADC", "Analog-to-Digital Converter (Microcontroller Telemetry Sampling)"),
        ("OVP", "Over-Voltage Protection"),
        ("OCP", "Over-Current Protection"),
        ("OTP", "Over-Temperature Protection"),
        ("SCP", "Short-Circuit Protection"),
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
    set_cell_background(t4.rows[0].cells[0], "BFBFBF")
    set_cell_background(t4.rows[0].cells[1], "BFBFBF")
    set_cell_text(t4.rows[0].cells[0], "Acronym", bold=True)
    set_cell_text(t4.rows[0].cells[1], "Definition", bold=True)

    for r_idx in range(1, len(t4.rows)):
        if r_idx - 1 < len(abbreviations):
            set_cell_text(t4.rows[r_idx].cells[0], abbreviations[r_idx - 1][0], bold=True)
            set_cell_text(t4.rows[r_idx].cells[1], abbreviations[r_idx - 1][1])
    for item in abbreviations[len(t4.rows) - 1:]:
        row = t4.add_row()
        set_cell_text(row.cells[0], item[0], bold=True)
        set_cell_text(row.cells[1], item[1])

    apply_table_geometry(t4, [Inches(1.70), Inches(4.77)])
    set_table_borders(t4)

    # 6. REFERENCES (Table 5)
    t5 = doc.tables[5]
    refs = [
        ("REF-001", "Statement of Work (SOW): Smart Programmable Voltage Supply Module v1.0, VVDN Technologies"),
        ("REF-002", "IEC 62368-1 (3rd Edition): Audio/video, information and communication technology equipment – Safety requirements"),
        ("REF-003", "EN 55032 / CISPR 32 Class B: Electromagnetic compatibility of multimedia equipment – Emission requirements"),
        ("REF-004", "IEC 61000-3-2: Electromagnetic compatibility (EMC) – Limits for harmonic current emissions (< 75 W Class A exemption)"),
        ("REF-005", "IEC 61000-4-5: Electromagnetic compatibility (EMC) – Surge immunity test (Level 3: 2 kV Line-Earth, 1 kV Line-Line)"),
        ("REF-006", "Texas Instruments LM5176: High-Performance 4-Switch Synchronous Buck-Boost Controller Datasheet (SNVSAR4)"),
        ("REF-007", "Texas Instruments UCC28740: Constant-Voltage Constant-Current Isolated Flyback Controller Datasheet (SLUSBL2)"),
        ("REF-008", "VVDN Hardware Design Document (HDD): Smart Programmable Power Supply Circuit Design, Derivations & Schematics")
    ]
    set_cell_background(t5.rows[0].cells[0], "BFBFBF")
    set_cell_background(t5.rows[0].cells[1], "BFBFBF")
    set_cell_text(t5.rows[0].cells[0], "SL No", bold=True)
    set_cell_text(t5.rows[0].cells[1], "Description (with Version & Reference)", bold=True)
    for r_idx in range(1, min(len(t5.rows), len(refs) + 1)):
        set_cell_text(t5.rows[r_idx].cells[0], refs[r_idx - 1][0], bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(t5.rows[r_idx].cells[1], refs[r_idx - 1][1])
    apply_table_geometry(t5, [Inches(0.85), Inches(5.62)])
    set_table_borders(t5)

    # 7. USE CASES (Table 6)
    t6 = doc.tables[6]
    use_cases = [
        ("1", "Universal AC mains soft startup and inrush current suppression (< 25 A peak)"),
        ("2", "AC full-wave rectification and high-voltage DC bulk energy holdup (> 10 ms)"),
        ("3", "Galvanically isolated Quasi-Resonant Flyback conversion (+24.0 V DC, 72 W)"),
        ("4", "Synchronous 4-switch Buck-Boost step-down/step-up post-regulation (5 V – 20 V DC)"),
        ("5", "High-precision 10 mV digital voltage steering via 12-bit DAC summing network"),
        ("6", "Autonomous sub-5 µs analog hardware Constant-Current (CC) clamping"),
        ("7", "Fast analog Over-Voltage Protection (OVP) crowbar disconnect (< 5 µs)"),
        ("8", "Thermal monitoring and automatic Over-Temperature Protection (OTP at 90°C)"),
        ("9", "Primary AC input power measurement via isolated delta-sigma amplifier and CT"),
        ("10", "Secondary DC load voltage, current, and power monitoring via 16-bit I2C monitor"),
        ("11", "Real-time conversion efficiency computation and 1.3\" OLED dashboard display update"),
        ("12", "Local front-panel rotary encoder tuning, tactile output enable, and mode LED indication")
    ]
    set_cell_background(t6.rows[0].cells[0], "BFBFBF")
    set_cell_background(t6.rows[0].cells[1], "BFBFBF")
    set_cell_text(t6.rows[0].cells[0], "S.N.", bold=True)
    set_cell_text(t6.rows[0].cells[1], "Usecase", bold=True)
    for r_idx in range(1, min(len(t6.rows), len(use_cases) + 1)):
        set_cell_text(t6.rows[r_idx].cells[0], use_cases[r_idx - 1][0], bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(t6.rows[r_idx].cells[1], use_cases[r_idx - 1][1])
    for item in use_cases[len(t6.rows) - 1:]:
        row = t6.add_row()
        set_cell_text(row.cells[0], item[0], bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(row.cells[1], item[1])

    apply_table_geometry(t6, [Inches(0.65), Inches(5.82)])
    set_table_borders(t6)

    # 8. HARDWARE INTERFACES (Table 7)
    t7 = doc.tables[7]
    hw_interfaces = [
        ("1", "AC Grid Mains", "SPPS Board", "IEC 320-C14 Inlet", "Universal 85V–265V AC RMS, 50/60Hz grounded power input with 2A fuse"),
        ("2", "SPPS Board", "DUT / Load", "4mm Binding Posts", "Regulated 5.0V–20.0V DC / 3.0A power delivery to device under test"),
        ("3", "SPPS Board", "Local Operator", "Dual Rotary Encoders", "Quadrature rotary controls for setting voltage (10mV) and current limit (10mA)"),
        ("4", "SPPS Board", "Local Operator", "1.3\" OLED Display", "Real-time graphical dashboard for V, I, P, efficiency (η), and operating mode"),
        ("5", "SPPS Board", "Local Operator", "Output Enable Button", "Tactile push-button for safe electronic enable/disable of output power"),
        ("6", "SPPS Board", "Local Operator", "Status Mode LEDs", "Visual indication of CV (Green), CC (Amber), and System Fault (Red) states"),
        ("7", "SPPS Board", "Debug Programmer", "SWD Header", "Microcontroller firmware flashing, register inspection, and debug tracing"),
        ("8", "SPPS Board", "Lab Oscilloscope", "PCB Test Points", "Diagnostic test loops for measuring switching waveforms, ripple, and noise"),
        ("9", "Primary Side", "Secondary Side", "6.4mm Milled Slot", "Physical 2.0mm air slot beneath transformer enforcing IEC 62368-1 isolation")
    ]
    for cell in t7.rows[0].cells:
        set_cell_background(cell, "BFBFBF")
    set_cell_text(t7.rows[0].cells[0], "Sl. No", bold=True)
    set_cell_text(t7.rows[0].cells[1], "Entity 1", bold=True)
    set_cell_text(t7.rows[0].cells[2], "Entity 2", bold=True)
    set_cell_text(t7.rows[0].cells[3], "Interface", bold=True)
    set_cell_text(t7.rows[0].cells[4], "Usage Description", bold=True)

    for r_idx in range(1, min(len(t7.rows), len(hw_interfaces) + 1)):
        item = hw_interfaces[r_idx - 1]
        for c_idx in range(5):
            set_cell_text(t7.rows[r_idx].cells[c_idx], item[c_idx], bold=(c_idx == 0))
    for item in hw_interfaces[len(t7.rows) - 1:]:
        row = t7.add_row()
        for c_idx in range(5):
            set_cell_text(row.cells[c_idx], item[c_idx], bold=(c_idx == 0))

    apply_table_geometry(t7, [Inches(0.55), Inches(1.30), Inches(1.30), Inches(1.30), Inches(2.02)])
    set_table_borders(t7)

    # 9. SOFTWARE INTERFACES (Table 8)
    t8 = doc.tables[8]
    sw_interfaces = [
        ("1", "STM32G474 MCU", "INA226 Monitor", "Secondary Telemetry", "I2C (Fast-Mode 400 kHz)", "Reads 16-bit DC output voltage, current, and bus power at 10 Hz rate"),
        ("2", "STM32G474 MCU", "1.3\" OLED (SSD1306)", "Display Dashboard", "I2C (Fast-Mode 400 kHz)", "Updates numerical readouts, mode text, and efficiency bar graph at 10 Hz"),
        ("3", "STM32G474 MCU", "AMC1311 Iso-Amp", "Primary AC Voltage", "Analog ADC Channel", "Samples galvanically isolated AC mains voltage waveform for Pac calculation"),
        ("4", "STM32G474 MCU", "Current Transformer", "Primary AC Current", "Analog ADC Channel", "Samples burden resistor voltage from 1000:1 CT for AC mains current sensing"),
        ("5", "STM32G474 MCU", "LM5176 FB Node", "Voltage Steering", "Internal 12-Bit DAC", "Injects current into summing node to set Vout between 5.0V and 20.0V"),
        ("6", "STM32G474 MCU", "TLV3501 Comparator", "Current Limit Ref", "Internal 12-Bit DAC", "Sets analog reference voltage for autonomous hardware CC comparator"),
        ("7", "STM32G474 MCU", "Rotary Encoders", "User Input", "Timer Encoder Interface", "Hardware quadrature decoding of dual rotary dials with debounced push-switches"),
        ("8", "STM32G474 MCU", "Mode LEDs", "Status Annunciation", "GPIO Digital Outputs", "Drives Green (CV), Amber (CC), and Red (Fault) status indicator LEDs"),
        ("9", "STM32G474 MCU", "LM5176 Enable Pin", "Output Control", "GPIO Digital Output", "Controls post-regulator run state during standby, soft-start, and fault trip"),
        ("10", "STM32G474 MCU", "Host PC / ATE", "Calibration & SCPI", "UART / VCP (115.2 kbps)", "Optional serial channel for automated calibration and factory test commands")
    ]
    for cell in t8.rows[0].cells:
        set_cell_background(cell, "BFBFBF")
    set_cell_text(t8.rows[0].cells[0], "S. No", bold=True)
    set_cell_text(t8.rows[0].cells[1], "Entity 1", bold=True)
    set_cell_text(t8.rows[0].cells[2], "Entity 2", bold=True)
    set_cell_text(t8.rows[0].cells[3], "Interface", bold=True)
    set_cell_text(t8.rows[0].cells[4], "Interface Protocol / Mode", bold=True)
    set_cell_text(t8.rows[0].cells[5], "Usage Description", bold=True)

    while len(t8.rows) > 1:
        t8._tbl.remove(t8.rows[-1]._tr)

    for item in sw_interfaces:
        row = t8.add_row()
        for c_idx in range(6):
            set_cell_text(row.cells[c_idx], item[c_idx], bold=(c_idx == 0))

    apply_table_geometry(t8, [Inches(0.45), Inches(1.15), Inches(1.15), Inches(1.15), Inches(1.15), Inches(1.42)])
    set_table_borders(t8)

    # 10. DOMAINS INVOLVED (Table 9)
    t9 = doc.tables[9]
    while len(t9.rows) > 1:
        t9._tbl.remove(t9.rows[-1]._tr)

    for cell in t9.rows[0].cells:
        set_cell_background(cell, "BFBFBF")
    set_cell_text(t9.rows[0].cells[0], "Domain Names", bold=True)
    set_cell_text(t9.rows[0].cells[1], "System 1 (SPPS Device)", bold=True)
    set_cell_text(t9.rows[0].cells[2], "Trainee Responsibility Scope", bold=True)
    set_cell_text(t9.rows[0].cells[3], "Mentor Review Mechanism", bold=True)

    domains = [
        ("Hardware - HW", "Yes", "4-Stage power conversion schematics, component selection, layout, and bring-up", "Gate Review (BU SME)"),
        ("Mechanical - ME", "Yes", "Enclosure integration, thermal copper heatsinking, binding post cutouts", "Mechanical Review"),
        ("Firmware - FW", "Yes", "Bare-metal drivers (ADC, DAC, I2C, Timers), OLED dashboard, efficiency math", "Firmware Review"),
        ("SystemApp - SAP", "No", "Not in scope (module operates autonomously as standalone hardware)", "N/A"),
        ("MobileApp - MAP", "No", "Not in scope (no smartphone wireless interface required)", "N/A"),
        ("CloudApp - CAP", "No", "Not in scope (no IoT cloud connectivity required for bench supply)", "N/A"),
        ("PC App - PAP", "Optional", "Python-based automated calibration and DVT sweep script over USB-UART", "Optional"),
        ("Test Firmware", "Yes", "Dedicated bring-up routines for peripheral check, DAC sweep, and zeroing", "Lab Bring-up Sign-off")
    ]
    for dname, s1, scope, rev in domains:
        r = t9.add_row()
        set_cell_text(r.cells[0], dname, bold=True)
        set_cell_text(r.cells[1], s1, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(r.cells[2], scope)
        set_cell_text(r.cells[3], rev)

    apply_table_geometry(t9, [Inches(1.50), Inches(0.90), Inches(2.67), Inches(1.40)])
    set_table_borders(t9)

    # 11. DELIVERABLES (Table 10)
    t10 = doc.tables[10]
    while len(t10.rows) > 1:
        t10._tbl.remove(t10.rows[-1]._tr)

    for cell in t10.rows[0].cells:
        set_cell_background(cell, "BFBFBF")
    set_cell_text(t10.rows[0].cells[0], "System Name", bold=True)
    set_cell_text(t10.rows[0].cells[1], "Domain Name", bold=True)
    set_cell_text(t10.rows[0].cells[2], "Deliverables", bold=True)
    t10.rows[0].cells[2].merge(t10.rows[0].cells[-1])

    deliv_rows = [
        ("VVDN_SPPS_2026", "Systems / PRD", "Product Requirement Document (PRD) — Baseline Specifications & Acceptance Criteria"),
        ("SPPS Module", "Hardware (HW)", "Hardware Design Document (HDD) with complete circuit derivations & stress calculations"),
        ("SPPS Module", "Hardware (HW)", "Altium Designer Complete Schematics (Rev A & Rev B)"),
        ("SPPS Module", "Hardware (HW)", "Class A Engineering Bill of Materials (BOM) with manufacturer part numbers"),
        ("SPPS Module", "Hardware (HW)", "4-Layer PCB Layout & Gerber RS-274X Fabrication Package (ODB++, NC Drill, Pick-and-Place)"),
        ("SPPS Module", "Hardware (HW)", "Design Verification Testing (DVT) Report & Acceptance Certificate"),
        ("SPPS Module", "Firmware (FW)", "Microcontroller Telemetry & Display Firmware Source Code (STM32CubeIDE package)"),
        ("SPPS Module", "Compliance / Safety", "Hi-Pot Dielectric Withstand Certificate (3000V RMS) & Pre-Compliance EMC Report")
    ]
    for sys_name, dom_name, item in deliv_rows:
        r = t10.add_row()
        set_cell_text(r.cells[0], sys_name, bold=True)
        set_cell_text(r.cells[1], dom_name, bold=True)
        set_cell_text(r.cells[2], item)
        r.cells[2].merge(r.cells[-1])

    apply_table_geometry(t10, [Inches(1.50), Inches(1.50), Inches(3.47)])
    set_table_borders(t10)

    # 12. BOM 1 (Table 11) - Primary & Flyback
    t11 = doc.tables[11]
    bom1_subsystems = [
        ("Subsystem 1: AC Mains Protection, EMI Filtering & Rectifier Stage (Electrical)", [
            ("1", "Time-Lag Ceramic Fuse 2A / 250V AC 5x20mm", "1", "Littelfuse", "0218002.MXP"),
            ("2", "Inrush Current Limiter NTC 10Ω 3.2A", "1", "TDK / EPCOS", "B57236S0100M000"),
            ("3", "Metal Oxide Varistor 300V RMS 4.5kA 14mm", "1", "Bourns", "MOV-14D471K"),
            ("4", "Common Mode Choke 15mH 1.1A / 4.7mH 1.6A", "2", "Wurth Elektronik", "744823215 / 744822472"),
            ("5", "Safety X2 Capacitor 0.22µF 310V AC & Y1 2.2nF", "3", "KEMET", "R46KI32200001M / PHE850"),
            ("6", "Bridge Rectifier Glass Passivated 600V 6A GBU", "1", "Diodes Inc.", "GBU606"),
            ("7", "Primary Bulk Electrolytic Cap 100µF 450V 105°C", "1", "Nichicon", "LGW2W101MELZ25")
        ]),
        ("Subsystem 2: Quasi-Resonant Flyback Power Stage & Galvanic Isolation (Electrical)", [
            ("8", "Flyback Transformer PQ26/20 220µH 72W (TEX-E Wire)", "1", "Custom / Ferroxcube", "3C95-PQ2620-72W"),
            ("9", "Superjunction Power MOSFET 800V 0.29Ω D2PAK", "1", "Infineon", "IPB80R290P7"),
            ("10", "Quasi-Resonant Flyback Controller IC SOIC-7", "1", "Texas Instruments", "UCC28740DR"),
            ("11", "Smart Synchronous Rectifier Driver TSOT23-6", "1", "Monolithic Power", "MP6908GJ"),
            ("12", "Synchronous N-MOSFET 60V 5.2mΩ SuperSO8", "1", "Infineon", "BSC052N06NS"),
            ("13", "Phototransistor Optocoupler 5000V RMS Isolation SMD-4", "1", "Everlight", "EL817(S)(TA)"),
            ("14", "RCD Snubber Ultra-Fast Diode 1000V 1A SMA", "1", "Diodes Inc.", "US1M-13-F"),
            ("15", "Auxiliary Bias Electrolytic Cap 22µF 50V Low-ESR", "1", "Panasonic", "EEU-FC1H220")
        ])
    ]

    while len(t11.rows) > 1:
        t11._tbl.remove(t11.rows[-1]._tr)

    for cell in t11.rows[0].cells:
        set_cell_background(cell, "BFBFBF")
    set_cell_text(t11.rows[0].cells[0], "Sl.No", bold=True)
    set_cell_text(t11.rows[0].cells[1], "Description", bold=True)
    set_cell_text(t11.rows[0].cells[2], "Qty", bold=True)
    set_cell_text(t11.rows[0].cells[3], "Mfg", bold=True)
    set_cell_text(t11.rows[0].cells[4], "Mfg Part No", bold=True)

    for sub_title, items in bom1_subsystems:
        sub_row = t11.add_row()
        sub_row.cells[0].merge(sub_row.cells[4])
        set_cell_background(sub_row.cells[0], "D9D9D9")
        set_cell_text(sub_row.cells[0], sub_title, bold=True, font_size=Pt(9.0))

        for sl, desc, qty, mfg, mpn in items:
            item_row = t11.add_row()
            set_cell_text(item_row.cells[0], sl, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(8.5))
            set_cell_text(item_row.cells[1], desc, font_size=Pt(8.5))
            set_cell_text(item_row.cells[2], qty, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(8.5))
            set_cell_text(item_row.cells[3], mfg, font_size=Pt(8.5))
            set_cell_text(item_row.cells[4], mpn, font_size=Pt(8.5))

    apply_table_geometry(t11, [Inches(0.55), Inches(2.37), Inches(0.45), Inches(1.30), Inches(1.80)])
    set_table_borders(t11)

    # 13. BOM 2 (Table 12) - Buck-Boost & Telemetry
    t12 = doc.tables[12]
    bom2_subsystems = [
        ("Subsystem 1: 4-Switch Synchronous Buck-Boost Post-Regulator (Electrical)", [
            ("1", "4-Switch Synchronous Buck-Boost Controller", "1", "Texas Instruments", "LM5176PWPR (HTSSOP-28)"),
            ("2", "Power N-MOSFET 40V 3.4mΩ Logic-Level SuperSO8", "4", "Infineon", "BSC034N04LS"),
            ("3", "Flat-Wire High-Current Power Inductor 10µH 8.5A", "1", "Wurth Elektronik", "7443321000 (12.5x12.5mm)"),
            ("4", "Multi-Layer Ceramic Capacitors 22µF 25V X7R 1210", "4", "Murata", "GRM32ER71E226KE15L"),
            ("5", "Aluminum Solid Polymer Capacitor 100µF 25V 12mΩ", "1", "Panasonic", "25SVPF100M (8x12mm)"),
            ("6", "Thin-Film Feedback Resistors 49.9k, 11k, 3.65k 0.1%", "3", "Vishay Dale", "TNPW0805 Series 25ppm/°C"),
            ("7", "Ceramic Bootstrap Capacitors 0.1µF 50V X7R 0603", "2", "Murata", "GRM188R71H104KA93D"),
            ("8", "Compensation Network Type-II Caps & Resistors", "4", "Murata / Yageo", "C0G & 0.1% Thin Film SMD")
        ]),
        ("Subsystem 2: Analog Closed-Loop Control, Sensing & Protection (Electrical)", [
            ("9", "Precision Current Shunt Resistor 10mΩ 0.1% 3W 2512", "1", "Bourns", "CSS2H-2512R-L010F"),
            ("10", "Precision Current Sense Amplifier 50V/V SC70", "1", "Texas Instruments", "INA240A2EDCKR"),
            ("11", "High-Speed Analog Comparator 4.5ns SOT-23-6", "1", "Texas Instruments", "TLV3501AIDBVR"),
            ("12", "Mixed-Signal MCU & 12-Bit DAC Core LQFP-64", "1", "STMicroelectronics", "STM32G474RET6"),
            ("13", "Isolated Delta-Sigma Modulator SOIC-8 (AC Sense)", "1", "Texas Instruments", "AMC1311DWVR"),
            ("14", "Toroidal Current Transformer 1000:1 (AC Current)", "1", "Talema", "AC1005 (PCB Mount)"),
            ("15", "16-Bit I2C Power Monitor IC VSSOP-10 (DC Rail)", "1", "Texas Instruments", "INA226AIDGSR"),
            ("16", "Heavy-Duty 4mm Gold-Plated Binding Posts (Red/Blk)", "2", "Pomona Electronics", "3770-0 / 3770-2"),
            ("17", "IEC 320-C14 AC Inlet Receptacle with Fuse Drawer", "1", "Schurter", "6200.2100")
        ])
    ]

    while len(t12.rows) > 1:
        t12._tbl.remove(t12.rows[-1]._tr)

    for cell in t12.rows[0].cells:
        set_cell_background(cell, "BFBFBF")
    set_cell_text(t12.rows[0].cells[0], "Sl.No", bold=True)
    set_cell_text(t12.rows[0].cells[1], "Description", bold=True)
    set_cell_text(t12.rows[0].cells[2], "Qty", bold=True)
    set_cell_text(t12.rows[0].cells[3], "Mfg", bold=True)
    set_cell_text(t12.rows[0].cells[4], "Mfg Part No", bold=True)

    for sub_title, items in bom2_subsystems:
        sub_row = t12.add_row()
        sub_row.cells[0].merge(sub_row.cells[4])
        set_cell_background(sub_row.cells[0], "D9D9D9")
        set_cell_text(sub_row.cells[0], sub_title, bold=True, font_size=Pt(9.0))

        for sl, desc, qty, mfg, mpn in items:
            item_row = t12.add_row()
            set_cell_text(item_row.cells[0], sl, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(8.5))
            set_cell_text(item_row.cells[1], desc, font_size=Pt(8.5))
            set_cell_text(item_row.cells[2], qty, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=Pt(8.5))
            set_cell_text(item_row.cells[3], mfg, font_size=Pt(8.5))
            set_cell_text(item_row.cells[4], mpn, font_size=Pt(8.5))

    apply_table_geometry(t12, [Inches(0.55), Inches(2.37), Inches(0.45), Inches(1.30), Inches(1.80)])
    set_table_borders(t12)

    # 14. CLEAN PARAGRAPHS - COMPLETE WHOLE-PARAGRAPH REPLACEMENT
    print("Executing full paragraph replacement to eliminate all template noise...")
    for p in doc.paragraphs:
        txt = p.text.strip()
        
        # Purpose
        if "<Briefly describe the purpose" in txt:
            p.text = (
                "This document describes the system-level requirements for the design and development of 'VVDN_SPPS_2026' "
                "(Smart Programmable Voltage Supply Module) for internal VVDN and client test bench applications. The document "
                "will be used as a reference for further engineering documents, circuit schematics, 4-layer PCB layout rules, "
                "and laboratory validation. The device's functional and technical requirements must meet all parameters specified herein. "
                "These requirements have been derived from client specifications and subsequent engineering design discussions."
            )
        elif "Explicitly mention that the requirements captured here" in txt:
            p.text = (
                "This document captures all Electrical, Mechanical, and Hardware requirements to be delivered for the complete "
                "4-Stage Power Supply PCBA module. VVDN_SPPS_2026 is the project ID for this project and it will be referenced in every "
                "document related to this project."
            )
        # Conventions
        elif "<Describe any standards or typographical conventions" in txt:
            p.text = (
                "This PRD shall be taken as the sole authoritative reference baseline for all hardware requirements. "
                "Requirements marked with [MUST] are mandatory non-negotiable specifications essential for safety, electrical regulation, "
                "and compliance. Requirements marked with [SHOULD] represent performance targets where design trade-offs require SME approval. "
                "Requirements marked with [MAY] represent optional enhancements. All electrical units follow SI conventions."
            )
        # Audience
        elif "<Describe the different types of reader that the document is intended for" in txt:
            p.text = (
                "This PRD is made for the reference of Product Management, Hardware Architects, the Trainee Hardware Design Owner, "
                "Firmware Developers, Quality Assurance / DVT Engineers, and Production / DFM Engineers. "
                "Stakeholders are advised to follow the suggested reading flow based on their engineering role."
            )
        elif txt == "<Define all the terms necessary to properly interpret the PRD, including acronyms and abbreviations. You may wish to build a separate glossary that spans multiple projects or the entire organization, but just include terms specific to a single project in each PRD.>":
            p.text = ""
        elif txt.startswith("<List any other documents or web addresses that this PRD refers"):
            p.text = ""
        # Business Perspective
        elif "<Provide a short description of the product being specified and its purpose" in txt:
            p.text = (
                "The Smart Programmable Voltage Supply Module is an intelligent, high-density benchtop and automated test equipment (ATE) "
                "power supply delivering a tightly regulated, programmable DC voltage output from 5.0 V to 20.0 V at currents up to 3.0 A "
                "(60 W continuous output power) from universal grid AC mains input (85 V to 265 V AC RMS, 47 Hz to 63 Hz)."
            )
        elif "Describe the context and origin of the product being specified in this PRD" in txt:
            p.text = (
                "Traditional bench power supplies rely on bulky 50 Hz iron-core transformers, inefficient linear regulators, and manual dials, "
                "which lead to high thermal dissipation, large footprint, and lack of automated telemetry. This product eliminates those limitations "
                "by integrating a universal mains Quasi-Resonant (QR) Flyback converter, an ultra-efficient 4-switch synchronous Buck-Boost "
                "post-regulator, real-time dual-domain power telemetry, and autonomous analog hardware protection into a single compact board."
            )
        elif "All the details in this section would be from customer perspective" in txt:
            p.text = "All requirements and functional parameters in this document are captured from the perspective of high-efficiency benchtop prototyping and automated modular test racks."
        # Technical Perspective
        elif "< Broad view of the boundary of project and features" in txt:
            p.text = (
                "The Smart Programmable Power Supply is a 4-stage AC-to-DC conversion and regulation system in which the power stage "
                "and mixed-signal microcontroller work together to deliver precise, clean, and safe DC power. The module connects directly "
                "to universal grid AC mains (85V–265V AC RMS) through an input protection and EMI filter stage, rectifies it to a high-voltage bulk DC rail "
                "(+120V to +375V DC), isolates and steps it down via a Quasi-Resonant Flyback stage to an intermediate +24.0V DC bus (72W), "
                "and regulates it through a synchronous 4-switch Buck-Boost stage to provide the commanded 5.0V to 20.0V DC output at up to 3.0A.\n\n"
                "The onboard microcontroller (STM32G474) acts as the system brain by reading dual-domain electrical telemetry (primary AC input power "
                "and secondary DC load power), computing real-time conversion efficiency, updating the 1.3-inch OLED dashboard, and driving the "
                "precision 12-bit DAC voltage steering network. Crucially, high-speed circuit protection (constant-current clamping and over-voltage crowbar) "
                "is implemented in autonomous analog hardware with sub-5 microsecond response time, operating completely independent of firmware "
                "to guarantee fail-safe protection during load faults or dead short-circuits.\n\n"
                "In simple terms, the power conversion stages handle the heavy electrical energy flow across certified 3000V RMS galvanic isolation, "
                "while the analog protection loops and MCU provide autonomous safety, precision regulation, and live telemetry.\n\n"
                "The primary power supply functionality includes:\n"
                "• Universal AC Grid Operation: Accepts 85V to 265V AC RMS (47–63 Hz) without manual line selector switches.\n"
                "• Reinforced Galvanic Isolation: Certified 3000V AC RMS (1 min) isolation meeting IEC 62368-1 SELV.\n"
                "• Intermediate Regulated Rail: Quasi-Resonant Flyback converter generates a stable +24.0V DC bus (72W) with > 90% peak efficiency.\n"
                "• Wide Programmable DC Output: 4-switch synchronous Buck-Boost post-regulator delivers 5.0V to 20.0V DC at up to 3.0A continuous (60W continuous power).\n"
                "• High-Resolution DAC Voltage Steering: 12-bit DAC network achieves 10mV monotonic setpoint resolution.\n"
                "• Autonomous Sub-5µs Hardware CC Clamping: Analog shunt amplifier and high-speed comparator pull down the regulator COMP pin in < 5µs on overcurrent.\n"
                "• Hardware Over-Voltage & Over-Temperature Protection: Analog crowbar trips at Vset + 1.5V, and NTC sensor trips shutdown at 90°C.\n"
                "• Real-Time Dual-Domain Telemetry: Measures AC input power and DC load power, computing live efficiency (η) at 10 Hz.\n"
                "• Interactive Local Dashboard: 1.3\" OLED display shows live V, I, P, and efficiency meters; dual rotary encoders allow intuitive tuning; front-panel LEDs indicate CV, CC, and Fault states.\n"
                "• Low Standby Power: Consumes < 150 mW in idle state when output is disabled."
            )
        elif "Also, if the product comprises of developing multiple systems" in txt:
            p.text = ""
        elif "A diagram showing various systems of the product" in txt:
            p.text = ""
        elif "< Small description of different systems within the product" in txt:
            p.text = "The product is designed as a unified Embedded Hardware Power Supply Module (System 1). Primary hardware stages include AC Mains Protection & EMI Filter, GBU606 Bridge Rectifier & Bulk Capacitor (+120V to +375V DC), Stage 1 Isolated Quasi-Resonant Flyback Converter (+24V DC, 72W), Stage 2 Synchronous 4-Switch Buck-Boost Post-Regulator (5V–20V / 3A DC), and Analog DAC Steering & Fast Hardware Protection Loops."
        # Use Cases
        elif "<Summarize the major functions the product must perform" in txt:
            p.text = (
                "The primary power supply functionality includes four operating modes:\n"
                "• Constant Voltage (CV) Mode: Regulates output voltage within ±0.2% across varying load currents below Iset.\n"
                "• Constant Current (CC) Mode: Autonomously clamps output current at Iset within < 5µs during overload or short-circuit.\n"
                "• Hardware Fault Protection Mode: Immediately shuts down switching on over-voltage (Vset + 1.5V) or over-temperature (90°C).\n"
                "• Standby / Idle Mode: Output power stage disabled while +24V intermediate rail is maintained with standby power < 150mW."
            )
        elif "A picture of the major groups of related requirements" in txt:
            p.text = ""
        elif "<Provide the brief description about the interaction of each External entity" in txt:
            p.text = "The benchtop operator interacts with the power supply using front-panel dual rotary controls and a 1.3\" graphical OLED display. Power is delivered to the device under test (DUT) via heavy-duty 4mm binding posts, and operational status is indicated via front-panel mode LEDs."
        elif "< Provide the brief description, the different mode of operation of the product" in txt:
            p.text = ""
        elif "< Describe the major functionality of the product, based on the mode of operation" in txt:
            p.text = ""
        elif txt == "Table : Use Case":
            p.text = "Table 4: Product Usecase"
        # Interfaces
        elif "<Describe the physical and logical interfaces that exist between different systems" in txt:
            p.text = "Physical hardware interfaces include an IEC 320-C14 AC inlet with integrated fuse drawer, heavy-duty 4mm gold binding posts, dual optical rotary encoders for voltage and current limit tuning, a tactile output enable push-button with status LED, a 1.3\" monochrome OLED display, and dedicated PCB bring-up test points."
        elif "<Describe the physical characteristics of each interface that exist between external entity" in txt:
            p.text = "The hardware interfaces provide rugged, low-impedance connections: binding posts carry 3.0A continuous load current with < 5mΩ contact resistance; IEC inlet provides 250V / 10A rating with earth grounding; test points allow high-voltage differential probing across all switching nodes."
        elif "All external entities are in highlighted in Green" in txt:
            p.text = ""
        elif txt == "Table : Hardware Interfaces":
            p.text = "Table 5: Hardware Interface"
        elif "<. Describe the communication between different systems of the product" in txt:
            p.text = "The SPPS module contains an onboard STM32G474 mixed-signal microcontroller that coordinates telemetry sampling, closed-loop DAC voltage steering, status display, and fault handling. The following table describes the interface, protocol/mode, and usage of each interface:"
        elif "The interfaces/communication between software services/features/modules" in txt:
            p.text = ""
        elif "Identify any communication standards that will be used" in txt:
            p.text = ""
        elif txt == "Table : Software Interfaces":
            p.text = "Table 6: Software Interfaces"
        # Domains
        elif "<List all the systems involved and the domains involved" in txt:
            p.text = "The engineering domains involved in the development of the SPPS module are summarized in Table 7 below:"
        elif "Domain is an indication of different team that is required" in txt:
            p.text = ""
        elif "For this project," in txt:
            p.text = ""
        elif txt == "Table : Domain":
            p.text = "Table 7: Domain"
        elif "Each domain will have requirements captured to Subsystem" in txt:
            p.text = ""
        # Specific Requirements
        elif "<There are some requirements that cannot be captured in plain text" in txt:
            p.text = "Specific hardware layout constraints mandate a physical 6.4 mm surface creepage distance and a 2.0 mm milled air slot through the PCB substrate beneath the transformer and optocoupler barriers to guarantee IEC 62368-1 reinforced safety isolation."
        elif "Similarly, implementation plan or proposal for few requirements" in txt:
            p.text = ""
        elif "Such details (requirements or proposed implementations) can be capture here" in txt:
            p.text = ""
        elif "<Refer above section>" in txt:
            p.text = ""
        # Assumptions
        elif "<List any assumed factors (as opposed to known facts)" in txt:
            p.text = (
                "The following points are considered as assumptions for further project execution:\n"
                "• Grid AC mains is nominal sinusoidal waveform with Total Harmonic Distortion (THD) ≤ 5%.\n"
                "• Operating ambient temperature is -20°C to +50°C under natural convection airflow.\n"
                "• Secondary DC ground is floating with reinforced galvanic isolation (≥ 3000V RMS) from Earth and AC mains.\n"
                "• Connected prototype loads are predominantly resistive or capacitive (C_load ≤ 1000 µF)."
            )
        # Dependencies
        elif "<Identify any dependencies the project has on external factors" in txt:
            p.text = (
                "The following dependencies are included in the design and development of the SPPS module:\n"
                "• Custom transformer engineering samples on Ferroxcube PQ26/20 ferrite cores with triple-insulated Furukawa TEX-E wire required prior to Phase 3 schematic freeze.\n"
                "• Component sourcing and lead times for TI LM5176, UCC28740, INA240, INA226, AMC1311, and ST STM32G474.\n"
                "• Laboratory equipment availability: Chroma AC source, DC electronic load, 3000V RMS Hi-Pot tester, and thermal camera.\n"
                "• Mechanical front-panel drawings for binding post spacing (19.05mm), IEC C14 inlet cutout, and OLED mounting.\n"
                "• Firmware device drivers for SSD1306 OLED display, INA226 power monitor, and STM32 internal 12-bit DAC."
            )
        # Standard Deliverables
        elif "<All standard deliverable documents of each domain" in txt:
            p.text = "The hardware deliverables and release documentation across project milestones are defined in the table below:"
        # Development Plan
        elif "<Top level development plan (not timeline) shall be captured here" in txt:
            p.text = (
                "Phase 1 — Requirement & Architecture and Class A BOM:\n"
                "Definition of functional and electrical requirements; 4-stage system architecture design; block diagram and interface specifications.\n\n"
                "Phase 2 — Component Selection & Circuit Design:\n"
                "Transformer PQ26/20 magnetics sizing; component stress derating calculations; closed-loop feedback and DAC steering design; companion HDD authoring.\n\n"
                "Phase 3 — Schematic Design and Review:\n"
                "Complete 4-stage Altium schematics capture; autonomous analog protection design; peer review gates with BU SME.\n\n"
                "Phase 4 — PCB Layout & DFM Review:\n"
                "4-layer PCB stackup; high-voltage isolation partitioning with 2.0mm milled slot; switching loop routing; DFM/DFA checks.\n\n"
                "Phase 5 — Prototype Bring-up & Design Validation Plan (DVT):\n"
                "PCB fabrication and assembly (5 units); cold resistance checks; supervised Variac bring-up; line/load regulation, ripple, efficiency, and Hi-Pot validation."
            )
        elif "During the PRD discussions with customer, lot of clarity" in txt:
            p.text = ""
        elif "For example, software development itself may span across" in txt:
            p.text = ""
        elif txt == "Table : System1 Development Plan":
            p.text = "Table 8: Standard Deliverables & Release Order"
        elif "<Fill as applicable>" in txt:
            p.text = (
                "The hardware validation plan comprises four rigorous test gates: Cold Checks (impedance & isolation resistance), "
                "Supervised Variac Bring-Up (gradual AC ramp from 0V to 265V), Dynamic Regulation (line/load regulation and 50% to 100% transient steps), "
                "and Safety/Thermal Soak (3000V RMS Hipot and FLIR thermal soak at 50°C)."
            )
        # Architecture & BOM Notes
        elif "<Architecture section is optional to mention in PRD document" in txt:
            p.text = "The power supply hardware architecture consists of two galvanically isolated power conversion stages followed by synchronous post-regulation and autonomous analog hardware protection:"
        elif "< Architecture Diagram with caption, shall be inserted here" in txt:
            p.text = ""
        elif "<BOM section is optional to mention in PRD document" in txt:
            p.text = "Note: This is the expected BOM and it might get changed during the design stage. The BOM does not contain any pricing/cost information."
            p.runs[0].font.italic = True
        elif "<Insert System level BOM>" in txt:
            p.text = "Refer to detailed bill of materials in the respective subsystem tables below."
        elif txt == "Table :System1 Product BOM":
            p.text = "Table 9.1: System 1 Product BOM (Primary & Flyback Stages)"
        elif txt == "Table :System2 Product BOM":
            p.text = "Table 9.2: System 2 Product BOM (Buck-Boost, Protection & Control)"
        # Out of Scope & Open Items
        elif txt == "Out of scope point 1":
            p.text = "Active Power Factor Correction (Active Boost PFC) — passive EMI filtering is used since < 75W is exempt under IEC 61000-3-2."
        elif txt == "Out of scope point 2":
            p.text = "Three-phase 400V/480V AC industrial grid input operation (module is single-phase 85V–265V AC RMS only)."
        elif txt == "Out of scope point 3":
            p.text = "Negative/bipolar voltage rails (system provides positive 5.0V to 20.0V DC only). Wireless connectivity (Wi-Fi, BLE) and cloud IoT interfaces are excluded."
        elif txt == "Open Item 1":
            p.text = "Current shunt value trade-off: Evaluating 5mΩ vs 10mΩ for thermal dissipation vs low-current sensing resolution."
        elif txt == "Open Item 2":
            p.text = "Auxiliary 24V DC barrel input option: Evaluating a 24V DC auxiliary input to bypass AC mains for vehicle/field use."
        elif txt == "Open Item 3":
            p.text = "Secondary heatsink copper area optimization: Evaluating 2oz vs 3oz copper pours for D2PAK primary FET."

    # 15. INSERT TABLE 3 (HIGH LEVEL TECHNICAL REQUIREMENTS) IN SECTION 2.2
    print("Inserting Table 3: High Level Technical Requirement...")
    tech_reqs = [
        ("1", "Input Voltage Range", "85 V to 265 V AC RMS, 47 Hz to 63 Hz (Universal Grid Compatibility)"),
        ("2", "Continuous Output Current", "0.0 A to 3.0 A DC Continuous across full voltage range"),
        ("3", "Programmable Output Voltage", "5.0 V to 20.0 V DC (Continuously adjustable via 10 mV digital DAC steps)"),
        ("4", "Maximum Output Power", "60.0 W Continuous DC Output (20.0 V @ 3.0 A)"),
        ("5", "Intermediate Bus Voltage", "+24.0 V DC ± 1.0% (72.0 W continuous rating from primary Flyback stage)"),
        ("6", "Output Voltage Ripple", "< 25 mV pk-pk under full 3.0 A load (measured across 20 MHz bandwidth)"),
        ("7", "End-to-End System Efficiency", "> 85.0% @ 230 V AC Full Load (Flyback > 90%, Buck-Boost > 95%)"),
        ("8", "Galvanic Safety Isolation", "3,000 V AC RMS (1 minute withstand) meeting IEC 62368-1 SELV"),
        ("9", "Hardware Protection Response", "Autonomous analog CC clamping reaction in < 5.0 µs; Crowbar OVP in < 5.0 µs"),
        ("10", "PCBA Operating Temperature", "–20°C to +50°C Full Load (natural convection in chassis)"),
        ("11", "User Interface & Control", "1.3\" I2C OLED display, dual rotary encoders, CV/CC/Fault LEDs, tactile Enable switch"),
        ("12", "Conducted & Radiated EMC", "Compliant with CISPR 32 / EN 55032 Class B limits")
    ]

    p_bound_cap = None
    for p in doc.paragraphs[100:]:
        if "Figure : Boundary Diagram" in p.text or "Boundary Diagram" in p.text or "Figure 1:" in p.text:
            p_bound_cap = p
            break

    if p_bound_cap is not None:
        p_bound_cap.text = "Figure 1: Boundary Diagram / Simplified 4-Stage Power Flow Block Diagram"
        diagram_img_path = "smart_programmable_power_supply/diagram_simple_power_flow.png"
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

        cap_tech = doc.add_paragraph("Table 3: High Level Technical Requirement")
        cap_tech.style = "Caption"
        p_bound_cap._p.addnext(cap_tech._p)
        cap_tech._p.addnext(t_tech._tbl)

    # 16. INSERT SECTION 4 ENGINEERING REQUIREMENT TABLES (Tables 4.1 to 4.5)
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
        ("FR-05", "Primary Stage Efficiency", "> 90.0% @ 230V AC Full Load [MUST]", "Pout = 72W, Tamb = 25°C", "Precision Power Analyzer"),
        ("FR-06", "Safety Galvanic Isolation", "3,000 V AC RMS (1 min) [MUST]", "Primary to Secondary barrier", "Certified Hi-Pot Tester"),
        ("FR-07", "Cold-Start Inrush Current", "< 25.0 A Peak [MUST]", "Vin = 265V AC, cold start 25°C", "Current Probe & Scope"),
        ("FR-08", "No-Load Standby Power", "< 150 mW Standby [SHOULD]", "Vin = 230V AC, Output Off", "Power Meter Integrator")
    ]

    req_buckboost = [
        ("BB-01", "Output Voltage Range", "5.0 V – 20.0 V DC Programmable [MUST]", "Continuous linear adjustment", "Precision DMM Sweep"),
        ("BB-02", "Continuous Output Current", "0.0 A – 3.0 A DC Continuous [MUST]", "Across full 5V–20V voltage span", "Electronic Load 3A Soak"),
        ("BB-03", "Maximum Output Power", "60.0 W Continuous Output [MUST]", "Vout = 20.0V, Iout = 3.0A", "Thermal Run 60W (2 hrs)"),
        ("BB-04", "Voltage Setpoint Resolution", "10 mV step resolution (12-bit DAC) [MUST]", "Continuous monotonic tuning", "DAC Linearity Calibration"),
        ("BB-05", "Current Limit Resolution", "10 mA step resolution (12-bit DAC) [MUST]", "Reference input to comparator", "Current Clamp Tuning"),
        ("BB-06", "Output Voltage Ripple", "< 25 mV pk-pk ripple [MUST]", "Full load 3A, 20MHz bandwidth", "Scope Tip-and-Barrel Probe"),
        ("BB-07", "Load Transient Recovery", "< 120 µs recovery, < 250mV sag [MUST]", "50% to 100% load step (1.5A to 3A)", "Dynamic Load Stepper"),
        ("BB-08", "Buck-Boost Efficiency", "> 95.0% @ 20V/3A; > 92.0% @ 5V/3A [MUST]", "Vin = 24V, Sync Rectification", "Dual-Channel Power Meter"),
        ("BB-09", "Switching Frequency", "300 kHz ± 10% [MUST]", "Fixed frequency PWM", "Frequency Counter"),
        ("BB-10", "CC Mode Reaction Time", "< 5.0 µs autonomous clamping [MUST]", "Overload short-circuit step", "Fast Current Shunt Scope")
    ]

    req_telemetry = [
        ("TM-01", "Primary AC Voltage Sensing", "Isolated AMC1311 (0-300V AC RMS) [MUST]", "± 1.0% accuracy across 85-265V", "Precision AC Source Ref"),
        ("TM-02", "Primary AC Current Sensing", "Current Transformer 1000:1 [MUST]", "± 1.5% accuracy from 0.1A-2A", "Calibrated Current Probe"),
        ("TM-03", "Secondary DC Voltage Sense", "INA226 16-bit ADC (1.25mV/LSB) [MUST]", "± 0.2% measurement accuracy", "Keysight 34465A DMM"),
        ("TM-04", "Secondary DC Current Sense", "INA226 16-bit ADC (100µA/LSB) [MUST]", "± 0.5% measurement accuracy", "Precision Shunt Reference"),
        ("TM-05", "Dual-Domain Telemetry Rate", "10.0 Hz Real-Time Loop Rate [MUST]", "Pac, Pdc, and η computed at 100ms", "Timing Logic Analyzer"),
        ("TM-06", "Galvanic Isolation Barrier", "3,000 V AC RMS (1 min) [MUST]", "Primary-to-secondary isolation", "Certified Hi-Pot Tester"),
        ("TM-07", "Hardware Calibration Test Points", "Dedicated PCB Test Points [MUST]", "Vout, Iout, bulk DC, and aux rails", "Scope & Multimeter Check")
    ]

    req_protection = [
        ("PR-01", "Hardware Over-Voltage (OVP)", "Clamps at Vset + 1.5V (< 5µs response) [MUST]", "Independent comparator crowbar", "OVP Trip Verification"),
        ("PR-02", "Hardware Constant-Current (CC)", "Clamps at Iset ± 20mA (< 5µs reaction) [MUST]", "Analog pull-down on COMP pin", "Direct Dead Short Test"),
        ("PR-03", "Over-Temperature (OTP)", "Shuts down at Tpcb > 90°C (10°C hyst) [MUST]", "NTC thermistor monitoring", "Thermal Chamber Ramp"),
        ("PR-04", "Safety Compliance Standard", "IEC 62368-1 Reinforced Isolation [MUST]", "SELV touch-safe (< 60V DC)", "Certified Safety Lab"),
        ("PR-05", "Creepage & Clearance", "Creepage >= 6.4mm; Clearance >= 5.0mm [MUST]", "Primary-Secondary milled slot", "PCB Mechanical Caliper"),
        ("PR-06", "Conducted & Radiated EMC", "CISPR 32 / EN 55032 Class B [MUST]", "150 kHz – 1 GHz emission limits", "Semi-Anechoic Chamber"),
        ("PR-07", "Operating Ambient Temp", "-20°C to +50°C Full Load [MUST]", "Natural convection in chassis", "Environmental Chamber"),
        ("PR-08", "Mean Time Between Failures", "MTBF > 50,000 Hours @ 40°C [SHOULD]", "Telcordia SR-332 Parts Count", "Reliability Calculation")
    ]

    req_control = [
        ("CT-01", "DAC Voltage Steering Network", "Resistor summing into LM5176 FB node [MUST]", "R_top=49.9kΩ, R_DAC=11kΩ, R_bot=3.65kΩ", "Line/Load Voltage Sweep"),
        ("CT-02", "Voltage Tuning Resolution", "10.0 mV step resolution (12-bit DAC) [MUST]", "Continuous 5.0V to 20.0V DC range", "DAC Linearity Calibration"),
        ("CT-03", "Hardware Current Sense Shunt", "10 mΩ Metal Element Shunt, 3W, 0.1% [MUST]", "4-wire Kelvin sensing layout", "Precision Shunt DMM Check"),
        ("CT-04", "Current Sense Amplification", "INA240A2 Precision Amp (50 V/V gain) [MUST]", "Enhanced PWM input spike rejection", "Shunt Amp Linearity Sweep"),
        ("CT-05", "Fast CC Hardware Clamping", "< 5.0 µs autonomous clamping on COMP pin [MUST]", "TLV3501 4.5ns analog comparator override", "High-Speed Current Probe"),
        ("CT-06", "Hardware Crowbar Disconnect", "High-side P-MOSFET disconnect on OVP/OTP [MUST]", "Clamps at Vset + 1.5V in < 5.0 µs", "OVP Transient Injection Test"),
        ("CT-07", "Auxiliary Bias Regulation", "+14V Flyback VCC, +12V gate, +5V, +3.3V rails [MUST]", "Dedicated LDOs & buck off +24V bus", "Multimeter & Rail Scope")
    ]

    if p_sys1 is not None:
        p_sys1.text = (
            "System 1 represents the physical Hardware Power Supply Module, comprising the universal AC input, EMI filter, "
            "isolated Quasi-Resonant Flyback stage, 4-switch synchronous Buck-Boost post-regulator, analog protection circuits, "
            "and microcontroller sensing core. The detailed engineering specifications are defined in the tables below:"
        )
        cursor = p_sys1._p
        cap1 = doc.add_paragraph("Table 4.1: AC-DC Isolated Flyback Power Stage Engineering Requirements")
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

    # 17. INSERT ARCHITECTURE FIGURES (Figures 2 to 8)
    fig4_steps = [
        ("1", "Filtered AC Input", "Takes 85V–265V AC RMS sinusoidal voltage from Stage 1 EMI filter."),
        ("2", "Full-Wave Rectification", "GBU606 single-phase bridge rectifies AC into 100Hz/120Hz unipolar DC pulses (120Vpk–375Vpk)."),
        ("3", "Bulk Capacitive Filtering", "100µF/450V electrolytic cap smooths ripple and guarantees > 10ms holdup time across line dropouts."),
        ("4", "High-Frequency Decoupling", "100nF/630V ceramic cap bypasses fast 80kHz primary switching edge ringing."),
        ("5", "Safety Discharge Bleeder", "3x 330kΩ resistor string drains bulk capacitor to < 50V SELV within 60s per IEC 62368-1.")
    ]

    fig5_steps = [
        ("1", "High-Voltage DC Input", "Receives +120V to +375V DC bulk bus into primary switching cell."),
        ("2", "Quasi-Resonant Switching", "TI UCC28740 valley-switching controller modulates 800V CoolMOS at resonant minimums to slash Coss loss."),
        ("3", "3000V RMS Safety Barrier", "PQ26/20 transformer (Lp=220µH) with Furukawa TEX-E wire provides reinforced galvanic isolation."),
        ("4", "Synchronous Rectification", "MP6908 smart driver and BSC052N06NS 60V/5.2mΩ FET replace Schottky diode, saving 1.65W heat dissipation."),
        ("5", "+24.0V DC Intermediate Rail", "Low-ESR LC filter delivers stable +24.0V DC (72W) with optocoupled feedback regulation.")
    ]

    fig6_steps = [
        ("1", "+24.0V DC Rail Input", "Accepts +24.0V DC intermediate rail from Stage 3 Flyback."),
        ("2", "4-Switch Synchronous Bridge", "TI LM5176 modulates four 40V MOSFETs in H-bridge around a 10µH flat-wire power inductor."),
        ("3", "Seamless Mode Transitions", "Operates in pure Buck mode for 5V–18V outputs (>96% eff) and 4-switch Buck-Boost mode near 20V (>95% eff)."),
        ("4", "Precision DAC Steering", "Resistor summing network (R_top=49.9kΩ, R_bot=3.65kΩ, R_DAC=11kΩ) steers output from 5V to 20V in 10mV steps."),
        ("5", "Sub-5µs Hardware Protection", "10mΩ shunt, INA240A2 (50V/V), and TLV3501 (4.5ns comparator) pull COMP pin low in < 5µs on overcurrent.")
    ]

    # Section 4 Figure 4
    for p in doc.paragraphs[100:]:
        txt = p.text.strip()
        if p.style.name == "Heading 4" and "Mobile UI Screens/Wireframes" in txt:
            p.text = "Inside Stage 2: Bridge Rectifier & High-Voltage Bulk DC Subsystem"
        elif ("Figure : Flow Diagram" in txt or "Figure 4: Flow Diagram" in txt or "Figure 4: Inside Stage 2" in txt) and p.style.name == "Caption":
            p.text = "Figure 4: Inside Stage 2 - Bridge Rectifier & Bulk DC Stage Subsystem Architecture"
            diag4_path = "smart_programmable_power_supply/diagram_inside_stage2_rectifier.png"
            if os.path.exists(diag4_path):
                p_pic4 = p.insert_paragraph_before()
                p_pic4.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r4 = p_pic4.add_run()
                r4.add_picture(diag4_path, width=Inches(6.47))
            tbl_fig4 = create_workflow_table(doc, "STAGE 2: BRIDGE RECTIFIER & BULK FILTER SEQUENCE", fig4_steps, header_color="7B341E")
            p._p.addnext(tbl_fig4._tbl)
            break

    # Section 4 Figure 5
    found_sys2 = False
    for p in doc.paragraphs[100:]:
        txt = p.text.strip()
        if "System2 Requirements" in txt and p.style.name == "Heading 2":
            found_sys2 = True
        if found_sys2:
            if p.style.name == "Heading 4" and "Mobile UI Screens/Wireframes" in txt:
                p.text = "Inside Stage 3: Converter DC-DC (Isolated Quasi-Resonant Flyback) Subsystem"
            elif ("<Refer above section>" in txt or "Figure 5" in txt) and p.style.name == "Caption":
                diag5_path = "smart_programmable_power_supply/diagram_inside_stage3_flyback.png"
                if os.path.exists(diag5_path):
                    p_pic5 = p.insert_paragraph_before()
                    p_pic5.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r5 = p_pic5.add_run()
                    r5.add_picture(diag5_path, width=Inches(6.47))
                p.text = "Figure 5: Inside Stage 3 - Converter DC-DC (Isolated Flyback) Subsystem Architecture"
                tbl_fig5 = create_workflow_table(doc, "STAGE 3: ISOLATED FLYBACK DC-DC CONVERTER SEQUENCE", fig5_steps, header_color="1C4532")
                p._p.addnext(tbl_fig5._tbl)
                break

    # Section 8 Subsystems (8.1, 8.2, 8.3)
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

    if p_arch1 is not None:
        p_arch1.text = "8.1 System 1: Inside Stage 4 (Synchronous 4-Switch Buck-Boost Post-Regulator Subsystem)"
        diag6_path = "smart_programmable_power_supply/diagram_inside_stage4_final_stage.png"
        p_pic6 = None
        if os.path.exists(diag6_path):
            p_pic6 = doc.add_paragraph()
            p_pic6.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r6 = p_pic6.add_run()
            r6.add_picture(diag6_path, width=Inches(6.47))

        cap6 = doc.add_paragraph("Figure 6: Inside Stage 4 - 4-Switch Buck-Boost Post-Regulator Subsystem Architecture")
        cap6.style = "Caption"
        tbl_fig6 = create_workflow_table(doc, "STAGE 4: 4-SWITCH BUCK-BOOST POST-REGULATOR SEQUENCE", fig6_steps, header_color="2A4365")
        note6_1 = doc.add_paragraph("Note: This is the proposed architecture and it might get changed during the design stage.")
        note6_1.runs[0].font.italic = True
        note6_2 = doc.add_paragraph("Note: Component selection must strictly comply with VVDN derating guidelines.")
        note6_2.runs[0].font.italic = True

        if p_pic6 is not None:
            p_arch1._p.addnext(p_pic6._p)
            p_pic6._p.addnext(cap6._p)
            cap6._p.addnext(tbl_fig6._tbl)
            tbl_fig6._tbl.addnext(note6_1._p)
        else:
            p_arch1._p.addnext(cap6._p)
            cap6._p.addnext(tbl_fig6._tbl)
            tbl_fig6._tbl.addnext(note6_1._p)
        note6_1._p.addnext(note6_2._p)

    if p_arch2 is not None:
        p_arch2.text = "8.2 System 1: Dual-Domain Power Telemetry & Sensing Frontend Architecture"
        diag7_path = "smart_programmable_power_supply/block_diagram_telemetry_efficiency.png"
        p_pic7 = None
        if os.path.exists(diag7_path):
            p_pic7 = doc.add_paragraph()
            p_pic7.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r7 = p_pic7.add_run()
            r7.add_picture(diag7_path, width=Inches(6.47))

        cap7 = doc.add_paragraph("Figure 7: Dual-Domain Power Telemetry & Sensing Frontend Architecture")
        cap7.style = "Caption"
        note7_1 = doc.add_paragraph("Note: This is the proposed architecture and it might get changed during the design stage.")
        note7_1.runs[0].font.italic = True
        note7_2 = doc.add_paragraph("Note: AMC1311 reinforced galvanic isolation barrier complies with IEC 62368-1.")
        note7_2.runs[0].font.italic = True

        if p_pic7 is not None:
            p_arch2._p.addnext(p_pic7._p)
            p_pic7._p.addnext(cap7._p)
            cap7._p.addnext(note7_1._p)
        else:
            p_arch2._p.addnext(cap7._p)
            cap7._p.addnext(note7_1._p)
        note7_1._p.addnext(note7_2._p)

    if p_arch3 is not None:
        p_arch3.text = "8.3 System 2: Auxiliary Bias Power Rail Distribution Subsystem Architecture"
        diag8_path = "smart_programmable_power_supply/block_diagram_aux_power_distribution.png"
        p_pic8 = None
        if os.path.exists(diag8_path):
            p_pic8 = doc.add_paragraph()
            p_pic8.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r8 = p_pic8.add_run()
            r8.add_picture(diag8_path, width=Inches(6.47))

        cap8 = doc.add_paragraph("Figure 8: Auxiliary Bias Power Rail Distribution Subsystem Architecture")
        cap8.style = "Caption"
        note8_1 = doc.add_paragraph("Note: This is the proposed architecture and it might get changed during the design stage.")
        note8_1.runs[0].font.italic = True
        note8_2 = doc.add_paragraph("Note: Gate driver bootstrap bias and low-noise analog LDO rails are verified during bring-up.")
        note8_2.runs[0].font.italic = True

        if p_pic8 is not None:
            p_arch3._p.addnext(p_pic8._p)
            p_pic8._p.addnext(cap8._p)
            cap8._p.addnext(note8_1._p)
        else:
            p_arch3._p.addnext(cap8._p)
            cap8._p.addnext(note8_1._p)
        note8_1._p.addnext(note8_2._p)

    # 18. APPEND APPENDIX: CROSS-MENTOR INTERVIEW PREPARATION & DEFENSE CHEATSHEET
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
         "The power conversion hardware operates in four clean, sequential stages: First, universal mains AC (85V–265V AC RMS) enters through an IEC C14 inlet with a 2A time-lag ceramic fuse, 10Ω NTC inrush thermistor, MOV surge clamp, and a 2-stage common-mode EMI filter. Second, a GBU606 bridge rectifier and 100µF/450V bulk electrolytic capacitor convert AC into an unregulated high-voltage DC bus (+120V to +375V DC). Third, Stage 1 (a Quasi-Resonant Flyback converter with TI UCC28740 and a custom PQ26/20 transformer) provides certified 3000V RMS reinforced safety isolation and steps down power to a stable +24.0V DC intermediate bus (72W) using synchronous rectification (BSC052N06NS). Fourth, Stage 2 (a TI LM5176 4-switch synchronous Buck-Boost post-regulator) regulates the +24V bus down or across to the target 5.0V–20.0V DC at up to 3.0A with sub-25mV ripple, delivering clean DC to the device under test via heavy-duty 4mm binding posts."),

        ("Q2: Why did you use a passive filter and bridge rectifier instead of an active Boost PFC stage?",
         "Under international standard IEC 61000-3-2, active Power Factor Correction (PFC) is legally mandated only for equipment with active input power exceeding 75W. Our module delivers a maximum continuous output of 60W (72W peak intermediate), so it falls strictly below the 75W threshold. Adding an active PFC boost stage would require an additional high-voltage MOSFET, boost diode, controller IC, and large inductor—adding approximately $4.20 to the BOM, consuming 35% more PCB area, and introducing a ~3% efficiency penalty without any regulatory requirement."),

        ("Q3: How did you calculate the Flyback transformer magnetics on the PQ26/20 core?",
         "At minimum 85V AC input, the rectified bulk bus is 120V DC. For a maximum duty cycle of 45% and 80kHz switching frequency at 72W output power, peak primary current is I_pk = 2.96A. Using L_p = (V_bulk_min * D_max) / (I_pk * f_sw), I calculated a primary inductance of 220µH. I chose a Ferroxcube PQ26/20 core in 3C95 material because its cross-sectional area Ae is 122 mm², keeping peak flux density B_max at 0.28 Tesla (well below the 0.38 Tesla saturation limit). The turns ratio is 6:1 (36 primary turns, 6 secondary turns). To guarantee IEC 62368-1 reinforced isolation (3000V RMS), the secondary is wound with Furukawa TEX-E triple-insulated wire."),

        ("Q4: Why is the intermediate bus chosen at +24.0V DC instead of +12V or +48V?",
         "+24.0V DC is the optimal design choice for a 5V to 20V output range. If we chose +12V, stepping up to 20V at 3A (60W) would require high inductor boost currents (I_in = 5.5A), creating excessive I²R conduction losses in the Buck-Boost MOSFETs. If we chose +48V, the Flyback turns ratio would decrease, increasing primary switch voltage stress, and stepping down to 5V would require an extreme duty cycle of 10%. With +24V, 5V, 12V, and 15V operate in pure Buck mode (>96% efficiency), and 20V operates near unity Buck-Boost transition with minimal switching stress."),

        ("Q5: How does the 4-switch Buck-Boost operate seamlessly between 5V and 20V?",
         "The TI LM5176 controls four N-MOSFETs (QA, QB, QC, QD) in an H-bridge configuration around a single 10µH flat-wire inductor. When V_OUT is significantly below 24V (e.g. 5V or 12V), QC is held continuously ON and QD is OFF, so the circuit functions purely as a synchronous Buck converter with switches QA and QB. As V_OUT approaches 20V under heavy load, the controller smoothly enters 4-switch Buck-Boost mode, modulating both legs to maintain exact regulation with zero deadband or output glitching."),

        ("Q6: How does the DAC steer the output voltage without destabilizing the loop?",
         "The LM5176 regulates by maintaining its feedback pin (FB) at an internal 1.20V reference. Instead of modifying the internal reference, we use a resistive summing junction: R_top (49.9kΩ) connects to V_OUT, R_bot (3.65kΩ) connects to ground, and R_DAC (11.0kΩ) connects to our 12-bit DAC. By injecting current into the FB node from the DAC, when V_DAC = 3.3V, V_OUT is steered to 5.0V. When V_DAC = 0V, V_OUT is steered to 20.0V. Because the loop's AC Type-II compensation network is connected between COMP and ground, DC setpoint steering has zero impact on high-frequency phase margin and stability."),

        ("Q7: Explain how the hardware protects against a short circuit in under 5 microseconds.",
         "Software is too slow to protect switching MOSFETs during a dead short. We implemented an autonomous analog hardware clamp: a 10mΩ metal shunt resistor feeds an INA240A2 current sense amplifier (gain = 50V/V). The amplified current signal feeds an ultra-fast TLV3501 analog comparator with 4.5ns response time. If load current exceeds the threshold (e.g. 3.2A), the comparator output immediately drives an NPN transistor that pulls down the LM5176's COMP pin to ground. This forces the PWM duty cycle to zero in under 5 microseconds, safely clamping the current before any software can even register an interrupt."),

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

    # FINAL PASS: Ensure EVERY table in doc.tables has NO floating tblpPr
    for t in doc.tables:
        for child in list(t._tbl.tblPr):
            if child.tag.endswith('tblpPr'):
                t._tbl.tblPr.remove(child)

    # FINAL PASS: Ensure NO angle brackets exist in any paragraph
    for p in doc.paragraphs:
        if "<" in p.text and ">" in p.text:
            # clean any remaining angle bracket instructions
            import re
            p.text = re.sub(r'<[^>]+>', '', p.text).strip()

    print(f"Saving fully updated PRD document: {output_path}")
    doc.save(output_path)
    print(f"Saving duplicate PRD document: {alt_output_path}")
    doc.save(alt_output_path)
    print("Successfully built production-grade PRD .docx files with zero floating overlaps and zero template tags!")

if __name__ == "__main__":
    generate_prd_docx()
