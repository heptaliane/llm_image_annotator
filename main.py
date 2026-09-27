import os
import random

from lib.annotator.base import ImageAnnotator
from lib.annotator.dummy import DummyImageAnnotator
from lib.app import start
from lib.registry.base import Registry
from lib.registry.memory import MemoryRegistry
from lib.runner import Runner
from lib.storage.base import ImageStorage
from lib.storage.hash import HashImageStorage

ENV_IMAGE_DIR = "IMAGE_DIR"
DEFAULT_IMAGE_DIR = "./data/images"


def setup_registry() -> Registry:
    return MemoryRegistry()


def setup_storage() -> ImageStorage:
    basedir = os.getenv(ENV_IMAGE_DIR, DEFAULT_IMAGE_DIR)
    os.makedirs(basedir, exist_ok=True)
    return HashImageStorage(basedir)


def setup_annotators() -> tuple[ImageAnnotator]:
    return (DummyImageAnnotator(iter(random.random, None)),)


if __name__ == "__main__":
    runner = Runner(
        registry=setup_registry(),
        storage=setup_storage(),
        annotators=setup_annotators(),
    )

    start(runner)
