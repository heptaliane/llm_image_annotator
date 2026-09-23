from typing import Iterable, Protocol

from ..registry.base import AnnotationResult, ImageSpec, TagSpec


class ImageAnnotator(Protocol):
    def annotate(
        self,
        pairs: Iterable[tuple[ImageSpec, TagSpec]],
    ) -> Iterable[AnnotationResult]: ...

    def name(self) -> str: ...
