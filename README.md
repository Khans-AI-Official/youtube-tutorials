# Khan's AI: YouTube tutorial code

Code from the tutorials on the [Khan's AI YouTube channel](https://www.youtube.com/@Khans-AI).

| Folder | Video | What it does |
|---|---|---|
| `01-pdf-chatbot` | Build a Chatbot That Answers From Your PDFs | Minimal RAG chatbot: pypdf + numpy + OpenAI API |
| `02-shelf-counting` | Count Products on a Shelf With Computer Vision | Train, count and export a YOLO detector with Ultralytics |

## 01: PDF chatbot
```bash
pip install pypdf numpy openai
export OPENAI_API_KEY="your-key-here"      # Windows: setx OPENAI_API_KEY "your-key-here"
python pdf_chatbot.py                      # put your file next to it as policy.pdf
```

## 02: Shelf counting
```bash
pip install ultralytics
python train_shelf.py        # needs your labelled dataset in YOLO format (see shelf.yaml)
python count_products.py     # counts products on shelf_photo.jpg
python export_model.py       # ONNX for servers, TFLite for Android
```

## Khan's AI
Applied AI studio in Peshawar, Pakistan: computer vision, AI chatbots and agents, machine learning and AI web apps.
Need something like this built for your business?

- YouTube: https://www.youtube.com/@Khans-AI
- LinkedIn: https://www.linkedin.com/company/khans-ai/
- Fiverr: https://www.fiverr.com/khans_ai
- Upwork: https://www.upwork.com/agencies/2012969747006873204/
