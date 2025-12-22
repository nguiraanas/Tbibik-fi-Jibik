from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
import tensorflow as tf
import pickle

from utils.hand_extractor import extract_keypoints
from utils.normalize import normalize_landmarks

app = FastAPI(title="Tunisian Sign Language API")

model = tf.keras.models.load_model("model/tsl_mlp_final.h5")
with open("model/label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

@app.post("/predict")
async def predict_sign(file: UploadFile = File(...)):
    contents = await file.read()
    np_img = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    kp = extract_keypoints(img)
    if kp is None:
        return {"error": "No hand detected"}

    feat = normalize_landmarks(kp)
    pred = model.predict(feat.reshape(1, -1), verbose=0)
    label = le.inverse_transform([np.argmax(pred)])[0]

    return {"prediction": label}
