from dataclasses import dataclass
from typing import Iterable, Protocol

from ..registry.base import ImageSpec, TagSpec


@dataclass(frozen=True)
class AnnotationResult:
    image: ImageSpec
    tag: TagSpec
    likelihood: float


class ImageAnnotator(Protocol):
    def annotate(
        self,
        pairs: Iterable[tuple[ImageSpec, TagSpec]],
    ) -> Iterable[AnnotationResult]: ...

    def name(self) -> str: ...
