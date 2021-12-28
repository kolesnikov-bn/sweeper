from __future__ import annotations

import shutil
import subprocess
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.persistence.storages import Storage


class StorageCreator(ABC):
    create_mode: int = 0o777

    @abstractmethod
    def prepare_storage(self, storage: Storage) -> None:
        raise NotImplementedError


class ConcreateCreator(StorageCreator):
    def prepare_storage(self, storage: Storage) -> None:
        if not storage.storage_path.exists():
            self.create(storage)

        #     try:
        #         self.render(storage)
        #     except Exception:
        #         self.create(storage)

    def create(self, storage: Storage) -> None:
        storage.storage_path.mkdir(mode=self.create_mode)

    def render(self, storage: Storage):
        shutil.copytree(storage.template_path, storage.storage_path, copy_function=shutil.copy)

        setfile_c_command = f"/usr/bin/SetFile -a C {storage.storage_path}"
        setfile_c_process = subprocess.Popen(setfile_c_command.split(), stdout=subprocess.PIPE)
        output, error = setfile_c_process.communicate()

        setfile_v_command = f"/usr/bin/SetFile -a V {storage.storage_path}/Icon\r"
        setfile_v_process = subprocess.Popen(setfile_v_command.split(), stdout=subprocess.PIPE)
        output, error = setfile_v_process.communicate()
