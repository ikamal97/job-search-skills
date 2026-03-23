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
      // Header with contact info
      new Paragraph({
        alignment: AlignmentType.LEFT,
        spacing: { after: 0 },
        children: [new TextRun({ text: "YOUR NAME", bold: true, size: 24 })]
      }),
      new Paragraph({
        alignment: AlignmentType.LEFT,
        spacing: { after: 0 },
        children: [new TextRun({ text: "Chicago, IL | (555) 123-4567 | user@example.com | linkedin.com/in/yourprofile", size: 20 })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "" })]
      }),

      // Date
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "January 8, 2026" })]
      }),

      // Recipient
      new Paragraph({
        spacing: { after: 0 },
        children: [new TextRun({ text: "Hiring Manager" })]
      }),
      new Paragraph({
        spacing: { after: 0 },
        children: [new TextRun({ text: "Absorb Software" })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "Remote" })]
      }),

      // Salutation
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "Dear Hiring Manager," })]
      }),

      // Opening paragraph
      new Paragraph({
        spacing: { after: 240 },
        alignment: AlignmentType.JUSTIFIED,
        children: [new TextRun({
          text: "I'm writing to express my strong interest in the Sales Operations Analyst position at Absorb Software. When I read Kim Brown's message about building an outbound team to unlock Absorb's untapped potential, it resonated immediately—I've spent my career turning operational complexity into scalable systems that drive revenue growth, and the opportunity to do this in a high-growth SaaS environment achieving 45% YoY growth is exactly what I'm looking for."
        })]
      }),

      // Body paragraph 1 - Analytics & reporting
      new Paragraph({
        spacing: { after: 240 },
        alignment: AlignmentType.JUSTIFIED,
        children: [new TextRun({
          text: "The \"crunchy\" work you described—pipeline reporting, data analysis, and building reliable dashboards—is where I thrive. At a Big 4 firm, I built executive dashboards and financial models that translated complex datasets into actionable insights for leadership, supporting strategic decisions across digital transformation initiatives. At a consulting firm, I developed predictive retention models in Python that identified at-risk customer segments and quantified revenue impact, supporting initiatives projected to reduce churn by 23%. I'm highly proficient in Excel (pivot tables, VLOOKUP, advanced formulas) and SQL for data analysis, and I learn new systems quickly—my Computer Science degree gives me the technical foundation to work efficiently across any tech stack."
        })]
      }),

      // Body paragraph 2 - CRM operations
      new Paragraph({
        spacing: { after: 240 },
        alignment: AlignmentType.JUSTIFIED,
        children: [new TextRun({
          text: "My operational experience directly mirrors what you need for pipeline management and data hygiene. At Company B, I implemented a CRM system and migrated 700+ client records from spreadsheets, establishing lifecycle stages and standardized fields to centralize customer and order tracking. I cleaned and normalized legacy data using Python scripts and governance rules, then owned ongoing data quality to ensure consistent team entry. At Company A, I built end-to-end onboarding workflows across CRM and payment platforms, performed rigorous testing on automations, and reduced onboarding effort from 3-5 hours to 1-2 hours per client. While my CRM experience has been with GoHighLevel and Notion rather than Salesforce specifically, the fundamentals are identical: lead routing, account hygiene, data validation, and building reports that drive decisions."
        })]
      }),

      // Body paragraph 3 - Company fit
      new Paragraph({
        spacing: { after: 240 },
        alignment: AlignmentType.JUSTIFIED,
        children: [new TextRun({
          text: "What excites me most about Absorb is the combination of remarkable growth, remote-first culture, and the opportunity to build operational infrastructure that scales with your new outbound initiative. I understand that sales operations is the engine room—when pipeline reporting is accurate, lead distribution is smooth, and data is clean, the entire revenue organization moves faster. I'm energized by that foundational work because I know its impact on business outcomes."
        })]
      }),

      // Closing paragraph
      new Paragraph({
        spacing: { after: 240 },
        alignment: AlignmentType.JUSTIFIED,
        children: [new TextRun({
          text: "I would welcome the opportunity to discuss how my analytical skills, CRM operations experience, and passion for data-driven decision-making can support Absorb's sales team as you unlock new customer segments and continue your impressive growth trajectory. Thank you for your consideration, and I look forward to speaking with you."
        })]
      }),

      // Signature
      new Paragraph({
        spacing: { before: 240 },
        children: [new TextRun({ text: "Sincerely," })]
      }),
      new Paragraph({
        spacing: { after: 0 },
        children: [new TextRun({ text: "Your Name" })]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("~/Downloads/Your_Name_CoverLetter_Absorb_Software.docx", buffer);
  console.log("Cover letter created: ~/Downloads/Your_Name_CoverLetter_Absorb_Software.docx");
});
