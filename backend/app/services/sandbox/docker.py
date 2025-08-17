from __future__ import annotations

import os
import subprocess
import tempfile
from textwrap import dedent
from .base import RunResult


class DockerExecutor:
    def __init__(self, image: str = "python:3.11-slim", memory: str = "512m", cpus: str = "0.5") -> None:
        self.image = image
        self.memory = memory
        self.cpus = cpus

    def run_code(self, code: str, timeout_seconds: int = 60) -> RunResult:
        with tempfile.TemporaryDirectory() as tmp:
            code_path = os.path.join(tmp, "main.py")
            with open(code_path, "w", encoding="utf-8") as f:
                f.write(code)

            cmd = [
                "docker", "run", "--rm",
                "--network", "none",
                "--memory", self.memory,
                "--cpus", self.cpus,
                "-v", f"{code_path}:/app/main.py:ro",
                "-w", "/app",
                self.image,
                "python", "main.py",
            ]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
            return RunResult(stdout=proc.stdout, stderr=proc.stderr, returncode=proc.returncode)


