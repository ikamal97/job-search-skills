# ResumeReviewer Workflow Design

**Date:** 2026-01-15
**Location:** JobSearchToolkit/Workflows/ResumeReviewer.md
**Status:** Approved

## Overview

A ruthless hiring manager simulation that critiques resumes and outputs revised versions. Integrates with existing JobSearchToolkit infrastructure.

## Requirements

- **Target user:** Single user (leverages Career Context files)
- **Modes:** General (default) or Job-specific (if JD provided)
- **Critique style:** Ruthless, no sugarcoating, 30-second scan simulation
- **Output:** Concise feedback (~200 words) + revised .docx to ~/Downloads/

## Triggers

| Trigger | Mode |
|---------|------|
| "review resume", "critique resume" | General |
| "review my resume for [Company/Role]" | Job-specific |
| "review [filepath]" | General (explicit file) |
| "review [filepath] against [JD]" | Job-specific (explicit) |

## Critique Framework

| Area | What They Judge | Example Feedback |
|------|-----------------|------------------|
| **First Impression** | Name, title, summary - care in 5 seconds? | "Generic summary. You sound like everyone else." |
| **Impact Proof** | Numbers, metrics, outcomes - or task lists? | "You 'managed projects' - so what? What happened?" |
| **Relevance** | Experience supports claimed expertise? | "You claim 'data analytics' but one SQL mention." |
| **Clarity** | Understand without re-reading? | "This bullet is 47 words. I stopped at 15." |
| **Red Flags** | Gaps, job-hopping, buzzword stuffing | "3 jobs in 2 years. Why should I risk you?" |
| **ATS Survival** | Will this reach a human? | "No keywords from the JD in your summary." |

**Master Context cross-check:** Catches underselling (unused metrics) and overselling (claimed expertise you don't have).

## Output Format

### Context Window (~200 words max)

```
## Resume Review: [filename]

### Verdict: [WEAK / DECENT / STRONG]

### 30-Second Scan Reaction
"[1-2 sentence gut reaction as hiring manager]"

### Critical Issues (fix these)
1. [Issue] → [Specific fix]
2. [Issue] → [Specific fix]
3. [Issue] → [Specific fix]

### Missed Opportunities (from Master Context)
- [Thing you could've mentioned but didn't]

### Job-Specific Gaps (if JD provided)
- Missing keywords: [list]
- Fit score: X/10

📄 Revised resume: ~/Downloads/Your_Name_Resume.docx
```

### DOCX Output

- **General:** `Your_Name_Resume.docx`
- **Job-specific:** `Your_Name_Resume_[Company].docx`
- Uses existing resume-spec.yaml formatting
- One-page enforcement from existing infrastructure

## Process Flow

```
1. Locate resume (auto-find or provided path)
2. Parse resume content
3. Load Master Context (ground truth)
4. Load JD if provided → parse requirements
5. Run critique framework (6 areas)
6. Generate revision (apply fixes, integrate missed opportunities)
7. Enforce one-page limit
8. Output .docx to ~/Downloads/
9. Return concise feedback to context
```

## Auto-Find Logic

Searches for most recent .docx with "resume" in filename:
1. `~/Downloads/`
2. `~/Career/`

## Integration

### Files to Create/Modify

1. **Create:** `Workflows/ResumeReviewer.md` - main workflow
2. **Modify:** `SKILL.md` - add workflow to routing table

### Shared Infrastructure

- `Templates/resume-spec.yaml` - formatting spec
- `Templates/TemplateProcessor.py` - DOCX generation
- Master Context loading pattern from other workflows
- One-page enforcement algorithm from ResumeTailoring

## SKILL.md Routing Entry

```markdown
| **ResumeReviewer** | "review resume", "critique resume", "review my resume for [Company]" | `Workflows/ResumeReviewer.md` (Ruthless hiring manager critique, outputs revised .docx) |
```
