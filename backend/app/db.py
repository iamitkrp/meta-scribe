from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator
from sqlmodel import SQLModel, Session, create_engine


engine = create_engine("sqlite:///./metascribe.db", echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


