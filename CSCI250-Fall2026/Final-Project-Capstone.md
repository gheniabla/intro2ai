# 🏆 Final Project — Build "My Assistant"
**CSCI 250 · Fall 2026 · 20% of your grade · Due Dec 19, 11:59 PM PT**

Your final project isn't a separate thing you cram at the end. It's **"My Assistant"** — one AI application you start in Week 8 and **upgrade a little every week**, then polish for finals. By Week 17 you'll have a working, deployed, evaluated app you'd be proud to show an employer.

---

## The big idea
Pick something **you** care about and build an AI assistant for it. Use your own data and interests — students who do this build the best projects. Examples: a study buddy over your course notes, a recipe helper, a fantasy-sports analyst, a plant-care advisor, a code reviewer for your own repos.

You'll grow it through the term:

| Version | Week | What it can do |
|---|---|---|
| **v1** | 9 | A chatbot with a **role/system prompt** and a reasoning style |
| **v2** | 11 | Answers from **your own documents** (RAG) |
| **v3** | 13 | Can **call a tool** (search, calculator, database, API), with a safety guardrail |
| **v4** | 15 | Accepts an **image or other media** (optional, for the Multimodal track) |
| **Capstone** | 17 | Polished, **deployed**, **evaluated**, documented |

---

## Pick a track (choose one)
You only need to go deep on **one** of these for the final. The others are optional bonus.

1. **🔎 RAG Assistant** — a domain expert grounded in a corpus you choose. Must do retrieval + grounding + an evaluation of answer quality.
2. **🛠️ Tool-Using Agent** — a reason→act→observe agent that calls **2+ tools** to complete multi-step tasks, with a safety guardrail.
3. **🖼️ Multimodal App** — accepts image/audio input (receipt parser, chart explainer, plant identifier).
4. **🎚️ Fine-Tuned Specialist** — a small open model fine-tuned for a narrow task, with **before/after** evaluation, pushed to the Hugging Face Hub.

**Every track must:** run on **free tiers**, be **reproducible** (a grader can open it and it works), include an **evaluation scorecard** (using `tools/eval_utils.py` or your own), and ship as a **public demo** (a Gradio app on Hugging Face Spaces, or a clearly-documented Colab notebook).

---

## Milestones (so you're never behind)
Each milestone is a small graded checkpoint inside the weekly assignments — not extra work, just your project moving forward.

| # | Due | Deliverable |
|---|---|---|
| **M1 — Proposal + prototype** | Week 9 | One paragraph: your idea, track, and data. A "wow in 5 min" demo cell that runs. |
| **M2 — Core build** | Week 11 | The central capability works end-to-end (RAG retrieves & grounds / agent loops / etc.). |
| **M3 — Evaluation harness** | Week 14 (prep) | An auto-scorecard that measures your system (RAG triad, task accuracy, or LLM-as-judge). |
| **M4 — Hardening** | Week 16 | Guardrails (input/output checks), a short red-team attempt, and a cost report. |
| **M5 — Ship it** | Week 17 | Public demo + README + **3-minute screencast** + honest "limitations" section. |

> A low bar to **pass** (your scorecard exists and shows any measured improvement) and a high ceiling to **excel** — so you're rewarded for going further, not punished for starting simple.

---

## Grading rubric (100 points → scaled to the 20 course points)
This 100-point rubric is what your final submission is scored against; that score is then **scaled to the 20 points** the Capstone contributes to your course grade (e.g., 90/100 → 18/20). The five milestones (M1–M5, which sum to 20 as checkpoints) are the staged path to this final submission.

| Criterion | Pts | What "excellent" looks like |
|---|---:|---|
| **It runs** (reproducible; deploys on a free tier) | 20 | Grader opens the Space/notebook and it works first try; costs documented |
| **Core technique** correctly applied | 25 | RAG retrieves & grounds / agent loops & calls tools / fine-tune improves a metric — done right, not just imported |
| **Evaluation** | 20 | A real harness + scorecard; **baseline vs. improved with numbers**, not vibes |
| **Safety & cost-awareness** | 10 | Guardrails present; a red-team attempt; cost/caching addressed; runs on free tier |
| **Compare-models reflection** | 10 | Justifies the model choice across Claude / Gemini / Ollama **with evidence** |
| **Communication** | 15 | Clear README, "what you'll see," 3-min screencast, honest limitations |

**Presentation:** short recorded demo (≤3 min) submitted by Dec 19; live presentation slots announced by Nov 30.

---

## What to submit (Week 17)
1. **Link** to your deployed demo (HF Space) or a self-contained Colab notebook.
2. **Code repo** (GitHub) with a README that includes a "What you'll see when you run this" banner and setup steps.
3. **Evaluation scorecard** (numbers: baseline vs. final).
4. **3-minute screencast** walking through the app and one thing you'd improve.
5. A short **AI-Use note** (which AI tools helped you build it, and how).

---

## Need an idea? Starter prompts
- *Study buddy:* RAG over your own lecture notes + past quizzes; evaluate with questions you know the answers to.
- *Repo reviewer:* an agent that reads a small repo and flags issues, using a code-search tool (built partly with Claude Code in Week 12).
- *Receipt/Doc parser:* multimodal app that turns an image into structured JSON; evaluate accuracy against known values.
- *Tiny specialist:* fine-tune a small model to write in a specific style/format; judge before vs. after with Gemini-as-judge.

Bring your idea to **office hours** or the **Q&A board** any time — earlier is better.
