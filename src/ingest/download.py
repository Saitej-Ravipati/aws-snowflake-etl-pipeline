import requests
import pathlib
import shutil
from src.utils.logging import get_logger
from src.config.settings import settings

logger = get_logger("download")


def download_file(
    url: str, dest_path: pathlib.Path, chunk_size: int = 1024 * 1024
) -> None:
    logger.info(f"Starting download: url={url} dest={dest_path}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(r.raw, f, length=chunk_size)
    logger.info(f"Download complete: {dest_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m src.ingest.download <destination_path>")
        exit(1)
    dest = pathlib.Path(sys.argv[1])
    download_file(settings.SOURCE_URL, dest)
