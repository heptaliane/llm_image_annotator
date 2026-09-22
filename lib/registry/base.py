from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, Protocol


@dataclass(frozen=True)
class TagKind:
    label: str


@dataclass(frozen=True)
class TagSpec:
    label: str
    kind: TagKind
    description: str


@dataclass(frozen=True)
class ImageSpec:
    path: Path
    tags: tuple[str, ...] = field(default_factory=tuple)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class GetTagFilterSpec:
    kind: TagKind | None = None
    label: str | None = None


@dataclass
class GetImageFilterSpec:
    created_after: datetime | None = None
    created_before: datetime | None = None
    include_tags: Iterable[str] = tuple()


class Registry(Protocol):
    def add_tag_kind(self, label: str): ...

    def get_tag_kinds(self) -> Iterable[TagKind]: ...

    def add_tag(self, label: str, kind: TagKind, description: str): ...

    def get_tags(self, filter_spec: GetTagFilterSpec) -> Iterable[TagSpec]: ...

    def add_images(self, paths: Iterable[Path]): ...

    def get_images(self, filter_spec: GetImageFilterSpec) -> Iterable[ImageSpec]: ...

    def add_image_tags(self, pairs: Iterable[tuple[ImageSpec, TagSpec]]): ...
