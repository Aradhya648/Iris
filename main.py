import pyaudio
import cv2
import numpy as np
import time
import logging

# ---------- CONFIG ----------
SAMPLE_RATE = 44100
CHUNK = 1024
CLAP_THRESHOLD = 7000
CAMERA_TIMEOUT = 5
# ----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

p = pyaudio.PyAudio()

stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=CHUNK
)

camera = None
last_clap_time = None
camera_active = False


def detect_clap(data):
    audio = np.frombuffer(data, dtype=np.int16)
    peak = np.max(np.abs(audio))
    return peak > CLAP_THRESHOLD


def open_camera():
    global camera, camera_active
    if not camera_active:
        camera = cv2.VideoCapture(0)
        camera_active = True
        logging.info("Camera ON")


def close_camera():
    global camera, camera_active
    if camera_active:
        camera.release()
        camera_active = False
        logging.info("Camera OFF")


print("Listening for clap... Ctrl+C to stop")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)

        if detect_clap(data):
            last_clap_time = time.time()
            if not camera_active:
                open_camera()

        if camera_active:
            ret, frame = camera.read()
            if ret:
                cv2.imshow("Camera", frame)

            if last_clap_time and (time.time() - last_clap_time > CAMERA_TIMEOUT):
                close_camera()
                cv2.destroyAllWindows()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

finally:
    close_camera()
    stream.stop_stream()
    stream.close()
    p.terminate()
    cv2.destroyAllWindows()
