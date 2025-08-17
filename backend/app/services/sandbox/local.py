from __future__ import annotations

import subprocess
import sys
import tempfile
from .base import RunResult


class LocalExecutor:
    def run_code(self, code: str, timeout_seconds: int = 60) -> RunResult:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fp:
            fp.write(code)
            fp.flush()
            proc = subprocess.run(
                [sys.executable, fp.name],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
        return RunResult(stdout=proc.stdout, stderr=proc.stderr, returncode=proc.returncode)


