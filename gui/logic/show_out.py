import os
import cv2
from ultralytics import YOLO

# Get the directory of the current script
script_directory = os.path.dirname(os.path.realpath(__file__))

# Construct the path to bird_model.pt
bird_model_path = os.path.join(script_directory, "bird_model.pt")
drone_model_path = os.path.join(script_directory, "drone_model.pt")

# bird_model_path = "bird_model.pt"
# drone_model_path = "drone_model.pt"

bird_model = YOLO(bird_model_path)
drone_model = YOLO(drone_model_path)

threshold_bird = 0.50
threshold_drone = 0.70

cap = cv2.VideoCapture("/home/danya/code/projects/bird_detection/videos/bd1.mp4")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    if frame_number % 5 != 0:
        continue

    frame = cv2.resize(frame, (360, 640))

    results_from_bird = bird_model(frame, verbose=False)[0]
    results_from_drone = drone_model(frame, verbose=False)[0]

    drone_detected = any(
        max(result.probs[0]) > threshold_drone if result.probs is not None else False
        for result in results_from_drone
    )

    if not drone_detected:
        for result in results_from_bird.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result

            if score > threshold_bird:
                cv2.rectangle(
                    frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 4
                )
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
