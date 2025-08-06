import queue
from src.streamer import Streamer

def test_streamer_initialization():
    streamer = Streamer("dummy_path.mp4", queue.Queue())
    assert streamer.video_path == "dummy_path.mp4"

def test_streamer_run_puts_frames(monkeypatch):
    output_queue = queue.Queue()
    frames = [b"frame1", b"frame2", None]

    def fake_read():
        if frames:
            return True, frames.pop(0)
        return False, None

    class DummyCap:
        def __init__(self):
            self.opened = True
        def isOpened(self):
            return self.opened and bool(frames)
        def read(self):
            return fake_read()
        def release(self):
            self.opened = False
        def get(self, prop):
            return 30.0

    monkeypatch.setattr("cv2.VideoCapture", lambda path: DummyCap())

    streamer = Streamer("dummy.mp4", output_queue)
    streamer.run()

    results = []
    while not output_queue.empty():
        results.append(output_queue.get())

    assert results[-1] is None
    assert b"frame1" in results or b"frame2" in results
