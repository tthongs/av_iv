#!/usr/bin/env python3
"""
Sanitizer for HARDWARE_DESIGN_DOCUMENT_HDD.md:
Removes all dollar signs ($ and $$), raw LaTeX markup, and unnecessary slashes/obliques,
converting mathematical and engineering expressions into clean, professional, human-readable text.
"""

import re
import sys
from pathlib import Path

HDD_MD_PATH = Path("/home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/HARDWARE_DESIGN_DOCUMENT_HDD.md")
CLEAN_MD_PATH = Path("/home/tthhongs/build_tthongs/av_iv/smart_programmable_power_supply/HDD_task/HARDWARE_DESIGN_DOCUMENT_HDD_CLEAN.md")

def clean_engineering_text(text: str) -> str:
    # 1. Fix corrupted control characters
    text = text.replace('\a', 'a').replace('\b', 'b').replace('\f', 'f').replace('\r', '')
    
    # 2. Fix tab characters that were unescaped \t
    # When written without raw strings, \text became \x09ext, \times became \x09imes, etc.
    text = re.sub(r'[\t\\]+text\{', r'\\text{', text)
    text = re.sub(r'[\t\\]+times\b', r'\\times', text)
    text = re.sub(r'[\t\\]+theta\b', r'\\theta', text)
    text = re.sub(r'[\t\\]+tau\b', r'\\tau', text)
    text = re.sub(r'[\t\\]+to\b', r'\\to', text)
    text = text.replace('\t', ' ')

    # 3. Handle combined engineering units with \mu and \Omega before stripping tags
    unit_patterns = [
        (r'\\mu\\text\{([A-Za-z]+)\}', r'µ\1'),
        (r'\\mu\s*\\text\{([A-Za-z]+)\}', r'µ\1'),
        (r'\\mu([A-Za-z])', r'µ\1'),
        (r'\\text\{k\}\\Omega', 'kΩ'),
        (r'\\text\{m\}\\Omega', 'mΩ'),
        (r'\\text\{M\}\\Omega', 'MΩ'),
        (r'\\text\{u\}\\Omega', 'µΩ'),
        (r'k\\Omega', 'kΩ'),
        (r'm\\Omega', 'mΩ'),
        (r'M\\Omega', 'MΩ'),
        (r'\\Omega', 'Ω'),
        (r'\^\\circ\\text\{C\}', '°C'),
        (r'\^\\circ\s*C', '°C'),
        (r'\^\\circ', '°'),
        (r'\\circ', '°'),
    ]
    for p, r in unit_patterns:
        text = re.sub(p, r, text)

    # 4. Remove \left and \right delimiters
    text = re.sub(r'\\(?:left|right)\s*([()\[\]|])', r'\1', text)

    # 5. Resolve inner \text{...}, \mathbf{...}, \mathrm{...}, \mathit{...} recursively
    for _ in range(5):
        text = re.sub(r'\\(?:text|mathbf|mathrm|mathit)\{([^{}]+)\}', r'\1', text)
        text = re.sub(r'(?:ext|mathbf|mathrm|mathit)\{([^{}]+)\}', r'\1', text)

    # 6. Convert \frac{A}{B} to (A / B) recursively
    for _ in range(6):
        text = re.sub(r'\\?frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1 / \2)', text)

    # 7. Convert \sqrt{A} to √(A)
    text = re.sub(r'\\sqrt\{([^{}]+)\}', r'√(\1)', text)
    text = re.sub(r'\\sqrt\s*(\d+)', r'√\1', text)

    # 8. Clean subscript and superscript braces
    text = re.sub(r'_\{([^{}]+)\}', r'_\1', text)
    text = re.sub(r'\^\{([^{}]+)\}', r'^\1', text)

    # 9. Mathematical symbols
    math_symbols = [
        (r'\\times', '×'),
        (r'\\cdot', '·'),
        (r'\\approx', '≈'),
        (r'\\le\b', '≤'),
        (r'\\ge\b', '≥'),
        (r'\\pm\b', '±'),
        (r'\\mp\b', '∓'),
        (r'\\ll\b', '<<'),
        (r'\\gg\b', '>>'),
        (r'\\neq\b', '≠'),
        (r'\\equiv\b', '≡'),
        (r'\\Delta\b', 'Δ'),
        (r'\\delta\b', 'δ'),
        (r'\\eta\b', 'η'),
        (r'\\theta\b', 'θ'),
        (r'\\pi\b', 'π'),
        (r'\\tau\b', 'τ'),
        (r'\\phi\b', 'φ'),
        (r'\\alpha\b', 'α'),
        (r'\\beta\b', 'β'),
        (r'\\gamma\b', 'γ'),
        (r'\\lambda\b', 'λ'),
        (r'\\sigma\b', 'σ'),
        (r'\\omega\b', 'ω'),
        (r'\\sum', 'Σ'),
        (r'\\int', '∫'),
        (r'\\,', ' '),
        (r'\\;', ' '),
        (r'\\!', ''),
        (r'\\quad', '  '),
        (r'\\qquad', '    '),
        (r'\\%', '%'),
        (r'\\_', '_'),
        (r'\\&', '&'),
        (r'\\mu\b', 'µ'),
    ]
    for p, r in math_symbols:
        text = re.sub(p, r, text)

    # 10. Remove dollar signs
    text = text.replace('$$', '')
    text = text.replace('$', '')

    # 11. Clean remaining stray backslashes before words
    text = re.sub(r'\\([a-zA-Z]+)', r'\1', text)
    text = text.replace('\\', '')

    # 12. Clean whitespace, double parens, degree signs
    text = text.replace('° C', '°C').replace('^°C', '°C')
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)
    text = re.sub(r'\(\s*\(', '(', text)
    text = re.sub(r'\)\s*\)', ')', text)
    text = re.sub(r'[ ]{2,}', ' ', text)

    return text

def main():
    with open(HDD_MD_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    clean_lines = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            clean_lines.append(line)
            continue
        
        if in_code_block:
            clean_lines.append(line)
        else:
            clean_lines.append(clean_engineering_text(line))

    with open(CLEAN_MD_PATH, "w", encoding="utf-8") as f:
        f.writelines(clean_lines)

    print(f"Cleaned Markdown written to: {CLEAN_MD_PATH}")

if __name__ == "__main__":
    main()
