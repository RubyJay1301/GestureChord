#This is used to determine the camera
import AVFoundation

devices = AVFoundation.AVCaptureDevice.devicesWithMediaType_(
    AVFoundation.AVMediaTypeVideo
)

if not devices:
    print("No cameras found.")
else:
    print("Cameras found:\n")

    for index, camera in enumerate(devices):
        print(f"OpenCV index: {index}")
        print(f"Name:          {camera.localizedName()}")
        print(f"Unique ID:     {camera.uniqueID()}")
        print("-" * 40)
