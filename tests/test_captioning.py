from PIL import Image

from src.captioning.model import generate_caption

def test_generate_caption():
    image = Image.open("sample_images/test.jpg")

    caption = generate_caption(image)

    assert isinstance(caption, str)
    assert len(caption) > 0