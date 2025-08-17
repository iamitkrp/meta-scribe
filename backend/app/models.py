from __future__ import annotations

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Paper(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    doc_id: str = Field(index=True)
    title: Optional[str] = None
    abstract: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Run(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    doc_id: Optional[str] = Field(default=None, index=True)
    code: str
    stdout: str
    stderr: str
    returncode: int
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class Evaluation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: int = Field(index=True, foreign_key="run.id")
    metric_name: str
    reported: float
    measured: float
    direction: str  # 'higher' or 'lower'
    delta: float
    threshold: float
    pattern: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


