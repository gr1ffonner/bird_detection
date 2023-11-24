import cv2
import os
from ultralytics import YOLO

model_path = "bird_model.pt"
IMAGES_DIR = os.path.join("img")

image_path = os.path.join(IMAGES_DIR, "bd3.jpg")
image_out_path = image_path.replace(".jpg", "_out.jpg")

# Load a model
model = YOLO(model_path)

# Load image
image = cv2.imread(image_path)

# Perform object detection
results = model(image, verbose=False)

threshold = 0.5

# Iterate over results
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs

    # Draw bounding boxes on the image
    for box in boxes:
        x1, y1, x2, y2, score, _ = box.data.tolist()[0]

        if score > threshold:
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(
                image,
                "Bird",
                (int(x1), int(y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.3,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

# Save the output image
cv2.imshow("Bird Detection", image)
cv2.waitKey(0)

cv2.imwrite(image_out_path, image)

print(f"Image with bounding boxes saved at: {image_out_path}")
