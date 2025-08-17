from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import uuid
from typing import Any, Dict
from ..services.pdf.parser import (
    extract_text_from_pdf_bytes,
    split_into_sections,
    detect_datasets,
    extract_equations,
    guess_abstract,
    guess_methodology,
)


router = APIRouter()


class ParseResponse(BaseModel):
    doc_id: str
    title: str | None = None
    abstract: str | None = None
    methodology: str | None = None
    equations: list[str] = []
    datasets: list[str] = []


@router.post("/parse", response_model=ParseResponse)
async def parse_paper(file: UploadFile = File(...)) -> Any:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported in MVP")

    pdf_bytes = await file.read()
    try:
        full_text = extract_text_from_pdf_bytes(pdf_bytes)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    sections = split_into_sections(full_text)
    abstract = guess_abstract(sections, full_text)
    methodology = guess_methodology(sections, full_text) or ""
    datasets = detect_datasets(full_text)
    equations = extract_equations(full_text, max_equations=5)

    return ParseResponse(
        doc_id=str(uuid.uuid4()),
        title=None,
        abstract=abstract,
        methodology=methodology,
        equations=equations,
        datasets=datasets,
    )


class ArxivRequest(BaseModel):
    url: str


@router.post("/parse-arxiv", response_model=ParseResponse)
async def parse_arxiv(req: ArxivRequest) -> Dict[str, Any]:
    return ParseResponse(
        doc_id=str(uuid.uuid4()),
        title=None,
        abstract=None,
        methodology="Extracted methodology placeholder from arXiv.",
        equations=[],
        datasets=[],
    )



