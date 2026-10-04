from PIL import Image, UnidentifiedImageError


def load_image(uploaded_file):
    """
    Open an uploaded image and return it as an RGB PIL Image.

    Parameters:
        uploaded_file: File-like object containing an image

    Returns:
        PIL.Image.Image: RGB image

    Raises:
        ValueError: If the uploaded file is not a valid image
    """
    try:
        image = Image.open(uploaded_file)
        return image.convert("RGB")

    except (UnidentifiedImageError, OSError) as error:
        raise ValueError("Invalid image file") from error
