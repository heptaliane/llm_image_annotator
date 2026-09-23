from collections.abc import Set
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, Protocol


@dataclass(frozen=True)
class TagKind:
    name: str


@dataclass(frozen=True)
class TagSpec:
    name: str
    kind_name: str
    description: str
    threshold: float


@dataclass(frozen=True)
class ImageSpec:
    path: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True, kw_only=True)
class AnnotatedImageSpec(ImageSpec):
    tag_names: frozenset[str]


@dataclass(frozen=True)
class AnnotationResult:
    image_path: str
    tag_name: str
    likelihood: float


@dataclass
class GetTagFilterSpec:
    kind_name: str | None = None
    name: str | None = None


@dataclass
class GetImagesFilterSpec:
    paths: Set[str] = field(default_factory=set)
    tag_names: Set[str] = field(default_factory=set)


@dataclass
class GetAnnotationFilterSpec:
    image_paths: Set[str] = field(default_factory=set)
    tag_names: Set[str] = field(default_factory=set)
    ignore_likelihood_threshold: bool = False


class Registry(Protocol):
    def add_tag_kind(self, kind: TagKind): ...

    def get_tag_kinds(self) -> Iterable[TagKind]: ...

    def add_tag(self, tag: TagSpec): ...

    def get_tags(self, filter_spec: GetTagFilterSpec) -> Iterable[TagSpec]: ...

    def add_images(self, imgs: Iterable[ImageSpec]): ...

    def get_images(
        self, filter_spec: GetImagesFilterSpec
    ) -> Iterable[AnnotatedImageSpec]: ...

    def add_annotations(self, results: Iterable[AnnotationResult]): ...

    def get_annotations(
        self,
        filter_spec: GetAnnotationFilterSpec,
    ) -> Iterable[AnnotationResult]: ...
