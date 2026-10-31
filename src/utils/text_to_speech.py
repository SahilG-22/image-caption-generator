
from gtts import gTTS
from io import BytesIO


def speak_text(text):
    """
    Convert text into speech and return MP3 audio bytes.

    Args:
        text (str): Text that should be spoken.

    Returns:
        BytesIO: Generated audio data.
    """
    if not text:
        return None

    audio_buffer = BytesIO()

    tts = gTTS(text=text, lang="en")
    tts.write_to_fp(audio_buffer)

    audio_buffer.seek(0)

    return audio_buffer
