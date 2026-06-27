"""Build Week 16 sample-code notebooks. Run: python build_code.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# ---------------------------------------------------------------- notebook 1
lora_demo = [
    ("md", "# Week 16 · Notebook 1 — LoRA / PEFT Fine-Tuning Demo\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Fine-tune a **tiny open model** with **LoRA** (low-rank adapters) on a few "
           "instruction examples, using the Hugging Face stack — **no OpenAI**.\n\n"
           "> **Run on a GPU:** Runtime → Change runtime type → **T4 GPU**.\n"
           "> Every heavy import is guarded with try/except, so the notebook degrades "
           "gracefully (clear message) if a GPU or library is missing."),
    ("md", "## 0. Install the Hugging Face fine-tuning stack"),
    ("code", "!pip -q install transformers datasets peft accelerate bitsandbytes 2>/dev/null\n"
             "print('installed (or already present)')"),
    ("md", "## 1. Check the environment\n"
           "We confirm a GPU is available and report VRAM. The demo still *builds* without "
           "one, but real training needs a GPU."),
    ("code", "HAS_GPU = False\n"
             "try:\n"
             "    import torch\n"
             "    HAS_GPU = torch.cuda.is_available()\n"
             "    if HAS_GPU:\n"
             "        name = torch.cuda.get_device_name(0)\n"
             "        vram = torch.cuda.get_device_properties(0).total_memory / 1e9\n"
             "        print(f'GPU: {name}  ~{vram:.1f} GB VRAM')\n"
             "    else:\n"
             "        print('No GPU detected. Switch the Colab runtime to a T4 GPU to train.')\n"
             "except Exception as e:\n"
             "    print('PyTorch not available yet:', e)"),
    ("md", "## 2. Memory math (why we use LoRA + quantization)\n"
           "A rough rule for *loading* a model for inference:\n"
           "- FP16 ~2 GB / billion params · 8-bit ~1 GB/B · 4-bit ~0.5 GB/B.\n"
           "Training needs far more (gradients + optimizer + activations) — so we freeze the "
           "base model and train only small **LoRA adapters**."),
    ("code", "def loading_gb(params_billions, bits=16):\n"
             "    return params_billions * (bits / 8) * 2  # ~2 bytes/param at 16-bit\n\n"
             "for b in [16, 8, 4]:\n"
             "    print(f'7B model @ {b}-bit: ~{loading_gb(7, b):.1f} GB to load')"),
    ("md", "## 3. A tiny instruction dataset\n"
           "Quality > quantity. Real projects use hundreds of clean, consistent examples; "
           "here we use a handful so the demo runs fast."),
    ("code", "train_examples = [\n"
             "    {'instruction': 'Summarize in one sentence.',\n"
             "     'input': 'The mitochondria is the powerhouse of the cell.',\n"
             "     'output': 'Mitochondria produce most of the cell\\'s energy.'},\n"
             "    {'instruction': 'Summarize in one sentence.',\n"
             "     'input': 'Python is a high-level, readable, general-purpose language.',\n"
             "     'output': 'Python is a readable general-purpose programming language.'},\n"
             "    {'instruction': 'Summarize in one sentence.',\n"
             "     'input': 'A GPU runs many matrix operations in parallel.',\n"
             "     'output': 'GPUs do parallel matrix math, ideal for neural networks.'},\n"
             "]\n"
             "def format_example(ex):\n"
             "    return (f\"### Instruction: {ex['instruction']}\\n\"\n"
             "            f\"### Input: {ex['input']}\\n\"\n"
             "            f\"### Response: {ex['output']}\")\n"
             "print(format_example(train_examples[0]))"),
    ("md", "## 4. Load a small base model + attach a LoRA adapter\n"
           "We use a tiny open model so it fits on a free Colab GPU. The base weights are "
           "**frozen**; only the LoRA `A`/`B` matrices train (often <1% of params)."),
    ("code", "MODEL_ID = 'sshleifer/tiny-gpt2'  # tiny open model — fast demo\n"
             "model = tokenizer = None\n"
             "try:\n"
             "    from transformers import AutoModelForCausalLM, AutoTokenizer\n"
             "    from peft import LoraConfig, get_peft_model\n"
             "    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)\n"
             "    if tokenizer.pad_token is None:\n"
             "        tokenizer.pad_token = tokenizer.eos_token\n"
             "    model = AutoModelForCausalLM.from_pretrained(MODEL_ID)\n"
             "    lora = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05,\n"
             "                      target_modules=['c_attn'], task_type='CAUSAL_LM')\n"
             "    model = get_peft_model(model, lora)\n"
             "    model.print_trainable_parameters()  # see the <1% figure\n"
             "except Exception as e:\n"
             "    print('Could not load model/PEFT (no GPU or libs?):', e)\n"
             "    print('That is OK — the rest of the notebook still explains the workflow.')"),
    ("md", "## 5. Tokenize and train for a couple of epochs\n"
           "We keep `num_train_epochs` tiny so it finishes quickly. Watch the **loss** drop. "
           "If validation loss rises while training loss falls, you are **overfitting**."),
    ("code", "try:\n"
             "    from datasets import Dataset\n"
             "    from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling\n"
             "    texts = [format_example(e) for e in train_examples]\n"
             "    ds = Dataset.from_dict({'text': texts})\n"
             "    def tok(batch):\n"
             "        return tokenizer(batch['text'], truncation=True, padding='max_length', max_length=64)\n"
             "    ds = ds.map(tok, batched=True, remove_columns=['text'])\n"
             "    collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)\n"
             "    args = TrainingArguments(output_dir='out', num_train_epochs=3,\n"
             "        per_device_train_batch_size=1, learning_rate=2e-4,\n"
             "        logging_steps=1, report_to=[])\n"
             "    trainer = Trainer(model=model, args=args, train_dataset=ds, data_collator=collator)\n"
             "    trainer.train()\n"
             "    print('Training complete.')\n"
             "except Exception as e:\n"
             "    print('Skipping training (no GPU/model):', e)"),
    ("md", "## 6. Save just the adapter (megabytes, not gigabytes)\n"
           "You ship the small adapter and load it on top of the same base model. You can keep "
           "many task adapters for one base model."),
    ("code", "try:\n"
             "    model.save_pretrained('my_lora_adapter')\n"
             "    import os\n"
             "    files = os.listdir('my_lora_adapter')\n"
             "    print('Adapter saved:', files)\n"
             "except Exception as e:\n"
             "    print('Nothing to save (training did not run):', e)"),
    ("md", "## 7. Takeaways\n"
           "- LoRA trains a tiny fraction of params and saves a small **adapter**.\n"
           "- **QLoRA** loads the frozen base in 4-bit so even big models fit one GPU.\n"
           "- Fine-tune only after prompting and RAG fall short.\n"
           "- Always keep a validation split and watch for **overfitting**."),
]
build_notebook(lora_demo, os.path.join(CODE, "01_lora_finetune_demo.ipynb"))

# ---------------------------------------------------------------- notebook 2
serving = [
    ("md", "# Week 16 · Notebook 2 — Serving an LLM Pipeline (GenAI Ops Sketch)\n"
           "**CSCI 250 · Fall 2026**\n\n"
           "Wrap an LLM call behind a small **API service**, add basic **monitoring** "
           "(latency + token cost), and discuss cost/latency levers. Uses **Claude** "
           "(swap in Gemini or a local model the same way). **No OpenAI.**"),
    ("md", "## 0. Install + load keys safely"),
    ("code", "!pip -q install anthropic flask\n"
             "import os\n"
             "try:\n"
             "    from google.colab import userdata\n"
             "    os.environ['ANTHROPIC_API_KEY'] = userdata.get('ANTHROPIC_API_KEY')\n"
             "except Exception:\n"
             "    pass  # locally, set ANTHROPIC_API_KEY in your shell\n"
             "print('Anthropic key set:', bool(os.environ.get('ANTHROPIC_API_KEY')))"),
    ("md", "## 1. A monitored pipeline function\n"
           "Before serving, build a plain function that calls the model **and records "
           "latency + token usage**. This is the core of GenAI Ops monitoring."),
    ("code", "import time\n"
             "MODEL = 'claude-haiku-4-5-20251001'  # smallest sufficient model = cheaper, faster\n\n"
             "def pipeline(user_msg, max_tokens=200):\n"
             "    try:\n"
             "        import anthropic\n"
             "        client = anthropic.Anthropic()\n"
             "        t0 = time.time()\n"
             "        msg = client.messages.create(\n"
             "            model=MODEL, max_tokens=max_tokens,\n"
             "            messages=[{'role': 'user', 'content': user_msg}])\n"
             "        dt = time.time() - t0\n"
             "        log = {'latency_s': round(dt, 2),\n"
             "               'in_tokens': msg.usage.input_tokens,\n"
             "               'out_tokens': msg.usage.output_tokens}\n"
             "        return msg.content[0].text, log\n"
             "    except Exception as e:\n"
             "        return f'[no API key / offline: {e}]', {'latency_s': None}\n\n"
             "reply, log = pipeline('Explain LoRA in one sentence.')\n"
             "print('REPLY:', reply)\n"
             "print('MONITOR:', log)"),
    ("md", "## 2. Estimate cost from token usage\n"
           "LLMs are priced per token (input + output). Track tokens per request so cost "
           "never surprises you. (Use current published prices; values below are illustrative.)"),
    ("code", "# Illustrative per-million-token prices — check the current pricing page.\n"
             "PRICE_IN, PRICE_OUT = 1.00, 5.00  # $ per 1M tokens (example)\n\n"
             "def estimate_cost(log):\n"
             "    if not log.get('in_tokens'):\n"
             "        return None\n"
             "    return (log['in_tokens'] * PRICE_IN + log['out_tokens'] * PRICE_OUT) / 1e6\n\n"
             "c = estimate_cost(log)\n"
             "print('estimated request cost: $%.6f' % c if c is not None else 'no usage to price')"),
    ("md", "## 3. Serve it as an API (Flask)\n"
           "This cell *defines* the service. In Colab you would expose it with a tunnel; "
           "on a server you run `flask run` or deploy behind gunicorn. The key idea: your "
           "pipeline + monitoring now has an HTTP endpoint other apps can call."),
    ("code", "from flask import Flask, request, jsonify\n"
             "app = Flask(__name__)\n\n"
             "@app.post('/chat')\n"
             "def chat():\n"
             "    user_msg = (request.json or {}).get('message', '')\n"
             "    reply, log = pipeline(user_msg)\n"
             "    log['cost_usd'] = estimate_cost(log)\n"
             "    return jsonify({'reply': reply, 'monitor': log})\n\n"
             "print('Flask app defined. Endpoints:', [r.rule for r in app.url_map.iter_rules()])"),
    ("md", "## 4. Test the endpoint in-process\n"
           "Use Flask's test client so we don't need a live server to verify the contract."),
    ("code", "client = app.test_client()\n"
             "resp = client.post('/chat', json={'message': 'Say hello in 5 words.'})\n"
             "print('HTTP', resp.status_code)\n"
             "print(resp.get_json())"),
    ("md", "## 5. Cost & latency levers (the GenAI Ops checklist)\n"
           "- **Smallest sufficient model**; route easy queries to a cheap model (Haiku/Flash), "
           "hard ones to a strong model (Opus/Pro).\n"
           "- **Cap `max_tokens`** and shorten context (let RAG fetch only what's needed).\n"
           "- **Cache** repeated prompts/answers; use prompt caching for long shared context.\n"
           "- **Self-hosted?** quantize and batch.\n"
           "- **Always log** prompts + responses, then re-score with an eval harness (Week 17)."),
    ("md", "## 6. Self-hosted alternative (local, no key)\n"
           "The same pipeline shape works with a **local** model via Ollama — privacy and "
           "per-token control, at the cost of running the hardware yourself."),
    ("code", "def local_pipeline(user_msg):\n"
             "    try:\n"
             "        import ollama, time\n"
             "        t0 = time.time()\n"
             "        out = ollama.chat(model='llama3.2',\n"
             "                          messages=[{'role': 'user', 'content': user_msg}])\n"
             "        return out['message']['content'], {'latency_s': round(time.time()-t0, 2)}\n"
             "    except Exception as e:\n"
             "        return f'[Ollama not running: {e}]', {}\n\n"
             "print(local_pipeline('Explain quantization in one sentence.'))"),
]
build_notebook(serving, os.path.join(CODE, "02_serving_sketch.ipynb"))

print("wrote Week 16 notebooks to", CODE)
