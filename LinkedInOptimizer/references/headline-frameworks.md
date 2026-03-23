# Headline Generation Frameworks

Generate 3 variants by default, each with a distinct strategic emphasis.

## Character Budget (220 max)

| Zone | Characters | Priority | Content |
|------|------------|----------|---------|
| **CRITICAL** | 1-60 | Highest | Primary keyword/role (search-indexed) |
| **HIGH** | 61-100 | High | Secondary keywords + differentiation |
| **STANDARD** | 101-160 | Medium | Supporting context, skills |
| **OPTIONAL** | 161-220 | Low | Nice-to-have (truncated on mobile) |

**Rule:** Put the most searchable term in characters 1-60. That's what LinkedIn indexes most heavily.

## Three-Variant Strategy

### Variant A: Keyword-Optimized (Maximum Discoverability)

**Purpose:** Maximize appearance in recruiter searches
**Focus:** Exact-match keywords from target job postings
**Risk:** May feel generic

**Structure:**
```
[Exact Job Title] | [Top 3 Searched Skills] | [Industry/Domain]
```

**Examples:**
```
Business Systems Analyst | SQL, Agile, Salesforce | Healthcare Tech
AI Implementation Specialist | Automation & Operations | B2B SaaS
Product Marketing Manager | SEO & Content Strategy | FinTech
```

**When to Use:**
- Active job search
- Targeting specific roles
- Want maximum recruiter visibility

### Variant B: Achievement-Led (Credibility)

**Purpose:** Establish credibility through quantified results
**Focus:** Impressive metrics and outcomes
**Risk:** Requires strong, verifiable metrics

**Structure:**
```
[Credential/Achievement] | [Role] | [Quantified Result]
```

**Examples:**
```
Ex-[Consulting Firm] Consultant | [University] CS | Automating Operations with 70%+ Efficiency Gains
Reduced API Errors 30% | Software Engineer | Python, AWS, APIs
Built $2M Pipeline | Sales Engineer | Enterprise SaaS Solutions
```

**When to Use:**
- Strong credential (top company, top school)
- Impressive metrics to share
- Want to stand out from keyword-only headlines

### Variant C: Value-Focused (Differentiation)

**Purpose:** Stand out with unique value proposition
**Focus:** What you uniquely do for companies/clients
**Risk:** May miss some keyword searches

**Structure:**
```
[Value Statement] | [Core Capability] | [Method/Approach]
```

**Examples:**
```
Operations Leader Who Automates | AI Systems Design | Turning Manual Processes into Scalable Solutions
Making Complex Systems Simple | Business Analyst & Process Architect
I Help Companies Ship 2x Faster | DevOps & Platform Engineering
```

**When to Use:**
- Crowded job market (need differentiation)
- Building personal brand
- Targeting senior/leadership roles

## Employment Status Patterns

### Currently Employed

**Structure:**
```
[Title] at [Company] | [Key Skill] | [Value Proposition]
```

**Examples:**
```
Senior Business Analyst at Accenture | Process Optimization | Driving Digital Transformation
Staff Engineer at Google | ML Infrastructure | Building Scalable AI Systems
```

### Between Jobs / Job Searching

**DO NOT say:** "Open to Opportunities", "Seeking New Role" (doesn't appear in searches)

**Better Patterns:**

```
# Pattern 1: Target Role Forward
[Target Role] | [Key Skills] | [Industry Focus]

Example: AI Implementation Specialist | Automation & Operations | Building AI-Powered Workflows

# Pattern 2: Identity/Achievement Forward
[Identity/Credential] | [Value Proposition] | [Open Signal]

Example: Ex-[Consulting Firm] Consultant | Automating Operations with AI | Available for Contract & Full-Time

# Pattern 3: Value Statement Forward
[What You Do] | [Who You Help] | [Result]

Example: I Help Companies Automate Operations | 70%+ Efficiency Gains | Ex-[Consulting Firm], [University] CS
```

### Entrepreneur / Founder

**Avoid:** "Founder & CEO" (can signal unemployment or failed startup)

**Better Framing:**
```
# Frame as operational experience, not title
Built AI Systems for SMB Operations | Ex-[Consulting Firm] | Automation & Process Design

# Frame as consulting/advisory
Operations Automation Consultant | Ex-[Consulting Firm] | Building Scalable Workflows for SMBs

# Frame by what you do, not company
I Automate Business Operations | AI & Workflow Design | 70%+ Manual Work Reduction
```

### Career Changer

**Pattern:** Lead with target, prove with transferable skills

```
[Target Role] | [Transferable Skill] | [Unique Background]

Example: Business Systems Analyst | Process Optimization | Former Operations Leader
Example: Product Manager | Customer Research & Strategy | Former Management Consultant
```

## Headline Comparison Table

| Variant | Strategy | Best For | Risk |
|---------|----------|----------|------|
| A | Keyword-optimized | Maximum discoverability | May feel generic |
| B | Achievement-led | Credibility-building | Requires strong metrics |
| C | Value-focused | Standing out | May miss keyword searches |

## Output Format

```markdown
## Headline Options (220 char max)

| Variant | Headline | Strategy | Chars |
|---------|----------|----------|-------|
| A | [Keyword-optimized headline] | Keyword-optimized | X/220 |
| B | [Achievement-led headline] | Achievement-led | X/220 |
| C | [Value-focused headline] | Value-focused | X/220 |

**Recommendation:** [Variant X] is recommended because [reason based on user's situation - job searching, building brand, targeting specific roles, etc.]

**Keywords in First 60 Chars:**
- Variant A: [keyword 1], [keyword 2]
- Variant B: [keyword 1], [keyword 2]
- Variant C: [keyword 1], [keyword 2]
```

## Validation Checklist

Before outputting headlines:

- [ ] Each variant ≤ 220 characters
- [ ] Primary keyword in first 60 chars of each
- [ ] No duplicate strategy across variants
- [ ] No generic filler phrases
- [ ] All claims verifiable in CONTEXT
- [ ] Handles user's employment status correctly
- [ ] Character count displayed for each

## Examples by Role Type

### Technical Roles

```
# Software Engineer
A: Software Engineer | Python, AWS, Kubernetes | Backend & Infrastructure
B: Reduced API Latency 50% | Senior Engineer | Building Scalable Systems at Scale
C: I Make Systems That Don't Break | Reliability Engineering | Former Amazon

# Data Scientist
A: Data Scientist | Python, SQL, ML | Healthcare Analytics
B: Built Models Driving $5M Revenue | Senior Data Scientist | ML & Predictive Analytics
C: Turning Data into Decisions | ML & Analytics | Ex-McKinsey
```

### Business Roles

```
# Business Analyst
A: Business Systems Analyst | SQL, Agile, Salesforce | Healthcare Tech
B: Ex-[Consulting Firm] Consultant | [University] CS | Process Optimization Expert
C: Bridging Business & Technology | Systems Analysis | Making Complex Simple

# Product Manager
A: Product Manager | B2B SaaS | User Research & Strategy
B: Launched Products with 2M+ Users | Senior PM | Mobile & Web
C: I Build Products People Actually Use | User-Centered Design | Ex-Google
```

### Operations/Strategy Roles

```
# Operations
A: AI Implementation Specialist | Automation & Operations | B2B SaaS
B: Reduced Manual Work 70% | Operations Leader | AI & Workflow Automation
C: I Automate What Shouldn't Be Manual | Operations Design | Ex-[Consulting Firm]

# Strategy
A: Strategy & Operations Manager | M&A, FP&A, Process Design | FinTech
B: Led $50M Integration | Strategy Lead | Post-Merger Operations Expert
C: Making Strategy Executable | Operations & Analytics | Ex-McKinsey
```
