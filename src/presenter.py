import cv2
from datetime import datetime

class Presenter:
    def __init__(self, input_queue):
        self.input_queue = input_queue

    def run(self):
        while True:
            item = self.input_queue.get()
            if item is None:
                break

            frame = item.frame.copy()
            detections = item.detections

            # Blur detections
            for (x, y, w, h) in detections:
                roi = frame[y:y+h, x:x+w]
                if roi.size == 0:
                    continue
                blurred = cv2.GaussianBlur(roi, (21, 21), 0)
                frame[y:y+h, x:x+w] = blurred

            # Timestamp
            timestamp = datetime.now().strftime('%H:%M:%S')
            cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2)

            # Draw rectangles
            for (x, y, w, h) in detections:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
