import os
import cv2
from ultralytics import YOLO
from tkinter import Toplevel, Label, messagebox
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk


bird_model_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "bird_model.pt"
)

drone_model_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "drone_model.pt"
)

# Load both models
bird_model = YOLO(bird_model_path)
drone_model = YOLO(drone_model_path)


def show_image(file_path, bird_model=bird_model, drone_model=drone_model):
    if not file_path:
        messagebox.showinfo("Error", "Please choose a file first.")
        return
    # Load image
    image = cv2.imread(file_path)

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

    # Create a new window for displaying the image with bounding boxes
    top_level = tk.Toplevel()
    top_level.title("Bird Detection Result")

    # Convert the image to RGB format for displaying in Tkinter
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(image_rgb)
    img = ImageTk.PhotoImage(image=img)

    # Create a label and display the image
    label = ttk.Label(top_level, image=img)
    label.image = img
    label.pack()

    # Close the new window when the user presses a key
    top_level.bind("<Escape>", lambda event: top_level.destroy())
    top_level.focus_set()

    top_level.mainloop()


def save_image(file_path, root, bird_model=bird_model, drone_model=drone_model):
    if not file_path:
        messagebox.showinfo("Error", "Please choose a file first.")
        return
    image_out_path = file_path.replace(".jpg", "_out.jpg")

    # Load image
    image = cv2.imread(file_path)

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
    # Save the image with bounding boxes
    cv2.imwrite(image_out_path, image)
    messagebox.showinfo("Info", f"Image with bounding boxes saved at: {image_out_path}")
