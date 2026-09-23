from typing import Iterable, Iterator

from ..registry.base import AnnotationResult, ImageSpec, TagSpec


class StaticImageAnnotator:
    def __init__(self, likelihood: Iterator[float]):
        self._likelihood = likelihood

    def annotate(
        self,
        pairs: Iterable[tuple[ImageSpec, TagSpec]],
    ) -> Iterable[AnnotationResult]:
        return (
            AnnotationResult(
                image_path=img.path,
                tag_name=tag.name,
                likelihood=next(self._likelihood),
            )
            for img, tag in pairs
        )

    def name(self) -> str:
        return "dummy"
