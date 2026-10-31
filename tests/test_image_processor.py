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


def test_preprocess_grayscale_image():
    image = Image.new("L", (100, 100), color=128)

    result = preprocess_image(image)

    assert result.mode == "RGB"
    assert result.size == (100, 100)


def test_preprocess_rgba_image():
    image = Image.new("RGBA", (100, 100), color=(255, 0, 0, 128))

    result = preprocess_image(image)

    assert result.mode == "RGB"
    assert result.size == (100, 100)


def test_preprocess_palette_image():
    image = Image.new("P", (100, 100))

    result = preprocess_image(image)

    assert result.mode == "RGB"
    assert result.size == (100, 100)


def test_preprocess_black_image():
    image = Image.new("RGB", (100, 100), color="black")

    result = preprocess_image(image)

    assert result.mode == "RGB"
    assert result.getpixel((0, 0)) == (0, 0, 0)


def test_preprocess_white_image():
    image = Image.new("RGB", (100, 100), color="white")

    result = preprocess_image(image)

    assert result.mode == "RGB"
    assert result.getpixel((0, 0)) == (255, 255, 255)


def test_preprocess_tiny_image():
    image = Image.new("RGB", (1, 1), color="white")

    result = preprocess_image(image)

    assert result.mode == "RGB"
    assert result.size == (1, 1)


def test_preprocess_extreme_aspect_ratio():
    image = Image.new("RGB", (1, 500), color="blue")

    result = preprocess_image(image)

    assert result.mode == "RGB"
    assert result.size == (1, 500)


def test_preprocess_rejects_invalid_input():
    with pytest.raises(TypeError):
        preprocess_image("not an image")


def test_load_image_rejects_empty_file():
    empty_file = BytesIO(b"")

    with pytest.raises(ValueError):
        load_image(empty_file)


def test_load_image_rejects_truncated_image():
    image = Image.new("RGB", (100, 100), color="blue")

    image_file = BytesIO()
    image.save(image_file, format="JPEG")

    # Remove part of the JPEG data to simulate a damaged file.
    damaged_data = image_file.getvalue()[:-100]
    truncated_file = BytesIO(damaged_data)

    with pytest.raises(ValueError):
        load_image(truncated_file)
