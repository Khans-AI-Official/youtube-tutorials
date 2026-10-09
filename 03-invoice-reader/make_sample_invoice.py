"""Create a sample invoice image to test the reader without real documents.
pip install pillow   |   python make_sample_invoice.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def font(size):
    for name in ["arial.ttf", "DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


lines = [
    ("Bright Office Supplies Ltd", 40),
    ("12 Saddar Road, Peshawar", 24),
    ("", 24),
    ("INVOICE", 36),
    ("Invoice No: INV-2048", 26),
    ("Date: 2026-10-05", 26),
    ("", 24),
    ("A4 paper, 10 reams          PKR 12,500", 26),
    ("Printer toner, 2 units       PKR 18,400", 26),
    ("Delivery                     PKR 1,100", 26),
    ("", 24),
    ("TOTAL:  PKR 32,000", 34),
]
img = Image.new("RGB", (900, 760), "white")
d = ImageDraw.Draw(img)
y = 50
for text, size in lines:
    d.text((60, y), text, fill="black", font=font(size))
    y += size + 22
Path("invoices").mkdir(exist_ok=True)
img.save("invoices/sample_invoice.png")
print("Saved invoices/sample_invoice.png")
