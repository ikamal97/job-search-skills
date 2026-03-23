# ResumeReviewer Workflow v1.0

**Ruthless hiring manager critique with revised resume output.**

---

## Hard Constraints (NON-NEGOTIABLE)

| Rule | Constraint | Type |
|------|------------|------|
| 1 | Simulate skeptical HM who's seen 500 resumes today | PERSONA |
| 2 | Cross-check ALL claims against Master Context | AUTHENTICITY |
| 3 | Output feedback ≤ 200 words | CONCISE |
| 4 | Revised resume exactly 1 page | HARD CEILING |
| 5 | Use ResumeGenerator.js for DOCX generation | TOOLING |

---

## Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **General** | "review resume", "critique resume" | Universal quality critique |
| **Job-Specific** | "review resume for [Company]" | Adds keyword gap analysis, fit critique |

---

## Step 0: Locate Resume

**Auto-find logic** (in order):
1. Most recent `.docx` with "resume" in filename in `~/Downloads/`
2. Most recent `.docx` with "resume" in filename in `04 - Career/`
3. Explicit path if provided by user

```bash
ls -t ~/Downloads/*[Rr]esume*.docx 2>/dev/null | head -1
```

**If not found**: Ask user for path. Do not proceed without resume.

---

## Step 1: Load Context

1. **Parse resume** - Extract all content (summary, skills, experience bullets)
2. **Load Career Context** from `04 - Career/CONTEXT/`:
   - Professional Background - Index.md (always first)
   - Experience Details.md (for cross-checking achievements)
   - Honest Gaps.md (for authenticity constraints)
3. **Load JD (if job-specific)** - Parse via JobDescriptionParser or use provided text

---

## Step 2: Run Critique Framework

Simulate a hiring manager doing a 30-second scan. Be ruthless.

### Critique Areas

| Area | What to Judge | Ruthless Questions |
|------|---------------|-------------------|
| **First Impression** | Name, title, summary | Do I care in 5 seconds? Is this generic? |
| **Impact Proof** | Metrics, outcomes | "So what?" - Did anything actually happen? |
| **Relevance** | Experience vs claims | Does the experience back up what they claim? |
| **Clarity** | Readability | Can I understand this without re-reading? |
| **Red Flags** | Gaps, inconsistencies | What would make me say "next"? |
| **ATS Survival** | Keywords, formatting | Will this even reach a human? |

### Master Context Cross-Check

| Check | Action |
|-------|--------|
| **Underselling** | Flag achievements in Master Context not on resume |
| **Overselling** | Flag claims with no backing in Master Context |
| **Missed Metrics** | Note quantifiable achievements user forgot |
| **Wrong Emphasis** | Note if weaker experience is highlighted over stronger |

### Job-Specific Additions (if JD provided)

| Check | Action |
|-------|--------|
| **Keyword Gaps** | List required keywords missing from resume |
| **Fit Score** | Rate 1-10 based on requirement alignment |
| **Fatal Gaps** | Note any hard requirements user cannot meet |

---

## Step 3: Generate Verdict

Rate the resume:

| Verdict | Criteria |
|---------|----------|
| **WEAK** | Multiple critical issues, would not get interview |
| **DECENT** | Passes basic checks, but not memorable |
| **STRONG** | Clear value prop, would likely get interview |

Write a 1-2 sentence gut reaction as the hiring manager would think it.

---

## Step 4: Generate Revised Resume

Apply fixes from critique:

1. **Rewrite weak elements** - Summary, unclear bullets
2. **Add missed opportunities** - From Master Context cross-check
3. **Integrate missing keywords** - If job-specific, add authentically
4. **Enforce one-page** - Use existing reduction algorithm

### Use ResumeGenerator.js

Prepare input JSON with corrected content:

```json
{
  "professional_title": "[Improved title]",
  "summary": "[Rewritten summary with impact]",
  "skills": { ... },
  "titles": {
    "kavalier": "[Appropriate title]",
    "vicegerent": "[Appropriate title]"
  },
  "bullets": [
    ["[Improved Kavalier bullets]"],
    ["[Improved Vicegerent bullets]"],
    ["[Improved Oliver Wyman bullets]"],
    ["[Improved Deloitte bullets]"]
  ]
}
```

Generate:
```bash
node ~/.claude/skills/JobSearchToolkit/Templates/ResumeGenerator.js /tmp/resume_data.json "[CompanyName]"
```

### File Naming

| Mode | Filename |
|------|----------|
| General | `Idrees_Kamal_Resume.docx` |
| Job-Specific | `Idrees_Kamal_Resume_[Company].docx` |

**Output location**: `~/Downloads/`

---

## Step 5: Format Output

**Keep context window output under 200 words.**

```markdown
## Resume Review: [filename]

### Verdict: [WEAK / DECENT / STRONG]

### 30-Second Scan Reaction
"[1-2 sentence gut reaction - ruthless, no sugarcoating]"

### Critical Issues
1. [Issue] → [Fix applied]
2. [Issue] → [Fix applied]
3. [Issue] → [Fix applied]

### Missed Opportunities
- [Achievement from Master Context you weren't using]

### Job-Specific Gaps (if applicable)
- Missing keywords: [list]
- Fit score: X/10

📄 Revised resume: ~/Downloads/Idrees_Kamal_Resume.docx
```

---

## Ruthless Feedback Examples

Use these as calibration for tone:

| Issue | Ruthless Feedback |
|-------|-------------------|
| Generic summary | "You sound like everyone else. I've read this exact summary 50 times today." |
| Task list bullets | "You 'managed projects' - so what? What actually happened because of you?" |
| Buzzword stuffing | "You listed 15 skills. I don't believe you're expert in any of them." |
| Weak metrics | "'Improved efficiency' - by how much? 1%? 50%? This means nothing." |
| Missing context | "You built a CRM. For who? How big? What was the outcome?" |
| Irrelevant experience | "Why is this on here? It has nothing to do with what I'm hiring for." |
| Long bullets | "This bullet is 50 words. I stopped reading at 15." |
| Gaps unexplained | "6-month gap. Are you going to make me ask about it?" |

---

## Quality Checklist (Pre-Output)

Before returning:

- [ ] Verdict assigned (WEAK/DECENT/STRONG)
- [ ] Gut reaction is ruthless and specific
- [ ] 3 critical issues identified with fixes
- [ ] Master Context cross-checked for missed opportunities
- [ ] Revised resume generated via ResumeGenerator.js
- [ ] Output ≤ 200 words
- [ ] DOCX saved to ~/Downloads/

---

## Error Handling

| Error | Action |
|-------|--------|
| Resume not found | Ask for path, do not proceed |
| Master Context missing | Warn, proceed with limited cross-check |
| ResumeGenerator fails | Fall back to manual DOCX creation, warn user |

---

## Notes

- **Tone calibration**: This is not a feel-good exercise. The goal is to make the resume actually get interviews.
- **Master Context is truth**: If it's not in Master Context, it shouldn't be on the resume.
- **Brevity**: Long feedback = ignored feedback. Keep it tight.
