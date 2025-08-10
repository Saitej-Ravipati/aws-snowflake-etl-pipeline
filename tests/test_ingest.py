from src.ingest.ingest_to_raw import ingest_to_raw


def test_ingest_to_raw_runs():
    path, n_rows = ingest_to_raw()
    assert path.exists()
    assert n_rows > 0
