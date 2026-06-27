# 💸 Free-Tier Playbook — Run Everything in CSCI 250 for $0
**Keep this open. It's how you get keys, run models, and never hit a paywall.**

This course is designed so you never have to pay. Below: how to get each free account, how to keep your keys safe, and how to keep costs at zero.

---

## The three model sources we use

| Source | What it gives you | Free tier | Get it |
|---|---|---|---|
| **Google Gemini / AI Studio** | Hosted LLM, multimodal, generous free quota — our **default** for most labs | Free tier with daily request limits | aistudio.google.com → "Get API key" |
| **Anthropic Claude + Claude Code** | Frontier LLM, great at coding & tool use | Free starter credit; pay-as-you-go after | console.anthropic.com |
| **Ollama (local)** | Run open models on your own machine — **no key, no cost, no limits, works offline** | Always free | ollama.com → install → `ollama pull llama3.2` |
| **Hugging Face** | Open models, datasets, embeddings, free hosting (Spaces) | Free account | huggingface.co |

> **Default to the cheapest path.** Notebooks default to **Gemini Flash** or **Claude Haiku** (cheap, fast) or **local Ollama** (free). You almost never need the big expensive models for coursework.

---

## Where the code runs: Google Colab (no install)
- Go to **colab.research.google.com**, sign in with a Google account, and open any course `.ipynb`.
- Colab gives you a free Python environment **and a free GPU** (Runtime → Change runtime type → GPU) for the fine-tuning week.
- For local-only work (Ollama), you can also run notebooks in VS Code / Jupyter on your own machine.

---

## 🔑 Keeping your API keys safe (important)
**Never** type a key directly into a notebook cell, and **never** commit a key to GitHub. Two safe ways:

**In Colab — use the Secrets panel:**
1. Click the **🔑 key icon** in the left sidebar.
2. Add `GEMINI_API_KEY` and `ANTHROPIC_API_KEY` with your values; toggle "Notebook access" on.
3. In code:
   ```python
   from google.colab import userdata
   import os
   os.environ["GEMINI_API_KEY"] = userdata.get("GEMINI_API_KEY")
   os.environ["ANTHROPIC_API_KEY"] = userdata.get("ANTHROPIC_API_KEY")
   ```

**On your own machine — use environment variables:**
```bash
export GEMINI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
```
The SDKs read these automatically. If a key leaks, **revoke and regenerate it** in the provider console immediately.

---

## Keeping cost at $0 — habits
- **Read the notebook banner.** Every notebook tells you the expected cost (free) and which key it needs.
- **Use small models for development.** Test with Gemini Flash / Claude Haiku / Ollama; only reach for bigger models if a task truly needs it.
- **Cap your output.** Keep `max_tokens` modest while experimenting.
- **Prefer local (Ollama)** for high-volume looping/experiments — it's unlimited and offline.
- **Set a $0 budget alert** in the Anthropic console for peace of mind.
- **Final project must run on free tiers** — that's part of the rubric.

---

## "It's not working" — quick fixes
| Symptom | Fix |
|---|---|
| `AuthenticationError` / no key | Key not set — re-check Colab Secrets or your env var name. |
| `RateLimitError` / quota | You hit the free daily limit — switch to **Ollama (local)** or wait for the quota to reset. |
| `ModuleNotFoundError` | Run the notebook's `!pip -q install ...` cell. |
| Ollama "connection refused" | Start it: run `ollama serve` (or just `ollama run llama3.2`) in a terminal. |
| Colab GPU unavailable | Runtime → Change runtime type → GPU; if none free, the notebook's CPU fallback still works. |

Still stuck after 15 minutes? **Post in the Q&A board** with the error text — don't spin your wheels.

---

## Need hardware or internet?
Palomar's Library/Learning Resources lends **laptops and hotspots**. Colab works on a Chromebook. If access is a barrier, contact me in Week 1 — we'll find a solution.
