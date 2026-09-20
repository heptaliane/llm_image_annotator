from typing import Iterable, Protocol

from PIL import Image


class ImageAnnotator(Protocol):
    def annotate(self, img: Image) -> Iterable[str]: ...
