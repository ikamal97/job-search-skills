#!/usr/bin/env python3
"""
Simplified TemplateProcessor - More robust approach using paragraph indices.

This version directly manipulates template paragraphs by position rather than
searching for text, which is more reliable.
"""

from __future__ import annotations

import os
import glob
import shutil
import tempfile
import subprocess
import sys
from typing import Optional, Dict, List

# Add Tools directory to path for imports
TOOLS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

# Document library - will be imported at runtime
Document = None

# Page verification - will be imported at runtime
get_page_count = None


# ============================================================================
# ONE-PAGE ENFORCEMENT FUNCTIONS
# ============================================================================

def estimate_content_length(tailored_data: Dict) -> int:
    """Estimate number of lines the resume will occupy.

    Calibrated against actual DOCX output with Arial 9.5pt body text.
    One page ≈ 52-55 lines with 1" margins at this font size.

    Key insight: Each bullet wraps at ~100-110 chars in the actual document,
    not 80 chars as previously assumed. This was causing over-reduction.
    """
    lines = 5  # Fixed: header, contact, title (more compact than assumed)

    # Summary (~110 chars per line in actual document)
    summary = tailored_data.get("summary", "")
    lines += len(summary) // 110 + 1

    # Skills (each category is ~1 line with wrapping)
    skills = tailored_data.get("skills", {})
    lines += len(skills) + 2  # Categories + header + spacing

    # Experience
    for job in tailored_data.get("experience", []):
        lines += 2  # Company + title lines
        for bullet in job.get("bullets", []):
            # Bullets wrap at ~100 chars in the actual document
            lines += max(1, len(bullet) // 100 + (1 if len(bullet) % 100 > 30 else 0))
        lines += 0.5  # Minimal spacing between jobs

    # Education
    lines += 2

    return int(lines)


def enforce_one_page(tailored_data: Dict, job_keywords: List[str] = None, max_lines: int = 52) -> Dict:
    """Reduce content to fit one page while preserving MAXIMUM content.

    CRITICAL: Check after EACH individual change and STOP as soon as under limit.
    Goal is to be as close to max_lines as possible without exceeding.

    Applies reductions in order:
    1. CONDENSE - Shorten ONE bullet at a time (preserve quantity)
    2. REDUCE - Remove ONE bullet at a time (maintain 2 min per job)
    3. MARGINS - Flag for margin reduction (last resort)

    Args:
        tailored_data: Resume data dict
        job_keywords: List of job-relevant keywords for scoring bullets
        max_lines: Target max lines (default 52 for 1" margins, calibrated to actual DOCX)

    Returns:
        Modified tailored_data dict with _reduce_margins flag if needed
    """
    if job_keywords is None:
        job_keywords = []

    original_lines = estimate_content_length(tailored_data)

    # Already under limit? No changes needed
    if original_lines <= max_lines:
        tailored_data["_one_page_stats"] = {
            "original_lines": original_lines,
            "final_lines": original_lines,
            "reduction_applied": 0,
            "margins_reduced": False
        }
        return tailored_data

    # ROUND 1: CONDENSE (preserve quantity) - ONE change at a time
    while estimate_content_length(tailored_data) > max_lines:
        # Try condensing ONE long bullet
        if condense_one_long_bullet(tailored_data, max_chars=150):
            if estimate_content_length(tailored_data) <= max_lines:
                break  # STOP - we're under the limit now
            continue
        # No more bullets to condense, try summary
        if condense_summary(tailored_data, max_sentences=2):
            if estimate_content_length(tailored_data) <= max_lines:
                break  # STOP
            continue
        break  # Move to Round 2

    # ROUND 2: REDUCE (only if still over) - ONE change at a time
    while estimate_content_length(tailored_data) > max_lines:
        # Remove ONE lowest-keyword-match bullet
        if remove_lowest_match_bullet(tailored_data, job_keywords, min_per_job=2):
            if estimate_content_length(tailored_data) <= max_lines:
                break  # STOP
            continue
        # Reduce skill categories
        if reduce_skill_categories(tailored_data, min_categories=4):
            if estimate_content_length(tailored_data) <= max_lines:
                break  # STOP
            continue
        break  # Move to Round 3

    # ROUND 3: MARGINS (last resort)
    if estimate_content_length(tailored_data) > max_lines:
        tailored_data["_reduce_margins"] = True
        # With 0.5" margins, we get ~58-60 lines per page
        if estimate_content_length(tailored_data) > 58:
            tailored_data["_page_overflow_warning"] = True

    final_lines = estimate_content_length(tailored_data)
    tailored_data["_one_page_stats"] = {
        "original_lines": original_lines,
        "final_lines": final_lines,
        "reduction_applied": original_lines - final_lines,
        "margins_reduced": tailored_data.get("_reduce_margins", False)
    }

    return tailored_data


def condense_one_long_bullet(tailored_data: Dict, max_chars: int = 150) -> bool:
    """Condense ONE bullet over max_chars. Returns True if one was condensed.

    Only condenses the FIRST long bullet found, then returns immediately.
    This allows checking page length after each individual change.
    """
    for job in tailored_data.get("experience", []):
        for i, bullet in enumerate(job.get("bullets", [])):
            if len(bullet) > max_chars:
                job["bullets"][i] = condense_bullet_text(bullet, max_chars)
                return True  # Stop after ONE change
    return False


def condense_long_bullets(tailored_data: Dict, max_chars: int = 150) -> bool:
    """Condense ALL bullets over max_chars. Returns True if any were condensed.

    DEPRECATED: Use condense_one_long_bullet for granular control.
    """
    condensed = False
    for job in tailored_data.get("experience", []):
        for i, bullet in enumerate(job.get("bullets", [])):
            if len(bullet) > max_chars:
                job["bullets"][i] = condense_bullet_text(bullet, max_chars)
                condensed = True
    return condensed


def condense_bullet_text(bullet: str, target_chars: int) -> str:
    """Condense bullet while preserving action verb + what + result.

    Strategy:
    1. Remove filler phrases
    2. If still over, find natural break point
    """
    # Remove filler phrases
    filler_phrases = [
        "in order to", "as well as", "in addition to", "that allowed",
        "which enabled", "resulting in the ability to", "across multiple",
        "various ", "different ", " that ", " which "
    ]
    result = bullet
    for phrase in filler_phrases:
        result = result.replace(phrase, " ")

    # Clean up double spaces
    while "  " in result:
        result = result.replace("  ", " ")
    result = result.strip()

    # If still over, truncate at last comma/semicolon before target
    if len(result) > target_chars:
        # Find a good break point between 70% and 100% of target
        min_break = int(target_chars * 0.7)
        for i in range(target_chars, min_break, -1):
            if i < len(result) and result[i] in ",;":
                result = result[:i].rstrip(",; ")
                break
        else:
            # No good break found, hard truncate at space
            if len(result) > target_chars:
                space_idx = result.rfind(" ", min_break, target_chars)
                if space_idx > min_break:
                    result = result[:space_idx].rstrip()

    return result.strip()


def condense_summary(tailored_data: Dict, max_sentences: int = 2) -> bool:
    """Condense summary to max_sentences. Returns True if condensed."""
    summary = tailored_data.get("summary", "")
    if not summary:
        return False

    # Split into sentences
    sentences = []
    current = ""
    for char in summary:
        current += char
        if char in ".!?" and len(current.strip()) > 10:
            sentences.append(current.strip())
            current = ""
    if current.strip():
        sentences.append(current.strip())

    if len(sentences) <= max_sentences:
        return False

    # Keep first max_sentences (usually the most important)
    tailored_data["summary"] = " ".join(sentences[:max_sentences])
    return True


def remove_lowest_match_bullet(tailored_data: Dict, job_keywords: List[str], min_per_job: int = 2) -> bool:
    """Remove the lowest-keyword-match bullet. Returns True if removed."""
    if not job_keywords:
        # Without keywords, remove from job with most bullets
        max_bullets_job = None
        max_bullets = 0
        for job in tailored_data.get("experience", []):
            if len(job.get("bullets", [])) > max_bullets and len(job.get("bullets", [])) > min_per_job:
                max_bullets = len(job["bullets"])
                max_bullets_job = job

        if max_bullets_job and len(max_bullets_job["bullets"]) > min_per_job:
            max_bullets_job["bullets"].pop()  # Remove last bullet
            return True
        return False

    # Score bullets by keyword matches
    lowest_score = float('inf')
    lowest_job = None
    lowest_idx = None

    keywords_lower = [kw.lower() for kw in job_keywords]

    for job in tailored_data.get("experience", []):
        bullets = job.get("bullets", [])
        if len(bullets) <= min_per_job:
            continue  # Don't reduce below minimum

        for i, bullet in enumerate(bullets):
            bullet_lower = bullet.lower()
            score = sum(1 for kw in keywords_lower if kw in bullet_lower)
            if score < lowest_score:
                lowest_score = score
                lowest_job = job
                lowest_idx = i

    if lowest_job is not None and lowest_idx is not None:
        lowest_job["bullets"].pop(lowest_idx)
        return True

    return False


def reduce_skill_categories(tailored_data: Dict, min_categories: int = 4) -> bool:
    """Reduce skill categories by merging least relevant. Returns True if reduced."""
    skills = tailored_data.get("skills", {})
    if len(skills) <= min_categories:
        return False

    # Find two smallest categories and merge them
    categories = list(skills.keys())
    if len(categories) < 2:
        return False

    # Sort by skill count
    sorted_cats = sorted(categories, key=lambda c: len(skills[c]))

    # Merge two smallest
    smallest = sorted_cats[0]
    second_smallest = sorted_cats[1]

    # Add skills from smallest to second smallest
    skills[second_smallest] = skills[second_smallest] + skills[smallest]
    del skills[smallest]

    return True


def _reduce_one_item(tailored_data: Dict, job_keywords: List[str] = None) -> bool:
    """Remove/condense ONE item. Returns True if reduced, False if at minimum.

    Priority order:
    1. Condense ONE long bullet (>180 chars)
    2. Remove ONE lowest-match bullet (min 2 per job)
    3. Condense summary (min 2 sentences)
    4. Reduce skill categories (min 4)
    """
    if job_keywords is None:
        job_keywords = []

    # Priority 1: Condense ONE long bullet (>180 chars → 150 chars)
    if condense_one_long_bullet(tailored_data, max_chars=150):
        return True

    # Priority 2: Remove ONE lowest-match bullet (respect 2-bullet minimum)
    if remove_lowest_match_bullet(tailored_data, job_keywords, min_per_job=2):
        return True

    # Priority 3: Condense summary
    if condense_summary(tailored_data, max_sentences=2):
        return True

    # Priority 4: Reduce skill categories
    if reduce_skill_categories(tailored_data, min_categories=4):
        return True

    return False  # At minimum, can't reduce further


# ============================================================================
# TEMPLATE FUNCTIONS
# ============================================================================

def find_template(verbose: bool = True) -> Optional[str]:
    """Find resume template in standard locations with diagnostics."""
    search_locations = [
        "/Users/idreeskamal/Downloads/Idrees_Kamal_BSA_Resume_01.02.26.docx",
        os.path.expanduser("~/Downloads/*Resume*.docx"),  # Fallback pattern
        "/Users/idreeskamal/Documents/Obsidian Vault/04 - Personal Operating System/Career/*.docx"
    ]

    if verbose:
        print(f"[TemplateProcessor] Searching for template...")

    for location in search_locations:
        if verbose:
            print(f"  Checking: {location}")

        if '*' in location:
            matches = glob.glob(location)
            if matches:
                result = max(matches, key=os.path.getmtime)
                if verbose:
                    print(f"  ✓ Found: {result}")
                return result
            elif verbose:
                print(f"  ✗ No matches")
        else:
            if os.path.exists(location):
                if verbose:
                    print(f"  ✓ Found: {location}")
                return location
            elif verbose:
                print(f"  ✗ Not found")

    if verbose:
        print(f"[TemplateProcessor] ERROR: No template found in any location")
    return None


def generate_resume_from_template(
    tailored_data: Dict,
    company_name: str,
    output_dir: str = None,
    job_keywords: List[str] = None,
    enforce_single_page: bool = True
) -> str:
    """
    Generate tailored resume from template with binary search optimization.

    Uses verification loop to maximize content while staying on exactly 1 page:
    1. Start with ALL content (no pre-emptive reductions)
    2. Generate DOCX → Verify page count
    3. If >1 page → Reduce ONE item → Repeat
    4. If =1 page → DONE (maximum content achieved)

    Args:
        tailored_data: Resume data with keys: header, professional_title, summary, skills, experience, education
        company_name: Company name for filename
        output_dir: Output directory (defaults to ~/Downloads)
        job_keywords: List of job-relevant keywords for one-page enforcement
        enforce_single_page: Whether to enforce one-page limit (default True)

    Returns:
        Path to generated DOCX file
    """
    global Document, get_page_count

    # Import Document library at runtime
    if Document is None:
        try:
            from scripts.document import Document as DocumentClass
            Document = DocumentClass
        except ImportError as e:
            raise ImportError(f"Document library not available: {e}")

    # Import page verification at runtime
    if get_page_count is None and enforce_single_page:
        try:
            from verify_page_count import get_page_count as _get_page_count
            get_page_count = _get_page_count
        except ImportError:
            # Fallback: disable verification if tool not available
            print("⚠️ verify_page_count not available, skipping page verification")
            enforce_single_page = False

    if output_dir is None:
        output_dir = os.path.expanduser("~/Downloads")

    # NO PRE-EMPTIVE REDUCTION - Start with full content
    # The verification loop below will reduce only if page count > 1

    # Find template
    template_path = find_template()
    if not template_path:
        raise FileNotFoundError(
            "Resume template not found.\n"
            "Searched locations:\n"
            "  1. /Users/idreeskamal/Downloads/Idrees_Kamal_BSA_Resume_01.02.26.docx\n"
            "  2. ~/Downloads/*Resume*.docx\n"
            "  3. Career folder (04 - Personal Operating System/Career/)\n"
            "Please ensure template exists in one of these locations."
        )

    # Prepare output path
    first_name = tailored_data["header"]["name"].split()[0]
    last_name = tailored_data["header"]["name"].split()[-1]
    filename = f"{first_name}_{last_name}_Resume_{company_name.replace(' ', '_')}.docx"
    output_path = os.path.join(output_dir, filename)

    # BINARY SEARCH VERIFICATION LOOP
    # Generate with full content, verify page count, reduce ONE item if >1 page, repeat
    MAX_ITERATIONS = 10

    for iteration in range(MAX_ITERATIONS):
        # Generate DOCX with current content
        _generate_single_docx(tailored_data, template_path, output_path)

        # Skip verification if disabled
        if not enforce_single_page:
            return output_path

        # Verify actual page count via LibreOffice conversion
        try:
            pages = get_page_count(output_path)
        except Exception as e:
            print(f"⚠️ Page verification failed: {e}")
            return output_path

        if pages == 1:
            # SUCCESS - maximum content that fits on exactly 1 page
            print(f"✓ Resume is exactly 1 page (iteration {iteration + 1})")
            return output_path

        if pages > 1:
            # Need to reduce - remove ONE item
            print(f"  Iteration {iteration + 1}: {pages} pages, reducing content...")
            if not _reduce_one_item(tailored_data, job_keywords):
                # Can't reduce further (at minimums)
                print("⚠️ Resume exceeds 1 page even at minimum content")
                return output_path

    # Safety exit after max iterations
    print(f"⚠️ Reached {MAX_ITERATIONS} iterations, returning current state")
    return output_path


def _generate_single_docx(tailored_data: Dict, template_path: str, output_path: str) -> None:
    """Generate a single DOCX file from template with given content.

    This is the core generation logic extracted for use in the verification loop.
    """
    global Document

    # Create temp directory and unpack template
    temp_dir = tempfile.mkdtemp(prefix="resume_")
    subprocess.run(['unzip', '-q', template_path, '-d', temp_dir], check=True)

    try:
        # Load document
        doc = Document(temp_dir)

        # Get all paragraphs for safer manipulation
        all_paragraphs = doc["word/document.xml"].dom.getElementsByTagName("w:p")

        # Replace name (paragraph 0 - first paragraph)
        _replace_text_in_paragraph(all_paragraphs[0], tailored_data["header"]["name"].upper())

        # Replace contact (paragraph 1)
        contact = tailored_data["header"]["contact"]
        contact_line = f"{contact.get('location', '')} | {contact.get('phone', '')} | {contact.get('email', '')} | {contact.get('linkedin', '')}"
        _replace_text_in_paragraph(all_paragraphs[1], contact_line)

        # Replace professional title (paragraph 2)
        _replace_text_in_paragraph(all_paragraphs[2], tailored_data["professional_title"].upper())

        # Replace summary (paragraph 3)
        _replace_text_in_paragraph(all_paragraphs[3], tailored_data["summary"])

        # Replace skills section (paragraphs 6-10 are skill categories)
        # Para 5 = "SKILLS AND TOOLS" header (keep)
        # Para 6-10 = 5 skill categories (replace)
        # Para 11 = empty (keep)
        if "skills" in tailored_data and tailored_data["skills"]:
            _replace_skills_section(doc, all_paragraphs, tailored_data["skills"])

        # Replace experience bullets (hardcoded job structure, variable bullets)
        # Each job: company para, title para, 2-4 bullets, empty para
        if "experience" in tailored_data and tailored_data["experience"]:
            _replace_experience_bullets(doc, all_paragraphs, tailored_data["experience"])

        # Save document
        doc.save()

        # Pack to DOCX
        _pack_docx(doc.unpacked_path, output_path)

    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def _replace_text_in_paragraph(paragraph, new_text: str) -> None:
    """Replace all text in a paragraph while preserving formatting.

    CRITICAL: Preserves run-level formatting (w:rPr) from the first run.
    Without this, Word won't apply bold, font size, font family correctly.
    """
    # Find all runs (w:r elements) in paragraph
    runs = paragraph.getElementsByTagName("w:r")

    if not runs:
        return

    # Find the first run that has a text element
    first_run_with_text = None
    first_text_element = None

    for run in runs:
        text_elements = run.getElementsByTagName("w:t")
        if text_elements:
            first_run_with_text = run
            first_text_element = text_elements[0]
            break

    if not first_run_with_text or not first_text_element:
        return

    # Replace text in first text element
    if first_text_element.firstChild:
        first_text_element.firstChild.nodeValue = new_text
    else:
        first_text_element.appendChild(first_text_element.ownerDocument.createTextNode(new_text))

    # Remove all OTHER runs (but keep the first one with its formatting intact)
    runs_to_remove = []
    for run in runs:
        if run != first_run_with_text:
            runs_to_remove.append(run)

    for run in runs_to_remove:
        if run.parentNode:
            run.parentNode.removeChild(run)

    # Also remove any extra text elements within the first run (keep only the first)
    text_elements_in_first_run = first_run_with_text.getElementsByTagName("w:t")
    for i, text_elem in enumerate(list(text_elements_in_first_run)):
        if i > 0 and text_elem.parentNode:
            text_elem.parentNode.removeChild(text_elem)


def _replace_skills_section(doc, all_paragraphs, skills_dict: Dict[str, List[str]]) -> None:
    """Replace skills section with dynamic categories.

    Template structure:
    - Para 5: "SKILLS AND TOOLS" header (keep)
    - Para 6-10: 5 skill categories (replace with new ones)
    - Para 11: empty paragraph (keep for spacing before EXPERIENCE)

    Args:
        doc: Document object
        all_paragraphs: NodeList of all paragraphs
        skills_dict: Dict mapping category name to list of skills
    """
    # Get the body element (parent of paragraphs)
    body = all_paragraphs[0].parentNode

    # Get reference paragraph for formatting (para 6 - first skill category)
    template_skill_para = all_paragraphs[6]

    # Get the SKILLS AND TOOLS header (para 5)
    skills_header = all_paragraphs[5]

    # Delete existing skill paragraphs (6-10) AND the empty paragraph (11)
    # We'll recreate the empty paragraph after our new skills
    paras_to_delete = []
    for i in range(6, 12):  # Delete 6-11 (skills + empty para)
        if i < len(all_paragraphs):
            paras_to_delete.append(all_paragraphs[i])

    for para in paras_to_delete:
        if para.parentNode:
            para.parentNode.removeChild(para)

    # Find EXPERIENCE header to insert before
    experience_header = None
    remaining_paras = body.getElementsByTagName("w:p")
    for para in remaining_paras:
        text_elems = para.getElementsByTagName("w:t")
        for t in text_elems:
            if t.firstChild and "EXPERIENCE" in t.firstChild.nodeValue:
                experience_header = para
                break

    # Insert new skill paragraphs before EXPERIENCE header
    for category, skills_list in skills_dict.items():
        skills_text = ", ".join(skills_list)
        new_para = _create_skill_paragraph(doc, category, skills_text, template_skill_para)
        body.insertBefore(new_para, experience_header)

    # Add empty paragraph before EXPERIENCE for spacing
    empty_para = _create_empty_paragraph(doc)
    body.insertBefore(empty_para, experience_header)


def _create_skill_paragraph(doc, category: str, skills_text: str, template_para) -> object:
    """Create a skill category paragraph with bold label and regular skills.

    Format: **Category:** skill1, skill2, skill3
    """
    dom = doc["word/document.xml"].dom

    # Clone the template paragraph structure
    new_para = template_para.cloneNode(False)  # Shallow clone (no children)

    # Clone paragraph properties from template
    pPr = template_para.getElementsByTagName("w:pPr")
    if pPr:
        new_para.appendChild(pPr[0].cloneNode(True))

    # Create bold run for category name
    bold_run = dom.createElement("w:r")
    bold_rPr = dom.createElement("w:rPr")
    bold_b = dom.createElement("w:b")
    bold_b.setAttribute("w:val", "1")
    bold_bCs = dom.createElement("w:bCs")
    bold_bCs.setAttribute("w:val", "1")
    bold_sz = dom.createElement("w:sz")
    bold_sz.setAttribute("w:val", "19")
    bold_szCs = dom.createElement("w:szCs")
    bold_szCs.setAttribute("w:val", "19")
    bold_rPr.appendChild(bold_b)
    bold_rPr.appendChild(bold_bCs)
    bold_rPr.appendChild(bold_sz)
    bold_rPr.appendChild(bold_szCs)
    bold_run.appendChild(bold_rPr)
    bold_t = dom.createElement("w:t")
    bold_t.setAttribute("xml:space", "preserve")
    bold_t.appendChild(dom.createTextNode(f"{category}: "))
    bold_run.appendChild(bold_t)
    new_para.appendChild(bold_run)

    # Create regular run for skills
    reg_run = dom.createElement("w:r")
    reg_rPr = dom.createElement("w:rPr")
    reg_sz = dom.createElement("w:sz")
    reg_sz.setAttribute("w:val", "19")
    reg_szCs = dom.createElement("w:szCs")
    reg_szCs.setAttribute("w:val", "19")
    reg_rPr.appendChild(reg_sz)
    reg_rPr.appendChild(reg_szCs)
    reg_run.appendChild(reg_rPr)
    reg_t = dom.createElement("w:t")
    reg_t.appendChild(dom.createTextNode(skills_text))
    reg_run.appendChild(reg_t)
    new_para.appendChild(reg_run)

    return new_para


def _create_empty_paragraph(doc) -> object:
    """Create an empty paragraph for spacing."""
    dom = doc["word/document.xml"].dom
    para = dom.createElement("w:p")
    pPr = dom.createElement("w:pPr")
    spacing = dom.createElement("w:spacing")
    spacing.setAttribute("w:before", "0")
    spacing.setAttribute("w:line", "240")
    spacing.setAttribute("w:lineRule", "auto")
    pPr.appendChild(spacing)
    para.appendChild(pPr)
    return para


def _replace_experience_bullets(doc, all_paragraphs, experience_list: List[Dict]) -> None:
    """Replace experience bullets for each job.

    Jobs are hardcoded (KAVALIER, VICEGERENT, OLIVER WYMAN, DELOITTE).
    Only the bullets are variable (2-4 bullets per job).

    Template structure (paragraph indices before any modifications):
    - KAVALIER: company=13, title=14, bullets=15-17, empty=18
    - VICEGERENT: company=19, title=20, bullets=21-23, empty=24
    - OLIVER WYMAN: company=25, title=26, bullets=27-28, empty=29
    - DELOITTE: company=30, title=31, bullets=32-35, empty=36

    Args:
        doc: Document object
        all_paragraphs: NodeList of all paragraphs
        experience_list: List of dicts with 'company' and 'bullets' keys
    """
    # Map company names to their expected experience data
    # The job order must match: KAVALIER, VICEGERENT, OLIVER WYMAN, DELOITTE
    job_configs = [
        {"name": "KAVALIER", "bullet_start": 15, "bullet_count": 3},
        {"name": "VICEGERENT", "bullet_start": 21, "bullet_count": 3},
        {"name": "OLIVER WYMAN", "bullet_start": 27, "bullet_count": 2},
        {"name": "DELOITTE", "bullet_start": 32, "bullet_count": 4},
    ]

    # Process in reverse order to avoid index shifting issues
    for i, job_config in enumerate(reversed(job_configs)):
        job_idx = len(job_configs) - 1 - i
        if job_idx < len(experience_list):
            job_data = experience_list[job_idx]
            bullets = job_data.get("bullets", [])

            # Enforce 2-4 bullet limit
            if len(bullets) < 2:
                bullets = bullets + [""] * (2 - len(bullets))  # Pad to minimum
            elif len(bullets) > 4:
                bullets = bullets[:4]  # Truncate to maximum

            _replace_job_bullets(
                doc,
                all_paragraphs,
                job_config["bullet_start"],
                job_config["bullet_count"],
                bullets
            )


def _replace_job_bullets(doc, all_paragraphs, bullet_start: int, old_bullet_count: int, new_bullets: List[str]) -> None:
    """Replace bullets for a single job.

    Args:
        doc: Document object
        all_paragraphs: NodeList of all paragraphs
        bullet_start: Index of first bullet paragraph
        old_bullet_count: Number of existing bullet paragraphs
        new_bullets: List of new bullet texts (2-4 items)
    """
    body = all_paragraphs[0].parentNode

    # Get template bullet paragraph for formatting
    template_bullet = all_paragraphs[bullet_start]

    # Get numId from template bullet for list formatting
    numPr = template_bullet.getElementsByTagName("w:numPr")
    numId = "1"  # Default
    if numPr:
        numId_elem = numPr[0].getElementsByTagName("w:numId")
        if numId_elem:
            numId = numId_elem[0].getAttribute("w:val")

    # Find insertion point (paragraph after last bullet)
    insert_before_idx = bullet_start + old_bullet_count
    insert_before = all_paragraphs[insert_before_idx] if insert_before_idx < len(all_paragraphs) else None

    # Delete existing bullet paragraphs
    for i in range(old_bullet_count):
        idx = bullet_start + i
        if idx < len(all_paragraphs):
            para = all_paragraphs[idx]
            if para.parentNode:
                para.parentNode.removeChild(para)

    # Insert new bullet paragraphs
    for bullet_text in new_bullets:
        if bullet_text:  # Skip empty bullets
            new_para = _create_bullet_paragraph(doc, bullet_text, template_bullet, numId)
            if insert_before:
                body.insertBefore(new_para, insert_before)
            else:
                body.appendChild(new_para)


def _create_bullet_paragraph(doc, text: str, template_para, numId: str) -> object:
    """Create a bullet paragraph with proper formatting.

    Args:
        doc: Document object
        text: Bullet text
        template_para: Template paragraph to clone formatting from
        numId: Numbering ID for bullet list
    """
    dom = doc["word/document.xml"].dom

    # Clone template paragraph structure
    new_para = template_para.cloneNode(True)

    # Update text content
    text_elems = new_para.getElementsByTagName("w:t")
    if text_elems:
        # Replace first text element content
        if text_elems[0].firstChild:
            text_elems[0].firstChild.nodeValue = text
        else:
            text_elems[0].appendChild(dom.createTextNode(text))

        # Remove extra text elements
        for i, t in enumerate(list(text_elems)):
            if i > 0 and t.parentNode:
                # Remove the parent run if it only contains this text
                parent_run = t.parentNode
                if parent_run.tagName == "w:r":
                    parent_run.parentNode.removeChild(parent_run)

    return new_para


def _pack_docx(unpacked_dir: str, output_path: str) -> None:
    """Pack directory back to DOCX file."""
    original_dir = os.getcwd()
    os.chdir(unpacked_dir)
    try:
        subprocess.run(['zip', '-r', '-q', output_path, '.'], check=True)
    finally:
        os.chdir(original_dir)
