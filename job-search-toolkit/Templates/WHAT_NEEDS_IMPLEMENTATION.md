# What Still Needs Implementation - Skills & Experience Sections

## Current State vs. Needed

### ✅ What's Currently Working

The `simple_template_processor.py` **successfully replaces the first 4 paragraphs** of the template:

```python
# Paragraph 0: Name
_replace_text_in_paragraph(all_paragraphs[0], "JOHN DOE")

# Paragraph 1: Contact line
_replace_text_in_paragraph(all_paragraphs[1], "Chicago, IL | (555) 123-4567 | john@example.com | linkedin.com/in/johndoe")

# Paragraph 2: Professional title
_replace_text_in_paragraph(all_paragraphs[2], "SENIOR BUSINESS ANALYST")

# Paragraph 3: Professional summary
_replace_text_in_paragraph(all_paragraphs[3], "Senior Business Analyst with 6+ years...")
```

**Result:** Header section of resume is perfect ✅

---

### ❌ What's Missing: Skills Section

**Problem:** Skills section has **dynamic categories** that change based on the job.

**Template Structure (paragraphs 4-11):**
```
Para 4: Empty paragraph
Para 5: Empty paragraph
Para 6: "SKILLS AND TOOLS" header (Arial Bold 22pt)
Para 7: "Requirements: elicitation, BRD/FRD, user stories..."
Para 8: "Process: as-is/to-be mapping, swimlanes, SOPs..."
Para 9: "Delivery: SDLC, Agile ceremonies, UAT..."
Para 10: "Data: SQL, data migration, data validation..."
Para 11: "Tools: Jira, Confluence, Rally, Visio..."
Para 12: Empty paragraph
```

**What needs to happen:**

1. **Delete paragraphs 7-11** (template's 5 skill categories)
2. **Insert NEW paragraphs dynamically** based on job requirements

**Example for a Salesforce role:**
```python
skills_data = {
    "CRM Platforms": ["Salesforce", "HubSpot", "Microsoft Dynamics"],
    "Technical Skills": ["SQL", "Python", "API integration"],
    "Tools & Platforms": ["Jira", "Confluence", "Tableau"],
    "Methodologies": ["Agile", "Scrum", "Waterfall"]
}

# Need to generate 4 paragraphs (not 5 like template)
# Each with format: **Bold Category:** regular, comma, separated, skills
```

**Why it's not implemented:**
- Need to **count** how many categories to generate (could be 3-7)
- Need to **clone the formatting** from template paragraph 7
- Need to **insert after** paragraph 6 ("SKILLS AND TOOLS" header)
- Need to **create XML** for each category paragraph

---

### ❌ What's Missing: Experience Section

**Problem:** Experience section has **variable number of jobs** (2-6+) and **variable bullets per job** (2-8).

**Template Structure (paragraphs 13-38):**
```
Para 13: "EXPERIENCE" header

Job 1 - KAVALIER (4 paragraphs total):
Para 14: "KAVALIER | Chicago, IL" (company/location - Bold 20pt)
Para 15: "Business Systems Analyst | Sep 2024 to Present" (title/dates - Regular 19pt)
Para 16: Bullet 1 (with numId="4" for list formatting)
Para 17: Bullet 2 (with numId="4")
Para 18: Bullet 3 (with numId="4")
Para 19: Empty paragraph (spacing)

Job 2 - VICEGERENT (5 paragraphs total):
Para 20: "VICEGERENT CUSTOM CLOTHIERS | Chicago, IL"
Para 21: "Business Operations Analyst | Jun 2022 to Sep 2024"
Para 22: Bullet 1 (with numId="1" - different from Job 1!)
Para 23: Bullet 2 (with numId="1")
Para 24: Bullet 3 (with numId="1")
Para 25: Bullet 4 (with numId="1")
Para 26: Empty paragraph

Job 3 - OLIVER WYMAN (4 paragraphs total):
Para 27: "OLIVER WYMAN | Chicago, IL"
Para 28: "Senior Consultant | Mar 2022 to Jun 2022"
Para 29: Bullet 1 (with numId="3")
Para 30: Bullet 2 (with numId="3")
Para 31: Empty paragraph

Job 4 - DELOITTE (7 paragraphs total):
Para 32: "DELOITTE CONSULTING LLP | Chicago, IL"
Para 33: "Business Analyst | Oct 2020 to Mar 2022"
Para 34: Bullet 1 (with numId="2")
Para 35: Bullet 2 (with numId="2")
Para 36: Bullet 3 (with numId="2")
Para 37: Bullet 4 (with numId="2")
Para 38: Bullet 5 (with numId="2")
Para 39: Empty paragraph

Para 40: Empty paragraph
```

**What needs to happen:**

1. **Delete paragraphs 14-40** (all template experience entries)
2. **Insert NEW paragraphs dynamically** for each job in `experience_list`
3. **Use different numId for each job** to keep bullet lists separate

**Example for 2 jobs:**
```python
experience_data = [
    {
        "company": "Tech Corp",
        "location": "San Francisco, CA",
        "title": "Senior Analyst",
        "dates": "Jan 2023 to Present",
        "bullets": [
            "Led requirements for $5M CRM implementation",
            "Created 50+ user stories for Agile sprints",
            "Reduced defect rate by 30% through UAT"
        ]
    },
    {
        "company": "Consulting Firm",
        "location": "Chicago, IL",
        "title": "Business Analyst",
        "dates": "Jun 2020 to Dec 2022",
        "bullets": [
            "Authored BRDs and FRDs for stakeholders",
            "Built process maps in Visio"
        ]
    }
]

# Need to generate:
# Job 1: 1 company para + 1 title para + 3 bullet paras + 1 empty = 6 paragraphs (numId="1")
# Job 2: 1 company para + 1 title para + 2 bullet paras + 1 empty = 5 paragraphs (numId="2")
# Total: 11 new paragraphs
```

**Why it's not implemented:**
- Need to **loop through** each job in experience list
- Need to **clone formatting** from template paragraphs 14, 15, 16
- Need to **increment numId** for each job (numId="1", then "2", then "3", etc.)
- Need to **create bullet XML** with proper `<w:numPr>` tags
- Need to **handle variable bullet counts** (some jobs have 2, others have 5)

---

## Technical Challenges

### Challenge 1: Finding The Right Insertion Point

**Skills Section:**
- Need to find paragraph 6 ("SKILLS AND TOOLS" header)
- Delete paragraphs 7-11
- Insert new paragraphs after paragraph 6

**Experience Section:**
- Need to find paragraph 13 ("EXPERIENCE" header)
- Delete paragraphs 14-40 (or however many exist until "EDUCATION")
- Insert new paragraphs after paragraph 13

### Challenge 2: Preserving Formatting XML

Each paragraph has complex XML formatting. Example bullet paragraph:

```xml
<w:p>
    <w:pPr>
        <w:numPr>
            <w:ilvl w:val="0"/>
            <w:numId w:val="4"/>  <!-- This must be different per job! -->
        </w:numPr>
        <w:spacing w:before="18.270263671875" w:line="228.48" w:lineRule="auto"/>
        <w:ind w:left="720" w:right="253.27" w:hanging="360"/>
        <w:rPr><w:sz w:val="19"/></w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr><w:sz w:val="19"/></w:rPr>
        <w:t>Bullet text goes here</w:t>
    </w:r>
</w:p>
```

**All these attributes must be preserved:**
- `<w:numPr>` - numbering properties (bullet formatting)
- `<w:spacing>` - space before/after
- `<w:ind>` - indentation (left, hanging)
- `<w:rPr>` - font size
- `<w:sz w:val="19"/>` - 19pt font

### Challenge 3: The numId Problem

**Why each job needs different numId:**

Template uses:
- Kavalier: `numId="4"`
- Vicegerent: `numId="1"`
- Oliver Wyman: `numId="3"`
- Deloitte: `numId="2"`

This keeps bullet lists **independent**. If they all used `numId="1"`, Word would think it's ONE big list continuing across all jobs.

**Solution needed:**
```python
num_id = 1
for job in experience_list:
    # Create company paragraph
    # Create title paragraph

    # Create bullets with THIS numId
    for bullet in job["bullets"]:
        create_bullet_paragraph(bullet, numId=num_id)

    # Increment for next job
    num_id += 1
```

---

## What The Implementation Needs To Do

### For Skills Section:

```python
def _insert_skills_section(doc, skills_dict, after_paragraph):
    """
    Insert dynamic skill categories.

    Steps:
    1. Clone template paragraph 7 formatting as baseline
    2. For each category in skills_dict:
       a. Create new paragraph XML
       b. Set category name as bold text
       c. Set skills as regular text (comma-separated)
       d. Insert after current position
    3. Add empty paragraph at end
    """
    # Clone formatting from template para 7
    template_para_xml = extract_paragraph_xml(doc, paragraph_index=7)

    # Loop through categories
    for category, skills_list in skills_dict.items():
        skills_text = ", ".join(skills_list)

        # Build paragraph with bold category + regular skills
        new_para_xml = f'''<w:p>
            <w:pPr>
                <w:spacing w:before="5.01" w:line="240" w:lineRule="auto"/>
                <w:rPr><w:sz w:val="19"/></w:rPr>
            </w:pPr>
            <w:r>
                <w:rPr><w:b w:val="1"/><w:sz w:val="19"/></w:rPr>
                <w:t xml:space="preserve">{category}: </w:t>
            </w:r>
            <w:r>
                <w:rPr><w:sz w:val="19"/></w:rPr>
                <w:t>{skills_text}</w:t>
            </w:r>
        </w:p>'''

        # Insert into document
        doc["word/document.xml"].insert_after(after_paragraph, new_para_xml)
```

**Estimated effort:** ~30-45 minutes

---

### For Experience Section:

```python
def _insert_experience_section(doc, experience_list, after_paragraph):
    """
    Insert experience entries with bullets.

    Steps:
    1. Clone template paragraphs 14 (company), 15 (title), 16 (bullet)
    2. For each job:
       a. Create company paragraph (bold, 20pt)
       b. Create title/dates paragraph (regular, 19pt)
       c. Create bullet paragraphs (with numId)
       d. Create empty paragraph for spacing
    3. Increment numId for each job
    """
    num_id = 1
    insert_point = after_paragraph

    for job in experience_list:
        # Company/location paragraph
        company_xml = f'''<w:p>
            <w:pPr>
                <w:spacing w:before="43.26" w:line="240"/>
                <w:ind w:left="14.74"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Arial"/>
                    <w:b w:val="1"/>
                    <w:sz w:val="20"/>
                </w:rPr>
                <w:t>{job["company"]} | {job["location"]}</w:t>
            </w:r>
        </w:p>'''

        # Title/dates paragraph
        title_xml = f'''<w:p>
            <w:pPr>
                <w:spacing w:before="0" w:line="240"/>
                <w:ind w:left="4.75"/>
            </w:pPr>
            <w:r>
                <w:rPr><w:sz w:val="19"/></w:rPr>
                <w:t>{job["title"]} | {job["dates"]}</w:t>
            </w:r>
        </w:p>'''

        # Bullet paragraphs
        for bullet_idx, bullet in enumerate(job["bullets"]):
            spacing_before = "18.27" if bullet_idx == 0 else "0"

            bullet_xml = f'''<w:p>
                <w:pPr>
                    <w:numPr>
                        <w:ilvl w:val="0"/>
                        <w:numId w:val="{num_id}"/>
                    </w:numPr>
                    <w:spacing w:before="{spacing_before}" w:line="228.48"/>
                    <w:ind w:left="720" w:right="253.27" w:hanging="360"/>
                    <w:rPr><w:sz w:val="19"/></w:rPr>
                </w:pPr>
                <w:r>
                    <w:rPr><w:sz w:val="19"/></w:rPr>
                    <w:t>{bullet}</w:t>
                </w:r>
            </w:p>'''

            # Insert each piece
            # (simplified - actual implementation needs proper insertion)

        # Empty paragraph after job
        empty_xml = '<w:p><w:pPr><w:spacing w:before="0"/></w:pPr></w:p>'

        # Increment numId for next job
        num_id += 1
```

**Estimated effort:** ~1-1.5 hours (more complex due to numId handling)

---

## Summary

### What Works Now ✅
- Name replacement
- Contact line replacement
- Professional title replacement
- Summary replacement

### What Needs Implementation ❌

**Skills Section (~30-45 min):**
1. Delete template's 5 skill paragraphs
2. Generate dynamic categories from job requirements
3. Create paragraphs with bold labels + regular skills
4. Preserve formatting (19pt, spacing, indents)

**Experience Section (~1-1.5 hours):**
1. Delete template's 4 experience entries
2. Loop through user's experience list (2-6+ jobs)
3. For each job, create 4-8 paragraphs:
   - Company/location (bold 20pt)
   - Title/dates (regular 19pt)
   - 2-8 bullets (with proper numId)
   - Empty spacing paragraph
4. Increment numId for each job to keep lists separate
5. Preserve all formatting (spacing, indents, fonts)

---

## Why Not Implemented Yet?

I prioritized getting the **core template cloning approach working** first (header section). This proves the concept and lets you test immediately.

Skills and experience sections require **more complex logic**:
- Dynamic paragraph count (unknown until runtime)
- XML generation with proper formatting
- NumId management for bullet lists
- Insertion point tracking

**The foundation is solid.** Adding skills/experience is now straightforward following the patterns shown above.

Would you like me to implement these sections now?
