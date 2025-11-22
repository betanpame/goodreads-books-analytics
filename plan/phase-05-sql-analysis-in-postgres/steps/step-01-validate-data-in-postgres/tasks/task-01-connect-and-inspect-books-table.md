## Task 01 – Connect to PostgreSQL and Inspect `books` Table

### Objective
Verify that you can connect to the PostgreSQL database and inspect the core `books` table using both a SQL client (psql/GUI) and, optionally, Python.

### Inputs
- PostgreSQL instance running (from previous phases or docker-compose).
- Connection details (host, port, database, user, password) from Phase 01.
- The `books` table already loaded from Phase 02.

### Outputs / Deliverables
- Successful manual connection to PostgreSQL (psql or GUI screenshot/notes).
- Basic information about the `books` table structure (columns, types, indexes).
- A short markdown note with connection commands/steps.

### Suggested Steps
1. **Start PostgreSQL container or service**  
   - If using Docker Compose, run the appropriate command (e.g., `docker compose up postgres`).  
   - Confirm the container is running (via `docker ps` or your Docker UI).

2. **Connect using a SQL client**  
   - Option A: `psql` from terminal.  
   - Option B: a GUI like DBeaver, pgAdmin, or TablePlus.  
   - Use connection parameters defined earlier.

3. **List databases and connect**  
   - From the client, list databases (e.g., `\l` in psql).  
   - Connect to your project database (e.g., `\c goodreads`).

4. **Inspect `books` table structure**  
   - List tables to confirm `books` exists (e.g., `\dt`).  
   - Describe table structure (e.g., `\d books`).  
   - Note column names and types; compare them mentally with `books.csv` columns.

5. **Run a few sample queries**  
   - `SELECT * FROM books LIMIT 5;`  
   - `SELECT COUNT(*) FROM books;`  
   - Optionally, check a few specific rows by `bookID`.

6. **(Optional) Connect from Python**  
   - In a Jupyter notebook, use `sqlalchemy` or `psycopg2` to connect.  
   - Run `pd.read_sql("SELECT * FROM books LIMIT 5", con)` to confirm Python ↔ PostgreSQL connectivity.

7. **Document connection details and notes**  
   - In your project docs (or a markdown cell), write down:  
     - How you start PostgreSQL.  
     - How you connect (CLI command, GUI connection string).  
     - Any issues encountered and how you solved them.

### Checklist
- [ ] PostgreSQL is running.  
- [ ] Connected to DB using a client.  
- [ ] Confirmed `books` table exists and inspected schema.  
- [ ] Ran sample `SELECT` queries.  
- [ ] (Optional) Verified Python connection with a small query.  
- [ ] Documented connection steps and notes.
