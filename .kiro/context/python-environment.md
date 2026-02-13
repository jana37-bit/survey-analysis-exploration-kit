# Python Environment for Survey Analysis

## Required Packages

Install before first use:
```bash
pip install pyreadstat pandas numpy scipy openpyxl python-pptx matplotlib seaborn
```

## Approved Packages and Usage

| Package | Use For | Critical Notes |
|---------|---------|----------------|
| `pyreadstat` | Loading/saving .sav files | ALWAYS use this, never `pandas.read_spss` |
| `pandas` | Data manipulation, crosstabs | Use `pd.crosstab()` for cross-tabulation |
| `numpy` | Array operations, NaN handling | Use `np.nan` for missing values |
| `scipy.stats` | Chi-square tests, t-tests | `chi2_contingency` for significance testing |
| `openpyxl` | Excel creation with formatting | Use for banner tables (not just `df.to_excel`) |
| `python-pptx` | PowerPoint generation | Required for presentation outputs |
| `matplotlib` | Chart creation for PPTX | Save to BytesIO buffer for embedding |
| `seaborn` | Statistical visualizations | Optional, for prettier charts |

## Standard Loading Pattern

```python
import pyreadstat
import pandas as pd
import numpy as np

# CORRECT: Load with full metadata
df, meta = pyreadstat.read_sav('data/survey.sav')

# Access metadata:
# meta.column_names              → list of variable names
# meta.column_labels             → list of variable labels (question text)  
# meta.variable_value_labels     → dict: {var_name: {code: label}}
# meta.number_rows               → respondent count
# meta.number_columns            → variable count
```

## Standard Saving Pattern

```python
# CORRECT: Save with all metadata
pyreadstat.write_sav(
    df_recoded,
    'outputs/survey_recoded.sav',
    column_labels=all_column_labels,      # list, same order as df.columns
    variable_value_labels=all_value_labels  # dict of dicts
)
```

## Common Mistakes to Avoid

1. ❌ `pd.read_spss()` — loses metadata
2. ❌ Modifying the original DataFrame without `.copy()` 
3. ❌ Using `df.to_excel()` alone — loses formatting control
4. ❌ Hardcoding don't know as code 99 — varies by survey
5. ❌ Assuming all Likert scales are 5-point — check each variable
6. ❌ Forgetting to handle NaN in percentage calculations (divide by zero)
