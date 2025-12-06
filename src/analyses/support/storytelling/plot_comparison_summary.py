"""Render the SQL vs pandas comparison summary chart for Phase 05 - Step 03."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DEFAULT_INPUT = Path("outputs/phase05_step03_task01/comparison_summary.csv")
DEFAULT_OUTPUT = Path("outputs/phase05_step03_task01/comparison_summary.png")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot the SQL vs pandas comparison summary as a PNG chart."
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="Path to comparison_summary.csv (default: outputs/phase05_step03_task01/comparison_summary.csv)",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Destination PNG path (default: outputs/phase05_step03_task01/comparison_summary.png)",
    )
    return parser.parse_args(argv)


def render_chart(input_csv: Path, output_png: Path) -> None:
    summary = pd.read_csv(input_csv)
    if summary.empty:
        raise SystemExit(
            f"{input_csv} is empty; run python -m src.analyses.portfolio.p04_sql_vs_pandas_compare first."
        )

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    axes[0].bar(summary["comparison"], summary["rows_sql"], label="SQL rows", color="#4e79a7")
    axes[0].bar(
        summary["comparison"],
        summary["rows_pandas"],
        label="pandas rows",
        color="#f28e2b",
        alpha=0.7,
    )
    axes[0].set_ylabel("Row count")
    axes[0].set_title("Row coverage per metric (SQL vs pandas)")
    axes[0].tick_params(axis="x", rotation=30)
    axes[0].legend(loc="upper right")

    axes[1].bar(summary["comparison"], summary["value_mismatches"], color="#e15759")
    axes[1].set_ylabel("Value mismatches")
    axes[1].set_title("Mismatch counts per metric")
    axes[1].tick_params(axis="x", rotation=30)

    for ax in axes:
        ax.grid(axis="y", linestyle="--", alpha=0.4)

    fig.tight_layout()
    output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_png, dpi=150, bbox_inches="tight")
    print(f"Saved chart to {output_png}")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    render_chart(input_csv=Path(args.input), output_png=Path(args.output))


if __name__ == "__main__":  # pragma: no cover
    main()
