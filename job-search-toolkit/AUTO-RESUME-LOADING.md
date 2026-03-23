# Auto-Resume Loading Feature

**ENHANCEMENT ADDED:** January 7, 2026

The CoverLetterGenerator workflow now automatically finds and loads your resume - no manual input needed!

---

## How It Works

### Step 0: Auto-Load (Runs Automatically)

When you request a cover letter, the system:

1. **Searches for your resume** in these locations (priority order):
   ```
   ✓ **/Career/**/*.pdf        (Primary - finds yours here!)
   ✓ **/career/**/*.pdf         (Case-insensitive)
   ✓ **/*resume*.pdf            (Anywhere with "resume" in name)
   ✓ **/Career/**/*.docx        (DOCX alternative)
   ✓ **/Career/**/*.md          (Markdown alternative)
   ```

2. **Extracts your information automatically:**
   - ✓ Contact info (name, phone, email, LinkedIn, location)
   - ✓ All work experience entries
   - ✓ All skills
   - ✓ Education
   - ✓ Certifications (if any)

3. **Uses YOUR real achievements** instead of generic examples

---

## Your Current Setup

**Resume Location:** ✅ FOUND
```
~/Career/CONTEXT/Your_Name_BSA_Resume_01.02.26 copy.pdf
```

**Extracted Data:**
- **Name:** Your Name
- **Phone:** (555) 123-4567
- **Email:** user@example.com
- **LinkedIn:** linkedin.com/in/yourprofile
- **Location:** Chicago, IL

**Experience (example - 5 positions):**
1. Company A - Business Systems Analyst (Sep 2024 - Present)
2. Company B - Business Operations Analyst (Jun 2022 - Sep 2024)
3. Consulting Firm - Senior Consultant (Mar 2022 - Jun 2022)
4. Enterprise Corp - Business Analyst (Oct 2020 - Mar 2022)
5. University - B.S. Computer Science (Sep 2017 - Jun 2020)

**Skills Extracted:** 20+ skills including BRD/FRD, Process Mapping, SDLC, Agile, UAT, SQL, Python, Jira, Confluence, Visio

---

## Usage

### Before Enhancement
```
You: "Generate a cover letter for [job]"
Me: "I need your contact info, experience, and skills..."
You: [Provides all info manually]
```

### After Enhancement (NOW)
```
You: "Generate a cover letter for [job URL]"
Me:
  ✓ Auto-finds resume in Career folder
  ✓ Extracts all your info
  ✓ Uses YOUR real achievements from:
    - Your most recent role (key accomplishments)
    - Previous roles (quantified metrics)
    - All positions in your resume
  ✓ Generates tailored cover letter
```

**Result:** Cover letters are authentic, accurate, and use your real metrics!

---

## Workflow Comparison

### Old Way (Generic Examples)
```markdown
"In my current role at a large healthcare payer organization, I led a
comprehensive process analysis and redesign initiative for our utilization
management department that reduced prior authorization turnaround time by 40%..."
```
❌ Problem: Generic, not YOUR experience

### New Way (Your Real Achievements)
```markdown
"In my role as Business Analyst at [Your Company], I authored BRDs and
FRDs to translate stakeholder needs into functional requirements, built
swimlane as-is/to-be process maps in Visio, and executed UAT by creating
test plans and tracking defects in Jira..."
```
✅ Result: Authentic, specific, YOUR actual experience

---

## What Gets Auto-Loaded

### Contact Information
- Full name
- Phone number (formatted)
- Email address
- LinkedIn URL
- Current location/city

### Experience Entries
For each job:
- Job title
- Company name
- Employment dates
- Location
- Key achievements (bullet points)
- Quantifiable metrics

### Skills
All skills from your resume's Skills section:
- Technical skills
- Process skills
- Tools & platforms
- Methodologies

### Education
- Degree(s)
- Institution(s)
- Graduation dates
- Relevant coursework (if listed)

### Certifications
- Any certifications listed
- Issuing organization
- Dates

---

## Fallback Behavior

### If Resume Not Found
```
⚠ Warning: Resume not found in Career folder

Searched locations:
- ~/Career/
- career/ (case-insensitive)
- Files with "resume" in name

Options:
1. Provide user profile manually
2. Specify resume file path
3. Continue with minimal profile (name + contact only)

Recommendation: Save resume to Career folder for automatic detection.
```

The system will ask for manual input rather than failing completely.

---

## Maintaining Your Resume

### Best Practices

**Keep Resume Updated:**
- Update `Career/` folder whenever you update your resume
- System always uses the **most recently modified** file
- Name it clearly (e.g., `Your_Name_BSA_Resume_[date].pdf`)

**File Format:**
- ✅ **PDF** (best - widely accepted, I can read it)
- ✅ DOCX (acceptable - also readable)
- ✅ Markdown (works but less common for applications)

**Location:**
- ✅ Keep in `~/Career/`
- ✅ Or anywhere with "Career" or "resume" in path

**Multiple Versions:**
- System picks **most recent** modification date
- Safe to keep old versions for reference
- They won't interfere with auto-load

---

## Example: Full Workflow

### You Say:
```
"Generate a cover letter for this Senior Business Process Analyst role at
CareFirst: [job URL]"
```

### What Happens Behind the Scenes:
```
Step 0: Auto-Load Resume
  ✓ Searching Career folder...
  ✓ Found: Your_Name_BSA_Resume_01.02.26 copy.pdf
  ✓ Reading PDF...
  ✓ Extracted contact: Your Name, (555) 123-4567, user@example.com
  ✓ Extracted 5 experience entries
  ✓ Extracted 20+ skills
  ✓ User profile built

Step 1: Process Job Input
  ✓ Fetching job description from URL...
  ✓ Parsing requirements...
  ✓ 26 keywords identified

Step 2: Company Research
  ✓ WebSearch: CareFirst mission...
  ✓ Found: Nonprofit serving 3.5M members in MD/DC/VA
  ✓ Mission: Affordable, accessible healthcare

Step 3: Match Your Achievements to Job
  ✓ [Company D]: BRD/FRD authoring → matches "requirements gathering"
  ✓ [Company D]: UAT execution → matches "testing"
  ✓ [Company A]: Workflow automation → matches "process improvement"
  ✓ [Company D]: Process mapping → matches "workflow mapping"

Step 4-7: Generate, Optimize, Validate, Output
  ✓ 398-word cover letter generated
  ✓ 85% keyword coverage (22/26 keywords)
  ✓ ATS score: 97.8/100
  ✓ Files created: MD, DOCX, PDF
```

### You Get:
```
✓ Cover letter using YOUR real achievements from all your listed positions
✓ Your actual contact info (no placeholders)
✓ Tailored to CareFirst's utilization management role
✓ ATS-optimized with 97.8/100 score
✓ Ready to submit
```

---

## Benefits

### Before Auto-Load
- ❌ Had to provide info manually every time
- ❌ Risk of generic/placeholder content
- ❌ Inconsistent contact details
- ❌ Time-consuming to specify achievements

### After Auto-Load
- ✅ Zero manual input needed
- ✅ Always uses YOUR real achievements
- ✅ Consistent, accurate contact info
- ✅ Instant generation with authentic content
- ✅ Every cover letter is personalized to YOU

---

## Technical Details

### Search Algorithm
```python
def find_user_resume():
    search_patterns = [
        "**/Career/**/*.pdf",      # Primary
        "**/career/**/*.pdf",       # Case-insensitive
        "**/*resume*.pdf",          # Filename match
        "**/Career/**/*.docx",      # DOCX format
        "**/Career/**/*.md"         # Markdown format
    ]

    for pattern in search_patterns:
        files = glob(pattern)
        if files:
            # Return most recently modified
            return max(files, key=os.path.getmtime)

    return None
```

### Extraction Process
1. **Read file** using appropriate parser (PDF/DOCX/MD)
2. **Parse header** for contact information
3. **Identify sections** (Experience, Skills, Education)
4. **Extract structured data** from each section
5. **Build profile object** for cover letter generation

### Privacy & Security
- ✅ All processing happens locally
- ✅ Resume data never leaves your system
- ✅ No external APIs for resume parsing
- ✅ Full control over what's shared

---

## Troubleshooting

### "Resume not found"
**Solution:** Ensure resume is in one of these locations:
- `~/Career/`
- Any folder named "Career" (case-insensitive)
- Any file with "resume" in filename

### "Could not extract contact info"
**Solution:** Ensure resume has standard header format:
```
Name
Phone | Email | LinkedIn | Location
```

### "Missing experience entries"
**Solution:** Resume should have clear section headers:
- "EXPERIENCE" or "Work Experience" or "Professional Experience"
- Job titles, companies, and bullet points clearly formatted

### Multiple resumes detected
**Solution:** System uses **most recent** file by modification date
- Update the resume you want to use
- Or remove old versions from Career folder

---

## Summary

**What Changed:**
- ✅ Added Step 0: Auto-Load User Resume
- ✅ Automatic resume search in Career folder
- ✅ Extracts contact info, experience, skills, education
- ✅ Uses YOUR real achievements instead of generic examples
- ✅ Zero manual input needed for future cover letters

**What You Need to Do:**
- ✅ Nothing! Your resume is already in the right place
- ✅ Just keep it updated when you make changes
- ✅ System handles everything else automatically

**Next Cover Letter:**
Just say: "Generate a cover letter for [job]"
→ System auto-loads your resume and creates personalized letter!

---

**Enhancement Complete: January 7, 2026**
