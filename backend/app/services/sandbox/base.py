from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class RunResult:
    stdout: str
    stderr: str
    returncode: int


class SandboxExecutor(Protocol):
    def run_code(self, code: str, timeout_seconds: int = 60) -> RunResult:  # pragma: no cover - protocol
        ...


