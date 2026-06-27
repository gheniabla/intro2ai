# Week 8 — LLM Concepts, Frameworks & Tools
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of October 12, 2026 · Online / Asynchronous*

---

## Learning objectives
By the end of this week you will be able to:
1. Explain what a **Large Language Model (LLM)** is and how next-token prediction produces fluent text.
2. Describe **tokens** and **tokenization**, and estimate the token cost of a prompt.
3. Explain the **context window** and why it limits what a model can "remember."
4. Control model output with **sampling** parameters — **temperature**, **top-p**, and `max_tokens`.
5. Use **in-context learning** (zero-shot and few-shot) to steer a model without retraining.
6. Recognize LLM **capabilities and failure modes**, especially **hallucination**, and how to mitigate them.
7. Call **Anthropic Claude** and **Google Gemini**, and run a **local** open model with **Ollama / Hugging Face**, then compare them.

> **Time budget:** ~10 hours this week (lecture + slides + videos + two notebooks + Assignment A7).

This week begins the **LLM block** of the course. Everything from here — prompt engineering (Week 9), RAG (Week 11), agents (Week 13) — builds on the mental model you form now.

> ### 🧭 How to approach this week (read first)
> This is **the most challenging week of the course**, and it lands right after the midterm — that is expected, so pace yourself.
> - The two from-scratch labs (**BPE tokenizer**, **attention in NumPy**) are **concepts-first**. The goal is to *understand* how a token and an attention weight come to be — **we stop at understanding.** You are **not** building a full Transformer and **not** training a real LLM. Every fill-in already ships with a working reference answer right below it.
> - **If you are short on time, prioritize running and understanding over the optional fill-ins.** Run each cell, read the output, and make sure the *idea* lands (what a merge does, what a softmax row means). You can always come back to the blanks.
> - The capstone "Start My Assistant" step this week is **deliberately tiny** — you only **pick your idea and track**. The graded proposal + prototype (Milestone M1) is not due until **Week 9**.
> - Order of attack: notebooks **1 → 2** (LLM behavior, the core ideas) first; then **3** (BPE) and **4** (attention) for the under-the-hood picture. The two from-scratch notebooks are independent — do them in either order.

> **🎯 Start My Assistant (Week 8 — pick only):** This is where your **final project begins**, but the *only* thing to do this week is **choose your idea and your track** (RAG / Tool-Using Agent / Multimodal / Fine-Tuned — see `Final-Project-Capstone.md`). **Don't build the app yet.** The graded proposal + a "wow in 5 min" prototype is **Milestone M1, due Week 9** (`capstone/M1.md`). Jot a one-line idea now; that's enough.

---

## 1. What is a Large Language Model?
An **LLM** is a neural network (a deep Transformer) trained on enormous amounts of text to do one deceptively simple thing: **predict the next token** given the tokens so far. By learning to continue text well, it absorbs grammar, facts, reasoning patterns, and style.

When you "chat" with an LLM, the model is repeatedly predicting the most plausible next token, appending it, and predicting again — an **autoregressive** loop. There is no database lookup; the answer is *generated* one token at a time from learned statistical patterns. This is the single most important idea for understanding both why LLMs are powerful and why they sometimes confidently make things up.

This builds directly on **Week 6** (neural networks): an LLM is a very large neural net with a special architecture (the Transformer) and a self-supervised training objective.

---

## 2. Tokens & tokenization
Models do not see characters or words — they see **tokens**, the integer IDs of sub-word chunks produced by a **tokenizer**.

- Common English words are usually **one token**; rare words split into several.
- A rough rule of thumb for English: **1 token ≈ 4 characters ≈ 0.75 words**, so ~100 tokens ≈ 75 words.
- Whitespace and punctuation count too.

```python
# Approximate Claude/Gemini-style token counts with a HuggingFace tokenizer
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("gpt2")   # any BPE tokenizer illustrates the idea
print(len(tok.encode("Artificial intelligence is reshaping software.")))
```

Why you care: **you pay per token**, prompts that exceed the context window are rejected or truncated, and `max_tokens` caps the *response* length. Anthropic also exposes a token-counting endpoint (`client.messages.count_tokens(...)`) for exact accounting.

---

## 3. The context window
The **context window** is the maximum number of tokens the model can attend to at once — your prompt **plus** its generated reply must fit inside it.

- Modern models have large windows (tens to hundreds of thousands of tokens; some reach 1M).
- Anything outside the window is simply not seen — the model has **no memory** between separate API calls unless *you* resend the prior conversation.
- "Chat history" in an app works because the client **replays** the whole conversation each turn.

Practical consequences: long documents may need **chunking** (Week 11 / RAG), and very long chats eventually drop or summarize older turns.

---

## 4. Sampling: temperature, top-p, and max_tokens
At each step the model produces a probability distribution over the next token. **Sampling parameters** decide how we pick from it.

- **temperature** (~0–1, sometimes up to 2): low = focused/deterministic; high = diverse/creative. Use **0** for extraction, classification, and code; **0.7–1.0** for brainstorming.
- **top-p (nucleus)**: sample only from the smallest set of tokens whose probabilities sum to *p* (e.g., 0.9).
- **max_tokens**: hard cap on the **response** length (and your bill).

```python
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=200,
    temperature=0.0,            # deterministic: same prompt → ~same answer
    messages=[{"role": "user", "content": "List 3 uses of LLMs."}],
)
```

Same prompt + `temperature=1.0` run several times gives noticeably different wordings — you will see this directly in the notebook.

---

## 5. In-context learning (zero-shot & few-shot)
LLMs can learn a task **from the prompt itself**, with no weight updates — this is **in-context learning**.

- **Zero-shot:** just describe the task. *"Classify the sentiment as positive or negative: 'The plot dragged.'"*
- **Few-shot:** include a few worked **examples** before the real input so the model infers the pattern and the **output format**.

```text
Review: "Loved every minute." -> positive
Review: "A complete waste of time." -> negative
Review: "The acting saved an otherwise dull script." ->
```

Few-shot is the cheapest way to improve reliability and lock output format — the foundation for Week 9 (Prompt Engineering).

---

## 6. Capabilities & failure modes
**Strengths:** summarizing, drafting, translating, explaining, classifying, extracting structured data, writing and refactoring code, and flexible reasoning over text.

**Failure modes to respect:**
- **Hallucination** — fluent, confident, **wrong**. The model generates plausible text, not verified fact; it will invent citations, APIs, or numbers.
- **Knowledge cutoff** — it doesn't know events after its training date unless you supply them (tools / RAG).
- **No true arithmetic or state** — it predicts text; complex math and exact counting are unreliable without tools.
- **Prompt sensitivity** — small wording changes shift answers.
- **Bias & safety** — it reflects patterns (including biases) in its training data.

**Mitigations** (developed all semester): ground answers in supplied context (**RAG**, Week 11), ask for sources, set **temperature=0** for factual tasks, give the model **tools** (Week 13), and **verify** anything important. The professional rule: *treat LLM output as a confident draft, not a source of truth.*

---

## 7. Three ways to run a model
| Source | What it is | Key? | Cost |
|---|---|---|---|
| **Anthropic Claude** | Frontier hosted LLM (`messages.create`) | Yes | Per token |
| **Google Gemini** | Hosted LLM + AI Studio | Yes | Per token / free tier |
| **Ollama / Hugging Face** | Run **open** models locally | No | Your hardware |

Local models (Llama, Mistral, Gemma, Phi via **Ollama** or HF `transformers`) trade some quality for **privacy, no per-call cost, and offline use** — a real engineering tradeoff you should be able to reason about.

```python
import anthropic
client = anthropic.Anthropic()                 # reads ANTHROPIC_API_KEY
msg = client.messages.create(
    model="claude-sonnet-4-6", max_tokens=200,
    messages=[{"role": "user", "content": "Explain tokens in one sentence."}],
)
print(msg.content[0].text)
```

See `code/01_llm_concepts.ipynb` (tokens, context, sampling, in-context learning, hallucination demos) and `code/02_claude_gemini_local.ipynb` (call Claude + Gemini + a local model and compare).

---

## 8. Tokens, hands-on: build a BPE tokenizer
You have used tokens at arm's length — counting them, paying for them. Now you build the **actual algorithm** that produces them: **Byte-Pair Encoding (BPE)**, the same family used by GPT-2, Llama, and most modern models. Doing it from scratch (Karpathy's *minbpe* / Stanford CS336 style) is the fastest way to truly *get* what a token is.

The algorithm is short:
1. Start with raw **bytes** (vocabulary of 256).
2. **Count every adjacent pair** of tokens in your text.
3. **Merge the most frequent pair** into a single new token and record the rule.
4. Repeat until you reach a **target vocab size**.

```python
def merge(ids, pair, new_id):           # replace every (a,b) with new_id
    a, b = pair; out = []; i = 0
    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == a and ids[i+1] == b:
            out.append(new_id); i += 2
        else:
            out.append(ids[i]); i += 1
    return out
```

To **encode**, you replay the learned merges; to **decode**, each token id maps back to its bytes and you concatenate — an **exact round-trip**. This makes two ideas concrete:

- **Vocab size vs sequence length tradeoff** — more merges shrink your sequences (fewer tokens to process and pay for) at the cost of a bigger vocabulary. Every model maker tunes this dial.
- **Why models can't count letters in "strawberry"** — a big-vocab tokenizer may pack the whole word into **one opaque token**, so the model never sees the individual `r`s. Tokens are also exactly what you're **billed** for. This is the under-the-hood reason behind a famous LLM failure.

The notebook (`code/03_build_bpe_tokenizer.ipynb`) has you fill in `merge`, `encode`, and `decode` with `assert` self-checks, run a round-trip on **your own text**, then compare against a **real Hugging Face** BPE tokenizer.

> **Scope cap (honest bound):** our `encode` applies the learned merges once in order, which is plenty to *see the idea*; production BPE re-scans the sequence and keeps applying the highest-priority merge until **no merge rule applies anymore**. Same algorithm, just run to completion — out of scope here.

---

## 9. Attention: the idea behind Transformers
Section 1 said an LLM is "a deep Transformer." The single operation that makes a Transformer work is **attention** — specifically **scaled dot-product attention**. It lets every word look at every other word and pull in the context it needs. Building it once in NumPy demystifies the whole architecture.

For a sentence, turn each word's embedding into three vectors — **Q** (query), **K** (key), **V** (value) — via learned weight matrices, then:

```python
scores  = (Q @ K.T) / np.sqrt(d)        # how well each query matches each key
weights = softmax_rows(scores)          # each row -> probabilities summing to 1
output  = weights @ V                    # context-aware mix of value vectors
```

- **scores = Q·Kᵀ/√d** measures how strongly each word should attend to each other word; the **√d** keeps values stable as dimension grows.
- **softmax** turns each row into attention **weights** that sum to 1.
- The **weighted sum of V** is each word's new, context-aware representation — this is where information flows between words.

Plotting `weights` as a **heatmap** shows exactly which words attend to which — the same picture researchers use to interpret models. **Multi-head** attention simply runs this several times in parallel, each head with its own Q/K/V, so different heads can capture different relationships (grammar, long-range references). Stack many such layers and you have a Transformer.

The notebook (`code/04_attention_from_scratch.ipynb`) has you fill in the scores, softmax, and weighted-sum steps with `assert` checks, draw the attention heatmap, and run it on **your own** toy sentence.

> **Scope cap (honest bound):** this is an **encoder-style** demo where every word can attend to every other word. Real **decoder-only** LLMs (the ones that generate text) add a **causal mask** so a token can only attend to tokens *before* it — one extra step we leave out to keep the core idea clear.

---

## 10. Reading & videos
- **Compact Guide to Large Language Models** (Canvas) — read the tokens, context-window, and sampling sections.
- Karpathy, *Let's build the GPT Tokenizer* (minbpe) and *Let's build GPT* — the from-scratch inspiration for notebooks 3 & 4 (linked in Canvas).
- *Attention Is All You Need* (Vaswani et al., 2017) — the original Transformer paper; skim sections 3.2 (scaled dot-product + multi-head attention).
- Anthropic docs: *Messages API*, *Models overview*, *Token counting* (linked in Canvas).
- Google AI Studio: *Gemini quickstart* and *generation config* docs.
- Ollama: *README / quickstart* (ollama.com).
- Video: "What is a Transformer / next-token prediction" (linked in Canvas).

---

## 11. Lab — Assignment A7 (due Sunday 11:59 PM PT)
**A7 is a short structured exercise** demonstrating you understand how LLMs work.

1. Open `code/01_llm_concepts.ipynb`. Run all cells and complete the inline tasks: tokenize three strings of your own, then run the **same prompt at temperature 0.0 and 1.0 three times each** and describe the difference.
2. Open `code/02_claude_gemini_local.ipynb`. Add your keys (Colab Secrets) and send **one shared prompt** to **Claude**, **Gemini**, and a **local** model (Ollama). Fill in the comparison table (length, tone, correctness, speed).
3. **Hallucination hunt:** craft one prompt that makes a model produce a confident but false answer (e.g., ask about a fake paper or person). Capture the output and write 2–3 sentences on *why* it happened and how you'd mitigate it.
4. **Under the hood:** open `code/03_build_bpe_tokenizer.ipynb`, complete the three fill-in cells (`merge`, `encode`, `decode`) until every `assert` passes, and run the round-trip on **your own** sentence. Then open `code/04_attention_from_scratch.ipynb`, complete the scores/softmax/weighted-sum fill-ins, and **paste the attention heatmap** you produced.
5. **Submit:** all completed notebooks (or Colab links) + the comparison table + the hallucination write-up + your attention heatmap. Include a one-line **AI Use** note.

*See the syllabus for the S-exercise rubric.*

---

## Key terms
**LLM**, **Transformer**, **next-token prediction**, **autoregressive**, **token**, **tokenizer / tokenization**, **byte-pair encoding (BPE)**, **merge rule**, **vocab size**, **context window**, **sampling**, **temperature**, **top-p / nucleus sampling**, **max_tokens**, **in-context learning**, **zero-shot**, **few-shot**, **hallucination**, **knowledge cutoff**, **local model**, **Ollama**, **attention**, **scaled dot-product attention**, **query / key / value (Q/K/V)**, **softmax**, **multi-head attention**.
