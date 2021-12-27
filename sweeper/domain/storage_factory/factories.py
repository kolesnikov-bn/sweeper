from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar, Type

from sweeper.common.enums import Priority
from sweeper.common.types import MIME
from sweeper.common.utils.mime_typer import MimeTyper
from sweeper.domain.file import File
from sweeper.domain.storage_factory.factory_mapper import FactoryRegistry
from sweeper.domain.storages import Application, Archive, Audio, Document, Image, Other, Storage, Torrent, Video

factory_registry = FactoryRegistry()


class StorageFactory(ABC):
    extensions: ClassVar[list[str]]
    mime_type: ClassVar[MIME]
    priority: ClassVar[Priority]
    storage: ClassVar[Type[Storage]]

    def __init__(self, mime_typer: MimeTyper):
        self.mime_typer = mime_typer

    @abstractmethod
    def match(self, source_file: File) -> bool:
        raise NotImplementedError("Subclasses must implement")

    def make_storage(self, source_file: File) -> Storage:
        return self.storage(source_file)


@factory_registry.register
class TorrentStorageFactory(StorageFactory):
    priority = Priority.normal
    extensions = [".torrent"]
    storage = Torrent

    def match(self, source_file: File) -> bool:
        return source_file.extension in self.extensions


@factory_registry.register
class ArchiveStorageFactory(StorageFactory):
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


@factory_registry.register
class VideoStorageFactory(StorageFactory):
    priority = Priority.normal
    extensions = [".mp4", ".avi", ".wmv", ".flv", ".mpg"]
    mime_type = MIME("video")
    storage = Video

    def match(self, source_file: File) -> bool:
        return source_file.mime_type == self.mime_type


@factory_registry.register
class ImageStorageFactory(StorageFactory):
    priority = Priority.normal
    extensions = [".gif", ".jpg", ".ico", ".icns", ".png", ".tiff", ".svg"]
    mime_type = MIME("image")
    storage = Image

    def match(self, source_file: File) -> bool:
        return source_file.mime_type == self.mime_type


@factory_registry.register
class AudioStorageFactory(StorageFactory):
    priority = Priority.normal
    extensions = [".mp3", ".m4a", ".flac", ".alac"]
    mime_type = MIME("audio")
    storage = Audio

    def match(self, source_file: File) -> bool:
        return source_file.mime_type == self.mime_type


@factory_registry.register
class ApplicationStorageFactory(StorageFactory):
    priority = Priority.normal
    extensions = [".app", ".exe"]
    storage = Application

    def match(self, source_file: File) -> bool:
        return source_file.extension in self.extensions


@factory_registry.register
class DocumentStorageFactory(StorageFactory):
    priority = Priority.normal
    extensions = [".djvu", ".pdf", ".doc", ".xlsx", ".txt", ".epub", ".rtf", ".docx"]
    storage = Document

    def match(self, source_file: File) -> bool:
        return source_file.extension in self.extensions


@factory_registry.register
class OtherStorageFactory(StorageFactory):
    priority = Priority.low
    extensions = []
    mime_type = MIME("text")
    storage = Other

    def match(self, source_file: File) -> bool:
        return source_file.mime_type == self.mime_type
