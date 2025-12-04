# Task 03 – Consider Future Normalization

## Objective

Think ahead about how you might normalize the schema in the future (without implementing it now).

## Instructions

1. In a markdown file (e.g., `docs/schema-notes.md`) or in your analysis script, brainstorm how the data could be split into multiple tables, for example:
   - `books` (core book information).
   - `authors` (one row per author).
   - `book_authors` (linking table between books and authors, since a book can have multiple authors).
   - `publishers` (publisher details).
2. Note potential benefits of normalization:
   - Avoiding repeated text for authors and publishers.
   - Easier maintenance if extended with more datasets.
3. Also note reasons to stay denormalized for this beginner project:
   - Simpler queries.
   - Faster to implement.
4. Decide on a strategy for **this project** (e.g., "keep one main table now, plan normalization for future projects").

## Checklist

- [ ] I have listed potential normalized tables and their relationships.
- [ ] I understand benefits and trade-offs of normalization vs denormalization.
- [ ] I have written down a decision for this project.

## Result

You understand how the schema could evolve in more advanced projects, while keeping this project focused and manageable.
