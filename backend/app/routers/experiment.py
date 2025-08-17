from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict
from ..core.config import settings
from ..services.sandbox import LocalExecutor, DockerExecutor


router = APIRouter()


class RunRequest(BaseModel):
    code: str


class RunResponse(BaseModel):
    stdout: str
    stderr: str
    returncode: int


@router.post("/run", response_model=RunResponse)
async def run_code(req: RunRequest) -> Dict[str, Any]:
    if settings.sandbox_mode == "docker":
        executor = DockerExecutor(
            image=settings.docker_image,
            memory=settings.docker_memory,
            cpus=settings.docker_cpus,
        )
    else:
        executor = LocalExecutor()

    result = executor.run_code(req.code, timeout_seconds=60)
    return RunResponse(stdout=result.stdout, stderr=result.stderr, returncode=result.returncode)



