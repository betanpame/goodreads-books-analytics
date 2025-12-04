# `books_clean` Schema Snapshot (Dec 4, 2025)

Source: PostgreSQL database defined in `docker-compose.postgresql.yml` after running `python -m dotenv run -- python -m src.run_full_pipeline --load-to-postgres`.

## Columns

| # | Column | Data Type | Nullable |
|---|--------|-----------|----------|
| 1 | book_id | bigint | NO |
| 2 | title | text | YES |
| 3 | authors | text | YES |
| 4 | average_rating | double precision | YES |
| 5 | isbn | text | YES |
| 6 | isbn13 | bigint | YES |
| 7 | language_code | text | YES |
| 8 | num_pages | bigint | YES |
| 9 | ratings_count | bigint | YES |
| 10 | text_reviews_count | bigint | YES |
| 11 | publication_date | date | YES |
| 12 | publisher | text | YES |
| 13 | authors_raw | text | YES |
| 14 | authors_clean | text | YES |

## Indexes

- `books_clean_pkey`: `CREATE UNIQUE INDEX books_clean_pkey ON public.books_clean USING btree (book_id);`
- `idx_books_clean_authors`: `CREATE INDEX idx_books_clean_authors ON public.books_clean USING btree (authors);`
- `idx_books_clean_average_rating`: `CREATE INDEX idx_books_clean_average_rating ON public.books_clean USING btree (average_rating);`
- `idx_books_clean_publication_date`: `CREATE INDEX idx_books_clean_publication_date ON public.books_clean USING btree (publication_date);`

## How to refresh this snapshot

```powershell
# 1. Rebuild the table and indexes
python -m dotenv run -- python -m src.run_full_pipeline --load-to-postgres

# 2. Capture schema via SQLAlchemy helper
python - <<'PY'
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os

load_dotenv()
url = os.getenv('DATABASE_URL')
if not url:
    from src.db_config import build_database_url_from_env
    url = build_database_url_from_env()
engine = create_engine(url)
with engine.connect() as conn:
    columns = conn.execute(text("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'books_clean' ORDER BY ordinal_position")).fetchall()
    indexes = conn.execute(text("SELECT indexname, indexdef FROM pg_indexes WHERE schemaname = 'public' AND tablename = 'books_clean' ORDER BY indexname")).fetchall()

for row in columns:
    print(row)
print('---')
for row in indexes:
    print(row)
PY
```

Update this markdown file whenever the schema changes so downstream phases have an authoritative reference for migrations and analytics assumptions.
