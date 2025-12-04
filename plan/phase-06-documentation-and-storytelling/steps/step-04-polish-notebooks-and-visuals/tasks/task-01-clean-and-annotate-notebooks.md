## Task 01 – Clean and Annotate Analysis Scripts

### Objective

Polish your analysis scripts so they read like **clear, guided analyses** rather than raw scratch work.

### Outputs

- All key analysis scripts cleaned, with explanatory markdown and minimal noise.

### Steps

1. **Identify key analysis scripts**

   - Decide which analysis scripts you want to show in your portfolio (e.g., EDA, cleaning, analysis, SQL comparison).
   - Focus cleanup efforts on these first.

2. **Add structure with markdown headings**

   - For each analysis script, add headings such as:
     - Introduction / Goals.
     - Data Loading.
     - EDA.
     - Cleaning.
     - Analysis & Visualizations.
     - Conclusions.

3. **Explain code blocks**

   - Before each major code block, add 1–3 sentences explaining what you are about to do and why.
   - Avoid explaining trivial imports, but do explain data transformations and analytical steps.

4. **Remove or minimize noisy sections**

   - Delete helper snippets that are purely debugging or repeated experiments.
   - If some experiments are useful for learning, group them in a separate "Appendix" section or move them to comments at the bottom.

5. **Ensure analysis scripts run from top to bottom**

   - Run each script from a clean terminal session (e.g., `python -m src.analyses.01_eda_books`) to confirm there are no missing dependencies or ordering issues.

6. **Standardize style**
   - Use consistent naming for variables and sections across analysis scripts.
   - Make sure plots are large enough and labeled.

### Checklist

- [ ] Portfolio analysis scripts identified.
- [ ] Headings added to structure each analysis script.
- [ ] Explanatory markdown added before important code blocks.
- [ ] Debug/noise sections removed or moved to Appendix.
- [ ] Analysis Scripts run cleanly from top to bottom.
- [ ] Style and tone consistent across analysis scripts.
