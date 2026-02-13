#!/usr/bin/env python3
"""
Interactive variable exploration for survey data.

Groups variables by type and shows distributions so the user can decide
how each group should be handled (top 2 box, tertile, quartile, as-is, etc.)

This is designed to be run in the terminal as a guided conversation
with the user. The script outputs structured findings; the agent then presents
them and asks the user for decisions.

Usage:
    explore_variables.py <sav_file> [--output <decisions.json>]

Examples:
    explore_variables.py data/survey.sav
    explore_variables.py data/survey.sav --output outputs/variable_decisions.json
"""

import sys
import json
from pathlib import Path
from collections import OrderedDict

try:
    import pyreadstat
    import pandas as pd
    import numpy as np
except ImportError:
    print("Missing packages. Run: pip install pyreadstat pandas numpy")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent))
from classify_variables import classify_all, LIKERT_INDICATORS, DK_PATTERNS


# ── Heuristics for grouping variables ────────────────────────────────────────

ATTITUDINAL_PATTERNS = [
    "agree", "disagree", "satisfied", "dissatisfied",
    "likely", "unlikely", "important", "trust",
    "confident", "comfortable", "concerned", "worried",
    "interested", "willing", "prefer", "recommend",
    "pleased", "disappointed", "happy", "frustrated"
]

USAGE_PATTERNS = [
    "how often", "how frequently", "how many times",
    "daily", "weekly", "monthly", "yearly",
    "hours per", "minutes per", "times per",
    "use", "usage", "frequency", "how long"
]

BEHAVIORAL_PATTERNS = [
    "have you ever", "did you", "do you currently",
    "purchased", "bought", "tried", "visited",
    "switched", "downloaded", "installed", "subscribed"
]

AWARENESS_PATTERNS = [
    "aware", "heard of", "familiar", "know about",
    "recognize", "seen", "noticed"
]

INTENT_PATTERNS = [
    "plan to", "intend to", "would you", "will you",
    "consider", "thinking about", "likelihood",
    "how likely", "purchase intent"
]


def classify_variable_group(var, label, val_labels):
    """Classify a variable into a thematic group based on its label and value labels."""
    text = f"{label} {' '.join(str(v) for v in val_labels.values())}".lower()

    for pattern in USAGE_PATTERNS:
        if pattern in text:
            return "usage"

    for pattern in BEHAVIORAL_PATTERNS:
        if pattern in text:
            return "behavioral"

    for pattern in AWARENESS_PATTERNS:
        if pattern in text:
            return "awareness"

    for pattern in INTENT_PATTERNS:
        if pattern in text:
            return "intent"

    for pattern in ATTITUDINAL_PATTERNS:
        if pattern in text:
            return "attitudinal"

    return "other"


def get_distribution(df, var, val_labels, max_values=15):
    """Get frequency distribution for a variable."""
    counts = df[var].value_counts(dropna=False).sort_index()
    total = len(df)
    valid = df[var].notna().sum()

    dist = []
    for val, count in counts.items():
        if pd.isna(val):
            label = "(Missing)"
        elif val_labels and val in val_labels:
            label = str(val_labels[val])
        else:
            label = str(val)

        pct = round(count / valid * 100, 1) if valid > 0 and not pd.isna(val) else 0
        dist.append({
            "value": None if pd.isna(val) else (int(val) if isinstance(val, (np.integer,)) else float(val) if isinstance(val, (np.floating,)) else str(val)),
            "label": label,
            "count": int(count),
            "pct": pct
        })

    return {
        "total": int(total),
        "valid": int(valid),
        "missing": int(total - valid),
        "distribution": dist[:max_values]
    }


def suggest_recoding(var_type, group, scale_points, dist):
    """Suggest a recoding approach based on variable type and group."""
    suggestions = []

    if group == "attitudinal" and var_type == "likert":
        suggestions.append({
            "method": "top2box",
            "description": f"Top 2 Box: combine highest 2 scale points → binary (agree/satisfied vs rest)",
            "recommended": True
        })
        suggestions.append({
            "method": "top3box",
            "description": f"Top 3 Box: combine highest 3 scale points → binary",
            "recommended": False
        })
        suggestions.append({
            "method": "as_is",
            "description": "Keep original scale — show all points in banner tables",
            "recommended": False
        })

    elif group == "usage":
        suggestions.append({
            "method": "as_is",
            "description": "Keep original categories (e.g., daily/weekly/monthly)",
            "recommended": True
        })
        suggestions.append({
            "method": "tertile",
            "description": "Split into 3 equal groups: light / medium / heavy users",
            "recommended": False
        })
        suggestions.append({
            "method": "quartile",
            "description": "Split into 4 equal groups: Q1-Q4",
            "recommended": False
        })
        suggestions.append({
            "method": "binary",
            "description": "Split into 2 groups: regular users vs occasional/non-users",
            "recommended": False
        })

    elif group == "behavioral" or group == "awareness":
        suggestions.append({
            "method": "as_is",
            "description": "Keep original (typically yes/no or checklist)",
            "recommended": True
        })

    elif group == "intent" and var_type == "likert":
        suggestions.append({
            "method": "top2box",
            "description": "Top 2 Box: definitely + probably → intent",
            "recommended": True
        })
        suggestions.append({
            "method": "as_is",
            "description": "Keep full scale",
            "recommended": False
        })

    else:
        suggestions.append({
            "method": "as_is",
            "description": "Keep as-is (no recoding)",
            "recommended": True
        })

    return suggestions


def explore(sav_path):
    """Main exploration: group variables, show distributions, suggest recoding."""
    df, meta = pyreadstat.read_sav(str(sav_path))

    # Classify all variables
    results = classify_all(sav_path)

    # Group variables thematically
    groups = OrderedDict()
    banner_candidates = []
    id_vars = []

    for i, var in enumerate(meta.column_names):
        label = meta.column_labels[i] if meta.column_labels and i < len(meta.column_labels) else ""
        val_labels = meta.variable_value_labels.get(var, {})
        var_class = next((c for c in results["classifications"] if c["variable"] == var), None)
        var_type = var_class["type"] if var_class else "other"
        scale_points = var_class["scale_points"] if var_class else 0

        # Banner candidates go in their own group
        if var_class and var_class.get("is_banner_candidate"):
            banner_candidates.append({
                "variable": var,
                "label": str(label),
                "type": var_type,
                "n_values": int(df[var].nunique()),
                "distribution": get_distribution(df, var, val_labels)
            })
            continue

        # Skip ID / weight variables
        if var_type in ("continuous", "other") and not val_labels:
            id_vars.append(var)
            continue

        # Group by theme
        group = classify_variable_group(var, label, val_labels)
        if group not in groups:
            groups[group] = []

        dist = get_distribution(df, var, val_labels)
        suggestions = suggest_recoding(var_type, group, scale_points, dist)

        # Detect DK codes
        dk_codes = {}
        for code, lbl in val_labels.items():
            if any(p in str(lbl).lower() for p in DK_PATTERNS):
                dk_codes[code] = str(lbl)

        groups[group].append({
            "variable": var,
            "label": str(label),
            "type": var_type,
            "scale_points": scale_points,
            "group": group,
            "dk_codes": dk_codes,
            "distribution": dist,
            "suggestions": suggestions
        })

    return {
        "file": str(sav_path),
        "n_respondents": int(meta.number_rows),
        "n_variables": int(meta.number_columns),
        "groups": groups,
        "banner_candidates": banner_candidates,
        "id_vars": id_vars
    }


def print_exploration(results):
    """Print formatted exploration output for terminal display."""
    print(f"\n{'='*70}")
    print(f"VARIABLE EXPLORATION: {results['file']}")
    print(f"{results['n_respondents']} respondents | {results['n_variables']} variables")
    print(f"{'='*70}")

    # Banner candidates
    if results["banner_candidates"]:
        print(f"\n{'─'*70}")
        print(f"📊 BANNER CANDIDATES (demographics / segments)")
        print(f"{'─'*70}")
        for bc in results["banner_candidates"]:
            print(f"\n  {bc['variable']} — {bc['label'][:60]}")
            for d in bc["distribution"]["distribution"][:8]:
                if d["label"] != "(Missing)":
                    bar = "█" * int(d["pct"] / 3)
                    print(f"    {d['label']:30s} {d['pct']:5.1f}%  {bar}  (n={d['count']})")

    # Variable groups
    GROUP_LABELS = {
        "attitudinal": "💭 ATTITUDINAL STATEMENTS (agreement, satisfaction, attitudes)",
        "usage": "📱 USAGE / FREQUENCY QUESTIONS",
        "behavioral": "✅ BEHAVIORAL QUESTIONS (actions, experience)",
        "awareness": "👁 AWARENESS QUESTIONS",
        "intent": "🎯 INTENT / LIKELIHOOD QUESTIONS",
        "other": "📋 OTHER VARIABLES"
    }

    for group, variables in results["groups"].items():
        print(f"\n{'─'*70}")
        print(f"{GROUP_LABELS.get(group, group.upper())} ({len(variables)} variables)")
        print(f"{'─'*70}")

        for v in variables[:5]:  # Show first 5 in detail
            print(f"\n  {v['variable']} — {v['label'][:65]}")
            if v['type'] == 'likert':
                print(f"  Scale: {v['scale_points']}-point")

            # Show distribution
            for d in v["distribution"]["distribution"][:7]:
                if d["label"] != "(Missing)":
                    bar = "█" * int(d["pct"] / 3)
                    print(f"    {d['label']:35s} {d['pct']:5.1f}%  {bar}")

            if v["dk_codes"]:
                dk_str = ", ".join(f"{k}='{v2}'" for k, v2 in v["dk_codes"].items())
                print(f"    ⚠ Don't know codes: {dk_str}")

        if len(variables) > 5:
            remaining = [v["variable"] for v in variables[5:]]
            print(f"\n  ... and {len(remaining)} more: {', '.join(remaining[:8])}")
            if len(remaining) > 8:
                print(f"      + {len(remaining) - 8} additional")

        # Recoding suggestions
        if variables:
            print(f"\n  SUGGESTED RECODING:")
            sample = variables[0]
            for s in sample["suggestions"]:
                marker = "→" if s["recommended"] else " "
                print(f"    {marker} {s['method']:12s} — {s['description']}")

    if results["id_vars"]:
        print(f"\n{'─'*70}")
        print(f"🔢 ID / WEIGHT / CONTINUOUS VARIABLES (skipped): {', '.join(results['id_vars'][:10])}")

    print(f"\n{'='*70}")
    print("DECISIONS NEEDED:")
    for group, variables in results["groups"].items():
        if variables:
            print(f"  • {group.upper()} ({len(variables)} vars): How should these be recoded?")
    print(f"{'='*70}\n")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    sav_path = Path(sys.argv[1])
    output_path = None

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = Path(sys.argv[idx + 1])

    if not sav_path.exists():
        print(f"File not found: {sav_path}")
        sys.exit(1)

    results = explore(sav_path)
    print_exploration(results)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Clean for JSON serialization
        clean = json.loads(json.dumps(results, default=str))
        with open(output_path, "w") as f:
            json.dump(clean, f, indent=2, ensure_ascii=False)
        print(f"Exploration saved to: {output_path}")


if __name__ == "__main__":
    main()
