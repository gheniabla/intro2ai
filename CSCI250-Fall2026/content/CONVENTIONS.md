# Content Build Conventions — CSCI 250 (Fall 2026)

Every week's folder under `content/WeekNN_*/` must contain, all matching the **Week 1 gold standard**
(`content/Week01_Python-Review/`):

1. **`document.md`** — lecture notes. Sections: H1 title + course/date line; **Learning objectives**;
   numbered topic sections with short code blocks; **Reading & videos**; **Lab/assignment** (the week's
   A#/S# from the schedule, or "no assignment this week"); **Key terms**. Aim ~150–300 lines.
2. **`build_slides.py`** — imports `slidegen` from `../../tools`, defines a `slides=[...]` list, and on
   `__main__` writes `slides.pptx` next to itself. Use slide types: `title, section, bullets, code,
   two_col, closing`. ~10–14 slides. Always open with a `title` and a "This Week" bullets slide; always
   end with a `closing` "To Do" slide. Keep bullets short; put real code in `code` slides.
3. **`build_code.py`** — imports `build_notebook` from `nbgen` in `../../tools`, builds 1–2 runnable
   `.ipynb` into `code/`. Cells are `("md", text)` / `("code", text)` tuples.
4. Generated **`slides.pptx`** and **`code/*.ipynb`** (produced by running the two build scripts).

After writing the scripts, **run both** (`python build_slides.py && python build_code.py`) and confirm
`slides.pptx` has >0 slides and the notebooks are valid JSON.

## Stack rules (important)
- Models/tools allowed: **Anthropic Claude + Claude Code**, **Google Gemini / AI Studio**,
  **open-source/local via Hugging Face + Ollama**. **Do NOT use OpenAI / GPT.**
- Correct model IDs: Claude → `claude-opus-4-8`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`;
  Gemini → `gemini-2.5-flash`, `gemini-2.5-pro`. Anthropic SDK: `anthropic.Anthropic().messages.create(...)`.
  Gemini SDK: `google.generativeai`. Local: `ollama.chat(...)` / Hugging Face `transformers`.
- Never hard-code API keys. Load via Colab `userdata.get(...)` or environment variables.
- Notebooks should be runnable in **Google Colab** (use `!pip -q install ...`).

## Voice & framing
- Audience: CSCI 114 grads, online/asynchronous, ~10 hrs/week.
- Practical, hands-on, encouraging. Tie each week to the project arc and the schedule description.
- AI-use policy reminder where relevant: students may use AI but must understand & disclose; exams are AI-restricted.

## Quality patterns (applied across the LLM weeks — keep them when editing)
- **Notebook banner:** every notebook's FIRST markdown cell is:
  `## ▶ What you'll see when you run this` + one concrete output line, then a line:
  `**Time:** ~N min · **Cost:** free (cheapest model: Gemini Flash / Claude Haiku / local Ollama) · **Keys:** <none|GEMINI_API_KEY|ANTHROPIC_API_KEY>`
- **Wow in 5 minutes:** the first CODE cell after the banner produces a visible result fast.
- **Pre-filled, runnable:** ship working code students modify; reserve blank fill-ins for graded self-checks (`assert`s).
- **Dumbest-baseline-first:** show the simple thing failing (keyword search, naive prompt) before the better technique.
- **Build-by-hand, then framework:** from-scratch (NumPy) before LangChain/MCP.
- **Compare-models:** run the same prompt through Claude vs Gemini vs Ollama where relevant.
- **Evaluation throughline:** use `tools/eval_utils.py` (`llm_judge`, `exact_match`, `scorecard`). From a notebook in `content/WeekNN/code/`, the tools dir is **`../../../tools`** (build scripts at `content/WeekNN/` use `../../tools`); prefer an upward search for `tools/eval_utils.py` so it works in Colab too.
- **Capstone callout:** LLM weeks include a `> **🎯 Capstone checkpoint —** ...` note advancing "My Assistant" (v1 Wk9 → v2 Wk11 → v3 Wk13 → v4 Wk15). See `Final-Project-Capstone.md`.
- **Per-deliverable:** state a time estimate + rubric pointer (`Rubrics.md`); skills checks are pass/revise.

## Reusable source templates (from last year's Canvas export)
`../.canvas_export/web_resources/` contains the instructor's prior notebooks — mine them for structure,
topics, and depth (rewrite to the stack rules above; add Claude + local-model variants alongside Gemini):
- `chapter0-part1/2.ipynb`, `chapter1-4,7,8.ipynb` (Python→ML), `Regression_and_Classification.pptx`
- `prompt_engineering_gemini.ipynb`, `gemini_api_guide.ipynb`, `rag_with_google_gemini_v1.ipynb`
- `agentic_ai_with_gemini (1).ipynb`, `multimodal_ai_with_gemini (1).ipynb`
- `fine_tuning_llms_guide_v1.ipynb`, `gpu_for_llms_genai_V1.ipynb`
- PDFs: `compact-guide-to-large-language-models.pdf`, `a-practical-guide-to-building-agents.pdf`

## Per-week specifications (from Schedule.md)

| Wk | Folder | Title | Focus / details | Assignment |
|---|---|---|---|---|
| 2 | Week02_Data-Processing-NumPy | Python Data Processing & Analytics | Datasets & data manipulation with **NumPy** (arrays, vectorization, broadcasting, indexing) | A2 |
| 3 | Week03_Data-Visualization | Python Data Visualization | **Pandas** (DataFrames, groupby) + **Matplotlib** plotting; use A_Z handwritten data | A3 |
| 4 | Week04_Intro-AI-ML-scikit-learn | Introduction to AI & ML — scikit-learn | AI vs ML vs DL vs GenAI; the end-to-end ML workflow; **scikit-learn** basics (fit/predict, train/test) | — |
| 5 | Week05_Regression-Classification | Regression & Classification (Supervised) | Linear/logistic regression, k-NN, decision trees; metrics (MAE, accuracy, precision/recall, confusion matrix); overfitting | A5 |
| 6 | Week06_Neural-Networks-DL | Neural Networks & Deep Learning Foundations | Perceptron, layers, activations, loss, gradient descent, backprop; tiny net in PyTorch/Keras; brief CV & sequence tour — frame as the foundation under LLMs | — |
| 7 | Week07_ML-Review-Midterm | ML Review & Midterm | Review weeks 1–6; provide a **study guide** + **sample/practice midterm** (AI-restricted) + solutions notebook | Midterm Exam (Oct 11) |
| 8 | Week08_LLM-Concepts | LLM Concepts, Frameworks & Tools | How LLMs work: tokens, context window, sampling/temperature, capabilities & failure modes; calling **Claude & Gemini**; running **local** models (Ollama/HF) | S1 |
| 9 | Week09_Prompt-Engineering | Prompt Engineering | Zero/few-shot, role/system prompts, chain-of-thought, structured/JSON output; prompt patterns for Claude & Gemini | A4 |
| 10 | Week10_GenAI-Frameworks-Vector | GenAI Frameworks & Vector Storage | **LangChain & LlamaIndex** building blocks; chains; embeddings; build/query a **vector store** (ChromaDB) | — (Final Project ideas posted) |
| 11 | Week11_RAG | Retrieval-Augmented Generation | Embeddings, chunking, vector DB retrieval, grounding; build a working **RAG** pipeline over a doc set (Claude + Gemini variants) | — |
| 12 | Week12_AI-Assisted-Coding-ClaudeCode | AI-Assisted Software Development | **Claude Code** & agentic coding workflows; prompting for code; reviewing/testing/securing AI-generated code; build a tested feature in a starter repo | A6 |
| 13 | Week13_Agents-MCP | GenAI Agents & MCP | Agent loop; **tool/function calling**; **Model Context Protocol (MCP)**; build a small agent; serve via Flask | S2 |
| 14 | Week14_Thanksgiving-Final-Prep | No Class / Final Project Prep | **Light week**: only a `document.md` = Final Project Prep guide (A7): proposal scope, milestones, rubric, examples. **No slides, no code.** | A7 (Final Project Prep) |
| 15 | Week15_Multimodal-LLMs | Multi-modal LLMs & Generative Media | Multimodal APIs (text+image+audio) with Claude & Gemini; image understanding; overview of image generation (diffusion) | A7 cont. |
| 16 | Week16_FineTuning-GenAIOps | Fine-Tuning, GenAI Ops & Deployment | When/why to fine-tune vs prompt vs RAG; PEFT/LoRA concept; GPUs; deploying & serving LLM pipelines (GenAI Ops) | — |
| 17 | Week17_Evaluation-Safety-Finals | LLM & GenAI Evaluation, Safety & Finals | Evaluating LLM systems (metrics, LLM-as-judge, eval harness); GenAI safety, bias, hallucination, limits; final wrap-up | Final Project due Dec 19 |
