import os
import sys
from multiprocessing import Queue, Process
from src.streamer import Streamer
from src.detector import Detector
from src.presenter import Presenter

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found at path: {video_path}")
    else:
        raise ValueError("Missing video path. Usage: python run_pipeline.py path/to/video.mp4")

    detector_queue = Queue(maxsize=10)
    presenter_queue = Queue(maxsize=10)

    streamer = Streamer(video_path, detector_queue)
    detector = Detector(detector_queue, presenter_queue)
    presenter = Presenter(presenter_queue)

    streamer_process = Process(target=streamer.run)
    detector_process = Process(target=detector.run)
    presenter_process = Process(target=presenter.run)

    streamer_process.start()
    detector_process.start()
    presenter_process.start()

    streamer_process.join()
    detector_process.join()
    presenter_process.join()
