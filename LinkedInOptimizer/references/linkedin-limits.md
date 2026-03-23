# LinkedIn Character Limits & Platform Rules (2026)

Single source of truth for all LinkedIn platform constraints.

## Character Limits by Section

### Headline

| Constraint | Value | Notes |
|------------|-------|-------|
| **Maximum** | 220 characters | Desktop limit |
| **Mobile Display** | ~240 characters | But truncates aggressively |
| **Search-Indexed Zone** | First 60 characters | LinkedIn search indexes this most heavily |
| **Mobile Visible** | First 40-60 characters | Rest hidden on mobile feeds |

**Character Budget Allocation:**

| Zone | Characters | Priority | Content |
|------|------------|----------|---------|
| CRITICAL | 1-60 | Highest | Primary keyword/role |
| HIGH | 61-100 | High | Secondary keywords + differentiation |
| STANDARD | 101-160 | Medium | Supporting context, skills |
| OPTIONAL | 161-220 | Low | Nice-to-have (truncated on mobile) |

### About Section (Summary)

| Constraint | Value | Notes |
|------------|-------|-------|
| **Maximum** | 2,600 characters | Hard LinkedIn limit |
| **Optimal Range** | 1,800-2,200 characters | 300-350 words |
| **"See more" Truncation** | ~300 characters | Desktop cutoff |
| **Mobile Truncation** | ~150-200 characters | Even less visible |

**Critical Zone:** First 300 characters must contain:
1. Hook sentence (creates curiosity)
2. Value proposition (one line)
3. Immediate credibility signal

### Experience Section

| Constraint | Value | Notes |
|------------|-------|-------|
| **Title** | 100 characters | Job title field |
| **Description** | 2,000 characters per entry | Each role separately |
| **Company Name** | 100 characters | |
| **Bullets Recommended** | 3-5 per role | Sweet spot for readability |

**Role-by-Role Guidance:**

| Role Type | Bullets | Why |
|-----------|---------|-----|
| Current role | 5-6 | Show comprehensive contributions |
| Previous roles | 3-4 | Key achievements |
| Older roles (5+ years) | 2-3 | Highlights only |

### Skills Section

| Constraint | Value | Notes |
|------------|-------|-------|
| **Maximum Skills** | 100 | Platform limit |
| **Recommended** | 15-30 | Focus on most relevant |
| **Top/Pinned Skills** | 3 | Featured prominently |
| **Visible by Default** | Top 3 only | Others require click to see |

### Other Sections

| Section | Limit |
|---------|-------|
| Name | 100 characters (50 first, 50 last) |
| Custom URL | 100 characters |
| Location | 200 characters |
| Education Description | 1,000 characters |
| Volunteer Description | 1,000 characters |
| Publications Description | 2,000 characters |
| Featured Items | 100 items |
| Certifications | 2,000 characters |

## All-Star Status Requirements

LinkedIn All-Star profiles are **40x more likely** to be found in searches.

**Required Elements (all 7):**

- [ ] Profile Photo
- [ ] Headline (optimized, not default)
- [ ] Industry & Location
- [ ] About Section (written summary)
- [ ] Experience (at least 1 position)
- [ ] Skills (minimum 5)
- [ ] Education (at least 1 entry)
- [ ] 50+ connections (milestone)

## Mobile Truncation Rules

**What Users Actually See:**

| Section | Desktop | Mobile Feed | Mobile Profile |
|---------|---------|-------------|----------------|
| Headline | Full 220 | ~50-60 chars | ~100 chars |
| About | 300 chars + "see more" | ~150 chars | ~200 chars |
| Experience Title | Full | Full | Full |
| Experience Bullets | First 2-3 visible | First 1-2 | First 2-3 |

**Implication:** Front-load everything. The most important content goes first.

## Keyword Optimization

**Where Keywords Matter (Priority Order):**

1. **Headline** - Most powerful SEO tool
2. **About section** - Natural density 5-10%
3. **Experience descriptions** - Match recruiter search terms
4. **Skills section** - Direct match to search queries
5. **Job titles** - Use industry-standard titles

**Keyword Density Targets:**

| Section | Target | Method |
|---------|--------|--------|
| Headline | 2-3 keywords | Every word counts |
| About | 8-12 keywords | Natural integration |
| Experience | 5-8 per entry | In bullets and descriptions |
| Skills | 15-30 total | From job posting analysis |

## Algorithm Considerations (2025-2026)

**What LinkedIn Algorithm Rewards:**

- Relevance over recency
- Quality over virality
- Comments longer than 10 words
- Expertise signals
- Consistent posting (2-3x per week)

**Engagement Metrics:**

| Factor | Weight |
|--------|--------|
| Comments | 2x likes |
| Shares | 1.5x likes |
| Profile views from post | High |
| Saves | High |
| Time spent on post | Medium |

## Validation Rules

Before output, verify:

```
Headline.length <= 220
Headline.first(60).includes(primary_keyword)
About.length <= 2600
About.length >= 1800 (recommended)
About.first(300).includes(hook + value_prop)
Experience.each.description.length <= 2000
Experience.each.bullets.count >= 3
Skills.count >= 5
Skills.count <= 30 (recommended)
```
