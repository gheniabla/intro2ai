# Week 14 — Thanksgiving Recess & Final Project Prep
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of November 23, 2026 · Online / Asynchronous · No new lecture content*

---

> **This is a light week.** Palomar is in **Thanksgiving recess** — there are no new lectures, slides, or sample notebooks. Instead, use the quieter week to **lock in your Final Project plan** and submit **Assignment A7: Final Project Proposal**. Everything you build in Weeks 15–17 will hang off the decision you make now, so spend your reduced hours (~4–6) wisely.

---

## Learning objectives
By the end of this week you will be able to:
1. Choose a **Final Project track** that fits your interests and the course stack (Claude, Gemini, local/open models — **no OpenAI**).
2. Write a focused **proposal** that names the problem, the users, the data, and the AI components.
3. Lay out a **milestone plan** across Weeks 15–17 that lands a working demo by the Dec 19 deadline.
4. Read and internalize the **grading rubric** so you build the right things.
5. Pick a realistic scope — **small and finished beats big and broken.**

---

## 1. The Final Project at a glance
The Final Project is the capstone of CSCI 250. It asks you to combine the semester's threads — LLM APIs, prompt engineering, RAG, agents, AI-assisted coding, and (next week) multimodal models — into **one working application or study that you designed and can explain**.

You may use AI assistants heavily (this is an AI course), but **you own and must understand every line you submit**, and you must **disclose** your AI use. The final *presentation/demo* is where you prove you understand it.

| Item | Detail |
|---|---|
| **Proposal (A7)** | Due **end of Week 14** (this week) |
| **Project arc** | Built across Weeks 15–17 |
| **Final submission** | Due **December 19, 2026, 11:59 PM PT** |
| **Weight** | See syllabus (the largest single graded item) |
| **Team size** | Solo, or pairs with instructor approval (scope scales up for pairs) |

---

## 2. Choose a track
Pick **one** of the five tracks below. Each maps directly to weeks you have already completed (or are about to), so you are not starting from zero.

### Track A — RAG application *(builds on Weeks 10–11)*
A question-answering app **grounded in a document set you choose** (course PDFs, a hobby wiki, product manuals, research papers). Chunk → embed → store in a vector DB (ChromaDB) → retrieve → answer with **Claude** or **Gemini**, with citations back to the source.

### Track B — Agent / tool-using assistant *(builds on Week 13)*
An agent that **calls tools** to accomplish a goal: e.g., a research assistant that searches + summarizes, a "data analyst" that runs Python on a dataset, or a task bot exposed over **MCP** or a small **Flask** API. Must show a real **agent loop** (model decides → calls tool → observes → continues).

### Track C — AI-assisted coding tool *(builds on Week 12)*
A developer tool you **build with Claude Code** and that itself uses an LLM: e.g., a code reviewer, a docstring/test generator, a commit-message writer, or a "explain this repo" CLI. Deliver a **tested** feature and document how AI helped you write it.

### Track D — Multimodal application *(builds on Week 15 — next week)*
An app that understands **images + text** (and optionally audio): e.g., a receipt/invoice extractor, a chart-reading assistant, an accessibility "describe this photo" tool, or a homework-helper that reads a photographed problem. Uses **Claude** or **Gemini** vision.

### Track E — Fine-tuning / evaluation study *(builds on Weeks 16–17)*
A **study**, not just an app. Either (1) fine-tune / PEFT-LoRA a small open model on a focused task and compare to a prompted baseline, **or** (2) build an **evaluation harness** (metrics + LLM-as-judge) that rigorously compares 2–3 models/prompts on a task. Deliverable is a **report with evidence**, plots, and an honest discussion of limits.

---

## 3. Deliverables
Every track submits the **same four artifacts**:

1. **Code** — a runnable repo or Colab notebook(s). Clean, organized, no hard-coded API keys (use Colab Secrets / env vars). Include a `README` with setup steps.
2. **Report** (~4–6 pages / ~1,500–2,500 words) — problem & motivation, design & architecture (a diagram helps), what you built, results/evaluation, **limitations & ethics**, and a short **AI-Use disclosure**.
3. **Recorded demo** (3–5 min) — screen recording showing the app/study actually running end-to-end. Narrate what is happening.
4. **Live(-ish) presentation** (~5 min, Week 17) — slides + the demo; be ready to answer "how does X work?" questions.

---

## 4. Milestone plan
Spread the work so nothing lands all at once in finals week.

| When | Milestone |
|---|---|
| **Week 14 (now)** | Submit **A7 proposal**: track, problem, data/inputs, AI components, success criteria, milestone dates. |
| **Week 15** | Spike the hardest unknown (e.g., the API call, the retrieval step, the agent loop). Get a **"hello world" end-to-end** path working, even if ugly. |
| **Week 16** | Build the core feature(s). Wire in your real data. Start the report's design section. |
| **Week 17** | Evaluate, polish, fix the top bugs, record the demo, finish the report, prep the presentation. **Submit by Dec 19.** |

**Rule of thumb:** if you do not have *something* running end-to-end by the end of Week 15, **cut scope** immediately.

---

## 5. Grading rubric
Total **100 points**. Your demo + report are how you earn the "understanding" points — code alone is not enough.

| Criterion | Pts | What we look for |
|---|---|---|
| **Working functionality** | 30 | The app/study runs end-to-end and does what the proposal promised. |
| **Technical design** | 20 | Sensible architecture; correct use of LLM/RAG/agent/multimodal pieces; appropriate model choice (Claude / Gemini / local). |
| **Code quality** | 15 | Organized, readable, no leaked keys, a `README`, reasonable error handling. |
| **Evaluation & results** | 15 | Evidence it works: test cases, metrics, example outputs, or a comparison study. Honest about failures. |
| **Report** | 10 | Clear problem framing, design, results, **limitations & ethics**, AI-Use disclosure. |
| **Demo & presentation** | 10 | Clear walkthrough; can answer "how does this work?" and "what would you do next?" |

**Automatic deductions:** hard-coded API keys (−5), no AI-Use disclosure (−5), cannot explain your own submitted code (up to −20, academic-integrity referral if egregious).

---

## 6. Four concrete example ideas
Use these as starting points — **narrow them down**, don't copy them wholesale.

1. **"Ask My Syllabus" (Track A — RAG).** Ingest this course's syllabus + schedule + a few lecture PDFs into ChromaDB; answer student questions ("When is the midterm? What's the late policy?") with **Claude** and cite the source section. Add a Gemini variant and compare answer quality.

2. **"Dataset Detective" (Track B — Agent).** An agent with two tools — `run_python(code)` and `describe_column(name)` — that takes a CSV and a plain-English question ("which region grew fastest?"), writes + runs pandas code in a loop, and returns an answer with a chart. Serve it behind a tiny **Flask** endpoint.

3. **"Receipt Reader" (Track D — Multimodal).** Upload a photo of a receipt or an invoice; use **Gemini / Claude vision** to extract vendor, date, line items, and total into clean JSON; flag low-confidence fields. Test on 10 sample images and report accuracy.

4. **"Model Judge" (Track E — Evaluation).** Pick a task (e.g., summarizing news blurbs). Build an eval harness that runs **Claude vs. Gemini vs. a local Ollama model**, scores each with an **LLM-as-judge** rubric plus one automatic metric (e.g., ROUGE), and produces a leaderboard + plots. Discuss where the judge itself is unreliable.

---

## 7. Reading & videos
- **Final Project Proposal (A7) prompt** and the **rubric above** (Canvas) — required.
- Re-skim your notes from the track week you chose (10/11 RAG, 12 Claude Code, 13 Agents/MCP).
- *A Practical Guide to Building Agents* and the *Compact Guide to LLMs* (Canvas resources) — for Tracks B and A/E.
- Optional: browse past student demos (Canvas) for scope calibration.

---

## 8. Lab — Assignment A7 (Final Project Proposal, due Sunday 11:59 PM PT)
Submit a **1-page proposal** (a form or short doc) containing:

1. **Title** and **track** (A–E).
2. **Problem & users:** what does it do, and for whom (2–3 sentences)?
3. **Inputs/data:** what data, documents, images, or dataset will you use? Where does it come from?
4. **AI components:** which models (Claude / Gemini / local) and techniques (RAG / agent / multimodal / fine-tune / eval)?
5. **Success criteria:** how will you know it works? (1–2 measurable checks.)
6. **Milestones:** one line each for Weeks 15, 16, 17.
7. **AI-Use note:** one line on how you plan to use AI assistants.

*A7 is graded for completeness and feasibility. The instructor will reply with scope feedback — read it before Week 15.*

---

## Key terms
**Final Project**, **proposal**, **project track**, **RAG**, **agent**, **multimodal**, **fine-tuning**, **evaluation harness**, **LLM-as-judge**, **milestone**, **rubric**, **demo**, **scope**, **AI-Use disclosure**.
