const { Document, Packer, Paragraph, TextRun, AlignmentType } = require('docx');
const fs = require('fs');

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
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      // HEADER
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 0 },
        children: [new TextRun({ text: "YOUR NAME", bold: true, size: 28 })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 240 },
        children: [new TextRun({ text: "Chicago, IL | (555) 123-4567 | user@example.com | linkedin.com/in/yourprofile", size: 20 })]
      }),

      // PROFESSIONAL SUMMARY (Enhanced with sales ops keywords)
      new Paragraph({
        spacing: { after: 0 },
        children: [new TextRun({ text: "SALES OPERATIONS ANALYST", bold: true, size: 22 })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        alignment: AlignmentType.JUSTIFIED,
        children: [new TextRun({
          text: "Sales Operations Analyst with 4+ years of experience in revenue operations, pipeline analytics, and CRM automation, delivering data-driven insights through Excel modeling (pivot tables, VLOOKUP, advanced formulas), SQL analysis, and lead routing optimization. Proven track record building operational systems that drive revenue growth and streamline sales processes in high-growth tech environments. Strong expertise in data hygiene, financial analysis, and cross-functional collaboration with Sales, Marketing, and Operations teams.",
          size: 22
        })]
      }),

      // SKILLS SECTION (Reordered for sales ops relevance)
      new Paragraph({
        spacing: { after: 0 },
        children: [new TextRun({ text: "SKILLS AND TOOLS", bold: true, size: 22 })]
      }),
      new Paragraph({
        spacing: { after: 0 },
        children: [
          new TextRun({ text: "Revenue Operations: ", bold: true, size: 20 }),
          new TextRun({ text: "Pipeline reporting, revenue analytics, bookings analysis, lead routing, sales operations", size: 20 })
        ]
      }),
      new Paragraph({
        spacing: { after: 0 },
        children: [
          new TextRun({ text: "Data & Analytics: ", bold: true, size: 20 }),
          new TextRun({ text: "Excel (pivot tables, VLOOKUP, formulas), SQL, Python, data hygiene, data governance, financial modeling", size: 20 })
        ]
      }),
      new Paragraph({
        spacing: { after: 0 },
        children: [
          new TextRun({ text: "CRM Operations: ", bold: true, size: 20 }),
          new TextRun({ text: "CRM automation, lead distribution, data migration, account management, workflow optimization", size: 20 })
        ]
      }),
      new Paragraph({
        spacing: { after: 0 },
        children: [
          new TextRun({ text: "Requirements & Process: ", bold: true, size: 20 }),
          new TextRun({ text: "BRD/FRD, user stories, acceptance criteria, process mapping, UAT", size: 20 })
        ]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun({ text: "Tools: ", bold: true, size: 20 }),
          new TextRun({ text: "Jira, Confluence, Notion, Excel, SQL, Python, GoHighLevel (CRM), Stripe (payment ops)", size: 20 })
        ]
      }),

      // EXPERIENCE (Enhanced bullets with keywords)
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "PROFESSIONAL EXPERIENCE", bold: true, size: 22 })]
      }),

      // KAVALIER
      new Paragraph({
        spacing: { after: 0 },
        children: [new TextRun({ text: "Business Systems Analyst | Company A | Chicago, IL | Sep 2024 to Present", bold: true, size: 20 })]
      }),
      new Paragraph({
        spacing: { before: 60, after: 0, line: { line: 276, rule: "auto" } },
        children: [new TextRun({
          text: "• Built end-to-end revenue operations workflow across CRM (GoHighLevel) and payment platform (Stripe), automating client onboarding, lead routing, and waiver delivery with stage-gate enforcement, reducing onboarding effort from 3–5 hours to 1–2 hours per client",
          size: 20
        })]
      }),
      new Paragraph({
        spacing: { after: 0, line: { line: 276, rule: "auto" } },
        children: [new TextRun({
          text: "• Designed CRM data model in Notion to centralize pipeline tracking, client lifecycle management, and delivery workflows, establishing data governance standards that reduced missed onboarding steps by 60% through standardized fields and required-stage completion",
          size: 20
        })]
      }),
      new Paragraph({
        spacing: { after: 180, line: { line: 276, rule: "auto" } },
        children: [new TextRun({
          text: "• Performed UAT-style testing and defect triage on CRM automation workflows, identifying and resolving data integrity issues to ensure accurate lead distribution and reporting, saving ~3–5 hours per week through workflow optimization",
          size: 20
        })]
      }),

      // VICEGERENT
      new Paragraph({
        spacing: { after: 0 },
        children: [new TextRun({ text: "Business Operations Analyst | Company B | Chicago, IL | Jun 2022 to Sep 2024", bold: true, size: 20 })]
      }),
      new Paragraph({
        spacing: { before: 60, after: 0, line: { line: 276, rule: "auto" } },
        children: [new TextRun({
          text: "• Implemented Notion-based CRM and operations hub, migrating 700+ client records from Google Sheets with data governance rules, establishing customer lifecycle stages and standardized fields to centralize order tracking and pipeline visibility",
          size: 20
        })]
      }),
      new Paragraph({
        spacing: { after: 0, line: { line: 276, rule: "auto" } },
        children: [new TextRun({
          text: "• Led data migration and data hygiene initiative using Python scripts to clean and normalize legacy data, then owned ongoing data quality through governance standards that ensured consistent data entry across operations and sales teams",
          size: 20
        })]
      }),
      new Paragraph({
        spacing: { after: 180, line: { line: 276, rule: "auto" } },
        children: [new TextRun({
          text: "• Authored SOPs and training documentation for order entry, production updates, and alterations tracking, enabling consistent operational execution and reducing errors by 40% through standardized processes",
          size: 20
        })]
      }),

      // OLIVER WYMAN
      new Paragraph({
        spacing: { after: 0 },
        children: [new TextRun({ text: "Senior Consultant | Consulting Firm | Chicago, IL | Mar 2022 to Jun 2022", bold: true, size: 20 })]
      }),
      new Paragraph({
        spacing: { before: 60, after: 0, line: { line: 276, rule: "auto" } },
        children: [new TextRun({
          text: "• Drove revenue operations strategy across Product, Engineering, and Marketing, quantifying revenue impact through financial modeling and supporting retention initiatives projected to reduce churn by 23% and increase customer lifetime value",
          size: 20
        })]
      }),
      new Paragraph({
        spacing: { after: 180, line: { line: 276, rule: "auto" } },
        children: [new TextRun({
          text: "• Developed predictive analytics models in Python using customer behavioral data to identify at-risk segments for pipeline forecasting and revenue optimization for major US telecom client",
          size: 20
        })]
      }),

      // DELOITTE
      new Paragraph({
        spacing: { after: 0 },
        children: [new TextRun({ text: "Business Analyst | Enterprise Corp | Chicago, IL | Oct 2020 to Mar 2022", bold: true, size: 20 })]
      }),
      new Paragraph({
        spacing: { before: 60, after: 0, line: { line: 276, rule: "auto" } },
        children: [new TextRun({
          text: "• Built executive dashboards and financial models in Excel (pivot tables, VLOOKUP, scenario analysis) to translate complex datasets into pipeline reports and revenue forecasts for C-suite stakeholders",
          size: 20
        })]
      }),
      new Paragraph({
        spacing: { after: 0, line: { line: 276, rule: "auto" } },
        children: [new TextRun({
          text: "• Authored BRDs and FRDs documenting business requirements, functional specifications, and data requirements, translating stakeholder needs into technical specifications for sales operations systems",
          size: 20
        })]
      }),
      new Paragraph({
        spacing: { after: 0, line: { line: 276, rule: "auto" } },
        children: [new TextRun({
          text: "• Executed UAT by creating test plans and tracking defects in Jira, ensuring data accuracy and system functionality before go-live for enterprise implementations",
          size: 20
        })]
      }),
      new Paragraph({
        spacing: { after: 240, line: { line: 276, rule: "auto" } },
        children: [new TextRun({
          text: "• Supported Agile delivery through backlog refinement and sprint ceremonies, maintaining story readiness with clear acceptance criteria and test coverage for cross-functional teams",
          size: 20
        })]
      }),

      // EDUCATION
      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({ text: "EDUCATION", bold: true, size: 22 })]
      }),
      new Paragraph({
        children: [new TextRun({ text: "University Name | B.S. Your Major | Sep YYYY to Jun YYYY", size: 20 })]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("~/Downloads/Your_Name_Resume_Absorb_Software.docx", buffer);
  console.log("✓ Tailored resume created: ~/Downloads/Your_Name_Resume_Absorb_Software.docx");
});
