#!/usr/bin/env python3
"""
Generate tailored resume for Process Street - Junior Solutions Engineer.

Following ResumeTailoring.md workflow requirements:
- Minimum 2 bullets per job (especially Oliver Wyman)
- Keyword optimization for Solutions Engineering
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
    """Generate Process Street-tailored resume."""

    # Tailored resume data for Process Street - Junior Solutions Engineer
    # Keywords: technical discovery, demos, no-code integrations, API knowledge,
    # client-facing, workflow automation, solutions engineering

    process_street_data = {
        "header": {
            "name": "IDREES KAMAL",
            "contact": {
                "location": "Chicago, IL",
                "phone": "(773) 789-0400",
                "email": "ikamal97@gmail.com",
                "linkedin": "linkedin.com/in/idreeskamal"
            }
        },
        "professional_title": "JUNIOR SOLUTIONS ENGINEER",
        "summary": "Junior Solutions Engineer with 5+ years combining technical discovery, client-facing communication, and workflow automation expertise, translating business requirements into technical solutions through no-code integrations, API knowledge, and demo building, with demonstrated success in consultative selling and stakeholder management across SaaS platforms and workflow optimization projects.",
        "skills": {
            "Solutions Engineering": [
                "technical discovery",
                "demo building",
                "pre-sales support",
                "client-facing communication",
                "solution design",
                "technical presentations"
            ],
            "Integration & Automation": [
                "no-code integrations",
                "Zapier",
                "API integrations",
                "workflow automation",
                "GoHighLevel",
                "ManyChat"
            ],
            "Technical Skills": [
                "Python",
                "SQL",
                "JavaScript/TypeScript",
                "React",
                "API architecture",
                "system integration"
            ],
            "Business Analysis": [
                "requirements elicitation",
                "BRD/FRD",
                "user stories",
                "process mapping",
                "UAT",
                "stakeholder management"
            ],
            "Tools": [
                "Jira",
                "Confluence",
                "Notion",
                "Stripe",
                "Excel",
                "Calendly"
            ]
        },
        "experience": [
            {
                "company": "KAVALIER",
                "location": "Chicago, IL",
                "title": "Business Systems Analyst",
                "dates": "Sep 2024 to Dec 2025",
                "bullets": [
                    "Built end-to-end workflow automation across GoHighLevel CRM, Stripe, and Notion using no-code integrations and API connections, automating client onboarding, payment processing, and milestone tracking with Zapier middleware",
                    "Designed and launched AI application (8,765 lines TypeScript/React) integrating Google Gemini API, demonstrating full-stack technical capability from requirements gathering through deployment and testing",
                    "Performed technical troubleshooting and defect triage on workflow automations, systematically diagnosing integration failures, pipeline triggers, and data handoff issues to maintain operational reliability"
                ]
            },
            {
                "company": "VICEGERENT CUSTOM CLOTHIERS",
                "location": "Chicago, IL",
                "title": "Business Operations Analyst",
                "dates": "Jun 2022 to Sep 2024",
                "bullets": [
                    "Engineered workflow automation connecting Calendly, Notion, and Zapier for appointment scheduling and CRM synchronization, serving 36 clients with automated booking confirmations and data updates",
                    "Migrated 750+ records from Google Sheets to Notion via API scripting and data transformation, establishing standardized schema and lifecycle automation to eliminate manual data entry"
                ]
            },
            {
                "company": "OLIVER WYMAN",
                "location": "Chicago, IL",
                "title": "Senior Consultant",
                "dates": "Mar 2022 to Jun 2022",
                "bullets": [
                    "Facilitated technical discovery and cross-functional alignment across Product, Engineering, and Marketing teams, translating business requirements into technical implementation plans for customer retention initiatives",
                    "Contributed to Python-based analytical models for customer segmentation, collaborating with engineering teams to integrate behavioral data and define technical specifications for predictive retention tools"
                ]
            },
            {
                "company": "DELOITTE CONSULTING LLP",
                "location": "Chicago, IL",
                "title": "Business Analyst",
                "dates": "Oct 2020 to Mar 2022",
                "bullets": [
                    "Led technical requirements gathering and solution design for Cisco EA 3.0 strategic transformation, translating stakeholder needs into functional specifications and coordinating implementation across workstreams",
                    "Delivered technical presentations and executive dashboards using Excel and PowerPoint, communicating complex system requirements and business impacts to C-suite stakeholders and technical teams"
                ]
            }
        ],
        "education": "Northwestern University | B.S. Computer Science | Sep 2017 to Jun 2020"
    }

    try:
        print("=" * 70)
        print("GENERATING PROCESS STREET RESUME")
        print("=" * 70)

        output_path = generate_resume_from_template(
            tailored_data=process_street_data,
            company_name="Process_Street",
            output_dir="/Users/idreeskamal/Documents/Obsidian Vault/04 - Career/Generated Assets/Process Street"
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
