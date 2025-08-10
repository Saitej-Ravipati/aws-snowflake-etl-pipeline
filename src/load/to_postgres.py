import pandas as pd
import psycopg
from src.config.settings import settings
from src.utils.logging import get_logger

logger = get_logger("to_postgres")


def create_schema_and_tables(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS taxi;")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS taxi.trips_staging (
                vendor_id TEXT,
                tpep_pickup_datetime TIMESTAMP,
                tpep_dropoff_datetime TIMESTAMP,
                passenger_count INT,
                trip_distance FLOAT,
                rate_code_id INT,
                store_and_fwd_flag BOOLEAN,
                pu_location_id INT,
                do_location_id INT,
                payment_type TEXT,
                fare_amount FLOAT,
                extra FLOAT,
                mta_tax FLOAT,
                tip_amount FLOAT,
                tolls_amount FLOAT,
                improvement_surcharge FLOAT,
                total_amount FLOAT,
                congestion_surcharge FLOAT,
                trip_duration_minutes FLOAT
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS taxi.trips (
                vendor_id TEXT,
                tpep_pickup_datetime TIMESTAMP,
                tpep_dropoff_datetime TIMESTAMP,
                passenger_count INT,
                trip_distance FLOAT,
                rate_code_id INT,
                store_and_fwd_flag BOOLEAN,
                pu_location_id INT,
                do_location_id INT,
                payment_type TEXT,
                fare_amount FLOAT,
                extra FLOAT,
                mta_tax FLOAT,
                tip_amount FLOAT,
                tolls_amount FLOAT,
                improvement_surcharge FLOAT,
                total_amount FLOAT,
                congestion_surcharge FLOAT,
                trip_duration_minutes FLOAT,
                PRIMARY KEY (tpep_pickup_datetime, tpep_dropoff_datetime, pu_location_id, do_location_id, total_amount)
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS taxi.metrics_daily (
                pickup_date DATE PRIMARY KEY,
                trips INT,
                avg_duration FLOAT,
                avg_distance FLOAT,
                total_revenue FLOAT,
                tip_rate FLOAT
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS taxi.metrics_hourly (
                pickup_date DATE,
                pickup_hour INT,
                trips INT,
                avg_duration FLOAT,
                avg_distance FLOAT,
                total_revenue FLOAT,
                tip_rate FLOAT,
                PRIMARY KEY (pickup_date, pickup_hour)
            );
            """
        )
    conn.commit()
    logger.info("Schema and tables created")


def load_staging(df: pd.DataFrame, conn):
    logger.info("Loading data to staging table")
    with conn.cursor() as cur:
        with cur.copy(
            "COPY taxi.trips_staging FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
        ) as copy:
            df.to_csv(copy, index=False)
    conn.commit()
    logger.info("Loaded to staging")


def upsert_to_final(conn):
    logger.info("Upserting from staging to final table")
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO taxi.trips
            SELECT * FROM taxi.trips_staging
            ON CONFLICT (tpep_pickup_datetime, tpep_dropoff_datetime, pu_location_id, do_location_id, total_amount)
            DO UPDATE SET
                passenger_count = EXCLUDED.passenger_count,
                trip_distance = EXCLUDED.trip_distance,
                payment_type = EXCLUDED.payment_type,
                fare_amount = EXCLUDED.fare_amount,
                tip_amount = EXCLUDED.tip_amount,
                total_amount = EXCLUDED.total_amount,
                trip_duration_minutes = EXCLUDED.trip_duration_minutes;
            """
        )
        cur.execute("TRUNCATE taxi.trips_staging;")
    conn.commit()
    logger.info("Upsert complete")


def load_metrics(daily: pd.DataFrame, hourly: pd.DataFrame, conn):
    logger.info("Loading metrics tables")
    with conn.cursor() as cur:
        for _, row in daily.iterrows():
            cur.execute(
                """
                INSERT INTO taxi.metrics_daily (pickup_date, trips, avg_duration, avg_distance, total_revenue, tip_rate)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (pickup_date) DO UPDATE SET
                    trips = EXCLUDED.trips,
                    avg_duration = EXCLUDED.avg_duration,
                    avg_distance = EXCLUDED.avg_distance,
                    total_revenue = EXCLUDED.total_revenue,
                    tip_rate = EXCLUDED.tip_rate;
                """,
                tuple(row),
            )
        for _, row in hourly.iterrows():
            cur.execute(
                """
                INSERT INTO taxi.metrics_hourly (pickup_date, pickup_hour, trips, avg_duration, avg_distance, total_revenue, tip_rate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (pickup_date, pickup_hour) DO UPDATE SET
                    trips = EXCLUDED.trips,
                    avg_duration = EXCLUDED.avg_duration,
                    avg_distance = EXCLUDED.avg_distance,
                    total_revenue = EXCLUDED.total_revenue,
                    tip_rate = EXCLUDED.tip_rate;
                """,
                tuple(row),
            )
    conn.commit()
    logger.info("Metrics loaded")


def get_connection():
    return psycopg.connect(
        host=settings.PG_HOST,
        port=settings.PG_PORT,
        dbname=settings.PG_DB,
        user=settings.PG_USER,
        password=settings.PG_PASSWORD,
        autocommit=False,
    )
