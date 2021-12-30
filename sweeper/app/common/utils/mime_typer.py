import mimetypes
import subprocess
from pathlib import Path

from sweeper.app.common.types import MIME, UndefinedMimeType
from sweeper.infrastructure.system_logger import logger


class MimeTyper:
    def from_file(self, source_file_path: Path) -> MIME:
        # mime_type, _ = mimetypes.guess_type(source_file_path.as_posix())
        mime_type = subprocess.run(
            ["file", "-b", "--mime-type", source_file_path.as_posix()], capture_output=True
        ).stdout.decode()
        major_mime = UndefinedMimeType

        if mime_type:
            try:
                major_mime = self._get_major_mimetype(mime_type)
            except Exception as ex:
                logger.error(ex, source_file_path)

        return major_mime

    def _get_major_mimetype(self, stdout: str) -> MIME:
        """Разделение полученного результат от команды `file` на основной тип и подтип. Возрвщаем основной тип.

        :param stdout: Результат выполнения команды `file`
        """
        major_type, subtype = stdout.split("/", maxsplit=1)

        return MIME(major_type)
