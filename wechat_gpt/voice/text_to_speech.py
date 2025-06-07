from __future__ import annotations
from ..llm.siliconflow_client import SiliconFlowClient


def text_to_speech(client: SiliconFlowClient, text: str) -> bytes:
    """Generate speech audio for the given text."""
    return client.text_to_speech(text)
