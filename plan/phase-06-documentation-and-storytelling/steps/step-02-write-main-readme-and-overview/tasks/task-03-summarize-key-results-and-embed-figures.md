## Task 03 – Summarize Key Results and Embed Figures in README

### Objective

Showcase the **most important insights and visualizations** directly in the README so visitors see value quickly.

### Outputs

- A "Key Insights" section in `README.md`.
- 2–3 embedded figures (or links) with short captions.

### Steps

1. **Select key insights**

   - From your analysis and case study, choose 5–7 insights that best represent the project.
   - Each insight should connect to a real-world question (e.g., "Which authors consistently get high ratings?").

2. **Map insights to visuals**

   - For each chosen insight, pick a supporting figure from `figures/`.
   - Ensure filenames are descriptive (e.g., `fig_top_authors_by_rating.png`).

3. **Write concise insight bullets**

   - In README, add a "Key Insights" section with bullets like:
     - "Top authors X and Y achieve consistently higher average ratings than peers, especially in books published after YEAR."
   - Avoid heavy technical language; focus on interpretation.

4. **Embed or link images**

   - Use markdown to embed 2–3 of the best figures:

   ```markdown
   ![Top authors by average rating](figures/fig_top_authors_by_rating.png)
   ```

   - Under each image, add a one-sentence caption explaining what it shows.

5. **Check rendering**
   - Preview the README in VS Code or GitHub to confirm images and formatting look good.

### Checklist

- [ ] 5–7 key insights identified.
- [ ] Insights written as clear, non-technical bullets.
- [ ] 2–3 figures chosen and embedded or linked.
- [ ] Captions added under each image.
- [ ] README previewed to confirm correct rendering.
