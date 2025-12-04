"""Smoke tests for the books_clean table when DATABASE_URL is available."""

from __future__ import annotations

import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from src.db_config import build_database_url_from_env

load_dotenv()


def _get_database_url() -> str | None:
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    try:
        return build_database_url_from_env()
    except RuntimeError:
        return None


@pytest.fixture(scope="module")
def pg_conn():
    url = _get_database_url()
    if not url:
        pytest.skip("DATABASE_URL is not defined; skipping Postgres smoke tests.")
    engine = create_engine(url)
    try:
        connection = engine.connect()
    except OperationalError as exc:  # pragma: no cover - depends on env
        pytest.skip(f"Cannot connect to Postgres: {exc}")
    try:
        yield connection
    finally:
        connection.close()
        engine.dispose()


def test_books_clean_table_has_rows(pg_conn) -> None:
    count = pg_conn.execute(text("SELECT COUNT(*) FROM books_clean")).scalar_one()
    assert count > 0


def test_books_clean_has_primary_key_and_indexes(pg_conn) -> None:
    pk_count = pg_conn.execute(
        text(
            """
            SELECT COUNT(*)
            FROM pg_constraint
            WHERE conrelid = 'books_clean'::regclass
              AND contype = 'p'
            """
        )
    ).scalar_one()
    assert pk_count == 1

    index_rows = pg_conn.execute(
        text(
            """
            SELECT indexname
            FROM pg_indexes
            WHERE schemaname = 'public'
              AND tablename = 'books_clean'
            """
        )
    ).fetchall()
    index_names = {row.indexname for row in index_rows}
    expected = {
        "idx_books_clean_publication_date",
        "idx_books_clean_average_rating",
        "idx_books_clean_authors",
    }
    missing = expected - index_names
    assert not missing, f"Missing expected indexes: {sorted(missing)}"
