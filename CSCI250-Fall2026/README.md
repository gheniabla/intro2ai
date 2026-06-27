# CSCI 250 — Introduction to Artificial Intelligence · Fall 2026
**Palomar College · CSIT Department · Instructor: Gheni Abla**

Complete course package: syllabus, 17-week schedule, and per-week content (lecture document, PowerPoint slides, and runnable sample code).

## Top-level files
| File | What |
|---|---|
| `Syllabus.md` / `CSCI250-Fall2026-Syllabus.docx` | Course syllabus (drop-in `.docx` for Canvas) |
| `Schedule.md` / `CSCI250-Fall2026-Schedule.docx` | Weekly class schedule (table) + capstone milestones |
| `Start-Here.md` | Student onboarding (read first): how the course works |
| `Free-Tier-Playbook.md` | Get free keys, run everything at $0, keep keys safe |
| `Final-Project-Capstone.md` | "My Assistant" capstone: tracks, milestones, rubric |
| `Rubrics.md` | Analytic rubrics + exemplars for every graded item |
| `assignments/` | Student assignment specs **A1–A10** (6 pts each, due Sundays 11:59 PM PST) |
| `capstone/` | Capstone milestone handouts **M1–M5** (the staged path to the 20-pt final project) |
| `content/` | Per-week materials (Weeks 1–17) |
| `tools/` | `slidegen.py` (deck theme) · `nbgen.py` (notebooks) · `eval_utils.py` (LLM-as-judge) |
| `course-design/` | Design notes + sources (rationale for the course design) |

## Quality design (benchmarked against top courses)
This course was benchmarked against Stanford CS224N/CS336/CS25, Karpathy's Zero-to-Hero, DeepLearning.AI, Hugging Face, Berkeley LLM-Agents, fast.ai, plus Quality Matters / RSI / UDL research. Highlights baked in: signature from-scratch labs (BPE tokenizer, attention, embeddings), **evaluation as a throughline** (LLM-as-judge), a **single capstone upgraded all term** ("My Assistant"), "wow-in-5-minutes" notebooks with cost banners, rubrics + exemplars, and an RSI engagement cadence. Full rationale + citations: `course-design/Design-Notes-and-Sources.md`.

## Weekly content layout
Each `content/WeekNN_*/` folder contains:
- **`document.md`** — lecture notes
- **`slides.pptx`** — slide deck (Week 14 is document-only)
- **`code/*.ipynb`** — Colab-runnable sample code
- **`build_slides.py`, `build_code.py`** — regenerate the deck/notebooks

## Week map
| Wk | Topic |
|---|---|
| 1 | Python Review & AI Dev Environment |
| 2 | Python Data Processing & Analytics (NumPy) |
| 3 | Python Data Visualization (Pandas/Matplotlib) |
| 4 | Introduction to AI & ML (scikit-learn) |
| 5 | Regression & Classification (Supervised) |
| 6 | Neural Networks & Deep Learning Foundations |
| 7 | ML Review & **Midterm** (Oct 11) |
| 8 | LLM Concepts, Frameworks & Tools |
| 9 | Prompt Engineering |
| 10 | GenAI Frameworks (LangChain/LlamaIndex) & Vector Storage |
| 11 | Retrieval-Augmented Generation (RAG) |
| 12 | AI-Assisted Software Development (Claude Code) |
| 13 | GenAI Agents & MCP |
| 14 | Thanksgiving recess — Final Project Prep (doc only) |
| 15 | Multi-modal LLMs & Generative Media |
| 16 | Fine-Tuning, GenAI Ops & Deployment |
| 17 | LLM & GenAI Evaluation, Safety & **Finals** (due Dec 19) |

## Tech stack (no OpenAI)
Anthropic **Claude** + **Claude Code**, Google **Gemini / AI Studio**, and open-source/local via **Hugging Face** + **Ollama**. Notebooks run in **Google Colab**, load keys via Colab Secrets / environment variables (never hard-coded), and degrade gracefully when a key or package is absent.

## Regenerating artifacts
```bash
# one week
cd content/Week01_Python-Review && python build_slides.py && python build_code.py

# all weeks
for d in content/Week*/; do
  [ -f "$d/build_slides.py" ] && (cd "$d" && python build_slides.py)
  [ -f "$d/build_code.py" ]   && (cd "$d" && python build_code.py)
done
```
Requires: `python-pptx` (slides). Notebook generation has no dependencies. To export documents to `.docx`/PDF: `pandoc document.md -o document.docx`.

## Building conventions
See `content/CONVENTIONS.md` for the authoring rules every week follows (used when generating this package and for adding/editing weeks).

## Source reference
`.canvas_export/` holds the unzipped Fall 2025 Canvas export (prior notebooks/slides) kept as a reference for future edits. Safe to delete if not needed.
