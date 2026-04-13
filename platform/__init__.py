import sys

from .mac import MacPlatform
from .windows import WindowsPlatform


def get_platform_handler():
    """Returns the platform handler for the current operating system."""
    if sys.platform == "darwin":
        return MacPlatform()

    if sys.platform.startswith("win"):
        return WindowsPlatform()

    return None
