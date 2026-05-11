# AI Powered Gesture Controlled Presentation System

A Computer Vision based presentation controller built using Python, OpenCV, MediaPipe, and PyAutoGUI.

This project allows users to control PowerPoint presentations using real-time hand gestures captured through a webcam.

---

# Features

- Real-time hand tracking
- Gesture-based slide navigation
- Touchless presentation control
- Pointer mode using index finger
- Pinch gesture detection
- OpenCV visual feedback
- MediaPipe hand landmark detection

---

# Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

---

# Current Gestures

| Gesture         | Finger Pattern                | Action             |
| --------------- | ----------------------------- | ------------------ |
| Swipe Right     | Hand moves right quickly      | Next Slide         |
| Swipe Left      | Hand moves left quickly       | Previous Slide     |
| Open Palm ✋    | `[1,1,1,1,1]`                 | Start Presentation |
| Fist ✊         | `[0,0,0,0,0]`                 | Black Screen       |
| Index Finger ☝️ | `[0,1,0,0,0]`                 | Pointer Mode       |
| Pinch 🤏        | `[1,1,0,0,0]` + fingers close | Click Detection    |

---

# How It Works

1. Webcam captures live video.
2. MediaPipe detects 21 hand landmarks.
3. Finger states are calculated.
4. Gestures are recognized using landmark positions.
5. PyAutoGUI executes presentation controls.

---

# Hand Landmark Detection

The system tracks important landmarks such as:

- Thumb Tip → Landmark 4
- Index Finger Tip → Landmark 8
- Middle Finger Tip → Landmark 12

MediaPipe returns normalized coordinates:

- `x` → horizontal position
- `y` → vertical position
- `z` → depth

---

# Author

Gauree
