from dataclasses import dataclass

@dataclass
class Detection:
    handedness: str
    gesture: tuple[int, ...]
    confidence: float
    
