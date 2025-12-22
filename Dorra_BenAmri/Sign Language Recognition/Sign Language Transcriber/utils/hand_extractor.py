import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

def extract_keypoints(frame):
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(img_rgb)

    if not res.multi_hand_landmarks:
        return None

    lm = res.multi_hand_landmarks[0].landmark
    return np.array([[p.x, p.y, p.z] for p in lm], dtype=np.float32)
