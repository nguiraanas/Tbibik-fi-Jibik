import cv2
import numpy as np
import tensorflow as tf
import pickle
from collections import deque

from utils.hand_extractor import extract_keypoints
from utils.normalize import normalize_landmarks

# Load model + encoder
model = tf.keras.models.load_model("model/tsl_mlp_final.h5")
with open("model/label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

# Stabilisation
buffer = deque(maxlen=10)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    kp = extract_keypoints(frame)

    if kp is not None:
        feat = normalize_landmarks(kp)
        pred = model.predict(feat.reshape(1, -1), verbose=0)
        label = le.inverse_transform([np.argmax(pred)])[0]

        buffer.append(label)
        final_label = max(set(buffer), key=buffer.count)

        cv2.putText(
            frame,
            f"TSL: {final_label}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3
        )

    cv2.imshow("Tunisian Sign Language - Realtime", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
