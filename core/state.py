import logging
import time


class SystemState:
    """Manages camera toggle state and clap debounce tracking."""

    def __init__(self, debounce_seconds: float):
        self.camera_active = False
        self.last_clap_time = None
        self.clap_debounce_seconds = debounce_seconds

    def should_process_clap(self) -> bool:
        """Returns True only when the clap falls outside the debounce window."""
        current_time = time.monotonic()

        if self.last_clap_time is not None:
            elapsed = current_time - self.last_clap_time
            if elapsed < self.clap_debounce_seconds:
                logging.info("Clap ignored during debounce window.")
                return False

        self.last_clap_time = current_time
        return True

    def toggle_camera_state(self) -> bool:
        """Toggles the desired camera state and returns the new state."""
        self.camera_active = not self.camera_active
        logging.info("Clap accepted. Camera target state is now %s.", self.camera_active)
        return self.camera_active

    def set_camera_state(self, active: bool) -> None:
        """Sets the camera's operational state."""
        self.camera_active = active

    def reset_state(self) -> None:
        """Resets all tracked state variables."""
        self.camera_active = False
        self.last_clap_time = None
