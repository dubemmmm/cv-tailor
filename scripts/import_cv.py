#!/usr/bin/env python3
"""Extract a master CV PDF into a reviewable Markdown file."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INBOX = ROOT / "master" / "inbox"
DEFAULT_OUTPUT = ROOT / "master" / "master_cv.md"
KNOWN_HEADINGS = {
    "summary",
    "education",
    "experience",
    "work experience",
    "professional experience",
    "projects",
    "skills",
    "technical skills",
    "certifications",
    "publications",
    "research",
    "leadership",
    "leadership & involvement",
    "awards",
    "volunteering",
}
BULLET_RE = re.compile(r"^\s*[•●▪◦‣]\s*")


def choose_input(explicit_path: Path | None, inbox: Path) -> Path:
    if explicit_path is not None:
        candidate = explicit_path.expanduser().resolve()
        if not candidate.is_file():
            raise ValueError(f"PDF not found: {candidate}")
        if candidate.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a .pdf file, got: {candidate.name}")
        return candidate

    pdfs = sorted(inbox.glob("*.pdf"))
    if not pdfs:
        raise ValueError(
            f"No PDF found in {inbox}. Add your CV there or pass a PDF path."
        )
    if len(pdfs) > 1:
        names = ", ".join(path.name for path in pdfs)
        raise ValueError(
            f"Found multiple PDFs in {inbox}: {names}. Pass the one to import."
        )
    return pdfs[0]


def line_to_markdown(line: str) -> str:
    """Apply conservative Markdown structure without rewriting CV content."""
    cleaned = re.sub(r"\s+", " ", line).strip()
    if not cleaned:
        return ""
    if BULLET_RE.match(cleaned):
        return f"- {BULLET_RE.sub('', cleaned)}"

    heading_key = cleaned.rstrip(":").casefold()
    if heading_key in KNOWN_HEADINGS:
        heading = cleaned.rstrip(":")
        return f"## {heading.title() if heading.isupper() else heading}"
    if (
        2 <= len(cleaned) <= 45
        and cleaned.isupper()
        and any(character.isalpha() for character in cleaned)
    ):
        return f"## {cleaned.title()}"
    return cleaned


def extract_markdown(pdf_path: Path) -> tuple[str, int]:
    reader = PdfReader(str(pdf_path))
    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception as exc:  # pypdf exposes several encryption errors
            raise ValueError("The PDF is password-protected and cannot be read.") from exc

    sections: list[str] = [
        "# Master CV",
        "",
        "<!-- Generated from a PDF. Review formatting and facts before tailoring. -->",
    ]
    extracted_characters = 0
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        extracted_characters += len(text.strip())
        lines = [line_to_markdown(line) for line in text.splitlines()]
        lines = [line for line in lines if line]
        if lines:
            sections.extend(["", f"<!-- Source page {page_number} -->", "", *lines])

    if extracted_characters < 40:
        raise ValueError(
            "Almost no text could be extracted. The PDF is probably scanned; "
            "run OCR on it first, then try again."
        )
    return "\n".join(sections).rstrip() + "\n", len(reader.pages)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a text-based CV PDF into Markdown for CV Tailor."
    )
    parser.add_argument(
        "pdf",
        nargs="?",
        type=Path,
        help="PDF path (default: the only PDF in master/inbox/)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Markdown destination (default: master/master_cv.md)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing output file",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    output = args.output.expanduser().resolve()
    try:
        source = choose_input(args.pdf, DEFAULT_INBOX)
        if output.exists() and not args.force:
            raise ValueError(
                f"Output already exists: {output}. Use --force to replace it."
            )
        markdown, page_count = extract_markdown(source)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown, encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Imported {page_count} page(s) from {source}")
    print(f"Wrote {output}")
    print("Next: review the Markdown and complete master/eligibility.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
