import pandas as pd
from src.utils.logging import get_logger

logger = get_logger("clean")


def clean_taxi_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting cleaning process")
    # Type casting
    df["tpep_pickup_datetime"] = pd.to_datetime(
        df["tpep_pickup_datetime"], errors="coerce"
    )
    df["tpep_dropoff_datetime"] = pd.to_datetime(
        df["tpep_dropoff_datetime"], errors="coerce"
    )
    df["passenger_count"] = (
        pd.to_numeric(df["passenger_count"], errors="coerce").fillna(1).astype(int)
    )
    df["trip_distance"] = pd.to_numeric(df["trip_distance"], errors="coerce")
    df["fare_amount"] = pd.to_numeric(df["fare_amount"], errors="coerce")
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")
    df["tip_amount"] = pd.to_numeric(df["tip_amount"], errors="coerce")
    df["congestion_surcharge"] = pd.to_numeric(
        df.get("congestion_surcharge", 0), errors="coerce"
    ).fillna(0)
    df["store_and_fwd_flag"] = (
        df["store_and_fwd_flag"].map({"Y": True, "N": False}).fillna(False)
    )
    payment_map = {
        1: "Credit card",
        2: "Cash",
        3: "No charge",
        4: "Dispute",
        5: "Unknown",
        6: "Voided trip",
    }
    df["payment_type"] = df["payment_type"].map(payment_map).fillna("Unknown")
    # Compute trip duration
    df["trip_duration_minutes"] = (
        df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60
    # Filter impossible trips
    df = df[
        (df["trip_duration_minutes"] > 0)
        & (df["trip_distance"] >= 0)
        & (df["trip_distance"] <= 200)
        & (df["fare_amount"] >= 0)
        & (df["total_amount"] >= 0)
    ]
    logger.info(f"Cleaned data shape: {df.shape}")
    return df
