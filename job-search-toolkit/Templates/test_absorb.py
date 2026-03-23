#!/usr/bin/env python3
"""
Test resume generation for Absorb Software Sales Operations Analyst role.
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
    """Generate tailored resume for Absorb Software."""

    # Tailored for: Sales Operations Analyst at Absorb Software
    # Key JD requirements: Excel, Salesforce, pipeline reporting, data hygiene,
    # revenue analytics, lead routing, SaaS environment

    absorb_data = {
        "header": {
            "name": "IDREES KAMAL",
            "contact": {
                "location": "Chicago, IL",
                "phone": "(773) 789-0400",
                "email": "ikamal97@gmail.com",
                "linkedin": "linkedin.com/in/idreeskamal"
            }
        },
        "professional_title": "SALES OPERATIONS ANALYST",
        "summary": "Sales Operations Analyst with 4+ years of experience in revenue operations, pipeline analytics, and CRM administration across SaaS and consulting environments. Expertise in building bookings and revenue reports using Excel (pivot tables, VLOOKUP, advanced formulas), maintaining Salesforce data hygiene, and driving operational execution through lead routing optimization and data-driven insights.",
        "skills": {
            "Revenue Operations": ["pipeline reporting", "bookings analysis", "revenue analytics", "lead routing", "territory management"],
            "Data & Analytics": ["Excel (pivot tables, VLOOKUP, formulas)", "SQL", "Python", "data hygiene", "large dataset analysis"],
            "CRM Administration": ["Salesforce", "lead distribution", "account management", "data governance", "workflow automation"],
            "Process & Delivery": ["process improvement", "operational execution", "cross-functional collaboration", "UAT", "reporting automation"],
            "Tools": ["Salesforce", "Excel", "SQL", "Python", "Jira", "Confluence", "Notion", "PowerBI"]
        },
        "experience": [
            {
                "company": "KAVALIER",
                "bullets": [
                    "Built revenue operations workflows across CRM and payment platforms, automating lead routing and client onboarding with stage-gate enforcement that reduced operational overhead by 60%",
                    "Designed CRM data model to centralize pipeline tracking and client lifecycle management, establishing data governance standards that improved data accuracy and reporting reliability",
                    "Performed UAT and defect triage on CRM automations, identifying data integrity issues to ensure accurate lead distribution and pipeline reporting"
                ]
            },
            {
                "company": "VICEGERENT",
                "bullets": [
                    "Implemented CRM operations hub and migrated 700+ account records with data hygiene rules, establishing lifecycle stages and standardized fields to centralize pipeline and order tracking",
                    "Led data migration and cleansing initiative using Python and Excel, normalizing legacy data and owning ongoing data quality through governance standards across sales and operations teams",
                    "Built operational reports and SOPs for order tracking and account updates, enabling consistent execution and reducing data entry errors by 40%"
                ]
            },
            {
                "company": "OLIVER WYMAN",
                "bullets": [
                    "Drove cross-functional alignment across Product, Engineering, and Marketing to define revenue operations strategy, quantifying impact through financial modeling and pipeline analysis",
                    "Developed predictive analytics models in Python to identify at-risk customer segments, supporting retention initiatives projected to reduce churn by 23%"
                ]
            },
            {
                "company": "DELOITTE",
                "bullets": [
                    "Built executive dashboards and financial models in Excel (pivot tables, VLOOKUP, scenario analysis) translating complex datasets into pipeline reports and revenue forecasts for leadership",
                    "Authored BRDs documenting business requirements and data specifications, translating stakeholder needs into technical requirements for sales operations systems",
                    "Executed UAT by creating test plans and tracking defects in Jira, ensuring data accuracy and system functionality before go-live for enterprise CRM implementations",
                    "Supported Agile delivery through backlog refinement and sprint ceremonies, maintaining story readiness and cross-functional coordination with Sales, Marketing, and Operations teams"
                ]
            }
        ],
        "education": "Northwestern University | B.S. Computer Science | Sep 2017 to Jun 2020"
    }

    try:
        print("=" * 70)
        print("ABSORB SOFTWARE - Sales Operations Analyst")
        print("=" * 70)
        print()
        print(f"Title: {absorb_data['professional_title']}")
        print(f"Summary: {absorb_data['summary'][:80]}...")
        print()

        output_path = generate_resume_from_template(
            tailored_data=absorb_data,
            company_name="Absorb_Software",
            output_dir=os.path.expanduser("~/Downloads")
        )

        print("✓ Resume generated successfully!")
        print(f"✓ Output: {output_path}")
        print()
        print("=" * 70)

        return 0

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
