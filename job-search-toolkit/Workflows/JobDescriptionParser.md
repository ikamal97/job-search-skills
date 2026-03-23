# JobDescriptionParser Workflow

**Extract and structure job requirements from postings for automated fit score calculation.**

## Objective

Parse unstructured job descriptions into structured, categorized requirements that can be programmatically analyzed against candidate profiles to calculate fit scores.

## Input Types

Accepts job descriptions in multiple formats:

| Format | Source | How to Handle |
|--------|--------|---------------|
| **URL** | Job board link | Use WebFetch to retrieve full posting |
| **Plain Text** | Copy-pasted description | Parse directly |
| **HTML** | Saved job page | Extract text, parse |
| **Multiple URLs** | Batch processing | Process sequentially or in parallel |

## Step-by-Step Process

### Step 1: Fetch or Receive Content

**If URL provided:**
```javascript
WebFetch(url, "Extract complete job description including requirements, qualifications, responsibilities")
```

**If text provided:**
```javascript
// Work directly with provided text
```

**Critical:** Preserve ALL requirement text - don't summarize or paraphrase.

### Step 2: Identify Section Boundaries

Locate key sections using common patterns:

| Section | Common Headers | Variations |
|---------|----------------|------------|
| **Requirements** | "Requirements", "Qualifications" | "What You'll Need", "Must Haves" |
| **Preferred** | "Preferred", "Nice to Have" | "Bonus Points", "Desired" |
| **Experience** | "Experience", "Years Required" | "Background", "Track Record" |
| **Responsibilities** | "Responsibilities", "Duties" | "What You'll Do", "Role" |
| **Education** | "Education", "Degree" | "Academic Requirements" |
| **Skills** | "Skills", "Technical Skills" | "Technologies", "Tools" |

**Parsing Strategy:**
1. Split on headers (case-insensitive)
2. If no clear headers, identify bullet points or numbered lists
3. If neither, use NLP to categorize sentences

### Step 3: Extract Structured Data

#### 3.1 Experience Requirements

**Pattern matching for years:**
```regex
(\d+)\+?\s*years?
(\d+)-(\d+)\s*years?
minimum of (\d+) years?
```

**Examples:**
- "5+ years of experience" → `experience_years_min: 5`
- "3-5 years" → `experience_years_min: 3, experience_years_max: 5`
- "Minimum 7 years" → `experience_years_min: 7`

**Level indicators:**
- "Entry-level" → `level: "entry"`
- "Senior" → `level: "senior"`
- "Lead" / "Principal" → `level: "lead"`

#### 3.2 Technical Skills

**Keyword extraction with categorization:**

| Category | Keywords | Extraction Method |
|----------|----------|-------------------|
| **Programming** | Python, Java, SQL, JavaScript, etc. | Exact match + common variants |
| **Frameworks** | React, Django, Spring, .NET | Case-insensitive match |
| **Tools** | Jira, Confluence, Tableau, Excel | Acronym + full name matching |
| **Methodologies** | Agile, Scrum, Waterfall, SDLC | Keyword + context |
| **Databases** | PostgreSQL, MySQL, MongoDB | Name + variant matching |
| **Cloud** | AWS, Azure, GCP, Docker, K8s | Abbreviation + full name |

**Required vs Preferred:**
- In "Requirements" section → `required: true`
- In "Preferred" / "Nice to Have" → `required: false`
- With "must have" language → `required: true`
- With "bonus" / "plus" language → `required: false`

**Example Extraction:**
```
Raw: "Must have 5+ years Python and SQL. Familiarity with Tableau is a plus."

Structured:
{
  "technical_skills": [
    {"skill": "Python", "required": true, "context": "5+ years"},
    {"skill": "SQL", "required": true, "context": "5+ years"},
    {"skill": "Tableau", "required": false, "context": "familiarity"}
  ]
}
```

#### 3.3 Education Requirements

**Pattern matching:**
```regex
Bachelor('s)?\s+(degree|in)?
BS\s+(in|degree)?
Master('s)?\s+(degree|in)?
PhD
```

**Extract:**
- **Degree Level:** Bachelor's, Master's, PhD
- **Field:** Computer Science, related field, Business, etc.
- **Substitution Allowed:** "or equivalent experience"

**Examples:**
```
"Bachelor's degree in Computer Science or related field"
→ {
    "degree_level": "Bachelor's",
    "field": ["Computer Science", "related field"],
    "substitution_ok": true
  }

"Master's degree required"
→ {
    "degree_level": "Master's",
    "field": null,
    "substitution_ok": false
  }
```

#### 3.4 Domain/Industry Experience

**Industry keywords:**
- Healthcare, Finance, Retail, SaaS, Insurance, etc.

**Context clues:**
- "Healthcare systems experience"
- "Knowledge of HIPAA regulations"
- "Financial services background"
- "Experience with PCI compliance"

**Extract:**
```json
{
  "domain": {
    "industry": "Healthcare",
    "required": true,
    "specific_knowledge": ["HIPAA", "EHR systems"],
    "context": "Healthcare systems experience preferred"
  }
}
```

#### 3.5 Soft Skills

**Common patterns:**
- Communication
- Leadership
- Collaboration / Teamwork
- Problem-solving
- Time management
- Stakeholder management

**Extraction approach:**
- Look for explicit mentions
- Categorize as required only if in "Requirements" section
- Note specific contexts (e.g., "executive stakeholder communication")

### Step 4: Calculate Metadata

Enrich parsed data with metadata:

```json
{
  "metadata": {
    "total_required_skills": 8,
    "total_preferred_skills": 3,
    "technical_skills_count": 6,
    "soft_skills_count": 5,
    "has_salary_range": true,
    "remote_eligible": true,
    "clearance_required": false
  }
}
```

### Step 5: Structure Final Output

**Complete output format:**

```json
{
  "job_info": {
    "title": "Business Systems Analyst III",
    "company": "Velera",
    "location": "Remote",
    "salary_range": "$85K-$108K",
    "source_url": "https://..."
  },
  "requirements": {
    "experience": {
      "years_min": 5,
      "years_max": null,
      "level": "mid-senior"
    },
    "education": {
      "degree_level": "Bachelor's",
      "field": ["Computer Science", "related field"],
      "required": true,
      "substitution_allowed": true
    },
    "technical_skills": {
      "required": [
        {"skill": "SQL", "proficiency": "expert", "years": 5},
        {"skill": "Agile", "proficiency": null, "years": null},
        {"skill": "SDLC", "proficiency": null, "years": null}
      ],
      "preferred": [
        {"skill": "Python", "proficiency": null, "years": null},
        {"skill": "Tableau", "proficiency": "familiar", "years": null}
      ]
    },
    "soft_skills": {
      "required": [
        "stakeholder management",
        "communication",
        "problem-solving"
      ],
      "preferred": [
        "leadership"
      ]
    },
    "domain": {
      "industry": "Data warehousing",
      "required": false,
      "specific_knowledge": ["ETL processes", "data governance"]
    }
  },
  "responsibilities": [
    "Gather and document business requirements",
    "Translate requirements into technical specifications",
    "Lead UAT and testing activities"
  ],
  "metadata": {
    "total_required_skills": 11,
    "total_preferred_skills": 4,
    "technical_weight": "high",
    "domain_specificity": "medium",
    "seniority_indicators": ["Lead", "III", "Senior-level work"]
  },
  "parsing_notes": [
    "Salary range confirmed in posting",
    "Remote-first culture mentioned",
    "Multiple education substitution paths"
  ]
}
```

## Quality Validation

Before returning parsed output, verify:

- [ ] All required vs preferred categorizations are accurate
- [ ] No fabricated requirements (only what's in posting)
- [ ] Years of experience correctly extracted
- [ ] Skills are standardized (e.g., "JS" → "JavaScript")
- [ ] Education requirements clearly specified
- [ ] No duplicate skills across required/preferred

## Error Handling

### Ambiguous Language
```
"3-5 years or equivalent experience"
→ Store as: years_min: 3, years_max: 5, substitution_allowed: true
```

### Missing Sections
```
No clear "Requirements" section
→ Extract from job description body
→ Flag in parsing_notes: "Requirements inferred from description"
```

### Conflicting Information
```
"5+ years required" in one section, "3 years minimum" in another
→ Use more stringent requirement (5 years)
→ Note conflict in parsing_notes
```

## Integration with Fit Score Calculation

Parsed output maps directly to fit score components:

| Fit Score Component | Parsed Data Source |
|---------------------|-------------------|
| Core Requirements (40%) | `requirements.technical_skills.required` + `requirements.soft_skills.required` |
| Experience Level (20%) | `requirements.experience.years_min` |
| Technical Skills (20%) | `requirements.technical_skills.required` |
| Domain/Industry (10%) | `requirements.domain` |
| Education (10%) | `requirements.education` |

**Pass parsed JSON directly to fit score calculator.**

## Performance Targets

- **Parse Speed:** < 3 seconds per job description
- **Accuracy:** 90%+ correct categorization of required/preferred
- **Completeness:** Extract 95%+ of explicitly stated requirements

## Usage Examples

**Example 1: Parse from URL**
```
User: "Parse this job description: https://builtin.com/job/..."
→ WebFetch to retrieve posting
→ Extract sections
→ Structure requirements
→ Return JSON
```

**Example 2: Parse from text**
```
User: "Here's a job description [pastes text]. Extract the requirements."
→ Identify sections in text
→ Parse requirements
→ Return structured output
```

**Example 3: Batch parsing**
```
User: "Parse these 5 job postings and extract requirements"
→ Process all 5 in parallel
→ Return array of structured outputs
→ Highlight commonalities across postings
```

**Example 4: Compare requirements**
```
User: "Parse these two similar roles and show me the differences in requirements"
→ Parse both
→ Generate diff showing unique requirements in each
→ Highlight which is more junior/senior based on requirements
```
