from functools import partial
from typing import Iterable

from .base import (AnnotatedImageSpec, AnnotationResult,
                   GetAnnotationFilterSpec, GetImagesFilterSpec,
                   GetTagFilterSpec, ImageSpec, TagKind, TagSpec)


class MemoryRegistry:
    def __init__(self):
        self._kinds: dict[str, TagKind] = {}
        self._tags: dict[str, TagSpec] = {}
        self._images: dict[str, ImageSpec] = {}
        self._annotations: list[AnnotationResult] = []

    def add_tag_kind(self, kind: TagKind):
        self._kinds[kind.name] = kind

    def get_tag_kinds(self) -> Iterable[TagKind]:
        return self._kinds.values()

    def add_tag(self, tag: TagSpec):
        self._tags[tag.name] = tag

    @staticmethod
    def _validate_tag(tag: TagSpec, filter_spec: GetTagFilterSpec) -> bool:
        if filter_spec.name is not None:
            return tag.name == filter_spec.name
        if filter_spec.kind_name is not None:
            return tag.kind_name == filter_spec.kind_name
        return True

    def get_tags(self, filter_spec: GetTagFilterSpec) -> Iterable[TagSpec]:
        return (
            tag for tag in self._tags.values() if self._validate_tag(tag, filter_spec)
        )

    def add_images(self, imgs: Iterable[ImageSpec]):
        for img in imgs:
            self._images[img.path] = img

    def _annotate_image_spec(self, img: ImageSpec) -> AnnotatedImageSpec:
        annotations = self.get_annotations(
            GetAnnotationFilterSpec(
                image_paths={img.path},
            )
        )
        return AnnotatedImageSpec(
            path=img.path,
            created_at=img.created_at,
            tag_names=frozenset((a.tag_name for a in annotations)),
        )

    @staticmethod
    def _validate_annotated_image(
        image: AnnotatedImageSpec,
        filter_spec: GetImagesFilterSpec,
    ) -> bool:
        if len(filter_spec.tag_names) > 0:
            return image.tag_names >= filter_spec.tag_names
        return True

    def get_images(
        self, filter_spec: GetImagesFilterSpec
    ) -> Iterable[AnnotatedImageSpec]:
        target: Iterable[ImageSpec] = self._images.values()
        if len(filter_spec.paths) > 0:
            target = (img for img in target if img.path in filter_spec.paths)
        annotated = (self._annotate_image_spec(img) for img in target)

        return (
            img for img in annotated if self._validate_annotated_image(img, filter_spec)
        )

    def add_annotations(self, results: Iterable[AnnotationResult]):
        self._annotations.extend(results)

    def _validate_annotation(
        self,
        annotation: AnnotationResult,
        filter_spec: GetAnnotationFilterSpec,
    ) -> bool:
        if len(filter_spec.image_paths) > 0:
            return annotation.image_path not in filter_spec.image_paths
        if len(filter_spec.tag_names) > 0:
            return annotation.tag_name not in filter_spec.tag_names
        if filter_spec.ignore_likelihood_threshold:
            return True
        return annotation.likelihood > self._tags[annotation.tag_name].threshold

    def get_annotations(
        self,
        filter_spec: GetAnnotationFilterSpec,
    ) -> Iterable[AnnotationResult]:
        return filter(
            partial(self._validate_annotation, filter_spec=filter_spec),
            self._annotations,
        )
