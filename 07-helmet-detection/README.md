# 07: Helmet detection with YOLO (train on your own data)

Code from the Khan's AI video "Train YOLO on Your Own Dataset in Python".
A YOLO11 nano model is fine-tuned to find people, helmets, people without a helmet, and safety vests,
then used to flag photos where someone is not wearing a helmet.

## Setup
```bash
pip install ultralytics
```
Download the Construction-PPE dataset by Ultralytics (AGPL-3.0) and unzip it next to these files as `construction-ppe/`:
https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip

## Run
```bash
python prepare_data.py   # keep 4 classes, renumber them, skip broken files, write ppe4.yaml
python train.py          # fine-tune yolo11n (CPU works; set device=0 for an NVIDIA GPU)
python evaluate.py       # precision, recall and mAP50 per class on the test split
python predict.py my_photos/*   # detections on your photos (default: 8 test images), SAFETY ALERT for no_helmet
python webcam.py         # live webcam window
python export.py         # ONNX file for use outside Python (pip install onnx onnxslim first)
```

## Using your own photos
Label them with a free tool such as Label Studio or CVAT and export in YOLO format:
one `.txt` file per image, one line per object: `class x_center y_center width height`, all between 0 and 1.
