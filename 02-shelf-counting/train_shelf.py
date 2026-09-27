"""Train a YOLO detector on your labelled shelf photos.
pip install ultralytics
"""
from ultralytics import YOLO

model = YOLO("yolo11n.pt")          # small pretrained model
model.train(data="shelf.yaml",      # dataset paths + class names
            epochs=100, imgsz=640)
