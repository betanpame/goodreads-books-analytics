# Phase 03 – EDA and Data Quality Assessment

## Goal

Perform a structured **Exploratory Data Analysis (EDA)** and evaluate the **data quality** of the Goodreads Books dataset. By the end of this phase you should have a clear understanding of distributions, relationships between key variables, and known data issues (with decisions on how to handle them).

## Inputs

- Phase 02 completed:
  - Data load into pandas working.
  - (Optional) Data available in PostgreSQL.
- At least one notebook created for initial exploration.

## Outputs / Deliverables

1. A dedicated **EDA notebook** (e.g., `01_eda_books.ipynb`) covering:
   - Univariate analysis (distributions of ratings, ratings_count, num_pages, etc.).
   - Bivariate analysis (e.g., rating vs number of pages, rating vs publication year).
   - Categorical analysis (e.g., by author, publisher, language_code).
2. A list of **data quality issues** and decisions, documented in markdown:
   - Missing values and how to handle them.
   - Outliers and extreme values.
   - Duplicates or near-duplicates.
   - Inconsistent formats (dates, language codes, author delimiters).
3. A simple **data cleaning plan** that you will apply in the next phase(s).

## Steps in This Phase

Detailed steps are under `steps/`:

1. **Step 1 – Univariate EDA (Distributions)**  
   Folder: `steps/step-01-univariate-eda/`

2. **Step 2 – Bivariate and Relationship Analysis**  
   Folder: `steps/step-02-bivariate-eda/`

3. **Step 3 – Data Quality Assessment and Cleaning Rules**  
   Folder: `steps/step-03-data-quality-and-cleaning-rules/`

## Tips

- Start simple: histograms, boxplots, and bar charts are enough at this stage.
- Always connect plots back to the **business questions**: what does this distribution say about reader behavior or book characteristics?
- Document your assumptions, even if they seem obvious. This is key for professional work and for future you.
