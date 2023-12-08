import os
import cv2
from ultralytics import YOLO
from tkinter import Toplevel, Label, Canvas, Scrollbar, RIGHT, Y, messagebox
from PIL import Image, ImageTk

drone_model_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "drone_model.pt"
)

drone_model = YOLO(drone_model_path)


def show_image(file_path, drone_model=drone_model):
    if not file_path:
        messagebox.showinfo("Error", "Please choose a file first.")
        return

    # Load image
    image = cv2.imread(file_path)

    # Perform object detection for drones
    results_from_drone = drone_model(image, verbose=False)

    threshold_drone = 0.70  # Adjust this threshold based on your needs

    # Draw bounding boxes on the image for drones
    for result in results_from_drone:
        for box in result.boxes:
            x1, y1, x2, y2, score, _ = box.data.tolist()[0]

            if score > threshold_drone:
                cv2.rectangle(
                    image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 1
                )
                cv2.putText(
                    image,
                    "Drone",
                    (int(x1), int(y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (255, 0, 0),
                    1,
                    cv2.LINE_AA,
                )

        # Get image dimensions
        img_height, img_width, _ = image.shape

        # Create a new window for displaying the image with bounding boxes
        top_level = Toplevel()
        top_level.title("Drone Detection Result")

        # Create a canvas with a scrollbar
        canvas = Canvas(top_level, width=img_width, height=img_height)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(top_level, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        # Convert the image to RGB format for displaying in Tkinter
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image_rgb)
        img = ImageTk.PhotoImage(image=img)

        # Create a label and display the image on the canvas
        label = Label(canvas, image=img)
        label.image = img
        label_id = canvas.create_window(0, 0, anchor="nw", window=label)

        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", configure_scroll_region)

        # Close the new window when the user presses a key
        top_level.bind("<Escape>", lambda event: top_level.destroy())
        top_level.focus_set()

        top_level.mainloop()


def save_image(file_path, root, drone_model=drone_model):
    if not file_path:
        messagebox.showinfo("Error", "Please choose a file first.")
        return

    # Load image
    image = cv2.imread(file_path)

    # Perform object detection for drones
    results_from_drone = drone_model(image, verbose=False)

    threshold_drone = 0.50  # Adjust this threshold based on your needs

    # Get drone detection results
    for result in results_from_drone:
        boxes = result.boxes  # Boxes object for bbox outputs

        # Draw bounding boxes on the image for drones
        for box in boxes:
            x1, y1, x2, y2, score, _ = box.data.tolist()[0]

            if score > threshold_drone:
                cv2.rectangle(
                    image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 1
                )
                cv2.putText(
                    image,
                    "Drone",
                    (int(x1), int(y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (255, 0, 0),
                    1,
                    cv2.LINE_AA,
                )

    # Save the image with bounding boxes
    image_out_path = file_path.replace(".jpg", "_out.jpg")
    cv2.imwrite(image_out_path, image)

    # Show message in the GUI
    messagebox.showinfo("Info", f"Image with drone bounding boxes saved at: {image_out_path}")
