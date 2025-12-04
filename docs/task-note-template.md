# Task Note Template for Phase 02 → Step 01

Use this template whenever you document a new task inside Phase 02 → Step 01. Keeping the same section order means reviewers instantly know where to find commands, outputs, and evidence.

## Standard section order

1. **Task definition and goal** – paraphrase the plan file and restate the objective in your own words.
2. **How to run this analysis script** – include the canonical three-command block:

   ```powershell
   cd C:\Users\shady\OneDrive\Documentos\GITHUB\goodreads-books-analytics
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m <module> --sample-size 1000 --verbose
   ```

   Swap `<module>` or CLI flags as needed, but keep the structure so others can copy/paste.

3. **Environment recap** – optional if nothing changed, but handy for pointing to Docker services, virtualenvs, or data paths.
4. **Findings/results** – tailor the number of sections you need (e.g., column summaries, plots, schema sketches).
5. **Expected output checkpoints** – bullet the exact log lines or summary stats that should appear when things work.
6. **Observations / insights** – capture follow-up ideas, gotchas, and next steps.
7. **Artifacts refreshed each run** – list the files (CSV, PNG, notebook HTML, etc.) that prove the script executed.
8. **Q&A / data troubleshooting** – answer 3–5 common questions (e.g., where to find a CSV, how to fix missing columns) and link to the global `docs/data-faq.md` when relevant.
9. **Checklist review** – mirror the plan file’s checklist with `[x]` ticks.
10. **Appendices (optional)** – code references, run-log transcripts, screenshots, etc.

## Writing tips

- Stick to ASCII characters unless the source data already uses accents—this avoids surprises in terminals and diff tools.
- Mention the exact CLI flags you passed (`--sample-size 1000 --verbose`) so the logs match your screenshots.
- When possible, cite concrete numbers (e.g., "Loaded shape: (rows=1000, columns=12)") in the Expected output section.
- Update the Artifacts section whenever a script writes new files so downstream teammates know what to inspect or commit.
- Use the Q&A section for issues unique to the task; push broader or recurring answers into `docs/data-faq.md` so you can link back instead of rewriting explanations.
- Close with a short reminder that the same structure should be used for future tasks.

Keeping this template close at hand should make future documentation faster while preserving the reproducibility standard we just established.
