from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


MODEL_NAME = "Salesforce/blip-image-captioning-base"


print("Loading BLIP model...")

processor = BlipProcessor.from_pretrained(MODEL_NAME)
model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)

print("Model loaded successfully!")


image = Image.open("sample_images/test.jpg").convert("RGB")

inputs = processor(
    images=image,
    return_tensors="pt"
)

output = model.generate(
    **inputs,
    max_new_tokens=30
)

caption = processor.decode(
    output[0],
    skip_special_tokens=True
)

print("Generated caption:", caption)