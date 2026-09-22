from typing import Iterable, Iterator

from ..annotator.base import AnnotationResult
from ..registry.base import ImageSpec, TagSpec


class StaticImageAnnotator:
    def __init__(self, likelihood: Iterator[float]):
        self._likelihood = likelihood

    def annotate(
        self,
        pairs: Iterable[tuple[ImageSpec, TagSpec]],
    ) -> Iterable[AnnotationResult]:
        return (
            AnnotationResult(image=img, tag=tag, likelihood=next(self._likelihood))
            for img, tag in pairs
        )

    def name(self) -> str:
        return "dummy"
