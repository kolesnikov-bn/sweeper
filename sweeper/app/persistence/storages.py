from abc import ABC
from pathlib import Path
from typing import ClassVar, Type

from sweeper.app.domain.actions import Action, NothingAction, TorrentAction
from sweeper.app.domain.file import File
from sweeper.infrastructure.settings.base import Settings


class Storage(ABC):
    storage_name: ClassVar[str]
    icon: ClassVar[str]
    action: ClassVar[Type[Action]]

    def __init__(self, settings: Settings, is_overwrite: bool = False):
        self.is_overwrite = is_overwrite
        self.settings = settings

    @property
    def storage_path(self) -> Path:
        return self.settings.base_dir / self.storage_name

    @property
    def icon_path(self) -> Path:
        return self.settings.resources / self.icon

    def is_file_exists(self, source_file: File) -> bool:
        """Проверяем наличие файла в хранилище"""
        return self.make_path(source_file).exists()

    def make_path(self, source_file: File) -> Path:
        """Создание нового пути от storage до нового файла"""
        return self.storage_path / source_file.name


class Application(Storage):
    storage_name: str = "1-Applications"
    action: Type[Action] = NothingAction
    icon: str = "blue.png"


class Archive(Storage):
    storage_name: str = "2-Archives"
    action: Type[Action] = NothingAction
    icon: str = "pink.png"


class Audio(Storage):
    storage_name: str = "3-Audios"
    action: Type[Action] = NothingAction
    icon: str = "purple.png"


class Torrent(Storage):
    storage_name: str = "4-Torrents"
    action: Type[Action] = TorrentAction
    icon: str = "green.png"


class Video(Storage):
    storage_name: str = "5-Videos"
    action: Type[Action] = NothingAction
    icon: str = "orange.png"


class Image(Storage):
    storage_name: str = "6-Images"
    action: Type[Action] = NothingAction
    icon: str = "yellow.png"


class Document(Storage):
    storage_name: str = "7-Docs"
    action: Type[Action] = NothingAction
    icon: str = "red.png"


class Other(Storage):
    storage_name: str = "8-Others"
    action: Type[Action] = NothingAction
    icon: str = "black.png"
