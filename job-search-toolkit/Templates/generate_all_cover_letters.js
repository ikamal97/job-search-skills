const { Document, Packer, Paragraph, TextRun, AlignmentType } = require('docx');
const fs = require('fs');
const path = require('path');

// Base output directory
const BASE_OUTPUT_DIR = "/Users/idreeskamal/Documents/Obsidian Vault/04 - Career/Generated Assets";

// Cover letter data for each company
const COVER_LETTERS = {
  "Vetcove": {
    hiring_manager: "Jennifer Bedard",
    company: "Vetcove",
    location: "Remote",
    date: "January 14, 2026",
    opening: "I am writing to express my interest in the SaaS Implementation Manager position at Vetcove. With 6+ years of experience leading end-to-end SaaS implementation lifecycles—from discovery and configuration to training and go-live—I bring both technical depth and client success orientation to platform onboarding.",
    body1: "At Kavalier, I built an end-to-end SaaS onboarding workflow across GoHighLevel and Stripe, automating client onboarding, payment processing, and waiver delivery. I implemented a Notion CRM system of record for client delivery by defining structured data models, reducing missed onboarding steps through standardized fields and stage-gate completion rules. Through UAT-style testing and defect triage, I reduced onboarding effort from 3-5 hours to 1-2 hours per client. At Vicegerent, I implemented a Notion-based CRM and migrated 700+ client records from spreadsheets, establishing lifecycle stages and standardized fields to centralize customer tracking. I built client onboarding automations using Calendly and Zapier integrations, reducing manual coordination by 80%.",
    body2: "My Computer Science background from Northwestern enables me to troubleshoot technical issues effectively and work closely with engineering teams. At Deloitte, I led enterprise software implementations for Fortune 500 clients, coordinating discovery, configuration, UAT, and go-live across technical and business stakeholders. I authored BRDs and FRDs to translate stakeholder needs into functional requirements, executed UAT by creating test plans and tracking defects in Jira, and supported Agile delivery through sprint ceremonies and backlog refinement.",
    body3: "What excites me about Vetcove is the opportunity to support veterinary practices through innovative B2B marketplace technology. I'm drawn to roles where I can be the bridge between technical capabilities and customer success—ensuring smooth implementations, training teams effectively, and building long-term client relationships through reliable platform delivery.",
    closing: "I would welcome the opportunity to discuss how my SaaS implementation experience can support Vetcove's veterinary clients. Thank you for your consideration. I am available at your convenience and look forward to speaking with you."
  },
  "Process Street": {
    hiring_manager: "Hiring Manager",
    company: "Process Street",
    location: "Remote",
    date: "January 14, 2026",
    opening: "I am writing to express my interest in the Junior Solutions Engineer position at Process Street. With 6+ years of experience in technical discovery, API integrations, and no-code workflow automation, I bring a unique blend of technical capability and client-facing communication that aligns well with solutions engineering.",
    body1: "At Kavalier, I built end-to-end workflow automation across GoHighLevel and Stripe APIs, integrating payment processing, CRM automation, and client onboarding through no-code configuration. I implemented Notion API integrations with Calendly and Zapier to automate client scheduling, data sync, and lifecycle stage tracking. Through UAT-style testing and troubleshooting, I identified and resolved integration issues, reducing onboarding effort by 60%. At Vicegerent, I built client onboarding automations using Calendly API and Zapier integrations, connecting scheduling data to Notion CRM for automated client record creation. I also implemented data migration from Google Sheets to Notion using API-based ETL scripts, migrating 700+ client records with validation and error handling.",
    body2: "My technical discovery and requirements gathering experience comes from Deloitte, where I conducted stakeholder discovery sessions to elicit requirements and define functional specifications for enterprise software implementations. I built demonstrations and proofs of concept for technical solutions, presenting to stakeholders and iterating based on feedback. I translated business requirements into user stories and acceptance criteria for technical implementation teams, supporting Agile delivery through sprint ceremonies and backlog refinement.",
    body3: "What excites me about Process Street is the opportunity to work at a workflow automation platform company—helping customers build reliable processes through technical solutions. I'm drawn to roles where I can combine technical problem-solving with customer success, demonstrating product capabilities and building trust through reliable delivery.",
    closing: "I would welcome the opportunity to discuss how my technical and client-facing experience can contribute to Process Street's solutions engineering team. Thank you for your consideration. I am available at your convenience and look forward to speaking with you."
  },
  "Motorola Solutions": {
    hiring_manager: "Scott Shepard",
    company: "Motorola Solutions",
    location: "Remote",
    date: "January 14, 2026",
    opening: "I am writing to express my interest in the IT Business Systems Analyst position at Motorola Solutions. With 6+ years of experience in requirements gathering, process optimization, and stakeholder management across enterprise IT transformations, I bring proven capabilities in Agile methodologies, UAT, and cross-functional alignment that align with your needs.",
    body1: "At Deloitte, I served as a Business Analyst supporting Fortune 500 clients through enterprise IT transformations. I authored BRDs and FRDs to translate stakeholder needs into functional requirements, including business rules, functional specs, and edge cases. I built swimlane as-is/to-be process maps in Visio and translated requirements into user stories and acceptance criteria to guide implementation planning. I executed UAT by creating test plans and test cases and tracking defects in Jira, building executive dashboards and scenario models to support data-driven decisions. I supported Agile delivery by participating in backlog refinement and sprint ceremonies, maintaining story readiness and supporting go-live readiness activities.",
    body2: "At Kavalier and Vicegerent, I applied these same business analysis capabilities to build operational systems from the ground up. At Kavalier, I built an end-to-end onboarding workflow across GoHighLevel and Stripe, automating processes and enforcing stage-gate rules. I built a Notion-based system of record by defining structured data models, reducing missed steps through standardized fields and required-stage completion. Through UAT-style testing and defect triage, I reduced onboarding effort from 3-5 hours to 1-2 hours per client. At Vicegerent, I implemented a Notion CRM and migrated 700+ client records, establishing lifecycle stages and standardized fields. I cleaned and normalized legacy data using Python scripts and owned ongoing data quality to ensure consistent team entry.",
    body3: "My Computer Science background from Northwestern provides the technical foundation to understand complex IT architectures and translate them into business value. At Oliver Wyman, I drove cross-functional alignment across Product, Engineering, and Marketing to define customer retention strategy, developing predictive retention models in Python using behavioral data to identify at-risk customer segments.",
    closing: "I would welcome the opportunity to discuss how my enterprise IT background and business analysis capabilities can support Motorola Solutions' needs. Thank you for your consideration. I am available at your convenience and look forward to speaking with you."
  },
  "HockeyStack": {
    hiring_manager: "Hiring Manager",
    company: "HockeyStack",
    location: "Remote",
    date: "January 14, 2026",
    opening: "I am writing to express my interest in the Implementation Manager position at HockeyStack. With 6+ years of experience leading analytics platform implementations, dashboard configuration, and data pipeline setup, I bring proven capabilities in marketing analytics and revenue tracking that align with your attribution platform needs.",
    body1: "At Kavalier, I built end-to-end analytics tracking across GoHighLevel and Stripe, implementing revenue reporting dashboards and client lifecycle analytics to track conversion rates and retention metrics. I implemented a Notion CRM system with structured data models for client tracking, lifecycle stages, and pipeline analytics, enabling data-driven business decisions. Through UAT-style testing and data validation on analytics automations, I ensured accurate reporting and reduced manual data entry effort by 60%. At Vicegerent, I implemented a Notion-based CRM and analytics hub and migrated 700+ client records from Google Sheets, establishing data pipelines for customer, order, and revenue tracking. I built marketing analytics dashboards tracking social media performance across Instagram, Facebook, TikTok, and LinkedIn, measuring engagement rates, impressions, and follower growth.",
    body2: "My analytics implementation experience extends to enterprise environments. At Deloitte, I led implementation of enterprise analytics platforms for Fortune 500 clients, coordinating discovery, configuration, UAT, and go-live across technical and business stakeholders. I built executive dashboards and scenario models in Excel to visualize business metrics and support data-driven decision-making. I executed UAT by creating test plans and test cases for analytics implementations, tracking defects in Jira and ensuring data accuracy. At Oliver Wyman, I drove implementation of customer retention analytics strategy, building predictive models in Python to identify at-risk customer segments and track retention metrics. I quantified revenue impact of retention initiatives and built analytics dashboards for executive stakeholders, projecting 23% churn reduction.",
    body3: "What excites me about HockeyStack is the opportunity to work at a marketing attribution platform—helping B2B companies understand their customer journey and revenue drivers through reliable analytics. I'm drawn to roles where I can combine technical implementation capabilities with customer success, ensuring clients derive maximum value from analytics platforms through clean data pipelines and actionable dashboards.",
    closing: "I would welcome the opportunity to discuss how my analytics implementation experience can support HockeyStack's customers. Thank you for your consideration. I am available at your convenience and look forward to speaking with you."
  }
};

function generateCoverLetter(companyName, data) {
  console.log(`\nGenerating cover letter for ${companyName}...`);

  const doc = new Document({
    styles: {
      default: {
        document: {
          run: { font: "Calibri", size: 22 } // 11pt
        }
      }
    },
    sections: [{
      properties: {
        page: {
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 inch margins
        }
      },
      children: [
        // Header with contact info
        new Paragraph({
          alignment: AlignmentType.LEFT,
          spacing: { after: 0 },
          children: [new TextRun({ text: "IDREES KAMAL", bold: true, size: 24 })]
        }),
        new Paragraph({
          alignment: AlignmentType.LEFT,
          spacing: { after: 0 },
          children: [new TextRun({ text: "Chicago, IL | (773) 789-0400 | ikamal97@gmail.com | linkedin.com/in/idreeskamal", size: 20 })]
        }),
        new Paragraph({
          spacing: { after: 240 },
          children: [new TextRun({ text: "" })]
        }),

        // Date
        new Paragraph({
          spacing: { after: 240 },
          children: [new TextRun({ text: data.date })]
        }),

        // Recipient
        new Paragraph({
          spacing: { after: 0 },
          children: [new TextRun({ text: data.hiring_manager })]
        }),
        new Paragraph({
          spacing: { after: 0 },
          children: [new TextRun({ text: data.company })]
        }),
        new Paragraph({
          spacing: { after: 240 },
          children: [new TextRun({ text: data.location })]
        }),

        // Salutation
        new Paragraph({
          spacing: { after: 240 },
          children: [new TextRun({ text: `Dear ${data.hiring_manager},` })]
        }),

        // Opening paragraph
        new Paragraph({
          spacing: { after: 240 },
          alignment: AlignmentType.JUSTIFIED,
          children: [new TextRun({ text: data.opening })]
        }),

        // Body paragraph 1
        new Paragraph({
          spacing: { after: 240 },
          alignment: AlignmentType.JUSTIFIED,
          children: [new TextRun({ text: data.body1 })]
        }),

        // Body paragraph 2
        new Paragraph({
          spacing: { after: 240 },
          alignment: AlignmentType.JUSTIFIED,
          children: [new TextRun({ text: data.body2 })]
        }),

        // Body paragraph 3
        new Paragraph({
          spacing: { after: 240 },
          alignment: AlignmentType.JUSTIFIED,
          children: [new TextRun({ text: data.body3 })]
        }),

        // Closing paragraph
        new Paragraph({
          spacing: { after: 240 },
          alignment: AlignmentType.JUSTIFIED,
          children: [new TextRun({ text: data.closing })]
        }),

        // Signature
        new Paragraph({
          spacing: { after: 0 },
          children: [new TextRun({ text: "Sincerely," })]
        }),
        new Paragraph({
          spacing: { after: 0 },
          children: [new TextRun({ text: "Idrees Kamal" })]
        })
      ]
    }]
  });

  // Determine output path
  const outputDir = path.join(BASE_OUTPUT_DIR, companyName);
  const fileName = `Idrees_Kamal_CoverLetter_${companyName.replace(/\s+/g, '_')}.docx`;
  const outputPath = path.join(outputDir, fileName);

  // Generate and save
  Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(outputPath, buffer);
    console.log(`✓ Cover letter generated: ${outputPath}`);
  });

  return outputPath;
}

function main() {
  console.log("=" * 70);
  console.log("GENERATING COVER LETTERS FOR TOP 4 FIT SCORE JOBS");
  console.log("=" * 70);

  const results = {};

  for (const [companyName, data] of Object.entries(COVER_LETTERS)) {
    try {
      const coverLetterPath = generateCoverLetter(companyName, data);
      results[companyName] = {
        coverLetter: coverLetterPath,
        success: true
      };
    } catch (error) {
      console.error(`✗ Error generating cover letter for ${companyName}:`, error);
      results[companyName] = {
        success: false,
        error: error.message
      };
    }
  }

  // Wait a bit for all async operations to complete
  setTimeout(() => {
    console.log("\n" + "=" * 70);
    console.log("GENERATION SUMMARY");
    console.log("=" * 70);

    for (const [companyName, result] of Object.entries(results)) {
      if (result.success) {
        console.log(`✓ ${companyName}: Cover letter generated successfully`);
      } else {
        console.log(`✗ ${companyName}: Failed - ${result.error}`);
      }
    }

    console.log("\n" + "=" * 70);
    console.log("ALL APPLICATION MATERIALS GENERATED");
    console.log("=" * 70);
    console.log("\nOutput structure:");
    console.log("04 - Career/Generated Assets/");
    console.log("├── Vetcove/");
    console.log("│   ├── Idrees_Kamal_Resume_Vetcove.docx");
    console.log("│   └── Idrees_Kamal_CoverLetter_Vetcove.docx");
    console.log("├── Process Street/");
    console.log("│   ├── Idrees_Kamal_Resume_Process_Street.docx");
    console.log("│   └── Idrees_Kamal_CoverLetter_Process_Street.docx");
    console.log("├── Motorola Solutions/");
    console.log("│   ├── Idrees_Kamal_Resume_Motorola_Solutions.docx");
    console.log("│   └── Idrees_Kamal_CoverLetter_Motorola_Solutions.docx");
    console.log("└── HockeyStack/");
    console.log("    ├── Idrees_Kamal_Resume_HockeyStack.docx");
    console.log("    └── Idrees_Kamal_CoverLetter_HockeyStack.docx");
    console.log("=" * 70);
  }, 2000); // 2 second delay to ensure all files are written
}

main();
