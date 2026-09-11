import logging
import numpy as np
import pygame
from src.model import Detection
from src.detector import RIGHT_GESTURES, MAJOR_GESTURES, MINOR_GESTURES

logger = logging.getLogger(__name__)

try:
    if not pygame.mixer.get_init():
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
    pygame.mixer.set_num_channels(8)
except Exception as e:
    logger.warning("Could not initialize pygame.mixer: %s", e)

NOTE_FREQUENCIES = {
    "C": 261.63,
    "Db": 277.18,
    "D": 293.66,
    "Eb": 311.13,
    "E": 329.63,
    "F": 349.23,
    "F#": 369.99,
    "G": 392.00,
    "Ab": 415.30,
    "A": 440.00,
    "Bb": 466.16,
    "B": 493.88,
}


class ActionManager:
    def __init__(self):
        self.mode = "major"
        self.current_chord = None
        self.active_channels = []

    def _generate_tone(self, frequency: float, duration_sec: float = 2.0) -> pygame.mixer.Sound:
        sample_rate = 44100
        n_samples = int(sample_rate * duration_sec)
        t = np.linspace(0, duration_sec, n_samples, False)

        envelope = np.ones(n_samples)
        fade_len = int(sample_rate * 0.01) 
        envelope[:fade_len] = np.linspace(0, 1, fade_len)
        envelope[-fade_len:] = np.linspace(1, 0, fade_len)

        wave = np.sin(2 * np.pi * frequency * t) * envelope
        audio = (wave * 32767 / 3).astype(np.int16)
        stereo_audio = np.column_stack((audio, audio))

        return pygame.sndarray.make_sound(stereo_audio)

    def stop_chord(self):
        if self.current_chord is not None:
            for channel in self.active_channels:
                channel.stop()
            self.active_channels.clear()
            self.current_chord = None
            logger.info("Chord playback stopped")

    def start_chord(self, root: str, mode: str):
        base_freq = NOTE_FREQUENCIES.get(root)
        if not base_freq or not pygame.mixer.get_init():
            return

        self.stop_chord()

        self.current_chord = f"{root} {mode}"
        logger.info("Starting chord playback: %s", self.current_chord)

        third_offset = 4 if mode == "major" else 3

        freq_root = base_freq
        freq_third = base_freq * (2 ** (third_offset / 12.0))
        freq_fifth = base_freq * (2 ** (7 / 12.0))

        sound_root = self._generate_tone(freq_root)
        sound_third = self._generate_tone(freq_third)
        sound_fifth = self._generate_tone(freq_fifth)

        ch2 = pygame.mixer.Channel(1)
        ch3 = pygame.mixer.Channel(2)

        ch1.play(sound_root, loops=-1)
        ch2.play(sound_third, loops=-1)
        ch3.play(sound_fifth, loops=-1)

        self.active_channels = [ch1, ch2, ch3]

    def set_major(self):
        if self.mode != "major":
            self.mode = "major"
            logger.info("Mode changed to major")
            if self.current_chord:
                root = self.current_chord.split()[0]
                self.start_chord(root, "major")

    def set_minor(self):
        if self.mode != "minor":
            self.mode = "minor"
            logger.info("Mode changed to minor")
            if self.current_chord:
                root = self.current_chord.split()[0]
                self.start_chord(root, "minor")

    def handle(self, detections: list[Detection]):
        right_hand_detected = False

        for detection in detections:
            if detection.confidence < 0.5:
                continue

            pattern = detection.gesture

            if detection.handedness == "Left":
                action = RIGHT_GESTURES.get(pattern)
                if action == "major_mode":
                    self.set_major()
                elif action == "minor_mode":
                    self.set_minor()

            elif detection.handedness == "Right":
                right_hand_detected = True
                
                root = MAJOR_GESTURES.get(pattern) if self.mode == "major" else MINOR_GESTURES.get(pattern)

                if root is None:
                    if self.current_chord is not None:
                        self.stop_chord()
                else:
                    target_chord = f"{root} {self.mode}"
                    
                    if self.current_chord != target_chord:
                        self.start_chord(root, self.mode)

        if not right_hand_detected and self.current_chord is not None:
            self.stop_chord()
