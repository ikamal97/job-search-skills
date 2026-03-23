# JobVerification Workflow

**MANDATORY GUARDRAIL: Every job MUST pass all 3 checks before inclusion in results.**

## Purpose

This is a deterministic verification gate that runs AFTER job discovery but BEFORE presenting results to user. Jobs that fail ANY check are excluded from final output.

## The 4 Verification Checks

| Check | Requirement | Pass Criteria | Fail Action |
|-------|-------------|---------------|-------------|
| **1. Remote Status** | Job must be fully remote | Location = "Remote" with no office requirements | Exclude from results |
| **2. URL Active** | Application link must work | HTTP 200 response (not 404/403/410) | Exclude from results |
| **3. Job Exists** | Posting must be live | Page contains job description, not "expired"/"closed" | Exclude from results |
| **4. Recency** | Posted within 3 weeks | Posted date ≤ 21 days ago | Exclude from results |

## CRITICAL: This Is Non-Negotiable

```
┌─────────────────────────────────────────────────────────────────┐
│  GUARDRAIL ENFORCEMENT                                          │
│                                                                 │
│  Every job found by JobBoardSearch MUST pass through this       │
│  verification workflow BEFORE being added to any output list,   │
│  tracker, or presentation to user.                              │
│                                                                 │
│  NO EXCEPTIONS. NO SHORTCUTS.                                   │
│                                                                 │
│  If verification cannot be performed (rate limiting, timeout),  │
│  the job is marked "UNVERIFIED" and flagged for manual review.  │
└─────────────────────────────────────────────────────────────────┘
```

## Step-by-Step Verification Process

### Step 1: Remote Status Verification

**Check Method:** Parse job location from search result AND full job description.

**Pass Criteria:**
- Location explicitly states "Remote" or "Work from Home" or "Remote - USA"
- No mention of required office days (e.g., "2 days in office")
- No hybrid language (e.g., "Hybrid - 3 days remote")
- No geographic restrictions that imply office (e.g., "Must be within 50 miles of HQ")

**Fail Criteria:**
- "Hybrid" anywhere in location
- "On-site" or "In-office"
- Specific city/state without "Remote" qualifier
- Language like "occasional travel to office required"
- "Remote with X days in office"

**Verification Code Pattern:**
```python
def verify_remote_status(job):
    """Returns True if job is fully remote, False otherwise."""
    location = job.get('location', '').lower()
    description = job.get('description', '').lower()

    # Fail conditions (check these first)
    fail_patterns = [
        'hybrid', 'on-site', 'onsite', 'in-office', 'in office',
        'days in office', 'days per week in', 'office presence',
        'relocate', 'relocation required'
    ]
    for pattern in fail_patterns:
        if pattern in location or pattern in description:
            return False, f"Failed: Contains '{pattern}'"

    # Pass conditions
    pass_patterns = ['remote', 'work from home', 'wfh', 'fully remote']
    for pattern in pass_patterns:
        if pattern in location:
            return True, "Passed: Remote confirmed"

    return False, "Failed: Remote status not confirmed"
```

### Step 2: URL Active Verification

**Check Method:** HTTP HEAD or GET request to job URL.

**Pass Criteria:**
- HTTP 200 OK response
- Page loads within 10 second timeout
- No redirect to generic "careers" or "search" page

**Fail Criteria:**
- HTTP 404 Not Found
- HTTP 403 Forbidden
- HTTP 410 Gone
- HTTP 301/302 redirect to non-job page
- Connection timeout (>10 seconds)
- SSL certificate error
- Domain unreachable

**Verification Code Pattern:**
```python
import urllib.request
import ssl

def verify_url_active(url, timeout=10):
    """Returns True if URL responds with 200, False otherwise."""
    try:
        # Create SSL context that handles various cert configurations
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

        response = urllib.request.urlopen(req, timeout=timeout, context=ssl_context)
        status = response.getcode()

        if status == 200:
            return True, f"Passed: HTTP {status}"
        else:
            return False, f"Failed: HTTP {status}"

    except urllib.error.HTTPError as e:
        return False, f"Failed: HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, f"Failed: {str(e.reason)}"
    except Exception as e:
        return False, f"Failed: {str(e)}"
```

### Step 3: Recency Verification

**Check Method:** Parse posted date from job listing and calculate days since posting.

**Pass Criteria:**
- Job posted within last 21 days (3 weeks)
- Posted date is parseable and valid

**Fail Criteria:**
- Job posted more than 21 days ago
- Posted date is "30+ days ago" or similar
- No posted date available AND job appears stale

**Date Extraction Patterns:**
```regex
Posted (\d+) days? ago
Posted (\d+) hours? ago
Posted (today|yesterday)
(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})
(January|February|...) \d{1,2}, \d{4}
```

**Verification Code Pattern:**
```python
from datetime import datetime, timedelta
import re

def verify_recency(job, max_days=21):
    """Returns True if job posted within max_days, False otherwise."""
    posted_date = job.get('posted_date')
    posted_text = job.get('posted_text', '').lower()

    # If we have a parsed date
    if posted_date:
        try:
            if isinstance(posted_date, str):
                posted_date = datetime.strptime(posted_date, '%Y-%m-%d')
            days_ago = (datetime.now() - posted_date).days
            if days_ago <= max_days:
                return True, f"Passed: Posted {days_ago} days ago"
            else:
                return False, f"Failed: Posted {days_ago} days ago (max: {max_days})"
        except:
            pass

    # Parse from text like "Posted 5 days ago"
    days_match = re.search(r'posted (\d+) days? ago', posted_text)
    if days_match:
        days_ago = int(days_match.group(1))
        if days_ago <= max_days:
            return True, f"Passed: Posted {days_ago} days ago"
        else:
            return False, f"Failed: Posted {days_ago} days ago (max: {max_days})"

    # Check for "30+ days" indicator
    if '30+ days' in posted_text or 'over a month' in posted_text:
        return False, "Failed: Posted 30+ days ago"

    # Check for recent indicators
    if any(x in posted_text for x in ['today', 'just now', 'hours ago', 'yesterday']):
        return True, "Passed: Posted recently"

    # If no date info, mark as unverified (not auto-fail)
    return None, "Unverified: No posting date found"
```

**Max Recency:** 21 days (3 weeks). Jobs older than this are excluded.

---

### Step 4: Job Exists Verification

**Check Method:** Fetch page content and verify job posting is still active.

**Pass Criteria:**
- Page contains job title or description text
- No "job has been filled" messaging
- No "posting expired" messaging
- No "position closed" messaging
- Apply button/link is present

**Fail Criteria:**
- Page shows "This job has been filled"
- Page shows "This posting has expired"
- Page shows "Position no longer available"
- Page shows "Job not found"
- Page redirects to generic job search
- Page content is empty or error page

**Verification Code Pattern:**
```python
def verify_job_exists(url, expected_title=None):
    """Returns True if job posting is still active, False otherwise."""

    # Use WebFetch to get page content
    content = WebFetch(url, "Check if this job posting is still active. Look for: job title, apply button, any 'expired' or 'filled' messages.")

    # Fail indicators
    closed_patterns = [
        'job has been filled', 'position has been filled',
        'no longer available', 'posting has expired',
        'job not found', 'this position is closed',
        'sorry, this job', 'job has been removed'
    ]

    content_lower = content.lower()
    for pattern in closed_patterns:
        if pattern in content_lower:
            return False, f"Failed: Job closed - '{pattern}'"

    # Pass indicators (at least one should be present)
    active_patterns = ['apply', 'submit application', 'requirements', 'qualifications']
    for pattern in active_patterns:
        if pattern in content_lower:
            return True, "Passed: Active job posting confirmed"

    return False, "Failed: Could not confirm job is active"
```

## Verification Workflow Execution

### Batch Verification Process

When verifying multiple jobs (e.g., after JobBoardSearch):

```
Input: List of 60 potential jobs from search

Step 1: Remote Status Check
├── Check all 60 jobs for remote status
├── Result: 52 pass, 8 fail (hybrid/on-site)
└── Proceed with 52 jobs

Step 2: URL Active Check
├── HTTP check all 52 URLs
├── Run 10 parallel requests at a time
├── Result: 48 pass, 4 fail (404s, 403s)
└── Proceed with 48 jobs

Step 3: Recency Check
├── Parse posted dates for all 48 jobs
├── Filter to jobs posted within 21 days
├── Result: 42 pass, 6 fail (older than 3 weeks)
└── Proceed with 42 jobs

Step 4: Job Exists Check
├── WebFetch all 42 URLs for content analysis
├── Check for closed/expired indicators
├── Result: 40 pass, 2 fail (filled positions)
└── Final verified list: 40 jobs

Output: 40 verified jobs ready for user
```

### Output Format

**Per-Job Verification Result:**
```json
{
  "job_id": "velera-bsa-001",
  "url": "https://...",
  "verification": {
    "remote_check": {
      "passed": true,
      "detail": "Passed: Remote confirmed"
    },
    "url_check": {
      "passed": true,
      "detail": "Passed: HTTP 200"
    },
    "recency_check": {
      "passed": true,
      "detail": "Passed: Posted 5 days ago"
    },
    "exists_check": {
      "passed": true,
      "detail": "Passed: Active job posting confirmed"
    },
    "overall": "VERIFIED"
  }
}
```

**Batch Summary:**
```json
{
  "verification_summary": {
    "total_input": 60,
    "passed_all_checks": 40,
    "failed_remote": 8,
    "failed_url": 4,
    "failed_recency": 6,
    "failed_exists": 2,
    "unverified": 0
  }
}
```

## Error Handling

### Rate Limiting
If job board blocks requests:
- Mark job as "UNVERIFIED"
- Add to manual review queue
- Note: "Rate limited - requires manual verification"

### Timeout
If URL doesn't respond within timeout:
- Retry once after 5 seconds
- If still fails, mark as "UNVERIFIED"
- Note: "Timeout - may be temporarily unavailable"

### WebFetch Blocked
If WebFetch can't retrieve content:
- Try alternative URL patterns (remove tracking params)
- If still fails, mark URL check as passed but exists check as "UNVERIFIED"
- Note: "Content blocked - URL works but content unverifiable"

## Integration Points

### With JobBoardSearch

JobBoardSearch MUST call this verification workflow before returning results:

```
JobBoardSearch Flow:
1. Execute searches → Find 60 potential jobs
2. [MANDATORY] Call JobVerification → 48 verified jobs
3. Return only verified jobs to user
```

### With Excel/Tracker Output

Only verified jobs go into trackers:

```
Tracker Creation Flow:
1. Receive verified job list
2. Each job has verification.overall = "VERIFIED"
3. Add to Excel with confidence
4. All URLs guaranteed working at time of creation
```

## Logging & Audit Trail

Every verification run produces a log:

```
[2026-01-07 21:30:15] JobVerification started
[2026-01-07 21:30:15] Input: 50 jobs
[2026-01-07 21:30:16] Remote Check: 45/50 passed
[2026-01-07 21:30:25] URL Check: 40/45 passed (5 HTTP errors)
[2026-01-07 21:30:45] Exists Check: 38/40 passed (2 filled)
[2026-01-07 21:30:45] Final verified: 38 jobs
[2026-01-07 21:30:45] Verification complete
```

## Quality Targets

- **False Positive Rate:** <1% (jobs marked verified that are actually invalid)
- **False Negative Rate:** <5% (valid jobs incorrectly rejected)
- **Verification Speed:** <2 seconds per job for URL check, <5 seconds for exists check
- **Overall Throughput:** 50 jobs verified in <3 minutes
