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
│  skills, summary, and titles for Kavalier/Vicegerent.           │
│                                                                 │
│  LOCKED ORDER (enforced automatically):                         │
│  1. Kavalier Coaching | Chicago, IL      (Sep 2024 - Dec 2025)  │
│  2. Vicegerent Custom Clothing | Chicago (Jun 2022 - Sep 2024)  │
│  3. Oliver Wyman | Chicago, IL           (Mar 2022 - Jun 2022)  │
│  4. Deloitte Consulting LLP | Chicago    (Oct 2020 - Mar 2022)  │
│                                                                 │
│  ✓ OK: Customize titles for Kavalier & Vicegerent               │
│  ✓ OK: Reorder BULLETS within a single job                      │
│  ✓ OK: Customize SKILLS categories                              │
│  ✗ LOCKED: Company names, locations, dates                      │
│  ✗ LOCKED: Oliver Wyman title ("Senior Consultant")             │
│  ✗ LOCKED: Deloitte title ("Business Technology Analyst")       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Generator Schema (Locked vs Dynamic Fields)

The `ResumeGenerator.js` enforces immutable fields at code level. Only provide dynamic fields in input JSON.

| Category | Field | Status |
|----------|-------|--------|
| Header | Name, contact info | LOCKED |
| Jobs | Company names | LOCKED: Kavalier Coaching, Vicegerent Custom Clothing, Oliver Wyman, Deloitte Consulting LLP |
| Jobs | Locations | LOCKED: All Chicago, IL |
| Jobs | Dates | LOCKED: Sep 2024-Dec 2025, Jun 2022-Sep 2024, Mar 2022-Jun 2022, Oct 2020-Mar 2022 |
| Jobs | Oliver Wyman title | LOCKED: "Senior Consultant" |
| Jobs | Deloitte title | LOCKED: "Business Technology Analyst" |
| Jobs | Kavalier title | **DYNAMIC** via `titles.kavalier` |
| Jobs | Vicegerent title | **DYNAMIC** via `titles.vicegerent` |
| Education | Degree info | LOCKED: Northwestern University, B.S. Computer Science, 2017-2020 |
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

Load these files from `04 - Career/CONTEXT/`:
1. **Professional Background - Index.md** (always first)
2. **Experience Details.md** - For verifiable achievements and metrics
3. **Technical Skills.md** - For skills inventory and resume tailoring notes
4. **Honest Gaps.md** - For authenticity constraints

**DO NOT extract or modify locked fields** (header, company names, locations, dates, Oliver Wyman/Deloitte titles) - these are enforced by the generator.

**Focus extraction on DYNAMIC fields only:**
- Verifiable achievements for bullet crafting
- Skills inventory for skills section
- Summary patterns to adapt
- Titles for Kavalier & Vicegerent (customize per job posting)

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
Kavalier Coaching (Sep 2024 - Dec 2025)           ← Title is DYNAMIC
• [Most relevant bullet to job posting]           ← Bullets reordered within this job
• [Second most relevant bullet]

Vicegerent Custom Clothing (Jun 2022 - Sep 2024)  ← Title is DYNAMIC
• [Bullets reordered within this job]

Oliver Wyman (Mar 2022 - Jun 2022)                ← Title LOCKED: "Senior Consultant"
• [Bullets reordered within this job]

Deloitte Consulting LLP (Oct 2020 - Mar 2022)     ← Title LOCKED: "Business Technology Analyst"
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
    "kavalier": "Founder & SaaS Implementation Lead",
    "vicegerent": "Business Operations & Technology Analyst"
  },
  "bullets": [
    ["Kavalier bullet 1...", "Kavalier bullet 2...", "Kavalier bullet 3..."],
    ["Vicegerent bullet 1...", "Vicegerent bullet 2...", "Vicegerent bullet 3..."],
    ["Oliver Wyman bullet 1...", "Oliver Wyman bullet 2..."],
    ["Deloitte bullet 1...", "Deloitte bullet 2...", "Deloitte bullet 3...", "Deloitte bullet 4..."]
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
node ~/.claude/skills/JobSearchToolkit/Templates/ResumeGenerator.js /tmp/resume_data.json "CompanyName"
```

3. Verify one page (if needed):
```bash
python ~/.claude/skills/JobSearchToolkit/Tools/verify_page_count.py ~/Downloads/Idrees_Kamal_Resume_Company.docx
```

**File naming**: `Idrees_Kamal_Resume_CompanyName.docx`
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

| Claim Area | Reality |
|------------|---------|
| Oliver Wyman Python work | Minimal involvement, project stalled |
| SQL proficiency | Foundational from coursework, not production |
| Enterprise CRM | Only SMB tools (Notion, GoHighLevel) |
| Management scope | Limited to 3 junior BAs at Deloitte |

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
- [ ] `titles.kavalier` and `titles.vicegerent` provided and appropriate for role
- [ ] Keyword match ≥ 75%
- [ ] ATS formatting compliant
- [ ] Exactly 1 page
- [ ] All 9 quality checks pass
- [ ] ≥ 2 bullets per job
- [ ] All claims verifiable
- [ ] DOCX file generated: `Idrees_Kamal_Resume_CompanyName.docx`

---

## Notes

- **Keyword target**: 75-85% (not 100%). Natural language > keyword stuffing.
- **Authenticity**: Only add skills with evidence. Never fabricate.
- **ATS 2026**: DOCX format, single-column, standard fonts, acronyms expanded.
- **Human recruiters**: Lead with metrics, quantify achievements, show impact.
