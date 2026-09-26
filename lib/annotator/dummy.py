from typing import Iterable, Iterator

from ..registry.base import AnnotationResult, ImageSpec, TagSpec

_DUMMY_ANNOTATOR_NAME = "dummy"


class DummyImageAnnotator:
    def __init__(self, likelihood: Iterator[float]):
        self._likelihood = likelihood

    def annotate(
        self,
        pairs: Iterable[tuple[ImageSpec, TagSpec]],
    ) -> Iterable[AnnotationResult]:
        return (
            AnnotationResult(
                annotator=_DUMMY_ANNOTATOR_NAME,
                image_path=img.path,
                tag_name=tag.name,
                likelihood=next(self._likelihood),
            )
            for img, tag in pairs
        )

    def name(self) -> str:
        return _DUMMY_ANNOTATOR_NAME
