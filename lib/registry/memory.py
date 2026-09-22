from pathlib import Path
from typing import Iterable

from .base import (GetImageFilterSpec, GetTagFilterSpec, ImageSpec, TagKind,
                   TagSpec)


class MemoryRegistry:
    def __init__(self):
        self._kinds: list[TagKind] = []
        self._tags: list[TagSpec] = []
        self._images: dict[Path, ImageSpec] = {}

    def add_tag_kind(self, kind: TagKind):
        self._kinds.append(kind)

    def get_tag_kinds(self) -> Iterable[TagKind]:
        return self._kinds

    def add_tag(self, tag: TagSpec):
        self._tags.append(tag)

    @staticmethod
    def _validate_tag(tag: TagSpec, filter_spec: GetTagFilterSpec) -> bool:
        if filter_spec.label is not None:
            return tag.label == filter_spec.label
        if filter_spec.kind is not None:
            return tag.kind == filter_spec.kind
        return True

    def get_tags(self, filter_spec: GetTagFilterSpec) -> Iterable[TagSpec]:
        return (t for t in self._tags if self._validate_tag(t, filter_spec))

    def add_images(self, imgs: Iterable[ImageSpec]):
        for img in imgs:
            self._images[img.path] = img

    @staticmethod
    def _validate_image(img: ImageSpec, filter_spec: GetImageFilterSpec) -> bool:
        for tag in filter_spec.include_tags:
            if tag not in img.tags:
                return False
        if filter_spec.created_after is not None:
            if img.created_at < filter_spec.created_after:
                return False
        if filter_spec.created_before is not None:
            if img.created_at > filter_spec.created_before:
                return False
        return True

    def get_images(self, filter_spec: GetImageFilterSpec) -> Iterable[ImageSpec]:
        return (
            img
            for img in self._images.values()
            if self._validate_image(img, filter_spec)
        )

    def add_image_tags(self, pairs: Iterable[tuple[ImageSpec, TagSpec]]):
        for img, tag in pairs:
            spec = self._images[img.path]
            self._images[img.path] = ImageSpec(
                path=img.path,
                tags=(*spec.tags, tag.label),
                created_at=spec.created_at,
            )
