from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    camera_index: int = 0
    camera_width: int = 1280
    camera_height: int = 720

    window_name: str = "Gesture Chord Controller"

    max_num_hands: int = 2

    model_complexity: int = 1

    min_detection_confidence: float = 0.5
    min_tracking_confidence: float = 0.5

    confidence_threshold: float = 0.6

    show_landmarks: bool = True
