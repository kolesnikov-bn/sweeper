import shutil
from pathlib import Path

from sweeper.infrastructure.system_logger import logger


def copy_file(source_file_path: Path, destination_file_path: Path) -> bool:
    status = False

    try:
        shutil.copyfile(source_file_path, destination_file_path)
    except (FileNotFoundError, IsADirectoryError) as ex:
        logger.error(f"{source_file_path=} file not found", ex)
    else:
        status = True

    return status
