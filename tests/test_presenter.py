import queue
import numpy as np
from src.presenter import Presenter
from src.detector import FrameData

def create_dummy_frame(color=(0, 0, 0), size=(100, 100)):
    return np.full((size[1], size[0], 3), color, dtype=np.uint8)

def test_presenter_initialization():
    q = queue.Queue()
    presenter = Presenter(q)
    assert presenter.input_queue == q

def test_presenter_run_processes_frame(monkeypatch):
    q = queue.Queue()

    dummy_frame = create_dummy_frame()
    dummy_detections = [(10, 10, 30, 30)]
    fd = FrameData(dummy_frame, dummy_detections)
    q.put(fd)
    q.put(None)

    presenter = Presenter(q)

    monkeypatch.setattr("cv2.imshow", lambda *args, **kwargs: None)
    monkeypatch.setattr("cv2.waitKey", lambda *args, **kwargs: -1)

    presenter.run()
