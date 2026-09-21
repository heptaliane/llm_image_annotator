from typing import Callable

from PIL.Image import Image

type ImageNameGenerator = Callable[[Image], str]
