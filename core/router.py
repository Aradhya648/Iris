import logging
from core.detector import SoundEvent, detect_sound_event
from core.state import SystemState
from modules.camera import CameraModule


class EventRouter:
    """Coordinates events (like clap detection) to update system state and modules."""

    def __init__(self, state: SystemState, camera_module: CameraModule):
        self.state = state
        self.camera_module = camera_module
        self.event_handlers = {
            SoundEvent.CLAP: self._handle_clap_event,
        }

    def _handle_clap_event(self) -> None:
        """Handles the current clap event behavior."""
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

    def process_sound_event(self, data: bytes) -> None:
        """Detects a sound event and routes it to the matching handler."""
        event = detect_sound_event(data)
        if event is None:
            return

        handler = self.event_handlers.get(event)
        if handler is None:
            logging.info("No handler registered for sound event: %s", event)
            return

        handler()

    def process_loop_cycle(self, audio_data: bytes) -> None:
        """The main event processing routine for one cycle."""
        # 1. Handle Audio Input / Sound Events (Event Trigger)
        self.process_sound_event(audio_data)

        # 2. Read and Display Camera Frame (Module Operation)
        if self.camera_module.is_active:
            self.camera_module.read_frame()
