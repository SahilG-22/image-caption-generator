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
        return preprocess_image(image)

    except (UnidentifiedImageError, OSError) as error:
        raise ValueError("Invalid image file") from error


def preprocess_image(image):
    """
    Prepare an image for the captioning model.

    Parameters:
        image: PIL Image

    Returns:
        PIL.Image.Image: RGB image

    Raises:
        TypeError: If the input is not a PIL Image
    """
    if not isinstance(image, Image.Image):
        raise TypeError("image must be a PIL Image")

    return image.convert("RGB")