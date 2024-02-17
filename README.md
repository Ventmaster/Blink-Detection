# Blink Detection using Face Landmarks

This Python script uses OpenCV and cvzone libraries to detect blinking using facial landmarks.

## Requirements

- Python 3.x
- OpenCV
- cvzone

Install the required libraries using pip: pip install opencv-python cvzone


## Usage

1. Run the `main.py` script.
2. Face your webcam.
3. Blink your eyes to see the blinking count on the screen.

## Code Overview

- The script captures video from the default camera using OpenCV.
- It uses the FaceMeshDetector class from cvzone to detect facial landmarks.
- The vertical-to-horizontal eye opening ratio is calculated based on specific facial landmark points.
- A LivePlot object from cvzone is used to plot the ratio over time.
- The script counts the number of blinks detected based on the ratio.

## Acknowledgements

- This script is based on the cvzone library developed by `@cvzone`.
