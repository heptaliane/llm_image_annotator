from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, Protocol

from PIL import Image


@dataclass(frozen=True)
class TagKind:
    label: str


@dataclass(frozen=True)
class TagSpec:
    label: str
    kind: TagKind
    description: str


@dataclass
class GetTagFilterSpec:
    kind: TagKind | None = None
    label: str | None = None


class TagRegistry(Protocol):
    def add_kind(self, label: str): ...

    def get_kind(self) -> Iterable[TagKind]: ...

    def add(self, tag: TagSpec): ...

    def get(self, filter_spec: GetTagFilterSpec) -> Iterable[TagSpec]: ...


@dataclass(frozen=True)
class ImageSpec:
    path: Path
    tags: tuple[str, ...] = field(default_factory=tuple)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class GetImageFilterSpec:
    created_after: datetime | None = None
    created_before: datetime | None = None
    include_tags: Iterable[str] = tuple()


class ImageRegistry(Protocol):
    def add(self, img: Image) -> ImageSpec: ...

    def add_tags(self, tags: Iterable[tuple[ImageSpec, TagSpec]]): ...

    def get(self, filter_spec: GetImageFilterSpec) -> Iterable[ImageSpec]: ...
