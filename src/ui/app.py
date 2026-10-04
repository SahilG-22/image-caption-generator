import sys
from pathlib import Path

# ============================================================
# PROJECT PATH SETUP
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st
from src.processing.image_processor import load_image

from src.captioning.model import generate_caption
from src.utils.text_to_speech import speak_text


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="VisionAI",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# HTML HELPER
# ============================================================
#
# IMPORTANT:
# We intentionally DO NOT use textwrap here.
#
# Streamlit's st.html() directly renders HTML/CSS and avoids
# Markdown interpreting indented HTML as code.
#
# ============================================================

def render_html(markup: str):
    st.html(markup.strip())


# ============================================================
# GLOBAL CSS
# ============================================================

render_html(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');


/* ======================================================
   GLOBAL
   ====================================================== */

html,
body,
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(99, 102, 241, 0.12),
            transparent 32%
        ),
        radial-gradient(
            circle at 85% 20%,
            rgba(6, 182, 212, 0.10),
            transparent 30%
        ),
        #070b16 !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    max-width: 1280px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

* {
    font-family: "DM Sans", sans-serif;
}


/* ======================================================
   NAVBAR
   ====================================================== */

.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 12px 18px;
    margin-bottom: 70px;

    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 18px;

    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(18px);

    box-shadow:
        0 10px 40px rgba(0, 0, 0, 0.25);
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;

    color: #f8fafc;

    font-size: 21px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.brand-icon {
    width: 42px;
    height: 42px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 13px;

    background:
        linear-gradient(
            135deg,
            #6366f1,
            #06b6d4
        );

    box-shadow:
        0 0 30px rgba(99, 102, 241, 0.35);

    font-size: 22px;
}

.nav-badge {
    padding: 8px 14px;

    border-radius: 999px;

    background: rgba(99, 102, 241, 0.10);
    border: 1px solid rgba(99, 102, 241, 0.25);

    color: #a5b4fc;

    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
    letter-spacing: 0.8px;
}


/* ======================================================
   HERO
   ====================================================== */

.hero {
    text-align: center;
    padding: 20px 20px 65px;
}

.hero-label {
    display: inline-flex;
    align-items: center;
    gap: 8px;

    padding: 8px 14px;

    border-radius: 999px;

    background: rgba(6, 182, 212, 0.08);
    border: 1px solid rgba(6, 182, 212, 0.22);

    color: #67e8f9;

    font-family: "JetBrains Mono", monospace;
    font-size: 12px;

    margin-bottom: 25px;
}

.hero h1 {
    margin: 0;

    color: #ffffff;

    font-size: clamp(45px, 7vw, 82px);
    line-height: 0.98;

    font-weight: 800;
    letter-spacing: -4px;

    background:
        linear-gradient(
            135deg,
            #ffffff 15%,
            #c7d2fe 48%,
            #67e8f9 100%
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero h1 span {
    display: block;

    background:
        linear-gradient(
            90deg,
            #818cf8,
            #22d3ee
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    max-width: 690px;

    margin: 28px auto 0;

    color: #94a3b8;

    font-size: 17px;
    line-height: 1.8;
}


/* ======================================================
   FEATURE PILLS
   ====================================================== */

.feature-row {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;

    margin-top: 30px;
}

.feature-pill {
    padding: 8px 14px;

    border-radius: 999px;

    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.15);

    color: #cbd5e1;

    font-size: 12px;
}


/* ======================================================
   SECTION HEADERS
   ====================================================== */

.section-label {
    margin-bottom: 12px;

    color: #818cf8;

    font-family: "JetBrains Mono", monospace;
    font-size: 12px;
    font-weight: 600;

    letter-spacing: 1px;
    text-transform: uppercase;
}

.section-title {
    margin-bottom: 25px;

    color: #f8fafc;

    font-size: 28px;
    font-weight: 700;

    letter-spacing: -1px;
}


/* ======================================================
   GLASS CARDS
   ====================================================== */

.glass-card {
    padding: 28px;

    border-radius: 24px;

    background:
        linear-gradient(
            145deg,
            rgba(30, 41, 59, 0.78),
            rgba(15, 23, 42, 0.65)
        );

    border: 1px solid rgba(148, 163, 184, 0.14);

    box-shadow:
        0 25px 80px rgba(0, 0, 0, 0.22);

    backdrop-filter: blur(20px);
}

.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-bottom: 18px;
}

.card-title {
    color: #f8fafc;

    font-size: 18px;
    font-weight: 700;
}

.step-number {
    color: #64748b;

    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
}


/* ======================================================
   UPLOAD
   ====================================================== */

.upload-heading {
    color: #e2e8f0;

    font-size: 15px;
    font-weight: 600;

    margin-bottom: 7px;
}

.upload-description {
    color: #64748b;

    font-size: 13px;
    line-height: 1.6;

    margin-bottom: 18px;
}

[data-testid="stFileUploader"] {
    width: 100%;
}

[data-testid="stFileUploaderDropzone"] {
    min-height: 190px !important;

    border: 1px dashed rgba(129, 140, 248, 0.45) !important;
    border-radius: 18px !important;

    background:
        linear-gradient(
            135deg,
            rgba(99, 102, 241, 0.07),
            rgba(6, 182, 212, 0.04)
        ) !important;

    transition: all 0.25s ease;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #818cf8 !important;

    background:
        linear-gradient(
            135deg,
            rgba(99, 102, 241, 0.13),
            rgba(6, 182, 212, 0.08)
        ) !important;
}


/* ======================================================
   IMAGE
   ====================================================== */

[data-testid="stImage"] {
    border-radius: 18px;
    overflow: hidden;

    border: 1px solid rgba(148, 163, 184, 0.15);

    box-shadow:
        0 20px 60px rgba(0, 0, 0, 0.25);
}


/* ======================================================
   BUTTONS
   ====================================================== */

.stButton > button {
    width: 100%;

    min-height: 48px;

    border-radius: 13px !important;

    border: 1px solid rgba(129, 140, 248, 0.35) !important;

    background:
        linear-gradient(
            135deg,
            #6366f1,
            #4f46e5
        ) !important;

    color: white !important;

    font-weight: 700 !important;
    font-size: 14px !important;

    box-shadow:
        0 10px 30px rgba(79, 70, 229, 0.25);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 15px 40px rgba(79, 70, 229, 0.38);
}


/* ======================================================
   RESULT
   ====================================================== */

.result-card {
    padding: 30px;

    margin-top: 18px;

    border-radius: 22px;

    background:
        linear-gradient(
            135deg,
            rgba(99, 102, 241, 0.11),
            rgba(6, 182, 212, 0.06)
        );

    border: 1px solid rgba(129, 140, 248, 0.25);
}

.result-icon {
    font-size: 28px;
    margin-bottom: 10px;
}

.result-title {
    color: #a5b4fc;

    font-family: "JetBrains Mono", monospace;
    font-size: 11px;

    text-transform: uppercase;
    letter-spacing: 1px;

    margin-bottom: 12px;
}

.result-text {
    color: #f8fafc;

    font-size: 22px;
    font-weight: 600;

    line-height: 1.55;

    letter-spacing: -0.3px;
}


/* ======================================================
   STATUS
   ====================================================== */

.status-card {
    display: flex;
    align-items: center;
    gap: 12px;

    padding: 13px 16px;

    margin-top: 18px;

    border-radius: 13px;

    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(148, 163, 184, 0.12);

    color: #94a3b8;

    font-size: 13px;
}

.status-dot {
    width: 8px;
    height: 8px;

    flex-shrink: 0;

    border-radius: 50%;

    background: #22c55e;

    box-shadow:
        0 0 12px rgba(34, 197, 94, 0.7);
}


/* ======================================================
   INFO CARDS
   ====================================================== */

.info-card {
    height: 100%;

    padding: 24px;

    border-radius: 20px;

    background: rgba(15, 23, 42, 0.62);

    border: 1px solid rgba(148, 163, 184, 0.12);

    transition:
        transform 0.2s ease,
        border-color 0.2s ease;
}

.info-card:hover {
    transform: translateY(-4px);
    border-color: rgba(129, 140, 248, 0.3);
}

.info-icon {
    font-size: 25px;
    margin-bottom: 14px;
}

.info-title {
    color: #f8fafc;

    font-size: 16px;
    font-weight: 700;

    margin-bottom: 8px;
}

.info-text {
    color: #64748b;

    font-size: 13px;
    line-height: 1.65;
}


/* ======================================================
   FOOTER
   ====================================================== */

.footer {
    text-align: center;

    margin-top: 80px;
    padding-top: 25px;

    border-top: 1px solid rgba(148, 163, 184, 0.10);

    color: #475569;

    font-size: 12px;
}

.footer strong {
    color: #818cf8;
}


/* ======================================================
   RESPONSIVE
   ====================================================== */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .navbar {
        margin-bottom: 40px;
    }

    .nav-badge {
        display: none;
    }

    .hero h1 {
        font-size: 48px;
        letter-spacing: -2px;
    }

    .hero-description {
        font-size: 15px;
    }

}

</style>
"""
)


# ============================================================
# SESSION STATE
# ============================================================

if "caption" not in st.session_state:
    st.session_state.caption = None


# ============================================================
# NAVIGATION
# ============================================================

render_html(
    """
<div class="navbar">

    <div class="brand">

        <div class="brand-icon">
            👁️
        </div>

        <div>
            VisionAI
        </div>

    </div>

    <div class="nav-badge">
        IMAGE INTELLIGENCE · AI
    </div>

</div>
"""
)


# ============================================================
# HERO
# ============================================================

render_html(
    """
<section class="hero">

    <div class="hero-label">
        ✦ Intelligent Visual Understanding
    </div>

    <h1>
        Turn images into
        <span>meaning.</span>
    </h1>

    <p class="hero-description">
        Upload an image and let AI understand what it sees.
        Generate a natural-language description and listen
        to it using built-in text-to-speech.
    </p>

    <div class="feature-row">

        <div class="feature-pill">
            🧠 AI Vision
        </div>

        <div class="feature-pill">
            ✨ Natural Captions
        </div>

        <div class="feature-pill">
            🔊 Text to Speech
        </div>

        <div class="feature-pill">
            ⚡ Local Processing
        </div>

    </div>

</section>
"""
)


# ============================================================
# MAIN WORKSPACE
# ============================================================

left_column, right_column = st.columns(
    2,
    gap="large",
)


# ============================================================
# LEFT COLUMN
# ============================================================

with left_column:

    render_html(
        """
<div class="section-label">
    WORKFLOW / 01
</div>

<div class="section-title">
    Give VisionAI something to see
</div>
"""
    )

    render_html(
        """
<div class="glass-card">

    <div class="card-header">

        <div class="card-title">
            Image Input
        </div>

        <div class="step-number">
            STEP 01
        </div>

    </div>

    <div class="upload-heading">
        Upload your image
    </div>

    <div class="upload-description">
        Give VisionAI an image to analyze.
        JPG, JPEG and PNG files are supported.
    </div>

</div>
"""
    )

    uploaded_image = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded_image is not None:

        try:

            image = load_image(uploaded_image)

            render_html(
                """
<div class="status-card">

    <span class="status-dot"></span>

    Image loaded successfully

</div>
"""
            )

            st.image(
                image,
                caption="Input image",
                use_container_width=True,
            )

            generate_button = st.button(
                "✨  Generate AI Caption",
                use_container_width=True,
            )

            if generate_button:

                with st.spinner(
                    "🧠 VisionAI is analyzing your image..."
                ):

                    try:

                        st.session_state.caption = generate_caption(
                            image
                        )

                    except Exception as error:

                        st.session_state.caption = None

                        st.error(
                            "Unable to generate the caption."
                        )

                        st.exception(error)

        except Exception as error:

            st.error(
                "Unable to open the uploaded image."
            )

            st.exception(error)

    else:

        render_html(
            """
<div class="status-card">

    <span
        class="status-dot"
        style="
            background:#64748b;
            box-shadow:none;
        "
    ></span>

    Waiting for an image

</div>
"""
        )


# ============================================================
# RIGHT COLUMN
# ============================================================

with right_column:

    render_html(
        """
<div class="section-label">
    WORKFLOW / 02
</div>

<div class="section-title">
    Let AI describe what it sees
</div>
"""
    )

    if st.session_state.caption:

        render_html(
            f"""
<div class="glass-card">

    <div class="card-header">

        <div class="card-title">
            AI Description
        </div>

        <div class="step-number">
            STEP 02
        </div>

    </div>

    <div class="result-card">

        <div class="result-icon">
            ✨
        </div>

        <div class="result-title">
            Generated Caption
        </div>

        <div class="result-text">
            {st.session_state.caption}
        </div>

    </div>

</div>
"""
        )

        render_html(
            """
<div style="height:18px"></div>
"""
        )

        if st.button(
            "🔊  Listen to Caption",
            use_container_width=True,
        ):

            with st.spinner(
                "🔊 Speaking your caption..."
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

        render_html(
            """
<div class="glass-card">

    <div class="card-header">

        <div class="card-title">
            AI Description
        </div>

        <div class="step-number">
            STEP 02
        </div>

    </div>

    <div class="result-card">

        <div class="result-icon">
            ✨
        </div>

        <div class="result-title">
            Waiting for input
        </div>

        <div class="result-text">
            Your generated caption
            will appear here.
        </div>

    </div>

</div>
"""
        )


# ============================================================
# HOW IT WORKS
# ============================================================

render_html(
    """
<div style="height:80px"></div>
"""
)

render_html(
    """
<div class="section-label">
    SYSTEM / OVERVIEW
</div>

<div class="section-title">
    From pixels to language
</div>
"""
)


info_one, info_two, info_three = st.columns(
    3,
    gap="large",
)


with info_one:

    render_html(
        """
<div class="info-card">

    <div class="info-icon">
        📤
    </div>

    <div class="info-title">
        01 · Upload
    </div>

    <div class="info-text">
        Select a JPG, JPEG or PNG image
        and provide the visual input for
        the AI captioning system.
    </div>

</div>
"""
    )


with info_two:

    render_html(
        """
<div class="info-card">

    <div class="info-icon">
        🧠
    </div>

    <div class="info-title">
        02 · Understand
    </div>

    <div class="info-text">
        The image captioning model analyzes
        the visual content and converts it
        into a meaningful natural-language
        description.
    </div>

</div>
"""
    )


with info_three:

    render_html(
        """
<div class="info-card">

    <div class="info-icon">
        🔊
    </div>

    <div class="info-title">
        03 · Listen
    </div>

    <div class="info-text">
        Use text-to-speech to hear the
        generated caption directly through
        your computer's speaker.
    </div>

</div>
"""
    )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
<div class="footer">

    <strong>VisionAI</strong>
    &nbsp;·&nbsp;
    AI Image Caption Generator
    &nbsp;·&nbsp;
    Intelligent Visual Understanding

</div>
"""
)