#!/usr/bin/env python3
"""
Create chart images for embedding in PowerPoint slides.

Usage:
    create_chart.py <type> <data.json> <output.png> [options]

Chart types:
    horizontal_bar    Horizontal bar chart (default for survey data)
    grouped_bar       Grouped horizontal bars (comparing across groups)
    stacked_bar       Stacked horizontal bars (showing full distribution)

Options:
    --title "Chart Title"
    --highlight VALUE       Highlight bars above this threshold
    --colors primary,accent Custom color scheme

Examples:
    create_chart.py horizontal_bar data.json chart.png --title "Satisfaction (Top 2 Box %)"
    create_chart.py grouped_bar data.json chart.png --title "By Region"
"""

import sys
import json
from pathlib import Path

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Missing packages. Run: pip install matplotlib numpy")
    sys.exit(1)

# Standard color palette
COLORS = {
    'primary': '#2F5496',
    'secondary': '#4472C4',
    'accent': '#ED7D31',
    'gray': '#A5A5A5',
    'gold': '#FFC000',
    'text': '#333333',
    'title': '#2F5496',
}

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Calibri', 'Arial', 'Helvetica'],
    'font.size': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.facecolor': 'white',
})


def horizontal_bar(data, output_path, title="", highlight_threshold=50):
    """
    Standard horizontal bar chart.

    data format:
    {
        "labels": ["Label 1", "Label 2", ...],
        "values": [45.2, 67.8, ...],
        "base": 500
    }
    """
    labels = data["labels"]
    values = data["values"]
    base = data.get("base", "")

    fig_height = max(3, len(labels) * 0.55 + 1.5)
    fig, ax = plt.subplots(figsize=(9, fig_height))

    colors = [COLORS['accent'] if v >= highlight_threshold else COLORS['primary'] for v in values]
    bars = ax.barh(range(len(labels)), values, color=colors, height=0.6)

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=10, color=COLORS['text'])
    ax.invert_yaxis()

    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2,
                f'{val:.1f}%', va='center', fontsize=10, color=COLORS['text'])

    ax.set_xlim(0, max(values) * 1.15 if values else 100)
    ax.set_xlabel('%', fontsize=10, color=COLORS['text'])

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', color=COLORS['title'], pad=15, loc='left')

    if base:
        ax.text(0, 1.02, f'Base: n={base}', transform=ax.transAxes,
                fontsize=9, color='#999999', fontstyle='italic')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()


def grouped_bar(data, output_path, title=""):
    """
    Grouped horizontal bar chart for comparing across groups.

    data format:
    {
        "labels": ["Q1", "Q2", ...],
        "groups": {
            "Group A": [45.2, 67.8, ...],
            "Group B": [38.1, 72.3, ...]
        },
        "base": {"Group A": 250, "Group B": 250}
    }
    """
    labels = data["labels"]
    groups = data["groups"]
    group_names = list(groups.keys())
    n_groups = len(group_names)
    n_labels = len(labels)

    fig_height = max(4, n_labels * 0.7 * n_groups / 2 + 2)
    fig, ax = plt.subplots(figsize=(10, fig_height))

    bar_height = 0.8 / n_groups
    group_colors = [COLORS['primary'], COLORS['accent'], COLORS['secondary'], COLORS['gray']]

    for i, (name, values) in enumerate(groups.items()):
        positions = [y + i * bar_height for y in range(n_labels)]
        color = group_colors[i % len(group_colors)]
        bars = ax.barh(positions, values, height=bar_height, label=name, color=color)

        for bar, val in zip(bars, values):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                    f'{val:.1f}%', va='center', fontsize=9, color=COLORS['text'])

    ax.set_yticks([y + bar_height * (n_groups - 1) / 2 for y in range(n_labels)])
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.legend(loc='lower right', fontsize=9)

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', color=COLORS['title'], pad=15, loc='left')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    chart_type = sys.argv[1]
    data_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    title = ""
    highlight = 50
    args = sys.argv[4:]
    i = 0
    while i < len(args):
        if args[i] == "--title" and i + 1 < len(args):
            title = args[i + 1]
            i += 2
        elif args[i] == "--highlight" and i + 1 < len(args):
            highlight = float(args[i + 1])
            i += 2
        else:
            i += 1

    with open(data_path) as f:
        data = json.load(f)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if chart_type == "horizontal_bar":
        horizontal_bar(data, str(output_path), title, highlight)
    elif chart_type == "grouped_bar":
        grouped_bar(data, str(output_path), title)
    else:
        print(f"Unknown chart type: {chart_type}")
        sys.exit(1)

    print(f"Chart saved: {output_path}")


if __name__ == "__main__":
    main()
