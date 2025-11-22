# Task 02 – Detect Outliers and Inconsistencies

## Objective

Identify suspicious or extreme values that may need special treatment.

## Instructions

1. Use visualizations (boxplots, histograms) and simple rules to detect outliers for numeric columns like:
   - `average_rating`
   - `num_pages`
   - `ratings_count`
   - `text_reviews_count`
2. Look for inconsistent or impossible values, such as:
   - `num_pages` very close to 0 or extremely high.
   - `average_rating` outside expected range (e.g., < 0 or > 5 if such cases exist).
3. For `publication_date` / `publication_year`:
   - Check for implausible dates (e.g., far in the future or very old years).
4. For categorical fields:
   - Look for obviously broken values (e.g., strange language codes).
5. Document examples of outliers and inconsistencies in markdown, including row samples.

## Checklist

- [ ] I have created visualizations suitable for spotting numeric outliers.
- [ ] I have identified at least a few concrete examples of outliers or inconsistencies.
- [ ] I have documented these findings with row samples.

## Result

You know which values might distort analysis if not handled, informing the cleaning rules you will define next.
