from dataclasses import dataclass

@dataclass
class Detection:
    handedness: str
    gesture: str
    confidence: float
    
