import pandas as pd
from src.utils.logging import get_logger

logger = get_logger("aggregate")


def aggregate_metrics(df: pd.DataFrame):
    logger.info("Aggregating daily and hourly metrics")
    df["pickup_date"] = df["tpep_pickup_datetime"].dt.date
    df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour

    daily = (
        df.groupby("pickup_date")
        .agg(
            trips=("vendor_id", "count"),
            avg_duration=("trip_duration_minutes", "mean"),
            avg_distance=("trip_distance", "mean"),
            total_revenue=("total_amount", "sum"),
            tip_rate=("tip_amount", lambda x: x.sum() / df["total_amount"].sum()),
        )
        .reset_index()
    )

    hourly = (
        df.groupby(["pickup_date", "pickup_hour"])
        .agg(
            trips=("vendor_id", "count"),
            avg_duration=("trip_duration_minutes", "mean"),
            avg_distance=("trip_distance", "mean"),
            total_revenue=("total_amount", "sum"),
            tip_rate=("tip_amount", lambda x: x.sum() / df["total_amount"].sum()),
        )
        .reset_index()
    )

    logger.info(f"Aggregated daily shape: {daily.shape}, hourly shape: {hourly.shape}")
    return daily, hourly
