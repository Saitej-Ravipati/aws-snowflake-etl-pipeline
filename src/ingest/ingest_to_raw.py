import pandas as pd
from src.config.settings import settings
from src.utils.io import ensure_dir, get_data_path
from src.utils.logging import get_logger

logger = get_logger("ingest_to_raw")


def ingest_to_raw():
    if settings.USE_SAMPLE_DATA:
        src = get_data_path("sample/yellow_tripdata_sample.csv")
        logger.info(f"Using sample data: {src}")
        df = pd.read_csv(src)
    else:
        src = get_data_path("raw/yellow_tripdata.parquet")
        logger.info(f"Using external data: {src}")
        df = pd.read_parquet(src)
    raw_path = get_data_path("raw/yellow_tripdata.parquet")
    ensure_dir(raw_path.parent)
    if not settings.USE_SAMPLE_DATA:
        df.to_parquet(raw_path, index=False)
    logger.info(f"Ingested data shape: {df.shape}")
    return raw_path, df.shape[0]


if __name__ == "__main__":
    ingest_to_raw()
