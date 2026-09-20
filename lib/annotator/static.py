from typing import Iterable

from ..repository.base import ImageSpec, TagSpec


class StaticImageAnnotator:
    def annotate(
        self,
        imgs: Iterable[ImageSpec],
        tags: Iterable[TagSpec],
    ) -> Iterable[tuple[ImageSpec, TagSpec]]:
        return ((img, tag) for img in imgs for tag in tags)
