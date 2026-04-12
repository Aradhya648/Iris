import time
import logging


class SystemState:
    """Manages the overall system state, including camera status and timeouts."""

    def __init__(self, timeout_seconds: int):
        self.camera_active = False
        self.last_clap_time = None
        self.CAMERA_TIMEOUT = timeout_seconds

    def update_clap_event(self) -> None:
        """Resets the timer upon detecting a clap."""
        self.last_clap_time = time.time()
        logging.info("Clap detected. Resetting camera activity timer.")

    def check_camera_status(self) -> tuple[bool, bool]:
        """
        Checks if the system requires the camera to be closed due to timeout.
        Returns: (is_active, needs_closing)
        """
        if self.last_clap_time is None:
            return self.camera_active, False

        elapsed = time.time() - self.last_clap_time
        needs_closing = elapsed > self.CAMERA_TIMEOUT
        return self.camera_active, needs_closing

    def set_camera_state(self, active: bool) -> None:
        """Sets the camera's operational state."""
        self.camera_active = active

    def reset_state(self):
        """Resets all tracked state variables."""
        self.camera_active = False
        self.last_clap_time = None
