"""Build Week 1 sample-code notebooks. Run: python build_code.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# ---------------------------------------------------------------- notebook 1
python_review = [
    ("md", "# Week 1 · Notebook 1 — Python Review\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Refresh the Python we use all semester. Run each cell, then complete the "
           "5 exercises at the bottom."),
    ("md", "## 1. Data types"),
    ("code", "scalars = (42, 3.14, True, 'ai')\n"
             "nums = [1, 2, 3]            # list (mutable)\n"
             "point = (3, 4)              # tuple (immutable)\n"
             "config = {'model': 'claude-sonnet-4-6', 'temp': 0.7}  # dict\n"
             "unique = {1, 2, 2, 3}       # set\n"
             "print(scalars, nums, point, config, unique)"),
    ("md", "## 2. Control flow"),
    ("code", "for i in range(5):\n"
             "    print(i, 'even' if i % 2 == 0 else 'odd')"),
    ("md", "## 3. Functions (with type hints)"),
    ("code", "def greet(name: str, excited: bool = False) -> str:\n"
             "    msg = f'Hello, {name}'\n"
             "    return msg + '!' if excited else msg\n\n"
             "print(greet('CSCI 250'))\n"
             "print(greet('AI', excited=True))"),
    ("md", "## 4. Comprehensions & f-strings"),
    ("code", "squares = [x * x for x in range(10)]\n"
             "evens = [x for x in squares if x % 2 == 0]\n"
             "print(f'squares={squares}')\n"
             "print(f'{len(evens)} even squares: {evens}')"),
    ("md", "## 5. Modules"),
    ("code", "import math, statistics\n"
             "data = [2, 4, 4, 4, 5, 5, 7, 9]\n"
             "print('mean =', statistics.mean(data))\n"
             "print('stdev =', round(statistics.stdev(data), 3))\n"
             "print('sqrt(2) =', math.sqrt(2))"),
    ("md", "---\n## Exercises (complete these for A1)\n"
           "1. Write a function `is_palindrome(s: str) -> bool`.\n"
           "2. Build a dict mapping each word in a sentence to its length.\n"
           "3. Use a comprehension to extract all numbers divisible by 3 from `range(50)`.\n"
           "4. Write `word_count(text: str) -> dict` returning word→count.\n"
           "5. Given `temps_c = [0, 20, 37, 100]`, build `temps_f` with a comprehension."),
    ("code", "# Your solutions here\n"),
]
build_notebook(python_review, os.path.join(CODE, "01_python_review.ipynb"))

# ---------------------------------------------------------------- notebook 2
first_calls = [
    ("md", "# Week 1 · Notebook 2 — Hello, AI (Your First Calls)\n"
           "**CSCI 250 · Fall 2026**\n\n"
           "Send the *same prompt* to three model sources and compare:\n"
           "- **Anthropic Claude** (cloud)\n- **Google Gemini** (cloud)\n- **Ollama** (local)\n\n"
           "> **Keys:** In Colab use the 🔑 *Secrets* panel and `userdata.get('NAME')`. "
           "Locally use environment variables. **Never commit keys.**"),
    ("md", "## 0. Install SDKs"),
    ("code", "!pip -q install anthropic google-generativeai ollama"),
    ("md", "## 1. Load API keys safely"),
    ("code", "import os\n"
             "try:\n"
             "    from google.colab import userdata  # Colab\n"
             "    os.environ['ANTHROPIC_API_KEY'] = userdata.get('ANTHROPIC_API_KEY')\n"
             "    os.environ['GEMINI_API_KEY'] = userdata.get('GEMINI_API_KEY')\n"
             "except Exception:\n"
             "    pass  # locally, set these in your shell environment\n"
             "print('Anthropic key set:', bool(os.environ.get('ANTHROPIC_API_KEY')))\n"
             "print('Gemini key set:', bool(os.environ.get('GEMINI_API_KEY')))"),
    ("md", "## 2. The shared prompt"),
    ("code", "PROMPT = 'In two sentences, explain what a large language model is to a new CS student.'"),
    ("md", "## 3. Anthropic Claude"),
    ("code", "import anthropic\n"
             "client = anthropic.Anthropic()\n"
             "msg = client.messages.create(\n"
             "    model='claude-sonnet-4-6',\n"
             "    max_tokens=300,\n"
             "    messages=[{'role': 'user', 'content': PROMPT}],\n"
             ")\n"
             "print('CLAUDE:\\n', msg.content[0].text)"),
    ("md", "## 4. Google Gemini"),
    ("code", "import google.generativeai as genai\n"
             "genai.configure(api_key=os.environ['GEMINI_API_KEY'])\n"
             "model = genai.GenerativeModel('gemini-2.5-flash')\n"
             "resp = model.generate_content(PROMPT)\n"
             "print('GEMINI:\\n', resp.text)"),
    ("md", "## 5. Local model with Ollama\n"
           "Install Ollama from ollama.com, then in a terminal: `ollama pull llama3.2`.\n"
           "(In Colab you can instead `!curl -fsSL https://ollama.com/install.sh | sh` and run the server.)"),
    ("code", "import ollama\n"
             "try:\n"
             "    out = ollama.chat(model='llama3.2',\n"
             "                      messages=[{'role': 'user', 'content': PROMPT}])\n"
             "    print('OLLAMA:\\n', out['message']['content'])\n"
             "except Exception as e:\n"
             "    print('Ollama not running locally yet:', e)"),
    ("md", "## 6. Compare\n"
           "Write 150 words: how did the three answers differ in length, tone, and accuracy? "
           "Which would you trust for a beginner, and why? (This is your A1 reflection.)"),
    ("code", "# notes:\n"),
]
build_notebook(first_calls, os.path.join(CODE, "02_first_ai_calls.ipynb"))

print("wrote Week 1 notebooks to", CODE)
