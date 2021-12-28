from abc import ABC, abstractmethod

from infrastructure.settings.base import settings

from sweeper.domain.file import File
from sweeper.persistence.rules.factories import RuleRegistry, rule_registry


class Iteractor(ABC):
    def __init__(self, registry: RuleRegistry):
        self.rule_registry = registry

    @abstractmethod
    def usecase(self) -> None:
        raise NotImplementedError


class SweeperUsecase(Iteractor):
    def usecase(self) -> None:
        files = self.collect_files()
        self.perform_storage_usecase(files)

    def collect_files(self) -> list[File]:
        files: list[File] = []

        for file_element in settings.base_dir.iterdir():
            if file_element.name not in settings.reserved_files:
                files.append(File(path=file_element))

        return files

    def perform_storage_usecase(self, files: list[File]) -> None:
        for file_element in files:
            if (storage := self.rule_registry.find(file_element)) is not None:
                storage.usecase()


def main() -> None:
    SweeperUsecase(rule_registry).usecase()


if __name__ == "__main__":
    main()
