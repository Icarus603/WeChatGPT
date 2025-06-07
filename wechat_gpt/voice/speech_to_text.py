from __future__ import annotations
from ..llm.siliconflow_client import SiliconFlowClient


def speech_to_text(client: SiliconFlowClient, audio_bytes: bytes) -> str:
    """Convert audio bytes to text using SiliconFlow."""
    return client.speech_to_text(audio_bytes)
