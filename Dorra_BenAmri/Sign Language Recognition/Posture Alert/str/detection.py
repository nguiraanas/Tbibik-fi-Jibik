class Detector:
    EAR_THRESHOLD = 0.2
    MAR_THRESHOLD = 0.25

    # Nouveaux seuils réalistes
    YAW_THRESHOLD = 25       # degrés
    PITCH_UP_THRESHOLD = 15  # degrés
    PITCH_DOWN_THRESHOLD = -15

    def __init__(self):
        self.yawning_counter = 0

    def check_alerts(self, features):
        alerts = {}

        # Fatigue
        ear_avg = (features['ear_left'] + features['ear_right']) / 2
        alerts['fatigue'] = ear_avg < self.EAR_THRESHOLD

        # Bâillement (MAR)
        if features['mar'] > self.MAR_THRESHOLD:
            self.yawning_counter += 1
        else:
            self.yawning_counter = 0
        alerts['yawning'] = self.yawning_counter >= 3

        # Distraction
        yaw = features['yaw']
        pitch = features['pitch']

        alerts['distraction'] = (
            abs(yaw) > self.YAW_THRESHOLD or
            pitch > self.PITCH_UP_THRESHOLD or
            pitch < self.PITCH_DOWN_THRESHOLD
        )

        return alerts
