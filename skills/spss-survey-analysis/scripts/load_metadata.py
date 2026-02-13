#!/usr/bin/env python3
"""
Load SPSS file and extract complete metadata.

Usage:
    load_metadata.py <sav_file> [--output <json_file>]

Examples:
    load_metadata.py data/survey.sav
    load_metadata.py data/survey.sav --output outputs/metadata.json
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


def load_metadata(sav_path):
    """Load SPSS file and return structured metadata dict."""
    df, meta = pyreadstat.read_sav(str(sav_path))

    metadata = {
        "file": str(sav_path),
        "n_respondents": int(meta.number_rows),
        "n_variables": int(meta.number_columns),
        "variables": {}
    }

    for i, var in enumerate(meta.column_names):
        label = meta.column_labels[i] if meta.column_labels and i < len(meta.column_labels) else ""
        val_labels = meta.variable_value_labels.get(var, {})

        # Convert numpy types for JSON serialization
        clean_val_labels = {}
        for k, v in val_labels.items():
            key = int(k) if isinstance(k, (np.integer, float)) else str(k)
            clean_val_labels[key] = str(v)

        sample_vals = df[var].dropna().unique()[:10]
        clean_samples = [int(v) if isinstance(v, (np.integer,)) else
                         float(v) if isinstance(v, (np.floating,)) else
                         str(v) for v in sample_vals]

        metadata["variables"][var] = {
            "label": str(label),
            "value_labels": clean_val_labels,
            "dtype": str(df[var].dtype),
            "n_unique": int(df[var].nunique()),
            "n_missing": int(df[var].isna().sum()),
            "sample_values": clean_samples
        }

    return df, meta, metadata


def print_summary(metadata):
    """Print human-readable summary."""
    print(f"\n{'='*60}")
    print(f"SPSS File: {metadata['file']}")
    print(f"Respondents: {metadata['n_respondents']}")
    print(f"Variables: {metadata['n_variables']}")
    print(f"{'='*60}\n")

    for var, info in metadata["variables"].items():
        print(f"  {var}")
        if info["label"]:
            print(f"    Label: {info['label']}")
        if info["value_labels"]:
            labels_str = ", ".join(f"{k}={v}" for k, v in list(info["value_labels"].items())[:8])
            if len(info["value_labels"]) > 8:
                labels_str += f" ... (+{len(info['value_labels'])-8} more)"
            print(f"    Values: {labels_str}")
        print(f"    Unique: {info['n_unique']} | Missing: {info['n_missing']} | Type: {info['dtype']}")
        print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    sav_path = Path(sys.argv[1])
    if not sav_path.exists():
        print(f"File not found: {sav_path}")
        sys.exit(1)

    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = Path(sys.argv[idx + 1])

    df, meta, metadata = load_metadata(sav_path)
    print_summary(metadata)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"Metadata saved to: {output_path}")


if __name__ == "__main__":
    main()
