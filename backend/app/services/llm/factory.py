from __future__ import annotations

from typing import Optional

from .base import LLMClient
from .gemini import GeminiClient


def create_llm_client(provider: str, *,
                      gemini_api_key: Optional[str] = None,
                      openai_api_key: Optional[str] = None,
                      anthropic_api_key: Optional[str] = None) -> LLMClient:
    p = (provider or "").lower()
    if p in ("gemini", "google", "googleai"):
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY missing")
        return GeminiClient(api_key=gemini_api_key)
    # Future: implement OpenAI/Anthropic adapters
    raise ValueError(f"Unsupported provider: {provider}")


