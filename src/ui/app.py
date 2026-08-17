import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="AI Image Caption Generator",
    page_icon="🖼️",
    layout="centered",
)


st.title("🖼️ AI Image Caption Generator")
st.write("Upload an image and generate an AI-powered caption.")


uploaded_image = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"],
)


if "caption" not in st.session_state:
    st.session_state.caption = None


if uploaded_image is not None:

    image = Image.open(uploaded_image)

    st.image(
        image,
        caption="Uploaded image",
        use_container_width=True,
    )

    if st.button("Generate Caption"):

        with st.spinner("Loading AI model and generating caption..."):

            try:
                from src.captioning.model import generate_caption

                st.session_state.caption = generate_caption(image)

            except Exception as error:
                st.session_state.caption = None
                st.error("Unable to generate the caption.")
                st.exception(error)

    if st.session_state.caption:

        st.subheader("Generated Caption")
        st.write(st.session_state.caption)

        if st.button("🔊 Listen to Caption"):

            with st.spinner("Speaking caption..."):

                try:
                    from src.utils.text_to_speech import speak_text

                    speak_text(st.session_state.caption)
                    st.success("Caption spoken successfully.")

                except Exception as error:
                    st.error("Unable to speak the caption.")
                    st.exception(error)