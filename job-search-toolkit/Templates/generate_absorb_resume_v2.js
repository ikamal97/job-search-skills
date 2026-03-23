const { Document, Packer, Paragraph, TextRun, AlignmentType } = require('docx');
const fs = require('fs');

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Calibri", size: 22 }
      }
    }
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      // Header
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 120 },
        children: [
          new TextRun({ text: "IDREES KAMAL", bold: true, size: 28 }),
          new TextRun({ text: "\nChicago, IL | (773) 789-0400 | ikamal97@gmail.com | linkedin.com/in/idreeskamal", size: 20 })
        ]
      }),

      // Summary Section
      new Paragraph({
        spacing: { before: 120, after: 60 },
        children: [new TextRun({ text: "SALES OPERATIONS ANALYST", bold: true, size: 22 })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        alignment: AlignmentType.JUSTIFIED,
        children: [new TextRun({
          text: "Sales Operations Analyst with 4+ years of experience in revenue operations, pipeline analytics, and CRM automation, delivering data-driven insights through Excel modeling (pivot tables, VLOOKUP, advanced formulas), SQL analysis, and lead routing optimization. Proven track record building operational systems that drive revenue growth and streamline sales processes in high-growth tech environments. Strong expertise in data hygiene, financial analysis, and cross-functional collaboration with Sales, Marketing, and Operations teams."
        })]
      }),

      // Skills
      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({ text: "SKILLS AND TOOLS", bold: true, size: 22 })]
      }),
      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({
          text: "Revenue Operations: Pipeline reporting, revenue analytics, bookings analysis, lead routing, sales operations\n\nData & Analytics: Excel (pivot tables, VLOOKUP, formulas), SQL, Python, data hygiene, data governance, financial modeling\n\nCRM Operations: CRM automation, lead distribution, data migration, account management, workflow optimization\n\nRequirements & Process: BRD/FRD, user stories, acceptance criteria, process mapping, UAT\n\nTools: Jira, Confluence, Notion, Excel, SQL, Python, GoHighLevel (CRM), Stripe (payment ops)"
        })]
      }),

      // Experience
      new Paragraph({
        spacing: { before: 120, after: 120 },
        children: [new TextRun({ text: "PROFESSIONAL EXPERIENCE", bold: true, size: 22 })]
      }),

      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({ text: "Business Systems Analyst | Kavalier | Chicago, IL | Sep 2024 to Present", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({
          text: "• Built end-to-end revenue operations workflow across CRM (GoHighLevel) and payment platform (Stripe), automating client onboarding, lead routing, and waiver delivery with stage-gate enforcement, reducing onboarding effort from 3–5 hours to 1–2 hours per client\n\n• Designed CRM data model in Notion to centralize pipeline tracking, client lifecycle management, and delivery workflows, establishing data governance standards that reduced missed onboarding steps by 60% through standardized fields and required-stage completion\n\n• Performed UAT-style testing and defect triage on CRM automation workflows, identifying and resolving data integrity issues to ensure accurate lead distribution and reporting, saving ~3–5 hours per week through workflow optimization"
        })]
      }),

      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({ text: "Business Operations Analyst | Vicegerent Custom Clothiers | Chicago, IL | Jun 2022 to Sep 2024", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({
          text: "• Implemented Notion-based CRM and operations hub, migrating 700+ client records from Google Sheets with data governance rules, establishing customer lifecycle stages and standardized fields to centralize order tracking and pipeline visibility\n\n• Led data migration and data hygiene initiative using Python scripts to clean and normalize legacy data, then owned ongoing data quality through governance standards that ensured consistent data entry across operations and sales teams\n\n• Authored SOPs and training documentation for order entry, production updates, and alterations tracking, enabling consistent operational execution and reducing errors by 40% through standardized processes"
        })]
      }),

      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({ text: "Senior Consultant | Oliver Wyman | Chicago, IL | Mar 2022 to Jun 2022", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({
          text: "• Drove revenue operations strategy across Product, Engineering, and Marketing, quantifying revenue impact through financial modeling and supporting retention initiatives projected to reduce churn by 23% and increase customer lifetime value\n\n• Developed predictive analytics models in Python using customer behavioral data to identify at-risk segments for pipeline forecasting and revenue optimization for major US telecom client"
        })]
      }),

      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({ text: "Business Analyst | Deloitte Consulting LLP | Chicago, IL | Oct 2020 to Mar 2022", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({
          text: "• Built executive dashboards and financial models in Excel (pivot tables, VLOOKUP, scenario analysis) to translate complex datasets into pipeline reports and revenue forecasts for C-suite stakeholders\n\n• Authored BRDs and FRDs documenting business requirements, functional specifications, and data requirements, translating stakeholder needs into technical specifications for sales operations systems\n\n• Executed UAT by creating test plans and tracking defects in Jira, ensuring data accuracy and system functionality before go-live for enterprise implementations\n\n• Supported Agile delivery through backlog refinement and sprint ceremonies, maintaining story readiness with clear acceptance criteria and test coverage for cross-functional teams"
        })]
      }),

      // Education
      new Paragraph({
        spacing: { before: 120, after: 60 },
        children: [new TextRun({ text: "EDUCATION", bold: true, size: 22 })]
      }),
      new Paragraph({
        children: [new TextRun({ text: "Northwestern University | B.S. Computer Science | Sep 2017 to Jun 2020" })]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  const outputPath = "/Users/idreeskamal/Downloads/Idrees_Kamal_Resume_Absorb_Software_v2.docx";
  fs.writeFileSync(outputPath, buffer);
  console.log("✓ Clean resume created: " + outputPath);
});
