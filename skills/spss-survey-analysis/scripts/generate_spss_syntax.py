#!/usr/bin/env python3
"""
Generate SPSS Custom Tables syntax for QA verification.

Usage:
    generate_spss_syntax.py --vars VAR1,VAR2 --banners BAN1,BAN2 --output <file.sps>

Options:
    --vars VAR1,VAR2          Row variables (comma-separated)
    --banners BAN1,BAN2       Banner variables (comma-separated)
    --recoded VAR_top2,...     Recoded variables (auto-detected if not specified)
    --output <file.sps>       Output path (default: outputs/spss_custom_tables_syntax.sps)

Examples:
    generate_spss_syntax.py --vars Q1,Q2,Q3 --banners Country,Age,Gender --output outputs/syntax.sps
"""

import sys
from pathlib import Path
from datetime import datetime


def generate_syntax(row_vars, banner_vars, recoded_vars=None, title="Survey Analysis"):
    """Generate SPSS CTABLES syntax."""
    recoded_vars = recoded_vars or []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"* ============================================.",
        f"* SPSS Custom Tables Syntax",
        f"* Generated: {now}",
        f"* Title: {title}",
        f"* ============================================.",
        "",
        f"* Banner variables: {', '.join(banner_vars)}.",
        f"* Row variables: {', '.join(row_vars)}.",
        "",
    ]

    # Original variables
    original_vars = [v for v in row_vars if v not in recoded_vars]
    if original_vars:
        lines.append("* --- Original Variables (All Scale Points) ---.")
        lines.append("")

        for var in original_vars:
            lines.append(f"CTABLES")
            lines.append(f"  /TABLE {var} [C][COUNT F40.0, COLPCT.COUNT PCT40.5]")
            lines.append(f"    BY {' + '.join(banner_vars)} [C]")
            lines.append(f"  /CATEGORIES VARIABLES={var} ORDER=A KEY=VALUE EMPTY=INCLUDE")
            for bv in banner_vars:
                lines.append(f"  /CATEGORIES VARIABLES={bv} ORDER=A KEY=VALUE EMPTY=INCLUDE")
            lines.append(".")
            lines.append("")

    # Recoded variables
    if recoded_vars:
        lines.append("* --- Recoded Variables (Top/Bottom Box) ---.")
        lines.append("")

        for var in recoded_vars:
            lines.append(f"CTABLES")
            lines.append(f"  /TABLE {var} [C][COUNT F40.0, COLPCT.COUNT PCT40.5]")
            lines.append(f"    BY {' + '.join(banner_vars)} [C]")
            lines.append(f"  /CATEGORIES VARIABLES={var} ORDER=A KEY=VALUE EMPTY=INCLUDE")
            for bv in banner_vars:
                lines.append(f"  /CATEGORIES VARIABLES={bv} ORDER=A KEY=VALUE EMPTY=INCLUDE")
            lines.append(".")
            lines.append("")

    lines.append("* ============================================.")
    lines.append("* END OF SYNTAX")
    lines.append("* ============================================.")

    return "\n".join(lines)


def main():
    row_vars = []
    banner_vars = []
    recoded_vars = []
    output_path = Path("outputs/spss_custom_tables_syntax.sps")

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--vars" and i + 1 < len(args):
            row_vars = [v.strip() for v in args[i + 1].split(",")]
            i += 2
        elif args[i] == "--banners" and i + 1 < len(args):
            banner_vars = [v.strip() for v in args[i + 1].split(",")]
            i += 2
        elif args[i] == "--recoded" and i + 1 < len(args):
            recoded_vars = [v.strip() for v in args[i + 1].split(",")]
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_path = Path(args[i + 1])
            i += 2
        else:
            i += 1

    if not row_vars or not banner_vars:
        print(__doc__)
        sys.exit(1)

    syntax = generate_syntax(row_vars, banner_vars, recoded_vars)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(syntax)

    print(f"SPSS syntax saved to: {output_path}")
    print(f"  {len(row_vars)} row variables, {len(banner_vars)} banner variables")
    if recoded_vars:
        print(f"  {len(recoded_vars)} recoded variables included")


if __name__ == "__main__":
    main()
