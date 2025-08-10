import logging
import os


def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        fmt = os.environ.get("LOG_FORMAT", "json")
        if fmt == "json":
            formatter = logging.Formatter(
                '{"level":"%(levelname)s","name":"%(name)s","message":"%(message)s","run_id":"%(process)d"}'
            )
        else:
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s %(message)s"
            )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    return logger
