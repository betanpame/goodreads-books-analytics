## Task 03 – Build End-to-End Pipeline Script

### Objective

Create a script that runs the **full pipeline** from raw CSV to cleaned data and (optionally) into PostgreSQL with a single command.

### Outputs

- A script such as `src/run_full_pipeline.py` that orchestrates loading, cleaning, and saving.

### Steps

1. **Decide pipeline stages**

   - Stages might include:
     - Load raw CSV into pandas.
     - Clean data using `clean_books`.
     - Save cleaned data to `data/derived/books_clean.csv`.
     - (Optional) Write cleaned data to a `books_clean` table in PostgreSQL.

2. **Implement script structure**

   - In `src/run_full_pipeline.py`, implement a `main()` function that:
     - Reads configuration (paths, DB connection).
     - Calls `load_books_to_postgres` or similar functions, or directly uses `clean_books` and database writes.

3. **Add CLI options**

   - Use `argparse` to control behavior:
     - Flags such as `--skip-db` or `--skip-file`.
     - Optional arguments for input/output paths.

4. **Integrate logging**

   - Print or log each stage:
     - "Loading raw CSV..."
     - "Cleaning data..."
     - "Writing cleaned data to ...".

5. **Test full run**
   - Execute the pipeline on your machine.
   - Confirm that outputs (clean file and/or tables) are created as expected.

### Checklist

- [ ] `src/run_full_pipeline.py` created.
- [ ] Pipeline stages implemented (load → clean → save).
- [ ] CLI options added for flexibility.
- [ ] Logging messages included.
- [ ] Full pipeline tested end-to-end.
