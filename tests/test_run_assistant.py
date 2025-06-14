import sys
from pathlib import Path
from unittest.mock import patch

import scripts.run_assistant as ra


def test_run_assistant_stt(tmp_path, capsys):
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"bytes")
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
api:
  token: T
  base_url: https://example.com
models:
  chat: chat
  stt: stt
  tts: tts
  image: img
params:
  temperature: 0.1
  top_p: 0.2
  top_k: 5
  max_tokens: 16
"""
    )

    with patch.object(sys, "argv", ["run_assistant.py", "--config", str(cfg), "--stt", str(audio)]), \
         patch("scripts.run_assistant.SiliconFlowClient") as Client, \
         patch("wechat_gpt.voice.speech_to_text.speech_to_text", return_value="hi") as stt:
        instance = Client.return_value
        instance.chat.return_value = "ok"
        ra.main()
        out, _ = capsys.readouterr()
        assert "Assistant: ok" in out
        stt.assert_called_once()
        instance.chat.assert_called_once_with([{"role": "user", "content": "hi"}])


def test_run_assistant_wechat(tmp_path, capsys):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
api:
  token: T
  base_url: https://example.com
models:
  chat: chat
  stt: stt
  tts: tts
  image: img
params:
  temperature: 0.1
  top_p: 0.2
  top_k: 5
  max_tokens: 16
"""
    )

    with patch.object(sys, "argv", ["run_assistant.py", "--config", str(cfg), "--wechat", "hi"]), \
         patch("scripts.run_assistant.SiliconFlowClient") as Client, \
         patch("wechat_gpt.wechat.client.send_message") as send:
        instance = Client.return_value
        instance.chat.return_value = "ok"
        ra.main()
        out, _ = capsys.readouterr()
        assert "Assistant: ok" in out
        send.assert_called_once_with("ok")
        instance.chat.assert_called_once_with([{"role": "user", "content": "hi"}])


def test_run_assistant_tts(tmp_path, capsys):
    output = tmp_path / "speech.wav"
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
api:
  token: T
  base_url: https://example.com
models:
  chat: chat
  stt: stt
  tts: tts
  image: img
params:
  temperature: 0.1
  top_p: 0.2
  top_k: 5
  max_tokens: 16
"""
    )

    with patch.object(sys, "argv", ["run_assistant.py", "--config", str(cfg), "--tts", str(output), "hi"]), \
         patch("scripts.run_assistant.SiliconFlowClient") as Client, \
         patch("wechat_gpt.voice.text_to_speech.text_to_speech", return_value=b"audio") as tts:
        instance = Client.return_value
        instance.chat.return_value = "ok"
        ra.main()
        out, _ = capsys.readouterr()
        assert "Assistant: ok" in out
        tts.assert_called_once_with(instance, "ok")
        assert output.read_bytes() == b"audio"
        instance.chat.assert_called_once_with([{"role": "user", "content": "hi"}])
