
# Gesture Control Photo App

Gesture Control Photo App is a Python application that enables users to capture photos and apply filters using simple hand gestures detected via webcam. It uses OpenCV and MediaPipe for real-time hand tracking and gesture recognition.

---

## Features

- **Real-time hand gesture detection** using MediaPipe
- **Capture photos** with a pinch gesture (thumb and index finger tips together)
- **Apply live filters** (Grayscale, Sepia, Negative, Blur) by touching thumb to middle, ring, or pinky finger
- **Debounce logic** to prevent accidental multiple actions
- **Visual feedback** on the webcam window

---

## How It Works

1. **Hand Tracking:** The app uses MediaPipe to detect hand landmarks in real time from your webcam feed.
2. **Gesture Recognition:**
   - **Photo Capture:** Touch your thumb and index finger tips together (pinch gesture) to capture a photo.
   - **Filter Change:** Touch your thumb to the tip of your middle, ring, or pinky finger to cycle through available filters.
3. **Photo Saving:** Captured photos are saved as `picture_<timestamp>.jpg` in the project directory.
4. **Exit:** Press `q` to quit the application.

---

## Requirements

- Python 3.7+
- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)
- NumPy (`numpy`)

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## Usage

1. **Clone or download this repository.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   python main.py
   ```
4. **Control the app with gestures:**
   - **Pinch (thumb + index):** Capture a photo
   - **Thumb + middle/ring/pinky:** Change filter
   - **Press `q`:** Quit

---

## Gesture Reference

| Gesture                        | Action             |
|--------------------------------|--------------------|
| Thumb + Index (Pinch)          | Capture Photo      |
| Thumb + Middle/Ring/Pinky      | Change Filter      |
| Press `q` on keyboard          | Quit Application   |

---

## Troubleshooting

- **Webcam not detected:** Ensure your webcam is connected and not used by another application.
- **No hand detected:** Make sure your hand is visible and well-lit in the webcam frame.
- **Dependencies error:** Double-check you have installed all required packages.

---

## Project Structure

- `main.py` — Main application file
- `requirements.txt` — Python dependencies
- `README.md` — Project documentation

---

## Credits

- Built with [OpenCV](https://opencv.org/) and [MediaPipe](https://mediapipe.dev/)
- Educational project for learning gesture-based computer vision

---

## License

This project is for educational purposes only.
