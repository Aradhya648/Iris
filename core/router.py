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
            if not self.state.should_process_clap():
                return

            should_enable_camera = self.state.toggle_camera_state()

            if should_enable_camera:
                logging.info("Clap received and camera is OFF. Attempting to open camera.")
                if not self.camera_module.open_camera():
                    logging.error("Camera failed to open. Reverting toggle state.")
                    self.state.set_camera_state(False)
            else:
                logging.info("Clap received and camera is ON. Closing camera.")
                self.camera_module.close_camera()
                self.state.set_camera_state(False)

    def process_loop_cycle(self, audio_data: bytes) -> None:
        """The main event processing routine for one cycle."""
        # 1. Handle Audio Input / Claps (Event Trigger)
        self.process_clap(audio_data)

        # 2. Read and Display Camera Frame (Module Operation)
        if self.camera_module.is_active:
            self.camera_module.read_frame()
