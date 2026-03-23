# Job Search Skills for Claude Code

> The open-source, privacy-first job search system for Claude Code. Run `/ineedajob`, answer questions about your career, and get tailored resumes, cover letters, and LinkedIn content — all on your machine.

Two Claude Code skills that automate the job search process end-to-end: from discovering roles and tailoring resumes to optimizing your LinkedIn profile.

## Quick Start

```
/ineedajob
```

That's it. The `/ineedajob` workflow interviews you about your career, skills, and goals, then generates all the context files that power every other workflow. No manual setup required.

## See It In Action

Browse a complete example to see what the skill pack produces — no setup required:

**Meet Alex Chen** — 6 years experience, targeting remote Product Operations roles.

| What | File | Description |
|------|------|-------------|
| **Career Context** | [`examples/alex-chen/`](examples/alex-chen/) | All 6 context files generated from the `/ineedajob` interview |
| **Honest Gaps** | [`Honest Gaps.md`](examples/alex-chen/Honest%20Gaps.md) | The authenticity constraints that keep the system honest |
| **Job Posting** | [`job-posting.md`](examples/alex-chen/job-posting.md) | A Product Operations Manager role at Acme Corp |
| **Tailored Resume** | [`output/Alex_Chen_Resume_Acme_Corp.md`](examples/alex-chen/output/Alex_Chen_Resume_Acme_Corp.md) | ATS-optimized resume tailored to the Acme Corp JD |
| **Cover Letter** | [`output/Alex_Chen_CoverLetter_Acme_Corp.md`](examples/alex-chen/output/Alex_Chen_CoverLetter_Acme_Corp.md) | Targeted cover letter with real achievements |
| **LinkedIn Profile** | [`output/linkedin-profile.md`](examples/alex-chen/output/linkedin-profile.md) | Optimized headline, about section, and skills |

Notice how the resume and cover letter reference real metrics from Alex's experience — but never overclaim. The Honest Gaps file ensures "Python scripting" doesn't become "Python developer" and "led 4-person ops team" doesn't become "senior engineering leader."

## Skills Included

### 1. Job Search Toolkit (`job-search-toolkit/`)

Automated job discovery, resume tailoring, and application material generation.

**Workflows:**
- **INeedAJob** — **START HERE** — Career intake interview that generates all context files
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

Run `/ineedajob` and the interview workflow will create all 6 context files for you automatically:

| File | Purpose |
|------|---------|
| `Professional Background - Index.md` | Quick reference: career timeline, target roles, job criteria |
| `Experience Details.md` | Company-by-company breakdown with metrics and achievements |
| `Specialization Profile.md` | Key projects, domain expertise, and problem-solving stories |
| `Technical Skills.md` | Skills inventory and proficiency levels |
| `Interview Prep.md` | STAR stories, soundbites, behavioral examples |
| `Honest Gaps.md` | Limitations and what NOT to overclaim |

Or create them manually — place context files in `job-search-toolkit/CONTEXT/` (the skill's self-contained context directory). No external path configuration needed.

### 3. Configure your resume template

Place your base resume as a `.docx` file at `job-search-toolkit/Templates/resume-template.docx`. This keeps the skill fully self-contained.

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
# First time? Start here:
/ineedajob                    # Full career interview (recommended)
/ineedajob quick              # Abbreviated version (4 phases)
/ineedajob update             # Update existing context files

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
/ineedajob (START HERE)
    │
    ▼
Career Context Files (6 files generated from interview)
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

## Roadmap

- **Interview Simulator** — Practice interviews with AI playing the hiring manager, using your job description and context files. Get feedback on answers, test your STAR stories, and prep for the questions your Honest Gaps file says you're weakest on.
- **Application Tracker** — Track which jobs you've applied to, interview stages, and follow-ups.

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- Web search capability (for job discovery and company research)
- Python 3.10+ and/or Node.js 18+ (for programmatic generators)

## License

MIT

---

*Examples generated from commit `39aa0ce`.*
