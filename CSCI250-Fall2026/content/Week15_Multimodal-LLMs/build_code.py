"""Build Week 15 sample-code notebooks. Run: python build_code.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# ---------------------------------------------------------------- notebook 1
multimodal_basics = [
    ("md", "## ▶ What you'll see when you run this\n"
           "- A generated 'PALOMAR CAFE' sign image, then **Claude and Gemini** reading it "
           "back as **alt-text** and exact **OCR** lines (`Open 7am - 3pm`, ...).\n\n"
           "**Time:** ~10 min · **Cost:** free (cheapest model: Gemini Flash / Claude Haiku) "
           "· **Keys:** none to build/preview the image — add `ANTHROPIC_API_KEY` and/or "
           "`GEMINI_API_KEY` for the vision calls (each is skipped gracefully if missing)."),

    ("md", "# Week 15 · Notebook 1 — Multimodal Basics (Describe & OCR)\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Send the **same image + prompt** to **Claude** and **Gemini** vision models "
           "and compare. We make a self-contained sample image with Matplotlib so the "
           "notebook runs even before you add an image of your own.\n\n"
           "> **Keys:** In Colab use the 🔑 *Secrets* panel and `userdata.get('NAME')`. "
           "Locally use environment variables. **Never commit keys.** If a key is missing, "
           "each cell prints a clear message instead of crashing."),

    ("md", "## 0. Install SDKs"),
    ("code", "!pip -q install anthropic google-generativeai pillow matplotlib"),

    ("md", "## 1. Load API keys safely (optional — cells degrade gracefully)"),
    ("code", "import os\n"
             "try:\n"
             "    from google.colab import userdata  # Colab\n"
             "    for k in ('ANTHROPIC_API_KEY', 'GEMINI_API_KEY'):\n"
             "        try:\n"
             "            os.environ[k] = userdata.get(k)\n"
             "        except Exception:\n"
             "            pass\n"
             "except Exception:\n"
             "    pass  # locally, set these in your shell environment\n"
             "HAVE_CLAUDE = bool(os.environ.get('ANTHROPIC_API_KEY'))\n"
             "HAVE_GEMINI = bool(os.environ.get('GEMINI_API_KEY'))\n"
             "print('Claude key set:', HAVE_CLAUDE)\n"
             "print('Gemini key set:', HAVE_GEMINI)"),

    ("md", "## 2. Make a self-contained sample image\n"
           "We draw a simple 'storefront sign' with text so we can test both "
           "**description** and **OCR** without downloading anything."),
    ("code", "import matplotlib\n"
             "matplotlib.use('Agg')\n"
             "import matplotlib.pyplot as plt\n\n"
             "fig, ax = plt.subplots(figsize=(6, 4))\n"
             "ax.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9,\n"
             "             facecolor='#0B1F3A', edgecolor='#128C8C', linewidth=4))\n"
             "ax.text(0.5, 0.62, 'PALOMAR CAFE', ha='center', va='center',\n"
             "        color='white', fontsize=26, fontweight='bold')\n"
             "ax.text(0.5, 0.42, 'Open 7am - 3pm', ha='center', va='center',\n"
             "        color='#CFE3E3', fontsize=16)\n"
             "ax.text(0.5, 0.28, 'Coffee  *  Bagels  *  Wifi', ha='center', va='center',\n"
             "        color='#CFE3E3', fontsize=14)\n"
             "ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')\n"
             "fig.savefig('sign.png', dpi=100, bbox_inches='tight')\n"
             "plt.close(fig)\n"
             "print('wrote sign.png')"),
    ("code", "from PIL import Image\n"
             "Image.open('sign.png')   # preview the image inline"),

    ("md", "## 3. Helpers: send an image to Claude and to Gemini\n"
           "Both helpers return a string and never crash if a key is missing."),
    ("code", "import base64, os\n\n"
             "def media_type_for(path):\n"
             "    \"\"\"Map a file extension to the Claude media_type (students may upload JPG).\"\"\"\n"
             "    ext = os.path.splitext(path)[1].lower()\n"
             "    return {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',\n"
             "            '.png': 'image/png', '.gif': 'image/gif',\n"
             "            '.webp': 'image/webp'}.get(ext, 'image/png')\n\n"
             "def ask_claude(image_path, prompt, model='claude-sonnet-4-6'):\n"
             "    if not HAVE_CLAUDE:\n"
             "        return '[Claude skipped — no ANTHROPIC_API_KEY set]'\n"
             "    import anthropic\n"
             "    client = anthropic.Anthropic()\n"
             "    b64 = base64.standard_b64encode(open(image_path, 'rb').read()).decode()\n"
             "    msg = client.messages.create(\n"
             "        model=model, max_tokens=500,\n"
             "        messages=[{'role': 'user', 'content': [\n"
             "            {'type': 'image', 'source': {'type': 'base64',\n"
             "                'media_type': media_type_for(image_path), 'data': b64}},\n"
             "            {'type': 'text', 'text': prompt}]}])\n"
             "    return msg.content[0].text"),
    ("code", "def ask_gemini(image_path, prompt, model='gemini-2.5-flash'):\n"
             "    if not HAVE_GEMINI:\n"
             "        return '[Gemini skipped — no GEMINI_API_KEY set]'\n"
             "    import google.generativeai as genai\n"
             "    from PIL import Image\n"
             "    genai.configure(api_key=os.environ['GEMINI_API_KEY'])\n"
             "    m = genai.GenerativeModel(model)\n"
             "    resp = m.generate_content([prompt, Image.open(image_path)])\n"
             "    return resp.text"),

    ("md", "## 4. Task A — describe the image"),
    ("code", "PROMPT_DESC = 'In two sentences, describe this image as screen-reader alt-text.'\n"
             "print('CLAUDE:\\n', ask_claude('sign.png', PROMPT_DESC))\n"
             "print('\\nGEMINI:\\n', ask_gemini('sign.png', PROMPT_DESC))"),

    ("md", "## 5. Task B — OCR (read the text exactly)"),
    ("code", "PROMPT_OCR = ('Extract every piece of text in this image, exactly as written, '\n"
             "              'one line per text element. Do not add commentary.')\n"
             "print('CLAUDE:\\n', ask_claude('sign.png', PROMPT_OCR))\n"
             "print('\\nGEMINI:\\n', ask_gemini('sign.png', PROMPT_OCR))"),

    ("md", "## 6. Compare\n"
           "Write ~150 words: did Claude and Gemini read the sign the same way? Which "
           "description was more useful as alt-text? Where did either add details that "
           "were not in the image (hallucination)? **Try your own photo:** upload an image, "
           "set `image_path`, and re-run. (This feeds your Final Project progress update.)"),
    ("code", "# notes:\n"),
]
build_notebook(multimodal_basics, os.path.join(CODE, "01_multimodal_basics.ipynb"))

# ---------------------------------------------------------------- notebook 2
charts_and_extraction = [
    ("md", "## ▶ What you'll see when you run this\n"
           "- A bar chart with **known** values, read back by Claude/Gemini as JSON, then "
           "scored against ground truth — e.g. `Claude MAE : 2.0`.\n\n"
           "**Time:** ~10 min · **Cost:** free (cheapest model: Gemini Flash / Claude Haiku) "
           "· **Keys:** none to build the chart — add `ANTHROPIC_API_KEY` and/or "
           "`GEMINI_API_KEY` for the vision read-back (each skipped gracefully if missing)."),

    ("md", "# Week 15 · Notebook 2 — Reading Charts & Structured Extraction\n"
           "**CSCI 250 · Fall 2026**\n\n"
           "Generate a **bar chart with known values**, ask a vision model to read it back "
           "as **JSON**, then **check its accuracy against the ground truth**. This is the "
           "core skill behind the Final Project 'chart reader' / 'receipt reader' (the "
           "Multimodal track).\n\n"
           "> Cells degrade gracefully if no API key is set."),

    ("md", "## 0. Install + keys"),
    ("code", "!pip -q install anthropic google-generativeai pillow matplotlib"),
    ("code", "import os\n"
             "try:\n"
             "    from google.colab import userdata\n"
             "    for k in ('ANTHROPIC_API_KEY', 'GEMINI_API_KEY'):\n"
             "        try:\n"
             "            os.environ[k] = userdata.get(k)\n"
             "        except Exception:\n"
             "            pass\n"
             "except Exception:\n"
             "    pass\n"
             "HAVE_CLAUDE = bool(os.environ.get('ANTHROPIC_API_KEY'))\n"
             "HAVE_GEMINI = bool(os.environ.get('GEMINI_API_KEY'))\n"
             "print('Claude:', HAVE_CLAUDE, '| Gemini:', HAVE_GEMINI)"),

    ("md", "## 1. Build a chart with KNOWN values (ground truth)"),
    ("code", "import matplotlib\n"
             "matplotlib.use('Agg')\n"
             "import matplotlib.pyplot as plt\n\n"
             "TRUTH = {'North': 42, 'South': 27, 'East': 58, 'West': 19}\n"
             "fig, ax = plt.subplots(figsize=(6, 4))\n"
             "ax.bar(list(TRUTH.keys()), list(TRUTH.values()), color='#128C8C')\n"
             "ax.set_title('Sales by Region (units)')\n"
             "ax.set_ylabel('Units sold')\n"
             "fig.savefig('chart.png', dpi=110, bbox_inches='tight')\n"
             "plt.close(fig)\n"
             "print('ground truth:', TRUTH)"),
    ("code", "from PIL import Image\n"
             "Image.open('chart.png')   # preview"),

    ("md", "## 2. Vision helpers (return raw text)"),
    ("code", "import base64\n\n"
             "def ask_claude(image_path, prompt, model='claude-sonnet-4-6'):\n"
             "    if not HAVE_CLAUDE:\n"
             "        return '[Claude skipped — no key]'\n"
             "    import anthropic\n"
             "    client = anthropic.Anthropic()\n"
             "    b64 = base64.standard_b64encode(open(image_path, 'rb').read()).decode()\n"
             "    msg = client.messages.create(\n"
             "        model=model, max_tokens=500,\n"
             "        messages=[{'role': 'user', 'content': [\n"
             "            {'type': 'image', 'source': {'type': 'base64',\n"
             "                'media_type': 'image/png', 'data': b64}},\n"
             "            {'type': 'text', 'text': prompt}]}])\n"
             "    return msg.content[0].text\n\n"
             "def ask_gemini(image_path, prompt, model='gemini-2.5-flash'):\n"
             "    if not HAVE_GEMINI:\n"
             "        return '[Gemini skipped — no key]'\n"
             "    import google.generativeai as genai\n"
             "    from PIL import Image\n"
             "    genai.configure(api_key=os.environ['GEMINI_API_KEY'])\n"
             "    m = genai.GenerativeModel(model)\n"
             "    return m.generate_content([prompt, Image.open(image_path)]).text"),

    ("md", "## 3. Ask for the chart as JSON"),
    ("code", "CHART_PROMPT = (\n"
             "    'This is a bar chart. Return ONLY a JSON object mapping each bar label '\n"
             "    'to its approximate numeric value, e.g. {\"North\": 40}. No prose, no '\n"
             "    'code fences.')\n"
             "claude_raw = ask_claude('chart.png', CHART_PROMPT)\n"
             "gemini_raw = ask_gemini('chart.png', CHART_PROMPT)\n"
             "print('CLAUDE raw:', claude_raw)\n"
             "print('GEMINI raw:', gemini_raw)"),

    ("md", "## 4. Parse JSON robustly\n"
           "Models sometimes wrap JSON in ```code fences``` or add a sentence. This helper "
           "pulls out the first `{...}` block and parses it."),
    ("code", "import json, re\n\n"
             "def parse_json(text):\n"
             "    if not text or text.startswith('['):\n"
             "        return None\n"
             "    m = re.search(r'\\{.*\\}', text, re.DOTALL)\n"
             "    if not m:\n"
             "        return None\n"
             "    try:\n"
             "        return json.loads(m.group(0))\n"
             "    except Exception:\n"
             "        return None\n\n"
             "claude_json = parse_json(claude_raw)\n"
             "gemini_json = parse_json(gemini_raw)\n"
             "print('Claude parsed:', claude_json)\n"
             "print('Gemini parsed:', gemini_json)"),

    ("md", "## 5. Score against ground truth\n"
           "Mean absolute error (MAE) between the model's read and the true values."),
    ("code", "def score(pred, truth):\n"
             "    if not pred:\n"
             "        return None\n"
             "    errs = []\n"
             "    for label, true_val in truth.items():\n"
             "        if label in pred:\n"
             "            try:\n"
             "                errs.append(abs(float(pred[label]) - true_val))\n"
             "            except (TypeError, ValueError):\n"
             "                pass\n"
             "    return round(sum(errs) / len(errs), 2) if errs else None\n\n"
             "print('TRUTH      :', TRUTH)\n"
             "print('Claude MAE :', score(claude_json, TRUTH))\n"
             "print('Gemini MAE :', score(gemini_json, TRUTH))"),

    ("md", "## 6. Reflect\n"
           "- How close were the read-off values? Which model was more accurate?\n"
           "- VLMs estimate values **from pixels** — good for 'which bar is biggest', "
           "risky for exact figures. When would that error matter in your project?\n"
           "- **Extend it:** swap in a receipt photo and a JSON schema "
           "(`vendor, date, items[], total`) to prototype the Track D 'Receipt Reader'."),
    ("code", "# notes / your extension here:\n"),
]
build_notebook(charts_and_extraction, os.path.join(CODE, "02_charts_and_extraction.ipynb"))

print("wrote Week 15 notebooks to", CODE)
