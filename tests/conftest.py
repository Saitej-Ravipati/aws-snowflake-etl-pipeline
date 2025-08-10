import pytest
import pandas as pd
from src.utils.io import get_data_path


@pytest.fixture
def sample_df():
    path = get_data_path("sample/yellow_tripdata_sample.csv")
    return pd.read_csv(path)
