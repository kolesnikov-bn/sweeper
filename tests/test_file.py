from sweeper.domain.file import File
from tests.utils.tools import copy_file


def test_file(fixtures_path):
    png_file = fixtures_path / "heatmap.png"
    file = File(path=png_file)

    assert file.name == "heatmap"
    assert file.mime_type == "image"
    assert file.extension == ".png"


def test_rename(fixtures_path, temp_dir):
    file_name = "heatmap.png"
    source_png_file = fixtures_path / file_name
    target_png_file = temp_dir / file_name
    copy_file(source_png_file, target_png_file)
    assert target_png_file.exists()

    file = File(path=target_png_file)
    file.rename()

    assert file.path.exists()
    assert file.path.name != file_name
