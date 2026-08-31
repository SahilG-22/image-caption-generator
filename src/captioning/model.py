import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForMultimodalLM


MODEL_NAME = "Salesforce/blip-image-captioning-base"


def get_device():
    """
    Select the best available device.

    Priority:
    1. MPS - Apple Silicon GPU
    2. CUDA - NVIDIA GPU
    3. CPU
    """

    if torch.backends.mps.is_available():
        return "mps"

    if torch.cuda.is_available():
        return "cuda"

    return "cpu"


# Select device
DEVICE = get_device()


# Load processor and model once
processor = AutoProcessor.from_pretrained(MODEL_NAME)

model = AutoModelForMultimodalLM.from_pretrained(MODEL_NAME)
model = model.to(DEVICE)

model.eval()


def generate_caption(image):
    """
    Generate a caption for a PIL image.

    Parameters:
        image: PIL Image

    Returns:
        str: Generated image caption
    """

    if not isinstance(image, Image.Image):
        raise TypeError("image must be a PIL Image")

    # Make sure the image is RGB
    image = image.convert("RGB")

    # Prepare image for the model
    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    # Move inputs to the selected device
    inputs = {
        key: value.to(DEVICE)
        for key, value in inputs.items()
    }

    # Generate caption
    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=30
        )

    # Convert output to text
    caption = processor.batch_decode(
        output,
        skip_special_tokens=True
    )[0]

    return caption