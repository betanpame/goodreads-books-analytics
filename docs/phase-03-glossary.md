# Phase 03 – EDA & Data Quality Glossary

Beginner-friendly definitions for terms used throughout Phase 03.

## Analytical Concepts

- **EDA (Exploratory Data Analysis)** – A structured process of summarizing datasets with tables, charts, and simple statistics to understand their shape before building models or dashboards.
- **Univariate analysis** – Looking at one variable at a time (for example, a histogram of `average_rating`) to learn about its distribution, range, and outliers.
- **Bivariate analysis** – Studying two variables together (for example, `average_rating` vs `num_pages`) to uncover relationships or trends.
- **Distribution** – Describes how values are spread; common visuals include histograms, boxplots, and kernel density estimates (KDE).
- **Histogram** – A bar-style chart that groups numeric values into bins so you can see which ranges occur most often.
- **Boxplot** – A compact chart that shows the median, quartiles, and potential outliers for a numeric variable.
- **Kernel Density Estimate (KDE)** – A smoothed curve that approximates the probability density of a numeric variable. Helpful for spotting skewness.
- **Scatter plot** – A chart that places one variable on the x-axis and another on the y-axis to highlight relationships (for example, `num_pages` vs `average_rating`). Transparency (alpha) helps when many points overlap.
- **Line chart** – A visual that connects data points ordered in time (or another continuous dimension) so you can see trends, peaks, and inflection points at a glance.
- **Temporal trend analysis** – A structured review of how metrics move over time, typically using line charts or rolling windows to spot seasonality, coverage gaps, or regime shifts.
- **Pearson correlation** – A statistic between -1 and 1 that measures the strength of a linear relationship between two numeric variables. Values near 0 imply little to no linear association.
- **Log scale** – A scale where each step increases by a multiplicative factor (10×, 100×, etc.). Useful when plotting skewed metrics such as `ratings_count` so both small and large values fit on the same axis.
- **Skewness** – When one tail of the distribution is longer than the other (e.g., ratings are often left-skewed because they cluster near 4 or 5).
- **Outlier** – An unusually high or low value compared to the rest of the data. For example, a `ratings_count` in the millions may be an outlier relative to the median.
- **Median** – The 50th percentile (middle) value of a distribution. Half the observations fall above it and half below, so it resists the pull of outliers. We use it for `ratings_count` and `text_reviews_count` to summarize engagement.
- **Winsorizing / Capping** – Replacing extreme values above (or below) a threshold with the threshold itself. In Phase 03 we cap `ratings_count` at 597,244 and `text_reviews_count` at 14,812 to keep visuals readable.
- **IQR (Interquartile Range)** – The span between the 25th and 75th percentiles. Often used to flag outliers (values outside 1.5×IQR from the quartiles).
- **Hard vs soft bounds** – Hard bounds ("valid min/max") mark impossible values that should be fixed or removed immediately (e.g., `num_pages < 1`). Soft bounds flag suspicious but explainable cases (such as `num_pages > 2,000` omnibuses) so analysts can bucket or annotate them instead of dropping the data outright.
- **Rule violation log** – A structured table (here: `outlier_rule_violations.csv`) that records each rule, the number of rows it caught, and the CSV/plot evidence generated. It keeps multiple anomaly checks auditable and prevents copy/paste mistakes in documentation.
- **Cleaning rulebook** – The living document (`docs/data-cleaning-rules.md`) that consolidates every data-quality decision (issue, columns, rule, rationale, priority) so engineers and analysts implement the same fixes without re-running EDA.
- **Missing value** – A blank, `NaN`, or `None` entry. During Phase 03 we count them and decide whether to drop, fill, or investigate them.
- **Missingness rate** – The percentage of rows where a column is missing. We report it alongside raw counts (for example, `publication_year` is missing in only 0.018% of rows) to show whether the gap is material.
- **Duplicate** – Two or more rows representing the same entity (for example, identical ISBNs). Duplicates can bias counts if left unresolved.
- **Partial duplicate subset** – A duplicate definition scoped to a handful of columns (here: normalized `title`, `authors`, `publication_date`). Useful when multiple SKUs represent the same story but the rest of the row (ISBN, narrator, etc.) differs.
- **Canonical book ID** – The identifier chosen to represent a cluster of partial duplicates (we take the lowest `bookID`). Analytics should group by this value to avoid double counting audiobooks or translated editions.
- **Bucket / Bin** – A labeled numeric range used to simplify continuous values. Example: grouping `num_pages` into `[0–199, 200–399, 400–599, 600+]` to summarize how ratings shift as books get longer.
- **Category-level aggregation** – Summarizing metrics (average rating, median engagement, counts) across a categorical column such as `language_code` or `publisher`. Helps compare groups without examining every row.
- **Top-N filter** – Limiting an analysis to the most common categories (e.g., top 10 languages) so charts stay legible and insights focus on cohorts with enough data.

## Goodreads Dataset Terms

- **`average_rating`** – Goodreads’ average reader score for a book on a 1–5 scale.
- **`ratings_count`** – Number of star ratings the book has received; a proxy for popularity.
- **`text_reviews_count`** – Number of written reviews; another engagement signal.
- **`num_pages`** – Page count reported in the source CSV (note the raw column contains leading spaces: `"  num_pages"`).
- **`language_code`** – Short identifier for the primary language (`eng`, `en-US`, `spa`, etc.).
- **`publication_date`** – Original release date (string in the raw CSV). In Phase 03 we parse it into ISO `YYYY-MM-DD` for plotting over time.
- **`publication_year`** – Integer year derived from `publication_date`. Coverage is ~100% for this dataset and fuels the temporal charts produced in Phase 03 Step 02 Task 02.
- **`authors`** – Slash-delimited list of author names in the raw CSV (e.g., `"J.K. Rowling/Mary GrandPré"`). Phase 02 created the `book_authors_stage` table to normalize this field.
- **`publisher`** – Free-text publisher name. Phase 03 notes help us track inconsistencies in spelling or casing.
- **`bookid_canonical_map`** – Postgres staging table (and matching CSV under `data/derived/`) that stores duplicate → canonical `bookID` pairs. Join on `duplicate_bookID` and coalesce to `canonical_bookID` so audiobooks and translated editions roll up to a single record.
- **`books_canonical_v`** – Database view created in Phase 03 Step 03 Task 01 that exposes both the canonical ID and original `book_id`, hiding the join logic so downstream SQL and BI tools automatically consume deduplicated rows.

Keep this glossary close while documenting EDA findings. Expand it whenever you introduce a new concept so future readers (or recruiters) can follow the narrative without Googling terminology.
