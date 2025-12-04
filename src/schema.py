"""Database schema utilities for the Goodreads pipeline."""

from __future__ import annotations

import re
from typing import Iterable, Tuple

from sqlalchemy import text
from sqlalchemy.engine import Engine

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(value: str) -> str:
    if not _IDENTIFIER_RE.match(value):
        raise ValueError(f"Invalid SQL identifier: {value!r}")
    return value


def _ensure_primary_key(engine: Engine, table: str) -> None:
    query = text(
        f"""
        SELECT COUNT(*)
        FROM pg_constraint
        WHERE conrelid = '{table}'::regclass
          AND contype = 'p'
        """
    )
    alter = text(f'ALTER TABLE "{table}" ADD PRIMARY KEY (book_id)')

    with engine.begin() as conn:
        has_pk = conn.execute(query).scalar_one()
        if not has_pk:
            conn.execute(alter)


def _ensure_indexes(engine: Engine, table: str, specs: Iterable[Tuple[str, str]]) -> None:
    statements = [
        text(f'CREATE INDEX IF NOT EXISTS "{index_name}" ON "{table}" ({column})')
        for index_name, column in specs
    ]
    with engine.begin() as conn:
        for statement in statements:
            conn.execute(statement)


def ensure_books_clean_schema(engine: Engine, table_name: str = "books_clean") -> None:
    """Ensure the books_clean table has a primary key and helpful indexes."""

    table = _validate_identifier(table_name)
    _ensure_primary_key(engine, table)
    index_specs = [
        (f"idx_{table}_publication_date", "publication_date"),
        (f"idx_{table}_average_rating", "average_rating"),
        (f"idx_{table}_authors", "authors"),
    ]
    _ensure_indexes(engine, table, index_specs)
