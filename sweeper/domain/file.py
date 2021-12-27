import uuid
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from sweeper.common.types import MIME
from sweeper.common.utils.mime_typer import MimeTyper
from sweeper.infrastructure.system_logger import logger


class File(BaseModel):
    path: Path
    mime_typer: MimeTyper = MimeTyper()

    class Config:
        arbitrary_types_allowed = True

    @property
    def name(self) -> str:
        return self.path.stem

    @property
    def extension(self) -> str:
        return self.path.suffix

    @property
    def mime_type(self) -> MIME:
        return self.mime_typer.from_file(self.path)

    def rename(self, target: Optional[str] = None) -> None:
        if target is None:
            target = uuid.uuid4().hex

        new_name = Path(f"{target}{self.extension}")

        logger.info(f"Target file exists {self.path=} rename to {new_name=}")
        new_path = self.path.with_stem(target)
        self.path = self.path.rename(new_path)
