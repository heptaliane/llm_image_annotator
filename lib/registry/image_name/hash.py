import hashlib
import io

from PIL.Image import Image


def image_hash(img: Image) -> str:
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    hash = hashlib.sha256(buffer.getvalue()).hexdigest()
    return hash
