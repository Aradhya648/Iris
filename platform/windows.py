from pathlib import Path


class WindowsPlatform:
    """Windows-specific system actions."""

    def capture_screenshot(self, output_path: Path) -> str:
        """Placeholder for future Windows screenshot support."""
        raise NotImplementedError(
            f"Screenshot capture is not implemented yet for Windows: {output_path}"
        )
