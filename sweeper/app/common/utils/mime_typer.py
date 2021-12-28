import mimetypes
from pathlib import Path

from sweeper.app.common.types import MIME


class MimeTyper:
    def from_file(self, source_file_path: Path) -> MIME:
        mime_type, _ = mimetypes.guess_type(source_file_path.as_posix())
        return self._get_major_mimetype(mime_type)

    def _get_major_mimetype(self, stdout: str) -> MIME:
        """Разделение полученного результат от команды `file` на основной тип и подтип. Возрвщаем основной тип.

        :param stdout: Результат выподнения команды `file`
        """
        major_type, subtype = stdout.split("/", maxsplit=1)
        return MIME(major_type)
