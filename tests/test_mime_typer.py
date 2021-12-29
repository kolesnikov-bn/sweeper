import pytest

from sweeper.app.common.utils.mime_typer import MimeTyper

files_with_expected = [
    ("heatmap.png", "image"),
    ("Keyboard_Configurator.jpg", "image"),
    ("Keyboard_Configurator.pdf", "application"),
    ("TestEmpty.txt", "text"),
    ("TestEmptyFile.rtf", "application"),
    ("heatmap.png.zip", "application"),
    ("sorting_test.dmg", "application"),
    ("test.mp3", "audio"),
    ("test.mov", "video"),
    ("layout.bin", "application"),
]

raw_mimetypes = [
    ("image/png", "image"),
    ("image/jpeg", "image"),
    ("application/pdf", "application"),
    ("text/plain", "text"),
    ("application/rtf", "application"),
    ("application/zip", "application"),
    ("application/zlib", "application"),
    ("audio/mpegapplication/octet-stream", "audio"),
    ("video/quicktime", "video"),
]


incorrect_files_with_expected = [
    ("file_without_ext", "undefined"),
]


@pytest.mark.parametrize("file,expected", files_with_expected)
def test_from_file(file, expected, fixtures_path):
    png_file = fixtures_path / file
    result = MimeTyper().from_file(png_file)

    assert result == expected


@pytest.mark.parametrize("mimetype,expected", raw_mimetypes)
def test__get_major_mimetype(mimetype, expected):
    result = MimeTyper()._get_major_mimetype(mimetype)

    assert result == expected


@pytest.mark.parametrize("file,expected", incorrect_files_with_expected)
def test_from_incorrect_file(file, expected, fixtures_path):
    png_file = fixtures_path / file
    result = MimeTyper().from_file(png_file)

    assert result == expected
