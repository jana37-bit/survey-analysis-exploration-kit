# Quick-Start Prompts for Kiro CLI

The workflow is baked into `KIRO.md` which Kiro reads automatically.
These prompts are all you need.

---

## Standard Analysis (most common)

```
Analyze my survey
```

Kiro will read KIRO.md, explore your variables, ask you how to recode each group, then generate everything.

---

## Just explore the data (no analysis yet)

```
Explore the variables in my survey — show me what's in the data and group them by type
```

---

## Skip straight to tables (data already recoded)

```
Generate banner tables from the recoded .sav in data/ using Country, Gender, Age as banners. Skip empty columns. Include significance tests.
```

---

## With PowerPoint

```
Analyze my survey. After the tables, also create a summary PowerPoint.
```

---

## Custom recoding

```
Analyze my survey with these specifics:
- Top 3 box instead of top 2
- Usage questions: split into tertile (light/medium/heavy)
- Banners: Country, Age, Gender, Device_Type
```
