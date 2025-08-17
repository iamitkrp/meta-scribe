from __future__ import annotations

from typing import Optional, Dict, Any, List

from .base import LLMClient


class GeminiClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash") -> None:
        import google.generativeai as genai  # lazy import

        self._genai = genai
        self._genai.configure(api_key=api_key)
        self._model_name = model

    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        **kwargs: Dict[str, Any],
    ) -> str:
        model = self._genai.GenerativeModel(self._model_name)

        contents: List[str] = []
        if system_prompt:
            contents.append(system_prompt)
        contents.append(prompt)

        generation_config = {
            "temperature": temperature,
        }
        if max_tokens is not None:
            generation_config["max_output_tokens"] = max_tokens

        resp = model.generate_content(
            contents,
            generation_config=generation_config,
        )

        try:
            return resp.text or ""
        except Exception:
            # some SDK versions use different structure
            if hasattr(resp, "candidates") and resp.candidates:
                parts = getattr(resp.candidates[0], "content", None)
                if parts and hasattr(parts, "parts") and parts.parts:
                    return getattr(parts.parts[0], "text", "")
            return ""


