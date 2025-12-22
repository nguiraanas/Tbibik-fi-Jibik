import numpy as np

def normalize_landmarks(landmarks_xyz):
    pts = landmarks_xyz.copy()

    wrist = pts[0]
    pts = pts - wrist

    ref = pts[5]
    scale = np.linalg.norm(ref[:2]) + 1e-8
    pts = pts / scale

    return pts.reshape(-1)  # (63,)
