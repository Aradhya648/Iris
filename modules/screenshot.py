import logging
from datetime import datetime
from pathlib import Path

from platform import get_platform_handler


class ScreenshotModule:
    """Handles saving desktop screenshots locally."""

    def __init__(self, output_dir: str = "screenshots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.platform_handler = get_platform_handler()

    def capture_screenshot(self) -> Path | None:
        """Captures a desktop screenshot and returns the saved path."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = self.output_dir / f"iris_screenshot_{timestamp}.png"

        try:
            if self.platform_handler is None:
                logging.error("No supported platform handler is available.")
                return None

            self.platform_handler.capture_screenshot(screenshot_path)
            logging.info("Screenshot saved to %s", screenshot_path)
            return screenshot_path
        except FileNotFoundError:
            logging.error("Required screenshot command is not available on this platform.")
            return None
        except NotImplementedError as exc:
            logging.error(str(exc))
            return None
        except Exception as exc:
            logging.error("Failed to capture screenshot: %s", exc)
            return None
