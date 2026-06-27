"""Build slides.pptx for Week 12. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 12 — AI-Assisted Software Development",
     "subtitle": "Claude Code & agentic coding · CSCI 250 · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "From autocomplete → chat → agentic coding",
        "Install & drive Claude Code (plan → edit → run → review)",
        "Prompt for code: context, constraints, acceptance criteria",
        "Review, test, and secure AI-generated code",
        "A sane git workflow + when AI helps vs. hurts",
        "Lab A6: finish a TESTED feature with AI help"]},

    {"type": "section", "title": "From Autocomplete to Agents"},
    {"type": "two_col", "title": "Three Kinds of AI Help",
     "left_title": "You integrate",
     "left": ["Autocomplete: next few tokens", "Chat: paste in, paste back",
              "No project awareness"],
     "right_title": "Agent integrates",
     "right": ["Claude Code reads your files", "Runs commands & tests",
               "Edits in a reason→act→observe loop"]},

    {"type": "section", "title": "Installing & Driving Claude Code"},
    {"type": "code", "title": "Install & Start",
     "code": "# Node 18+ required\n"
             "npm install -g @anthropic-ai/claude-code\n\n"
             "cd my-project\n"
             "claude                 # interactive session\n"
             "claude -p \"what does this repo do?\"   # one-shot\n\n"
             "# in-session: /init  /clear  /review  (Esc = interrupt)",
     "caption": "/init writes a CLAUDE.md the agent reloads every session"},

    {"type": "section", "title": "Prompting for Code"},
    {"type": "bullets", "title": "Context · Constraints · Criteria", "bullets": [
        "Context: what the project is, which file, what works",
        "Constraints: stack, style, what NOT to change, edge cases",
        "Criteria: how we both know it's done — usually 'tests pass'",
        ("Bad: 'add caching'", 1),
        ("Good: 'cache get_rate() in pricing.py, keep the signature,", 1),
        ("add a pytest proving the 2nd call doesn't refetch'", 1)]},
    {"type": "bullets", "title": "Plan First, Then Edit", "bullets": [
        "Ask for a 4–6 step plan BEFORE any edits",
        "Use Claude Code's plan mode — investigate, don't write",
        "Reading the plan catches wrong assumptions early",
        ("Highest-value habit of the week: separate planning from editing", 1)]},

    {"type": "section", "title": "Review · Test · Secure"},
    {"type": "code", "title": "Test-Driven AI Coding",
     "code": "# 1. a FAILING test captures the requirement\n"
             "# 2. ask Claude to make it pass\n"
             "# 3. run tests yourself — then READ the diff\n\n"
             "python -m pytest -q\n"
             "git diff            # does it do that, and ONLY that?",
     "caption": "Green tests are a contract the AI can't talk its way out of"},
    {"type": "bullets", "title": "Securing AI Code", "bullets": [
        "Secrets hard-coded instead of read from env",
        "Injection: input into SQL / shell / eval",
        "Unsafe deserialization: pickle/eval on untrusted data",
        "Dependencies you didn't vet",
        ("/security-review and /review help — but YOU sign off", 1)]},

    {"type": "two_col", "title": "When AI Helps vs. Hurts",
     "left_title": "Helps",
     "left": ["Boilerplate, scaffolding, tests", "Explaining unfamiliar code",
              "Refactors with tests as safety net", "Repetitive multi-file edits"],
     "right_title": "Hurts",
     "right": ["Novel algorithms, subtle bugs", "Concurrency / numerical edge cases",
               "Anything you can't verify", "Code you skim instead of read"]},

    {"type": "code", "title": "Git Workflow with AI",
     "code": "git checkout -b feature/discount-codes\n"
             "# ... AI helps implement + test ...\n"
             "git add -p          # stage small, reviewed chunks\n"
             "git commit -m \"Add discount validation + tests\"\n"
             "git diff main       # read it all before merging",
     "caption": "Small commits, branch per feature, read every diff, disclose AI use"},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Install Claude Code; try /init on a repo",
        "Open code/starter_repo — run pytest, see failing tests",
        "Plan with the AI, then implement best_price",
        "Make tests green; add one edge-case test of your own",
        "Submit Lab A6 + reflection by Sunday 11:59 PM PT"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
