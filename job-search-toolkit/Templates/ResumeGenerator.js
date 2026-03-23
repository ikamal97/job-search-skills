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
// 0. LOCKED RESUME DATA - CUSTOMIZE FOR YOUR CAREER
// ─────────────────────────────────────────────────────────
// CUSTOMIZE: Replace these example values with your own career data.
// These fields are enforced by the generator at runtime.
// Input JSON only provides: professional_title, summary, skills, bullets

const LOCKED_RESUME_DATA = {
  header: {
    name: "Your Name",                           // CUSTOMIZE: Your full name
    contact: {
      location: "City, ST",                      // CUSTOMIZE: Your city, state
      phone: "(555) 123-4567",                   // CUSTOMIZE: Your phone number
      email: "user@example.com",                 // CUSTOMIZE: Your email
      linkedin: "linkedin.com/in/yourprofile"    // CUSTOMIZE: Your LinkedIn URL
    }
  },
  // CUSTOMIZE: Replace with your own work experience (reverse chronological)
  // Each entry: company name, location, title (null = dynamic from input), dates
  experience: [
    {
      company: "Company A",                      // CUSTOMIZE: Most recent employer
      location: "City, ST",
      title: null,  // DYNAMIC - provided in input JSON per job application
      dates: "Jan 2023 - Present"
    },
    {
      company: "Company B",                      // CUSTOMIZE: Previous employer
      location: "City, ST",
      title: null,  // DYNAMIC - provided in input JSON per job application
      dates: "Jun 2021 - Dec 2022"
    },
    {
      company: "Consulting Firm",                // CUSTOMIZE: Earlier employer
      location: "City, ST",
      title: "Senior Consultant",  // LOCKED - set title here if not dynamic
      dates: "Mar 2020 - Jun 2021"
    },
    {
      company: "Enterprise Corp",                // CUSTOMIZE: Earlier employer
      location: "City, ST",
      title: "Business Analyst",   // LOCKED - set title here if not dynamic
      dates: "Oct 2018 - Mar 2020"
    }
  ],
  education: "University Name | B.S. Your Major | Year - Year"  // CUSTOMIZE
};

// ─────────────────────────────────────────────────────────
// 0.5. MERGE INPUT WITH LOCKED DATA
// ─────────────────────────────────────────────────────────
// Input JSON provides: professional_title, summary, skills, bullets[], titles (for dynamic-title jobs)
// Locked data provides: header, experience (company/location/dates), education
// Titles: Jobs 1 & 2 = DYNAMIC (from input), Jobs 3 & 4 = LOCKED (from LOCKED_RESUME_DATA)

function mergeWithLockedData(input) {
  // Validate bullets array
  if (!input.bullets || !Array.isArray(input.bullets)) {
    throw new Error('Input must include bullets array with 4 sub-arrays (one per job)');
  }
  if (input.bullets.length !== 4) {
    throw new Error(`Expected 4 bullet arrays (one per job), got ${input.bullets.length}`);
  }

  // Validate titles for dynamic positions
  if (!input.titles || !input.titles.job1 || !input.titles.job2) {
    throw new Error('Input must include titles.job1 and titles.job2 (these are dynamic per job posting)');
  }

  // Merge experience: locked fields + input bullets + dynamic titles
  const experience = LOCKED_RESUME_DATA.experience.map((job, idx) => {
    let title = job.title;  // Use locked title if set

    // Dynamic titles for Job 1 (idx 0) and Job 2 (idx 1)
    if (idx === 0) title = input.titles.job1;
    if (idx === 1) title = input.titles.job2;

    return {
      ...job,
      title,
      bullets: input.bullets[idx] || []
    };
  });

  return {
    header: LOCKED_RESUME_DATA.header,
    professional_title: input.professional_title || "Professional",
    summary: input.summary || "",
    skills: input.skills || {},
    experience,
    education: LOCKED_RESUME_DATA.education
  };
}

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
          },
          run: {
            size: b.size || 16  // Bullet character size (8pt = 16 half-points)
          }
        }
      }]
    }))
  };
}

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
        console.error('');
        console.error('Input JSON format:');
        console.error(JSON.stringify({
          professional_title: "Job Title",
          summary: "Professional summary...",
          skills: { "Category": ["Skill1", "Skill2"] },
          titles: {
            job1: "Your Title at Job 1",
            job2: "Your Title at Job 2"
          },
          bullets: [
            ["Company A bullet 1", "Company A bullet 2"],
            ["Company B bullet 1", "Company B bullet 2"],
            ["Consulting Firm bullet 1", "Consulting Firm bullet 2"],
            ["Enterprise Corp bullet 1", "Enterprise Corp bullet 2"]
          ]
        }, null, 2));
        console.error('');
        console.error('LOCKED: Company names, locations, dates, Job 3 title, Job 4 title');
        console.error('DYNAMIC: professional_title, summary, skills, bullets, Job 1 title, Job 2 title');
        process.exit(1);
      }

      const input = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
      const data = mergeWithLockedData(input);
      const spec = loadSpec(path.join(__dirname, 'resume-spec.yaml'));

      const outputDir = path.join(os.homedir(), 'Downloads');
      const safeName = LOCKED_RESUME_DATA.header.name.replace(/\s+/g, '_');
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
