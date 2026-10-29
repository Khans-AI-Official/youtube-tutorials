"""Export the trained model to ONNX, for use outside Python."""
from ultralytics import YOLO

model = YOLO("runs/detect/ppe4/weights/best.pt")
model.export(format="onnx", imgsz=480)
