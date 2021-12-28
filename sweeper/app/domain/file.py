import uuid
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from sweeper.app.common.types import MIME, UndefinedMimeType
from sweeper.app.common.utils.mime_typer import MimeTyper
from sweeper.infrastructure.system_logger import logger


class File(BaseModel):
    path: Path
    mime_typer: MimeTyper = MimeTyper()

    class Config:
        arbitrary_types_allowed = True

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def extension(self) -> str:
        return self.path.suffix.lower()

    @property
    def mime_type(self) -> MIME:
        if self.path.is_dir():
            return UndefinedMimeType

        return self.mime_typer.from_file(self.path)

    def rename(self, new_stem: Optional[str] = None) -> str:
        if new_stem is None:
            new_stem = uuid.uuid4().hex

        new_name = Path(f"{new_stem}{self.extension}")

        logger.info(f"Target file exists {self.path=} rename to {new_name=}")
        new_path = self.path.with_stem(new_stem)
        self.path = self.path.rename(new_path)

        return self.path.name

    def move_to(self, destination_file_path: Path) -> None:
        """
        Перемещение файла в каталог конкретного продукта
        Replace: если файл уже есть в целевой директории, то он его заменяет
        """
        logger.info(f"Move file {self.path=} to {destination_file_path=}")
        self.path.replace(destination_file_path)
        logger.info(f"New path {destination_file_path}")
