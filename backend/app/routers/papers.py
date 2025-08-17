from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import uuid
from typing import Any, Dict


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

    # MVP stub: read bytes and return placeholders
    _bytes = await file.read()
    _ = len(_bytes)

    return ParseResponse(
        doc_id=str(uuid.uuid4()),
        title=None,
        abstract=None,
        methodology="Extracted methodology placeholder.",
        equations=[],
        datasets=[],
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



