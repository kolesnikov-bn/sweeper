from abc import ABC
from dataclasses import dataclass, field
from typing import Optional, Type

from sweeper.common.utils.mime_typer import MimeTyper
from sweeper.domain.file import File
from sweeper.domain.storage_factory.factories import StorageFactory
from sweeper.domain.storages import Storage
from sweeper.infrastructure.system_logger import logger


@dataclass
class FactoryRegistry(ABC):
    _factories: list[StorageFactory] = field(init=False, default_factory=list)
    _registered: set[str] = field(init=False, default_factory=set)

    def register(self, klass: Type[StorageFactory]) -> Type[StorageFactory]:
        """Регистрация фабрики продуктов

        :param klass: фабрика создания продукта
        """
        if not issubclass(klass, StorageFactory):
            raise TypeError("Можно регистрировать только субклассы от Factory")

        if klass.__name__ in self._registered:
            raise ValueError(f"Класс `{klass.__name__}` уже зарегистрирован")

        self._factories.append(klass(MimeTyper()))
        self._registered.add(klass.__name__)

        return klass

    def find(self, source_file_path: File) -> Optional[Storage]:
        matches: list[StorageFactory] = [factory for factory in self._factories if factory.match(source_file_path)]

        if not matches:
            logger.info(f"Не удается найти фабрику для элемента: `{source_file_path}`")
            return None

        if len(matches) > 1:
            logger.info(f"Найдено более одной фабрики!!!", matches)
            # Если нашли более одной фабрики, то выбираем фабрику с наивысшим приоритетом.
            matches = [max(matches, key=lambda factory: factory.priority)]

        product = matches[0]
        logger.info(f"Найдена фабрика: `{product.__class__.__name__}`")

        return product.make_storage(source_file_path)
