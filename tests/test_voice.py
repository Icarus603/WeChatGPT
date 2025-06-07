from unittest.mock import Mock
from wechat_gpt.voice.speech_to_text import speech_to_text
from wechat_gpt.voice.text_to_speech import text_to_speech


def test_speech_to_text():
    client = Mock()
    client.speech_to_text.return_value = "hello"
    result = speech_to_text(client, b"bytes")
    assert result == "hello"
    client.speech_to_text.assert_called_once_with(b"bytes")


def test_text_to_speech():
    client = Mock()
    client.text_to_speech.return_value = b"audio"
    result = text_to_speech(client, "hi")
    assert result == b"audio"
    client.text_to_speech.assert_called_once_with("hi")
