---
name: pptx-survey
description: "PowerPoint presentation generation for survey research results. Use when creating summary decks, research presentations, or data-driven slide outputs from SPSS survey analysis. Handles chart creation, stat callouts, methodology slides, and research-standard formatting. Trigger when user mentions presentation, deck, slides, PowerPoint, .pptx, or summary of findings."
---

# PowerPoint Survey Presentations

Creates professional market research presentations from survey analysis results using python-pptx.

## Quick Reference

| Task | Script |
|------|--------|
| Create chart image for embedding | `scripts/create_chart.py <data.json> <output.png>` |
| Build full presentation | `scripts/build_presentation.py <analysis_results.json> <output.pptx>` |
| Convert slides to images for QA | See QA section below |

## Design Standards

Read `references/design-standards.md` for the complete visual specification. Key rules:

- **16:9 widescreen** (13.333" × 7.5")
- **Color palette**: Deep blue (#2F5496) primary, orange (#ED7D31) accent
- **Typography**: Calibri throughout — 32-36pt titles, 14-16pt body, 9pt source lines
- **Every data slide** must have: title + visual + insight text + base/source line
- **One chart per slide** (unless comparing two related items)
- **Source line** at bottom of every data slide: `Source: [Survey Name], n=X.`

## Slide Deck Structure

1. **Title slide** — Dark blue background, project name, date, sample size
2. **Methodology** — Sample description, fielding dates, key demographics
3. **Executive summary** — 3-5 large stat callouts (60pt numbers with labels)
4. **Section dividers** — One per analysis topic (dark background)
5. **Data slides** — Chart + key insight per variable/topic
6. **Appendix** — Detailed tables, methodology notes

## Creating Charts

Charts are created as PNG images with matplotlib and embedded into slides:

```python
import matplotlib.pyplot as plt
import io

# Create chart → save to buffer → embed in slide
buf = io.BytesIO()
# ... matplotlib chart code ...
plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
buf.seek(0)

# Embed
from pptx.util import Inches
slide.shapes.add_picture(buf, Inches(1), Inches(1.5), Inches(10), Inches(5))
```

Read `references/design-standards.md` for chart styling specifications.

## QA Process

After creating the presentation:

1. Convert to images for visual inspection:
   ```bash
   libreoffice --headless --convert-to pdf output.pptx
   pdftoppm -jpeg -r 150 output.pdf slide
   ```
2. Check every slide for: text overflow, overlapping elements, missing data, wrong numbers
3. Verify chart values match the Excel banner tables
4. Confirm base sizes appear on every data slide
5. Check source lines are present and accurate
