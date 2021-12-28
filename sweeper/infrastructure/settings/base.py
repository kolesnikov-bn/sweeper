from pathlib import Path

from pydantic import BaseSettings

ROOT_PATH = Path(__file__).parent.parent.parent.absolute()


class Settings(BaseSettings):
    root_path: Path = ROOT_PATH
    home_dir: Path = Path.home()
    sweeper_dir: str = "Downloads"
    application_folder: Path = Path("/Applications")
    reserved_files: list[str] = [
        "$RECYCLE.BIN",
        ".DS_Store",
        ".localized",
        "1-Applications",
        "2-Archives",
        "3-Audios",
        "4-Torrents",
        "5-Videos",
        "6-Images",
        "7-Docs",
        "8-Others",
        "Icon\r",
        "Telegram Desktop",
    ]

    @property
    def base_dir(self) -> Path:
        return self.home_dir.joinpath(self.sweeper_dir)

    @property
    def resources(self) -> Path:
        return self.root_path.joinpath("resources")


settings = Settings()
