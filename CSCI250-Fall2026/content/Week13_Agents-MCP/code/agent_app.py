"""agent_app.py — serve a tool-using agent over HTTP (CSCI 250, Week 13 / S2).

Run:
    export ANTHROPIC_API_KEY=...        # optional; falls back without it
    python agent_app.py
    # then:
    curl -X POST localhost:5000/ask -H "Content-Type: application/json" \
         -d '{"message": "What is 12 + 30, and the price of coffee?"}'

NEVER hard-code your API key here — it is read from the environment.
"""
import os
import re
from flask import Flask, request, jsonify

# ----------------------------------------------------------------- tools
def add(a, b):
    """Add two numbers."""
    return a + b

def get_price(item):
    """Look up a menu price in dollars."""
    return {"coffee": 4, "tea": 3, "cocoa": 5}.get(str(item).lower(), 0)

TOOLS = {"add": add, "get_price": get_price}

TOOL_SCHEMAS = [
    {"name": "add", "description": "Add two numbers.",
     "input_schema": {"type": "object",
        "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
        "required": ["a", "b"]}},
    {"name": "get_price", "description": "Look up a menu price in dollars.",
     "input_schema": {"type": "object",
        "properties": {"item": {"type": "string"}}, "required": ["item"]}},
]

# ----------------------------------------------------------------- agents
def run_claude_agent(user_msg, max_turns=5):
    """Explicit reason->act->observe loop using Claude tool calling."""
    import anthropic
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": user_msg}]
    for _ in range(max_turns):                       # bounded loop (safety)
        resp = client.messages.create(
            model="claude-sonnet-4-6", max_tokens=600,
            tools=TOOL_SCHEMAS, messages=messages)
        if resp.stop_reason != "tool_use":
            return "".join(b.text for b in resp.content if b.type == "text")
        messages.append({"role": "assistant", "content": resp.content})
        results = []
        for b in resp.content:
            if b.type == "tool_use":
                out = TOOLS[b.name](**b.input)        # ACT
                results.append({"type": "tool_result",
                                "tool_use_id": b.id, "content": str(out)})  # OBSERVE
        messages.append({"role": "user", "content": results})
    return "stopped: hit max turns"


def run_fallback_agent(user_msg, max_turns=5):
    """No-key stand-in that runs the SAME loop with a rule-based 'model'."""
    calls = []
    m = re.search(r"(\d+)\s*\+\s*(\d+)", user_msg)
    if m:
        calls.append(("add", {"a": int(m.group(1)), "b": int(m.group(2))}))
    for item in ("coffee", "tea", "cocoa"):
        if item in user_msg.lower():
            calls.append(("get_price", {"item": item}))
    obs = []
    for name, args in calls[:max_turns]:
        obs.append(f"{name}={TOOLS[name](**args)}")
    return "(fallback) " + (", ".join(obs) if obs else "no tool matched")


def get_run_agent():
    return run_claude_agent if os.environ.get("ANTHROPIC_API_KEY") else run_fallback_agent


# ----------------------------------------------------------------- flask
def create_app():
    app = Flask(__name__)
    run_agent = get_run_agent()

    @app.route("/ask", methods=["POST"])
    def ask():
        msg = request.get_json(force=True).get("message", "")
        return jsonify({"answer": run_agent(msg)})

    @app.route("/health")
    def health():
        return jsonify({"ok": True})

    return app


if __name__ == "__main__":
    create_app().run(port=5000)
