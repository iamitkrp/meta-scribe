from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..core.config import settings
from ..services.llm.factory import create_llm_client


router = APIRouter()


class PseudocodeRequest(BaseModel):
    methodology: str
    provider: str | None = None
    api_key: str | None = None


class PseudocodeResponse(BaseModel):
    pseudocode: str


@router.post("/generate", response_model=PseudocodeResponse)
async def generate_pseudocode(req: PseudocodeRequest) -> PseudocodeResponse:
    provider = req.provider or settings.llm_provider
    api_key = req.api_key or settings.gemini_api_key
    if not api_key:
        raise HTTPException(status_code=400, detail="Missing API key for LLM provider")
    client = create_llm_client(provider, gemini_api_key=api_key)
    system = (
        "You are an expert ML research engineer. Convert the provided methodology into precise,\n"
        "stepwise pseudocode suitable for implementing in PyTorch or TensorFlow. Keep it concise and executable."
    )
    text = client.generate_text(
        prompt=f"Methodology:\n{req.methodology}\n\nReturn only pseudocode.",
        system_prompt=system,
        temperature=0.2,
        max_tokens=1024,
    )
    return PseudocodeResponse(pseudocode=text.strip())



