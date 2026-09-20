from typing import Iterable, Protocol

from ..repository import ImageSpec, TagSpec


class ImageAnnotator(Protocol):
    def annotate(
        self,
        imgs: Iterable[ImageSpec],
        tags: Iterable[TagSpec],
    ) -> Iterable[tuple[ImageSpec, TagSpec]]: ...
