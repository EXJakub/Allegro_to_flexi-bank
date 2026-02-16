# Allegro → Flexi movement connector

This repository contains a lightweight Python connector that synchronizes **all seller account movements** from Allegro to Flexi.

## What it does

- Pulls account balance operations from Allegro (`/billing/balance` endpoint)
- Keeps an incremental checkpoint (`occurredAt`, `id`) so movements are not duplicated
- Maps Allegro movement details into a Flexi movement payload
- Pushes each movement to Flexi via HTTP API
- Stores processed movement IDs in a local SQLite DB for idempotency

## Project structure

- `src/connector/config.py` – environment-driven config
- `src/connector/state.py` – SQLite state + deduplication
- `src/connector/allegro_client.py` – Allegro API access
- `src/connector/flexi_client.py` – Flexi API access
- `src/connector/mapping.py` – movement mapping logic
- `src/connector/sync_service.py` – orchestrates synchronization
- `src/connector/main.py` – CLI entrypoint

## Configuration

Use environment variables:

| Variable | Required | Description |
| --- | --- | --- |
| `ALLEGRO_BASE_URL` | no | default `https://api.allegro.pl` |
| `ALLEGRO_ACCESS_TOKEN` | yes | OAuth access token for Allegro |
| `ALLEGRO_ACCOUNT_ID` | no | Optional seller account identifier passed to Allegro |
| `FLEXI_BASE_URL` | yes | Flexi API base URL |
| `FLEXI_API_KEY` | yes | API key for Flexi |
| `FLEXI_MOVEMENTS_PATH` | no | default `/api/movements` |
| `SQLITE_PATH` | no | default `./connector_state.db` |
| `SYNC_BATCH_SIZE` | no | default `100` |
| `SYNC_LOOKBACK_HOURS` | no | default `24` |

## Run

```bash
python -m src.connector.main --once
```

Continuous mode:

```bash
python -m src.connector.main --interval-seconds 60
```

## Notes

- This connector is intentionally generic because Flexi API schemas vary by deployment.
- Update `MovementMapper.to_flexi_payload` to match your exact Flexi payload contract.
