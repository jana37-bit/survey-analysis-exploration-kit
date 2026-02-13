#!/usr/bin/env python3
"""
Recode SPSS variables: handle don't knows and create top-N-box binaries.

Produces a new .sav file with original + recoded variables, all metadata preserved.

Usage:
    recode_variables.py <input.sav> <output.sav> [options]

Options:
    --scheme top2|top3|bottom2    Recoding scheme (default: top2)
    --vars Q1,Q2,Q3              Specific variables to recode (default: auto-detect Likert)
    --metadata <output.json>     Save recoding documentation

Examples:
    recode_variables.py data/survey.sav outputs/survey_recoded.sav
    recode_variables.py data/survey.sav outputs/survey_recoded.sav --scheme top3
    recode_variables.py data/survey.sav outputs/survey_recoded.sav --vars Q1,Q2,Q3 --metadata outputs/metadata.json
"""

import sys
import json
from pathlib import Path

try:
    import pyreadstat
    import pandas as pd
    import numpy as np
except ImportError:
    print("Missing packages. Run: pip install pyreadstat pandas numpy")
    sys.exit(1)

# Import classify logic
sys.path.insert(0, str(Path(__file__).parent))
from classify_variables import classify_all, DK_PATTERNS


def find_dk_codes(meta):
    """Scan value labels for don't know / refused codes."""
    dk_codes = {}
    for var in meta.column_names:
        val_labels = meta.variable_value_labels.get(var, {})
        var_dk = {}
        for code, label in val_labels.items():
            label_lower = str(label).lower().strip()
            if any(p in label_lower for p in DK_PATTERNS):
                var_dk[code] = str(label)
        if var_dk:
            dk_codes[var] = var_dk
    return dk_codes


def recode_dont_knows(df, dk_codes):
    """Replace don't know codes with NaN."""
    df_clean = df.copy()
    recoded_count = 0
    for var, codes in dk_codes.items():
        if var in df_clean.columns:
            for code in codes.keys():
                mask = df_clean[var] == code
                recoded_count += mask.sum()
                df_clean.loc[mask, var] = np.nan
    return df_clean, recoded_count


def recode_likert(df, meta, likert_vars, scheme="top2"):
    """
    Recode Likert scales to binary top/bottom box.

    Schemes:
        top2: Highest 2 values → 1, rest → 0
        top3: Highest 3 values → 1, rest → 0
        bottom2: Lowest 2 values → 1, rest → 0
    """
    n_box = int(scheme.replace("top", "").replace("bottom", ""))
    is_bottom = scheme.startswith("bottom")

    df_out = df.copy()
    new_labels = {}
    new_value_labels = {}
    suffix = f"_{scheme}"
    recoding_doc = []

    for var in likert_vars:
        val_labels = meta.variable_value_labels.get(var, {})

        # Get scale values (exclude DK codes already removed as NaN)
        if val_labels:
            scale_values = sorted([k for k in val_labels.keys()
                                   if isinstance(k, (int, float, np.integer, np.floating))
                                   and not any(p in str(val_labels.get(k, "")).lower() for p in DK_PATTERNS)])
        else:
            valid = df[var].dropna().unique()
            scale_values = sorted([v for v in valid if isinstance(v, (int, float, np.integer, np.floating))])

        if len(scale_values) < 3:
            continue

        if is_bottom:
            threshold_values = scale_values[:n_box]
        else:
            threshold_values = scale_values[-n_box:]

        new_var = f"{var}{suffix}"
        df_out[new_var] = np.where(
            df_out[var].isna(),
            np.nan,
            np.where(df_out[var].isin(threshold_values), 1, 0)
        )

        # Transfer label
        idx = list(meta.column_names).index(var)
        orig_label = meta.column_labels[idx] if meta.column_labels and idx < len(meta.column_labels) else var
        box_label = f"Top {n_box} Box" if not is_bottom else f"Bottom {n_box} Box"
        new_labels[new_var] = f"{orig_label} [{box_label}]"
        new_value_labels[new_var] = {0: "Bottom box", 1: box_label}

        # Document
        threshold_labels = [str(val_labels.get(v, v)) for v in threshold_values]
        recoding_doc.append({
            "original": var,
            "recoded": new_var,
            "scheme": scheme,
            "scale_points": len(scale_values),
            "threshold_values": [float(v) for v in threshold_values],
            "threshold_labels": threshold_labels,
            "original_label": str(orig_label),
            "recoded_label": new_labels[new_var]
        })

    return df_out, new_labels, new_value_labels, recoding_doc


def save_recoded_sav(df, meta, new_labels, new_value_labels, output_path):
    """Save recoded DataFrame as SPSS file with complete metadata."""
    all_col_labels = []
    for col in df.columns:
        if col in new_labels:
            all_col_labels.append(new_labels[col])
        elif col in meta.column_names:
            idx = list(meta.column_names).index(col)
            lbl = meta.column_labels[idx] if meta.column_labels and idx < len(meta.column_labels) else ""
            all_col_labels.append(str(lbl))
        else:
            all_col_labels.append("")

    all_val_labels = {}
    for col in df.columns:
        if col in new_value_labels:
            all_val_labels[col] = new_value_labels[col]
        elif col in meta.variable_value_labels:
            all_val_labels[col] = meta.variable_value_labels[col]

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pyreadstat.write_sav(
        df, str(output_path),
        column_labels=all_col_labels,
        variable_value_labels=all_val_labels
    )


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    scheme = "top2"
    specific_vars = None
    metadata_path = None

    args = sys.argv[3:]
    i = 0
    while i < len(args):
        if args[i] == "--scheme" and i + 1 < len(args):
            scheme = args[i + 1]
            i += 2
        elif args[i] == "--vars" and i + 1 < len(args):
            specific_vars = [v.strip() for v in args[i + 1].split(",")]
            i += 2
        elif args[i] == "--metadata" and i + 1 < len(args):
            metadata_path = Path(args[i + 1])
            i += 2
        else:
            i += 1

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    print(f"Loading {input_path}...")
    df, meta = pyreadstat.read_sav(str(input_path))
    print(f"  {meta.number_rows} respondents, {meta.number_columns} variables")

    # Find don't know codes
    dk_codes = find_dk_codes(meta)
    if dk_codes:
        print(f"\nHandling don't knows in {len(dk_codes)} variables...")
        df, dk_count = recode_dont_knows(df, dk_codes)
        print(f"  Replaced {dk_count} don't know values with missing")

    # Identify Likert variables
    if specific_vars:
        likert_vars = specific_vars
    else:
        results = classify_all(input_path)
        likert_vars = results["summary"]["likert"]

    print(f"\nRecoding {len(likert_vars)} Likert variables with scheme: {scheme}")

    # Recode
    df_recoded, new_labels, new_value_labels, doc = recode_likert(
        df, meta, likert_vars, scheme
    )

    recoded_count = len([d for d in doc])
    print(f"  Created {recoded_count} recoded variables")

    # Save
    print(f"\nSaving to {output_path}...")
    save_recoded_sav(df_recoded, meta, new_labels, new_value_labels, output_path)
    print(f"  {len(df_recoded.columns)} total columns ({meta.number_columns} original + {recoded_count} recoded)")

    # Save metadata
    if metadata_path:
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        metadata = {
            "source_file": str(input_path),
            "output_file": str(output_path),
            "scheme": scheme,
            "dk_codes_found": {k: v for k, v in dk_codes.items()},
            "recodings": doc,
            "n_original_vars": int(meta.number_columns),
            "n_total_vars": len(df_recoded.columns),
            "n_respondents": int(meta.number_rows)
        }
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2, default=str)
        print(f"  Metadata saved to {metadata_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
