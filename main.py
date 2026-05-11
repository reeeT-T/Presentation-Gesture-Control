import cv2
import mediapipe as mp
import pyautogui
import math
import time

# --------------------------------
# MediaPipe Setup
# --------------------------------
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# --------------------------------
# Webcam Setup
# --------------------------------
cap = cv2.VideoCapture(0)

screen_width, screen_height = pyautogui.size()

prev_x = 0

gesture_delay = 1
last_gesture_time = time.time()

# --------------------------------
# Finger Detection Function
# --------------------------------
def fingers_up(landmarks):

    fingers = []

    # Thumb
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tips = [8, 12, 16, 20]
    joints = [6, 10, 14, 18]

    for tip, joint in zip(tips, joints):

        if landmarks[tip].y < landmarks[joint].y:
            fingers.append(1)

        else:
            fingers.append(0)

    return fingers

# --------------------------------
# Main Loop
# --------------------------------
while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    h, w, c = frame.shape

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = hand_landmarks.landmark

            coords = []

            for lm in landmarks:

                coords.append((
                    int(lm.x * w),
                    int(lm.y * h)
                ))

            fingers = fingers_up(landmarks)

            # SHOW FINGER STATES
            cv2.putText(
                frame,
                f"Fingers: {fingers}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            current_time = time.time()

            # --------------------------------
            # INDEX FINGER
            # --------------------------------
            x, y = coords[8]

            cv2.circle(frame, (x, y), 15, (0, 255, 0), cv2.FILLED)

            # --------------------------------
            # SWIPE RIGHT
            # --------------------------------
            if x - prev_x > 150 and current_time - last_gesture_time > gesture_delay:

                print("➡ NEXT SLIDE")

                cv2.putText(
                    frame,
                    "NEXT SLIDE",
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3
                )

                last_gesture_time = current_time

            # --------------------------------
            # SWIPE LEFT
            # --------------------------------
            elif prev_x - x > 150 and current_time - last_gesture_time > gesture_delay:

                print("⬅ PREVIOUS SLIDE")

                cv2.putText(
                    frame,
                    "PREVIOUS SLIDE",
                    (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                last_gesture_time = current_time

            prev_x = x

            # --------------------------------
            # OPEN PALM
            # --------------------------------
            if fingers == [1,1,1,1,1]:

                if current_time - last_gesture_time > gesture_delay:

                    print("✋ START PRESENTATION")

                    cv2.putText(
                        frame,
                        "OPEN PALM DETECTED",
                        (50, 220),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 0),
                        3
                    )

                    last_gesture_time = current_time

            # --------------------------------
            # FIST
            # --------------------------------
            if fingers == [0,0,0,0,0]:

                if current_time - last_gesture_time > gesture_delay:

                    print("✊ BLACK SCREEN")

                    cv2.putText(
                        frame,
                        "FIST DETECTED",
                        (50, 280),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 255),
                        3
                    )

                    last_gesture_time = current_time

            # --------------------------------
            # POINTER MODE
            # --------------------------------
            if fingers == [0,1,0,0,0]:

                print("☝ POINTER MODE")

                screen_x = screen_width / w * x
                screen_y = screen_height / h * y

                cv2.putText(
                    frame,
                    "POINTER MODE",
                    (50, 340),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    3
                )

            # --------------------------------
            # PINCH GESTURE
            # --------------------------------
            thumb_x, thumb_y = coords[4]
            index_x, index_y = coords[8]

            distance = math.hypot(
                index_x - thumb_x,
                index_y - thumb_y
            )

            cv2.putText(
                frame,
                f"Pinch Distance: {int(distance)}",
                (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2
            )

            if distance < 40 and fingers == [1,1,0,0,0]:

                print("🤏 CLICK / PINCH DETECTED")

                cv2.putText(
                    frame,
                    "PINCH DETECTED",
                    (50, 400),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,255,255),
                    3
                )

                time.sleep(0.3)

    # --------------------------------
    # Exit text
    # --------------------------------
    cv2.putText(
        frame,
        "Press Q to Quit",
        (10, h - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,255),
        2
    )

    # --------------------------------
    # Show webcam
    # --------------------------------
    cv2.imshow("Gesture Presentation Controller", frame)

    # --------------------------------
    # Quit
    # --------------------------------
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --------------------------------
# Cleanup
# --------------------------------
cap.release()
cv2.destroyAllWindows()