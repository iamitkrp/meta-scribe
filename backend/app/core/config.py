from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    cors_allow_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    openai_api_key: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


