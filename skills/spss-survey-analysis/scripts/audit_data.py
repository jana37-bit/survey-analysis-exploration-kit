#!/usr/bin/env python3
"""
Audit SPSS data before generating banner tables.

This is the intermediate step between recoding and table generation.
It verifies what was created and gives the user a chance to catch
issues before the final output is built.

Usage:
    audit_data.py <recoded.sav> [--banners VAR1,VAR2]

Output:
    Prints a comprehensive summary of what's in the file and what
    the banner tables will contain.

Examples:
    audit_data.py outputs/survey_recoded.sav
    audit_data.py outputs/survey_recoded.sav --banners Country,Gender,Age
"""

import sys
from pathlib import Path

try:
    import pyreadstat
    import pandas as pd
    import numpy as np
except ImportError:
    print("Missing packages. Run: pip install pyreadstat pandas numpy")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent))
from classify_variables import classify_all


def audit(sav_path, banner_vars=None):
    df, meta = pyreadstat.read_sav(str(sav_path))

    print(f"\n{'='*70}")
    print(f"DATA AUDIT: {sav_path}")
    print(f"{'='*70}")
    print(f"\nRespondents: {meta.number_rows}")
    print(f"Variables:   {meta.number_columns}")

    # Separate original vs recoded
    recoded = [c for c in df.columns if any(c.endswith(s) for s in ['_top2', '_top3', '_T2B', '_bottom2'])]
    originals = [c for c in df.columns if c not in recoded]

    print(f"\nOriginal variables: {len(originals)}")
    print(f"Recoded variables:  {len(recoded)}")

    # Classify originals
    results = classify_all(sav_path)
    likert = results["summary"]["likert"]
    nominal = results["summary"]["nominal"]
    binary = results["summary"]["binary"]

    print(f"\n--- Variable Types ---")
    print(f"Likert scales:    {len(likert)} → these get full distribution + T2B in tables")
    print(f"Nominal/category: {len(nominal)} → good banner candidates")
    print(f"Binary:           {len(binary)}")

    # Check recoded → original mapping
    print(f"\n--- Recoded Variable Mapping ---")
    orphaned = []
    for rec in recoded:
        # Try to find original
        orig_name = rec
        for suffix in ['_top2', '_top3', '_T2B', '_bottom2']:
            orig_name = orig_name.replace(suffix, '')
        if orig_name in df.columns:
            # Get scale points of original
            val_labels = meta.variable_value_labels.get(orig_name, {})
            n_points = len(val_labels) if val_labels else df[orig_name].nunique()
            print(f"  {rec:30s} ← {orig_name} ({n_points}-point scale)")
        else:
            orphaned.append(rec)
            print(f"  {rec:30s} ← ⚠ ORIGINAL NOT FOUND")

    if orphaned:
        print(f"\n⚠ WARNING: {len(orphaned)} recoded variables have no matching original!")
        print(f"  The banner tables need BOTH original distributions AND T2B.")

    # Banner analysis
    if banner_vars:
        print(f"\n--- Banner Columns Preview ---")
        for bvar in banner_vars:
            if bvar not in df.columns:
                print(f"  ⚠ Banner '{bvar}' NOT FOUND in data!")
                continue
            val_labels = meta.variable_value_labels.get(bvar, {})
            print(f"\n  {bvar}:")
            if val_labels:
                for code in sorted(val_labels.keys()):
                    n = int((df[bvar] == code).sum())
                    pct = round(n / len(df) * 100, 1)
                    flag = " ⚠ EMPTY" if n == 0 else ""
                    print(f"    {val_labels[code]:30s} n={n:>5d} ({pct}%){flag}")
            else:
                for val in sorted(df[bvar].dropna().unique()):
                    n = int((df[bvar] == val).sum())
                    print(f"    {str(val):30s} n={n:>5d}")

    # What banner tables will contain
    row_vars_for_tables = []
    for var in likert:
        row_vars_for_tables.append(('original', var))
        matching_rec = [r for r in recoded if r.startswith(var)]
        for r in matching_rec:
            row_vars_for_tables.append(('recoded', r))

    print(f"\n--- Banner Table Preview ---")
    print(f"Row variables to include: {len(row_vars_for_tables)}")
    print(f"  ({len(likert)} original full distributions + {len([r for _, r in row_vars_for_tables if _ == 'recoded'])} recoded)")
    print()
    for vtype, var in row_vars_for_tables[:20]:
        idx = list(meta.column_names).index(var) if var in meta.column_names else None
        label = meta.column_labels[idx][:60] if idx is not None and meta.column_labels else ""
        tag = "FULL DIST" if vtype == 'original' else "T2B"
        print(f"  [{tag:9s}] {var:30s} {label}")
    if len(row_vars_for_tables) > 20:
        print(f"  ... and {len(row_vars_for_tables) - 20} more")

    print(f"\n{'='*70}")
    print("Review the above. If everything looks correct, proceed to:")
    print(f"  python scripts/create_banner_tables.py {sav_path} outputs/banner_tables.xlsx")
    print(f"{'='*70}\n")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    sav_path = Path(sys.argv[1])
    banner_vars = None

    if "--banners" in sys.argv:
        idx = sys.argv.index("--banners")
        if idx + 1 < len(sys.argv):
            banner_vars = [v.strip() for v in sys.argv[idx + 1].split(",")]

    if not sav_path.exists():
        print(f"File not found: {sav_path}")
        sys.exit(1)

    audit(sav_path, banner_vars)


if __name__ == "__main__":
    main()
