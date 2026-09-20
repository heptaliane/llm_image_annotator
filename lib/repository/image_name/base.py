from typing import Callable

from PIL import Image

type ImageNameGenerator = Callable[[Image], str]
