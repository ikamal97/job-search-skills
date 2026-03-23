# Spec-Driven Resume Generator Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace Python template-based resume generation with a declarative YAML spec + JavaScript generator using docx-js.

**Architecture:** YAML spec file declares all formatting (typography, spacing, bullets). ResumeGenerator.js reads spec + JSON data, builds DOCX programmatically via docx-js. One-page verification uses existing Python script as subprocess.

**Tech Stack:** Node.js, docx-js, js-yaml, existing verify_page_count.py

---

## Task 1: Add js-yaml Dependency

**Files:**
- Modify: `~/.claude/skills/JobSearchToolkit/Templates/package.json`

**Step 1: Check current package.json**

Run: `cat ~/.claude/skills/JobSearchToolkit/Templates/package.json`
Expected: See current dependencies (should have docx already)

**Step 2: Install js-yaml**

Run: `cd ~/.claude/skills/JobSearchToolkit/Templates && npm install js-yaml`
Expected: Package installed, package.json updated

**Step 3: Verify installation**

Run: `node -e "require('js-yaml'); console.log('js-yaml OK')"`
Expected: "js-yaml OK"

**Step 4: Commit**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add Templates/package.json Templates/package-lock.json
git commit -m "chore: add js-yaml dependency for spec parsing"
```

---

## Task 2: Create resume-spec.yaml

**Files:**
- Create: `~/.claude/skills/JobSearchToolkit/Templates/resume-spec.yaml`

**Step 1: Create the spec file**

```yaml
# resume-spec.yaml
# Measurements: twips (1" = 1440), font sizes: half-points (19 = 9.5pt)

meta:
  version: "1.0"

page:
  width: 12240
  height: 15840
  margins:
    top: 720
    bottom: 720
    left: 720
    right: 720

defaults:
  font: "Arial"
  line_spacing: 240
  line_rule: "auto"
  spacing_after: 0
  widow_control: false

typography:
  name:
    size: 34
    bold: true
    alignment: "center"

  contact:
    size: 20
    alignment: "center"
    spacing_before: 33
    separator: " | "

  professional_title:
    size: 24
    bold: true
    alignment: "center"
    spacing_before: 77

  summary:
    size: 19
    spacing_before: 77

  section_header:
    size: 22
    bold: true
    spacing_before_first: 77
    spacing_before_subsequent: 12

  skill_category:
    label_size: 19
    label_bold: true
    items_size: 19
    spacing_before: 5.01

  experience:
    company:
      size: 20
      bold: true
      spacing_before_first: 43.26
      spacing_before_subsequent: 25
      indent_left: 14.74
    title:
      size: 19
      indent_left: 4.75
    bullet:
      size: 19
      spacing_before_first: 18.27
      spacing_before_subsequent: 0
      line_spacing: 228.48

  education:
    size: 19

bullets:
  character: "●"
  indent_left: 720
  indent_hanging: 360
  indent_right: 253.27

numbering:
  start_num_id: 1
  increment_per_job: true
```

**Step 2: Verify YAML is valid**

Run: `cd ~/.claude/skills/JobSearchToolkit/Templates && node -e "const yaml = require('js-yaml'); const fs = require('fs'); const spec = yaml.load(fs.readFileSync('resume-spec.yaml', 'utf8')); console.log('Spec version:', spec.meta.version);"`
Expected: "Spec version: 1.0"

**Step 3: Commit**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add Templates/resume-spec.yaml
git commit -m "feat: add resume formatting spec (YAML)"
```

---

## Task 3: Create ResumeGenerator.js - Spec Loader

**Files:**
- Create: `~/.claude/skills/JobSearchToolkit/Templates/ResumeGenerator.js`

**Step 1: Write spec loader with validation**

```javascript
// ResumeGenerator.js - Spec-driven resume generation
const {
  Document, Packer, Paragraph, TextRun,
  AlignmentType, LevelFormat
} = require('docx');
const yaml = require('js-yaml');
const fs = require('fs');
const path = require('path');
const os = require('os');

// ─────────────────────────────────────────────────────────
// 1. SPEC LOADER
// ─────────────────────────────────────────────────────────

function loadSpec(specPath) {
  try {
    const raw = fs.readFileSync(specPath, 'utf8');
    return yaml.load(raw);
  } catch (err) {
    if (err.code === 'ENOENT') {
      throw new Error(`Spec not found: ${specPath}`);
    }
    throw new Error(`Invalid YAML: ${err.message}`);
  }
}

// Temporary test export
if (require.main === module) {
  const spec = loadSpec(path.join(__dirname, 'resume-spec.yaml'));
  console.log('Loaded spec version:', spec.meta.version);
  console.log('Default font:', spec.defaults.font);
  console.log('Name size:', spec.typography.name.size, 'half-points');
}

module.exports = { loadSpec };
```

**Step 2: Test spec loader**

Run: `cd ~/.claude/skills/JobSearchToolkit/Templates && node ResumeGenerator.js`
Expected:
```
Loaded spec version: 1.0
Default font: Arial
Name size: 34 half-points
```

**Step 3: Commit**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add Templates/ResumeGenerator.js
git commit -m "feat: add spec loader for ResumeGenerator"
```

---

## Task 4: Add Numbering Config Generator

**Files:**
- Modify: `~/.claude/skills/JobSearchToolkit/Templates/ResumeGenerator.js`

**Step 1: Add numbering config function after spec loader**

```javascript
// ─────────────────────────────────────────────────────────
// 2. NUMBERING CONFIG (bullet independence per job)
// ─────────────────────────────────────────────────────────

function generateNumberingConfig(experienceList, spec) {
  const b = spec.bullets;
  return {
    config: experienceList.map((_, idx) => ({
      reference: `job-${idx}-bullets`,
      levels: [{
        level: 0,
        format: LevelFormat.BULLET,
        text: b.character,
        alignment: AlignmentType.LEFT,
        style: {
          paragraph: {
            indent: { left: b.indent_left, hanging: b.indent_hanging }
          }
        }
      }]
    }))
  };
}
```

**Step 2: Add test for numbering config**

Update the `if (require.main === module)` block:

```javascript
if (require.main === module) {
  const spec = loadSpec(path.join(__dirname, 'resume-spec.yaml'));
  console.log('Loaded spec version:', spec.meta.version);

  // Test numbering config
  const testExperience = [{}, {}, {}]; // 3 jobs
  const numConfig = generateNumberingConfig(testExperience, spec);
  console.log('Numbering configs:', numConfig.config.length);
  console.log('First job ref:', numConfig.config[0].reference);
  console.log('Bullet char:', numConfig.config[0].levels[0].text);
}
```

**Step 3: Test numbering config**

Run: `cd ~/.claude/skills/JobSearchToolkit/Templates && node ResumeGenerator.js`
Expected:
```
Loaded spec version: 1.0
Numbering configs: 3
First job ref: job-0-bullets
Bullet char: ●
```

**Step 4: Commit**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add Templates/ResumeGenerator.js
git commit -m "feat: add numbering config for bullet independence"
```

---

## Task 5: Add Header Builder

**Files:**
- Modify: `~/.claude/skills/JobSearchToolkit/Templates/ResumeGenerator.js`

**Step 1: Add buildHeader function**

```javascript
// ─────────────────────────────────────────────────────────
// 3. SECTION BUILDERS
// ─────────────────────────────────────────────────────────

function buildHeader(data, spec) {
  const t = spec.typography;
  const contact = data.header.contact;
  const contactLine = [contact.location, contact.phone, contact.email, contact.linkedin]
    .filter(Boolean).join(t.contact.separator);

  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: data.header.name.toUpperCase(), bold: t.name.bold, size: t.name.size })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: t.contact.spacing_before },
      children: [new TextRun({ text: contactLine, size: t.contact.size })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: t.professional_title.spacing_before },
      children: [new TextRun({ text: data.professional_title.toUpperCase(), bold: t.professional_title.bold, size: t.professional_title.size })]
    }),
    new Paragraph({
      spacing: { before: t.summary.spacing_before },
      children: [new TextRun({ text: data.summary, size: t.summary.size })]
    })
  ];
}
```

**Step 2: Add test for header builder**

Update the test block:

```javascript
if (require.main === module) {
  const spec = loadSpec(path.join(__dirname, 'resume-spec.yaml'));

  const testData = {
    header: {
      name: "John Doe",
      contact: { location: "Chicago, IL", phone: "555-1234", email: "john@test.com", linkedin: "linkedin.com/in/johndoe" }
    },
    professional_title: "Software Engineer",
    summary: "Experienced engineer with 5+ years..."
  };

  const headerParas = buildHeader(testData, spec);
  console.log('Header paragraphs:', headerParas.length);
  console.log('First para type:', headerParas[0].constructor.name);
}
```

**Step 3: Test header builder**

Run: `cd ~/.claude/skills/JobSearchToolkit/Templates && node ResumeGenerator.js`
Expected:
```
Header paragraphs: 4
First para type: Paragraph
```

**Step 4: Commit**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add Templates/ResumeGenerator.js
git commit -m "feat: add header section builder"
```

---

## Task 6: Add Skills Builder

**Files:**
- Modify: `~/.claude/skills/JobSearchToolkit/Templates/ResumeGenerator.js`

**Step 1: Add buildSkills function**

```javascript
function buildSkills(data, spec) {
  const t = spec.typography;
  const paragraphs = [
    new Paragraph({
      spacing: { before: t.section_header.spacing_before_first },
      children: [new TextRun({ text: "SKILLS AND TOOLS", bold: t.section_header.bold, size: t.section_header.size })]
    })
  ];

  Object.entries(data.skills).forEach(([category, items]) => {
    paragraphs.push(new Paragraph({
      spacing: { before: t.skill_category.spacing_before },
      children: [
        new TextRun({ text: `${category}: `, bold: t.skill_category.label_bold, size: t.skill_category.label_size }),
        new TextRun({ text: items.join(", "), size: t.skill_category.items_size })
      ]
    }));
  });

  return paragraphs;
}
```

**Step 2: Test skills builder**

Add to test block:

```javascript
  const testData = {
    // ... existing header data
    skills: {
      "Technical": ["Python", "JavaScript", "SQL"],
      "Tools": ["Git", "Docker", "AWS"]
    }
  };

  const skillsParas = buildSkills(testData, spec);
  console.log('Skills paragraphs:', skillsParas.length); // 1 header + 2 categories = 3
```

**Step 3: Run test**

Run: `cd ~/.claude/skills/JobSearchToolkit/Templates && node ResumeGenerator.js`
Expected: `Skills paragraphs: 3`

**Step 4: Commit**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add Templates/ResumeGenerator.js
git commit -m "feat: add skills section builder"
```

---

## Task 7: Add Experience Builder

**Files:**
- Modify: `~/.claude/skills/JobSearchToolkit/Templates/ResumeGenerator.js`

**Step 1: Add buildExperience function**

```javascript
function buildExperience(data, spec) {
  const t = spec.typography;
  const exp = t.experience;

  const paragraphs = [
    new Paragraph({
      spacing: { before: t.section_header.spacing_before_subsequent },
      children: [new TextRun({ text: "EXPERIENCE", bold: t.section_header.bold, size: t.section_header.size })]
    })
  ];

  data.experience.forEach((job, jobIdx) => {
    const isFirst = jobIdx === 0;

    // Company | Location
    paragraphs.push(new Paragraph({
      spacing: { before: isFirst ? exp.company.spacing_before_first : exp.company.spacing_before_subsequent },
      indent: { left: exp.company.indent_left },
      children: [new TextRun({ text: `${job.company} | ${job.location}`, bold: exp.company.bold, size: exp.company.size })]
    }));

    // Title | Dates
    paragraphs.push(new Paragraph({
      indent: { left: exp.title.indent_left },
      children: [new TextRun({ text: `${job.title} | ${job.dates}`, size: exp.title.size })]
    }));

    // Bullets
    job.bullets.forEach((bullet, bulletIdx) => {
      paragraphs.push(new Paragraph({
        numbering: { reference: `job-${jobIdx}-bullets`, level: 0 },
        spacing: {
          before: bulletIdx === 0 ? exp.bullet.spacing_before_first : exp.bullet.spacing_before_subsequent,
          line: exp.bullet.line_spacing
        },
        children: [new TextRun({ text: bullet, size: exp.bullet.size })]
      }));
    });
  });

  return paragraphs;
}
```

**Step 2: Test experience builder**

Add to test block:

```javascript
  const testData = {
    // ... existing data
    experience: [
      { company: "Acme Corp", location: "Chicago, IL", title: "Engineer", dates: "2020-Present", bullets: ["Built X", "Led Y"] },
      { company: "StartupCo", location: "Remote", title: "Developer", dates: "2018-2020", bullets: ["Created Z"] }
    ]
  };

  const expParas = buildExperience(testData, spec);
  console.log('Experience paragraphs:', expParas.length); // 1 header + (2+2+2) + (2+2+1) = 1 + 6 + 5 = 12
```

**Step 3: Run test**

Run: `cd ~/.claude/skills/JobSearchToolkit/Templates && node ResumeGenerator.js`
Expected: `Experience paragraphs: 10` (1 header + 2 jobs × (company + title) + 3 bullets)

**Step 4: Commit**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add Templates/ResumeGenerator.js
git commit -m "feat: add experience section builder with bullet independence"
```

---

## Task 8: Add Education Builder

**Files:**
- Modify: `~/.claude/skills/JobSearchToolkit/Templates/ResumeGenerator.js`

**Step 1: Add buildEducation function**

```javascript
function buildEducation(data, spec) {
  const t = spec.typography;
  return [
    new Paragraph({
      spacing: { before: t.section_header.spacing_before_subsequent },
      children: [new TextRun({ text: "EDUCATION", bold: t.section_header.bold, size: t.section_header.size })]
    }),
    new Paragraph({
      children: [new TextRun({ text: data.education, size: t.education.size })]
    })
  ];
}
```

**Step 2: Test education builder**

Add to test block:

```javascript
  const testData = {
    // ... existing data
    education: "Northwestern University | B.S. Computer Science | 2020"
  };

  const eduParas = buildEducation(testData, spec);
  console.log('Education paragraphs:', eduParas.length); // 2
```

**Step 3: Run test**

Run: `cd ~/.claude/skills/JobSearchToolkit/Templates && node ResumeGenerator.js`
Expected: `Education paragraphs: 2`

**Step 4: Commit**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add Templates/ResumeGenerator.js
git commit -m "feat: add education section builder"
```

---

## Task 9: Add Main Generator Function

**Files:**
- Modify: `~/.claude/skills/JobSearchToolkit/Templates/ResumeGenerator.js`

**Step 1: Add generateResume async function**

```javascript
// ─────────────────────────────────────────────────────────
// 4. MAIN GENERATOR
// ─────────────────────────────────────────────────────────

async function generateResume(data, spec, outputPath) {
  if (!data.header?.name || !data.experience?.length) {
    throw new Error('Missing required fields: header.name or experience');
  }

  const doc = new Document({
    styles: {
      default: {
        document: {
          run: { font: spec.defaults.font, size: spec.defaults.line_spacing }
        }
      }
    },
    numbering: generateNumberingConfig(data.experience, spec),
    sections: [{
      properties: {
        page: { margin: spec.page.margins }
      },
      children: [
        ...buildHeader(data, spec),
        ...buildSkills(data, spec),
        ...buildExperience(data, spec),
        ...buildEducation(data, spec)
      ]
    }]
  });

  const buffer = await Packer.toBuffer(doc);
  await fs.promises.writeFile(outputPath, buffer);
  return outputPath;
}
```

**Step 2: Commit**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add Templates/ResumeGenerator.js
git commit -m "feat: add main generateResume function"
```

---

## Task 10: Add CLI Entry Point

**Files:**
- Modify: `~/.claude/skills/JobSearchToolkit/Templates/ResumeGenerator.js`

**Step 1: Replace test block with CLI entry point**

```javascript
// ─────────────────────────────────────────────────────────
// 5. CLI ENTRY POINT
// ─────────────────────────────────────────────────────────

if (require.main === module) {
  (async () => {
    try {
      const dataPath = process.argv[2];
      const companyName = process.argv[3] || 'Company';

      if (!dataPath) {
        console.error('Usage: node ResumeGenerator.js <data.json> [company_name]');
        process.exit(1);
      }

      const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
      const spec = loadSpec(path.join(__dirname, 'resume-spec.yaml'));

      const outputDir = path.join(os.homedir(), 'Downloads');
      const safeName = data.header.name.replace(/\s+/g, '_');
      const safeCompany = companyName.replace(/\s+/g, '_');
      const outputPath = path.join(outputDir, `${safeName}_Resume_${safeCompany}.docx`);

      await generateResume(data, spec, outputPath);
      console.log(outputPath);
    } catch (err) {
      console.error(`Error: ${err.message}`);
      process.exit(1);
    }
  })();
}

module.exports = { generateResume, loadSpec };
```

**Step 2: Commit**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add Templates/ResumeGenerator.js
git commit -m "feat: add CLI entry point for ResumeGenerator"
```

---

## Task 11: Create Test Data File

**Files:**
- Create: `~/.claude/skills/JobSearchToolkit/Templates/test-resume-data.json`

**Step 1: Create comprehensive test data**

```json
{
  "header": {
    "name": "IDREES KAMAL",
    "contact": {
      "location": "Chicago, IL",
      "phone": "(773) 789-0400",
      "email": "ikamal97@gmail.com",
      "linkedin": "linkedin.com/in/idreeskamal"
    }
  },
  "professional_title": "BUSINESS SYSTEMS ANALYST",
  "summary": "Business Systems Analyst with Deloitte and Oliver Wyman background. Expert in CRM implementation, data migration, and workflow automation. Built end-to-end client onboarding systems reducing effort by 60%.",
  "skills": {
    "Implementation & Delivery": ["Client Onboarding", "Data Migration", "Requirements Gathering", "UAT"],
    "Technical Skills": ["SQL", "Python", "API Integrations", "Workflow Automation"],
    "Tools & Platforms": ["Salesforce", "HubSpot", "Notion", "Jira"]
  },
  "experience": [
    {
      "company": "KAVALIER",
      "location": "Chicago, IL",
      "title": "Business Systems Analyst",
      "dates": "Sep 2024 to Present",
      "bullets": [
        "Built end-to-end onboarding workflow reducing client setup from 3-5 hours to 1-2 hours",
        "Implemented CRM automation and led data migration of 700+ client records"
      ]
    },
    {
      "company": "OLIVER WYMAN",
      "location": "Chicago, IL",
      "title": "Business Analyst",
      "dates": "Jan 2022 to Aug 2024",
      "bullets": [
        "Developed predictive retention models identifying at-risk customer segments",
        "Created executive dashboards translating complex datasets into actionable insights"
      ]
    },
    {
      "company": "DELOITTE",
      "location": "Chicago, IL",
      "title": "Analyst",
      "dates": "Jun 2020 to Dec 2021",
      "bullets": [
        "Supported digital transformation initiatives across enterprise clients",
        "Built financial models and executive dashboards for leadership decision-making"
      ]
    }
  ],
  "education": "Northwestern University | B.S. Computer Science | Sep 2017 to Jun 2020"
}
```

**Step 2: Commit**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add Templates/test-resume-data.json
git commit -m "test: add test data for resume generator"
```

---

## Task 12: End-to-End Test

**Files:**
- None (verification only)

**Step 1: Generate test resume**

Run: `cd ~/.claude/skills/JobSearchToolkit/Templates && node ResumeGenerator.js test-resume-data.json TestCompany`
Expected: `/Users/idreeskamal/Downloads/IDREES_KAMAL_Resume_TestCompany.docx`

**Step 2: Verify file exists**

Run: `ls -la ~/Downloads/IDREES_KAMAL_Resume_TestCompany.docx`
Expected: File exists with non-zero size

**Step 3: Open and visually verify**

Run: `open ~/Downloads/IDREES_KAMAL_Resume_TestCompany.docx`
Expected: Document opens in Word with correct formatting

**Step 4: Commit (if any fixes needed)**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add -A
git commit -m "fix: address issues found in end-to-end test"
```

---

## Task 13: Update ResumeTailoring Workflow

**Files:**
- Modify: `~/.claude/skills/JobSearchToolkit/Workflows/ResumeTailoring.md`

**Step 1: Update Step 7 to use Node generator**

Find the Step 7 section and replace the Python code block with:

```markdown
## Step 7: Generate DOCX from Spec

Use the spec-driven generator:

1. Write tailored data to temp file:
```bash
echo '$TAILORED_JSON' > /tmp/resume_data.json
```

2. Generate DOCX:
```bash
node ~/.claude/skills/JobSearchToolkit/Templates/ResumeGenerator.js /tmp/resume_data.json "CompanyName"
```

3. Verify one page (if needed):
```bash
python ~/.claude/skills/JobSearchToolkit/Tools/verify_page_count.py ~/Downloads/Name_Resume_Company.docx
```

**File naming**: `FirstName_LastName_Resume_CompanyName.docx`
**Output location**: `~/Downloads/`
```

**Step 2: Commit**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add Workflows/ResumeTailoring.md
git commit -m "feat: update workflow to use spec-driven generator"
```

---

## Task 14: Validation - Compare with Python Output

**Files:**
- None (verification only)

**Step 1: Generate resume with current Python processor**

Run: `cd ~/.claude/skills/JobSearchToolkit/Templates && python -c "from TemplateProcessor import generate_resume_from_template; ..." 2>/dev/null || echo "Python generator may need template file"`

**Step 2: Generate same resume with Node**

Run: `node ResumeGenerator.js test-resume-data.json ValidationTest`

**Step 3: Visual comparison**

Open both DOCXs side-by-side in Word and verify:
- [ ] Font sizes match
- [ ] Spacing matches
- [ ] Bullet indentation matches
- [ ] Page margins match

**Step 4: Document any differences**

If differences found, adjust resume-spec.yaml values and regenerate.

---

## Task 15: Cleanup (After Validation)

**Files:**
- Delete: `~/.claude/skills/JobSearchToolkit/Templates/TemplateProcessor.py`
- Delete: `~/.claude/skills/JobSearchToolkit/Templates/simple_template_processor.py`

**Step 1: Remove Python files (only after successful validation)**

Run: `rm ~/.claude/skills/JobSearchToolkit/Templates/TemplateProcessor.py ~/.claude/skills/JobSearchToolkit/Templates/simple_template_processor.py`

**Step 2: Remove pycache**

Run: `rm -rf ~/.claude/skills/JobSearchToolkit/Templates/__pycache__`

**Step 3: Final commit**

```bash
cd ~/.claude/skills/JobSearchToolkit
git add -A
git commit -m "chore: remove deprecated Python template processors"
```

---

## Summary

| Task | Description | Est. Time |
|------|-------------|-----------|
| 1 | Add js-yaml dependency | 2 min |
| 2 | Create resume-spec.yaml | 3 min |
| 3 | Spec loader | 3 min |
| 4 | Numbering config | 3 min |
| 5 | Header builder | 3 min |
| 6 | Skills builder | 3 min |
| 7 | Experience builder | 5 min |
| 8 | Education builder | 2 min |
| 9 | Main generator | 3 min |
| 10 | CLI entry point | 3 min |
| 11 | Test data file | 3 min |
| 12 | End-to-end test | 5 min |
| 13 | Update workflow | 3 min |
| 14 | Validation comparison | 10 min |
| 15 | Cleanup | 2 min |

**Total: ~50 minutes**
