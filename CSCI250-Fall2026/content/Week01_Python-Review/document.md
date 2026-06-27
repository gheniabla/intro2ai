# Week 1 — Python Review & AI Development Environment
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of August 24, 2026 · Online / Asynchronous*

---

## Learning objectives
By the end of this week you will be able to:
1. Navigate the course (Canvas, weekly rhythm, how to get help) and the syllabus expectations.
2. Refresh core Python you will rely on all semester: data types, control flow, functions, and modules.
3. Stand up your AI development environment: Google Colab, Git/GitHub, and API access to **Anthropic Claude** and **Google Gemini**, plus a local model with **Ollama**.
4. Make your **first AI API call** and run your **first local model**.
5. Take a first look at **AI-assisted coding** with **Claude Code**.

> **Time budget:** ~10 hours this week (lecture + slides + videos + Lab A1).

---

## 1. Welcome & how this course works
This is a hands-on, project-based introduction to Artificial Intelligence with a strong emphasis on **Large Language Models (LLMs), Generative AI, and AI-assisted coding**. Each week a Module opens on Monday with:
- a **lecture document** (this file) and **slides**,
- **sample code** notebooks to run and modify,
- short **videos** and a **reading list**, and
- a **lab/assignment** due Sunday 11:59 PM Pacific.

Read the syllabus in full this week. Note the two **office hours** (Tue 5–6 PM, Sat 10–11 AM PT on Zoom) and the **"CSCI250 -"** email subject prefix.

### A note on using AI in an AI course
You are encouraged to use AI assistants (Claude, Gemini, Claude Code) on assignments — but **you own everything you submit** and must be able to explain it. Exams are AI-restricted. Always add a short "AI Use" note to assignments. See the syllabus for the full policy.

---

## 2. Python refresher
We assume CSCI 114. Here is the subset of Python we use constantly.

### 2.1 Core data types
- **int, float, bool, str** — scalars.
- **list** — ordered, mutable: `nums = [1, 2, 3]`.
- **tuple** — ordered, immutable: `point = (3, 4)`.
- **dict** — key→value: `config = {"model": "claude", "temp": 0.7}`.
- **set** — unique items: `{1, 2, 2}` → `{1, 2}`.

### 2.2 Control flow
```python
for i in range(3):
    if i % 2 == 0:
        print(i, "even")
    else:
        print(i, "odd")
```

### 2.3 Functions
```python
def greet(name: str, excited: bool = False) -> str:
    msg = f"Hello, {name}"
    return msg + "!" if excited else msg
```
Type hints (`name: str`) are optional but we use them — they make AI assistants and your classmates understand your intent.

### 2.4 Modules, packages, and `pip`
Python organizes code into **modules** (files) and **packages** (folders). You install third-party packages with `pip`:
```bash
pip install anthropic google-generativeai
```
In Colab, prefix shell commands with `!`: `!pip install anthropic`.

### 2.5 List comprehensions & f-strings (used everywhere)
```python
squares = [x * x for x in range(5)]          # [0, 1, 4, 9, 16]
print(f"There are {len(squares)} squares.")  # f-string formatting
```

---

## 3. The AI development environment

### 3.1 Google Colab (recommended)
Colab runs Python notebooks in your browser with free GPUs — no install needed. Go to <https://colab.research.google.com>, sign in with Google, and open a new notebook. This is where most of our `.ipynb` sample code runs.

### 3.2 Git & GitHub
Version control is a professional baseline and required for the AI-assisted coding weeks.
```bash
git init
git add .
git commit -m "first commit"
```
Create a free GitHub account and (recommended) apply for the **GitHub Student Developer Pack**.

### 3.3 API keys — keep them secret
This semester we use three model sources:

| Source | What it is | Get a key |
|---|---|---|
| **Anthropic Claude** | Frontier hosted LLM + **Claude Code** | console.anthropic.com |
| **Google Gemini** | Hosted LLM + AI Studio | aistudio.google.com |
| **Ollama** | Run open models **locally**, no key, no cost | ollama.com |

**Never** paste an API key into code you share or commit. In Colab, store keys with the **Secrets** panel (🔑 icon) and read them with `userdata.get(...)`. Locally, use environment variables.

### 3.4 First look at Claude Code
**Claude Code** is a command-line AI coding assistant. We use it in Week 12. Install preview:
```bash
npm install -g @anthropic-ai/claude-code
claude        # starts an interactive coding session in your project
```
For now, just install it and run `claude --help` so it's ready.

---

## 4. Hello, AI — your first calls
This week's notebooks walk through:
- **Claude** (`anthropic` SDK)
- **Gemini** (`google-generativeai` SDK)
- **Ollama** (local, via its REST API or the `ollama` package)

A minimal Claude call looks like:
```python
import anthropic
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    messages=[{"role": "user", "content": "Explain what an LLM is in 2 sentences."}],
)
print(msg.content[0].text)
```

See `code/02_first_ai_calls.ipynb` for the full, runnable versions of all three.

---

## 5. Reading & videos
- **Syllabus** and **Class Schedule** (Canvas) — required.
- *Machine Learning Systems* (mlsysbook.ai) — skim the preface/intro.
- Video: "Google Colab Intro" (linked in Canvas).
- Anthropic and Google "quickstart" docs (linked in Canvas).

---

## 6. Lab — Assignment A1 (due Sunday 11:59 PM PT)
**Goal:** prove your environment works and make your first AI calls.

1. Open `code/01_python_review.ipynb`, complete the 5 short exercises.
2. Open `code/02_first_ai_calls.ipynb`. Add your API keys (via Colab Secrets) and run all cells so you get a response from **Claude** and **Gemini**. Running a **local** model (Ollama) is **optional in Colab** (no server is started there) — do it only if you're running locally or you start a server in Colab first.
3. Install **Claude Code** and paste the output of `claude --help`.
4. Write a 150-word reflection: what surprised you about the three models' answers to the same prompt?
5. **Submit:** your completed notebooks (or Colab share links) + the reflection. Include a one-line **AI Use** note.

*A1 is graded for completion/effort (see syllabus).*

---

## Key terms
**LLM**, **API key**, **notebook (.ipynb)**, **Colab**, **repository**, **commit**, **local model**, **token**, **prompt**.
