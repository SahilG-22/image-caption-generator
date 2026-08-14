from unittest.mock import patch

from src.utils.text_to_speech import speak_text


def test_speak_text_with_empty_text():
    result = speak_text("")

    assert result is None


@patch("src.utils.text_to_speech.pyttsx3.init")
def test_speak_text(mock_init):
    mock_engine = mock_init.return_value

    speak_text("A dog is playing in a park.")

    mock_init.assert_called_once()
    mock_engine.say.assert_called_once_with("A dog is playing in a park.")
    mock_engine.runAndWait.assert_called_once()