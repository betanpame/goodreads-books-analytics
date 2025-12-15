# Phase 04 · Step 04 · Task 02 – Portfolio Case Study Structure

## 1. Case Study Outline

**Introduction & Context**

- Project goals and dataset overview
- Motivation for business questions and metrics
- Dockerized, reproducible workflow

**Dataset Description**

- Source: Goodreads books dataset (11,127 records)
- Cleaning and deduplication process
- Canonical mapping and engagement caps

**Problem / Business Questions**

- Six core business questions (see metrics catalog)
- Mapping to metrics and visualizations

**Methodology (EDA, Cleaning, Metrics)**

- EDA findings from Phase 03
- Cleaning pipeline (Step 01)
- Metrics catalog and computation (Step 02)
- Visualization plan and implementation (Step 03)

**Key Insights & Visualizations**

- Eight must-have charts (see outputs/phase04_visualizations/)
- Captions and findings for each chart
- Reference to metric CSVs and code

**Limitations & Next Steps**

- Stretch metrics and future analysis
- Outlier detection and deeper dives
- SQL validation in Phase 05
- Portfolio expansion ideas

## 2. Mapping Sections to Project Assets

| Section                | Project Asset / Output                                                                                          |
| ---------------------- | --------------------------------------------------------------------------------------------------------------- |
| Introduction           | README.md, phase-04-step-04-task-01-notes.md                                                                    |
| Dataset Description    | data/derived/books_clean.csv, cleaning notes                                                                    |
| Business Questions     | outputs/phase04_metrics_catalog.md, step-02 notes                                                               |
| Methodology            | src/pipelines/run_cleaning.py, src/analyses/portfolio/p03_core_metrics_suite.py, plot_phase04_visualizations.py |
| Key Insights           | outputs/phase04_visualizations/\*.png, step-03 notes                                                            |
| Limitations/Next Steps | step-04-task-01-notes.md, FAQ, glossary                                                                         |

## 3. Next Steps Ideas

- Add SQL-based validation and comparison in Phase 05
- Develop interactive dashboards for portfolio presentation
- Expand analysis to include publisher and author engagement metrics
- Document troubleshooting and reproducibility tips in FAQ

---

This outline is designed for portfolio reviewers and beginners. Each section is mapped to concrete project assets, ensuring transparency and ease of navigation for anyone following or evaluating the project.
