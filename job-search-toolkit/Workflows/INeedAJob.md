# INeedAJob — Career Context Interview

**The entrypoint to the entire job search toolkit. Interviews you to build comprehensive career context files that power all downstream workflows.**

---

## Overview

This workflow conducts an adaptive interview across 8 phases to extract your professional background, skills, achievements, and job search criteria. It then generates 6 structured context files that enable resume tailoring, cover letter generation, LinkedIn optimization, and more.

**Think of it as your career intake session.** Run this once, and every other workflow in the toolkit has what it needs.

---

## Triggers

| Trigger | Mode | Behavior |
|---------|------|----------|
| `/ineedajob` | **Full interview** | Complete 8-phase interview, generates all 6 context files |
| `/ineedajob update` | **Update mode** | Re-run specific phases to update existing context files |
| `/ineedajob quick` | **Quick mode** | Abbreviated 4-phase interview (identity + experience + skills + criteria) |
| "I need a job", "help me find a job", "set up my job search" | **Full interview** | Same as `/ineedajob` |

---

## Hard Constraints (NON-NEGOTIABLE)

| Rule | Constraint | Type |
|------|------------|------|
| 1 | ONLY use information the user explicitly provides | AUTHENTICITY |
| 2 | NEVER fabricate metrics, achievements, or experience | ZERO HALLUCINATION |
| 3 | Ask follow-up probes when answers lack specifics | DEPTH |
| 4 | Generate files in exact format downstream workflows expect | COMPATIBILITY |
| 5 | Each phase ≤ 5 questions (avoid survey fatigue) | UX |

**Conflict Priority**: Authenticity > Completeness > Speed

---

## Step 0: Setup

Before starting the interview:

1. **Ask where to save context files:**
   ```
   Where should I save your career context files?
   Default: ~/Career/CONTEXT/
   ```

2. **Check for existing context files** in that directory:
   - If found: offer to update specific files or start fresh
   - If not found: proceed with full interview

3. **Offer resume fast-track:**
   ```
   Do you have an existing resume I can start from?
   If yes: I'll extract what I can and only interview you on the gaps.
   If no: No problem — we'll build everything from scratch.
   ```

   If user provides a resume (PDF/DOCX path):
   - Extract: name, contact, work history, education, skills
   - Pre-populate interview phases with extracted data
   - Skip questions already answered by resume
   - Focus interview on gaps: achievements depth, honest gaps, interview stories, job criteria

---

## Phase 1: Identity & Current Status

**Goal:** Establish who you are and where you're at right now.

**Questions (ask all, adapt based on resume fast-track):**

1. **What's your full name and preferred contact info?** (email, phone, LinkedIn, location)
2. **What's your current professional status?** (employed and looking, between jobs, career change, new grad, returning to workforce)
3. **If currently employed:** What's your current role and company? What's prompting the search?
4. **If between jobs:** When did your last role end? What happened? (layoff, resignation, contract end — this helps frame the narrative)

**Follow-up probes (trigger if answers are thin):**
- "What city/region are you based in? Are you open to relocation?"
- "Do you have a LinkedIn profile URL?"

**Data captured → used in:** Professional Background - Index.md (header, status section)

---

## Phase 2: Career History

**Goal:** Build the complete career timeline with companies, roles, dates, and core responsibilities.

**Questions:**

1. **Walk me through your work history, starting from your most recent role.** For each position, I need:
   - Company name
   - Your title
   - Start and end dates (month/year)
   - Location (city, state — or remote)
   - 2-3 sentences on what you did / were responsible for

2. **What about education?** Degree(s), institution(s), graduation year(s), relevant coursework or honors.

3. **Any certifications, licenses, or professional development?** (PMP, AWS, CPA, bootcamps, etc.)

**Follow-up probes:**
- "You mentioned [Company] — what was the team size? Who did you report to?"
- "Were there any promotions or title changes during your time at [Company]?"
- "Any freelance, consulting, or side projects worth including?"

**Data captured → used in:** Professional Background - Index.md (career timeline), Experience Details.md (company breakdown)

---

## Phase 3: Achievements & Impact

**Goal:** Extract quantified accomplishments and impact stories for each role.

**Questions:**

1. **For each role you mentioned, what are you most proud of accomplishing?** I'm looking for specific outcomes — revenue generated, costs saved, time reduced, processes improved, teams built, problems solved.

2. **Can you give me 2-3 examples with numbers?** For example:
   - "Reduced report generation time from 4 hours to 15 minutes"
   - "Led migration of 50K customer records with zero downtime"
   - "Built onboarding process that cut ramp time by 40%"

3. **What's the biggest problem you solved at work?** Walk me through: what was broken, what you did, what happened as a result.

**Follow-up probes (CRITICAL — trigger if answers lack metrics):**
- "You said you 'improved the process' — by how much? What was it before and after?"
- "When you say 'managed a project' — what was the budget? Timeline? Team size? Outcome?"
- "That's a great story — can you put a number on the impact? Even an estimate helps."

**Data captured → used in:** Experience Details.md (achievement bullets), Interview Prep.md (STAR stories)

---

## Phase 4: Skills Inventory

**Goal:** Build a categorized skills inventory with honest proficiency levels.

**Questions:**

1. **What are your strongest technical skills?** (software, tools, languages, platforms, methodologies)

2. **What tools do you use daily vs. occasionally?** This helps me separate "expert" from "familiar with."

3. **What soft skills do people compliment you on?** (stakeholder management, communication, problem-solving, leadership, etc.)

4. **Any skills you're currently learning or want to develop?**

**Follow-up probes:**
- "You mentioned SQL — are we talking basic queries or complex joins/CTEs/stored procedures?"
- "When you say 'project management' — which methodologies? Agile, Scrum, Waterfall, SAFe?"
- "Any industry-specific tools? (Salesforce, Jira, SAP, Figma, etc.)"

**Data captured → used in:** Technical Skills.md (categorized inventory)

---

## Phase 5: Specialization & Domain Expertise

**Goal:** Identify the user's professional niche and signature projects.

**Questions:**

1. **If someone asked 'what do you specialize in?' — what would you say?** What's your professional niche or the thing you're known for?

2. **Tell me about your 2-3 most impressive projects.** What made them complex? What was your specific role? What was the outcome?

3. **What industries or domains do you have deep knowledge in?** (healthcare, fintech, e-commerce, manufacturing, SaaS, government, etc.)

**Follow-up probes:**
- "You mentioned [domain] — how many years? What specific sub-areas?"
- "For that project — what would have happened if you weren't on it?"
- "Is there a technical depth area where you know more than most people in your role?"

**Data captured → used in:** Specialization Profile.md

---

## Phase 6: Job Search Criteria

**Goal:** Define exactly what the user is looking for.

**Questions:**

1. **What job titles are you targeting?** (list 2-5 titles you'd apply to)

2. **What's your target compensation?** (salary range, total comp expectations — be realistic)

3. **What are your hard requirements?** (remote only, hybrid OK, specific cities, visa sponsorship needed, benefits must-haves)

4. **What industries or company types interest you?** (startup, enterprise, agency, nonprofit, specific sectors)

5. **What's a dealbreaker?** (things that would make you immediately pass on a role)

**Follow-up probes:**
- "When you say 'remote' — fully remote or remote with occasional travel?"
- "Is there a company size sweet spot? (10-person startup vs 10K-person enterprise)"
- "How important is title vs compensation vs work-life balance? Rank them."

**Data captured → used in:** Professional Background - Index.md (job criteria section)

---

## Phase 7: Honest Gaps

**Goal:** Identify limitations to ensure authenticity in all materials.

**Framing (important — set the tone):**
```
This part is about being honest with ourselves. The best job search materials
are authentic — they sell your real strengths without overclaiming.

I need to know what NOT to put on your resume. This keeps you out of
interviews where you'll get exposed, and into interviews where you'll shine.
```

**Questions:**

1. **Are there any skills on your resume that you'd be nervous getting quizzed on?** ("I list Python but I've only written basic scripts")

2. **Any experience claims that need qualification?** ("I say 'led a team' but it was 2 interns" — that's fine, I just need to know)

3. **What types of roles should you NOT apply to?** (roles that require skills you don't actually have)

4. **Any gaps in your resume that need explanation?** (career gaps, short stints, terminations — we'll frame these well, but I need the truth)

**Follow-up probes:**
- "If a hiring manager grilled you on [skill], how deep could you go?"
- "Is there anything you've been exaggerating that we should dial back?"

**Data captured → used in:** Honest Gaps.md

---

## Phase 8: Interview Stories & Soundbites

**Goal:** Build a bank of ready-to-use interview responses.

**Questions:**

1. **Give me a time you dealt with a difficult stakeholder or conflict at work.** (Behavioral: conflict resolution)

2. **Tell me about a time something went wrong and how you handled it.** (Behavioral: problem-solving under pressure)

3. **Why are you leaving your current/last role?** (Let's craft the right answer together — the real reason and the interview-ready version)

4. **What's your 30-second elevator pitch?** If you don't have one, I'll draft one based on everything you've told me.

5. **What questions do you always struggle with in interviews?** (I'll help prep answers)

**Follow-up probes:**
- "For that story — what was the specific result? How did the stakeholder react?"
- "Can you give me the STAR version? Situation, Task, Action, Result."

**Data captured → used in:** Interview Prep.md (STAR stories, soundbites, elevator pitch)

---

## Phase 9: Context File Generation

After all interview phases are complete, generate the 6 context files.

### Generation Rules

1. **Use ONLY information the user provided.** Never infer, embellish, or fabricate.
2. **Flag thin sections.** If a file has insufficient data, add a `<!-- NEEDS MORE DETAIL: [what's missing] -->` comment.
3. **Use exact filenames** that downstream workflows expect.
4. **Write files to the directory specified in Step 0.**

### File 1: Professional Background - Index.md

```markdown
# Professional Background — Index

## Quick Reference
- **Name:** [Full Name]
- **Email:** [Email]
- **Phone:** [Phone]
- **LinkedIn:** [URL]
- **Location:** [City, State]
- **Current Status:** [Employed/Searching/Career Change/etc.]

## Career Timeline

| Dates | Company | Role | Location |
|-------|---------|------|----------|
| [Most recent] | [Company] | [Title] | [City, ST] |
| ... | ... | ... | ... |

## Education

| Degree | Institution | Year | Notes |
|--------|-------------|------|-------|
| [Degree] | [School] | [Year] | [Honors/relevant coursework] |

## Certifications
- [Cert 1]
- [Cert 2]

## Target Roles
- [Title 1]
- [Title 2]
- [Title 3]

## Job Criteria
- **Compensation:** [Range]
- **Location:** [Remote/Hybrid/On-site preferences]
- **Industries:** [Preferred industries]
- **Company Size:** [Preference]
- **Dealbreakers:** [List]

## Positioning Statement
[2-3 sentence elevator pitch synthesized from interview]
```

### File 2: Experience Details.md

```markdown
# Experience Details

## [Company Name] | [Title] | [Dates]
**Location:** [City, ST or Remote]
**Reports to:** [If known]
**Team size:** [If known]

### Responsibilities
- [Core responsibility 1]
- [Core responsibility 2]

### Key Achievements
- [Achievement with metric]
- [Achievement with metric]
- [Achievement with metric]

### Context
[Any additional context: why they joined, why they left, what made this role unique]

---

## [Next Company] | [Title] | [Dates]
[Same structure repeated for each role]
```

### File 3: Specialization Profile.md

```markdown
# Specialization Profile

## Professional Niche
[1-2 paragraphs on what the user specializes in]

## Domain Expertise
| Domain | Depth | Years | Details |
|--------|-------|-------|---------|
| [Industry/Domain] | [Deep/Moderate/Familiar] | [Years] | [Specifics] |

## Signature Projects

### [Project Name/Description]
- **Context:** [What was the situation]
- **Role:** [User's specific contribution]
- **Complexity:** [What made it hard]
- **Outcome:** [Result with metrics if available]

### [Next Project]
[Same structure]

## Technical Depth Areas
- [Area 1]: [What sets user apart in this area]
- [Area 2]: [What sets user apart]
```

### File 4: Technical Skills.md

```markdown
# Technical Skills

## Skills by Category

### [Category 1: e.g., Programming Languages]
| Skill | Proficiency | Context |
|-------|------------|---------|
| [Skill] | [Expert/Proficient/Familiar] | [Where/how used] |

### [Category 2: e.g., Tools & Platforms]
| Skill | Proficiency | Context |
|-------|------------|---------|
| [Skill] | [Expert/Proficient/Familiar] | [Where/how used] |

### [Category 3: e.g., Methodologies]
- [Method 1] — [Context]
- [Method 2] — [Context]

## Soft Skills
- [Skill 1] — [Evidence/example]
- [Skill 2] — [Evidence/example]

## Currently Learning
- [Skill/topic]

## Role-Skill Mapping
| Target Role | Must-Have Skills | Nice-to-Have | Gaps to Address |
|-------------|-----------------|--------------|-----------------|
| [Role 1] | [Skills user has] | [Skills user has] | [Skills to develop] |
```

### File 5: Interview Prep.md

```markdown
# Interview Prep

## Elevator Pitch (30 seconds)
[Crafted from interview data]

## STAR Stories

### Story 1: [Title — e.g., "Conflict Resolution with VP Stakeholder"]
- **Situation:** [Context]
- **Task:** [What was needed]
- **Action:** [What user did specifically]
- **Result:** [Outcome with metric if available]
- **Best for:** [Which interview questions this answers]

### Story 2: [Title]
[Same STAR structure]

## Common Questions — Prepared Answers

### "Why are you leaving / did you leave your last role?"
[Interview-ready answer crafted from real reason]

### "Tell me about yourself"
[2-minute version of elevator pitch]

### "What's your biggest weakness?"
[Honest answer that shows self-awareness]

### [User-identified struggle questions]
[Prepared answers]

## Soundbites
- [Memorable 1-liner about their work]
- [Memorable 1-liner about their impact]
- [Memorable 1-liner about their approach]
```

### File 6: Honest Gaps.md

```markdown
# Honest Gaps

## Skills with Caveats

| Skill/Claim | Reality | Resume Implication |
|-------------|---------|-------------------|
| [Skill user listed] | [Actual proficiency] | [How to represent honestly] |
| [Experience claim] | [What actually happened] | [How to frame without overclaiming] |

## Roles to Avoid
- [Role type]: [Why — missing skills/experience]

## Resume Gaps
| Gap | Duration | Real Reason | Interview Frame |
|-----|----------|-------------|-----------------|
| [Date range] | [Length] | [Truth] | [How to explain positively] |

## Authenticity Rules
- Never claim: [Things user explicitly said not to claim]
- Qualify: [Things that need context/caveats]
- Safe to emphasize: [Things user is genuinely strong in]
```

---

## Post-Interview Summary

After generating all files, display:

```
═══════════════════════════════════════════════════
  CAREER CONTEXT COMPLETE
═══════════════════════════════════════════════════

  Files generated in [output directory]:

  ✅ Professional Background - Index.md
  ✅ Experience Details.md
  ✅ Specialization Profile.md
  ✅ Technical Skills.md
  ✅ Interview Prep.md
  ✅ Honest Gaps.md

  ⚠️  Thin sections (needs more detail):
  - [List any sections flagged with NEEDS MORE DETAIL]

  NEXT STEPS:
  1. Review the generated files and add any missing details
  2. "Search for [role] jobs" → JobBoardSearch
  3. "Tailor my resume for [company]" → ResumeTailoring
  4. "Optimize my LinkedIn" → LinkedInOptimizer

  Run /ineedajob update to re-interview specific sections.
═══════════════════════════════════════════════════
```

---

## Update Mode

When triggered with `/ineedajob update`:

1. Read existing context files
2. Ask: "Which area do you want to update?"
   - Professional background (role change, new contact info)
   - Experience (new role, updated achievements)
   - Skills (new skills, changed proficiency)
   - Specialization (new projects, domain shifts)
   - Job criteria (new target roles, salary change)
   - Honest gaps (new limitations, removed ones)
   - Interview prep (new stories, updated answers)
3. Run only the relevant phase(s)
4. Merge new data into existing files (don't overwrite untouched sections)

---

## Quick Mode

When triggered with `/ineedajob quick`:

Run only Phases 1, 2, 4, and 6 (Identity, Career History, Skills, Job Criteria).
Generate only:
- Professional Background - Index.md
- Experience Details.md (basic — responsibilities only, no deep achievements)
- Technical Skills.md

Print message: "Quick context created. Run `/ineedajob` for the full interview to unlock cover letters, interview prep, and LinkedIn optimization."
