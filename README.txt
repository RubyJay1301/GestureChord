To install the libraries needed: pip install -r requirements.txt 
To run: python main.py

Skills and concepts used in this project:
 - Practical experience with edge vision frameworks (MediaPipe, OpenCV)
 - Handling real-time, frame-by-frame data streams and processing 3D spatial key points with minimal latency
 - Uses vector calculations to map raw spatial key points into discrete finger states
 - Clean object-oriented architecture separating video streaming, computer vision, audio synthesis, and system configurations into distinct, single-responsibility modules.
 - Good coding practices - Uses structured logging, immutable configurations, dynamic audio DSP via NumPy and automatic unit testing

Structure for the code:

Project
|
|-- src/
|   |-- webcam.py
|   |-- detector.py
|   |-- action_manager.py
|   |-- model.py
|   |-- settings.py
|
|-- tests/
|   |-- test_detector.py
|   |-- test_actions.py
|
|-- requirements.txt
|-- README.md
|-- main.py

12 hand gestures on left hand and 2 with right hand to switch between major and minor chords

Right Hand Gestures:
Open hand : Major
Closed hand : Minor

Left Hand Gestures:
Index only: C
Middle only: G
Pinky only: F
Thumb and index: D
index and Middle: A
Thumb and Pinky: E
Thumb Index and Middle: B
All fingers: F#
Index Middle and Ring: Bb
Index and Pinky: Eb
Thumb Index and Pinky: Ab
Index Middle Ring and Pinky: Db



 
