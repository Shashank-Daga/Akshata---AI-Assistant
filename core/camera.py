import cv2
import os
import time
import threading
from datetime import datetime

SAVE_DIR = os.path.join("data", "photos")
os.makedirs(SAVE_DIR, exist_ok=True)

# Flag to stop time-lapse
stop_lapse = False


def take_photo(filename=None):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        return "Could not access the camera."

    ret, frame = cam.read()
    cam.release()

    if not ret:
        return "Failed to capture the image."

    if not filename:
        filename = f"photo_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    else:
        filename = filename if filename.endswith(".jpg") else filename + ".jpg"

    full_path = os.path.join(SAVE_DIR, filename)

    try:
        cv2.imwrite(full_path, frame)
        return f"Photo captured and saved as {filename}."
    except Exception as e:
        return f"Failed to save image: {e}"


def start_webcam():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        return "Could not access the webcam."

    cv2.namedWindow("Webcam - Press 'q' to exit.")

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow("Webcam - Press 'q' to exit.", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    return "Webcam closed."


# 📸 Time-lapse logic
def start_time_lapse(interval_sec, duration_sec):
    global stop_lapse

    def lapse_worker():
        start_time = time.time()
        count = 1
        while not stop_lapse and (time.time() - start_time) < duration_sec:
            filename = f"timelapse_{count}_{datetime.now().strftime('%H-%M-%S')}.jpg"
            result = take_photo(filename)
            print(result)
            count += 1
            time.sleep(interval_sec)

    stop_lapse = False
    thread = threading.Thread(target=lapse_worker, daemon=True)
    thread.start()
    return f"Started time-lapse: every {interval_sec} seconds for {duration_sec} seconds."


def stop_time_lapse():
    global stop_lapse
    stop_lapse = True
    return "Time-lapse stopped."
