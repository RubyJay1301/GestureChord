class ActionManager:
    def __init__(self):
        self.mode = "major"

        self.current_chord = None

    def set_major(self):
        self.mode = "major"
        print("Major mode")

    def set_minor(self):
        self.mode = "minor"
        print("Minor mode")

    def select_chord(self, root):
        chord = f"{root} {self.mode}"
        self.current_chord = chord
        print(
            f"Chord selected: {chord}"
        )

    def handle(self, detections):
        for detection in detections:
            if detection.handedness == "Right":
                if detection.gesture == "major_mode":
                    self.set_major()

                elif detection.gesture == "minor_mode":
                    self.set_minor()

            elif detection.handedness == "Left":
                self.select_chord(
                    detection.gesture
                )
