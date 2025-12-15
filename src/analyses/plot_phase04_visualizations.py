"""
Phase 04 · Step 03 · Task 02 – Portfolio Visualization Script

This script generates all must-have charts for Phase 04 using the outputs from the core metrics suite. Each chart is saved as a PNG in outputs/phase04_visualizations/ and includes a caption for portfolio documentation.

Usage (from repo root):
    docker compose --env-file .env.example -f docker-compose.python.yml run --no-deps --rm app python -m src.analyses.plot_phase04_visualizations --input-dir outputs/phase04_core_metrics --output-dir outputs/phase04_visualizations
"""
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chart definitions (mapping from plan)
CHARTS = [
    {
        "csv": "M1_top_authors_by_weighted_rating.csv",
        "title": "Top Authors by Weighted Rating",
        "caption": "Shows the 15 highest-rated authors (weighted by ratings count, min 5,000 ratings)",
        "type": "barh",
        "x": "Weighted rating",
        "y": "Author",
        "filter": lambda df: df.head(15),
        "filename": "M1_top_authors_by_weighted_rating.png"
    },
    {
        "csv": "M3_top_books_by_ratings_count.csv",
        "title": "Top Books by Ratings Count (Capped)",
        "caption": "Highlights the 20 most-rated books (capped at 597,244)",
        "type": "barh",
        "x": "Ratings count (capped)",
        "y": "Book title",
        "filter": lambda df: df.head(20),
        "filename": "M3_top_books_by_ratings_count.png"
    },
    {
        "csv": "M4_top_books_by_text_reviews.csv",
        "title": "Top Books by Text Reviews (Capped)",
        "caption": "Highlights the 20 books with the most text reviews (capped at 14,812)",
        "type": "barh",
        "x": "Text reviews count (capped)",
        "y": "Book title",
        "filter": lambda df: df.head(20),
        "filename": "M4_top_books_by_text_reviews.png"
    },
    {
        "csv": "M5_median_rating_by_page_length.csv",
        "title": "Median Rating by Page Length Bucket",
        "caption": "Compares median ratings across page length buckets (short, zero/audio, multi-volume)",
        "type": "box",
        "x": "Page length bucket",
        "y": "Median rating",
        "filter": None,
        "filename": "M5_median_rating_by_page_length.png"
    },
    {
        "csv": "M7_average_rating_by_year.csv",
        "title": "Average Rating by Publication Year",
        "caption": "Shows average rating trends from 1900 to 2012",
        "type": "line",
        "x": "Publication year",
        "y": "Average rating",
        "filter": None,
        "filename": "M7_average_rating_by_year.png"
    },
    {
        "csv": "M8_median_ratings_count_by_year.csv",
        "title": "Median Ratings Count by Publication Year",
        "caption": "Shows median ratings count trends from 1900 to 2012",
        "type": "line",
        "x": "Publication year",
        "y": "Median ratings count (capped)",
        "filter": None,
        "filename": "M8_median_ratings_count_by_year.png"
    },
    {
        "csv": "M9_language_rating_summary.csv",
        "title": "Average Rating by Language",
        "caption": "Ranks languages with at least 50 canonical books by average rating",
        "type": "bar",
        "x": "Language code",
        "y": "Average rating",
        "filter": None,
        "filename": "M9_language_rating_summary.png"
    },
    {
        "csv": "M11_duplicate_share.csv",
        "title": "Duplicate Share of Catalog",
        "caption": "Pie chart showing the proportion of canonical vs duplicate rows",
        "type": "pie",
        "x": "Duplicate status",
        "y": "Share (%)",
        "filter": None,
        "filename": "M11_duplicate_share.png"
    }
]

def plot_barh(df, x, y, title, caption, out_path):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=x, y=y, data=df, orient="h")
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"Saved: {out_path}\nCaption: {caption}")

def plot_bar(df, x, y, title, caption, out_path):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=x, y=y, data=df)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"Saved: {out_path}\nCaption: {caption}")

def plot_box(df, x, y, title, caption, out_path):
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=x, y=y, data=df)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"Saved: {out_path}\nCaption: {caption}")

def plot_line(df, x, y, title, caption, out_path):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=x, y=y, data=df)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"Saved: {out_path}\nCaption: {caption}")

def plot_pie(df, x, y, title, caption, out_path):
    plt.figure(figsize=(7, 7))
    plt.pie(df[y], labels=df[x], autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"Saved: {out_path}\nCaption: {caption}")

def main(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for chart in CHARTS:
        csv_path = os.path.join(input_dir, chart["csv"])
        if not os.path.exists(csv_path):
            print(f"Missing CSV: {csv_path}")
            continue
        df = pd.read_csv(csv_path)
        if chart["filter"]:
            df = chart["filter"](df)
        out_path = os.path.join(output_dir, chart["filename"])
        if chart["type"] == "barh":
            plot_barh(df, chart["x"], chart["y"], chart["title"], chart["caption"], out_path)
        elif chart["type"] == "bar":
            plot_bar(df, chart["x"], chart["y"], chart["title"], chart["caption"], out_path)
        elif chart["type"] == "box":
            plot_box(df, chart["x"], chart["y"], chart["title"], chart["caption"], out_path)
        elif chart["type"] == "line":
            plot_line(df, chart["x"], chart["y"], chart["title"], chart["caption"], out_path)
        elif chart["type"] == "pie":
            plot_pie(df, chart["x"], chart["y"], chart["title"], chart["caption"], out_path)
        else:
            print(f"Unknown chart type: {chart['type']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 04 Portfolio Visualization Script")
    parser.add_argument("--input-dir", type=str, default="outputs/phase04_core_metrics", help="Directory with metric CSVs")
    parser.add_argument("--output-dir", type=str, default="outputs/phase04_visualizations", help="Directory to save figures")
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)
