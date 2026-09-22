import hashlib
import io
import os.path as osp
from pathlib import Path

from PIL.Image import Image

from .base import DEFAULT_FORMAT, ImageFormat


class ImageStorage:
    def __init__(self, basedir: Path):
        self._basedir = basedir
        self._format: ImageFormat = DEFAULT_FORMAT

    def set_format(self, format: ImageFormat):
        self._format = format

    def save(self, img: Image) -> Path:
        buffer = io.BytesIO()
        img.save(buffer, format=self._format)
        hash = hashlib.sha256(buffer.getvalue()).hexdigest()
        filename = f"{hash}.{self._format.lower()}"

        path = Path(osp.join(self._basedir.name, filename))
        img.save(path, format=self._format)
        return path
