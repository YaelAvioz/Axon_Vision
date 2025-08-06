import queue
import numpy as np
import cv2
from src.detector import Detector

def create_dummy_frame(color=(0, 0, 0), size=(100, 100)):
    frame = np.full((size[1], size[0], 3), color, dtype=np.uint8)
    return frame

def test_detector_initialization():
    detector = Detector(queue.Queue(), queue.Queue())
    assert detector.input_queue is not None
    assert detector.output_queue is not None
    assert detector.fgbg is None

def test_detect_motion_no_motion():
    detector = Detector(queue.Queue(), queue.Queue())
    detector.fgbg = cv2.createBackgroundSubtractorMOG2()

    black_frame = create_dummy_frame(color=(0,0,0))

    detector.fgbg.apply(black_frame)

    detections = detector.detect_motion(black_frame)
    assert detections == [], "Expected no detections on static black frame"

def test_detect_motion_detects_something():
    detector = Detector(queue.Queue(), queue.Queue())
    detector.fgbg = cv2.createBackgroundSubtractorMOG2()

    black_frame = create_dummy_frame(color=(0,0,0))
    white_frame = create_dummy_frame(color=(255,255,255))

    detector.fgbg.apply(black_frame)

    detections = detector.detect_motion(white_frame)
    assert isinstance(detections, list)
    assert all(isinstance(d, tuple) and len(d) == 4 for d in detections)
    assert len(detections) > 0
