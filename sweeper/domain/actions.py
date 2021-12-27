import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

from sweeper.common.enums import StatusEnum
from sweeper.infrastructure.settings.base import Settings
from sweeper.infrastructure.system_logger import logger


class Action(ABC):
    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    def perform(self, source_file_path: Path) -> None:
        """Действие над файлом"""
        raise NotImplementedError("Subclasses must implement")


class NothingAction(Action):
    def perform(self, source_file_path: Path) -> None:
        """Пустое действие"""


class TorrentAction(Action):
    def __init__(self, settings: Settings):
        super(TorrentAction, self).__init__(settings)
        self.torrent_path: Path = self.settings.application_folder / "Transmission Remote GUI.app"

    def perform(self, source_file_path: Path) -> None:
        logger.info(f"Perform Torrent Action: {source_file_path=}")
        status_code = subprocess.run(["open", self.torrent_path, source_file_path], capture_output=True).returncode
        status = StatusEnum(status_code)
        logger.info(f"{status=}")
