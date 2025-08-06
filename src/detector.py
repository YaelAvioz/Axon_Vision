import cv2

class FrameData:
    def __init__(self, frame, detections):
        self.frame = frame
        self.detections = detections

class Detector:
    def __init__(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.fgbg = None

    def detect_motion(self, frame):
        fgmask = self.fgbg.apply(frame)
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detections = []
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            detections.append((x, y, w, h))
        return detections

    def run(self):
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        while True:
            frame = self.input_queue.get()
            if frame is None:
                self.output_queue.put(None)
                break
            detections = self.detect_motion(frame)
            self.output_queue.put(FrameData(frame, detections))
