from __future__ import annotations

import requests
from typing import Iterable
from ..config import Config
from ..util.logger import get_logger

logger = get_logger(__name__)


class SiliconFlowClient:
    def __init__(self, config: Config):
        self.config = config
        self.base_url = config.api.base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {config.api.token}",
            "Content-Type": "application/json",
        }

    def chat(self, messages: Iterable[dict]) -> str:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.config.models.chat,
            "messages": list(messages),
            "stream": False,
            "max_tokens": self.config.params.max_tokens,
            "temperature": self.config.params.temperature,
            "top_p": self.config.params.top_p,
            "top_k": self.config.params.top_k,
            "n": 1,
            "response_format": {"type": "text"},
        }
        resp = requests.post(url, json=payload, headers=self.headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        logger.debug("Chat response: %s", data)
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")

    def speech_to_text(self, audio_bytes: bytes) -> str:
        url = f"{self.base_url}/audio/transcriptions"
        files = {
            "file": ("audio.wav", audio_bytes, "audio/wav"),
            "model": (None, self.config.models.stt),
        }
        headers = {"Authorization": f"Bearer {self.config.api.token}"}
        resp = requests.post(url, files=files, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        logger.debug("STT response: %s", data)
        return data.get("text", "")

    def text_to_speech(self, text: str) -> bytes:
        url = f"{self.base_url}/audio/speech"
        payload = {
            "model": self.config.models.tts,
            "input": text,
            "voice": f"{self.config.models.tts}:alex",
            "response_format": "mp3",
            "sample_rate": 32000,
            "stream": False,
            "speed": 1,
            "gain": 0,
        }
        resp = requests.post(url, json=payload, headers=self.headers, timeout=60)
        resp.raise_for_status()
        logger.debug("TTS status code: %s", resp.status_code)
        return resp.content

    def generate_image(self, prompt: str, negative_prompt: str | None = None) -> bytes:
        url = f"{self.base_url}/images/generations"
        payload = {
            "model": self.config.models.image,
            "prompt": prompt,
            "negative_prompt": negative_prompt or "",
            "image_size": "1024x1024",
            "batch_size": 1,
            "num_inference_steps": 20,
            "guidance_scale": 7.5,
        }
        resp = requests.post(url, json=payload, headers=self.headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        logger.debug("Image response: %s", data)
        if data.get("data"):
            # SiliconFlow returns base64 strings in 'data'
            import base64

            return base64.b64decode(data["data"][0]["b64_json"])
        return b""
