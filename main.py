import time
import logging
import cv2

from core.detector import AudioStreamHandler
from core.state import SystemState
from modules.camera import CameraModule
from modules.screenshot import ScreenshotModule
from core.router import EventRouter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main_orchestrator():
    """Main function to initialize resources and run the detection loop."""
    print("Listening for clap... Ctrl+C to stop")

    audio_handler = AudioStreamHandler()
    if not audio_handler.initialize_stream():
        logging.critical("Exiting due to failure in audio initialization.")
        return

    camera_module = CameraModule()
    screenshot_module = ScreenshotModule()

    try:
        state = SystemState(debounce_seconds=0.3)
        router = EventRouter(
            state=state,
            camera_module=camera_module,
            screenshot_module=screenshot_module,
        )

        while True:
            audio_data = audio_handler.read_data()

            if audio_data is None:
                time.sleep(0.01)
                continue

            router.process_loop_cycle(audio_data)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    except KeyboardInterrupt:
        pass

    finally:
        camera_module.close_camera()
        audio_handler.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main_orchestrator()
