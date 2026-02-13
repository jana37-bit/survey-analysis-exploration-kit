# Recoding Rules

Technical specification for how variables are recoded. Reference this when modifying the recoding scripts or when the user asks about recoding logic.

## Naming Conventions

| Original | Recoded | Suffix |
|----------|---------|--------|
| Q1 | Q1_top2 | `_top2` for top-2-box |
| Q1 | Q1_top3 | `_top3` for top-3-box |
| Q1 | Q1_bottom2 | `_bottom2` for bottom-2-box |

## Recoded Variable Labels

Format: `{original_label} [{Box Type}]`

Example: `"How satisfied are you with the service?" → "How satisfied are you with the service? [Top 2 Box]"`

## Recoded Value Labels

All recoded variables use the same value label scheme:

```
0 = "Bottom box"
1 = "Top 2 Box"    (or "Top 3 Box", "Bottom 2 Box" depending on scheme)
```

## Scale Detection

The script determines scale range by examining value labels, excluding don't know codes:

```
5-point scale:  values 1,2,3,4,5      → top2 threshold = 4  (values 4,5 → 1)
7-point scale:  values 1,2,3,4,5,6,7  → top2 threshold = 6  (values 6,7 → 1)
10-point scale: values 1,2,3,4,5,6,7,8,9,10 → top2 threshold = 9 (values 9,10 → 1)
```

General formula for top-N-box: `threshold = max_scale_value - N + 1`

## Don't Know Detection

Codes are identified by scanning value labels for these patterns (case-insensitive):

```
"don't know", "dont know", "dk", "not sure", "unsure",
"can't say", "no opinion", "refused", "prefer not",
"decline", "not applicable", "n/a"
```

These codes are replaced with `NaN` (system missing) **before** any recoding occurs.

## Edge Cases

- **Mixed scales in same file**: Each variable is handled independently. Q1 might be 5-point while Q10 is 7-point.
- **Variables with fewer than 3 scale points**: Skipped (not meaningful to recode).
- **All-missing variable**: Recoded variable will also be all NaN.
- **Don't know is the most common response**: Still replaced with NaN. The base will be smaller, which is correct — it means fewer people had an opinion.

## File Output

The recoded .sav file contains:
- ALL original variables (unchanged)
- ALL recoded variables (appended after originals)
- Complete variable labels for both original and recoded
- Complete value labels for both original and recoded
- Same number of respondents as original file
