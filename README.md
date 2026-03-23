# Job Search Skills for Claude Code

Two Claude Code skills that automate the job search process end-to-end: from discovering roles and tailoring resumes to optimizing your LinkedIn profile.

## Skills Included

### 1. Job Search Toolkit (`job-search-toolkit/`)

Automated job discovery, resume tailoring, and application material generation.

**Workflows:**
- **JobBoardSearch** — Search LinkedIn, Indeed, Glassdoor, Built In for roles matching your criteria
- **JobDescriptionParser** — Extract and structure requirements from any job posting
- **JobVerification** — Validate postings are live, remote, and recent (mandatory guardrail)
- **HiringManagerResearch** — Find hiring managers, LinkedIn profiles, emails, and draft outreach
- **ResumeTailoring** — Generate ATS-optimized, one-page DOCX resumes tailored to specific roles
- **CoverLetterGenerator** — Create targeted cover letters with company research
- **BespokeApplicationGenerator** — End-to-end batch: discover jobs, verify, score fit, generate materials
- **BatchAssetGenerator** — Generate resume + cover letter for all unapplied jobs in your tracker
- **ResumeReviewer** — Ruthless hiring manager critique with revised output

### 2. LinkedIn Optimizer (`LinkedInOptimizer/`)

Section-by-section LinkedIn profile optimization with keyword targeting and quality review.

**Features:**
- 3-variant headline generation (keyword-optimized, achievement-led, value-focused)
- About section with mobile-optimized hook in first 300 chars
- Character limit enforcement (220 headline, 2600 about, 2000 per experience)
- 3-persona quality review: Recruiter Quick Scan, Hiring Manager Fit Check, Authenticity Check
- All-Star status checklist

## Setup

### 1. Install the skills

Copy both skill directories into your Claude Code skills folder:

```bash
# Clone this repo
git clone https://github.com/ikamal97/job-search-skills.git

# Copy skills to Claude Code
cp -r job-search-skills/job-search-toolkit ~/.claude/skills/
cp -r job-search-skills/LinkedInOptimizer ~/.claude/skills/
```

### 2. Create your Career Context

Both skills rely on career context files to generate accurate, personalized materials. Create a `CONTEXT/` folder in your career directory with these files:

| File | Purpose |
|------|---------|
| `Professional Background - Index.md` | Quick reference: career timeline, target roles, job criteria |
| `Experience Details.md` | Company-by-company breakdown with metrics and achievements |
| `Specialization Profile.md` | Key projects, domain expertise, and problem-solving stories |
| `Technical Skills.md` | Skills inventory and proficiency levels |
| `Interview Prep.md` | STAR stories, soundbites, behavioral examples |
| `Honest Gaps.md` | Limitations and what NOT to overclaim |

Update the context folder path in `job-search-toolkit/SKILL.md` and `LinkedInOptimizer/SKILL.md` to match your setup.

### 3. Configure your resume template

Place your base resume as a `.docx` file in `~/Downloads/` or your career folder. Update the template path in `job-search-toolkit/SKILL.md` under "Template Locations".

### 4. Install template dependencies (optional)

If you want to use the programmatic resume/cover letter generators:

```bash
cd job-search-toolkit/Templates
npm install    # For JS-based generators
pip install python-docx  # For Python-based generators
```

## Usage

Once installed, use natural language with Claude Code:

```
# Job Search
"Search for remote Product Manager roles paying $120k+"
"Parse this job description and calculate my fit score"
"Tailor my resume for this Stripe PM role"
"Generate a cover letter for the HubSpot position"
"Review my resume for this role — be ruthless"

# LinkedIn
"Optimize my LinkedIn for AI Product Manager roles"
"Give me 3 headline options"
"Rewrite my About section"
```

## Customization

### Authenticity Constraints

The LinkedInOptimizer includes an authenticity check system. Edit the "Known Authenticity Constraints" table in `LinkedInOptimizer/SKILL.md` with your own limitations — things you should NOT overclaim on your profile.

### Job Search Criteria

Edit `job-search-toolkit/SKILL.md` to customize:
- Default job verification rules (remote-only, recency window)
- Resume template formatting specs
- Output file naming conventions

## How It Works

```
User Request
    │
    ├─► JobBoardSearch ──► JobVerification ──► HiringManagerResearch
    │                                              │
    │                                              ▼
    │                                    Verified Jobs + Contacts
    │
    ├─► ResumeTailoring ──► ATS-Optimized DOCX (one page)
    │
    ├─► CoverLetterGenerator ──► Targeted Cover Letter
    │
    └─► LinkedInOptimizer ──► Optimized Profile Content
```

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- Web search capability (for job discovery and company research)
- Python 3.10+ and/or Node.js 18+ (for programmatic generators)

## License

MIT
