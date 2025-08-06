import cv2
import time

class Streamer:
    def __init__(self, video_path, output_queue):
        self.video_path = video_path
        self.output_queue = output_queue

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            self.output_queue.put(frame)
            time.sleep(1 / cap.get(cv2.CAP_PROP_FPS))
        cap.release()
        self.output_queue.put(None)
