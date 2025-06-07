from unittest.mock import patch
from wechat_gpt.wechat.client import send_message


def test_send_message():
    with patch("subprocess.run") as run:
        send_message("hi")
        assert run.call_count == 2
