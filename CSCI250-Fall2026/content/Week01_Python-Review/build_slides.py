"""Build slides.pptx for Week 1. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 1 — Python Review & AI Dev Environment",
     "subtitle": "CSCI 250 — Introduction to Artificial Intelligence · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "Tour the course: Canvas, weekly rhythm, how to get help",
        "Refresh the Python we use all semester",
        "Stand up your AI dev environment",
        "Make your first AI API call + run a local model",
        "First look at AI-assisted coding (Claude Code)"]},

    {"type": "section", "title": "How This Course Works"},
    {"type": "bullets", "title": "Weekly Rhythm", "bullets": [
        "Module opens Monday: document + slides + videos + code",
        "Discussion / lab / quiz due Sunday 11:59 PM PT",
        "Office hours: Tue 5–6 PM, Sat 10–11 AM PT (Zoom)",
        "Email subject prefix: \"CSCI250 -\"  (48-hr reply)",
        ("Using AI is allowed & encouraged — but you own what you submit", 1),
        ("Exams are AI-restricted; add an 'AI Use' note to assignments", 1)]},

    {"type": "section", "title": "Python Refresher"},
    {"type": "bullets", "title": "Core Data Types", "bullets": [
        "int, float, bool, str — scalars",
        "list — ordered, mutable  [1, 2, 3]",
        "tuple — ordered, immutable  (3, 4)",
        "dict — key→value  {'model': 'claude'}",
        "set — unique items  {1, 2, 3}"]},
    {"type": "code", "title": "Functions & f-strings",
     "code": "def greet(name: str, excited: bool = False) -> str:\n"
             "    msg = f\"Hello, {name}\"\n"
             "    return msg + \"!\" if excited else msg\n\n"
             "squares = [x * x for x in range(5)]\n"
             "print(f\"{len(squares)} squares: {squares}\")",
     "caption": "Type hints + comprehensions + f-strings — used all semester"},

    {"type": "section", "title": "The AI Dev Environment"},
    {"type": "two_col", "title": "Three Model Sources",
     "left_title": "Cloud APIs (need a key)",
     "left": ["Anthropic Claude + Claude Code", "Google Gemini + AI Studio"],
     "right_title": "Local (no key, no cost)",
     "right": ["Ollama (run open models)", "Hugging Face"]},
    {"type": "bullets", "title": "Setup Checklist", "bullets": [
        "Google Colab — browser notebooks, free GPU",
        "Git + GitHub account (Student Developer Pack)",
        "API keys: Claude (console.anthropic.com), Gemini (aistudio.google.com)",
        "Ollama installed locally",
        ("Never commit or share API keys — use Colab Secrets / env vars", 1)]},

    {"type": "code", "title": "Hello, AI (Claude)",
     "code": "import anthropic\n"
             "client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY\n"
             "msg = client.messages.create(\n"
             "    model=\"claude-sonnet-4-6\",\n"
             "    max_tokens=300,\n"
             "    messages=[{\"role\": \"user\",\n"
             "               \"content\": \"Explain an LLM in 2 sentences.\"}],\n"
             ")\nprint(msg.content[0].text)",
     "caption": "Full versions for Claude, Gemini, and Ollama in 02_first_ai_calls.ipynb"},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Read the syllabus + schedule",
        "Run 01_python_review.ipynb (5 exercises)",
        "Run 02_first_ai_calls.ipynb — Claude, Gemini, Ollama",
        "Install Claude Code",
        "Submit Lab A1 by Sunday 11:59 PM PT"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
