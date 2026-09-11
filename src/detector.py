import cv2
import mediapipe as mp
from dataclasses import dataclass

@dataclass
class Detection:
    handedness: str
    gesture: tuple[int, int, int, int, int]
    confidence: float

RIGHT_GESTURES = {
    (1, 1, 1, 1, 1): "major_mode",  # Thumbs up
    (0, 0, 0, 0, 0): "minor_mode",  # Fist
}

MAJOR_GESTURES = {
    (1, 0, 0, 0, 0): "C",   # Thumb only
    (0, 1, 0, 0, 0): "G",   # Index point
    (0, 0, 0, 0, 1): "F",   # Pinky only
    (1, 1, 0, 0, 0): "D",   # L-Shape
    (0, 1, 1, 0, 0): "A",   # Peace Sign
    (1, 0, 0, 0, 1): "E",   # Shaka
    (1, 1, 1, 0, 0): "B",   # Gun Gesture
    (0, 1, 1, 1, 0): "Bb",  # Scout Sign
    (0, 1, 0, 0, 1): "Eb",  # Rock / Horns
    (1, 0, 1, 0, 0): "Ab",  # Thumb + Middle
    (0, 1, 1, 1, 1): "Db",  # 4 Fingers Up
    (1, 1, 1, 1, 1): "F#",  # Open Hand
}

MINOR_GESTURES = MAJOR_GESTURES.copy()

class Detector:
    def __init__(self, settings):
        self.settings = settings
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=settings.max_num_hands,
            model_complexity=settings.model_complexity,
            min_detection_confidence=settings.min_detection_confidence,
            min_tracking_confidence=settings.min_tracking_confidence,
        )

    def get_finger_pattern(self, landmarks, handedness: str) -> tuple[int, int, int, int, int]:
        wrist = landmarks[0]

        def is_extended(tip_idx, pip_idx):
            tip_dist = (landmarks[tip_idx].x - wrist.x)**2 + (landmarks[tip_idx].y - wrist.y)**2
            pip_dist = (landmarks[pip_idx].x - wrist.x)**2 + (landmarks[pip_idx].y - wrist.y)**2
            return int(tip_dist > pip_dist)

        index = is_extended(8, 6)
        middle = is_extended(12, 10)
        ring = is_extended(16, 14)
        pinky = is_extended(20, 18)

        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]

        if handedness == "Right":
            thumb = int(thumb_tip.x < thumb_ip.x - 0.02)
        else:
            thumb = int(thumb_tip.x > thumb_ip.x + 0.02)

        return (thumb, index, middle, ring, pinky)

    def detect(self, frame) -> list[Detection]:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = self.hands.process(rgb_frame)

        detections = []

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness_info in zip(results.multi_hand_landmarks, results.multi_handedness):
                handedness = handedness_info.classification[0].label  # "Left" or "Right"
                confidence = handedness_info.classification[0].score

                pattern = self.get_finger_pattern(hand_landmarks.landmark, handedness)

                detections.append(
                    Detection(
                        handedness=handedness,
                        gesture=pattern,
                        confidence=confidence
                    )
                )

        return detections

    def close(self):
        if hasattr(self, "hands") and self.hands:
            self.hands.close()
