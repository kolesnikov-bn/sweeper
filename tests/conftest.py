import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture(scope="session")
def fixtures_path() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory(prefix="temp_downloads") as tmp:
        yield Path(tmp)
