import os
from ultralytics import YOLO
import cv2
import logging
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

logging.getLogger("utils.general").setLevel(logging.WARNING)


def save_out(video_path, root):
    video_path_out = video_path.replace(".mp4", "_out.mp4")
    cap = cv2.VideoCapture(video_path)

    ret, frame = cap.read()
    H, W, _ = frame.shape
    out = cv2.VideoWriter(
        video_path_out,
        cv2.VideoWriter_fourcc(*"mp4v"),
        int(cap.get(cv2.CAP_PROP_FPS)),
        (W, H),
    )

    model_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "drone_model.pt"
    )

    # Load a model
    model = YOLO(model_path)  # load a custom model

    threshold = 0.60

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    progress_window = tk.Toplevel(root)
    progress_window.title("Video Processing")
    progress_window.geometry("300x100")
    progress_label = ttk.Label(progress_window, text="Processing...")
    progress_label.pack(pady=10)
    progress_bar = ttk.Progressbar(
        progress_window,
        orient=tk.HORIZONTAL,
        length=200,
        mode="determinate",
        maximum=length,
    )
    progress_bar.pack(pady=10)

    def process_frame(i):
        nonlocal ret, frame

        if not ret or i >= length:
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Info", f"Output is saved into {video_path_out}")
            progress_window.destroy()
            return

        results = model(frame, verbose=False)[0]
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, _ = result
            if score > threshold:
                cv2.rectangle(
                    frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 1
                )
                cv2.putText(
                    frame,
                    "Drone",
                    (int(x1), int(y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (255, 0, 0),
                    1,
                    cv2.LINE_AA,
                )
        out.write(frame)
        ret, frame = cap.read()

        progress_bar["value"] = i
        progress_window.update_idletasks()

        progress_window.after(1, process_frame, i + 1)

    progress_window.after(1, process_frame, 0)
    progress_window.mainloop()
