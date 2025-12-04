## Task 02 – Build and Refine Charts in Python

### Objective

Implement the planned visualizations using Python plotting libraries and refine them so that they are **clear, readable, and portfolio-ready**.

### Inputs

- Cleaned dataset `df_clean`.
- Summary tables and metric functions from Step 02.
- Visualization plan from Task 01.

### Outputs / Deliverables

- 5–8 completed plots in your main analysis analysis script.
- Well-formatted figures with titles, axis labels, legends, and annotations.
- (Optional) Saved image files (PNG/SVG) for reuse in documentation.

### Suggested Steps

1. **Set up plotting environment**

   - Import `matplotlib.pyplot` and `seaborn` (or your preferred library).
   - Set a consistent style (e.g., `sns.set_theme(style="whitegrid")`).

2. **Implement charts one by one**

   - For each chart in your plan:
     - Select the correct DataFrame (e.g., `df_top_authors`).
     - Write the plotting code using bar/line/scatter/etc.
     - Start with a simple version and refine.

3. **Apply good visualization practices**

   - Add descriptive titles that mention the question being answered.
   - Label axes clearly and use readable units.
   - Rotate x-axis labels if needed for readability.
   - Add legends only when necessary and keep them concise.
   - Consider adding annotations for key points (e.g., top book/author).

4. **Iterate on design**

   - Adjust figure sizes for clarity (e.g., `plt.figure(figsize=(10, 6))`).
   - Choose color palettes that are readable and colorblind-friendly.
   - Avoid clutter: remove unnecessary gridlines or chart elements.

5. **Save key figures**

   - Create a `figures/` folder in the project root if it does not exist.
   - Save the most important charts as image files, e.g.:
     - `plt.savefig("figures/top_authors_by_rating.png", bbox_inches="tight", dpi=150)`.

6. **Add brief captions**
   - Under each plot in the analysis script, add a short markdown caption explaining what the reader should notice.

### Checklist

- [ ] Plotting libraries imported and global style set.
- [ ] Each planned chart implemented in code.
- [ ] Titles, labels, and legends added.
- [ ] Figures visually checked and refined.
- [ ] Key figures saved under `figures/`.
- [ ] Captions added for each chart.
