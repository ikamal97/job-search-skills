# JobBoardSearch Workflow

**Automated job discovery across major job boards with filtering and ranking.**

## Objective

Search multiple job boards simultaneously to discover relevant positions matching user criteria (role, location, salary, remote preference, etc.), returning structured, actionable results.

## Input Requirements

Before searching, gather:

| Parameter | Required | Example |
|-----------|----------|---------|
| **Job Title/Role** | Yes | "Business Systems Analyst", "Data Analyst" |
| **Location** | No | "Remote", "San Francisco", "Hybrid - NYC" |
| **Salary Range** | No | "$80K+", "$100K-$150K" |
| **Experience Level** | No | "Mid-level (3-5 years)", "Senior (5+ years)" |
| **Industry/Domain** | No | "Healthcare", "Fintech", "SaaS" |
| **Recency** | No | "Last 7 days", "Last 14 days" (default: 14 days) |

## Step-by-Step Process

### Step 1: Construct Search Queries

Create optimized search queries for each job board:

**LinkedIn Format:**
```
[Job Title] [location] [salary range] [remote/hybrid] site:linkedin.com/jobs
```

**Indeed Format:**
```
[Job Title] [location] [salary range] site:indeed.com
```

**Glassdoor Format:**
```
[Job Title] [location] site:glassdoor.com/Job
```

**Built In Format:**
```
[Job Title] remote site:builtin.com/jobs
```

**Example Query Set:**
```
User criteria: "Remote Business Systems Analyst, $80K+, healthcare"

Queries:
1. "Business Systems Analyst remote $80k healthcare site:linkedin.com/jobs"
2. "Business Systems Analyst remote $80000 healthcare site:indeed.com"
3. "Business Systems Analyst remote healthcare site:glassdoor.com/Job"
4. "Business Systems Analyst remote healthcare site:builtin.com/jobs"
```

### Step 2: Execute Parallel Searches

Use **WebSearch** tool to query all job boards in parallel:

```javascript
// Parallel search execution
await Promise.all([
  WebSearch("Business Systems Analyst remote $80k healthcare site:linkedin.com/jobs"),
  WebSearch("Business Systems Analyst remote $80000 healthcare site:indeed.com"),
  WebSearch("Business Systems Analyst remote healthcare site:glassdoor.com/Job"),
  WebSearch("Business Systems Analyst remote healthcare site:builtin.com/jobs")
]);
```

**CRITICAL:** Make all 4 searches in a SINGLE message with multiple tool calls to maximize efficiency.

### Step 3: Extract Job Data

For each search result, extract:

- **Job Title** (exact from posting)
- **Company Name**
- **Location** (Remote, Hybrid, On-site + city)
- **Salary Range** (if visible in search results)
- **Posted Date** (if available)
- **Source** (LinkedIn, Indeed, Glassdoor, Built In)
- **URL** (direct link to posting)

**If salary/date not in search results:** Note as "Unknown" - do NOT fabricate.

### Step 4: Fetch Full Job Descriptions

For top 10-15 results (by recency and relevance), use **WebFetch** to get full posting:

```javascript
WebFetch(url, "Extract job requirements, responsibilities, and qualifications")
```

**What to extract:**
- Full requirements section
- Responsibilities/duties
- Qualifications (required vs preferred)
- Salary range (if not in search results)
- Company description
- Benefits/perks

### Step 5: MANDATORY Job Verification

```
┌─────────────────────────────────────────────────────────────────┐
│  GUARDRAIL: Before proceeding, ALL jobs MUST be verified.      │
│  See: Workflows/JobVerification.md                              │
└─────────────────────────────────────────────────────────────────┘
```

**Run 4 verification checks on every job:**

1. **Remote Status Check**
   - Verify job is fully remote (not hybrid/on-site)
   - Fail if: "hybrid", "X days in office", specific location without "remote"
   - Pass if: "Remote", "Work from Home", "Fully Remote"

2. **URL Active Check**
   - HTTP request to each job URL
   - Fail if: 404, 403, 410, timeout, redirect to non-job page
   - Pass if: HTTP 200 OK

3. **Recency Check**
   - Parse posted date from job listing
   - Fail if: Posted more than 21 days ago (3 weeks)
   - Pass if: Posted within last 21 days

4. **Job Exists Check**
   - Fetch page content via WebFetch
   - Fail if: "position filled", "job expired", "no longer available"
   - Pass if: Job description present, apply button visible

**Verification Code:**
```python
import urllib.request
import ssl
from datetime import datetime
import re

def verify_job(job, max_days=21):
    """Run all 4 verification checks. Returns (passed, reason)."""
    url = job['url']
    location = job.get('location', '').lower()
    posted_date = job.get('posted_date')
    posted_text = job.get('posted_text', '').lower()

    # Check 1: Remote Status
    if any(x in location for x in ['hybrid', 'on-site', 'onsite']):
        return False, "Failed: Not remote"
    if 'remote' not in location and 'work from home' not in location:
        return False, "Failed: Remote status unclear"

    # Check 2: URL Active
    try:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        })
        response = urllib.request.urlopen(req, timeout=10, context=ssl_ctx)
        if response.getcode() != 200:
            return False, f"Failed: HTTP {response.getcode()}"
    except Exception as e:
        return False, f"Failed: {str(e)}"

    # Check 3: Recency (must be posted within last 21 days)
    if posted_date:
        try:
            if isinstance(posted_date, str):
                posted_date = datetime.strptime(posted_date, '%Y-%m-%d')
            days_ago = (datetime.now() - posted_date).days
            if days_ago > max_days:
                return False, f"Failed: Posted {days_ago} days ago (max: {max_days})"
        except:
            pass
    elif '30+ days' in posted_text or 'over a month' in posted_text:
        return False, "Failed: Posted 30+ days ago"

    # Check 4: Job Exists (via WebFetch content analysis)
    # WebFetch the URL and check for closed/expired indicators

    return True, "Verified"
```

**Only jobs passing ALL 4 checks proceed to ranking.**

### Step 6: Structure and Rank Results

**Initial Ranking Criteria:**
1. **Recency** - Posted within last 7 days = highest priority
2. **Salary Visibility** - Transparent salary = higher trust
3. **Title Match** - Exact title match vs close variant
4. **Source Quality** - Direct company postings > job boards

**Output Format:**
```json
{
  "search_criteria": {
    "role": "Business Systems Analyst",
    "location": "Remote",
    "salary_min": "$80K",
    "industry": "Healthcare"
  },
  "verification_summary": {
    "total_discovered": 60,
    "passed_remote_check": 52,
    "passed_url_check": 48,
    "passed_recency_check": 42,
    "passed_exists_check": 40,
    "final_verified": 40
  },
  "top_matches": [
    {
      "rank": 1,
      "title": "Business Systems Analyst III",
      "company": "Velera",
      "location": "Remote",
      "salary": "$85K-$108K",
      "posted_date": "2026-01-05",
      "recency_days": 1,
      "source": "Built In",
      "url": "https://builtin.com/job/...",
      "requirements_summary": "5+ years BA experience, SQL, Agile, stakeholder management",
      "full_description": "[Full text if fetched]",
      "verification": {
        "remote_check": "PASSED",
        "url_check": "PASSED (HTTP 200)",
        "recency_check": "PASSED (5 days ago)",
        "exists_check": "PASSED",
        "status": "VERIFIED"
      }
    }
  ]
}
```

## Error Handling

### No Results Found
```
"No positions found matching criteria. Suggestions:
1. Broaden location (remove remote-only requirement)
2. Lower salary minimum
3. Try related titles (e.g., 'Business Analyst' instead of 'Business Systems Analyst')
4. Expand industry search"
```

### Rate Limiting / Blocked
```
"Hit rate limit on [job board]. Retrieved N results from other sources.
Recommend: Try again in 15 minutes OR use direct company career pages"
```

### Stale Results (all >30 days old)
```
"Warning: All results are 30+ days old. Market may be slow.
Recommendations:
- Set up job alerts for future postings
- Check company career pages directly
- Consider adjacent roles"
```

## Quality Filters

Apply these filters AFTER search, BEFORE presenting results:

| Filter | Rule | Action |
|--------|------|--------|
| **Duplicate Detection** | Same company + same title | Keep most recent |
| **Spam Detection** | Title contains "urgently hiring", "immediate start" | Flag as low quality |
| **Salary Red Flags** | Wide range (e.g., "$40K-$150K") | Flag as unclear comp |
| **Recruiting Firms** | Company is Robert Half, Insight Global, etc. | Note as "via recruiter" |
| **Commission-Based** | Salary includes "commission", "uncapped earnings" | Flag clearly |

## Output Presentation

### Summary View (Always Show)
```
Found 47 Business Systems Analyst positions (Remote, Healthcare, $80K+)

TOP 5 MATCHES (by recency & fit):
1. Velera - Business Systems Analyst III ($85K-$108K) - Posted 1 day ago
2. MedImpact - Client Services BSA III ($83K-$146K) - Posted 3 days ago
3. Centene - Business Systems Analyst ($80K-$110K) - Posted 5 days ago
...

[View full details] | [Calculate fit scores] | [Export to tracker]
```

### Detailed View (On Request)
Show full structured JSON with all extracted fields.

## Integration Points

**With JobVerification (MANDATORY):**
```
After search complete → Run 3-check verification → Only verified jobs proceed
```

**With JobDescriptionParser:**
```
After verification → Pass verified URLs to parser → Get structured requirements
```

**With job-search-specialist agent:**
```
Verified results → Parser extracts requirements → Agent calculates fit scores → Ranked output
```

**Complete Pipeline:**
```
JobBoardSearch → JobVerification → JobDescriptionParser → Fit Score → Output
      ↓               ↓                    ↓                 ↓          ↓
   60 jobs      →  45 verified      →  45 parsed       →  45 scored  → Excel
```

## Performance Targets

- **Search Speed:** < 10 seconds for 4 parallel searches
- **Fetch Speed:** < 5 seconds per full job description
- **Total Time:** < 2 minutes for complete search + parse workflow
- **Result Quality:** 80%+ of results match user criteria

## Usage Examples

**Example 1: Basic Search**
```
User: "Find remote data analyst jobs paying $90k+"
→ Search LinkedIn, Indeed, Glassdoor, Built In
→ Filter for remote, $90K+ salary
→ Return top 10 by recency
```

**Example 2: Targeted Search**
```
User: "Search for Business Systems Analyst roles in healthcare, remote, posted in last week"
→ Add "healthcare" to query
→ Filter results to last 7 days
→ Fetch full descriptions for top 5
→ Return structured list
```

**Example 3: Multi-Location Search**
```
User: "Find product manager jobs in SF, NYC, or remote"
→ Create 3 separate query sets
→ Merge and deduplicate results
→ Rank by location preference (remote > SF > NYC per user)
```
