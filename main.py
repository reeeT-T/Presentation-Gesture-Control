import cv2
import mediapipe as mp
import pyautogui
import time
import math

# -----------------------------
# MediaPipe Hand Setup
# -----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# -----------------------------
# Webcam Setup
# -----------------------------
cap = cv2.VideoCapture(0)

prev_x = 0
gesture_delay = 1
last_gesture_time = time.time()

# -----------------------------
# Main Loop
# -----------------------------
while True:
    success, frame = cap.read()

    if not success:
        break

    # Flip frame for mirror view
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process hand landmarks
    results = hands.process(rgb_frame)

    h, w, c = frame.shape

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Get Index Finger Tip
            index_tip = hand_landmarks.landmark[8]

            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            # Draw fingertip
            cv2.circle(frame, (x, y), 15, (0, 255, 0), cv2.FILLED)

            current_time = time.time()

            # ---------------------------------
            # Swipe Right -> Next Slide
            # ---------------------------------
            if x - prev_x > 150 and current_time - last_gesture_time > gesture_delay:
                pyautogui.press("right")
                last_gesture_time = current_time

                cv2.putText(
                    frame,
                    "NEXT SLIDE",
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3
                )

            # ---------------------------------
            # Swipe Left -> Previous Slide
            # ---------------------------------
            elif prev_x - x > 150 and current_time - last_gesture_time > gesture_delay:
                pyautogui.press("left")
                last_gesture_time = current_time

                cv2.putText(
                    frame,
                    "PREVIOUS SLIDE",
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

            prev_x = x

    # Show Window
    cv2.imshow("Gesture Controlled Presentation", frame)

    # Press Q to Exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -----------------------------
# Cleanup
# -----------------------------
cap.release()
cv2.destroyAllWindows()