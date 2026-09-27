"""Chat with your PDF: a minimal RAG chatbot in plain Python.
pip install pypdf openai numpy     |  set OPENAI_API_KEY first
"""
import numpy as np
from pypdf import PdfReader
from openai import OpenAI

client = OpenAI()                      # reads OPENAI_API_KEY
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"             # any chat model you have access to


# Step 1: load the PDF and split it into overlapping chunks
def load_chunks(path, size=800, overlap=150):
    text = ""
    for page in PdfReader(path).pages:
        text += (page.extract_text() or "") + "\n"
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


# Step 2: turn text into embeddings (lists of numbers)
def embed(texts):
    res = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return np.array([d.embedding for d in res.data])


# Step 3: find the chunks closest in meaning to the question
def search(question, chunks, vectors, k=4):
    q = embed([question])[0]
    scores = vectors @ q / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(q))
    best = np.argsort(scores)[::-1][:k]
    return [chunks[i] for i in best]


# Step 4: answer using only the retrieved context
def answer(question, chunks, vectors):
    context = "\n---\n".join(search(question, chunks, vectors))
    prompt = ("Answer using only the context below. "
              "If the answer is not in the context, say you don't know.\n\n"
              f"Context:\n{context}\n\nQuestion: {question}")
    res = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}])
    return res.choices[0].message.content


if __name__ == "__main__":
    chunks = load_chunks("policy.pdf")
    vectors = embed(chunks)
    print(answer("What is the refund period?", chunks, vectors))
