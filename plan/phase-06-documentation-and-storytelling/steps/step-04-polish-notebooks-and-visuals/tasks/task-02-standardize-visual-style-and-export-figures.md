## Task 02 – Standardize Visual Style and Export Figures

### Objective

Ensure your visualizations have a **consistent, professional look**, and export the most important ones as standalone image files.

### Outputs

- Updated plots in notebooks with consistent styling.
- A curated set of figure files saved under `figures/`.

### Steps

1. **Choose a default plotting style**

   - For example, use `seaborn.set_theme(style="whitegrid")` at the top of analysis notebooks.
   - Stick to a small, consistent set of color palettes.

2. **Review and refine each key chart**

   - Check titles, axis labels, legends, and fonts.
   - Remove unnecessary chart junk (e.g., excessive gridlines, unreadable labels).
   - Ensure x-axis labels are readable (rotate them if needed).

3. **Align figure sizes**

   - Use consistent `figsize` where appropriate (e.g., `(10, 6)` for most charts).
   - Make sure important details are visible without zooming.

4. **Export key figures to `figures/`**

   - For each chosen chart, use `plt.savefig("figures/fig_name.png", dpi=150, bbox_inches="tight")`.
   - Use descriptive filenames like `fig_top_authors_by_rating.png`, `fig_ratings_by_year.png`.

5. **Verify exported images**
   - Open the saved images in your file explorer or VS Code to ensure they look correct.
   - Re-export if you spot issues (e.g., cut-off labels).

### Checklist

- [ ] Global plotting style set in main analysis notebooks.
- [ ] Titles, labels, and legends cleaned up for key charts.
- [ ] Figure sizes consistent and readable.
- [ ] Important charts exported to `figures/` with clear filenames.
- [ ] Exported images manually checked.
