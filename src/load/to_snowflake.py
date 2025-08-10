from src.config.settings import settings
from src.utils.logging import get_logger

logger = get_logger("to_snowflake")

try:
    import snowflake.connector
except ImportError:
    snowflake = None


def get_snowflake_connection():
    if not all(
        [
            settings.SNOWFLAKE_ACCOUNT,
            settings.SNOWFLAKE_USER,
            settings.SNOWFLAKE_PASSWORD,
        ]
    ):
        raise ValueError("Snowflake credentials not set in .env")
    return snowflake.connector.connect(
        account=settings.SNOWFLAKE_ACCOUNT,
        user=settings.SNOWFLAKE_USER,
        password=settings.SNOWFLAKE_PASSWORD,
        role=settings.SNOWFLAKE_ROLE,
        database=settings.SNOWFLAKE_DB,
        schema=settings.SNOWFLAKE_SCHEMA,
        warehouse=settings.SNOWFLAKE_WAREHOUSE,
    )


def create_tables_and_merge_example():
    logger.info("DDL and MERGE example for Snowflake")
    ddl = """
    CREATE OR REPLACE TABLE TAXI.TRIPS (
        VENDOR_ID STRING,
        TPEP_PICKUP_DATETIME TIMESTAMP,
        TPEP_DROPOFF_DATETIME TIMESTAMP,
        PASSENGER_COUNT INT,
        TRIP_DISTANCE FLOAT,
        RATE_CODE_ID INT,
        STORE_AND_FWD_FLAG BOOLEAN,
        PU_LOCATION_ID INT,
        DO_LOCATION_ID INT,
        PAYMENT_TYPE STRING,
        FARE_AMOUNT FLOAT,
        EXTRA FLOAT,
        MTA_TAX FLOAT,
        TIP_AMOUNT FLOAT,
        TOLLS_AMOUNT FLOAT,
        IMPROVEMENT_SURCHARGE FLOAT,
        TOTAL_AMOUNT FLOAT,
        CONGESTION_SURCHARGE FLOAT,
        TRIP_DURATION_MINUTES FLOAT,
        PRIMARY KEY (TPEP_PICKUP_DATETIME, TPEP_DROPOFF_DATETIME, PU_LOCATION_ID, DO_LOCATION_ID, TOTAL_AMOUNT)
    );
    """
    merge = """
    MERGE INTO TAXI.TRIPS t
    USING TAXI.TRIPS_STAGING s
    ON t.TPEP_PICKUP_DATETIME = s.TPEP_PICKUP_DATETIME
      AND t.TPEP_DROPOFF_DATETIME = s.TPEP_DROPOFF_DATETIME
      AND t.PU_LOCATION_ID = s.PU_LOCATION_ID
      AND t.DO_LOCATION_ID = s.DO_LOCATION_ID
      AND t.TOTAL_AMOUNT = s.TOTAL_AMOUNT
    WHEN MATCHED THEN
      UPDATE SET
        PASSENGER_COUNT = s.PASSENGER_COUNT,
        TRIP_DISTANCE = s.TRIP_DISTANCE,
        PAYMENT_TYPE = s.PAYMENT_TYPE,
        FARE_AMOUNT = s.FARE_AMOUNT,
        TIP_AMOUNT = s.TIP_AMOUNT,
        TOTAL_AMOUNT = s.TOTAL_AMOUNT,
        TRIP_DURATION_MINUTES = s.TRIP_DURATION_MINUTES
    WHEN NOT MATCHED THEN
      INSERT VALUES (
        s.VENDOR_ID, s.TPEP_PICKUP_DATETIME, s.TPEP_DROPOFF_DATETIME, s.PASSENGER_COUNT,
        s.TRIP_DISTANCE, s.RATE_CODE_ID, s.STORE_AND_FWD_FLAG, s.PU_LOCATION_ID, s.DO_LOCATION_ID,
        s.PAYMENT_TYPE, s.FARE_AMOUNT, s.EXTRA, s.MTA_TAX, s.TIP_AMOUNT, s.TOLLS_AMOUNT,
        s.IMPROVEMENT_SURCHARGE, s.TOTAL_AMOUNT, s.CONGESTION_SURCHARGE, s.TRIP_DURATION_MINUTES
      );
    """
    print(ddl)
    print(merge)
    logger.info("See printed DDL and MERGE SQL for Snowflake loading.")
