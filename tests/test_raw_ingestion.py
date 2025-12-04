"""Tests for repairing malformed rows when loading the raw books CSV."""

from __future__ import annotations

from pathlib import Path

from src.raw_ingestion import COLUMN_NAMES, load_books_csv


def _write_csv(path: Path, rows: list[list[str]]) -> None:
    header = ",".join(COLUMN_NAMES)
    payload = [header]
    payload.extend(",".join(row) for row in rows)
    path.write_text("\n".join(payload), encoding="utf-8")


def test_load_books_csv_preserves_well_formed_rows(tmp_path) -> None:
    csv_path = tmp_path / "books.csv"
    rows = [
        [
            "1",
            "Title",
            "Alpha / Beta",
            "4.0",
            "1234567890",
            "9781234567897",
            "en",
            "100",
            "10",
            "2",
            "1/1/2020",
            "Publisher",
        ]
    ]
    _write_csv(csv_path, rows)

    df, stats = load_books_csv(str(csv_path))

    assert len(df) == 1
    assert stats.repaired_rows == 0
    assert df.loc[0, "authors"] == "Alpha / Beta"


def test_load_books_csv_repairs_author_commas(tmp_path) -> None:
    csv_path = tmp_path / "books.csv"
    malformed_row = [
        "2",
        "Another Title",
        "Author One",
        " Jr./Coauthor",
        "3.5",
        "0987654321",
        "9780987654321",
        "en",
        "200",
        "20",
        "4",
        "2/2/2020",
        "Another Publisher",
    ]
    _write_csv(csv_path, [malformed_row])

    df, stats = load_books_csv(str(csv_path))

    assert len(df) == 1
    assert stats.repaired_rows == 1
    assert df.loc[0, "authors"] == "Author One, Jr./Coauthor"