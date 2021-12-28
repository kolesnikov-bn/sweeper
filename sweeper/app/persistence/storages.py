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
    def template_path(self) -> Path:
        return self.settings.resources / self.storage_name

    def check_file_exists(self, source_file: File) -> bool:
        """Проверяем наличие файла в хранилище"""
        storage_file = self.storage_path / source_file.name

        return storage_file.exists()

    def make_path(self, source_file: File) -> Path:
        """Создание нового пути от storage до нового файла"""
        return self.storage_path / source_file.name


class Application(Storage):
    storage_name: str = "1-Applications"
    action: Type[Action] = NothingAction
    icon: str = "blue.rsrc"


class Archive(Storage):
    storage_name: str = "2-Archives"
    action: Type[Action] = NothingAction
    icon: str = "cyan.rsrc"


class Audio(Storage):
    storage_name: str = "3-Audios"
    action: Type[Action] = NothingAction
    icon: str = "purple.rsrc"


class Torrent(Storage):
    storage_name: str = "4-Torrents"
    action: Type[Action] = TorrentAction
    icon: str = "green.rsrc"


class Video(Storage):
    storage_name: str = "5-Videos"
    action: Type[Action] = NothingAction
    icon: str = "orange.rsrc"


class Image(Storage):
    storage_name: str = "6-Images"
    action: Type[Action] = NothingAction
    icon: str = "yellow.rsrc"


class Document(Storage):
    storage_name: str = "7-Docs"
    action: Type[Action] = NothingAction
    icon: str = "red.rsrc"


class Other(Storage):
    storage_name: str = "8-Others"
    action: Type[Action] = NothingAction
    icon: str = "grey.rsrc"
