import os
from typing import Type
from unittest import mock

from app.domain.actions import Action, NothingAction
from app.persistence.storage_creator import ConcreateCreator
from app.persistence.storages import Storage

from sweeper.infrastructure.settings.base import Settings


class TestStorage(Storage):
    storage_name: str = "1-Applications"
    action: Type[Action] = NothingAction
    icon: str = "blue.rsrc"


def test_create(temp_dir, temp_file):
    with mock.patch.dict(os.environ, {"SWEEPER_DIR": str(temp_dir)}):
        creator = ConcreateCreator()
        storage = TestStorage(Settings())
        creator.create(storage)

        assert storage.storage_path.exists()


def test_check_storage_exists(temp_dir, temp_file):
    with mock.patch.dict(os.environ, {"SWEEPER_DIR": str(temp_dir)}):
        creator = ConcreateCreator()
        storage = TestStorage(Settings())
        creator.prepare_storage(storage)

        assert storage.storage_path.exists()
