from typing import Iterable

from PIL import Image


class StaticImageAnnotator:
    def __init__(self, tags: Iterable[str]):
        self._tags = tags

    def annotate(self, _img: Image) -> Iterable[str]:
        return self._tags
