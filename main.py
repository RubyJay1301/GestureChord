import logging
import cv2

from src.webcam import Webcam
from src.detector import Detector
from src.action_manager import ActionManager
from src.settings import Settings

def main():
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        )
    )

    settings = Settings()

    webcam = None
    detector = None

    try:
        
        webcam = Webcam(
            camera_index=settings.camera_index,
            width=settings.camera_width,
            height=settings.camera_height
        )

        detector = Detector(settings)

        action_manager = ActionManager()

        while True:

            frame = webcam.get_frame()

            detections = detector.detect(frame)

            action_manager.handle(detections)

            cv2.imshow(
                settings.window_name,
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:

        logging.info(
            "Application stopped by user"
        )

    except Exception:

        logging.exception(
            "Unexpected application error"
        )

        raise

    finally:

        if detector is not None:
            detector.close()

        if webcam is not None:
            webcam.release()

        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
