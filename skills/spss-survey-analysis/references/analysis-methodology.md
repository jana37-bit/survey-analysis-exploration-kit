# Analysis Methodology

This document explains the reasoning behind each phase of the survey analysis workflow.
Read this when you need to understand **why** certain decisions are made, not just how.

## Why This Order Matters

Market researchers follow a strict sequence because each step depends on the previous one being correct. Skipping ahead (e.g., generating banner tables before handling don't knows) produces wrong percentages that are hard to debug later.

```
Understand → Prepare → Analyze → Deliver
```

Each phase has a quality gate: you must verify results before moving to the next.

## Phase 1: Understanding the Data

**Why examine metadata first?** SPSS files encode meaning in metadata that isn't visible in the raw numbers. A column of values `1,2,3,4,5,97,98` looks like continuous data until you read the value labels and discover `97="Don't know"` and `98="Refused"`. Without this step, your recoding thresholds will be wrong.

**What to look for:**
- Variable labels tell you the actual survey question ("How satisfied are you with X?")
- Value labels tell you what the numbers mean (1="Very dissatisfied" ... 5="Very satisfied")
- The presence and coding of don't know/refused responses varies by survey — there is no universal code

**Why pause for user confirmation?** Variable classification is heuristic. Some variables look like Likert scales but aren't (e.g., a ranking question 1-5 where order matters differently). The researcher knows their data better than any algorithm.

## Phase 2: Data Preparation

### Don't Know Handling

**Why replace with NaN?** Don't know responses are not valid scale points. If someone answers "Don't know" to a satisfaction question, including their `97` in a mean or percentage calculation is a mathematical error. Setting to NaN excludes them from the denominator, which is standard practice.

**Why identify by value labels, not fixed codes?** Different surveys use different codes. Some use 99, some use 97, some use -1, some use 8 or 9. The only reliable way to identify them is by reading what the value label says.

### Likert Recoding

**Why top-2-box?** Market researchers often need to simplify Likert responses for executive reporting. "72% agree" is more actionable than showing the full distribution. Top-2-box (combining the top 2 scale points) is the industry standard.

**Scale detection logic:**
- 5-point scale (1-5): Top 2 = values 4 and 5
- 7-point scale (1-7): Top 2 = values 6 and 7
- 10-point scale (1-10): Top 2 = values 9 and 10
- General rule: the highest N values on the scale

**Why create new variables?** Never modify originals. Researchers need both: the full distribution for detailed analysis, and the binary for quick comparisons. The `_top2` suffix makes it clear which is which.

**Why transfer variable labels?** Without labels, a variable named `Q3_top2` is meaningless. Adding "[Top 2 Box]" to the original label ("How satisfied are you? [Top 2 Box]") keeps the output self-documenting.

## Phase 3: Analysis

### Banner Tables

**Why percentages only?** Banner tables are for comparison across groups. Percentages enable this; raw counts don't (because group sizes differ). This matches the output format of SPSS Custom Tables.

**Why separate base rows?** The base (n) tells you how many respondents answered this question in each group. It's essential for interpretation: "80% satisfied" means different things with n=500 vs n=12. Embedding the base inside percentage cells makes the data harder to use.

**Why include both original and recoded?** The full distribution shows nuance (perhaps satisfaction is bimodal). The top-2-box gives a single headline number. Researchers use both for different purposes.

### Significance Testing

**Why chi-square?** For categorical data (which all Likert and recoded variables are), chi-square is the standard test for whether differences between groups are statistically significant.

**Color coding convention:**
- Green (p < 0.05): statistically significant at 95% confidence
- Orange (0.05 ≤ p < 0.10): marginally significant, worth noting
- No highlight (p ≥ 0.10): not significant

## Phase 4: Delivery

### Why generate SPSS syntax?

The .sps file serves as a verification mechanism. Researchers can run it in SPSS and compare the output against the Excel tables. If the percentages match, they trust the analysis. If they don't, something went wrong. This is the single most important quality assurance step.

### Why save the Python script?

Reproducibility. If the data changes or a mistake is found, the researcher (or their colleague) can re-run the exact same analysis. It also documents exactly what was done, which matters for audit trails.
