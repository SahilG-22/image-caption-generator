import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="AI Image Caption Generator",
    page_icon="🖼️",
    layout="centered",
)


st.title("🖼️ AI Image Caption Generator")

st.write(
    "Upload an image and generate an AI-powered caption."
)


uploaded_image = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"],
)


if uploaded_image is not None:

    # Display the uploaded image
    image = Image.open(uploaded_image)

    st.image(
        image,
        caption="Uploaded image",
        use_container_width=True,
    )

    # Generate caption button
    if st.button("Generate Caption"):

        with st.spinner("Generating caption..."):

            try:
                # Import only when caption generation is requested.
                from src.captioning.model import generate_caption

                caption = generate_caption(image)

                st.subheader("Generated Caption")
                st.write(caption)

            except Exception as error:
                st.error(
                    "Unable to generate the caption."
                )
                st.exception(error)

    # Text-to-speech will be connected later.
    if st.button("🔊 Listen to Caption"):
        st.info(
            "Text-to-speech will be connected in a later step."
        )