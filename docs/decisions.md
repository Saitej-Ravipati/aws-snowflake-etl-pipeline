# Architectural Decisions

## 1. Data Ingestion

- Support both sample CSV and full Parquet download for local dev and scale.
- Use chunked streaming for large files to avoid memory issues.

## 2. Data Quality

- Great Expectations suite for critical columns and ranges.
- Pipeline fails on critical DQ errors if `FAIL_ON_DQ_ERRORS=true`.

## 3. Warehouse Loading

- Use staging tables and upsert/merge to ensure idempotency.
- Index on natural keys for deduplication and fast lookups.

## 4. Orchestration

- Airflow DAG for production-like scheduling, retries, and alerting.
- Local runner for fast iteration and CI.

## 5. Testing & CI

- Pytest for unit/integration tests.
- GitHub Actions for lint, test, and coverage on every push/PR.

## 6. Logging

- Structured logging (JSON) with run_id and step names for traceability.
