# METASCRIBE

AI Agent for Research Paper Implementation.

## Structure
- `frontend/`: Next.js app (MVP UI)
- `backend/`: FastAPI service

## Quickstart (Windows PowerShell)

```powershell
# Backend
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000

# Frontend (in new terminal)
cd frontend
npm run dev
```

Open `http://localhost:3000`.
