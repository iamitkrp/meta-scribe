from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.papers import router as papers_router
from .routers.pseudocode import router as pseudocode_router
from .routers.codegen import router as codegen_router
from .routers.experiment import router as experiment_router
from .routers.eval import router as eval_router
from .core.config import settings
from .db import init_db


def create_app() -> FastAPI:
    application = FastAPI(
        title="METASCRIBE API",
        version="0.1.0",
        description="Backend API for METASCRIBE: AI Agent for Research Paper Implementation",
    )

    # CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    application.include_router(papers_router, prefix="/papers", tags=["papers"])
    application.include_router(pseudocode_router, prefix="/pseudocode", tags=["pseudocode"])
    application.include_router(codegen_router, prefix="/codegen", tags=["codegen"])
    application.include_router(experiment_router, prefix="/experiment", tags=["experiment"])
    application.include_router(eval_router, prefix="/eval", tags=["eval"])

    @application.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return application


app = create_app()

# Initialize DB at import time for dev simplicity
try:
    init_db()
except Exception:
    pass


