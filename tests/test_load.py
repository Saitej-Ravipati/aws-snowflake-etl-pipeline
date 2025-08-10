import pandas as pd
from src.load.to_postgres import (
    get_connection,
    create_schema_and_tables,
    load_staging,
    upsert_to_final,
)


def test_postgres_load(monkeypatch):
    # This is a stub; in CI, use a test DB or mock
    conn = get_connection()
    create_schema_and_tables(conn)
    df = pd.DataFrame(
        {
            "vendor_id": ["VTS"],
            "tpep_pickup_datetime": ["2024-01-01 00:00:00"],
            "tpep_dropoff_datetime": ["2024-01-01 00:10:00"],
            "passenger_count": [1],
            "trip_distance": [2.5],
            "rate_code_id": [1],
            "store_and_fwd_flag": [False],
            "pu_location_id": [142],
            "do_location_id": [236],
            "payment_type": ["Credit card"],
            "fare_amount": [10.5],
            "extra": [0.5],
            "mta_tax": [0.5],
            "tip_amount": [2.0],
            "tolls_amount": [0.0],
            "improvement_surcharge": [0.3],
            "total_amount": [13.8],
            "congestion_surcharge": [2.5],
            "trip_duration_minutes": [10.0],
        }
    )
    load_staging(df, conn)
    upsert_to_final(conn)
    conn.close()
