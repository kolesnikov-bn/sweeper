from abc import ABC, abstractmethod

from sweeper.domain.file import File
from sweeper.infrastructure.settings.base import Settings
from sweeper.persistence.rules.factories import RuleRegistry


class Iteractor(ABC):
    def __init__(self, registry: RuleRegistry, settings: Settings):
        self.rule_registry = registry
        self.settings = settings

    @abstractmethod
    def usecase(self) -> None:
        raise NotImplementedError


class SweeperUsecase(Iteractor):
    def usecase(self) -> None:
        files = self.collect_files()
        self.perform_storage_usecase(files)

    def collect_files(self) -> list[File]:
        files: list[File] = []

        for file_element in self.settings.base_dir.iterdir():
            is_not_reserved_file = file_element.name not in self.settings.reserved_files

            if is_not_reserved_file:
                files.append(File(path=file_element))

        return files

    def perform_storage_usecase(self, files: list[File]) -> None:
        for file_element in files:
            if (storage := self.rule_registry.find(file_element)) is not None:
                storage.usecase()
