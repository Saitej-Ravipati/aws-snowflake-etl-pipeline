# Runbook

## Operations

- **Start Postgres:** `make up`
- **Run pipeline (sample):** `make run`
- **Run pipeline (full):** Set `USE_SAMPLE_DATA=false` in `.env`, then `make run`
- **Run Airflow:** See [airflow/README.md](../airflow/README.md)
- **Run tests:** `make test`
- **Lint/format:** `make lint` / `make format`

## Troubleshooting

- **Postgres connection errors:** Ensure Docker is running and port 5432 is free.
- **Data quality failures:** See logs for failed Great Expectations checks.
- **Import errors:** Activate venv (`source .venv/bin/activate`) and check `PYTHONPATH`.
- **Airflow import errors:** Ensure `src/` is in `PYTHONPATH` for DAGs.

## SLAs

- **Pipeline SLA:** 30 minutes per daily batch (configurable in Airflow).
- **Alerting:** Email on failure (see `.env` and Airflow config).
