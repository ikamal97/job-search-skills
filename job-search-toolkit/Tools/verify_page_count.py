#!/usr/bin/env python3
"""
Verify DOCX fits on exactly one page.
Uses LibreOffice for conversion, pdfinfo for page counting.

Usage:
    python verify_page_count.py <docx_file>

Exit codes:
    0 = Document is exactly 1 page
    1 = Document is NOT 1 page (returns page count in output)
    2 = Error (conversion failed, file not found, etc.)
"""
import subprocess
import tempfile
import sys
from pathlib import Path


def get_page_count(docx_path: str) -> int:
    """
    Convert DOCX to PDF and return page count.

    Args:
        docx_path: Path to the DOCX file

    Returns:
        Number of pages in the document

    Raises:
        FileNotFoundError: If the DOCX file doesn't exist
        RuntimeError: If conversion fails or page count can't be determined
    """
    docx_path = Path(docx_path).resolve()

    if not docx_path.exists():
        raise FileNotFoundError(f"File not found: {docx_path}")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Convert DOCX to PDF using LibreOffice
        result = subprocess.run([
            'soffice', '--headless', '--convert-to', 'pdf',
            '--outdir', tmpdir, str(docx_path)
        ], capture_output=True, timeout=60)

        if result.returncode != 0:
            stderr = result.stderr.decode() if result.stderr else "Unknown error"
            raise RuntimeError(f"PDF conversion failed: {stderr}")

        # Find the PDF file
        pdf_path = Path(tmpdir) / (docx_path.stem + '.pdf')

        if not pdf_path.exists():
            raise RuntimeError(f"PDF not created at expected path: {pdf_path}")

        # Count pages using pdfinfo
        result = subprocess.run(
            ['pdfinfo', str(pdf_path)],
            capture_output=True, text=True, timeout=10
        )

        if result.returncode != 0:
            raise RuntimeError(f"pdfinfo failed: {result.stderr}")

        for line in result.stdout.split('\n'):
            if line.startswith('Pages:'):
                return int(line.split(':')[1].strip())

        raise RuntimeError("Could not determine page count from pdfinfo output")


def verify_single_page(docx_path: str) -> bool:
    """
    Returns True if document is exactly one page.

    Args:
        docx_path: Path to the DOCX file

    Returns:
        True if document is exactly 1 page, False otherwise
    """
    return get_page_count(docx_path) == 1


def main():
    if len(sys.argv) != 2:
        print("Usage: python verify_page_count.py <docx_file>")
        print("\nVerifies that a DOCX file fits on exactly one page.")
        print("Exit code 0 = exactly 1 page, Exit code 1 = not 1 page")
        sys.exit(2)

    docx_path = sys.argv[1]

    try:
        pages = get_page_count(docx_path)

        if pages == 1:
            print(f"✓ Document is exactly 1 page")
            sys.exit(0)
        else:
            print(f"✗ Document is {pages} pages (needs reduction)")
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(2)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(2)


if __name__ == '__main__':
    main()
