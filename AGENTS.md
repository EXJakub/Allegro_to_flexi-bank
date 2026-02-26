# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a **pure Python CLI connector** (zero third-party dependencies) that syncs seller account movements from the Allegro API to a Flexi API, using SQLite for state/deduplication. Python 3.10+ is required (3.12.3 available on this VM).

### Running the connector

See `README.md` for full config reference. The connector requires three environment variables:
- `ALLEGRO_ACCESS_TOKEN` — OAuth token for Allegro
- `FLEXI_BASE_URL` — Flexi API base URL
- `FLEXI_API_KEY` — API key for Flexi

Run once: `python3 -m src.connector.main --once`  
Run continuously: `python3 -m src.connector.main --interval-seconds 60`

### Local testing without real API credentials

Since the connector uses only `urllib` (stdlib), you can mock both APIs with a single Python HTTP server on localhost. Point `ALLEGRO_BASE_URL` and `FLEXI_BASE_URL` to the mock server, set dummy tokens, and run `--once`. The mock needs:
- `GET /billing/balance` → return `{"balanceOperations": [...]}` with movement objects containing `id`, `occurredAt`, `type`, `value`, etc.
- `POST /api/movements` → return 201.

### Linting

No linter is configured in the repo. Use `python3 -m ruff check src/` (ruff installed in the VM) for lint checks.

### Key caveats

- There are no automated tests in the repository — no test framework, no test files.
- The SQLite database file (`connector_state.db`) is created in the working directory by default. It is gitignored.
- The connector has **no build step** — it runs directly as a Python module from the repo root.
- All imports are relative within the `src.connector` package; always run from the workspace root (`/workspace`).
