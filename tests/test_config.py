from pathlib import Path
from wechat_gpt.config import load_config

def test_load_config(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
api:
  token: TOKEN
  base_url: https://example.com
models:
  chat: a
  stt: b
  tts: c
  image: d
params:
  temperature: 0.1
  top_p: 0.2
  top_k: 5
  max_tokens: 128
"""
    )
    config = load_config(cfg)
    assert config.api.token == "TOKEN"
    assert config.models.chat == "a"
    assert config.params.max_tokens == 128
