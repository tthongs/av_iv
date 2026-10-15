#!/usr/bin/env python3
"""
Generate a clean, standalone .docx document containing the comprehensive
architecture and component specification table for:
Stage 3: Converter DC-DC (Isolated Flyback) Subsystem

Designed for seamless copying and pasting directly into Microsoft Word PRD documents.
"""

import os
import sys

# Ensure python-docx from venv can be imported
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

def set_cell_margins(cell, top=120, bottom=120, left=140, right=140):
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

def apply_table_geometry(table, col_widths, total_width_inches=7.0):
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

def set_cell_content(cell, text, font_name="Arial", font_size=Pt(8.5), bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, color_rgb=(26, 32, 44)):
    """Set formatted text in a cell."""
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = font_size
    run.font.bold = bold
    run.font.color.rgb = RGBColor(*color_rgb)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    set_cell_margins(cell, top=100, bottom=100, left=130, right=130)

def main():
    doc = docx.Document()

    # Configure 0.75-inch page margins for clean presentation
    for sec in doc.sections:
        sec.top_margin = Inches(0.75)
        sec.bottom_margin = Inches(0.75)
        sec.left_margin = Inches(0.75)
        sec.right_margin = Inches(0.75)

    # Document Header / Context
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("Stage 3: Converter DC-DC (Uniform-Frequency Isolated Flyback) Subsystem")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(14)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(26, 54, 93)  # Dark Blue #1A365D

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(12)
    run_sub = sub_p.add_run("Internal Subsystem Architecture, Component Selection & Engineering Requirements Table")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(10)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(74, 85, 104)

    # Table Column Configuration (Total = 7.0 inches)
    col_widths = [
        Inches(1.20),  # Functional Sub-Block
        Inches(0.85),  # Circuit Ref
        Inches(1.40),  # Selected Component / Part No
        Inches(1.65),  # Key Specifications & Ratings
        Inches(1.90)   # Functional Role & Performance Target
    ]

    headers = [
        "Functional Sub-Block",
        "Circuit Ref",
        "Selected Component / IC",
        "Key Specifications & Ratings",
        "Functional Role & Performance Target"
    ]

    table_data = [
        (
            "HVDC Input Interface",
            "+HVDC",
            "Stage 2 Bulk DC Bus Link",
            "+120 V to +375 V DC operating span",
            "Low-impedance high-voltage input rail feeding transformer primary winding and snubber network."
        ),
        (
            "Uniform-Freq PWM Controller",
            "U1",
            "Texas Instruments UC3843 / UCC28C43 (SOIC-8 / DIP-8)",
            "Uniform 65 kHz clock, RT/CT oscillator, cycle-by-cycle CS, direct totem-pole gate out",
            "Generates constant-frequency PWM switching pulses at a uniform 65 kHz rate, providing predictable EMI harmonics and deterministic current-mode control."
        ),
        (
            "Oscillator Timing Network",
            "R_T\nC_T",
            "Precision Thin-Film Resistor +\nC0G/NP0 Ceramic Capacitor",
            "R_T = 10.0 kΩ (1%),\nC_T = 2.2 nF (50V C0G)",
            "Sets constant oscillator clock frequency: f_sw approx 1.72 / (R_T x C_T) = 65 kHz uniform clock without frequency jitter."
        ),
        (
            "Primary Power Switch",
            "Q1",
            "STMicroelectronics STP10NK80Z / Infineon IPB80R290P7",
            "800 V, 17 A, R_DS(on) = 0.29 Ω, V_DS,peak = 599 V",
            "Main switching element modulated by 65 kHz PWM gate drive. Voltage stress derated to 74.9% of 800V rating (< 75% limit)."
        ),
        (
            "Primary Current Sensing",
            "R_CS",
            "Current Sense Shunt Resistor Network",
            "Low-inductance metal strip, 0.25 Ω, 1%, 2 W",
            "Monitors primary switch peak current (I_pk = 2.96 A) on UC3843 ISENSE pin (Pin 3) with 1.0 V internal comparator threshold for cycle-by-cycle OCP."
        ),
        (
            "RCD Snubber Clamp",
            "D_snub\nR_snub\nC_snub",
            "Diodes Inc. US1M +\n3x 68 kΩ in parallel (22.6 kΩ, 3W) +\n1.0 nF / 1 kV Ceramic",
            "Diode: 1000 V, 1 A, t_rr = 75 ns;\nCap: 1 nF / 1000 V ceramic;\nClamp: ~216 V clamp level",
            "Damps high-voltage inductive kick caused by transformer leakage inductance (L_lk approx 2.2 uH); clamps peak drain voltage spike safely below 650 V peak."
        ),
        (
            "Flyback Power Transformer",
            "TX1",
            "Ferroxcube PQ26/20 (3C95 Ferrite) / EE25 Core",
            "L_p = 220 uH +/- 10%, B_max = 0.148 T (B_sat = 0.38 T), N_p = 36 T",
            "Stores energy during switch on-time and delivers 72 W continuous power to secondary during off-time (Np:Ns = 6:1 turns ratio)."
        ),
        (
            "Auxiliary Bias Winding",
            "TX1_AUX",
            "N_aux = 5 T (0.25 mm wire) +\nFast Diode (UF4004) & 47 µF Cap",
            "Output: +14.0 V DC bias rail",
            "Sustains UC3843 VCC pin (Pin 7) above UVLO threshold (8.4 V start / 7.6 V min) after initial high-voltage bleed startup."
        ),
        (
            "Galvanic Safety Isolation Barrier",
            "TX1_ISO",
            "Furukawa TEX-E Triple-Insulated Wire (TIW)",
            "N_s = 6 T (N_p:N_s = 6:1), Reinforced insulation, >= 6.4 mm creepage",
            "Complies with IEC 62368-1 standard. Provides certified >= 3000 V RMS dielectric withstand between primary hot domain and secondary touch-safe SELV domain."
        ),
        (
            "Secondary Schottky Barrier Rectifier",
            "D_SEC",
            "ON Semi / Vishay MBR10100 / MBR20100CT",
            "100 V, 10 A Schottky Barrier Diode, V_F = 0.60 V, TO-220 with heatsink",
            "Performs high-speed passive rectification of secondary flyback pulses. Highly reliable and robust passive design, eliminating active gate driver IC complexity."
        ),
        (
            "Secondary LC Output Filter",
            "C_sec\nL_sec",
            "470 µF / 35 V Low-ESR Electrolytic +\n2.2 µH Inductor + 22 µF MLCC",
            "Low-ESR filtering, Delta V_ripple < 50 mV pk-pk",
            "Attenuates 65 kHz fundamental switching ripple and high-frequency commutation spikes to produce a quiet intermediate DC rail."
        ),
        (
            "Isolated Closed-Loop Feedback",
            "OPTO1\nU3",
            "Everlight PC817 / EL817 Optocoupler +\nTI TL431 Shunt Regulator",
            "5000 V RMS optical isolation, 2.495 V internal bandgap, 0.5%",
            "Precision resistor divider samples +24.0 V rail, driving optocoupler LED to pull down UC3843 COMP pin (Pin 1), regulating rail to +/- 1.0%."
        ),
        (
            "Intermediate Rail Output",
            "+24V_BUS",
            "Intermediate DC Power Distribution Bus",
            "+24.0 V DC +/- 1.0%, 72.0 W continuous (3.0 A), 84 W peak",
            "Delivers stable intermediate regulated DC power to Stage 4 (Synchronous Buck-Boost Post-Regulator) and secondary auxiliary housekeeping LDOs."
        )
    ]

    # Create Table
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="CBD5E0", sz="4")
    apply_table_geometry(table, col_widths, total_width_inches=7.0)

    # Populate Header Row
    header_row = table.rows[0]
    for c_idx, heading in enumerate(headers):
        cell = header_row.cells[c_idx]
        set_cell_background(cell, "1A365D")  # Dark Blue #1A365D
        set_cell_content(
            cell, heading,
            font_name="Arial",
            font_size=Pt(9.0),
            bold=True,
            align=WD_ALIGN_PARAGRAPH.CENTER,
            color_rgb=(255, 255, 255)
        )

    # Populate Data Rows
    for r_idx, row_values in enumerate(table_data):
        row = table.add_row()
        bg_color = "F8FAFC" if (r_idx % 2 == 1) else "FFFFFF"

        for c_idx, val in enumerate(row_values):
            cell = row.cells[c_idx]
            set_cell_background(cell, bg_color)
            is_bold = (c_idx == 0 or c_idx == 1)
            align = WD_ALIGN_PARAGRAPH.CENTER if (c_idx == 1) else WD_ALIGN_PARAGRAPH.LEFT
            set_cell_content(
                cell, val,
                font_name="Arial",
                font_size=Pt(8.5),
                bold=is_bold,
                align=align,
                color_rgb=(26, 32, 44)
            )

    apply_table_geometry(table, col_widths, total_width_inches=7.0)

    # Note paragraph beneath table
    note_p = doc.add_paragraph()
    note_p.paragraph_format.space_before = Pt(8)
    note_p.paragraph_format.space_after = Pt(0)
    note_run = note_p.add_run("Note: This table is pre-formatted with standard cell margins, repeating headers, and fixed column widths. You can select the entire table in Word, copy it (Ctrl+C), and paste it (Ctrl+V) directly into your PRD document.")
    note_run.font.name = "Arial"
    note_run.font.size = Pt(8.5)
    note_run.font.italic = True
    note_run.font.color.rgb = RGBColor(113, 128, 150)

    # Save to both target locations
    out1 = "smart_programmable_power_supply/STAGE_3_FLYBACK_SUBSYSTEM_TABLE.docx"
    out2 = "STAGE_3_FLYBACK_SUBSYSTEM_TABLE.docx"

    doc.save(out1)
    doc.save(out2)
    print(f"Successfully generated DOCX files:\n1. {out1}\n2. {out2}")

if __name__ == "__main__":
    main()
