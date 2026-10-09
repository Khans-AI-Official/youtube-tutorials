"""Read invoices automatically: OCR + an LLM + Excel, in plain Python.

pip install pytesseract pillow openai pandas openpyxl
Also install the Tesseract OCR engine:
  Windows: https://github.com/UB-Mannheim/tesseract/wiki   (then add it to PATH)
  Ubuntu:  sudo apt install tesseract-ocr
  macOS:   brew install tesseract
Set OPENAI_API_KEY first, then put invoice images in a folder called invoices/
"""
import json
import sys
from pathlib import Path

import pandas as pd
import pytesseract
from PIL import Image, ImageOps
from openai import OpenAI

CHAT_MODEL = "gpt-4o-mini"             # any chat model you have access to
FIELDS = ["vendor", "invoice_number", "date", "total", "currency"]


# Step 1: OCR, turn the image into text
def read_text(path):
    img = Image.open(path)
    img = ImageOps.grayscale(img)                  # cleaner input for OCR
    img = img.resize((img.width * 2, img.height * 2))
    return pytesseract.image_to_string(img)


# Step 2: ask the model for the fields, as JSON
def extract_fields(text, client):
    prompt = (
        "Extract these fields from the invoice text: "
        f"{', '.join(FIELDS)}. Reply with JSON only. "
        "Use null for any field you cannot find. Do not guess.\n\n"
        f"Invoice text:\n{text}")
    res = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0)
    return json.loads(res.choices[0].message.content)


# Step 3: check the result, flag anything for a person to review
def check(fields):
    missing = [f for f in FIELDS if not fields.get(f)]
    total = str(fields.get("total") or "").replace(",", "")
    try:
        float(total)
    except ValueError:
        missing.append("total (not a number)")
    fields["needs_review"] = ", ".join(missing)
    return fields


# Step 4: process a whole folder into one Excel file
def process_folder(folder="invoices", out="invoices.xlsx"):
    client = OpenAI()                              # reads OPENAI_API_KEY
    rows = []
    files = sorted(p for p in Path(folder).iterdir()
                   if p.suffix.lower() in {".png", ".jpg", ".jpeg"})
    for path in files:
        fields = check(extract_fields(read_text(path), client))
        fields["file"] = path.name
        rows.append(fields)
        print(path.name, "->", fields.get("vendor"), fields.get("total"))
    pd.DataFrame(rows).to_excel(out, index=False)
    print(f"Saved {len(rows)} invoices to {out}")


if __name__ == "__main__":
    process_folder(*sys.argv[1:])
