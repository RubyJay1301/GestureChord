from unittest.mock import patch
from src.action_manager import ActionManager
from src.model import Detection

@patch("src.action_manager.pygame")
def test_default_mode_is_major(mock_pygame):
    manager = ActionManager()
    detection = Detection(
        handedness="Left",
        gesture=(0, 0, 0, 0, 0, 0),
        confidence=0.95
    )
    assert manager.mode == "major"

@patch("src.action_manager.pygame")
def test_right_hand_switches_to_minor(mock_pygame):
    manager = ActionManager()
    
    # Gesture tuple (0, 0, 0, 0) maps to "minor_mode" in RIGHT_GESTURES
    detection = Detection(
        handedness="Right",
        gesture=(1, 0, 0, 0, 0),
        confidence=0.95
    )

    manager.handle([detection])
    assert manager.mode == "minor"

@patch("src.action_manager.pygame")
def test_right_hand_switches_to_major(mock_pygame):
    manager = ActionManager()
    manager.mode = "minor"
    
    # Gesture tuple (1, 1, 1, 1) maps to "major_mode" in RIGHT_GESTURES
    detection = Detection(
        handedness="Right",
        gesture=(1, 1, 1, 1),
        confidence=0.95
    )

    manager.handle([detection])
    assert manager.mode == "major"

@patch("src.action_manager.pygame")
def test_left_hand_selects_chord(mock_pygame):
    manager = ActionManager()
    
    # Gesture tuple (1, 0, 0, 0) maps to "C" in MAJOR_GESTURES
    detection = Detection(
        handedness="Left",
        gesture=(1, 0, 0, 0),
        confidence=0.95
    )

    manager.handle([detection])
    assert manager.current_chord == "C major"
