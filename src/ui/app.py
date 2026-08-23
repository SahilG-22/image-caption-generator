import streamlit as st
from PIL import Image

from src.captioning.model import generate_caption
from src.utils.text_to_speech import speak_text


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="VisionAI | Image Caption Generator",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE
# ============================================================

if "caption" not in st.session_state:
    st.session_state.caption = None

if "image_name" not in st.session_state:
    st.session_state.image_name = None


# ============================================================
# CUSTOM CSS
#
# IMPORTANT:
# This CSS is contained in ONE st.markdown() call.
# There is no HTML layout inside the CSS.
# ============================================================

st.markdown(
    """
<style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(99, 102, 241, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(6, 182, 212, 0.14),
                transparent 30%
            ),
            #070b16;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- HIDE STREAMLIT CHROME ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* ---------- TYPOGRAPHY ---------- */

    h1, h2, h3 {
        color: #f8fafc !important;
    }

    p {
        color: #94a3b8;
    }

    /* ---------- TOP BRAND ---------- */

    .brand-title {
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #f8fafc;
        margin-bottom: 0;
    }

    .brand-subtitle {
        color: #64748b;
        font-size: 0.78rem;
        margin-top: -5px;
    }

    /* ---------- HERO ---------- */

    .hero-title {
        font-size: clamp(2.8rem, 7vw, 5.8rem);
        line-height: 0.95;
        font-weight: 850;
        letter-spacing: -4px;
        margin-top: 50px;
        margin-bottom: 25px;
        color: #ffffff;
    }

    .hero-gradient {
        background: linear-gradient(
            90deg,
            #818cf8,
            #22d3ee
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-text {
        max-width: 700px;
        font-size: 1.05rem;
        line-height: 1.8;
        color: #94a3b8;
        margin-bottom: 25px;
    }

    /* ---------- BADGES ---------- */

    .badge {
        display: inline-block;
        padding: 7px 13px;
        margin-right: 7px;
        margin-bottom: 7px;
        border-radius: 999px;
        background: rgba(99, 102, 241, 0.10);
        border: 1px solid rgba(129, 140, 248, 0.25);
        color: #c7d2fe;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* ---------- CARDS ---------- */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(15, 23, 42, 0.68);
        border: 1px solid rgba(148, 163, 184, 0.13);
        border-radius: 22px;
        padding: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.22);
    }

    /* ---------- FILE UPLOADER ---------- */

    [data-testid="stFileUploaderDropzone"] {
        background: rgba(30, 41, 59, 0.45) !important;
        border: 1px dashed rgba(129, 140, 248, 0.45) !important;
        border-radius: 18px !important;
        min-height: 170px;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #818cf8 !important;
        background: rgba(99, 102, 241, 0.08) !important;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 13px;
        border: 1px solid rgba(129, 140, 248, 0.35);
        background: linear-gradient(
            135deg,
            #6366f1,
            #4f46e5
        );
        color: white;
        font-weight: 700;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 12px 35px rgba(79, 70, 229, 0.35);
    }

    /* ---------- CAPTION ---------- */

    .caption-box {
        padding: 25px;
        border-radius: 18px;
        background:
            linear-gradient(
                135deg,
                rgba(99, 102, 241, 0.12),
                rgba(6, 182, 212, 0.07)
            );
        border: 1px solid rgba(129, 140, 248, 0.25);
        margin-top: 15px;
    }

    .caption-label {
        color: #818cf8;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .caption-text {
        color: #f8fafc;
        font-size: 1.25rem;
        line-height: 1.6;
        font-weight: 600;
    }

    /* ---------- IMAGE ---------- */

    [data-testid="stImage"] {
        border-radius: 18px;
        overflow: hidden;
    }

    /* ---------- DIVIDER ---------- */

    hr {
        border-color: rgba(148, 163, 184, 0.10);
        margin-top: 45px;
        margin-bottom: 45px;
    }

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# NAVBAR
# ============================================================

top_left, top_right = st.columns([3, 1])

with top_left:
    st.markdown(
        "### 🖼️ VisionAI"
    )
    st.caption(
        "Intelligent visual understanding"
    )

with top_right:
    st.markdown(
        "<div style='text-align:right;'>"
        "🤖 AI VISION<br>"
        "<small>LOCAL PROCESSING</small>"
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-title">
        Turn images into<br>
        <span class="hero-gradient">meaning.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-text">
        Upload an image and let an AI vision model understand
        what it sees. Generate a natural-language description
        and listen to the result using text-to-speech.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <span class="badge">🧠 AI Vision</span>
    <span class="badge">✨ Natural Captions</span>
    <span class="badge">🔊 Text to Speech</span>
    <span class="badge">⚡ Local Processing</span>
    """,
    unsafe_allow_html=True,
)


st.divider()


# ============================================================
# MAIN WORKSPACE
# ============================================================

left, right = st.columns(
    [1, 1],
    gap="large",
)


# ============================================================
# LEFT SIDE — INPUT
# ============================================================

with left:

    with st.container(border=True):

        st.subheader("01 · Image Input")

        st.write(
            "Give VisionAI an image to analyze."
        )

        uploaded_image = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png"],
            label_visibility="visible",
        )

        if uploaded_image is None:

            st.info(
                "Upload a JPG, JPEG or PNG image to begin."
            )

        else:

            image = Image.open(uploaded_image)

            st.success(
                f"Image loaded: {uploaded_image.name}"
            )

            st.image(
                image,
                caption="Your image",
                use_container_width=True,
            )

            if st.button(
                "✨ Generate AI Caption",
                key="generate_caption",
            ):

                with st.spinner(
                    "🧠 VisionAI is analyzing your image..."
                ):

                    try:

                        caption = generate_caption(image)

                        st.session_state.caption = caption
                        st.session_state.image_name = (
                            uploaded_image.name
                        )

                    except Exception as error:

                        st.session_state.caption = None

                        st.error(
                            "Unable to generate the caption."
                        )

                        st.exception(error)


# ============================================================
# RIGHT SIDE — OUTPUT
# ============================================================

with right:

    with st.container(border=True):

        st.subheader("02 · AI Description")

        if st.session_state.caption:

            st.markdown(
                """
                <div class="caption-box">
                    <div class="caption-label">
                        Generated Caption
                    </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                    <div class="caption-text">
                        {st.session_state.caption}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")

            if st.button(
                "🔊 Listen to Caption",
                key="listen_caption",
            ):

                with st.spinner(
                    "🔊 Speaking caption..."
                ):

                    try:

                        speak_text(
                            st.session_state.caption
                        )

                        st.success(
                            "Caption spoken successfully."
                        )

                    except Exception as error:

                        st.error(
                            "Unable to speak the caption."
                        )

                        st.exception(error)

        else:

            st.info(
                "Your generated caption will appear here."
            )

            st.write("")

            st.markdown(
                """
                ### ✨ Ready for AI

                Upload an image on the left and click
                **Generate AI Caption**.

                The caption will appear here automatically.
                """
            )


# ============================================================
# HOW IT WORKS
# ============================================================

st.divider()

st.subheader("How VisionAI works")

st.write(
    "A simple three-step pipeline transforms visual information "
    "into understandable language."
)


step1, step2, step3 = st.columns(3)


with step1:

    with st.container(border=True):

        st.markdown("### 📤 01")
        st.markdown("**Upload**")
        st.write(
            "Choose an image from your computer."
        )


with step2:

    with st.container(border=True):

        st.markdown("### 🧠 02")
        st.markdown("**Understand**")
        st.write(
            "The image captioning model analyzes "
            "the visual content."
        )


with step3:

    with st.container(border=True):

        st.markdown("### 🔊 03")
        st.markdown("**Listen**")
        st.write(
            "Hear the generated caption through "
            "your computer speaker."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "VisionAI · AI Image Caption Generator · "
    "Computer Vision + Natural Language + Text-to-Speech"
)