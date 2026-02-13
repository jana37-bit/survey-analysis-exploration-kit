# Excel Formatting Standards

Complete specification for survey analysis Excel outputs.

## Color Palette

| Element | Color | Hex | RGB |
|---------|-------|-----|-----|
| Header background | Dark blue | #2F5496 | 47, 84, 150 |
| Header text | White | #FFFFFF | 255, 255, 255 |
| Variable name | Black (bold) | #000000 | 0, 0, 0 |
| Variable label | Gray (italic) | #666666 | 102, 102, 102 |
| Base row text | Dark gray (italic) | #444444 | 68, 68, 68 |
| Data text | Black | #000000 | 0, 0, 0 |
| Row separator | Light gray border | #CCCCCC | 204, 204, 204 |
| Significant (p<.05) | Green fill | #C6EFCE | 198, 239, 206 |
| Marginal (p<.10) | Orange fill | #FCE4D6 | 252, 228, 214 |

## Typography

| Element | Font | Size | Style |
|---------|------|------|-------|
| Header | Arial | 11pt | Bold, White |
| Variable name | Arial | 11pt | Bold |
| Variable label | Arial | 10pt | Italic |
| Base row | Arial | 10pt | Italic |
| Data values | Arial | 10pt | Regular |

## Number Formats (openpyxl)

| Data Type | Format String | Stored Value | Display |
|-----------|---------------|--------------|---------|
| Percentages | `'0.0%'` | 0.765 | 76.5% |
| Percentages (5dp) | `'0.00000%'` | 0.7654321 | 76.54321% |
| Base counts | `'#,##0'` | 1523 | 1,523 |
| Chi-square | `'0.0000'` | 15.2341 | 15.2341 |
| p-value | `'0.000000'` | 0.001234 | 0.001234 |

**Critical**: Percentages are stored as DECIMALS (0.765) and displayed using Excel's built-in percentage format (`'0.0%'`). This renders as "76.5%" in the cell. Do NOT store as 76.5 with `'0.00000'` format — that shows a plain number without % and confuses researchers into thinking these are counts.

## Column Dimensions

| Column | Width | Content |
|--------|-------|---------|
| A | 45 | Variable names, labels, value labels |
| B onwards | 18 | Banner column data |

## openpyxl Style Objects

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

HEADER_FILL = PatternFill("solid", fgColor="2F5496")
HEADER_FONT = Font(name="Arial", bold=True, color="FFFFFF", size=11)
VARNAME_FONT = Font(name="Arial", bold=True, size=11)
LABEL_FONT = Font(name="Arial", italic=True, size=10, color="666666")
BASE_FONT = Font(name="Arial", italic=True, size=10, color="444444")
DATA_FONT = Font(name="Arial", size=10)
CENTER = Alignment(horizontal="center")
WRAP_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
THIN_BORDER = Border(bottom=Side(style="thin", color="CCCCCC"))
GREEN_FILL = PatternFill("solid", fgColor="C6EFCE")
ORANGE_FILL = PatternFill("solid", fgColor="FCE4D6")
```

## Sheet-Specific Rules

### Banner Tables Sheet
- Freeze pane at A2 (header row always visible)
- Autofilter on header row
- Print area: all populated cells
- Each variable block separated by thin bottom border + blank row

### Validation Crosstabs Sheet
- Freeze pane at A2
- Simple table layout: Variable, Original Value, Label, Count, %, Recoded Var, Recoded Value, Recoded Count
- Blank row between variable groups

### Significance Tests Sheet
- Freeze pane at A2
- Entire row colored (not just p-value cell) for significant results
- Green for p<.05, Orange for p<.10
