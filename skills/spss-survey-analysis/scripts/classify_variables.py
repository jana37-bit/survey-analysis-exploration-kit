#!/usr/bin/env python3
"""
Classify SPSS variables into types: likert, nominal, binary, other.
Also detects don't know / refused codes from value labels.

Usage:
    classify_variables.py <sav_file> [--output <json_file>]

Examples:
    classify_variables.py data/survey.sav
    classify_variables.py data/survey.sav --output outputs/classifications.json
"""

import sys
import json
from pathlib import Path

try:
    import pyreadstat
    import numpy as np
except ImportError:
    print("Missing packages. Run: pip install pyreadstat numpy")
    sys.exit(1)


LIKERT_INDICATORS = [
    "agree", "disagree", "satisfied", "dissatisfied",
    "likely", "unlikely", "important", "unimportant",
    "good", "poor", "excellent", "fair",
    "always", "never", "often", "rarely",
    "very", "somewhat", "not at all", "extremely",
    "strongly", "completely", "definitely", "probably"
]

DK_PATTERNS = [
    "don't know", "dont know", "don\u2019t know", "dk",
    "not sure", "unsure", "can't say", "no opinion",
    "refused", "prefer not", "decline",
    "not applicable", "n/a"
]


def classify_variable(var, df, meta):
    """Classify a single variable."""
    val_labels = meta.variable_value_labels.get(var, {})
    n_unique = int(df[var].nunique())

    # Detect don't know codes
    dk_codes = {}
    for code, label in val_labels.items():
        label_lower = str(label).lower().strip()
        if any(pattern in label_lower for pattern in DK_PATTERNS):
            dk_codes[code] = str(label)

    # Count scale values (excluding don't know codes)
    scale_labels = {k: v for k, v in val_labels.items() if k not in dk_codes}
    n_scale_values = len(scale_labels)

    # Check if Likert
    is_likert = False
    scale_points = 0

    if scale_labels and 3 <= n_scale_values <= 11:
        label_text = " ".join(str(v).lower() for v in scale_labels.values())
        is_likert = any(ind in label_text for ind in LIKERT_INDICATORS)

        if not is_likert:
            numeric_keys = sorted([k for k in scale_labels.keys()
                                   if isinstance(k, (int, float, np.integer, np.floating))])
            if len(numeric_keys) >= 3:
                diffs = [numeric_keys[i+1] - numeric_keys[i] for i in range(len(numeric_keys)-1)]
                if all(d == 1 for d in diffs):
                    is_likert = True

        if is_likert:
            scale_points = n_scale_values

    # Classify
    if is_likert:
        var_type = "likert"
    elif n_unique <= 2:
        var_type = "binary"
    elif n_unique <= 20 and val_labels:
        var_type = "nominal"
    elif n_unique > 20:
        var_type = "continuous"
    else:
        var_type = "other"

    idx = list(meta.column_names).index(var)
    label = meta.column_labels[idx] if meta.column_labels and idx < len(meta.column_labels) else ""

    return {
        "variable": var,
        "label": str(label),
        "type": var_type,
        "scale_points": scale_points,
        "n_unique": n_unique,
        "dk_codes": dk_codes,
        "is_banner_candidate": var_type in ("nominal", "binary") and not dk_codes
    }


def classify_all(sav_path):
    """Classify all variables in an SPSS file."""
    df, meta = pyreadstat.read_sav(str(sav_path))

    results = {
        "file": str(sav_path),
        "classifications": [],
        "summary": {
            "likert": [],
            "nominal": [],
            "binary": [],
            "continuous": [],
            "other": [],
            "banner_candidates": [],
            "vars_with_dk": []
        }
    }

    for var in meta.column_names:
        info = classify_variable(var, df, meta)
        results["classifications"].append(info)

        results["summary"][info["type"]].append(var)
        if info["is_banner_candidate"]:
            results["summary"]["banner_candidates"].append(var)
        if info["dk_codes"]:
            results["summary"]["vars_with_dk"].append({
                "variable": var,
                "codes": info["dk_codes"]
            })

    return results


def print_summary(results):
    """Print classification summary."""
    s = results["summary"]

    print(f"\n{'='*60}")
    print("VARIABLE CLASSIFICATION SUMMARY")
    print(f"{'='*60}\n")

    if s["likert"]:
        print(f"LIKERT SCALES ({len(s['likert'])} variables):")
        for c in results["classifications"]:
            if c["type"] == "likert":
                print(f"  {c['variable']:20s} ({c['scale_points']}-point) {c['label'][:50]}")
        print()

    if s["banner_candidates"]:
        print(f"BANNER CANDIDATES ({len(s['banner_candidates'])} variables):")
        for c in results["classifications"]:
            if c["is_banner_candidate"]:
                print(f"  {c['variable']:20s} ({c['n_unique']} values) {c['label'][:50]}")
        print()

    if s["vars_with_dk"]:
        print(f"DON'T KNOW CODES DETECTED ({len(s['vars_with_dk'])} variables):")
        for dk in s["vars_with_dk"]:
            codes_str = ", ".join(f"{k}='{v}'" for k, v in dk["codes"].items())
            print(f"  {dk['variable']:20s} → {codes_str}")
        print()

    other_types = ["nominal", "binary", "continuous", "other"]
    for t in other_types:
        if s[t] and t != "nominal":
            print(f"{t.upper()} ({len(s[t])}): {', '.join(s[t][:10])}")
            if len(s[t]) > 10:
                print(f"  ... and {len(s[t])-10} more")

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

    results = classify_all(sav_path)
    print_summary(results)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Convert numpy types for JSON
        clean = json.loads(json.dumps(results, default=str))
        with open(output_path, "w") as f:
            json.dump(clean, f, indent=2, ensure_ascii=False)
        print(f"Classifications saved to: {output_path}")


if __name__ == "__main__":
    main()
