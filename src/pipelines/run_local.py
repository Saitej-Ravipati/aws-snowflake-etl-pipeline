import pandas as pd
from src.utils.logging import get_logger
from src.utils.timeit import timeit
from src.ingest.ingest_to_raw import ingest_to_raw
from src.transform.clean import clean_taxi_data
from src.transform.validate import validate_taxi_data
from src.transform.aggregate import aggregate_metrics
from src.load.to_postgres import (
    get_connection,
    create_schema_and_tables,
    load_staging,
    upsert_to_final,
    load_metrics,
)

logger = get_logger("run_local")


@timeit
def main():
    logger.info("Starting local pipeline run")
    raw_path, n_rows = ingest_to_raw()
    logger.info(f"Ingested {n_rows} rows from {raw_path}")
    df = pd.read_parquet(raw_path)
    validate_taxi_data(df)
    df_clean = clean_taxi_data(df)
    validate_taxi_data(df_clean)
    daily, hourly = aggregate_metrics(df_clean)
    conn = get_connection()
    create_schema_and_tables(conn)
    load_staging(df_clean, conn)
    upsert_to_final(conn)
    load_metrics(daily, hourly, conn)
    conn.close()
    logger.info("Pipeline complete")


if __name__ == "__main__":
    main()
