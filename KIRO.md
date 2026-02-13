# Survey Analysis Kit

Automated SPSS survey analysis with a guided, interactive workflow.

## First Time Setup
Run `bash scripts/setup_env.sh` to install Python dependencies.

## How To Use
1. Drop your .sav file in `data/`
2. Launch: `kiro-cli chat --agent survey-analyst` (or `/agent swap survey-analyst` in an existing session)
3. Type: **`Analyze my survey`**

That's it. The workflow below handles the rest.

---

## Workflow (read this before doing anything)

When the user says "analyze my survey" (or similar), follow these steps **in order**. Read `.kiro/steering.md` and `.kiro/skills/spss-survey-analysis/SKILL.md` first.

### Step 1 → Load and explore
Run `scripts/explore_variables.py` on the .sav file in `data/`.

Present findings to the user grouped by type:
- "Here are your **attitudinal statements** — satisfaction, agreement scales. Here are their distributions. Shall I do top 2 box on all of these?"
- "Here are your **usage/frequency questions**. Keep original categories, or split into tertile/quartile/binary?"
- "Here are your **behavioral questions**. These are typically kept as-is."
- "These look like your **demographics/banner candidates** with base sizes. Which ones for column breaks?"

**⏸ WAIT for user decisions before proceeding.**

### Step 2 → Recode
Apply the user's choices. Run `scripts/recode_variables.py`.
Save recoded .sav with BOTH originals AND new variables to `outputs/`.

### Step 3 → Audit
Run `scripts/audit_data.py` on the recoded file.
Show the user: original vs recoded variable counts, banner column bases, table preview.

**⏸ WAIT for user confirmation.**

### Step 4 → Generate tables
Run `scripts/create_banner_tables.py` with `--skip-empty-banners`.
Run `scripts/significance_tests.py` and add results to the workbook.
Run `scripts/generate_spss_syntax.py`.
Add syntax sheet to workbook.

### Step 5 → Deliver
Save everything to `outputs/`:
- `survey_recoded.sav` (original + recoded variables, all metadata)
- `banner_tables.xlsx` (4 sheets: Banners, Validation, Significance, Syntax)
- `spss_custom_tables_syntax.sps`
- `analysis_script.py`
- `metadata.json`

## Rules
- ALWAYS read `.kiro/skills/spss-survey-analysis/SKILL.md` before coding
- Use pyreadstat for SPSS files (never pandas.read_spss)
- Preserve all SPSS metadata (variable labels, value labels)
- Banner tables: percentages with % symbol, per-variable base rows
- Include BOTH original distributions AND recoded variables
- Skip empty banner columns (0 respondents)
- Always run significance tests
- Always generate SPSS syntax for QA
