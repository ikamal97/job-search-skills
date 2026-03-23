# Resume Template Processor - Production Guide

## Overview

Template-based resume generation for 100% deterministic formatting consistency.

**Method:** Unpack template DOCX → Replace content → Repack

**Benefits:**
- Exact formatting match to template (fonts, sizes, spacing, indents)
- No formatting drift between generated resumes
- Preserves all template specifications automatically

---

## Quick Start

### Prerequisites

Install required Python packages:

```bash
pip3 install --break-system-packages defusedxml lxml
```

### Test the System

Run the test script to verify everything works:

```bash
cd ./Templates
python3 generate_resume.py
```

This will generate a test resume at:
```
Output/IDREES_KAMAL_Resume_Test_Company.docx
```

Open the file and verify it matches the template formatting.

---

## Production Usage

### Basic Usage

```python
import os
import sys

# Set up PYTHONPATH
DOCX_SKILL_ROOT = "~/.claude/skills/docx"
sys.path.insert(0, DOCX_SKILL_ROOT)
sys.path.insert(0, "./Templates")

# Import generator
from simple_template_processor import generate_resume_from_template

# Prepare data
resume_data = {
    "header": {
        "name": "JOHN DOE",
        "contact": {
            "location": "San Francisco, CA",
            "phone": "(555) 123-4567",
            "email": "john@example.com",
            "linkedin": "linkedin.com/in/johndoe"
        }
    },
    "professional_title": "SENIOR BUSINESS ANALYST",
    "summary": "Senior Business Analyst with 6+ years...",
    "skills": {...},  # Dict of skill categories
    "experience": [...],  # List of experience dicts
    "education": "University | Degree | Dates"
}

# Generate resume
output_path = generate_resume_from_template(
    tailored_data=resume_data,
    company_name="Google",
    output_dir=os.path.join(os.path.dirname(__file__), '..', 'Output')
)

print(f"Resume generated: {output_path}")
```

---

## Integration with ResumeTailoring Workflow

### Step 1: Update ResumeTailoring.md Step 7

The workflow documentation has been updated to reference the template-based approach.

### Step 2: Call from Workflow

When the ResumeTailoring workflow reaches Step 7 (Generate DOCX), use:

```python
# In ResumeTailoring workflow implementation
import os
import sys

# Set up environment
DOCX_SKILL_ROOT = "~/.claude/skills/docx"
TEMPLATES_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, DOCX_SKILL_ROOT)
sys.path.insert(0, TEMPLATES_DIR)

# Import generator
from simple_template_processor import generate_resume_from_template

# Use tailored data from previous steps
output_file = generate_resume_from_template(
    tailored_data=tailored_resume_data,
    company_name=job_info["company"],
    output_dir=os.path.join(os.path.dirname(__file__), '..', 'Output')
)
```

---

## Template File Locations

The system auto-searches for template files in:

1. `Templates/resume-template.docx` (relative to skill root)
2. `CONTEXT/*.docx` (relative to skill root)

**Template refers to:** The universal structure and formatting specification. Content is dynamic based on job description.

---

## Current Status

### ✅ Completed

- [x] Template auto-search functionality
- [x] Header/contact/title/summary replacement
- [x] Document library integration
- [x] Environment setup (PYTHONPATH, dependencies)
- [x] Test script with sample data
- [x] Production-ready wrapper
- [x] Error handling

### ⚠️ In Progress / Future Enhancements

- [ ] Skills section dynamic category generation
- [ ] Experience section with variable entries (2-6+)
- [ ] Bullet points with proper numbering (numId)
- [ ] Education section replacement
- [ ] Full end-to-end testing with real job descriptions

**Current Version:** Handles header, contact, professional title, and summary.

**Production Recommendation:** For full functionality, complete the skills/experience/education replacement logic based on the patterns shown in `TemplateProcessor.py` (lines 200-400).

---

## Data Structure Reference

### Required Data Format

```python
tailored_data = {
    "header": {
        "name": str,           # Full name in UPPER CASE
        "contact": {
            "location": str,   # "City, State"
            "phone": str,      # "(123) 456-7890"
            "email": str,      # Email address
            "linkedin": str    # LinkedIn profile URL
        }
    },
    "professional_title": str,  # Job title in UPPER CASE
    "summary": str,              # 1-2 sentence professional summary
    "skills": {                  # Dict mapping category → list of skills
        "Category Name": ["skill1", "skill2", ...]
    },
    "experience": [              # List of experience dicts
        {
            "company": str,      # Company name
            "location": str,     # "City, State"
            "title": str,        # Job title
            "dates": str,        # "Mon YYYY to Mon YYYY" or "Present"
            "bullets": [str]     # List of achievement bullets
        }
    ],
    "education": str            # "University | Degree | Dates"
}
```

---

## Template Formatting Specifications

All formatting preserved from template:

| Element | Font | Size | Alignment | Spacing Before |
|---------|------|------|-----------|----------------|
| Name | Arial Bold | 34pt | Centered | 0 |
| Contact | Arial Regular | 20pt | Centered | ~33pt |
| Title | Arial Bold | 24pt | Centered | ~77pt |
| Summary | Arial Regular | 19pt | Justified | ~77pt |
| Section Headers | Arial Bold | 22pt | Left | ~77pt (first), ~12pt (subsequent) |
| Company Name | Arial Bold | 20pt | Left | ~43pt (first), ~25pt (subsequent) |
| Job Title/Dates | Arial Regular | 19pt | Left | 0 |
| Bullets | Arial Regular | 19pt | Left | ~18pt (first), 0 (subsequent) |

**Bullet Formatting:**
- Style: ● (filled circle)
- Left indent: 720 twips (0.5")
- Hanging indent: 360 twips (0.25")
- Line spacing: ~228pt

---

## Troubleshooting

### Error: "Module not found: defusedxml"

**Solution:**
```bash
pip3 install --break-system-packages defusedxml lxml
```

### Error: "Document library not available"

**Cause:** PYTHONPATH not set correctly.

**Solution:** Ensure this code runs before import:
```python
sys.path.insert(0, "~/.claude/skills/docx")
```

### Error: "Template not found"

**Cause:** Template file missing from expected locations.

**Solution:** Verify template exists at:
- `Templates/resume-template.docx` (relative to skill root), OR
- `CONTEXT/` (any .docx file, relative to skill root)

### Error: "Multiple nodes found"

**Cause:** Search text appears multiple times in template.

**Solution:** Use the simplified processor (`simple_template_processor.py`) which uses paragraph indices instead of text search.

---

## Files

- `generate_resume.py` - Test script with sample data
- `simple_template_processor.py` - Production-ready simplified processor
- `TemplateProcessor.py` - Full implementation (reference, may need completion)
- `README.md` - This file

---

## Next Steps for Full Production

To complete the full implementation:

1. **Complete Skills Section Logic**
   - Parse `tailored_data["skills"]` dict
   - Generate dynamic categories based on job type
   - Insert paragraphs with bold category labels + regular text skills

2. **Complete Experience Section Logic**
   - Support variable number of entries (2-6+)
   - Clone bullet formatting from template
   - Use separate numId for each experience entry

3. **Complete Education Section**
   - Simple text replacement in education paragraph

4. **Integration Testing**
   - Test with 5+ real job descriptions
   - Validate ATS parsing with Jobscan/Resume Worded
   - Verify visual consistency across all generated resumes

5. **Deploy to ResumeTailoring Workflow**
   - Update workflow to call template processor
   - Test end-to-end from job URL to DOCX output

---

## Support

For issues or questions:
- Check troubleshooting section above
- Review template formatting specifications
- Verify PYTHONPATH and dependencies are correctly set
- Test with `generate_resume.py` first before integrating
