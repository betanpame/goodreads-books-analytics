## Task 02 – Extract Cleaning Logic into a Reusable Module

### Objective

Move your `clean_books` logic out of analysis scripts into a **Python module** so it can be reused by scripts and tests.

### Outputs

- A `src/cleaning.py` file with a function like `clean_books(df: pd.DataFrame) -> pd.DataFrame`.

### Steps

1. **Review existing cleaning steps in analysis scripts**

   - Find the sections in your analysis scripts where you implemented cleaning (types, missing values, outliers, text normalization, etc.).

2. **Create `src/cleaning.py`**

   - Define a function signature, e.g.:
     - `def clean_books(df: pd.DataFrame) -> pd.DataFrame:`.

3. **Move cleaning logic into the function**

   - Copy the core transformations from the analysis script into the function body.
   - Keep steps in a clear order (type casting, missing values, outliers, text normalization).

4. **Add docstrings and comments**

   - At the top of the function, describe:
     - Expected input DataFrame structure (columns).
     - Main cleaning rules applied.
     - What the function returns.

5. **Update analysis scripts to use the module**

   - Replace inline cleaning code in analysis scripts with:
     - `from src.cleaning import clean_books`
     - `df_clean = clean_books(df_raw)`.

6. **Run analysis scripts to confirm behavior**
   - Ensure cleaned results are equivalent to what you had before moving the logic.

### Checklist

- [ ] `src/cleaning.py` created.
- [ ] `clean_books` function implemented with documented rules.
- [ ] Analysis Scripts import and use `clean_books`.
- [ ] Cleaned outputs validated against prior version.
