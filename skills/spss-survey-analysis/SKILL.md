---
name: spss-survey-analysis
description: "Complete SPSS survey data analysis workflow. Use when analyzing .sav files, creating banner tables, recoding Likert scales, handling don't know responses, generating crosstabs, and producing market research deliverables (Excel workbooks, recoded SPSS files, SPSS syntax, PowerPoint summaries). Trigger when user mentions SPSS, .sav, survey data, banner tables, crosstabs, Likert scales, top 2 box, or market research analysis."
---

# SPSS Survey Analysis

Standardized market research workflow: load SPSS data → understand metadata → recode variables → generate banner tables → deliver finished files.

## Quick Reference

| Task | Script |
|------|--------|
| Load SPSS and extract metadata | `scripts/load_metadata.py <file.sav>` |
| Classify variables automatically | `scripts/classify_variables.py <file.sav>` |
| **Explore & decide recoding** | `scripts/explore_variables.py <file.sav>` |
| Recode Likert scales + handle don't knows | `scripts/recode_variables.py <file.sav> <output.sav>` |
| **Audit data before table generation** | `scripts/audit_data.py <recoded.sav> --banners X,Y,Z` |
| Generate banner tables (Excel) | `scripts/create_banner_tables.py <file.sav> <output.xlsx>` |
| Generate SPSS syntax for QA | `scripts/generate_spss_syntax.py` |
| Run significance tests | `scripts/significance_tests.py <file.sav>` |

## Workflow

### Phase 1: Understand the data

```bash
python scripts/load_metadata.py data/survey.sav
```

Quick structural overview: respondent count, variable count, data types.

### Phase 1.5: Explore variables and decide recoding (INTERACTIVE)

```bash
python scripts/explore_variables.py data/survey.sav
```

This is the most important step. The script groups variables by type and shows distributions:

- **Attitudinal statements** (agreement, satisfaction) → show the scales and suggest top 2 box
- **Usage/frequency questions** (how often, how many) → suggest keeping as-is, or tertile/quartile splits
- **Behavioral questions** (have you ever, do you) → usually keep as-is
- **Awareness questions** → usually keep as-is
- **Intent/likelihood** → suggest top 2 box
- **Banner candidates** (demographics) → show base sizes per value

**Present each group to the user and ask:**
1. "Here are your attitudinal statements with distributions. Top 2 box for all of these?"
2. "Here are your usage questions. Keep the original categories, or split into tertile/quartile?"
3. "These look like your banner variables. Which ones do you want as column breaks?"

**Wait for the user's decisions before proceeding.** Record their choices — you'll need them for the recoding step.

For methodology details, read `references/analysis-methodology.md`.

### Phase 2: Prepare the data

```bash
python scripts/recode_variables.py data/survey.sav outputs/survey_recoded.sav --scheme top2
```

Apply the recoding decisions from Phase 1.5. This handles don't know recoding and Likert scale recoding in one step. Read `references/recoding-rules.md` for the recoding logic and naming conventions.

**Critical**: The recoded .sav MUST contain BOTH original variables AND new _top2 variables. If the recoding script drops the originals, the banner tables will be incomplete.

### Phase 2.5: Audit (intermediate verification)

```bash
python scripts/audit_data.py outputs/survey_recoded.sav --banners Country,Gender,Age
```

This step exists because the most common failure mode is generating banner tables from incomplete data. The audit script shows:
- How many original vs recoded variables exist
- Whether each recoded variable has a matching original
- Which banner columns have 0 respondents (these should be skipped)
- A preview of exactly what the banner table will contain

**Pause for user confirmation again.** If the audit shows missing originals or unexpected variable counts, fix the recoding step before proceeding.

### Phase 3: Generate deliverables

```bash
python scripts/create_banner_tables.py outputs/survey_recoded.sav outputs/banner_tables.xlsx \
    --banners "Country,Gender,Age" --skip-empty-banners
python scripts/significance_tests.py outputs/survey_recoded.sav \
    --banners "Country,Gender,Age" --output outputs/banner_tables.xlsx
python scripts/generate_spss_syntax.py \
    --vars "Q1-Q15" --banners "Country,Gender,Age" \
    --output outputs/spss_custom_tables_syntax.sps
```

The banner tables script generates an Excel workbook with:
- **ORIGINAL variables** showing all scale points (e.g., Very dissatisfied → Very satisfied) as percentages
- **RECODED variables** showing Top 2 Box as percentages
- **Per-variable base rows** (not one global base at the bottom)
- **Percentages formatted as %** in Excel (76.5%, not 76.5)
- **Empty banner columns skipped** when using `--skip-empty-banners`

The significance tests script ADDS a sheet to the existing workbook with chi-square results and color coding.

For Excel formatting standards, read the xlsx-survey skill. For PowerPoint, read the pptx-survey skill.

### Phase 4: Verify and deliver

Check `references/output-checklist.md` to verify all deliverables are complete. Run the validation step in the banner tables script to spot-check percentages.

## Output Files

All deliverables go to `outputs/`:

| File | Description |
|------|-------------|
| `survey_recoded.sav` | New SPSS file: original + recoded variables, all metadata preserved |
| `banner_tables.xlsx` | Excel workbook (4 sheets: banners, validation, significance, syntax) |
| `spss_custom_tables_syntax.sps` | SPSS syntax for QA verification in SPSS |
| `analysis_script.py` | Combined Python script for reproducibility |
| `metadata.json` | Variable dictionary and recoding documentation |

## Important Principles

The reason these rules exist is that market researchers need to verify AI outputs against SPSS and existing workflows. Breaking these conventions creates distrust and rework.

- **Use `pyreadstat`** for SPSS I/O — `pandas.read_spss` loses metadata that researchers depend on
- **Preserve all metadata** — variable labels are the question text; losing them makes outputs unusable
- **Both original AND recoded variables in banner tables** — researchers need the full distribution (all 5 or 7 scale points as rows with percentages) alongside the T2B headline number. A table with only T2B variables is incomplete and will be rejected.
- **Percentages in cells, formatted as %** — use Excel's percentage format (`0.0%`) so cells display as "76.5%" not as a plain number "76.5". This avoids confusion with counts.
- **Per-variable base rows** — each variable block gets its own base row showing valid N per banner column. A single global base at the bottom doesn't work because different questions may have different response rates.
- **Skip empty banner columns** — if a country/group has 0 respondents, omit it entirely rather than showing a column of zeros or dashes (use `--skip-empty-banners` flag)
- **Always generate .sps syntax** — researchers verify by running syntax in SPSS and comparing to the Excel
- **Always run significance tests** — add the Significance Tests sheet to the Excel workbook; don't deliver a workbook without it
- **Recoded .sav files keep everything** — original variables untouched, new variables added with `_top2` suffix
- **Run the audit step** — `audit_data.py` catches the most common problems before they become expensive Excel rework
