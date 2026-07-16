import re
from pathlib import Path

import fitz
import pdfplumber

CLAUSE_HEADER_RE = re.compile(
    r'(?P<header>\b(?:Section|Article|Clause|Chapter|Part)\s+[0-9A-Za-z\-\.]+)\b',
    re.IGNORECASE,
)


def extract_text_with_pages(pdf_path):
    """
    Extract text from each page of a PDF and return a list of page dictionaries.
    Falls back to pdfplumber OCR-style extraction for empty pages.
    """
    pdf_path = Path(pdf_path)
    page_texts = []

    with fitz.open(pdf_path) as pdf, pdfplumber.open(pdf_path) as plumber_pdf:
        for page_number in range(len(pdf)):
            page = pdf[page_number]
            text = page.get_text("text") or ""

            if not text.strip():
                pdfplumber_page = plumber_pdf.pages[page_number]
                text = pdfplumber_page.extract_text() or ""

            page_texts.append({"page": page_number + 1, "text": text.strip()})

    return page_texts


def chunk_by_clauses(page_texts):
    """
    Split page texts into legal clause chunks using headings.
    If no clause headers are detected, fall back to an overlapping word chunker.
    """
    chunks = []

    for page in page_texts:
        text = page.get("text", "")
        if not text:
            continue

        matches = list(CLAUSE_HEADER_RE.finditer(text))
        if not matches:
            continue

        for index, match in enumerate(matches):
            start = match.start()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            chunk_text = text[start:end].strip()
            clause_label = match.group("header").strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page": page["page"],
                    "clause": clause_label,
                })

    if chunks:
        return chunks

    return _fallback_chunk_by_words(page_texts)


def _fallback_chunk_by_words(page_texts, chunk_size=300, overlap=50):
    """
    Create overlapping chunks when explicit clause headers cannot be found.
    """
    tokenized = []
    for page in page_texts:
        words = page.get("text", "").split()
        for word in words:
            tokenized.append({"word": word, "page": page["page"]})

    if not tokenized:
        return []

    chunks = []
    start = 0
    total_words = len(tokenized)

    while start < total_words:
        end = min(start + chunk_size, total_words)
        words = [token["word"] for token in tokenized[start:end]]
        page = tokenized[start]["page"]
        text = " ".join(words)

        chunks.append(
            {
                "text": text,
                "page": page,
                "clause": f"Page {page} fallback",
            }
        )

        if end == total_words:
            break

        start += chunk_size - overlap

    return chunks
