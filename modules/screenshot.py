import logging
import subprocess
from datetime import datetime
from pathlib import Path


class ScreenshotModule:
    """Handles saving desktop screenshots locally."""

    def __init__(self, output_dir: str = "screenshots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def capture_screenshot(self) -> Path | None:
        """Captures a desktop screenshot and returns the saved path."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = self.output_dir / f"iris_screenshot_{timestamp}.png"

        try:
            subprocess.run(
                ["screencapture", str(screenshot_path)],
                check=True,
                capture_output=True,
                text=True,
            )
            logging.info("Screenshot saved to %s", screenshot_path)
            return screenshot_path
        except FileNotFoundError:
            logging.error("screencapture command is not available on this platform.")
            return None
        except subprocess.CalledProcessError as exc:
            logging.error("Failed to capture screenshot: %s", exc.stderr.strip())
            return None
