---
name: job-search-toolkit
description: Job search automation toolkit for discovering roles, analyzing job requirements, and tailoring application materials. USE WHEN user needs to search job boards, parse job descriptions, extract requirements, tailor resumes, review resumes, OR generate cover letters. Integrates with job-search-specialist agent.
---

# JobSearchToolkit

**Automated job discovery and requirement analysis for strategic job searching.**

This skill provides tools to automate the job search process, from discovering relevant positions across major job boards to extracting and structuring job requirements for fit score calculation.

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **INeedAJob** | `/ineedajob`, "I need a job", "set up my job search", "help me find a job" | `Workflows/INeedAJob.md` (**START HERE** — interviews you and creates all career context files) |
| **JobBoardSearch** | "search jobs", "find positions", "job boards" | `Workflows/JobBoardSearch.md` |
| **JobDescriptionParser** | "parse job description", "extract requirements", "analyze posting" | `Workflows/JobDescriptionParser.md` |
| **JobVerification** | MANDATORY after any job discovery | `Workflows/JobVerification.md` |
| **HiringManagerResearch** | AUTOMATIC after JobBoardSearch | `Workflows/HiringManagerResearch.md` (Finds hiring managers, LinkedIn, email, drafts outreach) |
| **CoverLetterGenerator** | "cover letter", "write cover letter", "generate letter", "application letter" | `Workflows/CoverLetterGenerator.md` (AUTO-LOADS resume from Career folder) |
| **ResumeTailoring** | "tailor resume", "customize resume", "optimize resume", "ATS resume" | `Workflows/ResumeTailoring.md` (AUTO-LOADS resume, reorders sections, adds keywords, outputs ATS-optimized DOCX) |
| **BespokeApplicationGenerator** | "batch applications", "bespoke applications", "prepare applications", "full application packages", "generate applications" | `Workflows/BespokeApplicationGenerator.md` (Orchestrates job discovery → verification → fit scoring → batch resume/cover letter generation) |
| **BatchAssetGenerator** | "batch generate assets", "generate all application materials", "create resumes for not applied jobs", "generate assets for [Company]" | `Workflows/BatchAssetGenerator.md` (Generates resume + cover letter for all "Not Applied" jobs in tracker, parallel processing, checkpoint recovery) |
| **ResumeReviewer** | "review resume", "critique resume", "review my resume for [Company]" | `Workflows/ResumeReviewer.md` (Ruthless hiring manager critique, cross-checks Master Context, outputs revised .docx) |

---

## MANDATORY GUARDRAIL: Job Verification

```
┌─────────────────────────────────────────────────────────────────┐
│  CRITICAL: ALL JOBS MUST BE VERIFIED BEFORE OUTPUT             │
│                                                                 │
│  Every job found MUST pass these 4 checks:                      │
│                                                                 │
│  1. REMOTE STATUS  - Confirm job is fully remote (not hybrid)  │
│  2. URL ACTIVE     - HTTP 200 response (not 404/403/410)       │
│  3. JOB EXISTS     - Posting is live (not expired/filled)      │
│  4. RECENCY        - Posted within last 21 days (3 weeks)      │
│                                                                 │
│  Jobs failing ANY check are EXCLUDED from results.             │
│  NO EXCEPTIONS. See Workflows/JobVerification.md for details.  │
└─────────────────────────────────────────────────────────────────┘
```

**Enforcement:** JobVerification workflow is automatically invoked after JobBoardSearch completes. Only verified jobs appear in final output.

---

## MANDATORY GUARDRAIL: One-Page Resume Limit

```
┌─────────────────────────────────────────────────────────────────┐
│  CRITICAL: ALL RESUMES MUST FIT ON A SINGLE PAGE                │
│                                                                 │
│  Enforced through adaptive reduction algorithm:                 │
│                                                                 │
│  ROUND 1: CONDENSE (preserve quantity)                          │
│  - Shorten bullets >150 chars to 120-150 chars                 │
│  - Condense summary to 2 sentences                             │
│                                                                 │
│  ROUND 2: REDUCE (only if condensing insufficient)             │
│  - Remove lowest-keyword-match bullets (2 min per job)         │
│  - Merge skill categories (4 minimum)                          │
│                                                                 │
│  ROUND 3: MARGINS (last resort)                                │
│  - Reduce from 1" → 0.5" (minimum)                             │
│                                                                 │
│  See Workflows/ResumeTailoring.md for full algorithm.          │
└─────────────────────────────────────────────────────────────────┘
```

**Enforcement:** `enforce_one_page()` is automatically called in `generate_resume_from_template()`. Stats logged in `_one_page_stats` field.

---

## Integration with job-search-specialist

This toolkit is designed to work alongside the `job-search-specialist` agent:

- **JobSearchToolkit** handles automated data collection and parsing
- **job-search-specialist** agent provides strategic guidance, fit scoring, and application materials

**Typical workflow:**
1. Use JobSearchToolkit to find and parse job postings
2. AUTOMATIC: Research hiring managers, LinkedIn profiles, emails, and draft outreach emails
3. Agent calculates fit scores from parsed requirements
4. Use ResumeTailoring to create ATS-optimized resumes for top matches
5. Use CoverLetterGenerator to create tailored cover letters
6. Apply with tailored resume + cover letter + hiring manager outreach

---

## MANDATORY: Career Context Files

```
┌─────────────────────────────────────────────────────────────────┐
│  CRITICAL: LOAD CONTEXT FILES BEFORE CREATING ANY              │
│  RESUMES, COVER LETTERS, OR APPLICATION MATERIALS              │
│                                                                 │
│  Context folder: CONTEXT/  (inside this skill directory)         │
│  (/ineedajob generates these files automatically)               │
│                                                                 │
│  Files:                                                         │
│  1. Professional Background - Index.md (ALWAYS load first)     │
│     → Quick reference, career timeline, job criteria           │
│                                                                 │
│  2. Experience Details.md                                       │
│     → Detailed company experience, cross-functional work       │
│                                                                 │
│  3. Specialization Profile.md                                   │
│     → Domain expertise, key projects, technical depth          │
│                                                                 │
│  4. Technical Skills.md                                         │
│     → Skills inventory, role recommendations, resume notes     │
│                                                                 │
│  5. Interview Prep.md                                           │
│     → Stories, soundbites, soft skills                         │
│                                                                 │
│  6. Honest Gaps.md                                              │
│     → Limitations, what NOT to oversell                        │
└─────────────────────────────────────────────────────────────────┘
```

**How to use context files:**

| Workflow | Files to Load |
|----------|---------------|
| **ResumeTailoring** | Index + Experience Details + Technical Skills + Honest Gaps |
| **CoverLetterGenerator** | Index + Experience Details + Specialization Profile |
| **FitScoreCalculation** | Index + Technical Skills + Experience Details |
| **HiringManagerOutreach** | Index + Specialization Profile + Interview Prep |
| **ResumeReviewer** | Index + Experience Details + Honest Gaps |
| **Interview Prep** | Index + Interview Prep + Honest Gaps |

**File purposes:**
- `Professional Background - Index.md` - Entry point, always load first
- `Experience Details.md` - Company-by-company breakdown, metrics
- `Specialization Profile.md` - Domain expertise, key projects, problem-solving stories
- `Technical Skills.md` - Skills inventory, role recommendations
- `Interview Prep.md` - Soundbites, STAR stories, behavioral examples
- `Honest Gaps.md` - Limitations, authenticity constraints

## Examples

**Example 1: Automated job discovery**
```
User: "Search for remote Business Systems Analyst roles paying $80k+"
→ Invokes JobBoardSearch workflow
→ Searches LinkedIn, Indeed, Glassdoor, Built In
→ Returns structured list with URLs, salaries, requirements
```

**Example 2: Requirement extraction**
```
User: "Parse this job description and extract the requirements"
→ Invokes JobDescriptionParser workflow
→ Separates required vs preferred qualifications
→ Categorizes skills, experience, education, domain knowledge
→ Returns structured data for fit score calculation
```

**Example 3: End-to-end automation**
```
User: "Find BSA roles in healthcare and calculate my fit scores"
→ JobBoardSearch finds relevant positions
→ JobDescriptionParser extracts requirements from each
→ job-search-specialist agent calculates fit scores
→ Returns ranked list with fit score breakdowns
```

**Example 4: Hiring manager research (AUTOMATIC)**
```
User: "Find me 50 Business Systems Analyst jobs"
→ JobBoardSearch finds 50 positions
→ AUTOMATIC: HiringManagerResearch workflow triggers
→ For each job: searches LinkedIn for hiring manager (VP/Director level)
→ Finds LinkedIn profile URLs
→ Infers email addresses using common patterns
→ Drafts personalized outreach email (150-200 words, includes job posting URL, references role & experience)
→ Returns all data in Excel with 14 columns including hiring manager info
```

**Example 5: Generate cover letter**
```
User: "Generate a cover letter for the Velera BSA role"
→ Invokes CoverLetterGenerator workflow
→ AUTO-LOADS user resume from Career folder (extracts contact info, experience, skills)
→ Parses job requirements (or uses cached parse)
→ Researches company using WebSearch
→ Generates ATS-optimized letter using REAL achievements from resume
→ Returns markdown + DOCX + PDF formats
→ Provides ATS score (target: 85+/100) and keyword coverage analysis
```

**Example 6: Tailor resume for specific job**
```
User: "Tailor my resume for this Absorb Software Sales Operations Analyst role"
→ Invokes ResumeTailoring workflow
→ AUTO-LOADS user resume from Career folder
→ Parses job requirements (or uses cached parse)
→ Analyzes keyword match: Current 67% → Target 75-85%
→ Reorders skills section (most relevant first)
→ Enhances experience bullets with missing keywords
→ Updates professional summary with job-specific keywords
→ Final match: 83% (+16 percentage points improvement)
→ Generates ATS-optimized DOCX: ~/Downloads/Your_Name_Resume_Absorb_Software.docx
→ Provides ATS score (91/100), keyword analysis, and honesty report
```

## Output Format

### JobBoardSearch Output (with Hiring Manager Research)
```json
{
  "jobs": [
    {
      "title": "Business Systems Analyst III",
      "company": "Company Name",
      "location": "Remote",
      "salary": "$85K-$108K",
      "posted_date": "2026-01-05",
      "source": "Built In",
      "url": "https://...",
      "raw_requirements": "5+ years experience, SQL, Agile...",
      "hiring_manager": "John Smith",
      "linkedin_url": "https://linkedin.com/in/johnsmith",
      "email": "john.smith@company.com",
      "draft_email": "Subject: Business Systems Analyst Role...\n\nHi John,\n\nI'm reaching out about the Business Systems Analyst III position at Company Name (https://...). [Personalized email body with achievements and value proposition]"
    }
  ]
}
```

### JobDescriptionParser Output
```json
{
  "title": "Business Systems Analyst III",
  "company": "Company Name",
  "requirements": {
    "required": {
      "experience_years": 5,
      "technical_skills": ["SQL", "Agile", "SDLC"],
      "soft_skills": ["stakeholder management", "communication"],
      "education": "Bachelor's degree in related field",
      "domain": "Healthcare IT experience preferred"
    },
    "preferred": {
      "technical_skills": ["Python", "Tableau"],
      "certifications": ["CBAP"]
    }
  }
}
```

### CoverLetterGenerator Output
```json
{
  "job_info": {
    "title": "Business Systems Analyst III",
    "company": "Velera",
    "url": "https://builtin.com/job/..."
  },
  "cover_letter": {
    "content_markdown": "[Full formatted cover letter]",
    "word_count": 328,
    "strategy_used": "achievement-focused"
  },
  "validation": {
    "keyword_coverage": 0.82,
    "ats_score": 94,
    "keywords_used": ["SQL", "Agile", "SDLC", "stakeholder management", "..."],
    "keywords_missing": ["CBAP"]
  },
  "files_generated": {
    "markdown": "Your_Name_CoverLetter_Velera.md",
    "docx": "Your_Name_CoverLetter_Velera.docx",
    "pdf": "Your_Name_CoverLetter_Velera.pdf"
  },
  "company_research": {
    "mission": "Transform credit union technology",
    "recent_news": ["Q4 2025 expansion"],
    "cultural_indicators": ["collaborative", "innovation-focused"]
  }
}
```

## Technical Details

### Data Sources
- LinkedIn Jobs API (via web search)
- Indeed (web scraping)
- Glassdoor (web scraping)
- Built In (web scraping)
- Company career pages (direct URLs)

### Parsing Strategy
- Keyword extraction for technical skills
- Regex patterns for experience requirements
- NLP for categorizing soft skills
- Salary range normalization
- Date parsing and recency scoring

---

## Template Files

**ResumeTailoring uses a deterministic template to ensure formatting consistency.**

### Template Locations

The system auto-searches for template files in these locations:

1. `~/Downloads/Your_Name_Resume.docx`
2. `CONTEXT/` (any .docx file, relative to skill root)

**Note:** "Template" refers to the universal structure and formatting specification. Content is dynamic based on job description.

### Template Structure

The template defines the exact formatting for all generated resumes:

| Section | Font | Size | Alignment | Spacing |
|---------|------|------|-----------|---------|
| Name | Arial Bold | 34pt (17pt) | Centered | 0 before |
| Contact | Arial Regular | 20pt (10pt) | Centered | ~33pt before |
| Title | Arial Bold | 24pt (12pt) | Centered | ~77pt before |
| Section Headers | Arial Bold | 22pt (11pt) | Left | ~77pt before (first), ~12pt (subsequent) |
| Company Name | Arial Bold | 20pt (10pt) | Left | ~43pt before (first), ~25pt (subsequent) |
| Job Title/Dates | Arial Regular | 19pt (9.5pt) | Left | 0 before |
| Body Text | Arial Regular | 19pt (9.5pt) | Left | Variable |
| Summary | Arial Regular | 19pt (9.5pt) | Justified | ~77pt before |

**Bullet Points:**
- Format: Numbered list (● filled circle)
- Left indent: 720 twips (0.5")
- Hanging indent: 360 twips (0.25")
- Line spacing: ~228pt
- Each experience entry uses separate numId to keep bullets independent

**Skills Section:**
- Dynamic categories based on job requirements
- Formatting pattern: **Bold category:** regular skills list
- Common patterns:
  - Business Analyst: Requirements, Process, Delivery, Data, Tools
  - Product Manager: Product Skills, Technical Skills, Tools & Platforms, Methodologies
  - Data Analyst: Technical Skills, Tools & Technologies, Statistical Methods, Domain Expertise
  - Software Engineer: Programming Languages, Frameworks & Libraries, Tools & Platforms, Methodologies

### Template-Based Generation

**Method:** Unpack → Replace content → Repack

**Advantages:**
- 100% formatting consistency across all generated resumes
- Preserves exact spacing, fonts, indents from template
- No manual font/style configuration needed
- Deterministic output - same input always produces identical formatting

**Implementation:**
Uses `Templates/TemplateProcessor.py` module with Document library (OOXML) for safe XML manipulation.

**File Output:**
- Filename format: `FirstName_LastName_Resume_CompanyName.docx`
- Location: `~/Downloads/`
- Example: `Your_Name_Resume_Absorb_Software.docx`

---
