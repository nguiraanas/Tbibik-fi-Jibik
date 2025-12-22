import cv2
import pygame
import threading
import os
import time

class AlertSystem:
    ALERT_DELAY = 2  # secondes avant le son

    def __init__(self):
        pygame.mixer.init()
        # sons différents pour chaque type
        self.sounds = {
            'fatigue': pygame.mixer.Sound(os.path.join('assets', 'alert.wav')),
            'yawning': pygame.mixer.Sound(os.path.join('assets', 'alert2.wav')),
            'distraction': pygame.mixer.Sound(os.path.join('assets', 'alert2.wav'))
        }
        self.colors = {
            'fatigue': (0,0,255),       # rouge
            'yawning': (0,255,255),     # jaune
            'distraction': (255,0,0)    # bleu ou autre
        }
        self.alert_start_times = {}

    def display_alerts(self, frame, alerts):
        y = 50
        current_time = time.time()

        for key, active in alerts.items():
            if active:
                # Texte coloré
                color = self.colors.get(key, (0,0,255))
                cv2.putText(frame, f"ALERT: {key.upper()}!", (50, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                y += 40

                # Son avec délai
                if key not in self.alert_start_times:
                    self.alert_start_times[key] = current_time

                elapsed = current_time - self.alert_start_times[key]
                if elapsed >= self.ALERT_DELAY:
                    threading.Thread(target=self.play_sound, args=(key,), daemon=True).start()
            else:
                # réinitialiser timestamp
                if key in self.alert_start_times:
                    del self.alert_start_times[key]

    def play_sound(self, key):
        sound = self.sounds.get(key)
        if sound and not pygame.mixer.get_busy():
            sound.play()
