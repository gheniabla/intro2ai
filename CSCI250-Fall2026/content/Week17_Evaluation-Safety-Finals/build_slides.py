"""Build slides.pptx for Week 17. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 17 — Evaluation, Safety & Finals",
     "subtitle": "CSCI 250 — Introduction to Artificial Intelligence · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "Evaluate GenAI: exact-match, rubric, LLM-as-judge",
        "Build a small eval harness (score over test cases)",
        "GenAI safety: hallucination, bias, prompt injection, privacy",
        "Limits & responsible use",
        "Course wrap-up + Final Project logistics",
        ("Final Project due Friday, Dec 19, 11:59 PM PT", 1)]},

    {"type": "section", "title": "Why Evaluation Matters"},
    {"type": "bullets", "title": "Turn Vibes Into Numbers", "bullets": [
        "GenAI is non-deterministic — 'it looked good once' is not a test",
        "You can't tell if a change helped without measuring",
        "Lets you justify a cheaper/faster model",
        "Loop: test cases → run → score → aggregate → compare",
        ("Re-run on every prompt or model change", 1)]},

    {"type": "section", "title": "Picking a Metric"},
    {"type": "two_col", "title": "Match Metric to Task",
     "left_title": "Objective",
     "left": ["exact-match / contains",
              "one right answer (class, extract, math)",
              "cheap but brittle for free text"],
     "right_title": "Open-ended",
     "right": ["rubric / structured checks",
               "LLM-as-judge (Claude / Gemini)",
               "nuance exact-match misses"]},
    {"type": "code", "title": "LLM-as-Judge (Claude)",
     "code": "import anthropic\n"
             "client = anthropic.Anthropic()\n"
             "prompt = f'''You are a strict grader. Score 1-5 for correctness.\n"
             "Question: {question}\n"
             "Reference answer: {reference}\n"
             "Model answer: {answer}\n"
             "Reply with ONLY a number 1-5.'''\n"
             "score = client.messages.create(\n"
             "    model='claude-sonnet-4-6', max_tokens=10,\n"
             "    messages=[{'role': 'user', 'content': prompt}],\n"
             ").content[0].text",
     "caption": "Judge hygiene: clear rubric, structured output, low temp, watch bias",
     "code_size": 14},

    {"type": "section", "title": "Building an Eval Harness"},
    {"type": "code", "title": "It's Just Cases + Scorer + Average",
     "code": "test_cases = [\n"
             "    {'input': 'Capital of France?', 'expected': 'Paris'},\n"
             "    {'input': '2 + 2?',            'expected': '4'},\n"
             "]\n\n"
             "def run_eval(system_fn, score_fn):\n"
             "    scores = [score_fn(system_fn(tc['input']), tc['expected'])\n"
             "              for tc in test_cases]\n"
             "    return sum(scores) / len(scores)   # average score",
     "caption": "Keep it in version control; full LLM-judge version in the notebook"},

    {"type": "section", "title": "GenAI Safety"},
    {"type": "bullets", "title": "Know the Failure Modes", "bullets": [
        "Hallucination: confident falsehoods → ground w/ RAG, cite, verify",
        "Bias: unfair across groups → test diverse inputs, human in loop",
        "Prompt injection: untrusted text hijacks system → separate data/instructions",
        "Privacy/IP: don't send secrets/PII; respect copyright; disclose AI media",
        ("Limits: LLMs predict plausible text, not truth — keep humans accountable", 1)]},
    {"type": "bullets", "title": "Prompt Injection — Defend", "bullets": [
        "Separate TRUSTED instructions from UNTRUSTED data",
        "Never blindly eval/exec model output",
        "Constrain tools & permissions; least privilege",
        "Validate outputs before acting on them"]},

    {"type": "section", "title": "Wrap-Up & Final Project"},
    {"type": "bullets", "title": "Final Project — Due Dec 19, 11:59 PM PT", "bullets": [
        "Working notebook/app: a runnable GenAI pipeline (keys via Secrets)",
        "Eval results: run your harness, report the score",
        "1-2 page write-up incl. a safety note",
        "5-minute recorded demo posted to Canvas",
        ("AI-Use note (required, as all semester)", 1)]},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Run 01_eval_harness.ipynb (LLM-as-judge over test cases)",
        "Review the safety checklist against your project",
        "Finish + record your Final Project demo",
        "Submit the Final Project by Fri Dec 19, 11:59 PM PT",
        "Congratulations on finishing CSCI 250!"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
