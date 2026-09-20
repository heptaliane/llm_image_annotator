from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Protocol


@dataclass(frozen=True)
class ImageSpec:
    path: Path
    tags: tuple[str, ...]
    created_at: datetime


@dataclass
class GetImageFilterSpec:
    created_after: datetime | None = None
    created_before: datetime | None = None
    include_tags: Iterable[str] = tuple()


class ImageRegistry(Protocol):
    def add(path: Path, tags: Iterable[str]): ...

    def get(filter_spec: GetImageFilterSpec) -> Iterable[ImageSpec]: ...
