"""Smoke tests for reporting artifacts (charts and slides)."""
from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from src.analyses.support.storytelling.plot_comparison_summary import render_chart
from src.analyses.support.storytelling.export_phase05_slide import export_slide

matplotlib.use("Agg")  # ensure headless-friendly backend


def _write_sample_summary(tmp_path: Path) -> Path:
    summary_path = tmp_path / "comparison_summary.csv"
    sample = pd.DataFrame(
        [
            {
                "comparison": "M1_top_authors_by_weighted_rating",
                "rows_sql": 15,
                "rows_pandas": 15,
                "shared_rows": 15,
                "row_match": "yes",
                "value_mismatches": 0,
                "diff_path": "",
                "notes": "Match",
            },
            {
                "comparison": "M3_top_books_by_ratings_count",
                "rows_sql": 20,
                "rows_pandas": 20,
                "shared_rows": 20,
                "row_match": "yes",
                "value_mismatches": 0,
                "diff_path": "",
                "notes": "Match",
            },
        ]
    )
    sample.to_csv(summary_path, index=False)
    return summary_path


def _write_dummy_chart(chart_path: Path) -> None:
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    ax.set_title("Placeholder chart")
    fig.savefig(chart_path)
    plt.close(fig)


def test_render_chart_creates_png(tmp_path: Path) -> None:
    summary_path = _write_sample_summary(tmp_path)
    output_png = tmp_path / "comparison_summary.png"

    render_chart(summary_path, output_png)

    assert output_png.exists()
    assert output_png.stat().st_size > 0


def test_export_slide_creates_pptx(tmp_path: Path) -> None:
    summary_path = _write_sample_summary(tmp_path)
    chart_path = tmp_path / "comparison_summary.png"
    _write_dummy_chart(chart_path)
    notes_path = tmp_path / "notes.md"
    notes_path.write_text("# Notes\n- Sample content")
    output_pptx = tmp_path / "phase05-slide.pptx"

    export_slide(notes_path, summary_path, chart_path, output_pptx)

    assert output_pptx.exists()
    assert output_pptx.stat().st_size > 0
