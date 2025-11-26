## Task 01 – Add Unit Tests for Cleaning Logic

### Objective

Ensure your cleaning function behaves as expected by adding **unit tests**.

### Outputs

- A `tests/` folder with a file such as `test_cleaning.py` containing tests for `clean_books`.

### Steps

1. **Set up testing framework**

   - Decide on `pytest` or `unittest` (pytest recommended for simplicity).
   - Ensure the library is listed in your dependencies (e.g., `requirements-dev.txt`).

2. **Create `tests/test_cleaning.py`**

   - Import `pandas` and `clean_books` from `src.cleaning`.

3. **Write small test DataFrames**

   - Create small inline DataFrames that simulate edge cases:
     - Invalid `average_rating` values.
     - Zero or negative `num_pages`.
     - Missing values in critical columns.

4. **Write assertions**

   - Check that after `clean_books`:
     - Ratings are within [0, 5].
     - `num_pages` is > 0.
     - Rows with invalid data are dropped or handled as designed.

5. **Run tests**
   - Run `pytest` (or `python -m pytest`) and ensure tests pass.
   - Fix any issues discovered.

### Checklist

- [ ] Testing framework chosen and installed.
- [ ] `tests/test_cleaning.py` created.
- [ ] Test DataFrames cover common edge cases.
- [ ] Assertions confirm cleaning behavior.
- [ ] Tests run successfully.
