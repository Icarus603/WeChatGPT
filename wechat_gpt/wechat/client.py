"""WeChat Desktop interaction via ClickClick.

This module provides minimal wrappers around the `ClickClick` command line tool
which is required for controlling the macOS WeChat client.  The implementation
here intentionally remains small and focuses on sending messages.  Retrieving
messages would require more extensive scripting and is left as future work.
"""
from __future__ import annotations

import subprocess
from ..util.logger import get_logger

logger = get_logger(__name__)


def send_message(text: str) -> None:
    """Send ``text`` to the active WeChat conversation using ClickClick."""
    try:
        subprocess.run(["clickclick", "type", text], check=True)
        subprocess.run(["clickclick", "key", "return"], check=True)
    except FileNotFoundError:
        logger.error(
            "ClickClick not found. Install it from https://github.com/anyshortcut/ClickClick"
        )


def get_latest_message() -> str:
    """Placeholder for retrieving the latest message from WeChat."""
    logger.warning(
        "get_latest_message is not implemented. This requires more complex ClickClick scripting."
    )
    return ""
