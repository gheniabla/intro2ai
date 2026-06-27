"""Build Week 8 sample-code notebooks. Run: python build_code.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# ---------------------------------------------------------------- notebook 1
llm_concepts = [
    ("md", "## ▶ What you'll see when you run this\n"
           "- A table of short strings with their **token counts** printed instantly — "
           "no API key needed for the first result.\n\n"
           "**Time:** ~10 min · **Cost:** free (defaults to cheapest model: Gemini Flash / "
           "Claude Haiku / local Ollama) · **Keys:** none for the first cell; "
           "**ANTHROPIC_API_KEY** for the live-model cells"),

    ("md", "# Week 8 · Notebook 1 — How LLMs Work\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Hands-on tour of the core ideas: **tokens**, the **context window**, "
           "**sampling / temperature**, **in-context learning**, and **hallucination**.\n\n"
           "> Some cells call the **Claude** API. In Colab use the 🔑 *Secrets* panel and "
           "`userdata.get('ANTHROPIC_API_KEY')`; locally use an environment variable. **Never commit keys.**"),

    ("md", "## 0. Wow in 5 seconds — count tokens with no API key\n"
           "Pure Python, runs immediately. Each emoji and rare word costs **more than one token**."),
    ("code", "# A crude byte-based token estimate so this cell ALWAYS runs (no install, no key).\n"
             "def rough_tokens(text):\n"
             "    # ~4 bytes per token is the classic rule of thumb for English.\n"
             "    return max(1, round(len(text.encode('utf-8')) / 4))\n\n"
             "for s in ['AI', 'Artificial intelligence', 'strawberry', '🍓🍓🍓']:\n"
             "    print(f'{rough_tokens(s):2d} est. tokens | {s!r}')"),

    ("md", "## 0b. Install (for the exact, model-grade tokenizer + live calls)"),
    ("code", "!pip -q install anthropic transformers"),

    ("md", "## 1. Tokens & tokenization\n"
           "Models see **tokens** (sub-word IDs), not characters. We use a public BPE tokenizer "
           "to *illustrate* the idea; exact counts differ per model."),
    ("code", "from transformers import AutoTokenizer\n"
             "tok = AutoTokenizer.from_pretrained('gpt2')\n\n"
             "samples = [\n"
             "    'AI',\n"
             "    'Artificial intelligence is reshaping software.',\n"
             "    'antidisestablishmentarianism',\n"
             "]\n"
             "for s in samples:\n"
             "    ids = tok.encode(s)\n"
             "    pieces = [tok.decode([i]) for i in ids]\n"
             "    print(f'{len(ids):2d} tokens | {s!r}')\n"
             "    print('     pieces:', pieces)\n"),
    ("md", "**Rule of thumb:** 1 token ≈ 4 characters ≈ 0.75 words. Notice the rare word "
           "splits into several tokens.\n\n"
           "**Task (A7):** add three strings of your own above and predict the token count "
           "before you run it."),

    ("md", "## 2. Exact token counting with Claude\n"
           "Anthropic exposes an exact token counter so you can budget prompts."),
    ("code", "import os\n"
             "try:\n"
             "    from google.colab import userdata\n"
             "    os.environ['ANTHROPIC_API_KEY'] = userdata.get('ANTHROPIC_API_KEY')\n"
             "except Exception:\n"
             "    pass\n\n"
             "import anthropic\n"
             "client = anthropic.Anthropic()\n"
             "try:\n"
             "    ct = client.messages.count_tokens(\n"
             "        model='claude-sonnet-4-6',\n"
             "        messages=[{'role': 'user', 'content': 'Explain tokens in one sentence.'}],\n"
             "    )\n"
             "    print('Claude input tokens:', ct.input_tokens)\n"
             "except Exception as e:\n"
             "    print('Set ANTHROPIC_API_KEY to run this cell:', e)"),

    ("md", "## 3. The context window\n"
           "Prompt **plus** reply must fit the model's context window. There is **no memory** "
           "between calls — a chat app works by *replaying* the whole conversation each turn."),
    ("code", "# A 'conversation' is just a growing list of messages you resend every turn.\n"
             "conversation = [\n"
             "    {'role': 'user', 'content': 'My favorite number is 7.'},\n"
             "    {'role': 'assistant', 'content': 'Got it — your favorite number is 7.'},\n"
             "    {'role': 'user', 'content': 'What is my favorite number?'},\n"
             "]\n"
             "try:\n"
             "    msg = client.messages.create(model='claude-sonnet-4-6', max_tokens=50,\n"
             "                                 messages=conversation)\n"
             "    print(msg.content[0].text)\n"
             "    print('--- if we DROP the history, the model can no longer know: ---')\n"
             "    msg2 = client.messages.create(model='claude-sonnet-4-6', max_tokens=50,\n"
             "        messages=[{'role':'user','content':'What is my favorite number?'}])\n"
             "    print(msg2.content[0].text)\n"
             "except Exception as e:\n"
             "    print('Set ANTHROPIC_API_KEY to run this cell:', e)"),

    ("md", "## 4. Sampling & temperature\n"
           "Run the **same prompt** at `temperature=0.0` (focused) and `temperature=1.0` "
           "(diverse) a few times and compare."),
    ("code", "def ask(prompt, temperature, n=3):\n"
             "    outs = []\n"
             "    for _ in range(n):\n"
             "        m = client.messages.create(model='claude-sonnet-4-6', max_tokens=40,\n"
             "                                   temperature=temperature,\n"
             "                                   messages=[{'role':'user','content':prompt}])\n"
             "        outs.append(m.content[0].text.strip().replace('\\n',' '))\n"
             "    return outs\n\n"
             "P = 'Give a one-line tagline for a coffee shop run by robots.'\n"
             "try:\n"
             "    print('TEMP 0.0 (deterministic):')\n"
             "    for o in ask(P, 0.0): print('  -', o)\n"
             "    print('TEMP 1.0 (creative):')\n"
             "    for o in ask(P, 1.0): print('  -', o)\n"
             "except Exception as e:\n"
             "    print('Set ANTHROPIC_API_KEY to run this cell:', e)"),
    ("md", "**Task (A7):** describe in 2–3 sentences how the temp-0 and temp-1 outputs "
           "differed. When would you want each?"),

    ("md", "## 5. In-context learning (zero-shot vs few-shot)\n"
           "Few-shot examples teach the task **and** lock the output format — no retraining."),
    ("code", "few_shot = (\n"
             "    'Classify the review sentiment as positive or negative.\\n'\n"
             "    'Review: \"Loved every minute.\" -> positive\\n'\n"
             "    'Review: \"A complete waste of time.\" -> negative\\n'\n"
             "    'Review: \"The acting saved an otherwise dull script.\" ->'\n"
             ")\n"
             "try:\n"
             "    m = client.messages.create(model='claude-sonnet-4-6', max_tokens=10,\n"
             "        temperature=0, messages=[{'role':'user','content':few_shot}])\n"
             "    print('Few-shot answer:', m.content[0].text.strip())\n"
             "except Exception as e:\n"
             "    print('Set ANTHROPIC_API_KEY to run this cell:', e)"),

    ("md", "## 6. Hallucination\n"
           "LLMs generate *plausible* text, not verified fact. Ask about something that "
           "does not exist and watch a confident, wrong answer appear."),
    ("code", "trap = ('Summarize the famous 2019 paper \"Quantum Transformers for '\n"
             "        'Underwater Basket Weaving\" by Dr. Eleanor Fakename.')\n"
             "try:\n"
             "    m = client.messages.create(model='claude-sonnet-4-6', max_tokens=150,\n"
             "        temperature=0, messages=[{'role':'user','content':trap}])\n"
             "    print(m.content[0].text)\n"
             "except Exception as e:\n"
             "    print('Set ANTHROPIC_API_KEY to run this cell:', e)"),
    ("md", "**Task (A7):** craft your **own** trap prompt that yields a confident but false "
           "answer. Paste the output and write 2–3 sentences on *why* it happened and how "
           "you would mitigate it (temperature=0, ask for sources, RAG, tools, verify)."),

    ("md", "---\n### Recap\n"
           "Tokens → context window → sampling → in-context learning → hallucination. "
           "Next notebook: call **Claude**, **Gemini**, and a **local** model and compare them."),

    ("md", "### 🎯 Start My Assistant — *just pick* (2 minutes)\n"
           "Your **final project** begins this week, but the only thing to do now is **pick "
           "your idea and track** — RAG / Tool-Using Agent / Multimodal / Fine-Tuned "
           "(see `Final-Project-Capstone.md`). **Don't build the app this week.** The graded "
           "proposal + a 'wow in 5 min' prototype is **Milestone M1, due Week 9** "
           "(`capstone/M1.md`). Jot one line below — that's the whole task."),
    ("code", "my_assistant_idea  = ''   # <- one line: what should your assistant help with?\n"
             "my_assistant_track = ''   # <- one of: RAG | Agent | Multimodal | Fine-Tuned\n"
             "print('Idea :', my_assistant_idea or '(fill me in — building comes in Week 9)')\n"
             "print('Track:', my_assistant_track or '(pick one)')"),
]
build_notebook(llm_concepts, os.path.join(CODE, "01_llm_concepts.ipynb"))

# ---------------------------------------------------------------- notebook 2
compare = [
    ("md", "## ▶ What you'll see when you run this\n"
           "- The **same prompt** answered side by side by Claude, Gemini, and a local "
           "model, each with its **response time** printed.\n\n"
           "**Time:** ~15 min · **Cost:** free (defaults to cheapest model: Gemini Flash / "
           "Claude Haiku / local Ollama) · **Keys:** **ANTHROPIC_API_KEY** and/or "
           "**GEMINI_API_KEY** (local Ollama needs none)"),

    ("md", "# Week 8 · Notebook 2 — Claude vs Gemini vs Local\n"
           "**CSCI 250 · Fall 2026**\n\n"
           "Send the **same prompt** to three model sources and compare length, tone, "
           "correctness, and speed:\n"
           "- **Anthropic Claude** (cloud)\n- **Google Gemini** (cloud)\n- **Ollama** (local, no key)\n\n"
           "> **Keys:** Colab 🔑 *Secrets* + `userdata.get('NAME')`; locally use env vars. **Never commit keys.**"),

    ("md", "## 0. A no-key warm-up (runs instantly)\n"
           "Before any API calls, confirm the notebook is alive."),
    ("code", "print('Notebook ready. We will send ONE shared prompt to 3 models below.')\n"
             "print('Cheapest defaults: Gemini Flash / Claude Haiku / local Ollama.')"),

    ("md", "## 0b. Install SDKs"),
    ("code", "!pip -q install anthropic google-generativeai ollama"),

    ("md", "## 1. Load API keys safely"),
    ("code", "import os\n"
             "try:\n"
             "    from google.colab import userdata\n"
             "    os.environ['ANTHROPIC_API_KEY'] = userdata.get('ANTHROPIC_API_KEY')\n"
             "    os.environ['GEMINI_API_KEY'] = userdata.get('GEMINI_API_KEY')\n"
             "except Exception:\n"
             "    pass  # locally, set these in your shell environment\n"
             "print('Anthropic key set:', bool(os.environ.get('ANTHROPIC_API_KEY')))\n"
             "print('Gemini key set:', bool(os.environ.get('GEMINI_API_KEY')))"),

    ("md", "## 2. The shared prompt + a timing helper"),
    ("code", "import time\n"
             "PROMPT = ('In exactly 3 bullet points, explain what a context window is to a '\n"
             "          'new CS student.')\n\n"
             "def timed(fn):\n"
             "    t0 = time.time()\n"
             "    out = fn()\n"
             "    return out, round(time.time() - t0, 2)"),

    ("md", "## 3. Anthropic Claude"),
    ("code", "import anthropic\n"
             "client = anthropic.Anthropic()\n\n"
             "def call_claude():\n"
             "    m = client.messages.create(model='claude-sonnet-4-6', max_tokens=200,\n"
             "        temperature=0.3, messages=[{'role':'user','content':PROMPT}])\n"
             "    return m.content[0].text\n\n"
             "try:\n"
             "    out, secs = timed(call_claude)\n"
             "    print(f'CLAUDE ({secs}s):\\n{out}')\n"
             "except Exception as e:\n"
             "    print('Claude error:', e)"),

    ("md", "## 4. Google Gemini"),
    ("code", "import google.generativeai as genai\n"
             "genai.configure(api_key=os.environ.get('GEMINI_API_KEY', ''))\n"
             "gem = genai.GenerativeModel('gemini-2.5-flash')\n\n"
             "def call_gemini():\n"
             "    r = gem.generate_content(\n"
             "        PROMPT,\n"
             "        generation_config={'temperature': 0.3, 'max_output_tokens': 200})\n"
             "    return r.text\n\n"
             "try:\n"
             "    out, secs = timed(call_gemini)\n"
             "    print(f'GEMINI ({secs}s):\\n{out}')\n"
             "except Exception as e:\n"
             "    print('Gemini error:', e)"),

    ("md", "## 5. Local model with Ollama\n"
           "Install Ollama from **ollama.com**, then in a terminal: `ollama pull llama3.2`.\n"
           "In Colab you can instead run:\n"
           "```\n!curl -fsSL https://ollama.com/install.sh | sh\n"
           "!nohup ollama serve >/tmp/ollama.log 2>&1 &\n!ollama pull llama3.2\n```"),
    ("code", "import ollama\n\n"
             "def call_ollama():\n"
             "    r = ollama.chat(model='llama3.2',\n"
             "                    messages=[{'role':'user','content':PROMPT}])\n"
             "    return r['message']['content']\n\n"
             "try:\n"
             "    out, secs = timed(call_ollama)\n"
             "    print(f'OLLAMA llama3.2 ({secs}s):\\n{out}')\n"
             "except Exception as e:\n"
             "    print('Ollama not running yet:', e)"),

    ("md", "## 6. Compare (fill this in for A7)\n"
           "| Model | Length | Tone | Correct? | Speed (s) |\n"
           "|---|---|---|---|---|\n"
           "| Claude (claude-sonnet-4-6) |  |  |  |  |\n"
           "| Gemini (gemini-2.5-flash) |  |  |  |  |\n"
           "| Local (llama3.2 via Ollama) |  |  |  |  |\n\n"
           "Then write ~150 words: which model would you pick for a **privacy-sensitive** task, "
           "for a **quick free** task, and for the **highest-quality** answer — and why?"),
    ("code", "# notes:\n"),
]
build_notebook(compare, os.path.join(CODE, "02_claude_gemini_local.ipynb"))

# ---------------------------------------------------------------- notebook 3
bpe = [
    ("md", "## ▶ What you'll see when you run this\n"
           "- Your own text getting **merged into BPE tokens step by step**, then a "
           "perfect **encode → decode round-trip** confirmed by `assert`.\n\n"
           "**Time:** ~20 min · **Cost:** free (pure Python/NumPy, no model calls) · "
           "**Keys:** none"),

    ("md", "# Week 8 · Notebook 3 — Build a BPE Tokenizer **From Scratch**\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Every LLM starts by chopping text into **tokens**. Here we build the real "
           "algorithm models use — **Byte-Pair Encoding (BPE)** — in plain Python "
           "(Karpathy *minbpe* / Stanford CS336 style, simplified).\n\n"
           "The plan: start from raw **bytes**, repeatedly **count adjacent pairs** and "
           "**merge the most frequent** one into a new token, until we hit a target "
           "vocab size. Then we **encode** new text and **decode** it back.\n\n"
           "> No API keys, no installs, no GPU. Just the idea behind every tokenizer."),

    ("md", "## 0. Wow in 5 seconds — bytes are the starting vocab\n"
           "Before any merging, a tokenizer sees text as a list of **byte values "
           "(0–255)**. That is the base vocabulary every BPE model grows from."),
    ("code", "text = 'the cat sat on the mat. the cat sat.'\n"
             "tokens = list(text.encode('utf-8'))   # each char -> its byte value\n"
             "print('characters:', len(text))\n"
             "print('byte tokens:', tokens[:20], '...')\n"
             "print('starting vocab size:', 256, '(one entry per possible byte)')"),

    ("md", "## 1. Count adjacent pairs\n"
           "BPE looks at every **neighbouring pair** of tokens and counts how often "
           "each pair occurs. The most common pair is the best candidate to merge."),
    ("code", "from collections import Counter\n\n"
             "def get_pair_counts(ids):\n"
             "    counts = Counter()\n"
             "    for a, b in zip(ids, ids[1:]):   # walk neighbouring pairs\n"
             "        counts[(a, b)] += 1\n"
             "    return counts\n\n"
             "counts = get_pair_counts(tokens)\n"
             "top = counts.most_common(3)\n"
             "print('most common adjacent pairs:', top)\n"
             "# self-check: the most common pair really is the max\n"
             "assert top[0][1] == max(counts.values())\n"
             "print('assert passed: top pair is the most frequent ✔')"),

    ("md", "## 2. Fill-in #1 — merge one pair\n"
           "**Your turn.** Complete `merge()` so that every occurrence of the pair "
           "`(a, b)` in `ids` is replaced by the single new token id `new_id`."),
    ("code", "def merge(ids, pair, new_id):\n"
             "    a, b = pair\n"
             "    out = []\n"
             "    i = 0\n"
             "    while i < len(ids):\n"
             "        # TODO: if ids[i], ids[i+1] == a, b -> append new_id and skip 2;\n"
             "        #       otherwise append ids[i] and skip 1.\n"
             "        if i < len(ids) - 1 and ids[i] == a and ids[i + 1] == b:\n"
             "            out.append(new_id)\n"
             "            i += 2\n"
             "        else:\n"
             "            out.append(ids[i])\n"
             "            i += 1\n"
             "    return out\n\n"
             "# self-check: merge the pair (6, 7) -> 99\n"
             "assert merge([5, 6, 7, 6, 7, 8], (6, 7), 99) == [5, 99, 99, 8]\n"
             "print('assert passed: merge() works ✔')"),

    ("md", "## 3. Train the tokenizer (repeat: count → merge)\n"
           "We loop: find the most frequent pair, mint a brand-new token id for it, "
           "merge, and remember the rule. Each new token grows the vocabulary by one."),
    ("code", "def train_bpe(text, vocab_size):\n"
             "    assert vocab_size >= 256\n"
             "    ids = list(text.encode('utf-8'))\n"
             "    merges = {}                       # (a, b) -> new_id\n"
             "    num_merges = vocab_size - 256\n"
             "    for k in range(num_merges):\n"
             "        counts = get_pair_counts(ids)\n"
             "        if not counts:\n"
             "            break\n"
             "        pair = max(counts, key=counts.get)   # most frequent pair\n"
             "        new_id = 256 + k\n"
             "        ids = merge(ids, pair, new_id)\n"
             "        merges[pair] = new_id\n"
             "    return merges, ids\n\n"
             "corpus = ('the cat sat on the mat. the cat sat on the hat. '\n"
             "          'a cat and a hat and a mat. ') * 8\n"
             "merges, trained_ids = train_bpe(corpus, vocab_size=276)  # 20 merges\n"
             "print('learned', len(merges), 'merge rules')\n"
             "print('tokens before:', len(corpus.encode('utf-8')))\n"
             "print('tokens after :', len(trained_ids))\n"
             "ratio = len(corpus.encode('utf-8')) / len(trained_ids)\n"
             "print(f'compression: {ratio:.2f}x fewer tokens')\n"
             "assert len(trained_ids) < len(corpus.encode('utf-8'))\n"
             "print('assert passed: BPE shortened the sequence ✔')"),

    ("md", "## 4. Fill-in #2 — encode new text with the learned merges\n"
           "**Your turn.** To encode, apply the learned merges **in the order they "
           "were learned** (lower new_id first). Complete the loop.\n\n"
           "> **Scope cap:** we apply each merge once, in order — enough to see the idea. "
           "**Production BPE re-scans the sequence and keeps applying the highest-priority "
           "merge until no merge rule applies anymore.** Same algorithm, run to completion."),
    ("code", "def encode(text, merges):\n"
             "    ids = list(text.encode('utf-8'))\n"
             "    # apply merges in learned order (new_id ascending)\n"
             "    for pair, new_id in sorted(merges.items(), key=lambda kv: kv[1]):\n"
             "        # TODO: replace the pair with new_id using merge()\n"
             "        ids = merge(ids, pair, new_id)\n"
             "    return ids\n\n"
             "enc = encode('the cat sat on the mat.', merges)\n"
             "print('encoded:', enc)\n"
             "# a word the tokenizer saw a lot should be shorter than its raw bytes\n"
             "assert len(enc) < len('the cat sat on the mat.'.encode('utf-8'))\n"
             "print('assert passed: encoding compresses familiar text ✔')"),

    ("md", "## 5. Fill-in #3 — decode back to text (round-trip)\n"
           "**Your turn.** Build a `vocab` mapping each id to its **bytes**, then "
           "decoding is just concatenating those byte-strings. This must round-trip "
           "**exactly**."),
    ("code", "def build_vocab(merges):\n"
             "    vocab = {i: bytes([i]) for i in range(256)}      # base bytes\n"
             "    for (a, b), new_id in sorted(merges.items(), key=lambda kv: kv[1]):\n"
             "        vocab[new_id] = vocab[a] + vocab[b]           # a token IS its bytes\n"
             "    return vocab\n\n"
             "def decode(ids, vocab):\n"
             "    # TODO: join the bytes for each id, then utf-8 decode\n"
             "    data = b''.join(vocab[i] for i in ids)\n"
             "    return data.decode('utf-8', errors='replace')\n\n"
             "vocab = build_vocab(merges)\n"
             "sample = 'the cat sat on the mat.'\n"
             "roundtrip = decode(encode(sample, merges), vocab)\n"
             "print('original :', sample)\n"
             "print('roundtrip:', roundtrip)\n"
             "assert roundtrip == sample, 'round-trip must be exact!'\n"
             "print('assert passed: encode -> decode is lossless ✔')"),

    ("md", "## 6. Try it on YOUR text (S-exercise)\n"
           "Replace the string below with **your own sentence**, then watch it encode "
           "and decode. Words your corpus never saw will fall back to raw bytes — that "
           "is fine and still round-trips."),
    ("code", "my_text = 'the cat wore a fancy hat'   # <- change me\n"
             "ids = encode(my_text, merges)\n"
             "print('your text     :', my_text)\n"
             "print('your tokens   :', ids)\n"
             "print('# tokens      :', len(ids), 'vs', len(my_text), 'characters')\n"
             "assert decode(ids, vocab) == my_text\n"
             "print('round-trip on YOUR text ✔')"),

    ("md", "## 7. Vocab size vs sequence length — the core tradeoff\n"
           "More merges = a **bigger vocabulary** but **shorter sequences** (fewer "
           "tokens to process). This is the dial every model maker tunes."),
    ("code", "import numpy as np\n\n"
             "sizes = [256, 266, 276, 296, 336]\n"
             "lengths = []\n"
             "for v in sizes:\n"
             "    m, ids = train_bpe(corpus, vocab_size=v)\n"
             "    lengths.append(len(ids))\n"
             "for v, L in zip(sizes, lengths):\n"
             "    print(f'vocab {v:4d} -> {L:4d} tokens')\n"
             "# bigger vocab never makes the sequence longer\n"
             "assert all(lengths[i] >= lengths[i + 1] for i in range(len(lengths) - 1))\n"
             "print('assert passed: bigger vocab -> same-or-shorter sequences ✔')"),

    ("md", "## 8. Why models can't easily count letters in *strawberry*\n"
           "A tokenizer often turns a whole word into **one token** — the model "
           "literally never sees the individual letters, so 'how many r's in "
           "strawberry?' is genuinely hard for it. Tokens also = **API cost**: you "
           "pay per token, not per character."),
    ("code", "word = 'strawberry'\n"
             "# pretend a big-vocab tokenizer mapped this whole word to ONE token:\n"
             "as_one_token = ['strawberry']\n"
             "print('the model may see:', as_one_token, '-> 1 opaque token')\n"
             "print('it does NOT see  :', list(word), '-> the letters are hidden')\n"
             "print('that is WHY counting letters is unreliable for an LLM.')\n"
             "# cost intuition: ~4 chars per token, billed per token\n"
             "prompt = 'Summarize this report in three bullet points. ' * 50\n"
             "est_tokens = round(len(prompt) / 4)\n"
             "print(f'\\na {len(prompt)}-char prompt ~= {est_tokens} tokens of API cost')"),

    ("md", "## 9. Compare with a REAL tokenizer (Hugging Face)\n"
           "Production models use the same BPE idea, just trained on billions of words. "
           "The import is guarded so the notebook still runs if `transformers` is "
           "missing."),
    ("code", "try:\n"
             "    from transformers import AutoTokenizer\n"
             "    hf = AutoTokenizer.from_pretrained('gpt2')   # a real BPE tokenizer\n"
             "    for s in ['strawberry', 'tokenization', 'the cat sat on the mat']:\n"
             "        ids = hf.encode(s)\n"
             "        pieces = [hf.decode([i]) for i in ids]\n"
             "        print(f'{len(ids):2d} tokens | {s!r} -> {pieces}')\n"
             "    print('\\nSame algorithm you just built, trained at scale.')\n"
             "except Exception as e:\n"
             "    print('transformers not available, skipping HF compare:', e)\n"
             "    print('Your from-scratch BPE above is the real idea either way.')"),

    ("md", "---\n### Recap\n"
           "bytes → count pairs → merge most frequent → repeat. You built encode + "
           "decode that round-trips exactly, saw the **vocab-size vs sequence-length** "
           "tradeoff, and connected tokens to **API cost** and the *strawberry* problem. "
           "Next notebook: the **attention** math behind the Transformer."),
]
build_notebook(bpe, os.path.join(CODE, "03_build_bpe_tokenizer.ipynb"))

# ---------------------------------------------------------------- notebook 4
attention = [
    ("md", "## ▶ What you'll see when you run this\n"
           "- A **matplotlib heatmap** of an attention matrix showing which words each "
           "word 'looks at' — the engine inside every Transformer, made visible.\n\n"
           "**Time:** ~20 min · **Cost:** free (pure NumPy + matplotlib, no model calls) · "
           "**Keys:** none"),

    ("md", "# Week 8 · Notebook 4 — Attention **From Scratch** (NumPy)\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "The Transformer that powers every modern LLM is built on one operation: "
           "**scaled dot-product attention**. We compute it by hand in NumPy on a tiny "
           "toy sentence, then **visualize** which words attend to which.\n\n"
           "The recipe:\n"
           "1. Turn each word into **Q** (query), **K** (key), **V** (value) vectors.\n"
           "2. **scores = Q · Kᵀ / √d** — how well each query matches each key.\n"
           "3. **softmax** each row → attention weights that sum to 1.\n"
           "4. **weighted sum of V** → each word's new, context-aware vector.\n\n"
           "> Pure NumPy. No keys, no GPU, no full Transformer — just the core engine."),

    ("md", "## 0. Wow in 5 seconds — our toy sentence as numbers\n"
           "Each word gets a small random **embedding** (a row of numbers). Real models "
           "learn these; we just make them up so the math is visible."),
    ("code", "import numpy as np\n"
             "np.random.seed(0)\n\n"
             "words = ['the', 'cat', 'sat', 'on', 'mat']\n"
             "n = len(words)          # sequence length\n"
             "d = 4                   # embedding dimension (tiny on purpose)\n"
             "X = np.random.randn(n, d)\n"
             "print('sentence:', words)\n"
             "print('embeddings X shape:', X.shape, '(one row per word)')\n"
             "print(np.round(X, 2))"),

    ("md", "## 1. Build Q, K, V with small random weight matrices\n"
           "Attention first projects each embedding into a **query**, a **key**, and a "
           "**value** using learned weight matrices `Wq, Wk, Wv`. We use random ones."),
    ("code", "Wq = np.random.randn(d, d) * 0.5\n"
             "Wk = np.random.randn(d, d) * 0.5\n"
             "Wv = np.random.randn(d, d) * 0.5\n\n"
             "Q = X @ Wq    # queries\n"
             "K = X @ Wk    # keys\n"
             "V = X @ Wv    # values\n"
             "print('Q, K, V shapes:', Q.shape, K.shape, V.shape)\n"
             "assert Q.shape == (n, d) and K.shape == (n, d) and V.shape == (n, d)\n"
             "print('assert passed: Q/K/V are (n_words, d) ✔')"),

    ("md", "## 2. Fill-in #1 — scaled dot-product scores\n"
           "**Your turn.** Compute `scores = Q · Kᵀ / √d`. Dividing by **√d** keeps the "
           "numbers from blowing up as the dimension grows (the 'scaled' part)."),
    ("code", "def attention_scores(Q, K):\n"
             "    d = Q.shape[1]\n"
             "    # TODO: matrix-multiply Q by K transpose, then divide by sqrt(d)\n"
             "    return (Q @ K.T) / np.sqrt(d)\n\n"
             "scores = attention_scores(Q, K)\n"
             "print('scores shape:', scores.shape, '(word-by-word match strength)')\n"
             "assert scores.shape == (n, n)\n"
             "print('assert passed: scores is n x n ✔')"),

    ("md", "## 3. Fill-in #2 — softmax each row into weights\n"
           "**Your turn.** Softmax turns each row of scores into **probabilities that "
           "sum to 1** — the attention weights. We subtract the row max first for "
           "numerical stability."),
    ("code", "def softmax_rows(M):\n"
             "    M = M - M.max(axis=1, keepdims=True)   # stability\n"
             "    e = np.exp(M)\n"
             "    # TODO: divide each row by its sum so the row totals 1\n"
             "    return e / e.sum(axis=1, keepdims=True)\n\n"
             "weights = softmax_rows(scores)\n"
             "print('each row sums to 1?')\n"
             "print(np.round(weights.sum(axis=1), 6))\n"
             "assert np.allclose(weights.sum(axis=1), 1.0)\n"
             "assert (weights >= 0).all()\n"
             "print('assert passed: weights are a valid probability distribution ✔')"),

    ("md", "## 4. Fill-in #3 — weighted sum of V (the output)\n"
           "**Your turn.** Each word's new vector is the **attention-weighted average "
           "of all value vectors**: `output = weights · V`. This is where context "
           "actually flows between words."),
    ("code", "def attention(Q, K, V):\n"
             "    scores = attention_scores(Q, K)\n"
             "    weights = softmax_rows(scores)\n"
             "    # TODO: multiply the weights by V to mix the value vectors\n"
             "    out = weights @ V\n"
             "    return out, weights\n\n"
             "output, weights = attention(Q, K, V)\n"
             "print('output shape:', output.shape, '(one context-aware vector per word)')\n"
             "assert output.shape == (n, d)\n"
             "print('assert passed: attention output is (n_words, d) ✔')"),

    ("md", "## 5. Visualize the attention matrix as a heatmap\n"
           "Row *i* shows how much word *i* attends to every other word. Brighter = more "
           "attention. **This is the picture researchers stare at to interpret models.**\n\n"
           "> **Scope cap:** this is an **encoder-style** demo — every word attends to every "
           "other word. Real **decoder-only** LLMs add a **causal mask** so a token can only "
           "attend to tokens *before* it. We leave that out to keep the core idea clear."),
    ("code", "import matplotlib.pyplot as plt\n\n"
             "fig, ax = plt.subplots(figsize=(5, 4))\n"
             "im = ax.imshow(weights, cmap='viridis')\n"
             "ax.set_xticks(range(n)); ax.set_xticklabels(words)\n"
             "ax.set_yticks(range(n)); ax.set_yticklabels(words)\n"
             "ax.set_xlabel('attends to (key)')\n"
             "ax.set_ylabel('query word')\n"
             "ax.set_title('Scaled Dot-Product Attention')\n"
             "for i in range(n):\n"
             "    for j in range(n):\n"
             "        ax.text(j, i, f'{weights[i, j]:.2f}', ha='center', va='center',\n"
             "                color='white', fontsize=8)\n"
             "fig.colorbar(im, ax=ax, label='attention weight')\n"
             "plt.tight_layout()\n"
             "plt.show()\n"
             "print('Each ROW sums to 1 — a word distributes its attention across the sentence.')"),

    ("md", "## 6. Multi-head attention — the concept\n"
           "Real Transformers run attention **several times in parallel** (multiple "
           "'heads'), each with its **own** Wq/Wk/Wv. One head might track grammar, "
           "another long-range references. The heads' outputs are concatenated. We "
           "don't build a full Transformer here — just see that more heads = more "
           "*kinds* of relationships captured at once."),
    ("code", "def make_head(seed):\n"
             "    rng = np.random.RandomState(seed)\n"
             "    Wq, Wk, Wv = (rng.randn(d, d) * 0.5 for _ in range(3))\n"
             "    out, w = attention(X @ Wq, X @ Wk, X @ Wv)\n"
             "    return w\n\n"
             "heads = [make_head(s) for s in (1, 2, 3)]\n"
             "print('built', len(heads), 'attention heads, each (n x n):',\n"
             "      [h.shape for h in heads])\n"
             "# different heads -> different attention patterns\n"
             "assert not np.allclose(heads[0], heads[1])\n"
             "print('assert passed: heads learn DIFFERENT patterns ✔')"),

    ("md", "## 7. Try it on YOUR words (S-exercise)\n"
           "Swap in your own short sentence below and re-run to get a fresh heatmap. "
           "Notice the weights still form a valid distribution (each row sums to 1)."),
    ("code", "my_words = ['ai', 'is', 'fun', 'today']   # <- change me\n"
             "m = len(my_words)\n"
             "Xv = np.random.randn(m, d)\n"
             "Qv, Kv, Vv = Xv @ Wq, Xv @ Wk, Xv @ Wv\n"
             "out_v, w_v = attention(Qv, Kv, Vv)\n"
             "print('your sentence:', my_words)\n"
             "print('attention rows sum to 1:', np.round(w_v.sum(axis=1), 4))\n"
             "assert np.allclose(w_v.sum(axis=1), 1.0)\n"
             "print('assert passed: your attention is a valid distribution ✔')"),

    ("md", "---\n### Recap\n"
           "Q/K/V → **QKᵀ/√d** → **softmax** → **weighted sum of V**. That four-step "
           "engine, stacked in many layers and many heads, **is** the Transformer "
           "behind every LLM. You computed it in NumPy and saw the attention heatmap "
           "that researchers use to interpret what a model is doing."),
]
build_notebook(attention, os.path.join(CODE, "04_attention_from_scratch.ipynb"))

print("wrote Week 8 notebooks to", CODE)
