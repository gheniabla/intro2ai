# Capstone Milestones — "My Assistant" (CSCI 250 · Fall 2026)

Your final project is **one app, built across the term** — "My Assistant." You don't cram it at the end; you grow it through five small graded checkpoints (M1–M5) that live inside the weekly flow. Full spec, the four tracks, and the 100-pt project rubric are in [`../Final-Project-Capstone.md`](../Final-Project-Capstone.md).

**The milestones together are worth 20 points** (the Capstone grade). The finished project is still assessed against the **100-pt rubric** in the master spec — these milestones are the **staged path** that gets you there, low-stress and on time.

## The five milestones

| Milestone | Week | Due (Sun 11:59 PM PST) | Targets | Points |
|---|---|---|---|---:|
| [M1 — Proposal + Prototype](M1.md) | 9 | **Oct 25** | "My Assistant" v1 (role/system prompt + reasoning) | **3** |
| [M2 — Core Build](M2.md) | 11 | **Nov 8** | v2 (RAG over your docs / core capability per track) | **5** |
| [M3 — Evaluation Harness](M3.md) | 14 | **Nov 29** | auto-scorecard (uses `tools/eval_utils.py`) | **4** |
| [M4 — Hardening](M4.md) | 16 | **Dec 13** | guardrails + red-team + cost report | **3** |
| [M5 — Ship It + Present](M5.md) | 17 | **Dec 19** | public demo + README + 3-min screencast | **5** |
| | | | **Total** | **20** |

## The four tracks (pick one to go deep)
1. **🔎 RAG Assistant** — retrieval + grounding + answer-quality eval over a corpus you choose.
2. **🛠️ Tool-Using Agent** — a reason→act→observe agent calling 2+ tools, with a guardrail.
3. **🖼️ Multimodal App** — image/audio input → structured output.
4. **🎚️ Fine-Tuned Specialist** — a small open model fine-tuned for a narrow task, with before/after eval.

## Ground rules
- **Free tiers only** (Claude / Gemini / Ollama — **no OpenAI**).
- **Reproducible**: a grader can open it and it works.
- **Evaluated**: use [`../tools/eval_utils.py`](../tools/eval_utils.py) (`llm_judge`, `exact_match`, `scorecard`) for M3/M4.
- **Shipped**: a public Gradio/HF Spaces app or a documented Colab notebook.

Bring questions to **office hours** or the **Q&A board** — earlier is better.
