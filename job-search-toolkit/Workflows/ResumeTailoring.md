# ResumeTailoring Workflow v2.0

**ATS-optimized resume customization tailored to specific job requirements.**

---

## Hard Constraints (NON-NEGOTIABLE)

| Rule | Constraint | Type |
|------|------------|------|
| 1 | Minimum 2 bullets per job | HARD FLOOR |
| 2 | Maximum 1 page | HARD CEILING |
| 3 | Keyword coverage 75-85% | TARGET RANGE |
| 4 | All claims verifiable in Professional Background | AUTHENTICITY |
| 5 | Use ResumeGenerator.js for DOCX generation | TOOLING |
| 6 | **Jobs in reverse chronological order (most recent first)** | ORDERING |

**Conflict Priority**: Authenticity > Chronological Order > Page limit > Keyword coverage

```
┌─────────────────────────────────────────────────────────────────┐
│  CHRONOLOGICAL ORDER IS ENFORCED BY GENERATOR                   │
│                                                                 │
│  The ResumeGenerator.js hardcodes job order. You cannot change  │
│  company names, locations, dates, or order - only bullets,      │
│  skills, summary, and titles for jobs 1 & 2.                    │
│                                                                 │
│  LOCKED ORDER (enforced automatically - CUSTOMIZE in            │
│  ResumeGenerator.js LOCKED_RESUME_DATA):                        │
│  1. Company A | City, ST        (most recent dates)             │
│  2. Company B | City, ST        (previous dates)                │
│  3. Company C | City, ST        (earlier dates)                 │
│  4. Company D | City, ST        (earliest dates)                │
│                                                                 │
│  ✓ OK: Customize titles for Jobs 1 & 2 (dynamic titles)        │
│  ✓ OK: Reorder BULLETS within a single job                      │
│  ✓ OK: Customize SKILLS categories                              │
│  ✗ LOCKED: Company names, locations, dates                      │
│  ✗ LOCKED: Job 3 title (set in LOCKED_RESUME_DATA)              │
│  ✗ LOCKED: Job 4 title (set in LOCKED_RESUME_DATA)              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Generator Schema (Locked vs Dynamic Fields)

The `ResumeGenerator.js` enforces immutable fields at code level. Only provide dynamic fields in input JSON.

| Category | Field | Status |
|----------|-------|--------|
| Header | Name, contact info | LOCKED (set in `ResumeGenerator.js` LOCKED_RESUME_DATA) |
| Jobs | Company names | LOCKED (set in LOCKED_RESUME_DATA) |
| Jobs | Locations | LOCKED (set in LOCKED_RESUME_DATA) |
| Jobs | Dates | LOCKED (set in LOCKED_RESUME_DATA) |
| Jobs | Job 3 title | LOCKED (set in LOCKED_RESUME_DATA) |
| Jobs | Job 4 title | LOCKED (set in LOCKED_RESUME_DATA) |
| Jobs | Job 1 title | **DYNAMIC** via `titles.job1` |
| Jobs | Job 2 title | **DYNAMIC** via `titles.job2` |
| Education | Degree info | LOCKED (set in LOCKED_RESUME_DATA) |
| Content | professional_title | **DYNAMIC** |
| Content | summary | **DYNAMIC** |
| Content | skills | **DYNAMIC** |
| Content | bullets (4 arrays) | **DYNAMIC** |

---

## Input Requirements

| Parameter | Required | Source |
|-----------|----------|--------|
| Job URL or Parsed Data | Yes | JobDescriptionParser output or direct URL |
| User Resume | Yes | Auto-loaded from Career folder |
| Target Match Rate | No | Default: 75-85% |

---

## Step 0: Load Career Context Files

Load these files from `~/Career/CONTEXT/`:
1. **Professional Background - Index.md** (always first)
2. **Experience Details.md** - For verifiable achievements and metrics
3. **Technical Skills.md** - For skills inventory and resume tailoring notes
4. **Honest Gaps.md** - For authenticity constraints

**DO NOT extract or modify locked fields** (header, company names, locations, dates, locked job titles) - these are enforced by the generator.

**Focus extraction on DYNAMIC fields only:**
- Verifiable achievements for bullet crafting
- Skills inventory for skills section
- Summary patterns to adapt
- Titles for Job 1 & Job 2 (customize per job posting)

> **Generator:** Use `ResumeGenerator.js` with JSON containing only dynamic fields. Locked fields are injected automatically.

---

## Step 1: Parse Job & Extract Keywords

1. **Parse job description** (if URL provided, call JobDescriptionParser)
2. **Extract keywords** by category:
   - Required: technical_skills, soft_skills, tools, methodologies, domain
   - Preferred: technical_skills, certifications
3. **Calculate current match rate**:
   - Count matched required keywords
   - Identify missing keywords

---

## Step 2: Select Tailoring Strategy

| Match Rate | Strategy | Actions |
|------------|----------|---------|
| < 60% | Aggressive | Add 10-15 keywords, reorder all sections, rewrite summary |
| 60-75% | Standard | Add 5-10 keywords, reorder skills, adjust 3-5 bullets |
| > 75% | Light | Add 2-5 keywords, reorder skills only |

---

## Step 3: Reorder Sections

**What CAN be reordered:**
1. **Skills categories**: Move job-relevant skill categories to top (score by keyword match)
2. **Bullets WITHIN a single job**: Reorder bullets to put most relevant achievements first

**What CANNOT be reordered:**
- ❌ **Job entries**: Jobs MUST remain in reverse chronological order (most recent first)
- ❌ **Education entries**: Must remain in reverse chronological order
- ❌ **Certification entries**: Must remain in chronological or relevance order

**Example of correct bullet reordering:**

```
Company A (Sep 2024 - Dec 2025)           ← Title is DYNAMIC
• [Most relevant bullet to job posting]           ← Bullets reordered within this job
• [Second most relevant bullet]

Company B (Jun 2022 - Sep 2024)  ← Title is DYNAMIC
• [Bullets reordered within this job]

Consulting Firm (Mar 2022 - Jun 2022)                ← Title LOCKED: "Senior Consultant"
• [Bullets reordered within this job]

Enterprise Corp (Oct 2020 - Mar 2022)     ← Title LOCKED: "Business Technology Analyst"
• [Bullets reordered within this job]
```

---

## Step 4: Add Missing Keywords (Authentically)

**CRITICAL**: Only add keywords that appear in experience bullets or Professional Background.

1. **Skills section**: Add missing skills IF mentioned elsewhere in resume
2. **Experience bullets**: Enhance existing bullets with missing keywords naturally
3. **Summary**: Rewrite to include top 5-7 job keywords

**Example enhancement:**
- Original: "Built a CRM system and migrated 700+ client records"
- Job requires: "data migration", "data governance", "CRM automation"
- Enhanced: "Implemented CRM automation and led data migration of 700+ client records, establishing data governance rules"

---

## Step 5: ATS Formatting Validation

Ensure resume passes these checks:
- [ ] Single-column layout (no tables)
- [ ] Standard fonts (Arial, Calibri 11-12pt)
- [ ] No graphics/images
- [ ] Standard section headings ("Work Experience", "Education", "Skills")
- [ ] Acronyms expanded on first use
- [ ] Jobs in reverse chronological order (ENFORCED BY GENERATOR - automatic)

---

## Step 6: Calculate Final Match Rate

Recalculate keyword match after tailoring:
- Required match %
- Preferred match %
- Overall match %
- Improvement from original

---

## Step 7: Generate DOCX from Spec

Prepare input JSON with **ONLY dynamic fields** (locked fields are injected automatically):

```json
{
  "professional_title": "Senior Implementation Consultant",
  "summary": "Results-driven professional with 4+ years...",
  "skills": {
    "Technical": ["Python", "SQL", "Tableau"],
    "Business": ["Process Optimization", "Stakeholder Management"]
  },
  "titles": {
    "job1": "Founder & SaaS Implementation Lead",
    "job2": "Business Operations & Technology Analyst"
  },
  "bullets": [
    ["Company A bullet 1...", "Company A bullet 2...", "Company A bullet 3..."],
    ["Company B bullet 1...", "Company B bullet 2...", "Company B bullet 3..."],
    ["Consulting Firm bullet 1...", "Consulting Firm bullet 2..."],
    ["Enterprise Corp bullet 1...", "Enterprise Corp bullet 2...", "Enterprise Corp bullet 3...", "Enterprise Corp bullet 4..."]
  ]
}
```

**CRITICAL**: Do NOT include header, company names, locations, dates, or locked titles - these are enforced by the generator and will be ignored.

1. Write JSON to temp file:
```bash
cat > /tmp/resume_data.json << 'EOF'
{ ... }
EOF
```

2. Generate DOCX:
```bash
node ./Templates/ResumeGenerator.js /tmp/resume_data.json "CompanyName"
```

3. Verify one page (if needed):
```bash
python ./Tools/verify_page_count.py ~/Downloads/Your_Name_Resume_Company.docx
```

**File naming**: `Your_Name_Resume_CompanyName.docx`
**Output location**: `~/Downloads/`

---

## Step 8: 3-Persona Quality Review (MANDATORY)

Run all 3 passes sequentially. Each pass has 3 binary (YES/NO) checks.

### Pass 1: Recruiter Quick Check (6-second scan)

| Check | Question |
|-------|----------|
| 1 | Header and contact info readable at a glance? |
| 2 | Top 1/3 of page shows strongest, most relevant achievements? |
| 3 | Clean visual breaks, no walls of text? |

**If any NO**: Fix the specific issue, then continue to Pass 2.

### Pass 2: Hiring Manager Fit Check (2-minute read)

| Check | Question |
|-------|----------|
| 1 | Career story flows logically (no unexplained jumps)? |
| 2 | Achievements clearly map to role requirements? |
| 3 | Based on this resume alone, would you interview this person? |

**If any NO**: Identify which bullet/section fails and revise it.

### Pass 3: Authenticity Check (skeptic perspective)

| Check | Question |
|-------|----------|
| 1 | All claims verifiable in Experience Details.md / Honest Gaps.md? |
| 2 | Specific details (not generic AI-written filler)? |
| 3 | No metrics that would invite "prove it" challenges? |

**If any NO**: Remove unverifiable claim OR ground it in documented experience.

### Review Completion

- **All 9 checks pass** = Resume approved
- **Max iterations**: 3 per pass. If still failing after 3, flag for human review.

### Known Authenticity Constraints (DO NOT enhance)

**CUSTOMIZE:** Fill in your own authenticity constraints below. These prevent the system from overselling areas where your experience is limited.

| Claim Area | Reality |
|------------|---------|
| [Skill/tool X] | [Actual proficiency level - e.g., "Foundational from coursework, not production"] |
| [Technology Y] | [Honest assessment - e.g., "Used briefly on one project"] |
| [Domain Z] | [Real scope - e.g., "Only SMB tools, not enterprise platforms"] |
| [Leadership claim] | [True scope - e.g., "Led 2-person team, not department-level"] |

---

## One-Page Enforcement

**ALWAYS start with FULL content. Only reduce if PDF verification shows > 1 page.**

### Process

1. Generate with ALL content (all bullets, full summary, all skill categories)
2. Verify page count: `python verify_page_count.py <resume.docx>`
3. If > 1 page, reduce ONE item at a time:
   - Condense ONE long bullet (>180 chars → 150 chars)
   - Remove ONE lowest-keyword-match bullet (min 2 per job)
   - Condense summary (min 2 sentences)
   - Reduce skill categories (min 4)
4. Re-verify. Repeat until exactly 1 page.

**Max iterations**: 10. If still > 1 page, warn user.

### Minimum Thresholds (NEVER reduce below)

| Element | Minimum |
|---------|---------|
| Bullets per job | 2 |
| Summary sentences | 2 |
| Skill categories | 4 |

---

## Output Format

```json
{
  "workflow": "ResumeTailoring",
  "version": "2.0",
  "job_info": {
    "title": "...",
    "company": "...",
    "url": "..."
  },
  "match_analysis": {
    "original_match": 0.67,
    "final_match": 0.83,
    "improvement": 0.16,
    "keywords_added": ["...", "..."]
  },
  "quality_review": {
    "recruiter": {
      "header_readable": "PASS",
      "top_third_strong": "PASS",
      "visual_clarity": "PASS"
    },
    "hiring_manager": {
      "story_flows": "PASS",
      "achievements_mapped": "PASS",
      "would_interview": "PASS"
    },
    "authenticity": {
      "claims_verifiable": "PASS",
      "specific_details": "PASS",
      "no_inflated_metrics": "PASS"
    }
  },
  "constraints_enforced": {
    "min_bullets": true,
    "max_pages": true,
    "keyword_range": true,
    "authenticity": true,
    "resume_generator": true
  },
  "file_generated": "~/Downloads/FirstName_LastName_Resume_Company.docx",
  "timestamp": "2026-01-15T00:00:00Z"
}
```

---

## Error Handling

### Resume Not Found
Block tailoring, request user to provide path or save resume to Career folder.

### Low Initial Match (<50%)
Warn user role may not be a good fit. Allow override with honesty disclaimer.

### Cannot Add Required Keywords
Warn which keywords cannot be added authentically. Recommend transferable skills or learning path.

---

## Quality Checklist (Pre-Output)

Before returning tailored resume:

- [ ] Jobs in reverse chronological order (ENFORCED BY GENERATOR - automatic)
- [ ] Input JSON contains only dynamic fields (no locked fields)
- [ ] `titles.job1` and `titles.job2` provided and appropriate for role
- [ ] Keyword match ≥ 75%
- [ ] ATS formatting compliant
- [ ] Exactly 1 page
- [ ] All 9 quality checks pass
- [ ] ≥ 2 bullets per job
- [ ] All claims verifiable
- [ ] DOCX file generated: `Your_Name_Resume_CompanyName.docx`

---

## Notes

- **Keyword target**: 75-85% (not 100%). Natural language > keyword stuffing.
- **Authenticity**: Only add skills with evidence. Never fabricate.
- **ATS 2026**: DOCX format, single-column, standard fonts, acronyms expanded.
- **Human recruiters**: Lead with metrics, quantify achievements, show impact.
