import logging
from core.detector import detect_clap
from core.state import SystemState
from modules.camera import CameraModule


class EventRouter:
    """Coordinates events (like clap detection) to update system state and modules."""

    def __init__(self, state: SystemState, camera_module: CameraModule):
        self.state = state
        self.camera_module = camera_module

    def process_clap(self, data: bytes) -> None:
        """Processes detected audio chunk for a clap event."""
        if detect_clap(data):
            self.state.update_clap_event()

            if not self.camera_module.is_active:
                logging.info("Clap received and camera is OFF. Attempting to open camera.")
                if self.camera_module.open_camera():
                    # Keep SystemState in sync with the actual camera state.
                    self.state.set_camera_state(True)

    def handle_timeout(self) -> None:
        """Checks system state for timeouts and closes the camera if necessary."""
        active, needs_closing = self.state.check_camera_status()

        if active and needs_closing:
            logging.warning("Camera timed out due to inactivity.")
            self.camera_module.close_camera()
            self.state.set_camera_state(False)

    def process_loop_cycle(self, audio_data: bytes) -> None:
        """The main event processing routine for one cycle."""
        # 1. Handle Audio Input / Claps (Event Trigger)
        self.process_clap(audio_data)

        # 2. Handle State Logic (Timeout Check)
        self.handle_timeout()

        # 3. Read and Display Camera Frame (Module Operation)
        if self.camera_module.is_active:
            self.camera_module.read_frame()
