"""Build Week 17 sample-code notebooks. Run: python build_code.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# ---------------------------------------------------------------- notebook 1
eval_harness = [
    ("md", "# Week 17 · Notebook 1 — A Small Eval Harness (LLM-as-Judge)\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Build a tiny **eval harness**: test cases + scorers + an aggregate report. "
           "We score with **exact-match** *and* an **LLM-as-judge** (Claude, with a Gemini "
           "alternative). **No OpenAI.**\n\n"
           "> Degrades gracefully: without an API key the judge falls back to a clear "
           "message, and exact-match still runs offline."),
    ("md", "## 0. Install + load keys safely"),
    ("code", "!pip -q install anthropic google-generativeai\n"
             "import os\n"
             "try:\n"
             "    from google.colab import userdata\n"
             "    os.environ['ANTHROPIC_API_KEY'] = userdata.get('ANTHROPIC_API_KEY')\n"
             "    os.environ['GEMINI_API_KEY'] = userdata.get('GEMINI_API_KEY')\n"
             "except Exception:\n"
             "    pass  # locally, set these in your shell environment\n"
             "print('Anthropic key set:', bool(os.environ.get('ANTHROPIC_API_KEY')))\n"
             "print('Gemini key set:', bool(os.environ.get('GEMINI_API_KEY')))"),
    ("md", "## 1. The system under test\n"
           "Any function `input -> output` works. We use Claude, but you would plug in your "
           "Final Project pipeline (RAG, agent, fine-tuned model, ...)."),
    ("code", "MODEL = 'claude-haiku-4-5-20251001'\n\n"
             "def system_under_test(question: str) -> str:\n"
             "    try:\n"
             "        import anthropic\n"
             "        client = anthropic.Anthropic()\n"
             "        msg = client.messages.create(\n"
             "            model=MODEL, max_tokens=100,\n"
             "            messages=[{'role': 'user',\n"
             "                       'content': f'Answer briefly: {question}'}])\n"
             "        return msg.content[0].text.strip()\n"
             "    except Exception as e:\n"
             "        return f'[offline/no key: {e}]'\n\n"
             "print(system_under_test('What is the capital of France?'))"),
    ("md", "## 2. Test cases\n"
           "Each case has an input and a reference of what 'good' looks like. 5-10 cases is "
           "enough to start; grow them as you find failures."),
    ("code", "test_cases = [\n"
             "    {'input': 'What is the capital of France?', 'expected': 'Paris'},\n"
             "    {'input': 'What is 2 + 2?',                 'expected': '4'},\n"
             "    {'input': 'What language is this course taught in?', 'expected': 'Python'},\n"
             "    {'input': 'Who wrote Romeo and Juliet?',    'expected': 'Shakespeare'},\n"
             "]\n"
             "print(len(test_cases), 'test cases')"),
    ("md", "## 3. Scorer A — exact-match / contains\n"
           "Objective and free. Good for single-answer tasks; brittle for free-form text "
           "('Paris.' vs 'The capital is Paris')."),
    ("code", "def contains_score(answer: str, expected: str) -> float:\n"
             "    return 1.0 if expected.lower() in answer.lower() else 0.0\n\n"
             "print(contains_score('The capital is Paris.', 'Paris'))  # 1.0\n"
             "print(contains_score('I am not sure.', 'Paris'))         # 0.0"),
    ("md", "## 4. Scorer B — LLM-as-judge (Claude)\n"
           "A strong model grades against a rubric. We ask for a single number and keep "
           "temperature low. **Judge hygiene:** clear rubric, structured output, spot-check "
           "against your own judgment, and remember judges can favor longer/own-style answers."),
    ("code", "def judge_score(answer: str, expected: str, question: str = '') -> float:\n"
             "    prompt = (\n"
             "        'You are a strict grader. Score the model answer for correctness.\\n'\n"
             "        f'Reference answer: {expected}\\n'\n"
             "        f'Model answer: {answer}\\n'\n"
             "        'Reply with ONLY 1 (correct) or 0 (incorrect).')\n"
             "    try:\n"
             "        import anthropic\n"
             "        client = anthropic.Anthropic()\n"
             "        out = client.messages.create(\n"
             "            model='claude-sonnet-4-6', max_tokens=5, temperature=0,\n"
             "            messages=[{'role': 'user', 'content': prompt}]).content[0].text\n"
             "        return 1.0 if '1' in out else 0.0\n"
             "    except Exception as e:\n"
             "        print('   (judge offline:', e, ')')\n"
             "        return float('nan')\n\n"
             "print('judge demo:', judge_score('It is Paris.', 'Paris'))"),
    ("md", "### Gemini judge alternative\n"
           "Same idea with Gemini — useful for a second opinion or if you only have a Gemini key."),
    ("code", "def gemini_judge(answer: str, expected: str) -> float:\n"
             "    try:\n"
             "        import google.generativeai as genai\n"
             "        genai.configure(api_key=os.environ['GEMINI_API_KEY'])\n"
             "        model = genai.GenerativeModel('gemini-2.5-flash')\n"
             "        prompt = (f'Reference: {expected}\\nAnswer: {answer}\\n'\n"
             "                  'Reply ONLY 1 if the answer is correct, else 0.')\n"
             "        out = model.generate_content(prompt).text\n"
             "        return 1.0 if '1' in out else 0.0\n"
             "    except Exception as e:\n"
             "        print('   (gemini judge offline:', e, ')')\n"
             "        return float('nan')"),
    ("md", "## 5. The harness — run, score, aggregate\n"
           "This is the whole point: one function that runs every case, scores it, and "
           "returns an average plus a per-case table."),
    ("code", "def run_eval(system_fn, score_fn):\n"
             "    rows, scores = [], []\n"
             "    for tc in test_cases:\n"
             "        answer = system_fn(tc['input'])\n"
             "        s = score_fn(answer, tc['expected'])\n"
             "        rows.append((tc['input'], answer, tc['expected'], s))\n"
             "        if s == s:  # skip NaN (judge offline)\n"
             "            scores.append(s)\n"
             "    avg = sum(scores) / len(scores) if scores else float('nan')\n"
             "    return avg, rows\n\n"
             "avg, rows = run_eval(system_under_test, contains_score)\n"
             "print(f'\\nExact-match average: {avg:.2f}\\n')\n"
             "for q, a, exp, s in rows:\n"
             "    print(f'  [{s}] Q: {q}\\n       A: {a}\\n       expected ~ {exp}\\n')"),
    ("md", "## 6. Run the LLM-as-judge eval\n"
           "Re-run with the judge scorer. Compare its average to exact-match — the judge "
           "often credits correct-but-differently-worded answers."),
    ("code", "judge_avg, judge_rows = run_eval(system_under_test,\n"
             "                                 lambda a, e: judge_score(a, e))\n"
             "print(f'LLM-judge average: {judge_avg:.2f}')"),
    ("md", "## 7. Track it over time\n"
           "Save the score with a label (model + prompt version). Re-run after every change "
           "to prove an improvement — and to justify a cheaper model."),
    ("code", "import datetime\n"
             "record = {'when': datetime.datetime.now().isoformat(timespec='minutes'),\n"
             "          'model': MODEL, 'exact_match': round(avg, 3),\n"
             "          'judge': None if judge_avg != judge_avg else round(judge_avg, 3)}\n"
             "print('eval record:', record)\n"
             "# Append records to a CSV/JSON in your repo to chart quality over versions."),
    ("md", "## 8. Use this in your Final Project\n"
           "- Swap `system_under_test` for **your** pipeline.\n"
           "- Add 5-10 test cases that matter for your problem.\n"
           "- Report the average score in your write-up.\n"
           "- Pair this with the **safety checklist** (hallucination, bias, prompt injection, "
           "privacy) from this week's document."),
]
build_notebook(eval_harness, os.path.join(CODE, "01_eval_harness.ipynb"))

print("wrote Week 17 notebooks to", CODE)
