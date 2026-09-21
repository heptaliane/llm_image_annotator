import hashlib
import io
import os.path as osp
from pathlib import Path

from PIL.Image import Image

from .base import ImageFormat


class ImageStorage:
    def __init__(self, basedir: Path):
        self._basedir = basedir

    def save(self, img: Image, format: ImageFormat) -> Path:
        buffer = io.BytesIO()
        img.save(buffer, format=format)
        hash = hashlib.sha256(buffer.getvalue()).hexdigest()
        filename = f"{hash}.{format.lower()}"

        path = Path(osp.join(self._basedir.name, filename))
        img.save(path, format=format)
        return path
