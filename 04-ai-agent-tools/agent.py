"""A tiny AI agent that uses tools, in plain Python (no framework).

pip install openai      |   set OPENAI_API_KEY first
python agent.py "Which product earned the most last month, and what is 15% of that?"
"""
import csv
import json
import sys
from datetime import date

from openai import OpenAI

CHAT_MODEL = "gpt-4o-mini"             # any model that supports tool calling
MAX_STEPS = 6                          # safety limit on the loop


# Step 1: the tools are ordinary Python functions
def get_sales(month):
    """Total sales per product for a month like '2026-09', from sales.csv."""
    totals = {}
    with open("sales.csv", newline="") as f:
        for row in csv.DictReader(f):
            if row["date"].startswith(month):
                totals[row["product"]] = totals.get(row["product"], 0) + float(row["amount"])
    return totals


def calculate(expression):
    """Evaluate simple arithmetic like '0.15 * 41250'."""
    if not set(expression) <= set("0123456789.+-*/() "):
        return "error: only numbers and + - * / ( ) are allowed"
    return eval(expression)


def today():
    return date.today().isoformat()


TOOLS = {"get_sales": get_sales, "calculate": calculate, "today": today}


# Step 2: describe the tools so the model knows when to use them
def spec(name, description, params=None):
    props = {p: {"type": "string"} for p in (params or [])}
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object", "properties": props,
                       "required": list(props)}}}


TOOL_SPECS = [
    spec("get_sales", "Total sales per product for a month, format YYYY-MM.", ["month"]),
    spec("calculate", "Evaluate an arithmetic expression.", ["expression"]),
    spec("today", "Today's date in YYYY-MM-DD format."),
]


# Step 3: the agent loop: think, call a tool, look at the result, repeat
def run_agent(question, client):
    messages = [
        {"role": "system", "content": "You are a careful business assistant. "
         "Use the tools for any data or maths. Never guess numbers."},
        {"role": "user", "content": question}]
    for step in range(MAX_STEPS):
        res = client.chat.completions.create(
            model=CHAT_MODEL, messages=messages, tools=TOOL_SPECS)
        msg = res.choices[0].message
        if not msg.tool_calls:                     # no tool needed: final answer
            return msg.content
        messages.append(msg)
        for call in msg.tool_calls:                # Step 4: run each tool
            args = json.loads(call.function.arguments or "{}")
            result = TOOLS[call.function.name](**args)
            print(f"  [tool] {call.function.name}({args}) -> {result}")
            messages.append({"role": "tool", "tool_call_id": call.id,
                             "content": json.dumps(result)})
    return "Stopped: too many steps. Please check the question."


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "Which product earned the most in 2026-09?"
    print(run_agent(q, OpenAI()))
