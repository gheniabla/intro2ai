# Design Notes & Sources — what we upgraded and why

The Fall 2026 redesign was benchmarked against the most respected and most-loved courses in this space, plus evidence on what earns high online-course ratings. This page records **what changed, why, and the source**, so the design is defensible (e.g., for curriculum review or accreditation).

## Benchmark courses
**University:** Stanford CS224N, CS336 (LM from scratch), CS25 (Transformers); Princeton COS597R/G; UC Berkeley LLM-Agents (Dawn Song); CMU 11-711 Advanced NLP; UW CSE 447/517; UWaterloo CS886; MIT 6.S191.
**Practitioner:** Karpathy "Neural Networks: Zero to Hero" / minbpe / nanoGPT / nanochat; DeepLearning.AI short courses; Hugging Face LLM & Agents courses; fast.ai; Anthropic Academy / cookbooks; Google Gemini cookbook / Kaggle 5-Day GenAI.
**Ratings/pedagogy:** Quality Matters Higher-Ed Rubric; SUNY OSCQR & federal RSI; UDL guidance; community-college retention research; RateMyProfessors rating-dimension docs; grade-satisfaction & rubric/specs-grading research.

## Content upgrades (closing gaps top courses teach)
| Change | Why / source | Where |
|---|---|---|
| **Build a BPE tokenizer from scratch** | CS336's & Karpathy minbpe's signature "aha"; demystifies tokens & cost; pure-Python, no GPU | Week 8 `03_build_bpe_tokenizer.ipynb` |
| **Attention from scratch (NumPy + heatmap)** | Every top course teaches attention; we make it concrete but guided (not a full transformer) — right altitude for 2nd-year | Week 8 `04_attention_from_scratch.ipynb` |
| **Embeddings + cosine-similarity semantic search *before* the vector DB** | Full Stack Bootcamp / CS224N; fixes the "black-box jump into RAG"; dumbest-baseline-first (keyword search fails → embeddings win) | Week 10 `00_embeddings_intuition.ipynb` |
| **Evaluation as a throughline (LLM-as-judge)** | The clearest gap vs. CS224N/CMU/Full-Stack; eval recurs in Wk 9/11/13/16/17, not just at the end | `tools/eval_utils.py`; Week 11 `03_rag_evaluation.ipynb`; Week 13 eval |
| **Chain-of-thought / reasoning** | Now central in CS224N/Princeton/Berkeley; pure prompting, zero cost | Week 9 `03_reasoning_and_cot.ipynb` |
| **Agent safety & prompt injection** | Berkeley LLM-Agents throughline; connects Wk 13 → Wk 17 | Week 13 `03_agent_safety_and_eval.ipynb` |
| **RAG evaluation (triad)** | DeepLearning.AI "Building & Evaluating Advanced RAG" | Week 11 |

*Deliberately skipped as grad-only* (taught as named concepts at most): custom CUDA/FlashAttention kernels, distributed training, scaling-law fitting, web-scale data pipelines.

## Pedagogy upgrades (what makes courses beloved)
| Pattern | Source | Applied |
|---|---|---|
| **"Wow in 5 minutes"** — visible result in cell 1 | HF `pipeline()`, fast.ai L1 | Notebook banner + first-cell result convention |
| **Pre-filled runnable code, blank only at checkpoints** | DeepLearning.AI | Notebooks run as-shipped; fill-ins reserved for graded self-checks |
| **One project upgraded all term ("My Assistant")** | Karpathy `makemore` | Capstone thread v1→v4, Weeks 8–17 |
| **Dumbest-baseline-first** | Karpathy bigram before NN | Keyword search before embeddings; prompting before fine-tuning |
| **Build-by-hand, then the framework** | DeepLearning.AI LangGraph; Karpathy | Attention/embeddings/agent loop by hand before LangChain/MCP |
| **Compare-models exercises** | Our 4-tool stack | Same prompt → Claude vs Gemini vs Ollama, repeatedly |
| **Cost banner + cheapest-model default** | Anthropic (Haiku default), nanochat "$100" | Banner on every LLM-week notebook; `Free-Tier-Playbook.md` |

## Ratings/quality upgrades
| Change | Source | Artifact |
|---|---|---|
| Identical **weekly module template** | QM consistency; async-friction research | `instructor.md` §D |
| **Rubrics + exemplars** on every item; revise-once | QM; specs-grading; grade-satisfaction research | `Rubrics.md` |
| **RSI cadence** (weekly announcement + video, feedback SLA, proactive outreach, pulse survey) | SUNY OSCQR / federal RSI; retention research | `instructor.md` §C |
| **Start-Here** onboarding + **Free-Tier Playbook** | reduce async friction; equity/access | `Start-Here.md`, `Free-Tier-Playbook.md` |
| **Accessibility/UDL** quick wins | UDL guidance | checklist in every design doc |
| **Capstone with tracks + milestones + low pass / high ceiling** | HF tiered certs; fast.ai ship-it; Karpathy report card | `Final-Project-Capstone.md` |

## Key source URLs
Stanford CS224N https://web.stanford.edu/class/cs224n/ · CS336 https://cs336.stanford.edu/ · CS25 https://web.stanford.edu/class/cs25/ · Princeton COS597R https://princeton-cos597r.github.io/ · Berkeley LLM Agents https://llmagents-learning.org/f24 · CMU 11-711 https://cmu-l3.github.io/anlp-spring2025/ · MIT 6.S191 https://introtodeeplearning.com/ · Karpathy https://karpathy.ai/zero-to-hero.html , https://github.com/karpathy/minbpe , https://github.com/karpathy/nanochat · DeepLearning.AI https://www.deeplearning.ai/courses · HF LLM Course https://huggingface.co/learn/llm-course · HF Agents https://huggingface.co/learn/agents-course · fast.ai https://course.fast.ai/ · Anthropic prompt tutorial https://github.com/anthropics/prompt-eng-interactive-tutorial · Anthropic cookbooks https://github.com/anthropics/claude-cookbooks · Gemini cookbook https://github.com/google-gemini/cookbook · Kaggle 5-Day GenAI https://www.kaggle.com/learn-guide/5-day-genai · Quality Matters https://www.qualitymatters.org/qa-resources/rubric-standards/higher-ed-rubric · SUNY RSI https://oscqr.suny.edu/rsi/ · Full Stack LLM Bootcamp https://fullstackdeeplearning.com/llm-bootcamp/
