# Survey Analysis — Kiro Project Steering

## What This Project Does

Guided SPSS survey analysis: explore data → decide recoding with user → generate banner tables, significance tests, SPSS syntax. Drop .sav files in `data/`, get deliverables in `outputs/`.

## How To Start

When user says "analyze my survey" (or similar), follow the workflow in KIRO.md at the project root. The full step-by-step is there. In short:

1. **Explore** → Run `scripts/explore_variables.py`, show grouped variables, ask how to recode each group. **WAIT.**
2. **Recode** → Apply user decisions with `scripts/recode_variables.py`
3. **Audit** → Run `scripts/audit_data.py`, show preview. **WAIT.**
4. **Generate** → Banner tables, significance tests, SPSS syntax
5. **Deliver** → All files to `outputs/`

## Skills (read these before doing the work)

Each skill has standalone scripts you can run directly, plus reference docs for context.

| When doing this... | Read this first |
|---------------------|-----------------|
| Any SPSS analysis | `.kiro/skills/spss-survey-analysis/SKILL.md` |
| Creating Excel output | `.kiro/skills/xlsx-survey/SKILL.md` |
| Creating PowerPoint | `.kiro/skills/pptx-survey/SKILL.md` |

Scripts live in each skill's `scripts/` folder. Example:
```bash
python .kiro/skills/spss-survey-analysis/scripts/explore_variables.py data/survey.sav
python .kiro/skills/spss-survey-analysis/scripts/create_banner_tables.py outputs/survey_recoded.sav outputs/banner_tables.xlsx --banners Country,Gender,Age --skip-empty-banners
```

Reference docs live in `references/` — read these when you need the *why* behind a decision.

## Rules

### Never rush to code
Before writing any Python: load the data, explore variables, show the user what you found, and get their decisions on how to handle each variable group. Only then proceed.

### Preserve SPSS metadata
Variable labels (question text) and value labels MUST be preserved in all outputs. The original .sav is NEVER modified.

### Use pyreadstat, not pandas.read_spss
```python
import pyreadstat
df, meta = pyreadstat.read_sav('data/survey.sav')
# meta.column_labels → question text
# meta.variable_value_labels → {var: {code: label}}
```

### Banner tables must include BOTH original and recoded variables
Original variables show the full scale distribution (all 5 or 7 points as rows). Recoded variables show the Top 2 Box binary. A table with only T2B is incomplete.

### Percentages formatted as %
Store as decimals (0.765), format with `'0.0%'` in openpyxl. Cells display as "76.5%".

### Per-variable base rows
Each variable block gets its own Base (n) row. NOT one global base at the bottom.

### Skip empty banner columns
Use `--skip-empty-banners` flag. Columns with 0 respondents should be omitted.

### Always run significance tests
Add the Significance Tests sheet to the workbook. Green fill for p<.05, orange for p<.10.

### Always generate SPSS syntax
The .sps file is how researchers verify the analysis. Always create it.

### Recoded .sav keeps everything
Original variables untouched + new _top2 variables appended. Both in the same file.

## Python Environment

```bash
pip install pyreadstat pandas numpy scipy openpyxl python-pptx matplotlib seaborn
```

Or run: `bash scripts/setup_env.sh`

## File Organization

| Location | Purpose |
|----------|---------|
| `data/` | Source .sav files (read-only, never modify) |
| `outputs/` | All deliverables |
| `.kiro/skills/` | Methodology, scripts, references |
| `.kiro/context/` | Checklists, environment docs |
