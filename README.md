# Khan's AI: YouTube tutorial code

Code from the tutorials on the [Khan's AI YouTube channel](https://www.youtube.com/@Khans-AI).

| Folder | Video | What it does |
|---|---|---|
| `01-pdf-chatbot` | Build a Chatbot That Answers From Your PDFs | Minimal RAG chatbot: pypdf + numpy + OpenAI API |
| `02-shelf-counting` | Count Products on a Shelf With Computer Vision | Train, count and export a YOLO detector with Ultralytics |
| `03-invoice-reader` | Read Invoices Automatically With Python and AI | OCR with Tesseract, fields extracted by an LLM, saved to Excel |
| `04-ai-agent-tools` | Build an AI Agent That Uses Tools | Tool-calling agent loop in plain Python, no framework |
| `05-chat-with-excel` | Chat With Your Excel Data Using Python and AI | LLM writes a JSON query plan, pandas computes the answer safely |
| `06-meeting-notes` | Transcribe and Summarize Meetings With Python | Local Whisper transcript, summary, decisions and action items |

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

## 03: Invoice reader
```bash
pip install pytesseract pillow openai pandas openpyxl
# also install the Tesseract OCR engine (see the top of invoice_reader.py)
export OPENAI_API_KEY="your-key-here"
python make_sample_invoice.py      # optional: creates invoices/sample_invoice.png
python invoice_reader.py           # reads every image in invoices/ into invoices.xlsx
```

## 04: AI agent with tools
```bash
pip install openai
export OPENAI_API_KEY="your-key-here"
python agent.py "Which product earned the most in 2026-09, and what is 15% of that?"
```

## 05: Chat with your Excel data

```
pip install pandas openpyxl openai
python make_sample_sales.py
python excel_chat.py sales.xlsx
```
The model only sees column names and 3 sample rows. It returns a JSON plan; unknown columns or operators are rejected, and no generated code is ever executed.

## 06: Meeting notes

```
pip install faster-whisper openai
python meeting_notes.py meeting.mp3        # or sample_transcript.txt
```
Saves `<name>_notes.md` with a summary, decisions and an action-item table.

## Khan's AI
Applied AI studio in Peshawar, Pakistan: computer vision, AI chatbots and agents, machine learning and AI web apps.
Need something like this built for your business?

- YouTube: https://www.youtube.com/@Khans-AI
- LinkedIn: https://www.linkedin.com/company/khans-ai/
- Fiverr: https://www.fiverr.com/khans_ai
- Upwork: https://www.upwork.com/agencies/2012969747006873204/
