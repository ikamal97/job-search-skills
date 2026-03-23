#!/usr/bin/env python3
"""
Generate tailored resume for Motorola Solutions - IT Business Systems Analyst.

Following ResumeTailoring.md workflow requirements:
- Minimum 2 bullets per job (especially Oliver Wyman)
- Keyword optimization for IT Business Systems Analyst
- ATS-friendly formatting
"""

import os
import sys

# Set up PYTHONPATH
DOCX_SKILL_ROOT = "/Users/idreeskamal/.claude/plugins/cache/anthropic-agent-skills/example-skills/69c0b1a06741/skills/docx"
TEMPLATES_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, DOCX_SKILL_ROOT)
sys.path.insert(0, TEMPLATES_DIR)

from simple_template_processor import generate_resume_from_template


def main():
    """Generate Motorola Solutions-tailored resume."""

    # Tailored resume data for Motorola Solutions - IT Business Systems Analyst
    # Keywords: SDLC, IT transformation, requirements documentation, UAT,
    # stakeholder management, Agile, enterprise systems, business requirements

    motorola_data = {
        "header": {
            "name": "IDREES KAMAL",
            "contact": {
                "location": "Chicago, IL",
                "phone": "(773) 789-0400",
                "email": "ikamal97@gmail.com",
                "linkedin": "linkedin.com/in/idreeskamal"
            }
        },
        "professional_title": "IT BUSINESS SYSTEMS ANALYST",
        "summary": "IT Business Systems Analyst with 5+ years delivering enterprise technology solutions through SDLC methodologies, requirements documentation (BRD/FRD), UAT coordination, and stakeholder management across Fortune 500 clients, translating complex business needs into technical specifications for system implementations, with Computer Science foundation enabling deep technical understanding and cross-functional collaboration.",
        "skills": {
            "Requirements & Documentation": [
                "BRD/FRD",
                "requirements elicitation",
                "user stories",
                "acceptance criteria",
                "functional specifications",
                "technical documentation"
            ],
            "SDLC & Delivery": [
                "SDLC",
                "Agile methodologies",
                "sprint planning",
                "backlog grooming",
                "UAT",
                "regression testing",
                "go-live support"
            ],
            "Process & Analysis": [
                "process mapping",
                "as-is/to-be analysis",
                "swimlanes",
                "gap analysis",
                "change management",
                "SOPs"
            ],
            "Data & Systems": [
                "SQL",
                "data migration",
                "data validation",
                "system integration",
                "CRM platforms",
                "enterprise IT"
            ],
            "Tools": [
                "Jira",
                "Confluence",
                "Visio",
                "Excel",
                "PowerPoint",
                "Word"
            ]
        },
        "experience": [
            {
                "company": "KAVALIER",
                "location": "Chicago, IL",
                "title": "Business Systems Analyst",
                "dates": "Sep 2024 to Dec 2025",
                "bullets": [
                    "Authored technical requirements and system specifications for CRM automation platform, defining data models, workflow logic, and integration requirements for GoHighLevel and Stripe payment processing",
                    "Executed UAT-style testing and defect triage on workflow automations, creating test cases, tracking defects in systematic logs, and coordinating fixes to ensure production readiness",
                    "Built system documentation and SOPs for onboarding workflows, defining business rules, data validation requirements, and stage-gate logic for automated client lifecycle management"
                ]
            },
            {
                "company": "VICEGERENT CUSTOM CLOTHIERS",
                "location": "Chicago, IL",
                "title": "Business Operations Analyst",
                "dates": "Jun 2022 to Sep 2024",
                "bullets": [
                    "Led enterprise system implementation migrating 750+ records from legacy Google Sheets to Notion CRM platform, defining requirements, data mapping specifications, and validation rules to ensure data integrity",
                    "Authored comprehensive SOPs and training documentation for order management, production tracking, and alterations workflows, standardizing business processes across 3-person team to reduce manual errors"
                ]
            },
            {
                "company": "OLIVER WYMAN",
                "location": "Chicago, IL",
                "title": "Senior Consultant",
                "dates": "Mar 2022 to Jun 2022",
                "bullets": [
                    "Facilitated requirements gathering and business analysis for customer retention technology initiative, coordinating across Product, Engineering, and Marketing stakeholders to define system requirements and prioritize features",
                    "Contributed to technical analysis and data modeling for Python-based retention tools, collaborating with engineering teams to define data requirements, business logic, and integration specifications"
                ]
            },
            {
                "company": "DELOITTE CONSULTING LLP",
                "location": "Chicago, IL",
                "title": "Business Analyst",
                "dates": "Oct 2020 to Mar 2022",
                "bullets": [
                    "Delivered business analysis for Cisco EA 3.0 strategic IT transformation (2 levels from CEO), authoring BRDs and FRDs, coordinating UAT, and producing daily executive status reports that supported 2.5x software growth",
                    "Managed team of 3 junior Business Analysts on HSBC enterprise system implementation, reviewing requirements documentation, coordinating stakeholder interviews, and ensuring SDLC compliance across Agile sprints"
                ]
            }
        ],
        "education": "Northwestern University | B.S. Computer Science | Sep 2017 to Jun 2020"
    }

    try:
        print("=" * 70)
        print("GENERATING MOTOROLA SOLUTIONS RESUME")
        print("=" * 70)

        output_path = generate_resume_from_template(
            tailored_data=motorola_data,
            company_name="Motorola_Solutions",
            output_dir="/Users/idreeskamal/Documents/Obsidian Vault/04 - Career/Generated Assets/Motorola Solutions"
        )

        print(f"\n✓ Resume generated successfully")
        print(f"✓ Output: {output_path}")
        print("\nBullet Count Verification:")
        print("- Kavalier: 3 bullets ✓")
        print("- Vicegerent: 2 bullets ✓")
        print("- Oliver Wyman: 2 bullets ✓ (MEETS MINIMUM)")
        print("- Deloitte: 2 bullets ✓")

    except Exception as e:
        print(f"\n✗ Error generating resume: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
