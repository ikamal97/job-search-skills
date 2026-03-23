#!/usr/bin/env python3
"""
TemplateProcessor.py - Deterministic resume generation from template

This module provides template-based DOCX resume generation to ensure
100% formatting consistency across all tailored resumes.

Template-based approach:
1. Unpack template DOCX
2. Replace content while preserving all formatting attributes
3. Repack into new DOCX

All formatting (fonts, sizes, spacing, indents) preserved from template.
"""

from __future__ import annotations

import os
import glob
import shutil
import tempfile
import subprocess
from typing import Optional, Dict, List, Tuple

# Document library - will be imported at runtime
Document = None
DocxXMLEditor = None


class ResumeTemplateProcessor:
    """Process DOCX resume template with content replacement."""

    def __init__(self):
        self.template_path: Optional[str] = None
        self.temp_dir: Optional[str] = None
        self.doc: Optional[Document] = None

    def find_template(self, verbose: bool = True) -> Optional[str]:
        """
        Find resume template in standard locations with diagnostics.

        Search order:
        1. Downloads folder (specific file)
        2. Downloads folder (any *Resume*.docx)
        3. CONTEXT/ directory (relative to skill root)

        Returns:
            Path to template file or None if not found
        """
        search_locations = [
            "~/Downloads/Your_Name_Resume.docx",
            os.path.expanduser("~/Downloads/*Resume*.docx"),  # Fallback pattern
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "CONTEXT", "*.docx")
        ]

        if verbose:
            print(f"[TemplateProcessor] Searching for template...")

        for location in search_locations:
            if verbose:
                print(f"  Checking: {location}")

            if '*' in location:
                # Glob pattern
                matches = glob.glob(location)
                if matches:
                    # Return most recently modified
                    self.template_path = max(matches, key=os.path.getmtime)
                    if verbose:
                        print(f"  ✓ Found: {self.template_path}")
                    return self.template_path
                elif verbose:
                    print(f"  ✗ No matches")
            else:
                # Exact path
                if os.path.exists(location):
                    self.template_path = location
                    if verbose:
                        print(f"  ✓ Found: {location}")
                    return self.template_path
                elif verbose:
                    print(f"  ✗ Not found")

        if verbose:
            print(f"[TemplateProcessor] ERROR: No template found in any location")
        return None

    def unpack_template(self, template_path: str, output_dir: Optional[str] = None) -> str:
        """
        Unpack DOCX template to directory.

        Args:
            template_path: Path to template DOCX file
            output_dir: Optional output directory (temp dir if not specified)

        Returns:
            Path to unpacked directory
        """
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="resume_template_")

        # DOCX is a ZIP archive
        subprocess.run(
            ['unzip', '-q', template_path, '-d', output_dir],
            check=True
        )

        self.temp_dir = output_dir
        return output_dir

    def load_document(self, unpacked_dir: str) -> Document:
        """
        Load unpacked document using Document library.

        Args:
            unpacked_dir: Path to unpacked DOCX directory

        Returns:
            Document instance
        """
        global Document, DocxXMLEditor

        # Import at runtime after PYTHONPATH is set
        if Document is None:
            try:
                from scripts.document import Document as DocumentClass, DocxXMLEditor as EditorClass
                Document = DocumentClass
                DocxXMLEditor = EditorClass
            except ImportError as e:
                raise ImportError(
                    f"Document library not available: {e}\n"
                    "Ensure PYTHONPATH includes docx skill root."
                )

        self.doc = Document(unpacked_dir)
        return self.doc

    def replace_header(self, name: str, contact: Dict[str, str]) -> None:
        """
        Replace header section (name and contact info).

        Args:
            name: Full name (e.g., "JOHN DOE")
            contact: Dict with keys: location, phone, email, linkedin
        """
        if not self.doc:
            raise ValueError("Document not loaded. Call load_document() first.")

        # Replace name (paragraph 1)
        name_node = self.doc["word/document.xml"].get_node(
            tag="w:p",
            line_number=range(1, 50),
            contains="YOUR NAME"
        )

        if name_node:
            # Find the text node within
            for elem in name_node.getElementsByTagName("w:t"):
                if "YOUR NAME" in elem.firstChild.nodeValue:
                    elem.firstChild.nodeValue = name.upper()

        # Replace contact line (paragraph 2)
        contact_line = f"{contact.get('location', 'Chicago, IL')} | {contact.get('phone', '')} | {contact.get('email', '')} | {contact.get('linkedin', '')}"

        contact_node = self.doc["word/document.xml"].get_node(
            tag="w:p",
            line_number=range(1, 100),
            contains="Chicago, IL"
        )

        if contact_node:
            # Find and replace contact text
            for elem in contact_node.getElementsByTagName("w:t"):
                text = elem.firstChild.nodeValue if elem.firstChild else ""
                if "Chicago, IL" in text or "@" in text or "linkedin" in text:
                    # Replace entire contact line in the main text node
                    if "Chicago, IL" in text:
                        elem.firstChild.nodeValue = contact_line
                        # Clear subsequent text nodes in this paragraph
                        break

    def replace_title(self, title: str) -> None:
        """
        Replace professional title.

        Args:
            title: Professional title (e.g., "BUSINESS SYSTEMS ANALYST")
        """
        if not self.doc:
            raise ValueError("Document not loaded")

        title_node = self.doc["word/document.xml"].get_node(
            tag="w:p",
            contains="BUSINESS SYSTEMS ANALYST"
        )

        if title_node:
            for elem in title_node.getElementsByTagName("w:t"):
                if "BUSINESS SYSTEMS ANALYST" in elem.firstChild.nodeValue:
                    elem.firstChild.nodeValue = title.upper()

    def replace_summary(self, summary: str) -> None:
        """
        Replace professional summary paragraph.

        Args:
            summary: Professional summary text (1-2 sentences)
        """
        if not self.doc:
            raise ValueError("Document not loaded")

        # Summary is paragraph 4 (after name, contact, title)
        summary_node = self.doc["word/document.xml"].get_node(
            tag="w:p",
            line_number=range(1, 200),
            contains="Business Systems Analyst with Enterprise Corp"
        )

        if summary_node:
            for elem in summary_node.getElementsByTagName("w:t"):
                if "Business Systems Analyst" in elem.firstChild.nodeValue:
                    elem.firstChild.nodeValue = summary
                    break

    def replace_skills(self, skills: Dict[str, List[str]]) -> None:
        """
        Replace skills section with dynamic categories.

        Args:
            skills: Dict mapping category name to list of skills
                    Example: {"Technical Skills": ["SQL", "Python"], ...}
        """
        if not self.doc:
            raise ValueError("Document not loaded")

        # Find skills section start (after "SKILLS AND TOOLS" header)
        skills_header = self.doc["word/document.xml"].get_node(
            tag="w:p",
            contains="SKILLS AND TOOLS"
        )

        if not skills_header:
            return

        # Get the parent to insert after
        parent = skills_header.parentNode
        current_node = skills_header

        # Remove existing skill paragraphs (5 categories in template)
        # They follow the SKILLS AND TOOLS header
        for _ in range(6):  # 5 categories + 1 empty para
            next_node = current_node.nextSibling
            if next_node and next_node.nodeName == "w:p":
                # Check if it's a skills category or empty para before EXPERIENCE
                check_para = True
                for text_elem in next_node.getElementsByTagName("w:t"):
                    if text_elem.firstChild:
                        text = text_elem.firstChild.nodeValue
                        if "EXPERIENCE" in text:
                            check_para = False
                            break

                if check_para:
                    to_remove = current_node.nextSibling
                    current_node = current_node.nextSibling
                    if to_remove:
                        parent.removeChild(to_remove)
                else:
                    break
            else:
                current_node = current_node.nextSibling

        # Insert new skill categories
        insert_after = skills_header

        for category, skill_list in skills.items():
            # Create skills paragraph with template formatting
            skills_text = ", ".join(skill_list)

            # Build paragraph XML (preserving template formatting)
            para_xml = f'''<w:p>
                <w:pPr>
                    <w:widowControl w:val="0"/>
                    <w:spacing w:before="5.009765625" w:line="240" w:lineRule="auto"/>
                    <w:ind w:right="-78"/>
                    <w:rPr><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>
                </w:pPr>
                <w:r>
                    <w:rPr><w:b w:val="1"/><w:bCs w:val="1"/><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>
                    <w:t xml:space="preserve">{category}: </w:t>
                </w:r>
                <w:r>
                    <w:rPr><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>
                    <w:t>{skills_text}</w:t>
                </w:r>
            </w:p>'''

            # Insert after current position
            new_nodes = self.doc["word/document.xml"].insert_after(insert_after, para_xml)
            insert_after = new_nodes[-1] if new_nodes else insert_after

        # Add empty paragraph after skills
        empty_para = '''<w:p>
            <w:pPr>
                <w:spacing w:after="0" w:before="0" w:line="240" w:lineRule="auto"/>
                <w:ind w:left="14.059982299804688" w:right="0" w:firstLine="0"/>
                <w:rPr><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>
            </w:pPr>
        </w:p>'''
        self.doc["word/document.xml"].insert_after(insert_after, empty_para)

    def replace_experience(self, experience_list: List[Dict]) -> None:
        """
        Replace experience section with tailored entries.

        Args:
            experience_list: List of experience dicts with keys:
                - company: Company name
                - location: City, State
                - title: Job title
                - dates: Date range
                - bullets: List of achievement bullets
        """
        if not self.doc:
            raise ValueError("Document not loaded")

        # Find EXPERIENCE header
        exp_header = self.doc["word/document.xml"].get_node(
            tag="w:p",
            contains="EXPERIENCE"
        )

        if not exp_header:
            return

        # Remove existing experience entries (up to EDUCATION header)
        parent = exp_header.parentNode
        current_node = exp_header.nextSibling

        while current_node:
            # Check if we reached EDUCATION section
            is_education = False
            if current_node.nodeName == "w:p":
                for text_elem in current_node.getElementsByTagName("w:t"):
                    if text_elem.firstChild and "EDUCATION" in text_elem.firstChild.nodeValue:
                        is_education = True
                        break

            if is_education:
                break

            # Remove node
            next_node = current_node.nextSibling
            parent.removeChild(current_node)
            current_node = next_node

        # Insert new experience entries
        insert_after = exp_header
        num_id = 1  # Start with numId 1 for first experience

        for idx, exp in enumerate(experience_list):
            # Company/Location paragraph (bold, 20pt)
            company_para = f'''<w:p>
                <w:pPr>
                    <w:spacing w:after="0" w:before="{"43.260498046875" if idx == 0 else "0"}" w:line="240" w:lineRule="auto"/>
                    <w:ind w:left="14.739990234375" w:right="0" w:firstLine="0"/>
                    <w:jc w:val="left"/>
                </w:pPr>
                <w:r>
                    <w:rPr>
                        <w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/>
                        <w:b w:val="1"/><w:bCs w:val="1"/>
                        <w:sz w:val="20"/><w:szCs w:val="20"/>
                    </w:rPr>
                    <w:t xml:space="preserve">{exp["company"]} | {exp["location"]} </w:t>
                </w:r>
            </w:p>'''

            new_nodes = self.doc["word/document.xml"].insert_after(insert_after, company_para)
            insert_after = new_nodes[-1] if new_nodes else insert_after

            # Title/Dates paragraph
            title_para = f'''<w:p>
                <w:pPr>
                    <w:spacing w:after="0" w:before="0" w:line="240" w:lineRule="auto"/>
                    <w:ind w:left="4.7499847412109375" w:right="0" w:firstLine="0"/>
                    <w:jc w:val="left"/>
                </w:pPr>
                <w:r>
                    <w:rPr><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>
                    <w:t>{exp["title"]}</w:t>
                </w:r>
                <w:r>
                    <w:rPr>
                        <w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/>
                        <w:sz w:val="19"/><w:szCs w:val="19"/>
                    </w:rPr>
                    <w:t xml:space="preserve"> | {exp["dates"]} </w:t>
                </w:r>
            </w:p>'''

            new_nodes = self.doc["word/document.xml"].insert_after(insert_after, title_para)
            insert_after = new_nodes[-1] if new_nodes else insert_after

            # Bullet points
            for bullet_idx, bullet in enumerate(exp["bullets"]):
                bullet_para = f'''<w:p>
                    <w:pPr>
                        <w:numPr><w:ilvl w:val="0"/><w:numId w:val="{num_id}"/></w:numPr>
                        <w:spacing w:after="0" w:before="{"18.270263671875" if bullet_idx == 0 else "0"}" w:line="228.48000526428223" w:lineRule="auto"/>
                        <w:ind w:left="720" w:right="253.272705078125" w:hanging="360"/>
                        <w:jc w:val="left"/>
                        <w:rPr><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>
                    </w:pPr>
                    <w:r>
                        <w:rPr><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>
                        <w:t>{bullet}</w:t>
                    </w:r>
                </w:p>'''

                new_nodes = self.doc["word/document.xml"].insert_after(insert_after, bullet_para)
                insert_after = new_nodes[-1] if new_nodes else insert_after

            # Empty paragraph after experience entry
            empty_para = '''<w:p>
                <w:pPr>
                    <w:spacing w:after="0" w:before="0" w:line="229.90785598754883" w:lineRule="auto"/>
                    <w:ind w:left="0" w:right="253.0810546875" w:firstLine="0"/>
                    <w:jc w:val="left"/>
                    <w:rPr><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>
                </w:pPr>
            </w:p>'''

            new_nodes = self.doc["word/document.xml"].insert_after(insert_after, empty_para)
            insert_after = new_nodes[-1] if new_nodes else insert_after

            # Increment numId for next experience (keeps bullets separate)
            num_id += 1

    def replace_education(self, education: str) -> None:
        """
        Replace education section.

        Args:
            education: Education text (e.g., "University | Degree | Dates")
        """
        if not self.doc:
            raise ValueError("Document not loaded")

        # Find education section
        edu_node = self.doc["word/document.xml"].get_node(
            tag="w:p",
            contains="University Name"
        )

        if edu_node:
            for elem in edu_node.getElementsByTagName("w:t"):
                if "University Name" in elem.firstChild.nodeValue:
                    elem.firstChild.nodeValue = education
                    break

    def save_and_pack(self, output_path: str) -> str:
        """
        Save document and repack to DOCX.

        Args:
            output_path: Path for output DOCX file

        Returns:
            Path to generated DOCX file
        """
        if not self.doc:
            raise ValueError("Document not loaded")

        # Save XML changes
        self.doc.save()

        # Pack back to DOCX
        self._pack_docx(self.doc.unpacked_path, output_path)

        return output_path

    def _pack_docx(self, unpacked_dir: str, output_path: str) -> None:
        """
        Pack directory back to DOCX file.

        Args:
            unpacked_dir: Path to unpacked directory
            output_path: Path for output DOCX file
        """
        # Change to unpacked directory and zip
        original_dir = os.getcwd()
        os.chdir(unpacked_dir)

        try:
            # Create ZIP with DOCX extension
            subprocess.run(
                ['zip', '-r', '-q', output_path, '.'],
                check=True
            )
        finally:
            os.chdir(original_dir)

    def cleanup(self) -> None:
        """Clean up temporary files."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


def generate_resume_from_template(
    tailored_data: Dict,
    company_name: str,
    output_dir: str = None
) -> str:
    """
    Generate tailored resume from template.

    Main entry point for template-based resume generation.

    Args:
        tailored_data: Dict with keys:
            - header: {name, contact: {location, phone, email, linkedin}}
            - professional_title: Title string
            - summary: Summary text
            - skills: {category: [skills]}
            - experience: [{company, location, title, dates, bullets}]
            - education: Education string
        company_name: Company name for filename
        output_dir: Output directory (defaults to ~/Downloads)

    Returns:
        Path to generated DOCX file
    """
    if output_dir is None:
        output_dir = os.path.expanduser("~/Downloads")

    processor = ResumeTemplateProcessor()

    try:
        # Find template
        template_path = processor.find_template()
        if not template_path:
            raise FileNotFoundError(
                "Resume template not found.\n"
                "Searched locations:\n"
                "  1. ~/Downloads/Your_Name_Resume.docx\n"
                "  2. ~/Downloads/*Resume*.docx\n"
                "  3. CONTEXT/*.docx (relative to skill root)\n"
                "Please ensure template exists in one of these locations."
            )

        # Unpack template
        unpacked_dir = processor.unpack_template(template_path)

        # Load document
        processor.load_document(unpacked_dir)

        # Replace sections
        processor.replace_header(
            tailored_data["header"]["name"],
            tailored_data["header"]["contact"]
        )
        processor.replace_title(tailored_data["professional_title"])
        processor.replace_summary(tailored_data["summary"])
        processor.replace_skills(tailored_data["skills"])
        processor.replace_experience(tailored_data["experience"])
        processor.replace_education(tailored_data["education"])

        # Generate filename
        first_name = tailored_data["header"]["name"].split()[0]
        last_name = tailored_data["header"]["name"].split()[-1]
        filename = f"{first_name}_{last_name}_Resume_{company_name.replace(' ', '_')}.docx"
        output_path = os.path.join(output_dir, filename)

        # Save and pack
        result_path = processor.save_and_pack(output_path)

        return result_path

    finally:
        # Cleanup temp files
        processor.cleanup()


if __name__ == "__main__":
    # Example usage
    sample_data = {
        "header": {
            "name": "JOHN DOE",
            "contact": {
                "location": "San Francisco, CA",
                "phone": "(555) 123-4567",
                "email": "john.doe@example.com",
                "linkedin": "linkedin.com/in/johndoe"
            }
        },
        "professional_title": "SENIOR BUSINESS ANALYST",
        "summary": "Senior Business Analyst with 6+ years of experience in requirements gathering, process optimization, and stakeholder management across enterprise software implementations.",
        "skills": {
            "Technical Skills": ["SQL", "Python", "Tableau", "PowerBI"],
            "Tools & Platforms": ["Jira", "Confluence", "Salesforce", "SAP"],
            "Methodologies": ["Agile", "Scrum", "Waterfall", "Six Sigma"]
        },
        "experience": [
            {
                "company": "Tech Corp",
                "location": "San Francisco, CA",
                "title": "Senior Business Analyst",
                "dates": "Jan 2020 to Present",
                "bullets": [
                    "Led requirements gathering for $5M CRM implementation serving 500+ users",
                    "Created 50+ user stories and acceptance criteria for Agile sprints",
                    "Reduced defect rate by 30% through comprehensive UAT planning"
                ]
            }
        ],
        "education": "Stanford University | B.S. Computer Science | Sep 2014 to Jun 2018"
    }

    # Generate resume
    output = generate_resume_from_template(sample_data, "Google")
    print(f"Resume generated: {output}")
