# Dataset Notes – Goodreads Books (`data/books.csv`)

These notes capture an initial, slightly deeper understanding of the Goodreads Books dataset based on inspecting the header and the first several dozen rows of `data/books.csv`.

They are written to satisfy **Phase 01 → Step 01 → Task 02 – Examine Dataset Preview** and to serve as a reference for later phases (EDA, schema design, cleaning rules).

---

## 1. Main columns and rough data types

Below is a first-pass classification of the key columns by type, based on how they appear in the CSV.

### 1.1 Numeric columns

- `bookID` – Integer identifier for each book (e.g., `1`, `2`, `4`).
- `average_rating` – Numeric rating, typically a float between 0 and 5 (e.g., `4.57`).
- `num_pages` – Integer count of pages in the book (e.g., `652`, `870`).
- `ratings_count` – Integer count of user ratings (e.g., `2095690`).
- `text_reviews_count` – Integer count of text reviews (e.g., `27591`).

These are the columns most likely to be treated as numeric in pandas and SQL (for aggregations, averages, distributions, etc.).

### 1.2 Text (string) columns

- `title` – Book title; sometimes includes series information in parentheses.
- `authors` – One or more author names, separated by `/` when there are multiple authors.
- `isbn` – 10-character book identifier; looks numeric but is safest as text because of leading zeros and the `X` suffix.
- `isbn13` – 13-character book identifier; also better treated as text.
- `language_code` – Short code for the language of the edition (e.g., `eng`, `en-US`, `fre`).
- `publisher` – Name of the publisher (e.g., `Scholastic Inc.`, `Houghton Mifflin Harcourt`).

These columns will usually be treated as strings and used for grouping, filtering, and display.

### 1.3 Date-like columns

- `publication_date` – Appears in `M/D/YYYY` or `MM/DD/YYYY` format (e.g., `9/16/2006`, `11/1/2003`). It is stored as text in the CSV but conceptually represents a **date**.

In pandas or SQL, this column will need to be **parsed** into a real date type to support time-based analysis (e.g., by year, by decade).

---

## 2. Columns most relevant for analysis

### 2.1 Book popularity

For understanding **popularity** (how many people engaged with a book), the most relevant columns are:

- `ratings_count` – Primary signal for how many users rated the book.
- `text_reviews_count` – How many users wrote a review (stronger engagement than a simple rating).
- `average_rating` – While more about satisfaction, it is also informative when combined with counts (e.g., a very high rating with very few ratings is less reliable).

Secondary signals that can help contextualize popularity:

- `num_pages` – May influence how many people are willing to read the book.
- `publication_date` – Older books have had more time to accumulate ratings; newer books may have high growth.
- `language_code` – Some languages might naturally have fewer ratings due to a smaller audience.

### 2.2 Reader satisfaction

For understanding **reader satisfaction**, the most important column is:

- `average_rating` – Direct measure of how readers rated the book.

Relevant context columns:

- `ratings_count` and `text_reviews_count` – A high `average_rating` with many ratings is a strong sign of consistent satisfaction.
- `title` and `authors` – Help interpret patterns (e.g., specific authors or series that consistently receive high ratings).
- `num_pages` – Might correlate with satisfaction (e.g., are very long books rated differently?).

### 2.3 Metadata useful for slicing the data

Additional columns that are not direct measures of popularity or satisfaction but help define **subgroups**:

- `language_code` – Analyze ratings by language.
- `publisher` – Compare publishers on average rating and popularity.
- `publication_date` – Look at trends over time (e.g., average rating by publication year).

---

## 3. Columns that are unclear or need further investigation

Based on the header and a small preview, most columns are reasonably clear. However, a few points are worth noting for later investigation:

- `language_code` – There are values like `eng`, `en-US`, `fre`. It would be useful to:

  - Check the full list of unique language codes.
  - Decide whether to group some of them together (e.g., `eng` and `en-US` both as "English").

- `isbn` and `isbn13` – While their purpose is clear (book identifiers), questions remain:

  - Are there missing values or malformed entries?
  - Do multiple rows share the same `isbn13` (different editions of essentially the same work)?

- Duplicate / multiple editions:
  - Some titles appear multiple times with slightly different authors or publishers (e.g., different editions, audio books).
  - Later we may need to decide how to treat these: as separate records or grouped by work.

At this stage, these are **notes to self**, not issues to solve immediately.

---

## 4. Initial questions and hypotheses about the data

To guide later EDA and analysis, here are some early questions and hypotheses inspired by the preview:

1. **Popularity vs rating**

   - _Question_: Are the most popular books by `ratings_count` also the highest rated by `average_rating`?
   - _Hypothesis_: Some very popular books may have slightly lower average ratings due to a wide, diverse audience.

2. **Book length and satisfaction**

   - _Question_: How does `num_pages` relate to `average_rating` and `ratings_count`?
   - _Hypothesis_: Extremely long books may receive fewer ratings but higher satisfaction from dedicated readers.

3. **Publishers and performance**

   - _Question_: Do some publishers systematically publish books with higher `average_rating` or more `ratings_count`?
   - _Hypothesis_: Large, well-known publishers might dominate in `ratings_count`, but niche publishers could have very high `average_rating` in specific genres.

4. **Language differences**
   - _Question_: Are there noticeable differences in `average_rating` or `ratings_count` across `language_code` values?
   - _Hypothesis_: English-language editions (`eng`, `en-US`) may have higher `ratings_count`, while other languages might show different rating distributions.

These questions will be refined and tested in later phases using pandas (Phase 02–04) and SQL in PostgreSQL (Phase 05).

---

## 5. How these notes will be used later

- In **Phase 02**, when designing the PostgreSQL schema, these data type assumptions will guide column definitions (e.g., numeric vs text vs date).
- In **Phase 03–04**, these hypotheses will shape EDA steps and visualizations (e.g., rating distributions, popularity vs rating plots, publisher comparisons).
- In **Phase 05**, the same columns will be used to write analytical SQL queries.

Keeping these notes here ensures that early observations and ideas are not lost and can be revisited as the project evolves.
