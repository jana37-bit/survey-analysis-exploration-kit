# Output Checklist

Verify all deliverables before declaring the analysis complete.

## Required Files (outputs/)

### survey_recoded.sav
- [ ] Contains all original variables (unchanged)
- [ ] Contains recoded variables with correct suffix (_top2, _top3, etc.)
- [ ] Variable labels transferred to recoded variables with [Box Type] suffix
- [ ] Value labels set: {0: "Bottom box", 1: "Top 2 Box"}
- [ ] Same respondent count as original
- [ ] Total columns = original columns + recoded columns

### banner_tables.xlsx
- [ ] Sheet "Banner Tables" exists
  - [ ] Header row: banner column names on blue background, frozen at A2
  - [ ] Section headers: "ORIGINAL VARIABLES" and "RECODED VARIABLES" separating the two groups
  - [ ] Per variable block: SPSS name (bold) → label (italic) → base row → value rows → separator
  - [ ] BOTH original variables (all scale points as rows) AND recoded _top2 variables present
  - [ ] Cells contain percentages formatted with % symbol (76.5%, stored as 0.765 with '0.0%' format)
  - [ ] Per-variable Base (n) rows show integer N values — NOT one global base at the bottom
  - [ ] Empty banner columns (0 respondents) are omitted (--skip-empty-banners)
  - [ ] Dash "-" shown where base is 0 for a specific variable × banner combination
- [ ] Sheet "Validation Crosstabs" exists
  - [ ] Shows original value → recoded value mapping for each variable
- [ ] Sheet "Significance Tests" exists
  - [ ] Green fill (#C6EFCE) for p < 0.05
  - [ ] Orange fill (#FCE4D6) for 0.05 ≤ p < 0.10
- [ ] Sheet "SPSS Syntax" exists (copy of the .sps content)

### spss_custom_tables_syntax.sps
- [ ] Valid SPSS syntax (CTABLES commands)
- [ ] Covers all original row variables
- [ ] Covers all recoded row variables
- [ ] Uses correct banner variable names
- [ ] Can be opened and run in SPSS directly

### analysis_script.py
- [ ] Complete Python script with all imports
- [ ] Runs end-to-end without errors
- [ ] Paths relative to project root

### metadata.json
- [ ] Lists all variables with names, labels, types
- [ ] Documents recoding scheme and thresholds
- [ ] Records don't know codes found
- [ ] Includes respondent count and variable count

## Quick Spot Checks

1. **Percentages sum check**: For any single variable in one banner column, the percentages across all values should sum to ~100% (allowing for rounding)
2. **Base consistency**: The base for a recoded variable should equal the base for its original (after don't know removal)
3. **Column count**: The recoded .sav should have more columns than the original
4. **Syntax variable names**: Every variable name in the .sps file should exist in the recoded .sav
