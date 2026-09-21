from pathlib import Path
from typing import Literal, Protocol

from PIL.Image import Image

type ImageFormat = Literal["JPEG", "PNG"]


class ImageStorage(Protocol):
    def save(self, img: Image, format: ImageFormat) -> Path: ...
