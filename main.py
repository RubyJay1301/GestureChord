import cv2
from src.webcam import Webcam

camera = Webcam()

while True:
    frame = camera.get_frame()

    cv2.imshow("Live Camera",frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
