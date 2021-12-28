from sweeper.app.common.types import MIME, UndefinedMimeType
from sweeper.app.domain.file import File
from tests.utils.tools import copy_file


def test_file(fixtures_path):
    png_file = fixtures_path / "heatmap.png"
    file = File(path=png_file)

    assert file.stem == "heatmap"
    assert file.name == "heatmap.png"
    assert file.mime_type == MIME("image")
    assert file.extension == ".png"


def test_file_uppercase(fixtures_path):
    """
    Проверяем если файл пришел в виде uppercase, в этом случае мы должны extension получить в виде lower_case
    для возможности сравнивать extension между собой
    """
    png_file = fixtures_path / "HEATMAP_UPPERCASE.PNG"
    file = File(path=png_file)

    assert file.name == "HEATMAP_UPPERCASE.PNG"
    assert file.stem == "HEATMAP_UPPERCASE"
    assert file.mime_type == MIME("image")
    assert file.extension == ".png"


def test_file_set_folder(fixtures_path):
    """
    Проверяем что будет если передали не файл, а каталог в объект
    """
    folder = fixtures_path
    file = File(path=folder)

    assert file.name == "fixtures"
    assert file.stem == "fixtures"
    assert file.mime_type == UndefinedMimeType
    assert file.extension == ""


def test_rename(fixtures_path, temp_dir):
    file_name = "heatmap.png"
    source_png_file = fixtures_path / file_name
    target_png_file = temp_dir / file_name
    copy_file(source_png_file, target_png_file)
    assert target_png_file.exists()

    file = File(path=target_png_file)
    assert file.path.name == file_name
    new_file_name = file.rename()

    assert file.path.exists()
    assert new_file_name != file_name
