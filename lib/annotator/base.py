from typing import Iterable, Protocol

from ..registry.base import ImageSpec, TagSpec


class ImageAnnotator(Protocol):
    def annotate(
        self,
        imgs: Iterable[ImageSpec],
        tags: Iterable[TagSpec],
    ) -> Iterable[tuple[ImageSpec, TagSpec]]: ...
