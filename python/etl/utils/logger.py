import logging
from pathlib import Path


def get_logger():

    project_root = (
        Path(__file__).resolve().parents[3]
    )

    log_folder = project_root / "logs"

    log_folder.mkdir(
        exist_ok=True
    )

    log_file = (
        log_folder / "etl_pipeline.log"
    )

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(
        "smart_retail_etl"
    )