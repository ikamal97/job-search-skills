# Resume Template Processor - Integration Guide

## Integration with JobSearchToolkit

This guide shows how to integrate the template-based resume generator with the JobSearchToolkit's ResumeTailoring workflow.

---

## Prerequisites

**Dependencies installed:**
```bash
pip3 install --break-system-packages defusedxml lxml
```

**Verified working:**
```bash
cd /Users/idreeskamal/.claude/skills/JobSearchToolkit/Templates
python3 generate_resume.py  # Should generate test resume successfully
```

---

## Integration Steps

### Option 1: Quick Integration (Recommended for Testing)

Add this code when ResumeTailoring workflow needs to generate DOCX:

```python
import os
import sys

# Setup environment
DOCX_SKILL_ROOT = "/Users/idreeskamal/.claude/plugins/cache/anthropic-agent-skills/example-skills/69c0b1a06741/skills/docx"
TEMPLATES_DIR = "/Users/idreeskamal/.claude/skills/JobSearchToolkit/Templates"

sys.path.insert(0, DOCX_SKILL_ROOT)
sys.path.insert(0, TEMPLATES_DIR)

# Import template processor
from simple_template_processor import generate_resume_from_template

# Call with tailored resume data
output_path = generate_resume_from_template(
    tailored_data={
        "header": {
            "name": user_name,
            "contact": user_contact_info
        },
        "professional_title": job_specific_title,
        "summary": tailored_summary,
        "skills": skill_categories,      # Note: Placeholder - needs implementation
        "experience": experience_list,    # Note: Placeholder - needs implementation
        "education": education_string
    },
    company_name=company_name,
    output_dir=os.path.expanduser("~/Downloads")
)

print(f"✓ Resume generated: {output_path}")
```

### Option 2: Module-Based Integration (Production)

Create a wrapper module in JobSearchToolkit:

**File: `/Users/idreeskamal/.claude/skills/JobSearchToolkit/resume_generator.py`**

```python
"""Resume generator wrapper for JobSearchToolkit."""

import os
import sys

# Auto-setup environment
_DOCX_SKILL = "/Users/idreeskamal/.claude/plugins/cache/anthropic-agent-skills/example-skills/69c0b1a06741/skills/docx"
_TEMPLATES = os.path.join(os.path.dirname(__file__), "Templates")

if _DOCX_SKILL not in sys.path:
    sys.path.insert(0, _DOCX_SKILL)
if _TEMPLATES not in sys.path:
    sys.path.insert(0, _TEMPLATES)

from simple_template_processor import generate_resume_from_template


def generate_tailored_resume(tailored_data: dict, company_name: str) -> str:
    """
    Generate tailored resume from template.

    Args:
        tailored_data: Resume data (see Templates/README.md for format)
        company_name: Company name for filename

    Returns:
        Path to generated DOCX file
    """
    return generate_resume_from_template(
        tailored_data=tailored_data,
        company_name=company_name,
        output_dir=os.path.expanduser("~/Downloads")
    )
```

**Then use in ResumeTailoring workflow:**

```python
from resume_generator import generate_tailored_resume

output_file = generate_tailored_resume(
    tailored_data=resume_data,
    company_name=job_company
)
```

---

## Data Mapping from ResumeTailoring to Template

The ResumeTailoring workflow produces structured data that needs to be mapped to template format:

### Header/Contact

```python
# From: resume_data extracted in Step 0
tailored_data["header"] = {
    "name": resume_data["header"]["name"],
    "contact": {
        "location": resume_data["header"]["location"],
        "phone": resume_data["header"]["phone"],
        "email": resume_data["header"]["email"],
        "linkedin": resume_data["header"]["linkedin"]
    }
}
```

### Professional Title

```python
# From: job requirements (Step 1)
# Generate from job title
tailored_data["professional_title"] = job_requirements["title"].upper()
# Or use tailored version from Step 4.3
```

### Summary

```python
# From: Step 4.3 (Update Professional Summary)
tailored_data["summary"] = enhanced_summary
```

### Skills (⚠️ Needs Implementation)

```python
# From: Step 3.1 (Reorder Skills Section) + Step 4.1 (Add Missing Skills)
# Generate dynamic categories based on job requirements

# Placeholder logic:
skill_categories = {
    "Requirements": ["BRD/FRD", "user stories", "elicitation"],
    "Process": ["process mapping", "as-is/to-be", "SOPs"],
    "Delivery": ["Agile", "UAT", "SDLC"],
    "Data": ["SQL", "data migration", "CRM automation"],
    "Tools": ["Jira", "Confluence", "Excel"]
}

tailored_data["skills"] = skill_categories
```

### Experience (⚠️ Needs Implementation)

```python
# From: Step 3.2 (Reorder Experience Bullets) + Step 4.2 (Weave Keywords)
# Map to template format

experience_list = []
for job in resume_data["experience"]:
    experience_list.append({
        "company": job["company"],
        "location": job["location"],
        "title": job["title"],
        "dates": job["dates"],
        "bullets": job["enhanced_bullets"]  # After keyword weaving
    })

tailored_data["experience"] = experience_list
```

### Education

```python
# From: resume_data extracted in Step 0
tailored_data["education"] = resume_data["education"]
```

---

## Current Limitations & Workarounds

### ⚠️ Skills Section

**Status:** Template processor currently doesn't generate skills section.

**Workaround:** Manually edit generated DOCX to add skills, OR complete the skills section implementation in `simple_template_processor.py`.

**To Complete:**
```python
# Add this function to simple_template_processor.py
def _insert_skills_section(doc, skills_dict, insert_after_paragraph_index):
    """Insert dynamic skill categories."""
    # Implementation needed
    pass
```

### ⚠️ Experience Section

**Status:** Template processor currently doesn't generate experience section.

**Workaround:** Manually edit generated DOCX to add experience, OR complete the experience section implementation.

**To Complete:**
```python
# Add this function to simple_template_processor.py
def _insert_experience_section(doc, experience_list, insert_after_paragraph_index):
    """Insert experience entries with bullets."""
    # Implementation needed
    pass
```

---

## Testing Integration

### Test Script

```python
# test_integration.py
import os
import sys

DOCX_SKILL = "/Users/idreeskamal/.claude/plugins/cache/anthropic-agent-skills/example-skills/69c0b1a06741/skills/docx"
TEMPLATES = "/Users/idreeskamal/.claude/skills/JobSearchToolkit/Templates"

sys.path.insert(0, DOCX_SKILL)
sys.path.insert(0, TEMPLATES)

from simple_template_processor import generate_resume_from_template

# Simulate ResumeTailoring workflow output
test_data = {
    "header": {
        "name": "IDREES KAMAL",
        "contact": {
            "location": "Chicago, IL",
            "phone": "(773) 789-0400",
            "email": "ikamal97@gmail.com",
            "linkedin": "linkedin.com/in/idreeskamal"
        }
    },
    "professional_title": "SENIOR BUSINESS SYSTEMS ANALYST",
    "summary": "Senior Business Systems Analyst with 6+ years of experience in Salesforce CRM implementations...",
    "skills": {},  # Placeholder
    "experience": [],  # Placeholder
    "education": "Northwestern University | B.S. Computer Science | Sep 2017 to Jun 2020"
}

result = generate_resume_from_template(
    tailored_data=test_data,
    company_name="Test_Integration"
)

print(f"✓ Test successful: {result}")
```

**Run:**
```bash
python3 test_integration.py
```

**Expected:** Resume generated at `~/Downloads/IDREES_KAMAL_Resume_Test_Integration.docx`

---

## Validation Checklist

After integration, verify:

- [ ] DOCX file generated successfully
- [ ] Filename format correct: `FirstName_LastName_Resume_CompanyName.docx`
- [ ] File opens in Word/LibreOffice without errors
- [ ] Header section: Name, contact info correct
- [ ] Professional title correct
- [ ] Summary paragraph correct
- [ ] **Skills section:** Currently placeholder (manual edit or implement)
- [ ] **Experience section:** Currently placeholder (manual edit or implement)
- [ ] Education section correct
- [ ] All fonts are Arial
- [ ] Font sizes match template (34pt name, 24pt title, etc.)
- [ ] Spacing matches template
- [ ] No formatting drift from original template

---

## Next Steps for Complete Integration

1. **Complete Skills Section Implementation**
   - Add `_insert_skills_section()` function
   - Parse skill categories from tailored data
   - Generate paragraphs with bold labels + regular text

2. **Complete Experience Section Implementation**
   - Add `_insert_experience_section()` function
   - Handle variable number of entries
   - Clone bullet formatting with proper numId

3. **End-to-End Testing**
   - Test with 5+ real job descriptions
   - Verify all sections populate correctly
   - Validate ATS compatibility

4. **Production Deployment**
   - Update ResumeTailoring workflow to use template processor
   - Add error handling for edge cases
   - Document any limitations

---

## Support & Troubleshooting

See `Templates/README.md` for:
- Detailed troubleshooting guide
- Template formatting specifications
- Data structure reference
- Common errors and solutions
