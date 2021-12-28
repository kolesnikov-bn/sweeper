from abc import ABC
from pathlib import Path
from typing import ClassVar, Type

from sweeper.app.domain.actions import Action, NothingAction, TorrentAction
from sweeper.app.domain.file import File
from sweeper.infrastructure.settings.base import settings
from sweeper.infrastructure.system_logger import logger


class Storage(ABC):
    storage_path: ClassVar[Path]
    action: ClassVar[Type[Action]]

    def __init__(self, source_file: File, overwrite: bool = False):
        self.source_file = source_file
        self.overwrite = overwrite

    def check_storage_exists(self) -> None:
        """Проверка существования каталога продуктов и если его нет, то создать"""
        if not self.storage_path.exists():
            self.storage_path.mkdir(mode=0o777)

    def prepare_file(self) -> Path:
        """Подготавливаем целевой файл к переносу"""
        destination = self.storage_path / self.source_file.name
        is_overwrite_file = self.overwrite is False

        if destination.exists() and is_overwrite_file:
            new_file_name = self.source_file.rename()
            destination = self.storage_path / new_file_name

        return destination

    def move(self, destination: Path) -> None:
        """
        Перемещение файла в каталог конкретного продукта
        Replace: если файл уже есть в целевой директории, то он его заменяет
        """
        logger.info(f"Move file {self.source_file=} to {destination=}")
        self.source_file = self.source_file.path.replace(destination)
        logger.info(f"New path {self.source_file}")

    def usecase(self) -> None:
        """Выполнение основных действий с файлом для конкретного продукта
        - Перемещаем файл в новый каталог
        - Выполняем действие над ним (запуск, распаковка, монтирование and etc.)
        """
        self.check_storage_exists()

        destination = self.prepare_file()
        self.move(destination)
        self.action(settings).perform_storage_usecase(destination)


class Application(Storage):
    storage_path: Path = settings.base_dir / "1-Applications"
    action: Type[Action] = NothingAction


class Archive(Storage):
    storage_path: Path = settings.base_dir / "2-Archives"
    action: Type[Action] = NothingAction


class Audio(Storage):
    storage_path: Path = settings.base_dir / "3-Audios"
    action: Type[Action] = NothingAction


class Torrent(Storage):
    storage_path: Path = settings.base_dir / "4-Torrents"
    action: Type[Action] = TorrentAction


class Video(Storage):
    storage_path: Path = settings.base_dir / "5-Videos"
    action: Type[Action] = NothingAction


class Image(Storage):
    storage_path: Path = settings.base_dir / "6-Images"
    action: Type[Action] = NothingAction


class Document(Storage):
    storage_path: Path = settings.base_dir / "7-Docs"
    action: Type[Action] = NothingAction


class Other(Storage):
    storage_path: Path = settings.base_dir / "8-Others"
    action: Type[Action] = NothingAction
