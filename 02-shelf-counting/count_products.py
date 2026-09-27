"""Count products on a shelf photo with a trained YOLO model.
pip install ultralytics
"""
from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")   # your trained weights
result = model("shelf_photo.jpg", conf=0.5)[0]

count = len(result.boxes)
print(f"Products on shelf: {count}")
result.save("counted.jpg")                            # photo with boxes drawn
