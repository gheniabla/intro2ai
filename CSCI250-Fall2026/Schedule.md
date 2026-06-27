# CSCI 250 — Introduction to Artificial Intelligence
## Class Schedule — Fall 2026 (Online, Asynchronous)

**Term:** Aug 24 – Dec 19, 2026 · Weekly modules open Mondays · **All assignments due Sunday 11:59 PM PST**

**Every week includes:** 🎥 a **Lecture Video**, 📖 a lecture document + slides, 💻 runnable notebook(s), ✅ an ungraded self-check, and (most weeks) 📝 a graded assignment.

**Holidays (campus closed):** Labor Day — Sep 7 · Native American Day — Sep 25 · Veterans’ Day — Nov 9 · Thanksgiving recess — Nov 23–28.

**Grading:** 10 Assignments (**A1–A10, 6 pts each = 60**) · Midterm Exam (**20**) · Capstone Final Project (**20**) = **100 pts**.

---

### Course Arc
Foundations & ML (Wks 1–6) → **Midterm** (Wk 7) → LLMs under the hood & prompting (Wks 8–9) → Frameworks, RAG & AI-assisted coding (Wks 10–13) → Multimodal, fine-tuning, evaluation & **Capstone** (Wks 14–17).

| No | Week | Description | Details | Materials | Events & Notes | Assignment (due Sun 11:59 PM PST) |
|---|---|---|---|---|---|---|
| 1 | Aug 24 | Python Review & AI Dev Environment | Syllabus & "Start Here." Python refresher (types, functions, modules). Set up Colab, Git/GitHub, API keys (Claude, Gemini), Ollama; first look at Claude Code. | 🎥 Lecture Video; document + slides; 01_python_review, 02_first_ai_calls | First week of the semester | **A1** (6) |
| 2 | Aug 31 | Python Data Processing & Analytics | Datasets & data manipulation with NumPy (arrays, vectorization, broadcasting, indexing). | 🎥 Lecture Video; document + slides; NumPy notebooks | — | **A2** (6) |
| 3 | Sep 7 | Python Data Visualization | Pandas (DataFrames, groupby) + Matplotlib (line/bar/scatter/hist). | 🎥 Lecture Video; document + slides; Pandas/viz notebooks | **Sep 7 Holiday → Labor Day** | **A3** (6) |
| 4 | Sep 14 | Introduction to AI & ML — scikit-learn | AI vs ML vs DL vs GenAI; end-to-end ML workflow; scikit-learn basics (fit/predict, train/test). | 🎥 Lecture Video; document + slides; ML-workflow notebooks | — | **A4** (6) |
| 5 | Sep 21 | Regression & Classification (Supervised) | Linear/logistic regression, k-NN, decision trees; metrics (MAE, accuracy, precision/recall, confusion matrix); overfitting. | 🎥 Lecture Video; document + slides; regression/classification notebooks | **Sep 25 Holiday → Native American Day** | **A5** (6) |
| 6 | Sep 28 | Neural Networks & Deep Learning Foundations | Perceptron, layers, activations, loss, gradient descent, backprop — the intuition that powers LLMs; brief CV & sequence tour. | 🎥 Lecture Video; document + slides; tiny-net + CNN/sequence notebooks | — | **A6** (6) |
| 7 | Oct 5 | ML Review & Midterm | Review Weeks 1–6. Study guide + practice midterm with solutions. | 🎥 Lecture Video; study guide + review/practice notebooks | **Midterm Exam: Oct 11, 5:30–11:59 PM PST (AI-restricted, 20 pts)** · Fast Track 1 ends Oct 17 | — |
| 8 | Oct 12 | LLM Concepts (under the hood) | How LLMs work, hands-on: **build a BPE tokenizer from scratch**, **attention from scratch**, context, sampling. Claude & Gemini APIs + local models (Ollama/HF). | 🎥 Lecture Video; document + slides; **03_build_bpe_tokenizer**, **04_attention_from_scratch** | 🎯 Start **"My Assistant"** | **A7** (6) |
| 9 | Oct 19 | Prompt Engineering | System prompts; structured/JSON output; **reasoning / chain-of-thought** & self-consistency (Claude vs Gemini). | 🎥 Lecture Video; document + slides; **03_reasoning_and_cot** | 🎯 **Capstone M1**: proposal + prototype | — *(capstone milestone)* |
| 10 | Oct 26 | GenAI Frameworks & Vector Storage | **Embeddings first** (cosine similarity by hand → top-k → ChromaDB), then LangChain/LlamaIndex building blocks. | 🎥 Lecture Video; document + slides; **00_embeddings_intuition**, langchain/llamaindex | Final Project ideas posted | **A8** (6) |
| 11 | Nov 2 | Retrieval-Augmented Generation (RAG) | RAG over your own docs; grounding; **evaluation — measure, don’t guess** (RAG triad via LLM-as-judge). | 🎥 Lecture Video; document + slides; rag pipeline + **03_rag_evaluation** | 🎯 **Capstone M2**: core build | — *(capstone milestone)* |
| 12 | Nov 9 | AI-Assisted Software Development (Claude Code) | Claude Code & agentic coding; prompting for code; reviewing/testing/securing AI-generated code; build a tested feature in a starter repo. | 🎥 Lecture Video; document + slides; ai_assisted_coding + starter_repo (pytest) | **Nov 9 Holiday → Veterans’ Day** | **A9** (6) |
| 13 | Nov 16 | GenAI Agents & MCP | Agents; tool/function calling; MCP; Flask serving. **Agent safety** (prompt injection, guardrails) **& evaluation**. | 🎥 Lecture Video; document + slides; agents + **03_agent_safety_and_eval** | 🎯 **"My Assistant" v3** (tool + guardrail) | **A10** (6) |
| 14 | Nov 23 | No Class or New Content | Thanksgiving recess. Work on the Capstone; instructor available via Canvas Inbox. | 🎥 Lecture Video (Final Project guidance); Final-Project-Capstone guide | **Thanksgiving recess Nov 23–28** · 🎯 **Capstone M3**: evaluation harness | — *(capstone milestone)* |
| 15 | Nov 30 | Multi-modal LLMs & Generative Media | Multimodal APIs (text + image + audio) with Claude & Gemini; overview of image generation (diffusion). | 🎥 Lecture Video; document + slides; multimodal notebooks | 🎯 **"My Assistant" v4** (optional: media) | — |
| 16 | Dec 7 | Fine-Tuning, GenAI Ops & Deployment | Prompt vs RAG vs fine-tune; PEFT/LoRA; GPUs; deploying & serving LLM pipelines (GenAI Ops). | 🎥 Lecture Video; document + slides; LoRA demo + serving notebooks | 🎯 **Capstone M4**: hardening (guardrails + cost) | — *(capstone milestone)* |
| 17 | Dec 14 | LLM & GenAI Evaluation, Safety & Final Presentations | Evaluating LLM systems (LLM-as-judge, eval harness); GenAI safety & limits. Final presentations. | 🎥 Lecture Video; document + slides; eval harness notebook | **Semester ends Dec 19** · 🎯 **Capstone M5**: ship it — **Final Project due Dec 19, 11:59 PM PST (20 pts)** | — *(capstone)* |

---

### Assignments (A1–A10 · 6 points each · 60 points total)
| Assignment | Week | Topic |
|---|---|---|
| **A1** | 1 | Environment setup + first AI API calls (Claude / Gemini / Ollama) |
| **A2** | 2 | NumPy data processing |
| **A3** | 3 | Pandas + Matplotlib visualization |
| **A4** | 4 | scikit-learn ML workflow |
| **A5** | 5 | Regression & classification with metrics |
| **A6** | 6 | Train & evaluate a small neural network |
| **A7** | 8 | Tokenization (BPE) + attention from scratch |
| **A8** | 10 | Embeddings + semantic search + a simple LLM app |
| **A9** | 12 | Build a tested feature using Claude Code (AI-assisted) |
| **A10** | 13 | A tool-using agent with a safety guardrail |

*All assignments due **Sunday 11:59 PM PST** of their week. Assignment specifications are released in Canvas each week.*

### 🎯 Capstone thread — "My Assistant" (build it across the term · 20 points)
One project, upgraded weekly, not crammed at the end. Full spec, tracks & rubric: **Final-Project-Capstone.md**.
- **Versions:** v1 role/system-prompt chatbot (Wk 9) → v2 RAG over your docs (Wk 11) → v3 tool-using agent + guardrail (Wk 13) → v4 multimodal (Wk 15, optional)
- **Milestones:** **M1** proposal+prototype (Wk 9) · **M2** core build (Wk 11) · **M3** eval harness (Wk 14) · **M4** hardening (Wk 16) · **M5** ship it + present (Wk 17, due Dec 19)

### Grade summary
| Component | Points |
|---|---:|
| Assignments A1–A10 (6 pts each) | 60 |
| Midterm Exam (Oct 11) | 20 |
| Capstone Final Project (Dec 19) | 20 |
| **Total** | **100** |

*Schedule is subject to change; any updates will be announced in Canvas.*
