# Video Analytics Pipeline

A real - time video analytics system built in a pipeline architecture consisting of three independent processes:

- **Streamer** - Extracts frames from a video file.
- **Detector** - Detects motion using OpenCV.
- **Presenter** - Displays the video frames with detection rectangles, timestamp, and blurring over detected regions.



## How to Run

1. Install dependencies:
(Make sure you’re using Python 3.8 or higher)

   ```bash
   pip3 install -r requirements.txt

2. Run the pipeline:

    ```bash
    python3 run_pipeline.py path/to/your/video.mp4

## Test the code

    ```bash
    python3 -m pytest tests/
