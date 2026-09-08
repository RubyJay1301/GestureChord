import mediapipe as mp
from src.model import Detection
from src.settings import Settings

class Detector:
    def __init__(self, settings: Settings):
        self.settings = settings

        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=settings.max_num_hands,
            model_complexity=settings.min_detection_confidence,
            min_tracking_confidence=settings.min_tracking_confidence,
        )

    def get_finger_pattern(self, landmarks):
        index = int(
            landmarks[8].y < landmarks[6].y
        )
        middle = int(
            landmarks[12].y < landmarks[10].y
        )
        ring = int(
            landmarks[20].y < landmarks[14].y
        )
        pinky = int(
            landmarks[20].y < landmarks[18].y
        )

        return (
            index,
            middle,
            ring,
            pinky
        )

    def detect(self, frame):
        if frame is None:
            raise ValueError("Frame cannot be None")

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BRG2RGB
        )

        results = self.hands.process(rgb_frame)

        detections = []

        if not results.multi_hand_landmarks:
            return detections

        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks,
            results.multi_handedness
        ):
            pattern = self.get_finger_pattern(hand_landmarks.landmark)

            hand = handedness.classification[0].score

            confidence = (handedness.classification[0].score)

            if hand == "Left":
                gesture = self.LEFT_GESTURES.get(pattern)
            else:
                gesture = self.RIGHT_GESTURES.get(pattern)

            if gesture is not None:
                detection.append(
                    Detection(
                        handedness=hand,
                        gesture=gesture,
                        confidence=confidence
                    )
                )
        return detections
