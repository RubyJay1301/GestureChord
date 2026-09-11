from src.detector import MAJOR_GESTURES, RIGHT_GESTURES

def test_c_gesture():
    result = MAJOR_GESTURES.get((1, 0, 0, 0))
    assert result == "C"

def test_g_gesture():
    result = MAJOR_GESTURES.get((1, 1, 0, 0))
    assert result == "G"

def test_major_gesture():
    result = RIGHT_GESTURES.get((1, 1, 1, 1))
    assert result == "major_mode"

def test_minor_gesture():
    result = RIGHT_GESTURES.get((0, 0, 0, 0))
    assert result == "minor_mode"
