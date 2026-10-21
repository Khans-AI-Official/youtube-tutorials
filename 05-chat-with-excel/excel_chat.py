"""Chat with your Excel or CSV file in plain English.

The model never sees your whole file. It reads the column names and a few
sample rows, then writes a small JSON "query plan". Python checks the plan
and runs it with pandas on your real data, so every number is computed,
not guessed. No generated code is ever executed.

Usage:
    pip install pandas openpyxl openai
    set OPENAI_API_KEY=your-key   (Windows)   or   export OPENAI_API_KEY=your-key
    python excel_chat.py sales.xlsx
"""
import json
import sys

import pandas as pd

CHAT_MODEL = "gpt-4o-mini"
OPS = {"==", "!=", ">", ">=", "<", "<=", "contains"}
AGGS = {"sum", "mean", "count", "max", "min"}


# ---------- Step 1: load the table and describe it ----------
def load_table(path):
    if path.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    return pd.read_csv(path)


def describe(df):
    cols = ", ".join(f"{c} ({t})" for c, t in df.dtypes.astype(str).items())
    sample = df.head(3).to_csv(index=False)
    return f"Columns: {cols}\nSample rows:\n{sample}"


# ---------- Step 2: ask the model for a query plan ----------
PLAN_RULES = (
    "Turn the question into a JSON query plan for the table below. "
    "Keys: filters (list of {column, op, value}; op is one of == != > >= < <= contains), "
    "group_by (column or null), metric (column or null), "
    "agg (sum, mean, count, max or min), sort (desc or asc), limit (number or null). "
    "Use only column names that exist. Reply with JSON only."
)


def ask_plan(question, schema, client):
    res = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": PLAN_RULES},
            {"role": "user", "content": f"{schema}\nQuestion: {question}"},
        ],
    )
    return json.loads(res.choices[0].message.content)


# ---------- Step 3: check the plan and run it with pandas ----------
def run_plan(df, plan):
    for f in plan.get("filters") or []:
        col, op, val = f["column"], f["op"], f["value"]
        if col not in df.columns or op not in OPS:
            raise ValueError(f"Unsafe or unknown filter: {f}")
        s = df[col]
        if op == "contains":
            df = df[s.astype(str).str.contains(str(val), case=False, na=False)]
        else:
            if pd.api.types.is_numeric_dtype(s):
                val = float(val)
            df = df[{"==": s == val, "!=": s != val, ">": s > val,
                     ">=": s >= val, "<": s < val, "<=": s <= val}[op]]

    group, metric = plan.get("group_by"), plan.get("metric")
    agg = plan.get("agg") or "sum"
    for c in (group, metric):
        if c and c not in df.columns:
            raise ValueError(f"Unknown column: {c}")
    if agg not in AGGS:
        raise ValueError(f"Unknown aggregation: {agg}")

    if group:
        out = df.groupby(group)[metric].agg(agg) if metric else df.groupby(group).size()
        out = out.sort_values(ascending=plan.get("sort") == "asc")
        if plan.get("limit"):
            out = out.head(int(plan["limit"]))
        return out.reset_index(name="value")
    if metric:
        return pd.DataFrame({"value": [df[metric].agg(agg)]})
    return pd.DataFrame({"value": [len(df)]})


# ---------- Step 4: turn the result into a short answer ----------
def explain(question, result, client):
    res = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        messages=[{"role": "user", "content":
                   "Answer the question in one or two sentences using ONLY this result table. "
                   f"Question: {question}\nResult:\n{result.to_csv(index=False)}"}],
    )
    return res.choices[0].message.content.strip()


def ask(df, question, client):
    plan = ask_plan(question, describe(df), client)
    result = run_plan(df, plan)
    return explain(question, result, client), result


def main():
    from openai import OpenAI
    if len(sys.argv) < 2:
        print("Usage: python excel_chat.py <file.xlsx or file.csv>")
        return
    df = load_table(sys.argv[1])
    client = OpenAI()
    print(f"Loaded {len(df)} rows. Ask a question (or press Enter to quit).")
    while True:
        q = input("\nYou: ").strip()
        if not q:
            break
        try:
            answer, table = ask(df, q, client)
            print("\n" + table.to_string(index=False))
            print("\nAI:", answer)
        except ValueError as e:
            print("Could not answer safely:", e)


if __name__ == "__main__":
    main()
