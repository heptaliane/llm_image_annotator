from datetime import datetime
from pathlib import Path
from typing import Iterable

from .base import GetImageFilterSpec, ImageSpec


class MemoryImageRegistry:
    def __init__(self):
        self._images: list[ImageSpec] = []

    def add(self, path: Path, tags: Iterable[str]):
        spec = ImageSpec(
            path=path,
            tags=(t for t in tags),
            created_at=datetime.now(),
        )
        self._images.append(spec)

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

    def get(self, filter_spec: GetImageFilterSpec) -> Iterable[ImageSpec]:
        return (img for img in self._images if self._validate_image(img, filter_spec))
