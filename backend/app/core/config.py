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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


