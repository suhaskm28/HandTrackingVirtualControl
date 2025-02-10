# Hand Tracking Virtual Control

## Overview
This project implements a real-time hand-tracking application that allows users to control computer functions using hand gestures. It leverages **OpenCV** for video processing, **MediaPipe** for hand landmark detection, and **PyAutoGUI** for simulating system interactions such as mouse control, volume adjustments, and finger counting.

## Features
- **Finger Counting:** Detects and displays the number of fingers shown.
- **Volume Control:** Adjusts system volume and media playback based on hand gestures.
- **Mouse Control:** Moves the cursor and simulates clicks using hand movements.

## Technologies Used
- **Python**
- **OpenCV** (for real-time video processing)
- **MediaPipe** (for hand tracking and gesture recognition)
- **PyAutoGUI** (for automating system interactions)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/hand-tracking-virtual-control.git
   cd hand-tracking-virtual-control
   ```
2. Install dependencies:
   ```sh
   pip install opencv-python mediapipe pyautogui numpy
   ```

## Usage
1. Run the main script:
   ```sh
   python HandTrackingVirtualControl.py
   ```
2. Ensure your webcam is enabled.
3. Use the following controls:
   - Press `1` for Finger Counting mode.
   - Press `2` for Volume Control mode.
   - Press `3` for Mouse Control mode.
   - Press `q` to exit.

## How It Works
1. **Hand Detection:** The system captures video frames and detects hand landmarks using MediaPipe.
2. **Gesture Recognition:** The application analyzes finger positions to determine gestures.
3. **Action Execution:** Based on recognized gestures, the system simulates cursor movement, volume control, and other interactions.

## Future Enhancements
- Improved accuracy and gesture recognition.
- Additional functionalities like scrolling and window navigation.
- Better handling of different lighting conditions and hand orientations.

## Contributors
- [Your Name](https://github.com/your-username)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
