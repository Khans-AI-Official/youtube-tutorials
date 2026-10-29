"""Step 4: use the model on new images and flag anyone without a helmet."""
import sys
from pathlib import Path
from ultralytics import YOLO

model = YOLO("runs/detect/ppe4/weights/best.pt")
images = sys.argv[1:] or sorted(Path("ppe4/images/test").glob("*"))[:8]

results = model.predict(images, imgsz=480, conf=0.4, device="cpu", save=True)
for result in results:
    counts = {}
    for cls in result.boxes.cls.tolist():
        name = model.names[int(cls)]
        counts[name] = counts.get(name, 0) + 1
    alert = "  <-- SAFETY ALERT" if counts.get("no_helmet") else ""
    print(f"{Path(result.path).name:16s} {counts}{alert}")
