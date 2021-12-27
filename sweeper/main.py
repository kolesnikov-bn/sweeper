from infrastructure.settings.base import settings


def main() -> None:
    files = sorted(
        file_element for file_element in settings.base_dir.iterdir() if file_element.name not in settings.reserved_files
    )


if __name__ == "__main__":
    main()
