import pytest
from unittest.mock import patch
from wechat_gpt.config import Config, APIConfig, ModelConfig, ParamsConfig
from wechat_gpt.llm.siliconflow_client import SiliconFlowClient


@pytest.fixture
def client():
    config = Config(
        api=APIConfig(token="T", base_url="https://example.com"),
        models=ModelConfig(chat="chat", stt="stt", tts="tts", image="image"),
        params=ParamsConfig(temperature=0.1, top_p=0.2, top_k=5, max_tokens=16),
    )
    return SiliconFlowClient(config)


def test_chat(client):
    with patch("requests.post") as post:
        post.return_value.json.return_value = {
            "choices": [{"message": {"content": "hi"}}]
        }
        post.return_value.status_code = 200
        post.return_value.raise_for_status = lambda: None
        reply = client.chat([{"role": "user", "content": "hi"}])
        assert reply == "hi"
        post.assert_called_once()
