# Volume Control with Hand Gestures

## Overview
This project is a Windows volume control application that uses hand gestures for input. It leverages the Python language and integrates the `pycaw` and `cv2` libraries to manage audio levels and process hand gesture inputs via a webcam.

## Features
- Control the system volume with hand gestures.
- Visual feedback of current volume level on-screen.
- Hand gesture recognition powered by `mediapipe` and a custom `VanzeDetector` module.

## Requirements
- Python 3.x
- OpenCV (`cv2` library)
- `mediapipe`
- `pycaw`
- `numpy`
- `comtypes`

## Installation
1. Clone the repository to your local machine.
2. Install the required packages using pip:
    ```bash
    pip install opencv-python mediapipe numpy comtypes pycaw
    ```
3. Run the main script to start the application:
    ```bash
    python volume_control.py
    ```

## Usage
Once you start the application, perform the following steps:
1. Allow the application to access your webcam.
2. Use your thumb and index finger to form a pinch gesture.
3. Move your hand closer or further away from the webcam to adjust the volume.

The volume level will be displayed on-screen, and a green bar will visually represent the current volume level.

## How It Works
The application initializes the webcam and continuously captures frames. The `VanzeDetector` hand tracking module detects the hand landmarks, and the pinch between thumb and index finger is used to adjust the volume.

Distance between thumb and index finger is calculated and converted to a volume level, which is then set using the `pycaw` library.

## Acknowledgements
- `pycaw`: https://github.com/AndreMiras/pycaw
- OpenCV: https://opencv.org/
- `mediapipe`: https://google.github.io/mediapipe/

## Author
[Your Name]

## License
This project is licensed under the [MIT License](LICENSE).

## Contributions
Contributions are welcome! Please read the [contribution guidelines](CONTRIBUTING.md) before starting any work.
