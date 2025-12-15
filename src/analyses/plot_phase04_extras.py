"""
Phase 04 · Step 03 · Optional/Stretch Visualizations

This script generates additional charts for deeper portfolio analysis, including author engagement index, publisher-level engagement, and annotated scatter plots for outlier detection. All figures are saved in outputs/phase04_visualizations/ with clear captions for documentation.

Usage (from repo root):
    docker compose --env-file .env.example -f docker-compose.python.yml run --no-deps --rm app python -m src.analyses.plot_phase04_extras --input-dir outputs/phase04_core_metrics --output-dir outputs/phase04_visualizations
"""
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

EXTRA_CHARTS = [
    {
        "csv": "M2_author_engagement_index.csv",
        "title": "Author Engagement Index",
        "caption": "Ranks authors by combined z-score of ratings_count_capped and text_reviews_count_capped.",
        "type": "barh",
        "x": "engagement_index",
        "y": "author_name",
        "filter": lambda df: df.sort_values("engagement_index", ascending=False).head(15),
        "filename": "M2_author_engagement_index.png"
    },
    {
        "csv": "M10_publisher_engagement.csv",
        "title": "Publisher-Level Engagement",
        "caption": "Shows median ratings_count_capped for publishers with ≥25 canonical titles.",
        "type": "barh",
        "x": "median_ratings_count_capped",
        "y": "publisher",
        "filter": lambda df: df.sort_values("median_ratings_count_capped", ascending=False).head(15),
        "filename": "M10_publisher_engagement.png"
    },
    {
        "csv": "M6_page_length_engagement_delta.csv",
        "title": "Page Length Engagement Delta",
        "caption": "Median ratings_count_capped and text_reviews_count_capped per page_length_bucket.",
        "type": "box",
        "x": "page_length_bucket",
        "y": "engagement_delta",
        "filter": None,
        "filename": "M6_page_length_engagement_delta.png"
    },
    {
        "csv": "M12_engagement_uplift_canonical.csv",
        "title": "Engagement Uplift for Canonical Editions",
        "caption": "Compares median ratings_count between canonical parents and duplicate children.",
        "type": "bar",
        "x": "edition_type",
        "y": "median_ratings_count",
        "filter": None,
        "filename": "M12_engagement_uplift_canonical.png"
    },
    {
        "csv": "M13_publisher_language_rankings.csv",
        "title": "Publisher Rankings by Language",
        "caption": "Ranks publishers by average rating and 75th-percentile engagement per language.",
        "type": "bar",
        "x": "publisher",
        "y": "average_rating",
        "filter": lambda df: df.sort_values("average_rating", ascending=False).head(15),
        "filename": "M13_publisher_language_rankings.png"
    },
    {
        "csv": "M14_publication_year_rolling_stats.csv",
        "title": "Publication Year Rolling Stats",
        "caption": "Shows rolling 3-year averages and medians for ratings and engagement.",
        "type": "line",
        "x": "publication_year",
        "y": "rolling_average_rating",
        "filter": None,
        "filename": "M14_publication_year_rolling_stats.png"
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

def main(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for chart in EXTRA_CHARTS:
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
        else:
            print(f"Unknown chart type: {chart['type']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 04 Optional Visualizations Script")
    parser.add_argument("--input-dir", type=str, default="outputs/phase04_core_metrics", help="Directory with metric CSVs")
    parser.add_argument("--output-dir", type=str, default="outputs/phase04_visualizations", help="Directory to save figures")
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)
