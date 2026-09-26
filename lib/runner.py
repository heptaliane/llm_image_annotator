from collections.abc import Set
from itertools import chain
from typing import Iterable

from PIL.Image import Image

from .annotator.base import ImageAnnotator
from .registry.base import (AnnotatedImageSpec, GetAnnotatedImagesFilterSpec,
                            GetImagesFilterSpec, GetTagFilterSpec, ImageSpec,
                            Registry, TagKind, TagSpec)
from .storage.base import ImageStorage


class Runner:
    def __init__(
        self,
        registry: Registry,
        storage: ImageStorage,
        annotators: Iterable[ImageAnnotator],
    ):
        self._registry = registry
        self._storage = storage
        self._annotators = {ia.name(): ia for ia in annotators}
        self._cursor = next(iter(self._annotators))

    def annotators(self) -> Iterable[str]:
        return self._annotators.keys()

    def use_annotator(self, annotator_name: str):
        if annotator_name in self._annotators:
            self._cursor = annotator_name

    def tag_kinds(self) -> Iterable[TagKind]:
        return self._registry.get_tag_kinds()

    def tags(self, kind_name: str) -> Iterable[TagSpec]:
        return self._registry.get_tags(GetTagFilterSpec(kind_name=kind_name))

    def images(
        self, tag_names: Set[str], annotator: str
    ) -> Iterable[AnnotatedImageSpec]:
        return self._registry.get_annotated_images(
            GetAnnotatedImagesFilterSpec(tag_names=tag_names, annotator=annotator),
        )

    def add_tag_kind(self, name: str):
        self._registry.add_tag_kind(TagKind(name=name))

    def add_tag(self, name: str, kind_name: str, description: str, threshold: float):
        tag = TagSpec(
            name=name,
            kind_name=kind_name,
            description=description,
            threshold=threshold,
        )
        self._registry.add_tag(tag)

    def add_images(self, imgs: Iterable[Image]):
        specs = (ImageSpec(path=self._storage.save(img).name) for img in imgs)
        self._registry.add_images(specs)

    def annotate_images(self, images: Iterable[ImageSpec]):
        tags = tuple(self._registry.get_tags(GetTagFilterSpec()))
        self._registry.add_annotations(
            chain.from_iterable(
                (
                    self._annotators[self._cursor].annotate(
                        ((image, tag) for tag in tags)
                    )
                    for image in images
                )
            )
        )

    def annotate_tags(self, tags: Iterable[TagSpec]):
        images = tuple(self._registry.get_images(GetImagesFilterSpec()))
        self._registry.add_annotations(
            chain.from_iterable(
                (
                    self._annotators[self._cursor].annotate(
                        ((image, tag) for image in images)
                    )
                    for tag in tags
                )
            )
        )
