# METASCRIBE Backend (FastAPI)

## Setup

```bash
python -m venv .venv
# PowerShell
. .venv/Scripts/Activate.ps1
pip install -r backend/requirements.txt
# For PDF parsing features, also install optional:
# pip install -r backend/requirements-optional.txt
uvicorn backend.app.main:app --reload --port 8000
```

## Endpoints (MVP)
- POST `/papers/parse` (multipart PDF)
- POST `/papers/parse-arxiv` (json: { url })
- POST `/pseudocode/generate` (json: { methodology })
- POST `/codegen/generate` (json: { pseudocode, framework })
- POST `/experiment/run` (json: { code })
- GET `/health`

```bash
curl http://localhost:8000/health
```

## LLM Configuration
-## Sandbox
- Modes:
- `SANDBOX_MODE=local` (default) executes with the host Python in a temp file
- `SANDBOX_MODE=docker` runs inside Docker with no network and resource limits
- Docker settings (env): `DOCKER_IMAGE` (default `python:3.11-slim`), `DOCKER_MEMORY` (e.g., `512m`), `DOCKER_CPUS` (e.g., `0.5`)

- Default provider: Gemini
- Env var: `GEMINI_API_KEY` (or pass `api_key` from frontend)
- Frontend can send `{ provider: "gemini", api_key: "..." }` for `/pseudocode/generate` and `/codegen/generate`.



