---
name: xlsx-survey
description: "Excel workbook creation for survey analysis outputs. Use when generating banner tables, crosstabs, formatted spreadsheets, or any .xlsx deliverable from SPSS survey data. Handles professional formatting, multiple sheets, percentage-only cells, base rows, significance color coding, and frozen headers. Trigger when user mentions Excel, spreadsheet, .xlsx, banner tables, or crosstab output."
---

# Excel Survey Output

Creates professionally formatted Excel workbooks for market research deliverables.

## Quick Reference

| Task | How |
|------|-----|
| Create banner table workbook | `scripts/format_workbook.py <input.xlsx>` |
| Add SPSS syntax sheet | `scripts/add_syntax_sheet.py <workbook.xlsx> <syntax.sps>` |
| Validate workbook | `scripts/validate_workbook.py <workbook.xlsx>` |

## Formatting Standards

Read `references/formatting-standards.md` for the full specification. Key rules:

- **Header row**: Dark blue (#2F5496) background, white bold Arial 11pt
- **Percentages**: Stored as decimals, displayed with Excel % format (76.5% not 76.5)
- **Number format**: `'0.0%'` in openpyxl — store value as 0.765, displays as "76.5%"
- **Base rows**: Italic, separate from data rows, integer format
- **No counts in data cells**: Percentages only; bases go in dedicated base rows
- **Column A**: 45 chars wide (labels). Data columns: 18 chars wide
- **Frozen header row**: Always freeze pane at A2
- **Autofilter**: Applied to header row

## Workbook Sheet Structure

| Sheet | Contents |
|-------|----------|
| Banner Tables | Main output: variable blocks with percentages |
| Validation Crosstabs | Original vs recoded value mapping |
| Significance Tests | Chi-square results with color coding |
| SPSS Syntax | Copy of .sps file content |

## Variable Block Layout

Each variable in the Banner Tables sheet follows this exact structure:

```
Row N  : Q1                              ← SPSS name, bold
Row N+1: How satisfied are you with...?  ← Variable label, italic gray
Row N+2: Base (n)  |  500  |  150  | ... ← Base row per THIS variable, italic, integers
Row N+3:   Very satisfied  | 23.5% | ... ← Value row, indented, percentage with %
Row N+4:   Satisfied       | 48.9% | ... ← Value row
Row N+5:   Neutral         | 15.2% | ... ← Value row
...
Row N+X: ─────────────────────────────── ← Thin border separator
Row N+X+1: (blank)                       ← Empty row before next variable
```

## Common Mistakes

These cause researchers to reject the output and redo manually:

- **Showing only T2B variables without original distributions** — the most common failure. Researchers need both: the full Likert scale (all 5 or 7 points) AND the binary T2B summary.
- **Percentages without % symbol** — storing 76.5 as a plain number instead of 0.765 with `'0.0%'` format. Researchers can't tell if "76.5" is a percentage or a count.
- **One global base row at the bottom** instead of per-variable base rows. Different questions have different valid-N counts.
- **Showing empty banner columns** (0 respondents) — creates columns of zeros/dashes that clutter the table.
- **Embedding base count inside percentage cells** (e.g., "45.2% (n=150)")
- **Missing the original variables** (showing only recoded top-2-box)
- **Forgetting to transfer variable labels to recoded variables**
- **Not freezing the header row**
- **Not running significance tests** — the workbook should always have a Significance Tests sheet
