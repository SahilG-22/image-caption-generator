import pyttsx3


def speak_text(text):
    """
    Convert text into speech.

    Args:
        text (str): Text that should be spoken.
    """
    if not text:
        return

    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()