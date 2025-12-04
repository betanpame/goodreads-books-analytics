# Task 01 – Create Initial EDA Analysis Script

## Objective

Create a Python CLI workflow analysis script that will serve as the starting point for your exploratory work on the Goodreads Books dataset.

## Instructions

1. Start your Python CLI Docker container (from Phase 01) or activate the local virtual environment.
2. Create the folder `src/analyses/` if it does not already exist.
3. Add a new Python script named, for example, `01_initial_inspection_books.py`.
4. At the top of the file, include a module docstring describing:
   - The purpose of the script (initial inspection of `books.csv`).
   - A short description of the dataset (what each row represents).
5. Add a `main()` function (even if empty for now) so future steps can call the script via `python -m src.analyses.01_initial_inspection_books`.

## Checklist

- [ ] The `src/analyses/` folder exists at the project root.
- [ ] I have created `01_initial_inspection_books.py`.
- [ ] The analysis script contains an introductory module docstring or comments explaining its purpose.

## Result

You now have a dedicated analysis script to use for initial exploration with pandas.
