---
name: LinkedInOptimizer
description: Generate optimized LinkedIn profile content section-by-section using resume data, target role context, and industry best practices. USE WHEN user wants to optimize LinkedIn profile, update LinkedIn headline, improve About section, write LinkedIn summary, generate LinkedIn content, OR tailor profile for job search. Produces ATS-friendly, keyword-optimized content. Integrates with job-search-toolkit for career context.
---

# LinkedIn Profile Optimizer

Optimize LinkedIn profiles section-by-section using resume data and career context. Generates keyword-optimized, authentic content that passes recruiter and hiring manager review.

## Workflow Overview

LinkedIn profile optimization involves these steps:

1. Load CONTEXT files (Professional Background, Experience Details, Honest Gaps)
2. Determine which sections to optimize (full profile, headline only, or about only)
3. Generate optimized content per section with character limits enforced
4. Run 3-persona quality review
5. Return copy-paste ready content with character counts

## Section-Specific Workflows

Determine the optimization scope based on user request:

| Trigger | Action | Reference Files |
|---------|--------|-----------------|
| "optimize my LinkedIn", "full LinkedIn profile" | Full profile (all sections) | All references |
| "LinkedIn headline", "headline options" | Headline only (3 variants) | `headline-frameworks.md`, `linkedin-limits.md` |
| "LinkedIn about", "LinkedIn summary" | About section only | `about-structure.md`, `content-rules.md` |
| "update my [section]" | Specific section update | Section-specific reference |

## Step 0: Load Profile Context (MANDATORY)

┌─────────────────────────────────────────────────────────────────┐
│  CRITICAL: LOAD CONTEXT FILES BEFORE OPTIMIZING ANY            │
│  LINKEDIN SECTIONS (HEADLINE, ABOUT, EXPERIENCE, SKILLS)       │
│                                                                 │
│  Context folder: ../job-search-toolkit/CONTEXT/                  │
│  (Shared with job-search-toolkit — context lives there)         │
│                                                                 │
│  1. Professional Background - Index.md (ALWAYS load first)     │
│     → Quick reference, career timeline, positioning            │
│                                                                 │
│  2. Experience Details.md                                       │
│     → Verifiable achievements and metrics                      │
│                                                                 │
│  3. Honest Gaps.md                                              │
│     → What NOT to overclaim in profile                         │
└─────────────────────────────────────────────────────────────────┘

**Read BEFORE any optimization from `../job-search-toolkit/CONTEXT/`:**

| File | Purpose | When Required |
|------|---------|---------------|
| **Professional Background - Index.md** | Entry point, always first | ALL workflows |
| **Experience Details.md** | Achievements with metrics | Profile optimization, headline |
| **Specialization Profile.md** | Key projects, domain expertise | For showcasing your specialization |
| **Technical Skills.md** | Skills inventory | Skills section optimization |
| **Honest Gaps.md** | Authenticity constraints | ALL workflows |

**CONTEXT File Loading by Section:**

| LinkedIn Section | CONTEXT Files Required |
|------------------|------------------------|
| Headline | Professional Background - Index.md, Technical Skills.md |
| About | Professional Background - Index.md, Experience Details.md, Specialization Profile.md |
| Experience | Experience Details.md, Honest Gaps.md |
| Skills | Technical Skills.md |
| Featured | Specialization Profile.md, Interview Prep.md |
| Recommendations | Interview Prep.md |

## Hard Constraints (NON-NEGOTIABLE)

┌─────────────────────────────────────────────────────────────────┐
│  CRITICAL: CHARACTER LIMITS ARE NON-NEGOTIABLE                  │
│                                                                 │
│  Headline: 220 chars (keywords in first 60)                     │
│  About: 2600 chars max (first 300 = hook + value prop)          │
│  Experience: 2000 chars per role                                │
│                                                                 │
│  Exceeding limits = content truncated by LinkedIn.              │
│  NO EXCEPTIONS. Verify counts before output.                    │
└─────────────────────────────────────────────────────────────────┘

| Rule | Constraint | Type |
|------|------------|------|
| 1 | Headline ≤ 220 characters | HARD CEILING |
| 2 | Keywords in first 60 chars of headline | SEO REQUIREMENT |
| 3 | About section 1800-2200 characters (max 2600) | RECOMMENDED RANGE |
| 4 | First 300 chars of About = hook + value prop | MOBILE VISIBILITY |
| 5 | Experience: 3-5 bullets per role | GUIDELINE |
| 6 | All claims verifiable in CONTEXT files | AUTHENTICITY |
| 7 | First-person voice throughout | VOICE |

**Conflict Priority**: Authenticity > Character limits > Keyword optimization > Variant count

## Detailed Reference Files

For detailed guidance on each section, see:

- **Character limits & platform rules**: [references/linkedin-limits.md](references/linkedin-limits.md)
- **Authenticity & keyword density**: [references/content-rules.md](references/content-rules.md)
- **Headline A/B/C frameworks**: [references/headline-frameworks.md](references/headline-frameworks.md)
- **About section structure**: [references/about-structure.md](references/about-structure.md)

## 3-Persona Quality Review (MANDATORY)

Run all 3 passes sequentially. Each pass has 3 binary (YES/NO) checks.

### Pass 1: Recruiter Quick Scan (5-second view)

| Check | Question |
|-------|----------|
| 1 | Headline immediately communicates value proposition? |
| 2 | Profile photo is professional and approachable? |
| 3 | About section hook works in first line? |

**If any NO**: Fix the specific issue, then continue to Pass 2.

### Pass 2: Hiring Manager Fit Check (30-second scroll)

| Check | Question |
|-------|----------|
| 1 | About section tells a coherent career story? |
| 2 | Experience entries show impact, not just duties? |
| 3 | Skills section aligns with target role keywords? |

**If any NO**: Identify which section fails and revise it.

### Pass 3: Authenticity Check (Skeptic Perspective)

| Check | Question |
|-------|----------|
| 1 | All claims verifiable in Experience Details.md / Honest Gaps.md? |
| 2 | No vague superlatives ("passionate", "driven leader")? |
| 3 | Metrics won't invite "prove it" challenges in interviews? |

**If any NO**: Remove unverifiable claim OR ground it in documented experience.

**Review Completion:**
- **All 9 checks pass** = Profile approved
- **Max iterations**: 3 per pass. If still failing after 3, flag for human review.

## Known Authenticity Constraints (DO NOT enhance)

<!-- CUSTOMIZE: Fill in your own authenticity constraints from your Honest Gaps file. -->
<!-- These prevent the optimizer from overclaiming in areas where your experience is limited. -->

| Claim Area | Reality | LinkedIn Implication |
|------------|---------|---------------------|
| [Skill/Project 1] | [Honest assessment of involvement] | [What NOT to claim on profile] |
| [Skill/Project 2] | [Honest assessment of proficiency] | [How to accurately represent it] |
| [Tool/Domain 3] | [Actual scope of experience] | [What NOT to overclaim] |
| [Management/Leadership] | [Actual scope, e.g., team size] | [Don't inflate title or scope] |

**Example entries (replace with your own):**

| Claim Area | Reality | LinkedIn Implication |
|------------|---------|---------------------|
| Python at [Previous Employer] | Minimal involvement, project stalled | Don't list "Python" as primary skill |
| SQL proficiency | Foundational from coursework | List as "SQL (Foundational)" not "Expert" |
| Enterprise CRM | Only used SMB tools | Don't claim "Enterprise CRM implementation" |
| Management scope | Led 3 junior analysts at [Consulting Firm] | Don't position as "Team Lead" or "Manager" |

## Error Handling

| Error | Action |
|-------|--------|
| Context files not found | Warn, request user to verify CONTEXT folder exists. Do not proceed without Professional Background - Index.md |
| Character limit impossible | Auto-trim with warning, prioritize by conflict priority chain |
| Conflicting optimization requirements | Apply conflict priority: Authenticity > Character limits > Keywords |
| Low keyword match for target role | Warn role may not be good fit, suggest alternative positioning |
| Honest Gaps violation detected | Remove claim, flag in output, explain what was removed and why |

## Output Format

Present optimized content in this copy-paste ready format:

```markdown
# LinkedIn Profile Optimization Results

**Target Role:** [Role from user or inferred]
**Generated:** [Timestamp]

---

## Headline (3 Options)

| Variant | Headline | Strategy | Chars |
|---------|----------|----------|-------|
| A | [text] | Keyword-optimized | X/220 |
| B | [text] | Achievement-led | X/220 |
| C | [text] | Value-focused | X/220 |

**Recommendation:** [Which to use and why]

---

## About Section (X/2,600 chars)

[Full About section text]

**First 300 chars preview:**
> [Mobile-visible portion]

---

## Experience

### [Company Name] | [Title] | [Dates]
- [Bullet 1 with metric]
- [Bullet 2 with metric]
- [Bullet 3]
- [Bullet 4]

---

## Skills (X skills)

**Top 3 (Pin These):**
1. [Skill 1]
2. [Skill 2]
3. [Skill 3]

**Additional Skills:**
- [Skill 4]
- [Skill 5]

---

## All-Star Status Checklist

- [ ] Photo uploaded
- [ ] Headline: [Status]
- [ ] About: [Status]
- [ ] Experience (2+ needed): [Count]
- [ ] Skills (5+ needed): [Count]
- [ ] Education: [Status]
- [ ] 50+ connections

---

## Quality Review

### Recruiter Quick Scan
[Pass/Fail with notes]

### Hiring Manager Review
[Pass/Fail with notes]

### Authenticity Check
[Pass/Fail with notes]
```

## Quality Checklist (Pre-Output)

Before returning LinkedIn content:

- [ ] Headline ≤ 220 chars with keywords in first 60
- [ ] About section 1800-2200 chars with hook in first 300
- [ ] First-person voice throughout
- [ ] All claims verifiable in CONTEXT files
- [ ] 3 headline variants provided (if full profile)
- [ ] All 9 quality checks pass
- [ ] Character counts displayed for each section
- [ ] No generic phrases ("passionate", "team player", "results-driven")

## Integration with job-search-toolkit

This skill complements the job-search-toolkit for complete application materials:

| Material | Skill |
|----------|-------|
| Resume (DOCX) | job-search-toolkit/ResumeTailoring |
| Cover Letter | job-search-toolkit/CoverLetterGenerator |
| **LinkedIn Profile** | LinkedInOptimizer |

**Typical workflow:**
1. Use ResumeTailoring for ATS-optimized resume
2. Use LinkedInOptimizer to align LinkedIn profile with resume
3. Ensure consistent messaging across materials

## Examples

### Example 1: Full Profile Optimization

**User:** "Optimize my LinkedIn for AI Implementation roles"

**Action:**
1. Load CONTEXT files (Professional Background, Experience Details, Technical Skills, Honest Gaps)
2. Extract target role keywords: "AI Implementation", "Automation", "Operations"
3. Generate 3 headline variants with different strategies
4. Write About section with hook in first 300 chars
5. Format Experience with 3-5 bullets per role
6. Run 3-persona quality review
7. Return formatted output with character counts

### Example 2: Headline Only

**User:** "Give me some LinkedIn headline options"

**Action:**
1. Load Professional Background - Index.md and Technical Skills.md
2. Identify current positioning and target roles
3. Generate 3 variants: Keyword-optimized, Achievement-led, Value-focused
4. Verify all within 220 chars with keywords in first 60
5. Return variants with character counts and recommendation

### Example 3: Between Jobs Scenario

**User:** "Update my LinkedIn - I'm currently job searching"

**Action:**
1. Recognize "between jobs" scenario from context
2. Use alternative headline patterns (no current company)
3. Position entrepreneurship period as operational experience
4. Frame positively without overclaiming
5. Emphasize target role keywords for discoverability
