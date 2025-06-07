"""WeChat Desktop interaction via AppleScript and ClickClick.

This is a simplified placeholder implementation. Real interaction requires the
`ClickClick` command line tool and accessibility permissions on macOS.
"""
from __future__ import annotations

import subprocess
from ..util.logger import get_logger

logger = get_logger(__name__)


def send_message(text: str) -> None:
    """Send a message to the active WeChat conversation using ClickClick."""
    script = f'tell application "System Events" to keystroke {text!r} & return'
    try:
        subprocess.run(["osascript", "-e", script], check=True)
    except FileNotFoundError:
        logger.error("osascript not found. This script must run on macOS.")


def get_latest_message() -> str:
    """Placeholder for retrieving the latest message from WeChat."""
    logger.warning("get_latest_message is not implemented. Returning empty string.")
    return ""
