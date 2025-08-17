from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    cors_allow_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    llm_provider: str = "gemini"  # default provider
    gemini_api_key: str | None = None
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    sandbox_mode: str = "local"  # 'local' | 'docker'
    docker_image: str = "python:3.11-slim"
    docker_memory: str = "512m"
    docker_cpus: str = "0.5"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        fields = {
            "sandbox_mode": {"env": ["SANDBOX_MODE"]},
            "docker_image": {"env": ["DOCKER_IMAGE"]},
            "docker_memory": {"env": ["DOCKER_MEMORY"]},
            "docker_cpus": {"env": ["DOCKER_CPUS"]},
            "gemini_api_key": {"env": ["GEMINI_API_KEY"]},
            "openai_api_key": {"env": ["OPENAI_API_KEY"]},
            "anthropic_api_key": {"env": ["ANTHROPIC_API_KEY"]},
        }


settings = Settings()


