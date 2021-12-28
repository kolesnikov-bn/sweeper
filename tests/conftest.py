import tempfile
from pathlib import Path
from typing import Generator

import pytest

from sweeper.app.domain.file import File
from tests.utils.tools import copy_file


@pytest.fixture(scope="session")
def fixtures_path() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory(prefix="temp_downloads") as tmp:
        yield Path(tmp)


@pytest.fixture
def temp_file(temp_dir, fixtures_path):
    file_name = "heatmap.png"
    source_png_file = fixtures_path / file_name
    target_png_file = temp_dir / file_name
    copy_file(source_png_file, target_png_file)

    return File(path=target_png_file)
