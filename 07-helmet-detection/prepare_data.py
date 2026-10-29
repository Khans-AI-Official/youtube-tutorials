"""Step 1: keep only the classes we care about and renumber them.

The original dataset has 11 classes. For a site-safety checker
we need four: person, helmet, no_helmet and vest.
"""
import shutil
from pathlib import Path

SRC = Path("construction-ppe")      # the downloaded dataset
DST = Path("ppe4")                  # our cleaned copy
KEEP = {6: 0, 0: 1, 7: 2, 2: 3}     # old class id -> new class id
NAMES = ["person", "helmet", "no_helmet", "vest"]

for split in ["train", "val", "test"]:
    (DST / "images" / split).mkdir(parents=True, exist_ok=True)
    (DST / "labels" / split).mkdir(parents=True, exist_ok=True)
    kept = boxes = missing = 0
    for label_file in sorted((SRC / "labels" / split).glob("*.txt")):
        new_lines = []
        for line in label_file.read_text().splitlines():
            cls, *box = line.split()
            if int(cls) in KEEP:
                new_lines.append(" ".join([str(KEEP[int(cls)])] + box))
        if not new_lines:
            continue                    # no useful objects in this image
        folder = SRC / "images" / split
        matches = list(folder.glob(label_file.stem + ".*"))  # .jpg or .jpeg
        if not matches:
            missing += 1                # label file with no image: skip it
            continue
        image = matches[0]
        shutil.copy(image, DST / "images" / split / image.name)
        out = DST / "labels" / split / label_file.name
        out.write_text("\n".join(new_lines) + "\n")
        kept, boxes = kept + 1, boxes + len(new_lines)
    print(f"{split:5s}: {kept} images, {boxes} boxes, "
          f"{missing} labels without an image")

yaml = (f"path: {DST.resolve()}\n"
        "train: images/train\nval: images/val\ntest: images/test\n"
        f"names: {NAMES}\n")
Path("ppe4.yaml").write_text(yaml)
print("Wrote ppe4.yaml")
