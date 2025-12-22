from camera import Camera
from face_detection import FaceDetector
from features import FeatureExtractor
from detection import Detector
from alerts import AlertSystem
import cv2

def main():
    # Initialisation modules
    camera = Camera()
    detector_face = FaceDetector()
    extractor = FeatureExtractor()
    detector = Detector()
    alerts = AlertSystem()

    while True:
        ret, frame = camera.get_frame()
        if not ret:
            break

        # Détection visage + landmarks
        landmarks = detector_face.get_landmarks(frame)

        if landmarks:
            # Calcul des features
            features = extractor.compute_features(frame, landmarks)
            # Affichage debug
            mar_value = features['mar']
            print(f"MAR: {mar_value:.3f}")  # affiche 3 décimales

            # Détection fatigue / inattention
            alert_flags = detector.check_alerts(features)

            # Affichage alertes
            alerts.display_alerts(frame, alert_flags)
            
            
            # Affichage Pitch / Yaw
            cv2.putText(frame, f"Pitch: {features['pitch']:.1f}, Yaw: {features['yaw']:.1f}",
                        (50, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

        cv2.imshow("Driver Alert System", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
