from sweeper.app.domain.file import File
from sweeper.app.persistence.rules.factories import rule_registry
from tests.utils.tools import copy_file


def test_torrent(temp_file):
    temp_file.path = temp_file.path.with_suffix(".torrent")
    storage = rule_registry.find(temp_file)

    assert storage.__class__.__name__ == "Torrent"


def test_archive(temp_file):
    temp_file.path = temp_file.path.with_suffix(".zip")
    storage = rule_registry.find(temp_file)

    assert storage.__class__.__name__ == "Archive"


def test_video(temp_dir, fixtures_path):
    file_name = "test.mov"
    video_path = fixtures_path / file_name
    source_file = File(path=video_path)
    storage = rule_registry.find(source_file)

    assert storage.__class__.__name__ == "Video"


def test_image(temp_dir, fixtures_path):
    file_name = "heatmap.png"
    image_path = fixtures_path / file_name
    source_file = File(path=image_path)
    storage = rule_registry.find(source_file)

    assert storage.__class__.__name__ == "Image"


def test_audio(temp_dir, fixtures_path):
    file_name = "test.mp3"
    file_path = fixtures_path / file_name
    source_file = File(path=file_path)
    storage = rule_registry.find(source_file)

    assert storage.__class__.__name__ == "Audio"


def test_app(temp_file):
    temp_file.path = temp_file.path.with_suffix(".app")
    storage = rule_registry.find(temp_file)

    assert storage.__class__.__name__ == "Application"


def test_doc(temp_dir, fixtures_path):
    file_name = "Keyboard_Configurator.pdf"
    file_path = fixtures_path / file_name
    source_file = File(path=file_path)
    storage = rule_registry.find(source_file)

    assert storage.__class__.__name__ == "Document"


def test_other(temp_dir, fixtures_path):
    file_name = "text_document"
    file_path = fixtures_path / file_name
    source_file = File(path=file_path)
    source_file.mime_typer.from_file(source_file.path)
    storage = rule_registry.find(source_file)

    assert storage.__class__.__name__ == "Other"
