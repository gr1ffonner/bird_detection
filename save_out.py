import os
from ultralytics import YOLO
import cv2
import progressbar
import logging

logging.getLogger("utils.general").setLevel(logging.WARNING)

widgets = [
    progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()
]

VIDEOS_DIR = os.path.join('videos')

video_path = os.path.join(VIDEOS_DIR, 'bird4.mp4')
video_path_out = video_path.replace(".mp4", "_out.mp4")

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

model_path = 'best.pt'

# Load a model
model = YOLO(model_path)  # load a custom model

threshold = 0.25

length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
with progressbar.ProgressBar(widgets=widgets, max_value=length) as bar:
    for i in range(length):

        results = model(frame, verbose=False)[0]

        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result

            if score > threshold:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                cv2.putText(frame, "bird", (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2, cv2.LINE_AA)
        out.write(frame)
        ret, frame = cap.read()
        bar.update(i + 1)

cap.release()
out.release()
cv2.destroyAllWindows()
