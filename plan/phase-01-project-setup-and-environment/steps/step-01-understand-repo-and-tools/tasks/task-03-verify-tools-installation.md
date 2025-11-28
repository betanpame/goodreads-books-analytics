# Task 03 – Verify Tools Installation

## Objective

Confirm that you have all required tools installed before moving on to Docker and environment configuration.

## Tools to Verify

You should have the following installed:

1. **Git** – for version control.
2. **VS Code** (or another code editor) – recommended editor.
3. **Docker Desktop** – for running containers.
4. **Python 3.x** – even though you will use Docker, having a local Python installation is useful.
5. **PostgreSQL in Docker** – a container image that you will use for SQL analysis.

## Instructions

1. Open a terminal (PowerShell, Command Prompt, or integrated terminal in VS Code).
2. Run commands to check versions, for example:
   - `git --version`
   - `docker --version`
   - `python --version` (optional but recommended)
3. If any of these commands fail or show an error, make a note in `docs/repo-notes.md` and look up how to install or fix that tool on your operating system (for example, "install Git on Windows" or "install Docker Desktop on Windows"). Do not worry if it takes time to fix this; it is normal.
4. Open Docker Desktop and confirm it is running without errors.
5. Verify that your PostgreSQL Docker container can start successfully (you can do this now or in a later phase, depending on your setup).

## Checklist

- [ ] Git is installed and accessible from the terminal.
- [ ] Docker Desktop is installed and running.
- [ ] Python 3.x is installed (optional but recommended).
- [ ] I know how to start and stop my PostgreSQL Docker container.
- [ ] I have noted any installation or configuration issues in `docs/repo-notes.md`.

## Result

You have confirmed that your basic toolchain is ready. If anything is missing or broken, fix it now before continuing.
