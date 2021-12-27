import subprocess
from pathlib import Path

from sweeper.common.types import MIME


class MimeTyper:
    def from_file(self, source_file_path: Path) -> MIME:
        stdout_result = subprocess.run(
            ["file", "-b", "--mime-type", source_file_path.as_posix()], capture_output=True
        ).stdout.decode()

        return self._get_major_mimetype(stdout_result)

    def _get_major_mimetype(self, stdout: str) -> MIME:
        """Разделение полученного результат от команды `file` на основной тип и подтип. Возрвщаем основной тип.

        :param stdout: Результат выподнения команды `file`
        """
        major_type, subtype = stdout.split("/", maxsplit=1)
        return MIME(major_type)
