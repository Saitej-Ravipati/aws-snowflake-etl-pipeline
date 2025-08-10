import great_expectations as ge
from src.utils.logging import get_logger

logger = get_logger("validate")


def validate_taxi_data(df):
    logger.info("Running Great Expectations suite")
    ge_df = ge.from_pandas(df)
    results = ge_df.expect_column_values_to_not_be_null("tpep_pickup_datetime")
    assert results.success, "Nulls in tpep_pickup_datetime"
    results = ge_df.expect_column_values_to_not_be_null("fare_amount")
    assert results.success, "Nulls in fare_amount"
    results = ge_df.expect_column_values_to_be_between("passenger_count", 0, 8)
    assert results.success, "passenger_count out of range"
    results = ge_df.expect_column_values_to_be_between("trip_distance", 0, 200)
    assert results.success, "trip_distance out of range"
    results = ge_df.expect_column_values_to_be_between("total_amount", 0, 1000)
    assert results.success, "total_amount out of range"
    results = ge_df.expect_column_values_to_match_regex(
        "payment_type", "^(Credit card|Cash|No charge|Dispute|Unknown|Voided trip)$"
    )
    assert results.success, "Invalid payment_type"
    logger.info("Data quality checks passed")
    return True
