# CoverLetterGenerator Workflow v2.0

**ATS-optimized cover letter generation tailored to job requirements and company research.**

---

## Hard Constraints (NON-NEGOTIABLE)

| Rule | Constraint | Type |
|------|------------|------|
| 1 | 250-400 words | LENGTH |
| 2 | 3-4 paragraphs | STRUCTURE |
| 3 | Company name in first paragraph | SPECIFICITY |
| 4 | Keyword coverage 70-85% | TARGET RANGE |
| 5 | All claims verifiable in Professional Background | AUTHENTICITY |

**Conflict Priority**: Authenticity > Word limit > Keyword coverage

---

## Input Requirements

| Parameter | Required | Source |
|-----------|----------|--------|
| Job URL or Parsed Data | Yes | JobDescriptionParser output or direct URL |
| User Profile | Yes | Auto-loaded from resume + Professional Background |
| Company Research | No | WebSearch or user-provided |

---

## Step 0: Auto-Load Career Context (MANDATORY)

**Read BEFORE any generation from `CONTEXT/` (relative to skill root):**
1. **Professional Background - Index.md** (always first)
2. **Experience Details.md** - For achievements with metrics
3. **Specialization Profile.md** - For domain expertise and key project stories
4. **Honest Gaps.md** - For what NOT to oversell

Extract:
- Specific achievements with metrics
- Stories that match job requirements
- Technical skills inventory
- Honest gaps (what NOT to oversell)

---

## Step 1: Input Processing

1. **Parse job description** (if URL provided, call JobDescriptionParser)
2. **Extract keywords** by category (required vs preferred)
3. **Auto-load resume** from Career folder
4. **Select strategy** based on experience level:
   - < 3 years: early-career
   - Industry/role change: career-transition
   - Director+ level: executive
   - Technical role: technical-specialist
   - Default: achievement-focused

---

## Step 2: Company Research

Use WebSearch to gather:
- Mission/values
- Recent news (2026)
- Cultural indicators
- Strategic initiatives

**If WebSearch fails**: Note `[Company research unavailable]` in output metadata. Use generic company language.

---

## Step 3: Match Experience to Requirements

1. **Extract keywords** from job requirements
2. **Map achievements** to requirements (prioritize with metrics)
3. **Select top 3-5 achievements** that:
   - Contain most job keywords
   - Have quantifiable metrics
   - Are recent (last 3-5 years)
4. **Calculate initial keyword coverage** (target: 70-85%)

---

## Step 4: Generate Cover Letter

### Structure

1. **Opening (50-60 words, 2-3 sentences)**
   - State the role and company
   - One compelling hook about your fit
   - Years of experience + achievement theme

2. **Body 1 (110-130 words, 3-4 sentences)**
   - Lead with top achievement + metric
   - Include 2-3 required skills with context
   - Connect to job responsibility

3. **Body 2 (70-80 words, 2-3 sentences)**
   - Reference company research (mission, initiative)
   - Connect your background to company need
   - Show cultural alignment

4. **Closing (50 words, 2-3 sentences)**
   - Restate key skills
   - Thank them
   - Call to action

5. **Signature**
   ```
   Sincerely,
   {User Name}
   ```

---

## Step 5: ATS Optimization

1. **Keyword enrichment** - Target 70-85% coverage
2. **Formatting validation**:
   - [ ] No tables or graphics
   - [ ] Standard font (Calibri/Arial 11-12pt)
   - [ ] Acronyms spelled out on first use
3. **Length validation** - Trim if > 400 words

---

## Step 6: 3-Persona Quality Review (MANDATORY)

Run all 3 passes sequentially. Each pass has 3 binary (YES/NO) checks.

### Pass 1: Recruiter Quick Check

| Check | Question |
|-------|----------|
| 1 | Opening hook is compelling (not "I am writing to apply")? |
| 2 | Company name and role mentioned in first paragraph? |
| 3 | Visually scannable (3-4 short paragraphs, no walls of text)? |

**If any NO**: Fix the specific issue, then continue to Pass 2.

### Pass 2: Hiring Manager Fit Check

| Check | Question |
|-------|----------|
| 1 | 2-3 role requirements addressed with specific examples? |
| 2 | Shows knowledge of company (not generic filler)? |
| 3 | Clear call to action in closing? |

**If any NO**: Identify which section fails and revise it.

### Pass 3: Authenticity Check

| Check | Question |
|-------|----------|
| 1 | All claims verifiable in Professional Background? |
| 2 | Specific achievements (not vague superlatives)? |
| 3 | Tone matches applicant's voice (not AI-written)? |

**If any NO**: Remove unverifiable claim OR ground it in documented experience.

### Review Completion

- **All 9 checks pass** = Cover letter approved
- **Max iterations**: 3 per pass. If still failing, flag for human review.

---

## Step 7: Generate DOCX Output

**File naming**: `FirstName_LastName_CoverLetter_CompanyName.docx`
**Output location**: `Output/` (relative to skill root)

**DOCX file contains ONLY the cover letter text** (no metadata).

---

## Output Format

```json
{
  "workflow": "CoverLetterGenerator",
  "version": "2.0",
  "job_info": {
    "title": "...",
    "company": "...",
    "url": "..."
  },
  "cover_letter": {
    "word_count": 328,
    "paragraph_count": 4,
    "keyword_coverage": 0.82
  },
  "quality_review": {
    "recruiter": {
      "compelling_hook": "PASS",
      "company_mentioned": "PASS",
      "visually_scannable": "PASS"
    },
    "hiring_manager": {
      "requirements_addressed": "PASS",
      "company_knowledge": "PASS",
      "call_to_action": "PASS"
    },
    "authenticity": {
      "claims_verifiable": "PASS",
      "specific_achievements": "PASS",
      "natural_voice": "PASS"
    }
  },
  "constraints_enforced": {
    "word_limit": true,
    "paragraph_count": true,
    "company_mentioned": true,
    "keyword_range": true,
    "authenticity": true
  },
  "company_research": {
    "success": true,
    "mission": "...",
    "recent_news": ["..."]
  },
  "file_generated": "Output/FirstName_LastName_CoverLetter_Company.docx",
  "timestamp": "2026-01-15T00:00:00Z"
}
```

---

## Error Handling

### Insufficient User Profile
Block generation if missing: name, email, or experience. Request user input.

### Low Keyword Coverage (<50%)
Warn user role may not be a good fit. Allow override with honesty disclaimer.

### Company Research Failed
Proceed with generic company paragraph. Warn user to customize before submission.

### Word Count Violation
If > 400 words after generation, auto-trim to 375-390 words. If still over, warn user.

---

## Quality Checklist (Pre-Output)

Before returning cover letter:

- [ ] Word count 250-400
- [ ] 3-4 paragraphs
- [ ] Keyword coverage ≥ 70%
- [ ] ≥ 2 quantifiable achievements
- [ ] Company name mentioned
- [ ] No generic phrases ("passionate", "team player")
- [ ] All 9 quality checks pass
- [ ] DOCX file generated

---

## Notes

- **Keyword target**: 70-85% (not 100%). Natural language > keyword stuffing.
- **Company research**: Optional but improves quality. Fallback to generic is acceptable.
- **Word count sweet spot**: 300-350 words for most roles.
- **Authenticity**: Only claim what's documented. Never fabricate.
