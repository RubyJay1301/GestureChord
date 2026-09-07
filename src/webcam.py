import logging
import cv2

logger = logging.getLogger(__name__)

class Webcam:
    def __init__(self, camera_index=0, width=1280, height=720):
        self.camera_index = camera_index
        self.camera = cv2.VideoCapture(camera_index, cv2.CAP_AVFOUNDATION)

        if not self.camera.isOpened():
            raise RuntimeError(
                f"Could not open webcam {camera_index}"
            )

        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            width
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            height
        )

        logger.info("Webcam opened")

    def get_frame(self):
        ret, frame = self.camera.read()

        if not ret:
            raise RuntimeError(
                "Could not read frame from webcam"
            )
        return frame

    def release(self):
        self.camera.release()
        logger.info("Webcam released")
