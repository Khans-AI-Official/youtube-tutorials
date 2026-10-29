"""Step 3: measure the trained model on the test images it never saw."""
from ultralytics import YOLO

model = YOLO("runs/detect/ppe4/weights/best.pt")
metrics = model.val(data="ppe4.yaml", split="test", imgsz=480, device="cpu")

print(f"\nmAP50 (all classes): {metrics.box.map50:.3f}")
for i, name in model.names.items():
    p, r, ap50, ap = metrics.box.class_result(i)
    print(f"{name:10s} precision {p:.2f}  recall {r:.2f}  mAP50 {ap50:.2f}")
