from __future__ import annotations

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

    @abstractmethod
    def create(self, storage: Storage) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_icon(self, storage: Storage) -> None:
        raise NotImplementedError


class ConcreateCreator(StorageCreator):
    def prepare_storage(self, storage: Storage) -> None:
        if not storage.storage_path.exists():
            self.create(storage)
            self.set_icon(storage)

    def create(self, storage: Storage) -> None:
        storage.storage_path.mkdir(mode=self.create_mode)

    def set_icon(self, storage: Storage) -> None:
        icon_alias = "/Icon$'\r'"

        rez_command = f"/usr/bin/Rez -append {storage.icon_path} -o {storage.storage_path}{icon_alias}"
        rez_process = subprocess.Popen(rez_command.split(), stdout=subprocess.PIPE)
        output, error = rez_process.communicate()

        setfile_c_command = f"/usr/bin/SetFile -a C {storage.storage_path}"
        setfile_c_process = subprocess.Popen(setfile_c_command.split(), stdout=subprocess.PIPE)
        output, error = setfile_c_process.communicate()

        setfile_v_command = f"/usr/bin/SetFile -a V {storage.storage_path}$'/Icon\r'"
        setfile_v_process = subprocess.Popen(setfile_v_command.split(), stdout=subprocess.PIPE)
        output, error = setfile_v_process.communicate()

        # SetFile -a C "$droplet"
        # SetFile -a V "$droplet"$'/Icon\r'
        # stdout_result = subprocess.run(
        #     ["file", "-b", "--mime-type", source_file_path.as_posix()], capture_output=True
        # ).stdout.decode()
        pass
