import os
from typing import Type
from unittest import mock

import pytest

from sweeper.app.domain.directories import AbstractDirectory
from sweeper.app.persistence.rules.actions import Action, NothingAction
from sweeper.app.persistence.storage_creator import ConcreateCreator
from sweeper.infrastructure.settings.base import Settings
from tests.utils.tools import copy_file


class TestDirectory(AbstractDirectory):
    storage_name: str = "29-TestDirectory"
    action: Type[Action] = NothingAction
    icon: str = "blue.png"


def test_create(temp_dir):
    with mock.patch.dict(os.environ, {"SWEEPER_DIR": str(temp_dir)}):
        creator = ConcreateCreator()
        storage = TestDirectory(Settings())
        creator.create_storage(storage)

        assert storage.path.exists()


def test_setup_icon_folder(temp_dir):
    with mock.patch.dict(os.environ, {"SWEEPER_DIR": str(temp_dir)}):
        creator = ConcreateCreator()
        storage = TestDirectory(Settings())
        creator.create_storage(storage)
        creator.setup_icon_folder(storage)

        folder_icon = storage.path / "Icon\r"
        assert folder_icon.exists()


def test_setup_icon_folder_incompleted_set(temp_dir):
    with mock.patch.dict(os.environ, {"SWEEPER_DIR": str(temp_dir)}):
        creator = ConcreateCreator()
        storage = TestDirectory(Settings())
        storage.icon = 1
        creator.create_storage(storage)
        with pytest.raises(TypeError):
            creator.setup_icon_folder(storage)


def test_check_storage_exists(temp_dir):
    with mock.patch.dict(os.environ, {"SWEEPER_DIR": str(temp_dir)}):
        creator = ConcreateCreator()
        storage = TestDirectory(Settings())
        creator.prepare_storage(storage)

        assert storage.path.exists()

        folder_icon = storage.path / "Icon\r"
        assert folder_icon.exists()


def test_storage_path(temp_dir):
    with mock.patch.dict(os.environ, {"SWEEPER_DIR": str(temp_dir)}):
        storage = TestDirectory(Settings())
        storage_path = storage.path

    expected = temp_dir / storage.storage_name

    assert storage_path == expected


def test_icon_path(temp_dir):

    with mock.patch.dict(os.environ, {"SWEEPER_DIR": str(temp_dir)}):
        settings = Settings()
        storage = TestDirectory(settings)
        icon_path = storage.icon_path

    expected = settings.resources / storage.icon

    assert icon_path == expected


def test_check_file_exists(temp_dir, temp_file):
    creator = ConcreateCreator()

    with mock.patch.dict(os.environ, {"SWEEPER_DIR": str(temp_dir)}):
        storage = TestDirectory(Settings())
        creator.create_storage(storage)

    is_file_exists = storage.has_file(temp_file)
    assert is_file_exists is False

    copy_file(temp_file.path, storage.path / temp_file.name)
    is_file_exists = storage.has_file(temp_file)
    assert is_file_exists


def test_make_path(temp_dir, temp_file):
    with mock.patch.dict(os.environ, {"SWEEPER_DIR": str(temp_dir)}):
        storage = TestDirectory(Settings())

    file_path = storage.make_new_path(temp_file)

    assert file_path == storage.path / temp_file.name
