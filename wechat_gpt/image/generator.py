from __future__ import annotations
from ..llm.siliconflow_client import SiliconFlowClient


def generate_image(client: SiliconFlowClient, prompt: str, negative_prompt: str | None = None) -> bytes:
    """Generate an image based on the given prompt."""
    return client.generate_image(prompt, negative_prompt)
