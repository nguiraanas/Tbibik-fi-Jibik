import cv2
import requests
from collections import deque

API_URL = "http://127.0.0.1:8000/predict"

cap = cv2.VideoCapture(0)

# Buffer pour stabiliser l'affichage
buffer = deque(maxlen=10)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Encode frame -> jpg
    _, img_encoded = cv2.imencode(".jpg", frame)

    try:
        response = requests.post(
            API_URL,
            files={"file": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")},
            timeout=1
        )

        if response.status_code == 200:
            data = response.json()
            if "prediction" in data:
                buffer.append(data["prediction"])
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

    except requests.exceptions.RequestException:
        cv2.putText(
            frame,
            "API OFFLINE",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 0, 255),
            3
        )

    cv2.imshow("TSL - FastAPI Client", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
