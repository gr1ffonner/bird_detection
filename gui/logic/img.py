import cv2
import os
from ultralytics import YOLO

bird_model_path = "bird_model.pt"
drone_model_path = "drone_model.pt"

IMAGES_DIR = os.path.join("img")

image_path = os.path.join(IMAGES_DIR, "flock.jpg")
image_out_path = image_path.replace(".jpg", "_out.jpg")

# Load both models
bird_model = YOLO(bird_model_path)
drone_model = YOLO(drone_model_path)

# Load image
image = cv2.imread(image_path)

# Perform object detection for both birds and drones
results_from_bird = bird_model(image, verbose=False)
results_from_drone = drone_model(image, verbose=False)

threshold_bird = 0.40
threshold_drone = 0.70  # Adjust this threshold based on your needs

# Get drone detection results
drone_detected = any(
    max(result.probs[0]) > threshold_drone if result.probs is not None else False
    for result in results_from_drone
)

# Iterate over results from the bird model
for result in results_from_bird:
    boxes = result.boxes  # Boxes object for bbox outputs

    # Draw bounding boxes on the image for birds, only if no drone is detected
    if not drone_detected:
        for box in boxes:
            x1, y1, x2, y2, score, _ = box.data.tolist()[0]

            if score > threshold_bird:
                cv2.rectangle(
                    image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1
                )
                cv2.putText(
                    image,
                    "Bird",
                    (int(x1), int(y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (0, 255, 0),
                    1,
                    cv2.LINE_AA,
                )

# Save the output image
cv2.imshow("Bird Detection", image)
cv2.waitKey(0)
cv2.imwrite(image_out_path, image)

print(f"Image with bounding boxes saved at: {image_out_path}")
