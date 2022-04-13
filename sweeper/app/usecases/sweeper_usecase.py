from abc import ABC, abstractmethod

from sweeper.app.domain.file import File
from sweeper.app.persistence.rules.factories import RuleRegistry
from sweeper.app.persistence.storage_creator import StorageCreator
from sweeper.infrastructure.settings.base import Settings


class Iteractor(ABC):
    def __init__(self, registry: RuleRegistry, settings: Settings, creator: StorageCreator):
        self.rule_registry = registry
        self.settings = settings
        self.directory_creator = creator

    @abstractmethod
    def allocate(self) -> None:
        raise NotImplementedError


class SweeperUsecase(Iteractor):
    def allocate(self) -> None:
        files = self.collect_files()

        for file in files:
            if (directory := self.rule_registry.find(file)) is not None:
                self.directory_creator.prepare_storage(directory)

                if directory.has_file(file) and not directory.is_overwrite:
                    file.rename()

                file.move_to(directory.make_path(file))
                directory.action(self.settings).perform(file)

    def collect_files(self) -> list[File]:
        files: list[File] = []

        for file_element in self.settings.base_dir.iterdir():
            is_not_reserved_file = file_element.name not in self.settings.reserved_files

            if is_not_reserved_file:
                files.append(File(path=file_element))

        return files
