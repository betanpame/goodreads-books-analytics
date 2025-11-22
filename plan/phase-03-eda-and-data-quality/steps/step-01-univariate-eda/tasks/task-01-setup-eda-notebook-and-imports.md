# Task 01 – Set Up EDA Notebook and Imports

## Objective

Create a dedicated EDA notebook and prepare it with all necessary imports and configuration.

## Instructions

1. In the `notebooks/` folder, create a new notebook named, for example, `01_eda_books.ipynb`.
2. In the first markdown cell, describe the purpose of this notebook:
   - "Univariate and bivariate EDA of the Goodreads Books dataset." 
3. In the first code cell, import commonly used libraries:
   - `pandas as pd`
   - `numpy as np`
   - `matplotlib.pyplot as plt`
   - `seaborn as sns`
4. Set basic plotting style, for example:
   - `sns.set(style="whitegrid")`
   - Configure figure size defaults if you like.
5. Load the cleaned or raw DataFrame created in Phase 02 (you can re-read `data/books.csv` or load from a saved intermediate file).

## Checklist

- [ ] I have created `01_eda_books.ipynb` in the `notebooks/` folder.
- [ ] I have added introductory markdown explaining the notebook's purpose.
- [ ] I have imported pandas, numpy, matplotlib, and seaborn.
- [ ] I have loaded the dataset into a DataFrame for analysis.

## Result

You now have a dedicated notebook prepared for EDA, with all essential libraries imported and data loaded.
