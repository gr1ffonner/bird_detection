import os
import cv2
from ultralytics import YOLO

# Define your paths
VIDEOS_DIR = os.path.join(".", "videos")
video_path = os.path.join(VIDEOS_DIR, "bd1.mp4")
bird_model_path = "bird_model.pt"

# Load the YOLO model
model = YOLO(bird_model_path)

threshold = 0.5

# Open the video capture
cap = cv2.VideoCapture(video_path)
fps = int(cap.get(cv2.CAP_PROP_FPS))

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Process every nth frame (e.g., process every 5th frame)
    frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    if frame_number % 5 != 0:
        continue

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(
                frame,
                "bird",
                (int(x1), int(y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

    cv2.imshow("Bird Detection", frame)

    # Press 'q' to exit the video playback
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
