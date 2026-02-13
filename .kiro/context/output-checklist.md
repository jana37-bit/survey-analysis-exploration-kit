# Output Checklist

## Full Analysis Deliverables

Before declaring the task complete, verify ALL of these exist in `/outputs`:

### Required Files

- [ ] `survey_recoded.sav` — New SPSS file
  - Contains ALL original variables (unchanged)
  - Contains ALL recoded variables (with _top2 suffix)
  - Variable labels transferred to new variables
  - Value labels set: {0: 'Bottom box', 1: 'Top 2 box'}
  - Same number of respondents as original

- [ ] `banner_tables.xlsx` — Excel workbook with multiple sheets
  - Sheet 1 "Banner Tables": Main banner output
    - Header row: banner column names on blue background, frozen
    - Per variable block: SPSS name (bold) → label (italic) → Base (n) row → value rows → separator
    - BOTH original variables (all scale points as rows) AND recoded _top2 variables
    - **Percentages formatted with % symbol** (76.5%, not plain 76.5)
    - Each variable has its own Base (n) row (NOT one global base at the bottom)
    - Empty banner columns (0 respondents) should be omitted
    - Section headers separating "Original Variables" from "Recoded Variables"
  - Sheet 2 "Validation Crosstabs": Original vs recoded distributions
  - Sheet 3 "Significance Tests": Chi-square results with green/orange color coding
  - Sheet 4 "SPSS Syntax": Copy of generated syntax

- [ ] `spss_custom_tables_syntax.sps` — Standalone SPSS syntax file
  - CTABLES syntax for all original variables
  - CTABLES syntax for all recoded variables
  - Can be opened and run directly in SPSS

- [ ] `analysis_script.py` — Complete Python script used
  - Fully runnable from command line
  - Includes all imports, functions, and execution
  - Paths relative to project root

- [ ] `metadata.json` — Variable dictionary
  - All variables with names, labels, types
  - Classification (likert/nominal/binary/other)
  - Don't know codes identified
  - Recoding documentation

### Optional Files (if requested)

- [ ] `summary_presentation.pptx` — PowerPoint with findings
- [ ] `charts/` — Individual chart images (PNG)

## Quality Checks

Before finalizing:
1. Open banner_tables.xlsx — verify percentages sum reasonably per column
2. Check survey_recoded.sav has more columns than original
3. Verify .sps syntax has no typos in variable names
4. Confirm metadata.json lists the correct number of variables
5. Run analysis_script.py to verify it completes without errors
