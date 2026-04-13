import subprocess
from pathlib import Path


class MacPlatform:
    """macOS-specific system actions."""

    def capture_screenshot(self, output_path: Path) -> str:
        """Captures a desktop screenshot using the native macOS utility."""
        result = subprocess.run(
            ["screencapture", str(output_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stderr.strip()
