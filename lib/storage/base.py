from pathlib import Path
from typing import Literal, Protocol

from PIL.Image import Image

type ImageFormat = Literal["JPEG", "PNG"]

DEFAULT_FORMAT: ImageFormat = "JPEG"


class ImageStorage(Protocol):
    def set_format(self, format: ImageFormat): ...
    def save(self, img: Image) -> Path: ...
