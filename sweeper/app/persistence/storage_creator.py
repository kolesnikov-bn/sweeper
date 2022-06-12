from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import Cocoa

from sweeper.infrastructure.system_logger import logger

if TYPE_CHECKING:
    from sweeper.app.domain.directories import AbstractDirectory


class StorageCreator(ABC):
    create_mode: int = 0o777

    @abstractmethod
    def prepare_storage(self, storage: AbstractDirectory) -> None:
        raise NotImplementedError


class DirCreator(StorageCreator):
    def prepare_storage(self, storage: AbstractDirectory) -> None:
        if not storage.path.exists():
            self.create_storage(storage)
            self.setup_icon_folder(storage)

    def create_storage(self, storage: AbstractDirectory) -> None:
        storage.path.mkdir(mode=self.create_mode)

    def setup_icon_folder(self, storage: AbstractDirectory) -> None:
        logger.debug(
            f"Setting up folder icon `{storage.icon_path.as_posix()}` "
            f"to storage -> {storage.path.as_posix()}"
        )
        try:
            icon_image = Cocoa.NSImage.alloc().initWithContentsOfFile_(storage.icon_path.as_posix())
            Cocoa.NSWorkspace.sharedWorkspace().setIcon_forFile_options_(icon_image, storage.path.as_posix(), 0)
        except Exception as ex:
            logger.error(ex)
