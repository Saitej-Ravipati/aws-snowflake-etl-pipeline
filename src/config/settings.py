from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional


class Settings(BaseSettings):
    SOURCE_URL: str = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
    )
    USE_SAMPLE_DATA: bool = True
    WAREHOUSE: Literal["postgres", "snowflake"] = "postgres"

    # Postgres
    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_DB: str = "analytics"
    PG_USER: str = "etl"
    PG_PASSWORD: str = "etl"

    # Snowflake
    SNOWFLAKE_ACCOUNT: Optional[str] = None
    SNOWFLAKE_USER: Optional[str] = None
    SNOWFLAKE_PASSWORD: Optional[str] = None
    SNOWFLAKE_ROLE: Optional[str] = None
    SNOWFLAKE_DB: str = "ANALYTICS"
    SNOWFLAKE_SCHEMA: str = "TAXI"
    SNOWFLAKE_WAREHOUSE: str = "COMPUTE_WH"

    # Logging and behavior
    LOG_LEVEL: str = "INFO"
    CHUNK_SIZE: int = 100000
    FAIL_ON_DQ_ERRORS: bool = True

    # Airflow notifications
    ALERT_EMAIL: str = "my-alerts@example.com"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
