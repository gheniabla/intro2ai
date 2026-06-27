"""Build Week 12 sample-code notebook AND the starter_repo for Lab A9.
Run: python build_code.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# ============================================================ NOTEBOOK
ai_coding = [
    ("md", "## ▶ What you'll see when you run this\n"
           "- The AI's **first** `best_price` patch is **wrong** — it crashes on the empty-coupons "
           "case — and your own test catches the bug, which you then fix.\n\n"
           "**Time:** ~12 min · **Cost:** free (cheapest model: Gemini Flash / Claude Haiku / "
           "local Ollama) · **Keys:** ANTHROPIC_API_KEY"),
    ("md", "# Week 12 · Notebook 1 — The AI-as-Coder Loop\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Claude Code lives in your terminal — but the *idea* (reason → act → "
           "observe → review) works in a notebook too. Here we drive an LLM to "
           "write code against a **failing test**, exactly the way Lab A9 asks you "
           "to work, and we keep a human in the loop the whole time.\n\n"
           "> Runs in Colab. **Degrades gracefully without an API key** — the "
           "fallback shows the same workflow with a hand-written patch."),
    ("md", "## 0. Install + load key safely"),
    ("code", "!pip -q install anthropic"),
    ("code", "import os\n"
             "try:\n"
             "    from google.colab import userdata\n"
             "    os.environ['ANTHROPIC_API_KEY'] = userdata.get('ANTHROPIC_API_KEY')\n"
             "except Exception:\n"
             "    pass  # locally: export ANTHROPIC_API_KEY=...\n"
             "HAVE_KEY = bool(os.environ.get('ANTHROPIC_API_KEY'))\n"
             "print('Anthropic key set:', HAVE_KEY)"),
    ("md", "## 1. The requirement, as a failing test\n"
           "We want a function `best_price(price, coupons)` that applies the **single "
           "best** coupon (each is a percent-off int) and never returns a negative price. "
           "We capture that as a test *first*."),
    ("code", "TARGET = '''\n"
             "def best_price(price, coupons):\n"
             "    \"\"\"Return price after applying the single best percent-off coupon.\n"
             "    coupons: list of ints (percent off). Empty list => price unchanged.\n"
             "    Never returns a negative number. Round to 2 decimals.\"\"\"\n"
             "    raise NotImplementedError\n"
             "'''\n\n"
             "TEST = '''\n"
             "def run_tests(best_price):\n"
             "    assert best_price(100, []) == 100\n"
             "    assert best_price(100, [10, 25, 5]) == 75.0   # best = 25% off\n"
             "    assert best_price(50, [200]) == 0.0           # clamp at 0\n"
             "    assert best_price(19.99, [10]) == 17.99\n"
             "    return 'all tests passed'\n"
             "'''\n"
             "print(TARGET); print(TEST)"),
    ("md", "## 2. Ask Claude to make the test pass\n"
           "Note the prompt: **context** (the stub), **constraints** (signature, no "
           "negatives, rounding), **acceptance criteria** (these asserts). This is the "
           "Section-3 recipe from the lecture."),
    ("code", "def ask_claude_for_code(target, test):\n"
             "    import anthropic\n"
             "    client = anthropic.Anthropic()\n"
             "    prompt = (\n"
             "        'Implement the function below so it passes the tests. '\n"
             "        'Keep the exact signature. Return ONLY a python code block.\\n\\n'\n"
             "        'STUB:\\n' + target + '\\nTESTS:\\n' + test\n"
             "    )\n"
             "    msg = client.messages.create(\n"
             "        model='claude-sonnet-4-6', max_tokens=600,\n"
             "        messages=[{'role': 'user', 'content': prompt}])\n"
             "    return msg.content[0].text\n\n"
             "def extract_code(text):\n"
             "    if '```' in text:\n"
             "        text = text.split('```')[1]\n"
             "        if text.startswith('python'):\n"
             "            text = text[len('python'):]\n"
             "    return text.strip()\n\n"
             "# NOTE: this fallback is the AI's *first* attempt — and it is BUGGY on purpose.\n"
             "# It forgets the empty-coupons case, so max([]) raises ValueError. Your job\n"
             "# (Section 3 below) is to CATCH that with the test and fix it.\n"
             "FALLBACK = '''\n"
             "def best_price(price, coupons):\n"
             "    best = max(coupons)              # BUG: crashes when coupons == []\n"
             "    result = price * (1 - best / 100)\n"
             "    return round(max(result, 0.0), 2)\n"
             "'''\n\n"
             "if HAVE_KEY:\n"
             "    code = extract_code(ask_claude_for_code(TARGET, TEST))\n"
             "    print('--- model wrote ---')\n"
             "else:\n"
             "    code = FALLBACK.strip()\n"
             "    print('--- no key: using fallback patch (same workflow) ---')\n"
             "print(code)"),
    ("md", "## 3. Review, then run the test yourself\n"
           "**Never trust green you didn't run.** We exec the model's code in a scratch "
           "namespace and run the asserts. Read the code above *before* you run this.\n\n"
           "> **Notice the AI's first attempt is wrong** — your job is to catch it with tests "
           "and fix it. The cell below is wrapped in `try/except`: when the first patch crashes "
           "on `best_price(100, [])`, that failure is the signal. Patch `code` to add the "
           "empty-coupons guard (`if not coupons: ...`), then re-run until you see "
           "`all tests passed`."),
    ("code", "ns = {}\n"
             "exec(code, ns)             # define best_price\n"
             "exec(TEST, ns)             # define run_tests\n"
             "try:\n"
             "    print(ns['run_tests'](ns['best_price']))\n"
             "except Exception as e:\n"
             "    print('Test FAILED — the AI got it wrong:', repr(e))\n"
             "    print('Fix the bug in `code` above (handle empty coupons), then re-run.')"),
    ("md", "## 4. Add YOUR own edge case\n"
           "The AI passed *our* tests. Did it handle a 0% coupon? Duplicate coupons? "
           "Add an assert the model wasn't given and re-run. This is the human-review "
           "step you'll repeat in Lab A9."),
    ("code", "def my_extra_tests(best_price):\n"
             "    assert best_price(100, [0]) == 100      # 0% off\n"
             "    assert best_price(100, [10, 10]) == 90  # duplicates\n"
             "    # TODO: add one more of your own\n"
             "    return 'my extra tests passed'\n\n"
             "print(my_extra_tests(ns['best_price']))"),
    ("md", "## 5. Reflection (for A9)\n"
           "In ~200 words: where did the AI help most, did it over-reach or hallucinate, "
           "and what did *you* have to verify? Then go do the real lab in "
           "`code/starter_repo/` with **Claude Code**."),
    ("code", "# notes:\n"),
]
build_notebook(ai_coding, os.path.join(CODE, "01_ai_assisted_coding.ipynb"))

# ============================================================ STARTER REPO
REPO = os.path.join(CODE, "starter_repo")
PKG = os.path.join(REPO, "mathkit")
TESTS = os.path.join(REPO, "tests")
for d in (PKG, TESTS):
    os.makedirs(d, exist_ok=True)


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


# ---- package __init__
write(os.path.join(PKG, "__init__.py"),
      '"""mathkit — a tiny pricing toolkit for CSCI 250 Lab A9."""\n'
      "from .discounts import apply_discount, best_price  # noqa: F401\n")

# ---- discounts.py : one WORKING fn + one INCOMPLETE fn
write(os.path.join(PKG, "discounts.py"),
      '"""Pricing helpers.\n\n'
      "`apply_discount` already works and has passing tests.\n"
      "`best_price` is INCOMPLETE — your Lab A9 task is to finish it (with AI help)\n"
      "so the failing tests in tests/test_discounts.py pass. Keep the signatures.\n"
      '"""\n\n\n'
      "def apply_discount(price, percent_off):\n"
      '    """Apply a single percent-off discount.\n\n'
      "    price: non-negative number.\n"
      "    percent_off: int/float percent (e.g. 25 means 25%% off).\n"
      "    Returns the new price, never negative, rounded to 2 decimals.\n"
      '    """\n'
      "    if price < 0:\n"
      '        raise ValueError("price must be non-negative")\n'
      "    result = price * (1 - percent_off / 100)\n"
      "    return round(max(result, 0.0), 2)\n\n\n"
      "def best_price(price, coupons):\n"
      '    """Apply the SINGLE BEST coupon from a list of percent-off values.\n\n'
      "    price:   non-negative number.\n"
      "    coupons: list of percent-off values (ints/floats). May be empty.\n\n"
      "    Rules (see tests/test_discounts.py):\n"
      "      * empty list  -> price unchanged (rounded to 2 dp)\n"
      "      * otherwise   -> apply only the largest discount\n"
      "      * never return a negative number\n"
      "      * round to 2 decimals\n\n"
      "    TODO (Lab A9): implement this. Hint: you can reuse apply_discount().\n"
      '    """\n'
      "    raise NotImplementedError(\"best_price is your Lab A9 task\")\n")

# ---- failing tests for best_price (+ passing tests for apply_discount)
write(os.path.join(TESTS, "test_discounts.py"),
      '"""Tests for mathkit.discounts.\n\n'
      "Run from starter_repo/:  python -m pytest -q\n\n"
      "The apply_discount tests already PASS. The best_price tests FAIL until you\n"
      "implement best_price() in mathkit/discounts.py (that is Lab A9).\n"
      '"""\n'
      "import pytest\n"
      "from mathkit.discounts import apply_discount, best_price\n\n\n"
      "# ---- apply_discount: these already pass --------------------------------\n"
      "def test_apply_discount_basic():\n"
      "    assert apply_discount(100, 25) == 75.0\n\n\n"
      "def test_apply_discount_clamps_at_zero():\n"
      "    assert apply_discount(50, 200) == 0.0\n\n\n"
      "def test_apply_discount_rejects_negative_price():\n"
      "    with pytest.raises(ValueError):\n"
      "        apply_discount(-1, 10)\n\n\n"
      "# ---- best_price: these FAIL until you implement it ---------------------\n"
      "def test_best_price_empty_coupons_unchanged():\n"
      "    assert best_price(100, []) == 100.0\n\n\n"
      "def test_best_price_picks_largest_discount():\n"
      "    assert best_price(100, [10, 25, 5]) == 75.0\n\n\n"
      "def test_best_price_clamps_at_zero():\n"
      "    assert best_price(50, [200]) == 0.0\n\n\n"
      "def test_best_price_rounds_to_two_decimals():\n"
      "    assert best_price(19.99, [10]) == 17.99\n")

# ---- pytest config so `mathkit` imports without install
write(os.path.join(REPO, "pytest.ini"),
      "[pytest]\n"
      "pythonpath = .\n"
      "testpaths = tests\n")

# ---- a CLAUDE.md so Claude Code has project memory
write(os.path.join(REPO, "CLAUDE.md"),
      "# mathkit — project notes for Claude Code\n\n"
      "Tiny pricing toolkit used in CSCI 250 Lab A9.\n\n"
      "## How to run tests\n"
      "```bash\n"
      "python -m pytest -q\n"
      "```\n\n"
      "## The task\n"
      "Implement `best_price(price, coupons)` in `mathkit/discounts.py` so the\n"
      "failing tests in `tests/test_discounts.py` pass. Keep the signature.\n"
      "Reuse `apply_discount` where it makes sense. Do not edit the tests.\n\n"
      "## Conventions\n"
      "- Prices are rounded to 2 decimals and never negative.\n"
      "- No new dependencies.\n")

# ---- README for students
write(os.path.join(REPO, "README.md"),
      "# Lab A9 starter repo — `mathkit`\n\n"
      "A tiny package with one working function and one **incomplete** function.\n\n"
      "## Your task\n"
      "Make the failing tests pass by implementing `best_price()` in\n"
      "`mathkit/discounts.py` — using an AI assistant (ideally **Claude Code**).\n\n"
      "## Steps\n"
      "```bash\n"
      "python -m pytest -q      # 1. see the best_price tests FAIL\n"
      "claude                   # 2. start Claude Code; ask for a PLAN first\n"
      "                         # 3. implement best_price, READ the diff\n"
      "python -m pytest -q      # 4. all green when done\n"
      "```\n\n"
      "Then add one edge-case test of your own, commit on a feature branch,\n"
      "and write the 200-word reflection. See the Week 12 document for details.\n")

# NOTE: no SOLUTION_NOTES.md is generated. The reference solution is kept by the
# instructor OUTSIDE this repo so the starter_repo never leaks the answer to students.

print("wrote Week 12 notebook + starter_repo to", CODE)
