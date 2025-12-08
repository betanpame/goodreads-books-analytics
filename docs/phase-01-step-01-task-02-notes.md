# Phase 01 – Step 01 – Task 02 Notes

This document records, in a teaching style, how **Task 02 – Examine Dataset Preview** was completed for the `goodreads-books-analytics` project. You can use it as a template for examining datasets in future analytics projects.

Task reference: `plan/phase-01-project-setup-and-environment/steps/step-01-understand-repo-and-tools/tasks/task-02-examine-dataset-preview.md`.

---

## 1. Goal of Task 02

The goal of Task 02 is to get a **slightly deeper understanding** of the Goodreads Books dataset **before** setting up the full environment.

Concretely, the task asks you to:

1. Open `data/books.csv` and view the column names.
2. Identify key columns (e.g., `bookID`, `title`, `authors`, `average_rating`, `num_pages`, `ratings_count`, `text_reviews_count`, `publication_date`, `publisher`).
3. In `docs/dataset-notes.md`, record:
   - Rough data types (numeric / text / date) for the main columns.
   - Which columns are most relevant for **book popularity** and **reader satisfaction**.
   - Any columns you do not fully understand yet.
   - 2–3 questions or hypotheses about the data.

The output is a richer `docs/dataset-notes.md` plus your own understanding of what the dataset can support.

---

## 2. Opening and inspecting `data/books.csv`

### Command block (copy/paste)

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
code data\books.csv
# Optional spreadsheet preview
start excel "C:\\Users\\shady\\documents\\GITHUB\\goodreads-books-analytics\\data\\books.csv"
```

### Estimated runtime & success outputs

- **Runtime:** Instant for VS Code preview; ~5 seconds if Excel needs to launch.
- **Success checklist:**
  - The VS Code tab shows the CSV header and the first ~50 rows without errors.
  - Excel (if used) opens the same file with columns aligned.
  - You can read column names such as `bookID`, `title`, `authors`, `average_rating`, confirming access to the dataset.

### 2.1. How to open the file

You can inspect the CSV in **VS Code** or in a **spreadsheet tool**.

**Option A – VS Code**

1. In the Explorer, expand the `data/` folder.
2. Click on `books.csv`.
3. VS Code will open it as a text file or table.
4. Look at the **header row** (the first line) to see the column names.
5. Scroll through the first 30–50 rows to see example values for each column.

**Option B – Excel (or similar)**

In PowerShell you can run:

```powershell
start excel "C:\Users\shady\documents\GITHUB\goodreads-books-analytics\data\books.csv"
```

This opens the CSV in Excel, where each column is easier to see.

### 2.2. What the first rows show

From the preview of `books.csv`, you can see columns like:

- `bookID`
- `title`
- `authors`
- `average_rating`
- `isbn`
- `isbn13`
- `language_code`
- `num_pages`
- `ratings_count`
- `text_reviews_count`
- `publication_date`
- `publisher`

By looking at the values in the first ~50 rows, you can infer data types:

- Numbers with no quotes (e.g., `4.57`, `652`, `2095690`) are numeric.
- Text values (titles, author names, publisher names) are strings.
- Dates like `9/16/2006` look like dates but are stored as strings in the raw CSV.

This "by-eye" inspection is simple but important. It ensures you understand what each column **looks like** before you write any code.

---

## 3. Filling in `docs/dataset-notes.md`

The official task instructions say to answer three types of questions in `docs/dataset-notes.md`:

1. Which columns look numeric, which are text, and which represent dates?
2. Which columns are most relevant for **book popularity** and **reader satisfaction**?
3. Are there any columns you do not understand yet? Also, write down a few questions or hypotheses.

### 3.1. Classifying columns by rough data type

In `docs/dataset-notes.md`, the columns were grouped as follows:

- **Numeric**:
  - `bookID`
  - `average_rating`
  - `num_pages`
  - `ratings_count`
  - `text_reviews_count`
- **Text**:
  - `title`
  - `authors`
  - `isbn`
  - `isbn13`
  - `language_code`
  - `publisher`
- **Date-like**:
  - `publication_date` (stored as text in the CSV, but conceptually a date)

This is a **first-pass classification**. Later, when loading the data into pandas or PostgreSQL, you will convert `publication_date` to a proper date type.

### 3.2. Choosing columns for popularity and satisfaction

In the same file, the columns were evaluated for two main concepts:

- **Book popularity** (how many people interacted with a book):

  - Key columns: `ratings_count`, `text_reviews_count`.
  - Support columns: `average_rating` (when combined with counts), `num_pages`, `publication_date`, `language_code`.

- **Reader satisfaction** (how much people liked a book):
  - Key column: `average_rating`.
  - Support columns: `ratings_count`, `text_reviews_count`, `title`, `authors`, `num_pages`.

The idea is that popularity and satisfaction are **related but different**:

- A book can be very popular with a large `ratings_count` but only moderate `average_rating`.
- A niche book can be highly rated (`average_rating`) but have fewer ratings and reviews.

### 3.3. Columns that are unclear or require decisions later

A few items were flagged as "to think about later":

- `language_code` – Contains values like `eng`, `en-US`, `fre`. Later, you may want to:

  - Inspect all distinct codes.
  - Decide how to group them (e.g., all English variants together).

- `isbn` and `isbn13` – Clearly identifiers, but we do not yet know:

  - How often they are missing or duplicated.
  - Whether different rows with the same `isbn13` correspond to different editions.

- Multiple editions / duplicate works – Some titles appear several times with slightly different metadata. Later stages will decide:
  - Whether to treat each row as a unique edition.
  - Or whether to aggregate by work/series if needed.

At this stage, you **do not need to solve** these questions; you just note them.

---

## 4. Recording initial questions and hypotheses

To complete Task 02, you also write down 2–3 questions or hypotheses about the data. These guide future EDA.

Examples that were recorded in `docs/dataset-notes.md`:

1. **Popularity vs rating**

   - _Question_: Are the most popular books by `ratings_count` also the highest rated (`average_rating`)?
   - _Hypothesis_: Very popular books may have slightly lower average ratings because they reach a wide, diverse audience.

2. **Book length and satisfaction**

   - _Question_: How does `num_pages` relate to `average_rating` and `ratings_count`?
   - _Hypothesis_: Very long books might get fewer ratings but could be highly rated by committed readers.

3. **Publishers and performance**

   - _Question_: Do some publishers systematically publish books with higher `average_rating` or more `ratings_count`?
   - _Hypothesis_: Large publishers may dominate in `ratings_count`, while smaller or niche publishers might excel in `average_rating`.

4. **Language differences**
   - _Question_: Are there differences in `average_rating` or `ratings_count` between languages (`language_code`)?
   - _Hypothesis_: English-language editions may have many more ratings, while other languages could show different rating patterns.

These questions will be revisited in later phases (EDA and analysis).

---

## 5. Why this step matters before coding

Completing Task 02 **before** setting up the full environment has several benefits:

- You enter later phases with **clear expectations** about the data.
- You already know which columns matter for popular questions (e.g., popularity, satisfaction, publishers, languages, time trends).
- Your early questions and hypotheses will guide which plots, group-bys, and SQL queries you write later.

From a portfolio perspective, this step shows that you **think about the data first**, instead of jumping straight into coding.

---

## 6. How to reuse this approach in other projects

When you work on a new dataset, you can follow the same pattern:

1. **Open the raw file** (CSV, JSON, etc.) and scan the header and first rows.
2. **List the main columns** and guess their meanings and types.
3. **Classify columns** into numeric, text, date/time, and identifiers.
4. **Pick key columns** for your main business questions (e.g., popularity, conversion, churn).
5. **Write down questions and hypotheses** before doing full EDA.
6. Document all of this in a `dataset-notes.md` file inside `docs/`.

Repeating this pattern makes your analytics projects **more structured**, **more thoughtful**, and **easier to present** in a professional portfolio.
