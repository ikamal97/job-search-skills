#!/usr/bin/env python3
"""
Production-ready resume generation script.

Usage:
    python3 generate_resume.py

This script generates a tailored resume from the template with proper
environment setup and error handling.
"""

import os
import sys

# Set up PYTHONPATH for Document library and TemplateProcessor
DOCX_SKILL_ROOT = "os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib', 'docx')"
TEMPLATES_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, DOCX_SKILL_ROOT)
sys.path.insert(0, TEMPLATES_DIR)

# Now import TemplateProcessor (using simplified version for production)
from simple_template_processor import generate_resume_from_template


def main():
    """Generate sample resume to test template processor."""

    # Sample tailored resume data (replace with actual data from ResumeTailoring workflow)
    sample_data = {
        "header": {
            "name": "YOUR NAME",
            "contact": {
                "location": "Chicago, IL",
                "phone": "(555) 123-4567",
                "email": "user@example.com",
                "linkedin": "linkedin.com/in/yourprofile"
            }
        },
        "professional_title": "SENIOR BUSINESS SYSTEMS ANALYST",
        "summary": "Senior Business Systems Analyst with 6+ years of experience in requirements gathering, process optimization, and stakeholder management across Salesforce CRM implementations, delivering business value through Agile methodologies, UAT, and data analysis in enterprise SaaS environments.",
        "skills": {
            "Requirements": ["BRD/FRD", "user stories", "acceptance criteria", "use cases", "elicitation"],
            "Process": ["process mapping", "as-is/to-be analysis", "swimlanes", "SOPs", "change management"],
            "Delivery": ["Agile", "SDLC", "sprint planning", "UAT", "regression testing", "go-live support"],
            "Data": ["SQL", "data migration", "data validation", "CRM automation", "data governance"],
            "Tools": ["Jira", "Confluence", "Salesforce", "Excel", "Python", "Visio"]
        },
        "experience": [
            {
                "company": "COMPANY_A",
                "location": "Chicago, IL",
                "title": "Business Systems Analyst",
                "dates": "Sep 2024 to Present",
                "bullets": [
                    "Built an end-to-end onboarding workflow across GoHighLevel and Stripe, automating onboarding and waiver delivery after payment and enforcing stage-gate rules before delivery could begin",
                    "Built a Notion-based system of record for client delivery by defining a structured CRM data model, reducing missed onboarding and delivery steps through standardized fields and required-stage completion",
                    "Performed UAT-style testing and defect triage on GoHighLevel automations, reducing onboarding effort from 3–5 hours to 1–2 hours per client and saving ~3–5 hours per week through workflow automation"
                ]
            },
            {
                "company": "COMPANY_B",
                "location": "Chicago, IL",
                "title": "Business Operations Analyst",
                "dates": "Jun 2022 to Sep 2024",
                "bullets": [
                    "Implemented a Notion-based CRM and operations hub and migrated 700+ client records from Google Sheets, establishing lifecycle stages and standardized fields to centralize customer, order, and production tracking",
                    "Cleaned and normalized legacy data during migration using Python scripts and spreadsheet governance rules, then owned ongoing data quality to ensure consistent entry by the team",
                    "Authored SOPs and training documentation for order entry, production updates, and alterations tracking, enabling consistent execution and reducing errors caused by pen-and-paper handoffs"
                ]
            },
            {
                "company": "CONSULTING_FIRM",
                "location": "Chicago, IL",
                "title": "Senior Consultant",
                "dates": "Mar 2022 to Jun 2022",
                "bullets": [
                    "Drove cross-functional alignment across Product, Engineering, and Marketing to define customer retention strategy, quantifying revenue impact and prioritizing initiatives projected to reduce churn by 23%",
                    "Developed predictive retention models in Python using behavioral data to identify at-risk customer segments for targeted intervention strategies"
                ]
            },
            {
                "company": "ENTERPRISE_CORP",
                "location": "Chicago, IL",
                "title": "Business Analyst",
                "dates": "Oct 2020 to Mar 2022",
                "bullets": [
                    "Authored BRDs and FRDs in Word to translate stakeholder needs into functional requirements, including business rules, functional specs, and edge cases",
                    "Built swimlane as-is/to-be process maps in Visio and translated requirements into user stories and acceptance criteria to guide implementation planning",
                    "Executed UAT by creating test plans and test cases and tracking defects and results in Jira; built executive dashboards and scenario models",
                    "Supported Agile delivery by participating in backlog refinement and sprint ceremonies, maintaining story readiness and supporting go-live readiness activities"
                ]
            }
        ],
        "education": "University Name | B.S. Your Major | Sep YYYY to Jun YYYY"
    }

    try:
        print("=" * 70)
        print("RESUME TEMPLATE PROCESSOR - Production Test")
        print("=" * 70)
        print()

        # Generate resume
        print("Generating resume from template...")
        print(f"- Name: {sample_data['header']['name']}")
        print(f"- Title: {sample_data['professional_title']}")
        print(f"- Company: Test_Company")
        print()

        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Output")
        os.makedirs(output_dir, exist_ok=True)
        output_path = generate_resume_from_template(
            tailored_data=sample_data,
            company_name="Test_Company",
            output_dir=output_dir
        )

        print("✓ Resume generated successfully!")
        print(f"✓ Output: {output_path}")
        print()
        print("=" * 70)
        print("NEXT STEPS:")
        print("1. Open the generated DOCX file in Word/LibreOffice")
        print("2. Verify formatting matches template exactly")
        print("3. Check all sections: header, title, summary, skills, experience, education")
        print("4. Validate bullet points, spacing, fonts, and alignment")
        print("=" * 70)

        return 0

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        print()
        print("Make sure template file exists at:")
        print("  Templates/resume-template.docx (relative to skill root)")
        print("  OR")
        print("  CONTEXT/ (relative to skill root)")
        return 1

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
