from src.transform.clean import clean_taxi_data
from src.transform.validate import validate_taxi_data


def test_clean_and_validate(sample_df):
    df_clean = clean_taxi_data(sample_df)
    assert not df_clean.isnull().any().any()
    assert (df_clean["trip_duration_minutes"] > 0).all()
    assert validate_taxi_data(df_clean)
