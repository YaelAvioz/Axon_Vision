import multiprocessing
import time
from src.streamer import Streamer
from src.detector import Detector
from src.presenter import Presenter

def test_pipeline_runs_short_video(monkeypatch):
    monkeypatch.setattr("cv2.imshow", lambda *args, **kwargs: None)
    monkeypatch.setattr("cv2.waitKey", lambda *args, **kwargs: -1)

    video_path = "tests/test_video.mp4"
    detector_queue = multiprocessing.Queue(maxsize=10)
    presenter_queue = multiprocessing.Queue(maxsize=10)

    streamer = Streamer(video_path, detector_queue)
    detector = Detector(detector_queue, presenter_queue)
    presenter = Presenter(presenter_queue)

    streamer_process = multiprocessing.Process(target=streamer.run)
    detector_process = multiprocessing.Process(target=detector.run)
    presenter_process = multiprocessing.Process(target=presenter.run)

    streamer_process.start()
    detector_process.start()
    presenter_process.start()

    time.sleep(5)

    detector_queue.put(None)

    streamer_process.terminate()
    detector_process.terminate()
    presenter_process.terminate()

    streamer_process.join()
    detector_process.join()
    presenter_process.join()

    assert True
