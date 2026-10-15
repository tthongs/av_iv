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
    run_title = title_p.add_run("Stage 3: Converter DC-DC (Isolated Flyback) Subsystem")
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
            "Quasi-Resonant Controller",
            "U1",
            "Texas Instruments UCC28740DR (SOIC-7)",
            "Valley-switching detector, aux ZCD, optical FB pin, cycle-by-cycle CS",
            "Modulates switching frequency (up to 80 kHz) to turn on primary MOSFET at drain voltage resonance minimums, slashing turn-on capacitive losses by > 60%."
        ),
        (
            "Primary Power Switch",
            "Q1",
            "Infineon IPB80R290P7 (CoolMOS P7, D2PAK)",
            "800 V, 17 A, R_DS(on) = 0.29 Ω, V_DS,peak = 599 V",
            "Low-loss primary switching element. Derated to 74.9% of breakdown voltage rating (strictly < 75% limit). Conduction loss <= 0.57 W."
        ),
        (
            "Primary Current Sensing",
            "R_CS",
            "Precision Sense Resistor Network",
            "Low-inductance metal foil, 0.25 Ω, 1%, 1 W",
            "Senses primary switch peak current (I_pk = 2.96 A) on UCC28740 CS pin for cycle-by-cycle overcurrent protection (OCP)."
        ),
        (
            "RCD Snubber Clamp",
            "D_snub\nR_snub\nC_snub",
            "Diodes Inc. US1M +\n3x 68 kΩ in parallel (22.6 kΩ, 3W) +\n1.0 nF / 1 kV Ceramic",
            "Diode: 1000 V, 1 A, t_rr = 75 ns;\nCap: 1 nF / 1000 V ceramic;\nClamp: ~216 V clamp level",
            "Absorbs transformer primary leakage inductance energy (L_lk approx 2.2 uH); clamps peak drain-source voltage spike safely below 650 V peak."
        ),
        (
            "Flyback Power Transformer",
            "TX1",
            "Ferroxcube PQ26/20 (3C95 Ferrite Core) / Custom",
            "L_p = 220 uH +/- 10%, B_max = 0.148 T (B_sat = 0.38 T), N_p = 36 T",
            "Primary energy storage inductor (72 W throughput, I_pk = 2.96 A, low core loss, air gap l_g = 0.52 mm)."
        ),
        (
            "Auxiliary Bias & Demag Winding",
            "TX1_AUX",
            "N_aux = 4 T (0.25 mm wire) +\nUltra-fast diode & 10 uF MLCC",
            "Output: +14.0 V DC bias rail",
            "Self-powers UCC28740 VCC pin after initial high-voltage startup and provides Zero Crossing Detection (ZCD) for core demagnetization timing."
        ),
        (
            "Galvanic Safety Isolation Barrier",
            "TX1_ISO",
            "Furukawa TEX-E Triple-Insulated Wire (TIW)",
            "N_s = 6 T (N_p:N_s = 6:1), Reinforced insulation, >= 6.4 mm creepage",
            "Conforms to IEC 62368-1 safety standards. Provides certified >= 3000 V RMS dielectric withstand between primary hot and secondary touch-safe SELV domains."
        ),
        (
            "Smart Synchronous Rectifier Driver",
            "U2",
            "Monolithic Power Systems MP6908GJ (TSOT23-6)",
            "Fast turn-off (35 ns gate fall), V_DS drain-sense detection",
            "Autonomous gate driver for secondary sync switch; eliminates external sync timing coils and prevents shoot-through during DCM/QR resonant ringing."
        ),
        (
            "Synchronous Rectifier Switch",
            "Q_SR",
            "Infineon BSC052N06NS (OptiMOS 5, SuperSO8)",
            "60 V, R_DS(on) = 5.2 mΩ, I_RMS,sec = 7.61 A",
            "Replaces lossy Schottky diode (V_F = 0.6 V); cuts secondary rectification dissipation from 1.80 W to 0.42 W (saving 1.38 W continuous heat, heatsink-free)."
        ),
        (
            "Secondary LC Output Filter",
            "C_sec\nL_sec",
            "Panasonic OS-CON 470 uF / 35 V Polymer +\n2.2 uH Inductor + 22 uF MLCC",
            "Ultra-low ESR (< 15 mΩ), Delta V_ripple < 50 mV pk-pk",
            "Suppresses high-frequency 80 kHz switching pulses and secondary flyback current spikes to form clean intermediate DC rail."
        ),
        (
            "Isolated Closed-Loop Feedback",
            "OPTO1\nU3",
            "Everlight EL817(S)(TA) Optocoupler +\nTI TL431AIDBZR Shunt Regulator",
            "5000 V RMS optical isolation, 2.495 V internal bandgap, 0.5%",
            "Secondary-side precision voltage divider senses the +24.0 V rail and transfers feedback error signal across isolation barrier to UCC28740 FB node."
        ),
        (
            "Intermediate Rail Output",
            "+24V_BUS",
            "Intermediate DC Power Distribution Bus",
            "+24.0 V DC +/- 1.0%, 72.0 W continuous (3.0 A), 84 W peak",
            "Delivers stable intermediate regulated power to Stage 4 (Synchronous Buck-Boost Post-Regulator) and secondary auxiliary housekeeping LDOs."
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
