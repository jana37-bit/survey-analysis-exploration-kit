# Presentation Design Standards

Visual specification for survey research PowerPoint outputs.

## Slide Dimensions

- Width: 13.333 inches (16:9 widescreen)
- Height: 7.5 inches
- Margins: 0.5" minimum on all sides

## Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary | Deep blue | #2F5496 | Headers, title backgrounds, chart primary |
| Secondary | Medium blue | #4472C4 | Chart secondary bars, supporting elements |
| Accent | Orange | #ED7D31 | Highlights, significant findings, callout numbers |
| Background | White | #FFFFFF | Default slide background |
| Text | Dark gray | #333333 | Body text |
| Subtitle | Medium gray | #666666 | Subtitles, secondary text |
| Source line | Light gray | #999999 | Source/footnote text |
| Title slide bg | Deep blue | #2F5496 | Title and divider slide backgrounds |
| Title text | White | #FFFFFF | Text on dark backgrounds |
| Title subtitle | Ice blue | #CADCFC | Subtitle on dark backgrounds |

## Typography (python-pptx)

| Element | Font | Size | Style | Color |
|---------|------|------|-------|-------|
| Slide title | Calibri | 32-36pt | Bold | #2F5496 |
| Subtitle | Calibri | 18-20pt | Regular | #666666 |
| Body text | Calibri | 14-16pt | Regular | #333333 |
| Stat callout number | Calibri | 60pt | Bold | #ED7D31 |
| Stat callout label | Calibri | 14pt | Regular | #333333 |
| Data labels | Calibri | 10-12pt | Regular | #333333 |
| Source line | Calibri | 9pt | Italic | #999999 |

## python-pptx Color Constants

```python
from pptx.dml.color import RGBColor

PRIMARY = RGBColor(0x2F, 0x54, 0x96)
SECONDARY = RGBColor(0x44, 0x72, 0xC4)
ACCENT = RGBColor(0xED, 0x7D, 0x31)
DARK_TEXT = RGBColor(0x33, 0x33, 0x33)
LIGHT_TEXT = RGBColor(0x66, 0x66, 0x66)
SOURCE_TEXT = RGBColor(0x99, 0x99, 0x99)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ICE_BLUE = RGBColor(0xCA, 0xDC, 0xFC)
```

## Matplotlib Chart Styling

For charts embedded as images:

```python
import matplotlib.pyplot as plt

# Global settings
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Calibri', 'Arial', 'Helvetica'],
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.facecolor': 'white',
    'savefig.facecolor': 'white',
    'savefig.dpi': 150,
})

# Standard colors for charts
CHART_COLORS = ['#2F5496', '#4472C4', '#ED7D31', '#A5A5A5', '#FFC000']
```

### Horizontal Bar Chart (most common for survey data)

```python
def style_horizontal_bar(ax, title, values, labels):
    colors = ['#2F5496' if v < 50 else '#ED7D31' for v in values]
    bars = ax.barh(labels, values, color=colors, height=0.6)
    
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}%', va='center', fontsize=10, color='#333333')
    
    ax.set_xlim(0, max(values) * 1.15)
    ax.set_title(title, fontsize=14, fontweight='bold', color='#2F5496', pad=15)
    ax.invert_yaxis()  # Highest value at top
```

## Slide Layout Templates

### Title Slide
- Dark blue (#2F5496) solid background
- Title: White, 36pt bold, left-aligned, positioned at ~30% from top
- Subtitle: Ice blue (#CADCFC), 18pt, left-aligned below title
- Content: "n=X | Date"

### Section Divider
- Dark blue background
- Section title: White, 32pt bold, centered vertically

### Data Slide
- White background
- Title: 32pt bold #2F5496, top-left (0.5" from top)
- Chart/visual: 60%+ of slide area, centered
- Insight text (optional): 14pt #333333, below or beside chart
- Source line: 9pt italic #999999, bottom-left (0.3" from bottom)

### Executive Summary (Stat Callouts)
- White background
- Title: "Key Findings" at top
- 3 stat boxes arranged horizontally:
  - Number: 60pt bold #ED7D31, centered
  - Label: 14pt #333333, centered below number
  - Each box ~4" wide

## Source Line Format

Every data slide must include:

```
Source: [Survey Name], n=X. [Methodology note if relevant].
```

Position: bottom of slide, 0.5" from left, 0.3" from bottom edge.

## Anti-Patterns to Avoid

- Text-only slides with no visual element
- More than one chart per slide
- Title text smaller than 28pt
- Missing source lines on data slides
- Charts without labeled axes
- Using the default matplotlib color cycle
- Accent lines under titles (looks AI-generated)
- Equal-weight colors (one color should dominate)
