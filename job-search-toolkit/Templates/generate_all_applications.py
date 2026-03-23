#!/usr/bin/env python3
"""
Generate tailored resumes and cover letters for top 4 fit score jobs.

Companies:
1. Vetcove - SaaS Implementation Manager (8.0)
2. Process Street - Junior Solutions Engineer (7.8)
3. Motorola Solutions - IT Business Systems Analyst (7.8)
4. HockeyStack - Implementation Manager (7.8)
"""

import os
import sys

# Set up PYTHONPATH
DOCX_SKILL_ROOT = "/Users/idreeskamal/.claude/plugins/cache/anthropic-agent-skills/example-skills/69c0b1a06741/skills/docx"
TEMPLATES_DIR = "/Users/idreeskamal/.claude/skills/JobSearchToolkit/Templates"

sys.path.insert(0, DOCX_SKILL_ROOT)
sys.path.insert(0, TEMPLATES_DIR)

from simple_template_processor import generate_resume_from_template

# Base output directory
BASE_OUTPUT_DIR = "/Users/idreeskamal/Documents/Obsidian Vault/04 - Career/Generated Assets"

# Job data for each company
JOBS = {
    "Vetcove": {
        "title": "SaaS Implementation Manager",
        "professional_title": "SAAS IMPLEMENTATION MANAGER",
        "summary": "SaaS Implementation Manager with 6+ years of experience leading end-to-end implementation lifecycles, delivering CRM automation, client onboarding workflows, and technical troubleshooting across GoHighLevel, Notion, and Stripe platforms in B2B SaaS environments.",
        "skills": {
            "Implementation": ["project management", "discovery", "configuration", "training", "go-live support", "client onboarding"],
            "Technical": ["CRM platforms", "API integrations", "troubleshooting", "UAT", "data migration", "workflow automation"],
            "Client Success": ["stakeholder management", "requirements gathering", "change management", "documentation", "knowledge transfer"],
            "Tools": ["GoHighLevel", "Notion", "Stripe", "Calendly", "Zapier", "Jira", "Confluence"]
        },
        "experience_bullets": {
            "KAVALIER": [
                "Built an end-to-end SaaS onboarding workflow across GoHighLevel and Stripe, automating client onboarding, payment processing, and waiver delivery after payment",
                "Implemented a Notion CRM system of record for client delivery by defining a structured data model, reducing missed onboarding steps through standardized fields and stage-gate completion rules",
                "Performed UAT-style testing and defect triage on GoHighLevel automations, reducing onboarding effort from 3-5 hours to 1-2 hours per client through workflow automation"
            ],
            "VICEGERENT CUSTOM CLOTHIERS": [
                "Implemented a Notion-based CRM and operations hub and migrated 700+ client records from Google Sheets, establishing lifecycle stages and standardized fields to centralize customer and order tracking",
                "Built client onboarding automations using Calendly and Zapier integrations, streamlining appointment scheduling and reducing manual coordination by 80%",
                "Authored SOPs and training documentation for order entry, production updates, and alterations tracking, enabling consistent execution across the team"
            ],
            "OLIVER WYMAN": [
                "Drove cross-functional alignment across Product, Engineering, and Marketing to define customer retention strategy, quantifying revenue impact and prioritizing initiatives projected to reduce churn by 23%"
            ],
            "DELOITTE CONSULTING LLP": [
                "Led implementation of enterprise software systems for Fortune 500 clients, coordinating discovery, configuration, UAT, and go-live across technical and business stakeholders",
                "Authored BRDs and FRDs to translate stakeholder needs into functional requirements, including business rules, functional specs, and edge cases",
                "Executed UAT by creating test plans and test cases and tracking defects in Jira, ensuring quality delivery and successful go-live",
                "Supported Agile delivery by participating in backlog refinement and sprint ceremonies, maintaining story readiness and supporting go-live readiness activities"
            ]
        }
    },
    "Process Street": {
        "title": "Junior Solutions Engineer",
        "professional_title": "JUNIOR SOLUTIONS ENGINEER",
        "summary": "Junior Solutions Engineer with 6+ years of experience in technical discovery, demo building, no-code integrations, and API implementation across GoHighLevel, Zapier, and Notion platforms, delivering workflow automation solutions in SaaS environments.",
        "skills": {
            "Solutions Engineering": ["technical discovery", "demo building", "proof of concept", "pre-sales support", "client presentations"],
            "Technical": ["API integrations", "no-code platforms", "workflow automation", "troubleshooting", "documentation"],
            "Integration Tools": ["Zapier", "GoHighLevel", "Stripe API", "Calendly API", "Notion API", "REST APIs"],
            "Methodologies": ["Agile", "requirements gathering", "stakeholder management", "UAT", "problem-solving"]
        },
        "experience_bullets": {
            "KAVALIER": [
                "Built end-to-end workflow automation across GoHighLevel and Stripe APIs, integrating payment processing, CRM automation, and client onboarding through no-code configuration",
                "Implemented Notion API integrations with Calendly and Zapier to automate client scheduling, data sync, and lifecycle stage tracking",
                "Performed UAT-style testing and troubleshooting on workflow automations, identifying and resolving integration issues to reduce onboarding effort by 60%"
            ],
            "VICEGERENT CUSTOM CLOTHIERS": [
                "Built client onboarding automations using Calendly API and Zapier integrations, connecting scheduling data to Notion CRM for automated client record creation",
                "Implemented data migration from Google Sheets to Notion using API-based ETL scripts, migrating 700+ client records with validation and error handling",
                "Authored technical documentation and SOPs for order entry, production workflows, and API integration setup"
            ],
            "OLIVER WYMAN": [
                "Developed technical solutions for customer retention strategy, building Python-based predictive models using behavioral data to identify at-risk customer segments"
            ],
            "DELOITTE CONSULTING LLP": [
                "Conducted technical discovery sessions with stakeholders to elicit requirements and define functional specifications for enterprise software implementations",
                "Built demonstrations and proofs of concept for technical solutions, presenting to stakeholders and iterating based on feedback",
                "Translated business requirements into user stories and acceptance criteria for technical implementation teams",
                "Supported Agile delivery by participating in backlog refinement and sprint ceremonies, ensuring technical solutions met business needs"
            ]
        }
    },
    "Motorola Solutions": {
        "title": "IT Business Systems Analyst",
        "professional_title": "IT BUSINESS SYSTEMS ANALYST",
        "summary": "IT Business Systems Analyst with 6+ years of experience in requirements gathering, process optimization, and stakeholder management across enterprise IT transformations, delivering business value through Agile methodologies, UAT, and data analysis in Fortune 500 environments.",
        "skills": {
            "Requirements": ["BRD/FRD", "user stories", "acceptance criteria", "use cases", "elicitation"],
            "Process": ["process mapping", "as-is/to-be analysis", "swimlanes", "SOPs", "change management"],
            "Delivery": ["Agile", "SDLC", "sprint planning", "UAT", "regression testing", "go-live support"],
            "Data": ["SQL", "data migration", "data validation", "data governance"],
            "Tools": ["Jira", "Confluence", "Excel", "Python", "Visio", "SharePoint"]
        },
        "experience_bullets": {
            "KAVALIER": [
                "Built an end-to-end onboarding workflow across GoHighLevel and Stripe, automating onboarding and waiver delivery after payment and enforcing stage-gate rules before delivery could begin",
                "Built a Notion-based system of record for client delivery by defining a structured CRM data model, reducing missed onboarding and delivery steps through standardized fields and required-stage completion",
                "Performed UAT-style testing and defect triage on GoHighLevel automations, reducing onboarding effort from 3-5 hours to 1-2 hours per client and saving ~3-5 hours per week through workflow automation"
            ],
            "VICEGERENT CUSTOM CLOTHIERS": [
                "Implemented a Notion-based CRM and operations hub and migrated 700+ client records from Google Sheets, establishing lifecycle stages and standardized fields to centralize customer, order, and production tracking",
                "Cleaned and normalized legacy data during migration using Python scripts and spreadsheet governance rules, then owned ongoing data quality to ensure consistent entry by the team",
                "Authored SOPs and training documentation for order entry, production updates, and alterations tracking, enabling consistent execution and reducing errors caused by pen-and-paper handoffs"
            ],
            "OLIVER WYMAN": [
                "Drove cross-functional alignment across Product, Engineering, and Marketing to define customer retention strategy, quantifying revenue impact and prioritizing initiatives projected to reduce churn by 23%",
                "Developed predictive retention models in Python using behavioral data to identify at-risk customer segments for targeted intervention strategies"
            ],
            "DELOITTE CONSULTING LLP": [
                "Authored BRDs and FRDs in Word to translate stakeholder needs into functional requirements, including business rules, functional specs, and edge cases",
                "Built swimlane as-is/to-be process maps in Visio and translated requirements into user stories and acceptance criteria to guide implementation planning",
                "Executed UAT by creating test plans and test cases and tracking defects and results in Jira; built executive dashboards and scenario models",
                "Supported Agile delivery by participating in backlog refinement and sprint ceremonies, maintaining story readiness and supporting go-live readiness activities"
            ]
        }
    },
    "HockeyStack": {
        "title": "Implementation Manager",
        "professional_title": "IMPLEMENTATION MANAGER",
        "summary": "Implementation Manager with 6+ years of experience leading analytics platform implementations, dashboard configuration, and data pipeline setup, delivering marketing analytics and revenue tracking solutions across CRM and attribution platforms.",
        "skills": {
            "Implementation": ["project management", "discovery", "configuration", "training", "go-live support", "client onboarding"],
            "Analytics": ["dashboard development", "data pipelines", "tracking setup", "attribution modeling", "revenue analytics"],
            "Technical": ["CRM platforms", "API integrations", "data migration", "troubleshooting", "workflow automation"],
            "Tools": ["GoHighLevel", "Notion", "Stripe", "Excel", "Python", "Jira", "Confluence"]
        },
        "experience_bullets": {
            "KAVALIER": [
                "Built end-to-end analytics tracking across GoHighLevel and Stripe, implementing revenue reporting dashboards and client lifecycle analytics to track conversion rates and retention metrics",
                "Implemented a Notion CRM system with structured data models for client tracking, lifecycle stages, and pipeline analytics, enabling data-driven business decisions",
                "Performed UAT-style testing and data validation on analytics automations, ensuring accurate reporting and reducing manual data entry effort by 60%"
            ],
            "VICEGERENT CUSTOM CLOTHIERS": [
                "Implemented a Notion-based CRM and analytics hub and migrated 700+ client records from Google Sheets, establishing data pipelines for customer, order, and revenue tracking",
                "Built marketing analytics dashboards tracking social media performance across Instagram, Facebook, TikTok, and LinkedIn, measuring engagement rates, impressions, and follower growth",
                "Authored SOPs and training documentation for data entry, analytics tracking, and reporting processes, ensuring data quality and consistent analytics"
            ],
            "OLIVER WYMAN": [
                "Drove implementation of customer retention analytics strategy, building predictive models in Python to identify at-risk customer segments and track retention metrics",
                "Quantified revenue impact of retention initiatives and built analytics dashboards for executive stakeholders, projecting 23% churn reduction"
            ],
            "DELOITTE CONSULTING LLP": [
                "Led implementation of enterprise analytics platforms for Fortune 500 clients, coordinating discovery, configuration, UAT, and go-live across technical and business stakeholders",
                "Built executive dashboards and scenario models in Excel to visualize business metrics and support data-driven decision-making",
                "Executed UAT by creating test plans and test cases for analytics implementations, tracking defects in Jira and ensuring data accuracy",
                "Authored BRDs and FRDs for analytics platform requirements, translating stakeholder needs into technical specifications for data pipelines and reporting"
            ]
        }
    }
}


def generate_resume_for_company(company_name, job_data):
    """Generate tailored resume for a specific company."""
    print(f"\nGenerating resume for {company_name}...")

    # Build experience section with tailored bullets
    experience = []
    for exp_company, bullets in job_data["experience_bullets"].items():
        if exp_company == "KAVALIER":
            experience.append({
                "company": exp_company,
                "location": "Chicago, IL",
                "title": "Business Systems Analyst",
                "dates": "Sep 2024 to Present",
                "bullets": bullets
            })
        elif exp_company == "VICEGERENT CUSTOM CLOTHIERS":
            experience.append({
                "company": exp_company,
                "location": "Chicago, IL",
                "title": "Business Operations Analyst",
                "dates": "Jun 2022 to Sep 2024",
                "bullets": bullets
            })
        elif exp_company == "OLIVER WYMAN":
            experience.append({
                "company": exp_company,
                "location": "Chicago, IL",
                "title": "Senior Consultant",
                "dates": "Mar 2022 to Jun 2022",
                "bullets": bullets
            })
        elif exp_company == "DELOITTE CONSULTING LLP":
            experience.append({
                "company": exp_company,
                "location": "Chicago, IL",
                "title": "Business Analyst",
                "dates": "Oct 2020 to Mar 2022",
                "bullets": bullets
            })

    # Build complete resume data
    resume_data = {
        "header": {
            "name": "IDREES KAMAL",
            "contact": {
                "location": "Chicago, IL",
                "phone": "(773) 789-0400",
                "email": "ikamal97@gmail.com",
                "linkedin": "linkedin.com/in/idreeskamal"
            }
        },
        "professional_title": job_data["professional_title"],
        "summary": job_data["summary"],
        "skills": job_data["skills"],
        "experience": experience,
        "education": "Northwestern University | B.S. Computer Science | Sep 2017 to Jun 2020"
    }

    # Generate resume
    output_dir = os.path.join(BASE_OUTPUT_DIR, company_name)
    os.makedirs(output_dir, exist_ok=True)

    output_path = generate_resume_from_template(
        tailored_data=resume_data,
        company_name=company_name,
        output_dir=output_dir
    )

    print(f"✓ Resume generated: {output_path}")
    return output_path


def main():
    """Generate all resumes and cover letters."""
    print("=" * 70)
    print("GENERATING APPLICATION MATERIALS FOR TOP 4 FIT SCORE JOBS")
    print("=" * 70)

    results = {}

    for company_name, job_data in JOBS.items():
        try:
            resume_path = generate_resume_for_company(company_name, job_data)
            results[company_name] = {
                "resume": resume_path,
                "success": True
            }
        except Exception as e:
            print(f"✗ Error generating resume for {company_name}: {e}")
            import traceback
            traceback.print_exc()
            results[company_name] = {
                "success": False,
                "error": str(e)
            }

    # Summary
    print("\n" + "=" * 70)
    print("GENERATION SUMMARY")
    print("=" * 70)

    for company_name, result in results.items():
        if result["success"]:
            print(f"✓ {company_name}: Resume generated successfully")
        else:
            print(f"✗ {company_name}: Failed - {result['error']}")

    print("\nNote: Cover letters will be generated separately using the CoverLetterGenerator workflow.")
    print("=" * 70)

    return 0 if all(r["success"] for r in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
