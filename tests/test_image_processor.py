from io import BytesIO

import pytest
from PIL import Image

from src.processing.image_processor import load_image, preprocess_image


def test_load_image():
    image = Image.new("RGB", (100, 100))

    image_file = BytesIO()
    image.save(image_file, format="JPEG")
    image_file.seek(0)

    result = load_image(image_file)

    assert isinstance(result, Image.Image)
    assert result.mode == "RGB"


def test_load_image_rejects_invalid_file():
    invalid_file = BytesIO(b"this is not an image")

    with pytest.raises(ValueError):
        load_image(invalid_file)


def test_preprocess_image_converts_to_rgb():
    image = Image.new("RGBA", (100, 100))

    result = preprocess_image(image)

    assert isinstance(result, Image.Image)
    assert result.mode == "RGB"


def test_preprocess_image_rejects_invalid_input():
    with pytest.raises(TypeError):
        preprocess_image("not an image")