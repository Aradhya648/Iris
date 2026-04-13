import logging
import time


class SystemState:
    """Manages camera state and shared timing helpers."""

    def __init__(self, debounce_seconds: float):
        self.camera_active = False
        self.clap_debounce_seconds = debounce_seconds

    def toggle_camera_state(self) -> bool:
        """Toggles the desired camera state and returns the new state."""
        self.camera_active = not self.camera_active
        logging.info("Clap accepted. Camera target state is now %s.", self.camera_active)
        return self.camera_active

    def current_time(self) -> float:
        """Returns a monotonic timestamp for clap sequencing logic."""
        return time.monotonic()

    def set_camera_state(self, active: bool) -> None:
        """Sets the camera's operational state."""
        self.camera_active = active

    def reset_state(self) -> None:
        """Resets all tracked state variables."""
        self.camera_active = False
