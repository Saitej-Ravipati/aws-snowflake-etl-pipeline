# Architecture

```mermaid
flowchart LR
  A[Source Parquet/CSV] --> B[Ingest Raw]
  B --> C[Validate (Great Expectations)]
  C --> D[Transform (Pandas/SQL)]
  D --> E[(Postgres Warehouse)]
  E --> F[Analytics Views & Metrics]
```

- **Ingest:** Download or use sample data, save to `data/raw/`
- **Validate:** Run Great Expectations suite
- **Transform:** Clean, filter, enrich, aggregate
- **Load:** Stage to Postgres, upsert to final tables
- **Aggregate:** Daily/hourly metrics
