from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class LLMClient(ABC):
    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        **kwargs: Dict[str, Any],
    ) -> str:
        raise NotImplementedError


