"""Turn a meeting recording into a summary, decisions and action items.

Whisper (run locally with faster-whisper) writes the transcript. A language
model then pulls out the summary, the decisions and the tasks, with owners
and due dates. Long meetings are processed in chunks and merged at the end.
The result is saved as a Markdown file you can paste into email or Slack.

Usage:
    pip install faster-whisper openai
    set OPENAI_API_KEY=your-key   (Windows)   or   export OPENAI_API_KEY=your-key
    python meeting_notes.py meeting.mp3          (audio or video file)
    python meeting_notes.py transcript.txt       (skip transcription)
"""
import json
import sys
from pathlib import Path

CHAT_MODEL = "gpt-4o-mini"
WHISPER_SIZE = "small"      # tiny, base, small, medium; bigger = slower but more accurate
CHUNK_WORDS = 2500


# ---------- Step 1: transcribe on your own PC ----------
def transcribe(path):
    from faster_whisper import WhisperModel
    model = WhisperModel(WHISPER_SIZE, compute_type="int8")
    segments, _ = model.transcribe(path, vad_filter=True)
    lines = []
    for s in segments:
        m, sec = divmod(int(s.start), 60)
        lines.append(f"[{m:02d}:{sec:02d}] {s.text.strip()}")
    return "\n".join(lines)


# ---------- Step 2: split long transcripts ----------
def chunk(text, size=CHUNK_WORDS):
    words = text.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)] or [""]


# ---------- Step 3: pull out what matters ----------
RULES = (
    "You take meeting notes. From the transcript, return JSON with keys: "
    "summary (3 to 5 short sentences), decisions (list of strings), "
    "actions (list of {task, owner, due}). Use only what was actually said. "
    "If an owner or due date was not mentioned, use null. Do not invent anything."
)


def extract(text, client):
    res = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": RULES},
                  {"role": "user", "content": text}],
    )
    return json.loads(res.choices[0].message.content)


def merge(parts, client):
    if len(parts) == 1:
        return parts[0]
    joined = json.dumps(parts)
    return extract("These are notes from consecutive parts of one meeting. "
                   "Merge them into one set, removing duplicates:\n" + joined, client)


# ---------- Step 4: save as Markdown ----------
def to_markdown(notes, title):
    out = [f"# {title}", "", "## Summary", notes.get("summary", ""), "", "## Decisions"]
    out += [f"- {d}" for d in notes.get("decisions") or ["None recorded"]]
    out += ["", "## Action items", "| Task | Owner | Due |", "|---|---|---|"]
    for a in notes.get("actions") or []:
        out.append(f"| {a.get('task')} | {a.get('owner') or '?'} | {a.get('due') or '?'} |")
    return "\n".join(out) + "\n"


def make_notes(path, client):
    p = Path(path)
    text = p.read_text(encoding="utf-8") if p.suffix == ".txt" else transcribe(str(p))
    notes = merge([extract(c, client) for c in chunk(text)], client)
    md = to_markdown(notes, f"Meeting notes: {p.stem}")
    out = p.with_name(p.stem + "_notes.md")
    out.write_text(md, encoding="utf-8")
    return out, notes


def main():
    from openai import OpenAI
    if len(sys.argv) < 2:
        print("Usage: python meeting_notes.py <audio, video or .txt transcript>")
        return
    out, notes = make_notes(sys.argv[1], OpenAI())
    print(f"Saved {out}  ({len(notes.get('actions') or [])} action items)")


if __name__ == "__main__":
    main()
