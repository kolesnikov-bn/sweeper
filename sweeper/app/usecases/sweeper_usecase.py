from abc import ABC, abstractmethod

from app.persistence.storage_creator import StorageCreator

from sweeper.app.domain.file import File
from sweeper.app.persistence.rules.factories import RuleRegistry
from sweeper.infrastructure.settings.base import Settings


class Iteractor(ABC):
    def __init__(self, registry: RuleRegistry, settings: Settings, creator: StorageCreator):
        self.rule_registry = registry
        self.settings = settings
        self.storage_creator = creator

    @abstractmethod
    def usecase(self) -> None:
        raise NotImplementedError


class SweeperUsecase(Iteractor):
    def usecase(self) -> None:
        files = self.collect_files()

        for file in files:
            if (storage := self.rule_registry.find(file)) is not None:
                self.storage_creator.prepare_storage(storage)

                if storage.check_file_exists(file) and not storage.is_overwrite:
                    file.rename()

                file.move_to(storage.make_path(file))
                storage.action(self.settings).perform(file)

    def collect_files(self) -> list[File]:
        files: list[File] = []

        for file_element in self.settings.base_dir.iterdir():
            is_not_reserved_file = file_element.name not in self.settings.reserved_files

            if is_not_reserved_file:
                files.append(File(path=file_element))

        return files
