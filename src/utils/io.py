import pathlib


def get_data_path(rel_path: str) -> pathlib.Path:
    return pathlib.Path(__file__).parent.parent.parent / "data" / rel_path


def ensure_dir(path: pathlib.Path):
    path.parent.mkdir(parents=True, exist_ok=True)
