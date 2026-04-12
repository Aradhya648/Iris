import cv2
import numpy as np
import logging
from typing import Tuple, Optional


class CameraModule:
    """Handles the OpenCV camera lifecycle (open, read, close)."""

    def __init__(self):
        self.camera = None
        self._is_active = False
        logging.info("Camera module initialized.")

    @property
    def is_active(self) -> bool:
        return self._is_active

    def open_camera(self) -> bool:
        """Initializes the OpenCV camera stream."""
        if self._is_active:
            return True
        try:
            self.camera = cv2.VideoCapture(0)
            if self.camera.isOpened():
                self._is_active = True
                logging.info("Camera ON")
                return True
            else:
                logging.error("Could not open camera.")
                return False
        except Exception as e:
            logging.error(f"Error opening camera: {e}")
            return False

    def close_camera(self):
        """Releases the OpenCV camera resources."""
        if self._is_active:
            try:
                self.camera.release()
                cv2.destroyAllWindows()
                self._is_active = False
                logging.info("Camera OFF")
            except Exception as e:
                logging.error(f"Error closing camera resources: {e}")

    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Reads the latest frame from the camera and displays it."""
        if not self._is_active:
            return False, None

        ret, frame = self.camera.read()

        if ret and frame is not None:
            cv2.imshow("Camera", frame)

        return ret, frame
