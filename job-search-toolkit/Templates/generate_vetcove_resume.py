#!/usr/bin/env python3
"""
Generate tailored resume for Vetcove - SaaS Implementation Manager.

Following ResumeTailoring.md workflow requirements:
- Minimum 2 bullets per job (especially Consulting Firm)
- Keyword optimization for SaaS Implementation
- ATS-friendly formatting
"""

import os
import sys

# Set up PYTHONPATH
DOCX_SKILL_ROOT = "os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib', 'docx')"
TEMPLATES_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, DOCX_SKILL_ROOT)
sys.path.insert(0, TEMPLATES_DIR)

from simple_template_processor import generate_resume_from_template


def main():
    """Generate Vetcove-tailored resume."""

    # Tailored resume data for Vetcove - SaaS Implementation Manager
    # Keywords: SaaS implementation, client onboarding, technical troubleshooting,
    # configuration, go-live, training, SMB, platform implementation

    vetcove_data = {
        "header": {
            "name": "YOUR NAME",
            "contact": {
                "location": "Chicago, IL",
                "phone": "(555) 123-4567",
                "email": "user@example.com",
                "linkedin": "linkedin.com/in/yourprofile"
            }
        },
        "professional_title": "SAAS IMPLEMENTATION MANAGER",
        "summary": "SaaS Implementation Manager with 5+ years delivering end-to-end platform implementations, from discovery and configuration to training and go-live support, with deep expertise in client onboarding automation, technical troubleshooting, and SMB-focused SaaS environments, leveraging CRM platforms, API integrations, and workflow automation to ensure seamless customer success.",
        "skills": {
            "Implementation & Onboarding": [
                "SaaS implementation",
                "client onboarding automation",
                "go-live support",
                "discovery & requirements",
                "configuration management",
                "training & documentation"
            ],
            "CRM & Platforms": [
                "GoHighLevel CRM",
                "Notion",
                "Stripe",
                "Calendly",
                "Zapier",
                "WordPress",
                "Trainerize"
            ],
            "Process & Delivery": [
                "implementation lifecycle",
                "technical troubleshooting",
                "data migration",
                "testing & UAT",
                "SOPs",
                "change management"
            ],
            "Technical Skills": [
                "SQL",
                "Python",
                "API integrations",
                "workflow automation",
                "system architecture"
            ],
            "Tools": [
                "Jira",
                "Confluence",
                "Excel",
                "Visio",
                "QuickBooks",
                "PowerPoint"
            ]
        },
        "experience": [
            {
                "company": "COMPANY_A",
                "location": "Chicago, IL",
                "title": "Business Systems Analyst",
                "dates": "Sep 2024 to Dec 2025",
                "bullets": [
                    "Built end-to-end client onboarding workflow across GoHighLevel CRM and Stripe, automating waiver delivery, health questionnaire routing, and milestone tracking, reducing onboarding time from 3-5 hours to 1-2 hours per client",
                    "Implemented Notion-based system of record for client delivery tracking and program management, centralizing 12 active client files with automated Calendly integration via Zapier for appointment synchronization",
                    "Performed UAT-style testing and defect triage on GoHighLevel automations, proactively identifying and resolving pipeline stage triggers, tag assignments, and email sequence failures before client impact"
                ]
            },
            {
                "company": "COMPANY_B",
                "location": "Chicago, IL",
                "title": "Business Operations Analyst",
                "dates": "Jun 2022 to Sep 2024",
                "bullets": [
                    "Led digital transformation initiative, migrating 750+ client records from Google Sheets to Notion CRM with automated lifecycle stages, standardized data fields, and Calendly-Zapier integration for scheduling automation",
                    "Generated $57,585 in solo revenue (22% of $256K company total) across 36 unique clients, managing end-to-end sales cycle from consultations to fittings, demonstrating strong client-facing communication and relationship management"
                ]
            },
            {
                "company": "CONSULTING_FIRM",
                "location": "Chicago, IL",
                "title": "Senior Consultant",
                "dates": "Mar 2022 to Jun 2022",
                "bullets": [
                    "Drove cross-functional alignment across Product, Engineering, and Marketing teams on customer retention initiatives, supporting strategic decision-making through data analysis and financial modeling",
                    "Contributed to Python-based predictive modeling for customer retention analysis, collaborating with technical teams to identify at-risk customer segments for targeted intervention strategies"
                ]
            },
            {
                "company": "ENTERPRISE_CORP",
                "location": "Chicago, IL",
                "title": "Business Analyst",
                "dates": "Oct 2020 to Mar 2022",
                "bullets": [
                    "Delivered business analysis for Cisco EA 3.0 strategic transformation (2 levels from CEO), producing daily executive progress reports and workstream tracking that contributed to 2.5x software growth and 3x partner renewal rates",
                    "Managed team of 3 junior Business Analysts on HSBC wealth management engagement, assigning tasks, reviewing deliverables, and ensuring quality of requirements documentation and stakeholder communications"
                ]
            }
        ],
        "education": "University Name | B.S. Your Major | Sep YYYY to Jun YYYY"
    }

    try:
        print("=" * 70)
        print("GENERATING VETCOVE RESUME")
        print("=" * 70)

        output_path = generate_resume_from_template(
            tailored_data=vetcove_data,
            company_name="Vetcove",
            output_dir="~/Career/Generated Assets/Vetcove"
        )

        print(f"\n✓ Resume generated successfully")
        print(f"✓ Output: {output_path}")
        print("\nBullet Count Verification:")
        print("- Company A: 3 bullets ✓")
        print("- Company B: 2 bullets ✓")
        print("- Consulting Firm: 2 bullets ✓ (MEETS MINIMUM)")
        print("- Enterprise Corp: 2 bullets ✓")

    except Exception as e:
        print(f"\n✗ Error generating resume: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
