"""Run the trained model live on a webcam."""
from ultralytics import YOLO

model = YOLO("runs/detect/ppe4/weights/best.pt")

# 0 is your first webcam; show=True opens a window with the boxes
model.predict(source=0, show=True, conf=0.4, imgsz=480)
