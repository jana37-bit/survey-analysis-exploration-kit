# Survey Analysis Kit for Kiro CLI

> Automated SPSS survey analysis — interactive variable exploration, Likert recoding, 
> banner tables with significance tests, SPSS syntax generation. All from your terminal.

---

## What This Does

Drop an SPSS file into `data/`, type `Analyze my survey`, and get production-ready deliverables:

| Feature | How It Works |
|---------|-------------|
| Interactive exploration | Groups variables by type, shows distributions, asks how to recode |
| Guided methodology | Phased workflow with checkpoints — you stay in control |
| Professional Excel output | Banner tables with per-variable bases, formatted percentages, sig tests |
| SPSS verification | Generated .sps syntax you can run in SPSS to cross-check results |
| Reusable methodology | Skills and scripts are version-controlled — same standards every time |

**You describe the analysis → Kiro reads your methodology → executes all phases → delivers finished files.**

---

## Quick Start (5 minutes)

### Step 1: Install Python Dependencies

```bash
pip install pyreadstat pandas numpy scipy openpyxl python-pptx matplotlib seaborn
```

### Step 2: Copy This Project to Your Machine

Copy the entire `survey-analysis-kit/` folder to your preferred location:

```bash
# Example: put it in your home directory
cp -r survey-analysis-kit ~/survey-analysis-kit
```

### Step 3: Add Your Data

Drop your SPSS file(s) into the `data/` folder:

```bash
cp /path/to/your/survey.sav ~/survey-analysis-kit/data/
```

### Step 4: Launch Kiro

Open the project folder in VS Code, then in the terminal:

```bash
cd ~/survey-analysis-kit
kiro-cli chat --agent survey-analyst
```

Or swap to the agent inside an existing Kiro session:
```
/agent swap survey-analyst
```

### Step 5: Start

Type:
```
Analyze my survey
```

That's it. Kiro reads `KIRO.md` automatically which contains the full guided workflow. It will:

1. **Explore** your variables, group them by type (attitudinal, usage, behavioral), and show distributions
2. **Ask you** how to handle each group — top 2 box? tertile? keep as-is?
3. **Recode** based on your decisions
4. **Audit** the recoded data and show you a preview before building tables
5. **Generate** banner tables, significance tests, SPSS syntax, and all deliverables

See `QUICK_START_PROMPTS.md` for other variations (e.g., skip to tables, add PowerPoint, custom recoding).

### Step 6: Collect Your Outputs

Everything lands in `outputs/`:

```
outputs/
├── survey_recoded.sav              # New SPSS file with recoded variables
├── banner_tables.xlsx              # Excel workbook (4 sheets)
├── spss_custom_tables_syntax.sps   # SPSS syntax for QA
├── analysis_script.py              # Python script for reproducibility
├── metadata.json                   # Variable dictionary
└── summary_presentation.pptx       # (if requested)
```

---

## Project Structure

```
survey-analysis-kit/
│
├── .kiro/                              ← KIRO CONFIGURATION
│   ├── steering.md                     ← Master project rules (read first)
│   ├── agents/
│   │   └── survey-analyst.json         ← Custom agent config
│   ├── context/
│   │   ├── python-environment.md       ← Approved packages & patterns
│   │   └── output-checklist.md         ← Quality assurance checklist
│   └── skills/
│       ├── spss-survey-analysis/       ← Core analysis methodology
│       │   ├── SKILL.md               ← Orchestration & quick reference
│       │   ├── scripts/               ← Standalone executable scripts
│       │   │   ├── load_metadata.py
│       │   │   ├── classify_variables.py
│       │   │   ├── recode_variables.py
│       │   │   ├── create_banner_tables.py
│       │   │   ├── generate_spss_syntax.py
│       │   │   └── significance_tests.py
│       │   └── references/            ← Domain docs loaded on demand
│       │       ├── analysis-methodology.md
│       │       ├── recoding-rules.md
│       │       └── output-checklist.md
│       ├── xlsx-survey/                ← Excel creation standards
│       │   ├── SKILL.md
│       │   ├── scripts/
│       │   │   ├── add_syntax_sheet.py
│       │   │   └── validate_workbook.py
│       │   └── references/
│       │       └── formatting-standards.md
│       └── pptx-survey/                ← PowerPoint creation standards
│           ├── SKILL.md
│           ├── scripts/
│           │   ├── create_chart.py
│           │   └── build_presentation.py
│           └── references/
│               └── design-standards.md
│
├── data/                               ← YOUR SPSS FILES (read-only)
│   └── (drop .sav files here)
│
├── outputs/                            ← DELIVERABLES (generated)
│   └── (Excel, PPTX, SAV, SPS files)
│
├── scripts/                            ← UTILITY SCRIPTS
│   └── setup_env.sh                    ← Environment setup script
│
├── templates/                          ← OPTIONAL TEMPLATES
│   └── (PowerPoint templates, etc.)
│
└── README.md                           ← This file
```

---

## How It Works (Under the Hood)

### What Kiro Reads Automatically

When you launch Kiro in this folder, the steering file and context files are loaded:

1. **`.kiro/steering.md`** — Project overview, golden rules, Python environment
2. **`.kiro/context/python-environment.md`** — Package requirements, code patterns
3. **`.kiro/context/output-checklist.md`** — What files to produce

### What Kiro Reads On-Demand

When you ask for analysis, the agent reads the relevant skill:

1. **`.kiro/skills/spss-survey-analysis/SKILL.md`** — Orchestration and quick reference for the 6-phase methodology
2. **`.kiro/skills/spss-survey-analysis/references/`** — Domain docs: methodology rationale, recoding rules, output checklist
3. **`.kiro/skills/spss-survey-analysis/scripts/`** — Standalone scripts that do the actual work
4. **`.kiro/skills/xlsx-survey/SKILL.md`** — Excel formatting standards
5. **`.kiro/skills/pptx-survey/SKILL.md`** — PowerPoint design standards

Each skill follows a standard structure:
`SKILL.md` (orchestration) + `scripts/` (executable code) + `references/` (domain docs)

### The Analysis Pipeline

```
[You: "Analyze survey.sav with top 2 box recoding"]
        │
        ▼
[Phase 1: UNDERSTAND]
├── Load SPSS file with pyreadstat
├── Extract all metadata
├── Classify variables (Likert / demographic / other)
├── Identify don't know codes from value labels
└── Show findings → ask for confirmation
        │
        ▼
[Phase 2: PREPARE]
├── Replace don't know codes with NaN
├── Recode Likert scales to _top2 binary variables
├── Transfer variable labels to new variables
└── Save recoded .sav file with full metadata
        │
        ▼
[Phase 3: ANALYZE]
├── Generate banner tables (percentages only)
├── Create validation crosstabs
├── Run chi-square significance tests
└── Build Excel workbook with all sheets
        │
        ▼
[Phase 4: DELIVER]
├── Save Excel workbook to outputs/
├── Generate SPSS syntax file
├── Save Python script for reproducibility
├── Save metadata JSON
├── (Optional) Create PowerPoint summary
└── Report: list all files created
```

---

## Customization

### Changing Recoding Scheme

Edit `.kiro/skills/spss-survey-analysis/references/recoding-rules.md` and the `recode_variables.py` script. Change the threshold logic:

- **Top 2 Box** (default): Highest 2 values → 1, rest → 0
- **Top 3 Box**: Highest 3 values → 1, rest → 0  
- **Bottom 2 Box**: Lowest 2 values → 1, rest → 0

### Adding New Banner Variables

Just specify them in your prompt:
```
Use Country, Region, Age, Gender, Income as banner columns
```

### Changing Variable Suffix

Replace `_top2` with your preferred suffix in the SPSS skill file.

### Adding a PowerPoint Template

Drop a .pptx template in `templates/` and reference it:
```
Create a summary presentation using the template in templates/my_template.pptx
```

---

## Tips for Best Results

1. **Be specific about variables**: "Q1-Q15 are 7-point Likert scales" helps Kiro classify correctly
2. **Name your banners**: "Use Total, Country, Age_3groups, Gender as columns" is better than "use demographics"
3. **One SPSS file at a time**: Keep one .sav in `data/` per analysis run
4. **Check validation sheet**: Always review Sheet 2 of the Excel to verify recoding
5. **Run the SPSS syntax**: Copy the .sps file into SPSS to verify percentages match
6. **The workflow is baked in**: `KIRO.md` contains the full guided workflow, so "Analyze my survey" is usually enough. If Kiro skips steps, explicitly say "Read .kiro/skills/spss-survey-analysis/SKILL.md first"

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Kiro doesn't follow methodology | Explicitly say: "Read .kiro/skills/spss-survey-analysis/SKILL.md first" |
| Missing packages | Run: `pip install pyreadstat pandas numpy scipy openpyxl python-pptx matplotlib seaborn` |
| Only top 2 boxes, no originals | Remind: "Include BOTH original variables with all scale points AND recoded variables" |
| Counts instead of percentages | Remind: "Percentages only in cells, bases as separate rows" |
| Recoded file is Excel, not .sav | Remind: "Save recoded data as .sav file using pyreadstat.write_sav" |
| No SPSS syntax generated | Remind: "Always generate a .sps syntax file for QA" |
| Agent forgets rules mid-session | Re-reference: "Check .kiro/steering.md and the output checklist" |

---

## Why This Approach

| Traditional SPSS Workflow | With This Kit |
|---------------------------|---------------|
| Open SPSS, manually recode variables | Automated recoding with configurable rules |
| Build tables one at a time in Custom Tables | Full banner tables generated in seconds |
| Copy-paste into Excel, format manually | Pre-formatted Excel with per-variable bases and % |
| Run sig tests separately | Significance tests built into the workbook |
| No documentation of decisions | Everything versioned: scripts, methodology, decisions |
| Knowledge lives in one person's head | Methodology codified in skill files — shareable with team |

**Key advantage**: Your methodology is codified in skill files. Every analysis follows the same standards. You can version-control it, share it with colleagues, and iterate on it over time.


---

## (Optional) Use these skills in Claude Code

This repo also includes Agent/Claude Code-compatible skills (see `skills/`). If you use Claude Code, you can install them as a plugin via the marketplace file at `.claude-plugin/marketplace.json`:

```
/plugin marketplace add jana37-bit/survey-analysis-kit
/plugin install survey-analysis-kit@jana-survey-tools
```

After installing, you can invoke skills like:

```
/spss-survey-analysis
/xlsx-survey
/pptx-survey
```
