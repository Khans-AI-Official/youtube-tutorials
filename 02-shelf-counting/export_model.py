from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")
model.export(format="onnx")      # for servers and laptops
model.export(format="tflite")    # for Android phones
