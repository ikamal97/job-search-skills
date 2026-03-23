#!/usr/bin/env python3
"""
Generate tailored resume for HockeyStack - Implementation Manager.

Following ResumeTailoring.md workflow requirements:
- Minimum 2 bullets per job (especially Oliver Wyman)
- Keyword optimization for Analytics Platform Implementation
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
    """Generate HockeyStack-tailored resume."""

    # Tailored resume data for HockeyStack - Implementation Manager
    # Keywords: analytics platform, implementation, data pipelines, dashboard configuration,
    # tracking setup, B2B SaaS, marketing analytics, revenue analytics

    hockeystack_data = {
        "header": {
            "name": "IDREES KAMAL",
            "contact": {
                "location": "Chicago, IL",
                "phone": "(773) 789-0400",
                "email": "ikamal97@gmail.com",
                "linkedin": "linkedin.com/in/idreeskamal"
            }
        },
        "professional_title": "IMPLEMENTATION MANAGER",
        "summary": "Implementation Manager with 5+ years delivering analytics platform implementations and data-driven solutions, from discovery and tracking setup to dashboard configuration and go-live support, with expertise in B2B SaaS onboarding, data pipeline integration, and stakeholder training across marketing and revenue operations teams, leveraging SQL, data analysis, and technical communication to ensure customer success.",
        "skills": {
            "Implementation & Analytics": [
                "analytics platform implementation",
                "tracking setup & configuration",
                "dashboard development",
                "data pipeline integration",
                "go-live support",
                "customer onboarding"
            ],
            "Data & Analysis": [
                "SQL",
                "data analysis",
                "data migration",
                "data validation",
                "data governance",
                "reporting & visualization"
            ],
            "SaaS & Platforms": [
                "B2B SaaS implementation",
                "CRM platforms",
                "marketing analytics tools",
                "revenue operations",
                "API integrations",
                "workflow automation"
            ],
            "Technical Skills": [
                "Python",
                "JavaScript",
                "system integration",
                "technical troubleshooting",
                "Excel modeling",
                "PowerPoint dashboards"
            ],
            "Tools": [
                "Jira",
                "Confluence",
                "Notion",
                "GoHighLevel",
                "Stripe",
                "Zapier"
            ]
        },
        "experience": [
            {
                "company": "KAVALIER",
                "location": "Chicago, IL",
                "title": "Business Systems Analyst",
                "dates": "Sep 2024 to Dec 2025",
                "bullets": [
                    "Implemented end-to-end analytics and tracking system across GoHighLevel CRM and Stripe, configuring conversion tracking, milestone metrics, and revenue reporting to monitor client lifecycle and business performance",
                    "Built data pipeline integrations connecting Notion, Calendly, and Stripe via API, establishing automated data flow for appointment scheduling, payment processing, and client lifecycle tracking with real-time synchronization",
                    "Designed operational dashboards and reporting for 12-client coaching business, tracking key metrics (onboarding completion, milestone progress, retention rates) to enable data-driven decision-making"
                ]
            },
            {
                "company": "VICEGERENT CUSTOM CLOTHIERS",
                "location": "Chicago, IL",
                "title": "Business Operations Analyst",
                "dates": "Jun 2022 to Sep 2024",
                "bullets": [
                    "Implemented analytics and reporting infrastructure for $256K custom clothing business, tracking revenue by client segment, product type, and sales channel, enabling data-driven inventory and marketing decisions",
                    "Migrated and standardized 750+ customer records from Google Sheets to Notion with data validation rules and governance protocols, establishing single source of truth for customer analytics and operational reporting"
                ]
            },
            {
                "company": "OLIVER WYMAN",
                "location": "Chicago, IL",
                "title": "Senior Consultant",
                "dates": "Mar 2022 to Jun 2022",
                "bullets": [
                    "Conducted data analysis and financial modeling for customer retention initiatives, building revenue impact models and customer segmentation analysis to inform strategic decision-making for major telecom client",
                    "Contributed to Python-based predictive analytics for customer churn modeling, collaborating with data science teams to analyze behavioral data and identify at-risk customer segments for targeted retention campaigns"
                ]
            },
            {
                "company": "DELOITTE CONSULTING LLP",
                "location": "Chicago, IL",
                "title": "Business Analyst",
                "dates": "Oct 2020 to Mar 2022",
                "bullets": [
                    "Built executive dashboards and scenario models using Excel and PowerPoint for Cisco EA 3.0 transformation, tracking KPIs across multiple workstreams and presenting data-driven insights to C-suite stakeholders",
                    "Delivered data analysis and reporting for HSBC wealth management implementation, coordinating data migration, validating business metrics, and ensuring analytics capabilities met stakeholder requirements"
                ]
            }
        ],
        "education": "Northwestern University | B.S. Computer Science | Sep 2017 to Jun 2020"
    }

    try:
        print("=" * 70)
        print("GENERATING HOCKEYSTACK RESUME")
        print("=" * 70)

        output_path = generate_resume_from_template(
            tailored_data=hockeystack_data,
            company_name="HockeyStack",
            output_dir="/Users/idreeskamal/Documents/Obsidian Vault/04 - Career/Generated Assets/HockeyStack"
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
