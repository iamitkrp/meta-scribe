from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import tempfile
import sys
from typing import Any, Dict


router = APIRouter()


class RunRequest(BaseModel):
    code: str


class RunResponse(BaseModel):
    stdout: str
    stderr: str
    returncode: int


@router.post("/run", response_model=RunResponse)
async def run_code(req: RunRequest) -> Dict[str, Any]:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fp:
        fp.write(req.code)
        fp.flush()
        proc = subprocess.run(
            [sys.executable, fp.name],
            capture_output=True,
            text=True,
            timeout=60,
        )
    return RunResponse(stdout=proc.stdout, stderr=proc.stderr, returncode=proc.returncode)



