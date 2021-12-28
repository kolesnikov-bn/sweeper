from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Optional, Type

from infrastructure.settings.base import Settings
from loguru import logger

from sweeper.app.common.enums import Priority
from sweeper.app.common.types import MIME
from sweeper.app.common.utils.mime_typer import MimeTyper
from sweeper.app.domain.file import File
from sweeper.app.persistence.storages import (
    Application,
    Archive,
    Audio,
    Document,
    Image,
    Other,
    Storage,
    Torrent,
    Video,
)


@dataclass
class RuleRegistry(ABC):
    _factories: list[StorageRule] = field(init=False, default_factory=list)
    _registered: set[str] = field(init=False, default_factory=set)

    def register(self, klass: Type[StorageRule]) -> Type[StorageRule]:
        """Регистрация фабрики продуктов

        :param klass: фабрика создания продукта
        """
        if not issubclass(klass, StorageRule):
            raise TypeError("Можно регистрировать только субклассы от Factory")

        if klass.__name__ in self._registered:
            raise ValueError(f"Класс `{klass.__name__}` уже зарегистрирован")

        self._factories.append(klass(MimeTyper(), Settings()))
        self._registered.add(klass.__name__)

        return klass

    def find(self, source_file_path: File) -> Optional[Storage]:
        matches = [factory for factory in self._factories if factory.match(source_file_path)]

        if not matches:
            logger.info(f"Не удается найти фабрику для элемента: `{source_file_path}`")
            return None

        if len(matches) > 1:
            logger.info(f"Найдено более одной фабрики!!!", matches)
            # Если нашли более одной фабрики, то выбираем фабрику с наивысшим приоритетом.
            matches = [max(matches, key=lambda factory: factory.priority)]

        factory = matches[0]
        logger.info(f"Найдена фабрика: `{factory.__class__.__name__}`")

        return factory.fetch_storage(source_file_path)


rule_registry = RuleRegistry()


class StorageRule(ABC):
    extensions: ClassVar[list[str]]
    mime_type: ClassVar[MIME]
    priority: ClassVar[Priority]
    storage: ClassVar[Type[Storage]]

    def __init__(self, mime_typer: MimeTyper, settings: Settings):
        self.mime_typer = mime_typer
        self.settings = settings

    @abstractmethod
    def match(self, source_file: File) -> bool:
        raise NotImplementedError("Subclasses must implement")

    def fetch_storage(self) -> Storage:
        return self.storage(self.settings)


@rule_registry.register
class TorrentRule(StorageRule):
    priority = Priority.normal
    extensions = [".torrent"]
    storage = Torrent

    def match(self, source_file: File) -> bool:
        return source_file.extension in self.extensions


@rule_registry.register
class ArchiveRule(StorageRule):
    priority = Priority.normal
    extensions = [
        ".dmg",
        ".zip",
        ".gz",
        ".tar",
        ".rpm",
        ".iso",
        ".rar",
        ".7z",
    ]
    storage = Archive

    def match(self, source_file: File) -> bool:
        return source_file.extension in self.extensions


@rule_registry.register
class VideoRule(StorageRule):
    priority = Priority.normal
    extensions = [".mp4", ".avi", ".wmv", ".flv", ".mpg"]
    mime_type = MIME("video")
    storage = Video

    def match(self, source_file: File) -> bool:
        return source_file.mime_type == self.mime_type


@rule_registry.register
class ImageRule(StorageRule):
    priority = Priority.normal
    extensions = [".gif", ".jpg", ".ico", ".icns", ".png", ".tiff", ".svg"]
    mime_type = MIME("image")
    storage = Image

    def match(self, source_file: File) -> bool:
        return source_file.mime_type == self.mime_type


@rule_registry.register
class AudioRule(StorageRule):
    priority = Priority.normal
    extensions = [".mp3", ".m4a", ".flac", ".alac"]
    mime_type = MIME("audio")
    storage = Audio

    def match(self, source_file: File) -> bool:
        return source_file.mime_type == self.mime_type


@rule_registry.register
class ApplicationRule(StorageRule):
    priority = Priority.normal
    extensions = [".app", ".exe"]
    storage = Application

    def match(self, source_file: File) -> bool:
        return source_file.extension in self.extensions


@rule_registry.register
class DocumentRule(StorageRule):
    priority = Priority.normal
    extensions = [".djvu", ".pdf", ".doc", ".xlsx", ".txt", ".epub", ".rtf", ".docx"]
    storage = Document

    def match(self, source_file: File) -> bool:
        return source_file.extension in self.extensions


@rule_registry.register
class OtherRule(StorageRule):
    priority = Priority.low
    extensions = []
    mime_type = MIME("text")
    storage = Other

    def match(self, source_file: File) -> bool:
        return source_file.mime_type == self.mime_type
