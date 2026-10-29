"""Step 2: fine-tune a small pretrained YOLO model on our four classes."""
from ultralytics import YOLO

model = YOLO("yolo11n.pt")          # 2.6M parameters, already trained on COCO

results = model.train(
    data="ppe4.yaml",   # where the images and labels are
    epochs=30,          # passes over the training set
    imgsz=480,          # images are resized to 480 x 480
    batch=16,
    device="cpu",       # use 0 if you have an NVIDIA GPU
    name="ppe4",
    seed=0,
)
