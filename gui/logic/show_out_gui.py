import os
import cv2
from ultralytics import YOLO
from tkinter import Toplevel, Label
from PIL import Image, ImageTk


class VideoPlayer:
    def __init__(self, root, video_path):
        self.root = root
        self.video_path = video_path
        self.model_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "drone_model.pt"
        )
        self.model = YOLO(self.model_path)
        self.threshold = 0.60
        self.cap = cv2.VideoCapture(video_path)
        self.player_window = None
        self.video_label = None
        self.create_player_window()

    def create_player_window(self):
        self.player_window = Toplevel(self.root)
        self.player_window.title("Video Player")

        self.video_label = Label(self.player_window)
        self.video_label.pack()

        self.player_window.bind("<Escape>", self.stop_video)  # Bind Escape key

        self.process_next_frame()

    def process_next_frame(self):
        ret, frame = self.cap.read()

        if ret:
            frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            if frame_number % 10 == 0:
                results = self.model(frame, verbose=False)[0]

                for result in results.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = result

                    if score > self.threshold:
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

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = ImageTk.PhotoImage(image=img)

                self.video_label.img = img
                self.video_label.config(image=img)
                self.video_label.image = img

                self.player_window.after(1, self.process_next_frame)
            else:
                self.player_window.after(1, self.process_next_frame)
        else:
            self.cap.release()
            self.root.after(100, self.release_and_destroy)

    def release_and_destroy(self):
        self.player_window.destroy()

    def stop_video(self, event):
        self.cap.release()
        self.player_window.destroy()


def show_out(root, video_path):
    video_player = VideoPlayer(root, video_path)
    root.protocol("WM_DELETE_WINDOW", video_player.release_and_destroy)
