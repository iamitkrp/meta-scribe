from __future__ import annotations

import io
import re
from typing import Dict, List, Optional, Tuple


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes using PyMuPDF if available, otherwise pdfplumber.

    Raises a RuntimeError if no supported backend is available.
    """
    # Try PyMuPDF (fitz)
    try:
        import fitz  # type: ignore

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        try:
            page_texts: List[str] = []
            for page in doc:
                try:
                    page_texts.append(page.get_text("text"))
                except Exception:
                    page_texts.append("")
            return "\n".join(page_texts)
        finally:
            doc.close()
    except ImportError:
        pass

    # Fallback: pdfplumber
    try:
        import pdfplumber  # type: ignore

        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            page_texts: List[str] = []
            for page in pdf.pages:
                try:
                    page_texts.append(page.extract_text() or "")
                except Exception:
                    page_texts.append("")
            return "\n".join(page_texts)
    except ImportError:
        pass

    raise RuntimeError(
        "No PDF text extraction backend available. Install PyMuPDF or pdfplumber (see requirements-optional.txt)."
    )


SECTION_KEYS = [
    "abstract",
    "introduction",
    "background",
    "related work",
    "method",
    "methods",
    "methodology",
    "approach",
    "experiments",
    "results",
    "discussion",
    "conclusion",
]


def _find_heading_spans(text: str) -> List[Tuple[str, int]]:
    """Return list of (heading_key, start_index) for detected headings."""
    spans: List[Tuple[str, int]] = []
    lowered = text.lower()
    for key in SECTION_KEYS:
        # heuristics: heading on its own line or followed by newline
        for m in re.finditer(rf"\n\s*{re.escape(key)}s?\s*\n", lowered):
            spans.append((key, m.start()))
        # also match at the very beginning
        if lowered.startswith(key):
            spans.append((key, 0))
    # deduplicate and sort by position
    seen: set[Tuple[str, int]] = set()
    unique_spans: List[Tuple[str, int]] = []
    for item in sorted(spans, key=lambda x: x[1]):
        if item not in seen:
            seen.add(item)
            unique_spans.append(item)
    return unique_spans


def split_into_sections(text: str) -> Dict[str, str]:
    """Very simple section splitter using heading heuristics."""
    sections: Dict[str, str] = {}
    if not text:
        return sections
    spans = _find_heading_spans(text)
    if not spans:
        sections["full"] = text
        return sections
    # Build ranges
    for idx, (key, start) in enumerate(spans):
        end = spans[idx + 1][1] if idx + 1 < len(spans) else len(text)
        chunk = text[start:end].strip()
        sections[key] = chunk
    return sections


COMMON_DATASETS = [
    "mnist",
    "fashion-mnist",
    "cifar-10",
    "cifar-100",
    "imagenet",
    "coco",
    "squad",
    "glue",
    "wikitext-103",
    "librispeech",
    "cityscapes",
    "kitti",
    "pascal voc",
    "ms coco",
    "places365",
    "celeba",
    "yelp",
    "ag news",
]


def detect_datasets(text: str) -> List[str]:
    lowered = text.lower()
    found: List[str] = []
    for name in COMMON_DATASETS:
        if name in lowered:
            found.append(name)
    # unique, keep order
    unique: List[str] = []
    for n in found:
        if n not in unique:
            unique.append(n)
    return unique


LATEX_INLINE = re.compile(r"\$(.+?)\$", re.DOTALL)
LATEX_BLOCK = re.compile(r"\\begin\{equation\}(.+?)\\end\{equation\}", re.DOTALL)


def extract_equations(text: str, max_equations: int = 5) -> List[str]:
    equations: List[str] = []
    for m in LATEX_BLOCK.finditer(text):
        equations.append(m.group(0).strip())
        if len(equations) >= max_equations:
            return equations
    for m in LATEX_INLINE.finditer(text):
        equations.append(m.group(0).strip())
        if len(equations) >= max_equations:
            return equations
    return equations


def guess_abstract(sections: Dict[str, str], full_text: str) -> Optional[str]:
    for key in ("abstract",):
        if key in sections:
            # Trim the heading itself if present
            return re.sub(r"^\s*abstract\s*\n", "", sections[key], flags=re.I).strip() or None
    # fallback: first 1200 chars from start
    snippet = full_text.strip()[:1200]
    return snippet or None


def guess_methodology(sections: Dict[str, str], full_text: str) -> Optional[str]:
    for key in ("methodology", "methods", "method", "approach"):
        if key in sections:
            # drop heading line
            return re.sub(rf"^\s*{key}\s*\n", "", sections[key], flags=re.I).strip() or None
    # fallback: try between introduction and experiments/results
    lower = full_text.lower()
    intro_idx = lower.find("introduction")
    exp_idx = lower.find("experiments")
    res_idx = lower.find("results")
    end_idx = min(x for x in [exp_idx, res_idx] if x != -1) if (exp_idx != -1 or res_idx != -1) else -1
    if intro_idx != -1 and end_idx != -1 and end_idx > intro_idx:
        return full_text[intro_idx:end_idx].strip()
    return None


