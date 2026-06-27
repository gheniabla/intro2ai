# Week 14 — Thanksgiving Recess & Capstone Evaluation Harness (M3)
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of November 23, 2026 · Online / Asynchronous · No new lecture content*

---

> **This is a light week.** Palomar is in **Thanksgiving recess** — there are no new lectures, slides, or sample notebooks. Your Capstone proposal is already done (that was **Milestone M1** back in Week 9), so this week is about **measuring what you've built**: complete **Capstone Milestone M3 — build your evaluation harness** using the shared helper `tools/eval_utils.py` (see `capstone/M3.md`). Spend your reduced hours (~4–6) turning "it feels better" into a number you can defend.

---

## Learning objectives
By the end of this week you will be able to:
1. Build an **evaluation harness** for your Capstone using `tools/eval_utils.py` (Claude/Gemini as judge, exact-match, scorecard — **no OpenAI**).
2. Assemble a small, honest **test set** of representative cases and pick **track-appropriate metrics**.
3. Score your assistant and turn "it feels better" into a **baseline-vs-improved number**.
4. Read the **scorecard** critically and write a 2–3 sentence read of what the numbers say.
5. Keep scope realistic over a short holiday week — **a small honest test set beats a big sloppy one.**

---

## 1. The Final Project at a glance
The Final Project is the capstone of CSCI 250. It asks you to combine the semester's threads — LLM APIs, prompt engineering, RAG, agents, AI-assisted coding, and (next week) multimodal models — into **one working application or study that you designed and can explain**.

You may use AI assistants heavily (this is an AI course), but **you own and must understand every line you submit**, and you must **disclose** your AI use. The final *presentation/demo* is where you prove you understand it.

| Item | Detail |
|---|---|
| **Proposal (Capstone M1)** | Done in **Week 9** |
| **This week (Capstone M3)** | **Evaluation harness** — due **end of Week 14** |
| **Project arc** | Built across the Capstone milestones M1–M5 (Weeks 9–17) |
| **Final submission** | Due **December 19, 2026, 11:59 PM PT** |
| **Weight** | See syllabus (the Capstone is the largest single graded item) |
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
| **Week 9** | **M1 — proposal + "My Assistant" v1** (done). |
| **Week 11** | **M2 — core build**: your assistant's central capability runs end-to-end. |
| **Week 14 (now)** | **M3 — evaluation harness**: build a scorecard with `tools/eval_utils.py` and report a baseline-vs-improved number. |
| **Week 16** | **M4 — hardening / polish**: fix the top failures the harness exposed; wire in real data; start the report. |
| **Week 17** | **M5 — finals**: final eval, demo, report, and presentation. **Submit by Dec 19.** |

**Rule of thumb:** if your M3 harness can't yet score your assistant on a handful of cases, **shrink the test set** until it can — a working scorecard now beats a perfect one never.

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
- **Capstone Milestone M3 handout** (`capstone/M3.md`) and the **rubric above** (Canvas) — required.
- Re-skim your notes from the track week you chose (10/11 RAG, 12 Claude Code, 13 Agents/MCP).
- *A Practical Guide to Building Agents* and the *Compact Guide to LLMs* (Canvas resources) — for Tracks B and A/E.
- Optional: browse past student demos (Canvas) for scope calibration.

---

## 8. Lab — Capstone Milestone M3: Evaluation Harness (due Sunday 11:59 PM PT)
This holiday week's graded deliverable is **Capstone Milestone M3 — build your evaluation harness** (see `capstone/M3.md`). The goal is to **measure your assistant, not just vibe-check it**: turn "it feels better" into "it scored 3.1 → 4.2." Use the shared helper `tools/eval_utils.py`, which gives you `llm_judge` (Claude or Gemini as judge), `exact_match`, and `scorecard`, and degrades gracefully with no API key so notebooks never crash.

1. **Build a test set** of 8–15 representative cases — reuse the inputs you collected during M2. Each case is a dict; include `expected` where you know the right answer.
2. **Score with `eval_utils`.** For example:
   ```python
   from eval_utils import llm_judge, exact_match, scorecard
   rows = [{**c, **llm_judge(c["q"], run_my_assistant(c["q"]), rubric)} for c in cases]
   scorecard(rows)
   ```
3. **Pick track-appropriate metrics:** RAG → the **RAG triad** (relevant retrieval / grounded answer / answers the question); Agent → **task success rate** + correct tool selection; Multimodal → **field accuracy** via `exact_match`; Fine-tuned → **before vs. after** on the same cases.
4. **Report a baseline-vs-improved number:** run the scorecard on at least two versions of your assistant and record both averages, plus a 2–3 sentence read of what the numbers say.

*M3 is a **4-pt Capstone checkpoint** (see the rubric in `capstone/M3.md`). Submit a runnable harness plus a scorecard with real numbers — evidence beats vibes. Keep it light: this is a ~4–6 hour holiday week.*

---

## Key terms
**Final Project**, **proposal**, **project track**, **RAG**, **agent**, **multimodal**, **fine-tuning**, **evaluation harness**, **LLM-as-judge**, **milestone**, **rubric**, **demo**, **scope**, **AI-Use disclosure**.
