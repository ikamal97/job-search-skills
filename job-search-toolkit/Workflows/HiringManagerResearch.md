# Hiring Manager Research Workflow

**Purpose:** Automatically identify hiring managers, find their LinkedIn profiles, infer email addresses, and draft personalized outreach emails for every job discovered.

**Trigger:** AUTOMATIC after JobBoardSearch completes

**Output:** Enriches job data with hiring manager information for proactive outreach

---

## Workflow Steps

### 1. Identify Target Hiring Manager Role

For each job, determine the likely hiring manager title based on the role category:

| Job Category | Target Hiring Manager Titles |
|--------------|------------------------------|
| Business Systems Analyst | VP/Director of IT, Engineering, Product, or Business Systems |
| Implementation Consultant | VP/Director of Customer Success, Professional Services, Implementation |
| RevOps / Revenue Operations | Chief Revenue Officer (CRO), VP Revenue Operations, Head of RevOps |
| Sales Operations | VP Sales Operations, Chief Revenue Officer, Head of Sales Ops |
| Customer Success Operations | VP Customer Success, Head of Customer Success Operations |
| Product Operations | VP Product, Head of Product Operations, Chief Product Officer |
| Solutions Consultant | VP Solutions Engineering, Head of Pre-Sales, VP Sales Engineering |

### 2. LinkedIn Research

**Search Pattern:**
```
"[Company Name] [Target Title] LinkedIn"
```

**Examples:**
- "Dropbox VP Engineering LinkedIn"
- "Apollo.io Chief Revenue Officer LinkedIn"
- "Samsara Director Customer Success LinkedIn"

**Search Strategy:**
- Start with most specific title (VP/Director level)
- If no results, broaden to department head
- Look for recent hires or current employees
- Verify profile matches company (check current employer)

**Fallback:** If no specific hiring manager found, use "Department Head" or "Hiring Team" as placeholder

### 3. Extract LinkedIn Profile URL

- Copy direct LinkedIn profile URL (https://linkedin.com/in/username)
- If profile not found, set to "Not found"
- Verify URL is accessible (not private/restricted)

### 4. Infer Email Address

Use common corporate email patterns based on hiring manager's name:

**Primary Patterns (in order of likelihood):**
1. `firstname.lastname@company.com`
2. `first.last@company.com`
3. `flast@company.com`
4. `firstname_lastname@company.com`
5. `firstnamelastname@company.com`

**Domain determination:**
- Use company website domain (e.g., apollo.io → apollo.io)
- For known companies, use standard domain (e.g., Salesforce → salesforce.com)
- If uncertain, use careers@company.com as fallback

**Note:** Email addresses are inferred, not verified. Users should verify before sending.

### 5. Draft Personalized Outreach Email

**Email Requirements:**
- **Length:** 150-200 words
- **Tone:** Professional but warm, conversational
- **Structure:**
  - Subject line referencing specific role + key qualifications
  - Greeting using hiring manager's first name
  - Opening: Reference specific job title and company **WITH JOB POSTING URL**
  - Body: 1-2 relevant achievements from candidate's background
  - Value proposition: How candidate's skills align with role
  - Clear CTA: Request for brief call/conversation
  - Sign-off: Professional closing with credentials

**CRITICAL: Job URL Inclusion**
- **ALWAYS include the job posting URL** in the opening paragraph
- Format: "I'm reaching out about the [Job Title] at [Company] ([JOB_URL])"
- This ensures hiring managers know exactly which role you're referencing
- Especially important when companies have multiple open positions

**Personalization Elements:**
- Reference specific job title (not generic "opening")
- Include job posting URL in first paragraph (MANDATORY)
- Mention relevant experience from candidate's resume (Deloitte, Oliver Wyman, Kavalier, etc.)
- Highlight 1-2 specific skills that match the role (e.g., BRDs/FRDs for BSA, RevOps for CRO)
- Research company mission/recent news when possible
- Tailor industry references (healthcare, fintech, SaaS, etc.)

**Email Template Structure:**
```
Subject: [Job Title] - [Key Qualification/Differentiator]

Hi [First Name],

[Opening: Reference specific job and company context WITH JOB URL]

[Body: 1-2 relevant achievements demonstrating qualifications]

[Value proposition: How experience aligns with role/company needs]

[CTA: Request for brief conversation]

Best regards,
[Candidate Name]
[Credential, e.g., B.S. Computer Science, Northwestern University]
```

**Example:**
```
Subject: Senior Revenue Operations Manager - RevOps + Analytics Background

Hi Adam,

I'm excited about the Senior Revenue Operations Manager role at Apollo.io (https://builtin.com/job/senior-customer-operations-manager/7091902). My background at Deloitte and Oliver Wyman includes building revenue operations frameworks, optimizing sales processes, and implementing CRM and analytics systems that drove predictable growth.

I've designed territory models, built pipeline forecasting tools, and created dashboards that gave revenue leaders real-time visibility into performance. At Kavalier, I built end-to-end revenue operations from scratch, managing everything from lead routing to customer retention.

I'd love to discuss how my RevOps expertise can support Apollo's hypergrowth. Could we schedule a call?

Best,
Idrees Kamal
```

---

## Implementation Guidelines

### Research Approach

1. **Batch Processing:** Process jobs in batches of 10-20 for efficiency
2. **Web Search Quota:** Each job requires 2-4 searches (hiring manager + verification)
3. **Parallel Execution:** Use Task agent with general-purpose subtype for large batches
4. **Fallback Handling:** Always provide placeholder values for missing data

### Quality Standards

**Verified Hiring Manager (High Confidence):**
- LinkedIn profile found and verified current at company
- Title matches expected hiring authority
- Profile is public and accessible

**Placeholder (Low Confidence):**
- No specific hiring manager identified
- Use "Department Head" or "Hiring Team"
- Email address: careers@company.com or generic department email

### Excel Integration

**Column Mapping:**
- Column K: Hiring Manager Name
- Column L: LinkedIn Profile URL (with hyperlink formatting)
- Column M: Email Address
- Column N: Draft Email (text wrapped, top-aligned)

**Formatting:**
- LinkedIn URLs: Blue underlined hyperlinks
- Draft emails: Wrap text enabled, vertical align top
- All columns: Auto-filter enabled

---

## Output Schema

```python
{
    "company": "Company Name",
    "job_title": "Job Title",
    "hiring_manager": "John Smith" | "Department Head",
    "linkedin_url": "https://linkedin.com/in/johnsmith" | "Not found",
    "email": "john.smith@company.com",
    "draft_email": "Subject: ...\n\nHi John,\n\n[Body]\n\nBest,\n[Name]"
}
```

---

## Best Practices

### Do's ✅
- Research thoroughly using multiple search queries
- Personalize each email based on company/role specifics
- Use professional but conversational tone
- Include specific achievements from candidate's resume
- Provide clear call-to-action
- Always include fallback values for missing data

### Don'ts ❌
- Don't use generic "I came across your posting" language
- Don't copy-paste identical emails across companies
- Don't exaggerate or misrepresent qualifications
- Don't use overly formal or salesy language
- Don't include attachments in initial outreach
- Don't guess email addresses without standard pattern

---

## Example: Full Research Output

**Job:** Business Analyst at Cleo

**Research Process:**
1. Search: "Cleo VP Engineering LinkedIn"
2. Found: Jorge Rodriguez - VP Engineering at Cleo
3. LinkedIn: https://www.linkedin.com/in/jrodriguez992002/
4. Email: jorge.rodriguez@meetcleo.com (firstname.lastname pattern)

**Draft Email:**
```
Subject: Business Analyst Role - Deloitte BSA Background

Hi Jorge,

I'm reaching out about the Business Analyst position at Cleo (https://www.builtinchicago.org/job/business-analyst/7933617). With my background as a Business Systems Analyst at Deloitte and Oliver Wyman, I've developed strong expertise in requirements gathering, process mapping, and cross-functional stakeholder management—skills that align perfectly with Cleo's mission to democratize financial services.

At Deloitte, I led multiple system implementations and authored comprehensive BRDs/FRDs that drove successful project outcomes. I've also built operational systems from the ground up at Kavalier, managing the full SDLC for customer-facing platforms.

I'd love to discuss how my analytical background and systems thinking can contribute to Cleo's growth. Are you available for a brief call this week?

Best regards,
Idrees Kamal
B.S. Computer Science, Northwestern University
```

---

## Integration with Job Search Workflow

**Sequence:**
1. JobBoardSearch → Finds jobs
2. JobVerification → Verifies jobs are active/remote/recent
3. **HiringManagerResearch** → Enriches with hiring manager data (YOU ARE HERE)
4. Excel Output → Complete tracking spreadsheet with 14 columns

**Automation:** This workflow runs automatically after JobBoardSearch completes. No user intervention required.
