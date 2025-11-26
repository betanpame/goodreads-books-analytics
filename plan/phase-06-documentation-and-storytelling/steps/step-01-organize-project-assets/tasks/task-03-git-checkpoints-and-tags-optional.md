## Task 03 – Create Git Checkpoints and Tags (Optional)

### Objective

Use Git to create **clear milestones** in the project history that align with major phases (setup, EDA, SQL, documentation).

### Outputs

- One or more Git tags or branches marking important points in the project.
- A short note in the docs explaining what each tag/branch represents.

### Steps

1. **Review current Git history**

   - Run `git log --oneline --graph --all` to see the commit history.
   - Identify commits that correspond roughly to the completion of phases (e.g., Phase 01, Phase 03, Phase 05).

2. **Create tags for major milestones**

   - Example tags (adapt names to your style):
     - `phase-01-env-setup`
     - `phase-03-eda-complete`
     - `phase-05-sql-analysis`
   - Use commands like:
     - `git tag phase-01-env-setup <commit-id>`
     - `git push origin phase-01-env-setup`.

3. **(Optional) Create branches for experiments**

   - If you want to try big changes (e.g., refactoring notebooks, adding dashboards), create feature branches:
     - `git checkout -b feature/refactor-notebooks`.

4. **Document tags and branches**
   - In `docs/project-structure.md` or a small `docs/git-milestones.md` file, list:
     - Each tag name.
     - What it represents (1–2 sentences).
     - Any special branches you plan to use.

### Checklist

- [ ] Key commits identified for milestones.
- [ ] Git tags created for important phases.
- [ ] (Optional) Feature branches created for experiments.
- [ ] Git milestones documented in the docs.
