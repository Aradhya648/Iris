import numpy as np
import logging
import pyaudio

# Configuration Constants
SAMPLE_RATE = 44100
CHUNK = 1024
CLAP_THRESHOLD = 7000  # Threshold for clap detection (device-dependent; tune as needed)


def detect_clap(data: bytes) -> bool:
    """Analyzes audio data to determine if a clap sound occurred."""
    try:
        audio = np.frombuffer(data, dtype=np.int16)
        peak = np.max(np.abs(audio))
        return peak > CLAP_THRESHOLD
    except Exception as e:
        logging.error(f"Error during clap detection: {e}")
        return False


class AudioStreamHandler:
    """Handles the PyAudio stream resource."""

    def __init__(self):
        self._p = None
        self._stream = None

    def initialize_stream(self) -> bool:
        """Initializes and opens the audio input stream."""
        try:
            self._p = pyaudio.PyAudio()
            self._stream = self._p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK,
            )
            logging.info("Audio Stream Initialized.")
            return True
        except Exception as e:
            logging.error(f"Failed to initialize audio stream: {e}")
            return False

    def read_data(self) -> bytes | None:
        """Reads a chunk of audio data."""
        if self._stream is None:
            logging.error("Stream not initialized.")
            return None
        try:
            return self._stream.read(CHUNK, exception_on_overflow=False)
        except IOError as e:
            logging.warning(f"IOError during stream read (Overflow): {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during stream read: {e}")
            return None

    def close(self):
        """Closes and cleans up the audio resources."""
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
        if self._p:
            self._p.terminate()
        logging.info("Audio Stream Closed.")
