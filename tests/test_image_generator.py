from unittest.mock import Mock
from wechat_gpt.image.generator import generate_image


def test_generate_image():
    client = Mock()
    client.generate_image.return_value = b"img"
    result = generate_image(client, "prompt")
    assert result == b"img"
    client.generate_image.assert_called_once_with("prompt", None)
