from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class PseudocodeRequest(BaseModel):
    methodology: str


class PseudocodeResponse(BaseModel):
    pseudocode: str


@router.post("/generate", response_model=PseudocodeResponse)
async def generate_pseudocode(req: PseudocodeRequest) -> PseudocodeResponse:
    # MVP: trivial deterministic pseudocode scaffold
    pseudo = (
        "INPUT: research methodology\n"
        "OUTPUT: runnable ML pipeline steps\n\n"
        "1. Parse problem setup and objectives\n"
        "2. Identify datasets and preprocessing\n"
        "3. Define model architecture\n"
        "4. Specify loss, metrics, and optimizer\n"
        "5. Implement training loop\n"
        "6. Evaluate and log results\n"
    )
    return PseudocodeResponse(pseudocode=pseudo)



