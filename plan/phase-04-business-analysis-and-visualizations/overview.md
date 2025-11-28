# Phase 04 – Business Analysis and Visualizations (Python)

## Goal

Use cleaned data and insights from EDA to answer the main **business questions** of the project, producing clear visualizations and narratives using Python (pandas + plotting libraries).

In this phase you turn EDA results into **business analysis**:

- You decide which metrics matter most (for example: average rating per author, number of ratings per publisher).
- You build charts that a non-technical person can understand at a glance.

## Inputs

- Phase 03 completed:
  - EDA notebook with key findings.
  - Documented cleaning rules.
- A cleaned or prepared DataFrame (either as a separate dataset or transformed within a notebook).

## Outputs / Deliverables

1. A main **analysis notebook** (e.g., `02_analysis_and_visualizations.ipynb`) that:
   - Applies cleaning steps decided in Phase 03.
   - Computes key metrics (e.g., top authors/publishers, rating distributions, trends over time).
   - Contains 5–8 clear, well-labeled charts answering the main business questions.
2. A set of **intermediate tables or DataFrames** that could be reused in SQL or future dashboards.
3. A short **written summary** (within the notebook or a markdown file) explaining major insights.

## Steps in This Phase

Detailed steps are under `steps/`:

1. **Step 1 – Implement Data Cleaning in Python**  
   Folder: `steps/step-01-implement-cleaning-in-python/`

2. **Step 2 – Define and Compute Key Business Metrics**  
   Folder: `steps/step-02-define-and-compute-metrics/`

3. **Step 3 – Build Insightful Visualizations**  
   Folder: `steps/step-03-build-visualizations/`

4. **Step 4 – Summarize Insights and Draft Storyline**  
   Folder: `steps/step-04-summarize-insights/`

## Tips

- Keep each chart focused on **one main message**.
- Use titles, axis labels, and annotations so that someone can understand the chart without reading the code.
- Save or export key figures so they can be embedded later in the main README or a slide deck.
- When you write your explanations, imagine you are explaining the chart to a friend who has never seen the dataset before.
