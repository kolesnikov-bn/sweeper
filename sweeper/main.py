from infrastructure.settings.base import settings

from sweeper.domain.file import File


def main() -> None:
    files: list[File] = []

    for file_element in settings.base_dir.iterdir():
        if file_element.name not in settings.reserved_files:
            files.append(File(path=file_element))


if __name__ == "__main__":
    main()
