# BespokeApplicationGenerator Workflow

**End-to-end batch application generation: Job discovery → Verification → Fit Scoring → Application Materials**

## Objective

Generate complete, ready-to-submit application packages for multiple jobs in a single command:
- Find jobs matching user criteria across multiple job boards
- Verify each job meets quality standards (remote, active, recent)
- Calculate fit scores and rank by match quality
- Generate tailored resume, cover letter, and hiring manager outreach for top N jobs
- Package all materials into organized folder structure

## Trigger Phrases

- "batch applications"
- "bespoke applications"
- "prepare applications"
- "full application packages"
- "generate applications for X roles"
- "find me N roles and prepare bespoke applications"

## Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| **job_criteria** | Yes | - | Job title/role type to search for |
| **location** | No | "Remote" | Geographic preference |
| **salary_min** | No | - | Minimum salary threshold |
| **top_n_applications** | No | 5 | Number of top jobs to generate materials for |
| **job_boards** | No | All 4 | Which boards to search: LinkedIn, Indeed, Glassdoor, Built In |

**Minimum Required:**
- Job criteria (title, keywords, or role type)

---

## Step-by-Step Process

### Phase 1: Job Discovery

**Step 1.1: Execute JobBoardSearch**

Search 4 job boards in parallel using WebSearch:

```
Search Query: "{job_criteria} {location} jobs"

Boards:
- LinkedIn Jobs: site:linkedin.com/jobs
- Indeed: site:indeed.com
- Glassdoor: site:glassdoor.com/job-listing
- Built In: site:builtin.com/job
```

**Target:** 50-100 raw job results

**Step 1.2: Execute JobVerification (MANDATORY)**

All jobs MUST pass these 4 checks:

| Check | Validation | Fail Action |
|-------|------------|-------------|
| Remote Status | Job description contains "remote" without "hybrid" qualifiers | EXCLUDE |
| URL Active | HTTP 200 response from job URL | EXCLUDE |
| Job Exists | Page contains job posting content, not "expired" or "no longer available" | EXCLUDE |
| Recency | Posted within last 21 days | EXCLUDE |

**Target:** 30-50 verified jobs

**Step 1.3: Auto-Trigger HiringManagerResearch**

For each verified job:
- Search LinkedIn for hiring manager (VP/Director level in relevant department)
- Extract LinkedIn profile URL
- Infer email address using common patterns
- Draft personalized outreach email (150-200 words)

---

### Phase 2: Fit Scoring & Selection

**Step 2.1: Parse Job Requirements**

For each verified job, invoke JobDescriptionParser to extract:

```json
{
  "required": {
    "experience_years": 5,
    "technical_skills": ["SQL", "Agile", "SDLC"],
    "soft_skills": ["stakeholder management"],
    "education": "Bachelor's degree",
    "domain": "Healthcare preferred"
  },
  "preferred": {
    "technical_skills": ["Python", "Tableau"],
    "certifications": ["CBAP"]
  }
}
```

**Step 2.2: Calculate Fit Scores**

**MANDATORY:** Read user profile from `CONTEXT/` (relative to skill root):
- Professional Background - Index.md (always first)
- Experience Details.md (for experience verification)
- Technical Skills.md (for skills matching)

Apply 5-component weighted formula:

| Component | Weight | Calculation |
|-----------|--------|-------------|
| **Core Requirements** | 40% | % of required skills/experience user meets |
| **Experience Level** | 20% | User years / Required years (capped at 100%) |
| **Technical Skills** | 20% | % of required tools/platforms user has |
| **Domain/Industry** | 10% | Direct (100%), Adjacent (70%), Transferable (40%), None (0%) |
| **Education** | 10% | Exceeds (100%), Meets (80%), Close (60%), Gap (30%) |

**Fit Score = (Core × 0.4) + (Experience × 0.2) + (Technical × 0.2) + (Domain × 0.1) + (Education × 0.1)**

**Score Interpretation:**

| Range | Priority | Recommendation |
|-------|----------|----------------|
| 9.0-10.0 | URGENT | Apply immediately |
| 7.5-8.9 | HIGH | Apply within 24-48 hours |
| 6.0-7.4 | MODERATE | Apply if interested, address gaps |
| 4.5-5.9 | LOW | Apply if willing to stretch |
| Below 4.5 | SKIP | Unless exceptional circumstances |

**Step 2.3: Select Top N Jobs**

Rank jobs by fit score (descending), then by:
1. Recency (newer is better)
2. Salary alignment (if specified)
3. Source credibility (Built In > LinkedIn > Indeed > Glassdoor)

Select top N jobs for application generation.

---

### Phase 3: Application Generation (Sequential)

**CRITICAL:** Process jobs sequentially to ensure reliability. Parallel processing can cause rate limits and inconsistent output.

For each top-N job:

**Step 3.1: Generate Tailored Resume**

Invoke ResumeTailoring workflow:
- Auto-load base resume from Career folder
- Reorder skills section (most relevant first)
- Enhance experience bullets with job keywords
- Update professional summary for role fit
- Target: 75-85% keyword match

**Output:** `Output/BespokeApplications_YYYYMMDD_HHMMSS/XX_Company_Role/Your_Name_Resume_Company.docx`

**Step 3.2: Generate Cover Letter**

Invoke CoverLetterGenerator workflow:
- Auto-load resume for context
- Research company (WebSearch)
- Match 70-90% of job keywords
- Include measurable achievements
- Target: ATS score 85+/100

**Output:** `Output/BespokeApplications_YYYYMMDD_HHMMSS/XX_Company_Role/Your_Name_CoverLetter_Company.docx`

**Step 3.3: Format Hiring Manager Outreach**

Create markdown file with:
- Contact name and LinkedIn URL
- Inferred email address
- Personalized outreach email (from HiringManagerResearch)
- Alternative contact strategies if primary unknown

**Output:** `Output/BespokeApplications_YYYYMMDD_HHMMSS/XX_Company_Role/hiring_manager_outreach.md`

**Step 3.4: Generate Job Metadata**

Create JSON with complete job information:

```json
{
  "job_title": "Business Systems Analyst III",
  "company": "Velera",
  "url": "https://builtin.com/job/...",
  "posted_date": "2026-01-05",
  "source": "Built In",
  "fit_score": 8.4,
  "fit_breakdown": {
    "core_requirements": 85,
    "experience": 100,
    "technical_skills": 75,
    "domain": 70,
    "education": 100
  },
  "salary_range": "$85K-$108K",
  "hiring_manager": {
    "name": "John Smith",
    "title": "VP of Engineering",
    "linkedin": "https://linkedin.com/in/johnsmith",
    "email": "john.smith@velera.com"
  },
  "materials_generated": {
    "resume": "Your_Name_Resume_Velera.docx",
    "cover_letter": "Your_Name_CoverLetter_Velera.docx",
    "outreach": "hiring_manager_outreach.md"
  },
  "keyword_match": {
    "resume": "83%",
    "cover_letter": "91%"
  },
  "ats_scores": {
    "resume": 89,
    "cover_letter": 94
  }
}
```

**Output:** `Output/BespokeApplications_YYYYMMDD_HHMMSS/XX_Company_Role/job_metadata.json`

---

### Phase 4: Package Output

**Step 4.1: Create Folder Structure**

```bash
mkdir -p Output/BespokeApplications_YYYYMMDD_HHMMSS/
```

**Step 4.2: Organize by Company**

Folders are numbered by fit score rank:

```
Output/BespokeApplications_20260112_143022/
├── SUMMARY.md
├── batch_metadata.json
├── all_verified_jobs.json
│
├── 01_Velera_BSA_III/
│   ├── Your_Name_Resume_Velera.docx
│   ├── Your_Name_CoverLetter_Velera.docx
│   ├── hiring_manager_outreach.md
│   └── job_metadata.json
│
├── 02_Absorb_Software_Sales_Ops_Analyst/
│   ├── Your_Name_Resume_Absorb_Software.docx
│   ├── Your_Name_CoverLetter_Absorb_Software.docx
│   ├── hiring_manager_outreach.md
│   └── job_metadata.json
│
└── 03_HubSpot_Operations_Analyst/
    ├── Your_Name_Resume_HubSpot.docx
    ├── Your_Name_CoverLetter_HubSpot.docx
    ├── hiring_manager_outreach.md
    └── job_metadata.json
```

**Step 4.3: Generate SUMMARY.md**

Create executive summary with results table:

```markdown
# Bespoke Application Batch - 2026-01-12

## Search Criteria
- **Role:** Business Systems Analyst
- **Location:** Remote
- **Applications Generated:** 5

## Results

| Rank | Company | Role | Fit Score | ATS (Resume) | ATS (Letter) | Status |
|------|---------|------|-----------|--------------|--------------|--------|
| 1 | Velera | BSA III | 8.4 | 89 | 94 | Ready |
| 2 | Absorb Software | Sales Ops Analyst | 8.1 | 91 | 88 | Ready |
| 3 | HubSpot | Operations Analyst | 7.8 | 87 | 92 | Ready |
| 4 | Samsara | Sr. Systems Analyst | 7.5 | 85 | 89 | Ready |
| 5 | Stripe | Revenue Operations | 7.3 | 88 | 86 | Ready |

## Quick Actions

Each folder contains:
- `*_Resume_*.docx` - Upload to ATS/application portal
- `*_CoverLetter_*.docx` - Upload where requested
- `hiring_manager_outreach.md` - Send via LinkedIn/email after applying

## Statistics
- **Jobs Discovered:** 87
- **Jobs Verified:** 42
- **Average Fit Score:** 7.8
- **Average ATS Score:** 88.6
```

**Step 4.4: Generate batch_metadata.json**

```json
{
  "generated_at": "2026-01-12T14:30:22Z",
  "search_criteria": {
    "job_criteria": "Business Systems Analyst",
    "location": "Remote",
    "salary_min": null
  },
  "statistics": {
    "jobs_discovered": 87,
    "jobs_verified": 42,
    "applications_generated": 5,
    "average_fit_score": 7.82,
    "average_ats_score": 88.6
  },
  "top_jobs": [
    // Array of job_metadata objects
  ]
}
```

---

## Error Handling

| Error | Strategy | User Message |
|-------|----------|--------------|
| Job board search fails | Retry once, partial results | "Found 35 jobs (Indeed unavailable)" |
| Resume tailoring fails | Skip job, continue batch | "Skipped Job 3 (see error_log.txt)" |
| Cover letter fails | Generate resume-only | "Job 2: Resume only (cover letter failed)" |
| Hiring manager not found | Use placeholder | "Hiring Manager: [Department Head]" |
| URL verification timeout | Skip job | "Job excluded: URL verification timeout" |

**Error Log:** `Output/BespokeApplications_YYYYMMDD_HHMMSS/error_log.txt`

---

## Performance Targets

| Phase | Target Time | Notes |
|-------|-------------|-------|
| Job Discovery | ~2 min | 4 parallel WebSearches |
| Verification | ~1 min | Batch processing |
| Fit Scoring | ~30 sec | Agent reasoning |
| Application Gen | ~45 sec/job | Sequential for reliability |
| **Total (5 apps)** | **~7-8 min** | End-to-end |

---

## Example Usage

**Basic:**
```
User: "Find me 5 remote BSA roles and prepare bespoke applications"
```

**With criteria:**
```
User: "Search for remote Revenue Operations Manager roles paying $90k+ and generate full application packages for top 3"
```

**Specific boards:**
```
User: "Search LinkedIn and Built In for Implementation Manager roles and prepare applications for top 10"
```

---

## Dependencies

**Existing Workflows (No Changes):**
- `JobBoardSearch.md` - Multi-board job discovery
- `JobVerification.md` - 4-check validation
- `HiringManagerResearch.md` - Contact research
- `JobDescriptionParser.md` - Requirements extraction
- `ResumeTailoring.md` - ATS-optimized resume generation
- `CoverLetterGenerator.md` - Cover letter generation

**Required Files:**
- `CONTEXT/` folder (relative to skill root) - Career context files (Index, Experience Details, Technical Skills, Honest Gaps)
- Template DOCX at `Templates/resume-template.docx` (relative to skill root)

---

## Output Return

After completion, return:

1. **Summary statement:** "Generated 5 bespoke application packages for remote BSA roles"
2. **Folder path:** `Output/BespokeApplications_20260112_143022/`
3. **Quick stats:** Jobs found, verified, average fit score
4. **Next actions:** "Open SUMMARY.md for application checklist"
