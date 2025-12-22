import cv2
import numpy as np

class FeatureExtractor:
    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]
    MOUTH = [78, 308, 13, 311, 81, 402] 

    def compute_features(self, frame, landmarks):
        features = {}
        features['ear_left'] = self.eye_aspect_ratio(landmarks, self.LEFT_EYE, frame.shape)
        features['ear_right'] = self.eye_aspect_ratio(landmarks, self.RIGHT_EYE, frame.shape)
        features['mar'] = self.mouth_aspect_ratio(landmarks, self.MOUTH, frame.shape)
        pitch, yaw, roll = self.compute_head_pose(landmarks, frame.shape)
        features['pitch'] = pitch
        features['yaw'] = yaw
        features['roll'] = roll
        features['head_pose'] = pitch  # pour la distraction simple
        return features

    def eye_aspect_ratio(self, landmarks, eye_indices, frame_shape):
        points = np.array([[landmarks[i].x * frame_shape[1], landmarks[i].y * frame_shape[0]] for i in eye_indices])
        A = np.linalg.norm(points[1]-points[5])
        B = np.linalg.norm(points[2]-points[4])
        C = np.linalg.norm(points[0]-points[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def mouth_aspect_ratio(self, landmarks, mouth_indices, frame_shape):
        # 6 points : coin gauche, coin droit, haut, bas
        points = np.array([[landmarks[i].x * frame_shape[1], landmarks[i].y * frame_shape[0]] 
                        for i in mouth_indices])
        # points[0] = coin gauche
        # points[1] = coin droit
        # points[2] = haut
        # points[3] = bas
        A = np.linalg.norm(points[2] - points[3])  # vertical
        C = np.linalg.norm(points[0] - points[1])  # horizontal
        mar = A / C
        return mar
    
    def rotationMatrixToEulerAngles(self, R):

        sy = np.sqrt(R[0,0] * R[0,0] + R[1,0] * R[1,0])

        singular = sy < 1e-6

        if not singular:
            x = np.arctan2(R[2,1], R[2,2])   # pitch
            y = np.arctan2(-R[2,0], sy)      # yaw
            z = np.arctan2(R[1,0], R[0,0])   # roll
        else:
            x = np.arctan2(-R[1,2], R[1,1])
            y = np.arctan2(-R[2,0], sy)
            z = 0

        return np.degrees(x), np.degrees(y), np.degrees(z)

    
    def compute_head_pose(self, landmarks, frame_shape):
        h, w = frame_shape[:2]

        # ✔ Nouveau modèle 3D compatible MediaPipe FaceMesh
        model_points_3d = np.array([
            (0, 0, 0),          # nez 1
            (0, 70, -2),        # menton 152
            (-34, -20, -30),    # coin oeil gauche 33
            (34, -20, -30),     # coin oeil droit 263
            (-20, 20, -20),     # bouche gauche 61
            (20, 20, -20)       # bouche droite 291
        ], dtype=np.float64)

        # Points 2D (image)
        image_points = np.array([
            (landmarks[1].x * w, landmarks[1].y * h),
            (landmarks[152].x * w, landmarks[152].y * h),
            (landmarks[33].x * w, landmarks[33].y * h),
            (landmarks[263].x * w, landmarks[263].y * h),
            (landmarks[61].x * w, landmarks[61].y * h),
            (landmarks[291].x * w, landmarks[291].y * h)
        ], dtype=np.float64)

        # Matrice caméra
        focal = w
        center = (w / 2, h / 2)
        camera_matrix = np.array([
            [focal, 0, center[0]],
            [0, focal, center[1]],
            [0,     0,        1]
        ], dtype=np.float64)

        dist_coeffs = np.zeros((4, 1))

        # solvePnP
        success, rotation_vector, translation_vector = cv2.solvePnP(
            model_points_3d,
            image_points,
            camera_matrix,
            dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            return 0.0, 0.0, 0.0

        # Matrice de rotation
        Rmat, _ = cv2.Rodrigues(rotation_vector)

        # Angles d'Euler corrects
        pitch, yaw, roll = self.rotationMatrixToEulerAngles(Rmat)

        # ✔ Correction des angles qui tournent autour de 180°
        if pitch > 90:
            pitch -= 180
        if pitch < -90:
            pitch += 180

        if yaw > 90:
            yaw -= 180
        if yaw < -90:
            yaw += 180

        return pitch, yaw, roll