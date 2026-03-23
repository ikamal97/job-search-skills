# BatchAssetGenerator Workflow

**Purpose:** Generate tailored resumes and cover letters for all "Not Applied" jobs in the tracker, with parallel processing and checkpoint recovery.

---

## Triggers

| Mode | Trigger Phrases |
|------|-----------------|
| **Single** | "generate assets for [Company]", "create resume for [Company] job" |
| **Batch** | "batch generate assets", "generate all application materials", "create resumes for not applied jobs" |

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. LOAD: Glob Job Applications/*.md                        │
│  2. FILTER: status == "Not Applied"                         │
│  3. SORT: By role-category (clustering) or date-sourced     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  PARALLEL BATCH (3-5 jobs concurrent)                       │
│                                                              │
│  For each job:                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  PARALLEL per job:                                      │ │
│  │  ├─ Task: ResumeTailoring → DOCX                       │ │
│  │  └─ Task: CoverLetterGenerator → DOCX                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                              │                               │
│                              ▼                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  POST-PROCESS:                                          │ │
│  │  1. Move DOCX to vault (Generated Assets/[Company]/)   │ │
│  │  2. Update frontmatter (resume-path, cover-letter-path)│ │
│  │  3. Save checkpoint                                     │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Execution

### Step 1: Load and Filter Jobs

```
1. Glob: ~/Career/Job Applications/*.md
2. For each file:
   a. Parse YAML frontmatter
   b. Check if status == "Not Applied"
   c. Extract: company, job-title, role-category, hiring-manager
   d. Parse body for Application URL (regex: **Application URL**: https://...)
3. Return filtered job list
```

**Required data per job:**
| Field | Source | Required |
|-------|--------|----------|
| company | frontmatter | Yes |
| job-title | frontmatter | Yes |
| application_url | body markdown | Yes |
| role-category | frontmatter | For clustering |
| hiring-manager | frontmatter | No |
| note_path | file path | Yes |

### Step 2: Parallel Asset Generation

**Per-Job Parallelization (2x speedup):**

For each job, spawn TWO parallel Task agents:

```
Task 1 (Resume):
  - Invoke ResumeTailoring workflow
  - Input: application_url, company
  - Output: ~/Downloads/Your_Name_Resume_[Company].docx

Task 2 (Cover Letter):
  - Invoke CoverLetterGenerator workflow
  - Input: application_url, company
  - Output: ~/Downloads/Your_Name_CoverLetter_[Company].docx
```

Wait for both to complete before post-processing.

**Multi-Job Parallelization (5x speedup):**

Process 3-5 jobs concurrently:
- Spawn 3-5 "job processor" agents
- Each handles full pipeline: extract → tailor → generate → save
- Checkpoint after each job completes

### Step 3: Storage and Linking

**Create folder:**
```bash
mkdir -p "~/Career/Generated Assets/[Company_Sanitized]/"
```

**Company name sanitization:**
- Remove special characters except alphanumeric, spaces, hyphens
- Replace spaces with nothing (e.g., "Apollo.io" → "Apolloio")

**Move files:**
```bash
mv ~/Downloads/Your_Name_Resume_[Company].docx \
   "~/Career/Generated Assets/[Company]/Your_Name_Resume_[Company].docx"

mv ~/Downloads/Your_Name_CoverLetter_[Company].docx \
   "~/Career/Generated Assets/[Company]/Your_Name_CoverLetter_[Company].docx"
```

### Step 4: Update Frontmatter

Add to job note YAML frontmatter:

```yaml
resume-path: "~/Career/Generated Assets/[Company]/Your_Name_Resume_[Company].docx"
cover-letter-path: "~/Career/Generated Assets/[Company]/Your_Name_CoverLetter_[Company].docx"
```

**Frontmatter update logic:**
1. Read note file content
2. Parse existing frontmatter (between `---` markers)
3. Add/update resume-path and cover-letter-path fields
4. Preserve all existing fields and tags
5. Write back to file

### Step 5: Checkpoint System

**Checkpoint file:** `~/.claude/state/batch-asset-checkpoint.json`

```json
{
  "batch_id": "batch-20260114-143000",
  "started_at": "2026-01-14T14:30:00Z",
  "total_jobs": 45,
  "processed": 12,
  "failed": 1,
  "pending": 32,
  "last_successful": "Stripe - Revenue Operations Analyst",
  "jobs": {
    "Stripe - Revenue Operations Analyst": {
      "status": "completed",
      "resume_path": "~/Career/Generated Assets/Stripe/...",
      "cover_letter_path": "~/Career/Generated Assets/Stripe/..."
    },
    "Apollo.io - Sales Operations Manager": {
      "status": "failed",
      "error": "URL returned 404",
      "retry_count": 1
    }
  }
}
```

**Recovery:**
- On start, check for existing checkpoint
- Resume from last_successful + 1
- Skip already-completed jobs

---

## Output Format

### Batch Summary Report

```markdown
# Batch Asset Generation Report

**Batch ID:** batch-20260114-143000
**Started:** 2026-01-14 14:30:00 CST
**Completed:** 2026-01-14 15:45:00 CST
**Duration:** 1h 15m

## Results

| Status | Count |
|--------|-------|
| Completed | 42 |
| Failed | 3 |
| Skipped | 0 |

## Generated Assets

| Company | Resume | Cover Letter |
|---------|--------|--------------|
| Stripe | ✅ | ✅ |
| Apollo.io | ✅ | ✅ |
| Samsara | ❌ URL 404 | ❌ URL 404 |

## Failed Jobs (Require Manual Review)

1. **Samsara - Sales Operations Manager**
   - Error: Application URL returned 404
   - Action: Verify URL or mark as expired

## Next Steps

- Review generated assets in Obsidian
- Check tracker base for ✅ indicators
- Apply to high-priority jobs first
```

---

## Error Handling

| Error Type | Action |
|------------|--------|
| URL 404/expired | Skip job, flag for manual review |
| Rate limit hit | Pause 60s, retry |
| DOCX generation failed | Retry once, then skip |
| Frontmatter parse error | Skip update, log warning |
| Timeout (>5 min per job) | Skip, flag for manual review |

---

## Integration with Existing Workflows

This workflow orchestrates:
1. **ResumeTailoring** (`Workflows/ResumeTailoring.md`)
2. **CoverLetterGenerator** (`Workflows/CoverLetterGenerator.md`)

Both workflows auto-load:
- User resume from Career folder
- Career context files from `CONTEXT/` (relative to skill root: Index, Experience Details, Technical Skills, Honest Gaps)
- Job requirements via URL parsing

---

## Performance Targets

| Metric | Target |
|--------|--------|
| Per-job time (parallel) | <90 seconds |
| Batch throughput | 40 jobs/hour |
| ATS score | ≥85/100 |
| Keyword coverage | 70-90% |

---

## Usage Examples

**Single job:**
```
User: "Generate resume and cover letter for the Stripe job"
→ Process single job
→ Save to Generated Assets/Stripe/
→ Update frontmatter
```

**Batch all:**
```
User: "Batch generate assets for all not applied jobs"
→ Load 45 "Not Applied" jobs
→ Process in batches of 5
→ Save all to Generated Assets/
→ Update all frontmatter
→ Report summary
```

**Resume from checkpoint:**
```
User: "Resume batch generation"
→ Load checkpoint
→ Skip completed jobs
→ Continue from last_successful + 1
```
