# Week 16 — Fine-Tuning, GenAI Ops & Deployment
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of December 7, 2026 · Online / Asynchronous*

---

## Learning objectives
By the end of this week you will be able to:
1. Decide **when to fine-tune vs. prompt vs. use RAG** for a given problem, and explain the trade-offs.
2. Describe **how fine-tuning works**: datasets, formatting, epochs, learning rate, and over/underfitting.
3. Explain **PEFT/LoRA** — why we rarely full-fine-tune large models anymore, and how low-rank adapters work.
4. Reason about **GPUs for LLMs**: why they are needed, how to estimate memory, and what **quantization** buys you.
5. Understand **GenAI Ops**: deploying and serving an LLM pipeline as an API service, with monitoring and cost/latency awareness.

> **Time budget:** ~10 hours this week (lecture + slides + videos + notebooks). **No graded assignment** — keep building your Final Project.

---

## 1. The big decision: prompt vs. RAG vs. fine-tune
Most "the model doesn't do what I want" problems are **not** solved by fine-tuning. Work down this ladder — cheapest and fastest first:

1. **Prompt engineering** (Week 9): better instructions, examples (few-shot), system prompts, structured output. Fixes *behavior and format*.
2. **RAG** (Week 11): inject the right *facts* at query time from a vector store. Fixes *knowledge gaps* and *freshness* without retraining.
3. **Fine-tuning**: update model weights on your data. Fixes *style/format you cannot prompt*, *domain tone*, *latency* (smaller specialized model), or *consistent structured behavior at scale*.

| Need | Best tool |
|---|---|
| "Answer in our brand voice / always output this JSON shape" | Prompt → then fine-tune if still inconsistent |
| "Answer questions about *our* documents / latest data" | **RAG** |
| "It keeps making facts up about my domain" | **RAG** (grounding), not fine-tuning |
| "I want a small, cheap, fast model that does one narrow task well" | **Fine-tune** a small open model |
| "Teach the model brand-new private knowledge" | RAG first; fine-tune only if you have lots of clean data |

**Rule of thumb:** *Prompting changes behavior, RAG changes knowledge, fine-tuning changes the model.* Try them in that order.

---

## 2. How fine-tuning works
Fine-tuning continues training a pretrained model on a smaller, task-specific **dataset** so its weights shift toward your task.

### 2.1 The dataset is the project
Quality and format matter more than quantity. For an instruction model you provide **input→output** pairs, often as chat turns:
```python
example = {
    "messages": [
        {"role": "user", "content": "Summarize: The mitochondria is the powerhouse of the cell."},
        {"role": "assistant", "content": "Mitochondria produce most of the cell's energy."},
    ]
}
```
- A few hundred *clean, consistent* examples often beat thousands of noisy ones.
- Hold out a **validation split** (e.g., 10–20%) to watch for overfitting.

### 2.2 Key training knobs
- **Epoch** — one full pass over the training set. Too few → underfit; too many → overfit (memorizes, stops generalizing).
- **Learning rate** — step size for weight updates. Too high → unstable; too low → slow / stuck.
- **Batch size** — examples processed per step (limited by GPU memory).
- **Loss** — what training minimizes; watch **training loss** *and* **validation loss**. If validation loss climbs while training loss falls, you are **overfitting**.

---

## 3. PEFT and LoRA — fine-tuning without melting your GPU
Full fine-tuning updates **all** of a model's billions of weights — expensive in memory and storage. **PEFT** (Parameter-Efficient Fine-Tuning) freezes the base model and trains only a tiny number of new parameters.

**LoRA** (Low-Rank Adaptation) is the most popular PEFT method:
- Freeze the original weight matrix **W**.
- Add a small, trainable low-rank pair **A·B** beside it (rank `r` is small, e.g. 8 or 16).
- Train only **A** and **B** — often **<1%** of the parameters.
- At the end you save just the small **adapter** (megabytes, not gigabytes); you can swap adapters per task on the same base model.

```python
from peft import LoraConfig
lora = LoraConfig(
    r=8, lora_alpha=16, lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],  # attention projections
    task_type="CAUSAL_LM",
)
```
**QLoRA** goes further: load the frozen base model in **4-bit** (quantized) and train LoRA adapters on top — this is how people fine-tune billion-parameter models on a single consumer/Colab GPU.

---

## 4. GPUs for LLMs: memory and quantization
LLMs are giant matrix multiplications. **GPUs** do thousands of these in parallel, so they are ~10–100× faster than CPUs for this work. The hard limit is usually **GPU memory (VRAM)**, not speed.

### 4.1 Estimating memory
A rough rule for just **loading** a model for inference:
- **FP16/BF16** (16-bit): ~**2 GB per billion** parameters.
- **8-bit**: ~1 GB per billion.
- **4-bit**: ~0.5 GB per billion.

So a 7B model needs ~14 GB in FP16, but only ~4–5 GB in 4-bit. **Training** needs much more (gradients + optimizer states + activations) — another reason LoRA/QLoRA win.

### 4.2 Quantization
**Quantization** stores weights in fewer bits (16 → 8 → 4), trading a small accuracy hit for big memory and speed savings. It is what makes large open models runnable on a free Colab T4 or your laptop (via Ollama, which ships quantized GGUF models).

```python
from transformers import BitsAndBytesConfig
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype="bfloat16")
```

---

## 5. GenAI Ops — deploying and serving an LLM pipeline
"GenAI Ops" (a.k.a. **LLMOps**) is everything between "my notebook works" and "users rely on it 24/7."

### 5.1 Serve it as an API
Wrap your model/RAG/agent pipeline behind a small web service (Flask/FastAPI) so apps can call it:
```python
from flask import Flask, request, jsonify
import anthropic
app = Flask(__name__)
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

@app.post("/chat")
def chat():
    user_msg = request.json["message"]
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001", max_tokens=300,
        messages=[{"role": "user", "content": user_msg}],
    )
    return jsonify({"reply": msg.content[0].text})
```
Hosted vs. self-hosted: a **hosted API** (Claude, Gemini) means no GPU to manage; a **self-hosted** open model (vLLM/Ollama/HF) gives privacy and per-token cost control but you operate the hardware.

### 5.2 What to monitor
- **Latency** — time to first token and total time; users feel slow responses.
- **Cost** — priced per **token** (input + output). Track tokens per request; cap `max_tokens`; use the *smallest model that passes eval* (e.g., Haiku/Flash for routing, Opus/Pro for hard tasks).
- **Quality / drift** — log prompts + responses; sample and re-score (Week 17's eval harness).
- **Reliability** — retries, timeouts, rate-limit handling, graceful fallback.

### 5.3 Cost & latency levers (memorize these)
- Pick the **smallest sufficient model**; route easy queries to a cheap model.
- **Cache** repeated prompts/answers; use **prompt caching** for long shared context.
- **Shorten context** (RAG retrieves only what's needed) and **cap output length**.
- **Quantize / batch** for self-hosted models.

### 5.4 Guardrails — validate the inputs and outputs
A served pipeline faces untrusted input and emits text other systems act on, so wrap the model call in **guardrails**:
- **Input validation:** length/format limits, allow-listed fields, and a **prompt-injection** check — keep *trusted instructions* (your system prompt) separate from *untrusted data* (user text, retrieved docs), and never auto-`eval`/shell model output.
- **Output validation:** verify the shape (e.g., JSON schema), reject or repair malformed/over-long responses, and scan for banned/unsafe content before returning.
- **PII handling:** don't send secrets/PII to a model you don't control; redact obvious PII (emails, phone numbers, keys) on the way in, and log redacted text only.

```python
import re
def guard_input(text: str, max_chars: int = 4000) -> str:
    if len(text) > max_chars:                       # cheap DoS / cost guard
        raise ValueError("input too long")
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[email]", text)  # redact PII
    return text

INJECTION = re.compile(r"ignore (all|previous) instructions", re.I)
def looks_injected(text: str) -> bool:
    return bool(INJECTION.search(text))             # flag, then handle as untrusted data
```
You'll wire input + output guardrails (plus the cost report from §5.2) into your Final Project pipeline for **Capstone M4**.

> **🎯 Capstone M4 — hardening (guardrails + cost report).** Add input/output **guardrails** (validation, injection defense, PII redaction) *and* a **cost/latency report** (tokens + estimated $ per request) to your "My Assistant" pipeline. This is the v4 → production-hardening step before you ship and present in **M5** (Week 17).

---

## 6. Reading & videos
- Hugging Face **PEFT** docs and the **LoRA** paper summary (linked in Canvas).
- Hugging Face **"Quantization"** and **bitsandbytes** quickstart.
- Video: "Fine-tuning vs RAG — when to use which" (linked in Canvas).
- Anthropic **prompt caching** and **token usage** docs; Gemini **pricing** page.

---

## 7. Lab / assignment
**No graded assignment this week.** Use the time to:
1. Run `code/01_lora_finetune_demo.ipynb` on a Colab **GPU** (Runtime → Change runtime type → T4 GPU). It LoRA-fine-tunes a tiny open model. It degrades gracefully (clear message) if no GPU or libraries are present.
2. Skim `code/02_serving_sketch.ipynb` to see how a pipeline becomes an API with monitoring.
3. Apply one **cost/latency lever** to your Final Project pipeline and note the result.

---

## Key terms
**fine-tuning**, **epoch**, **learning rate**, **overfitting**, **PEFT**, **LoRA**, **QLoRA**, **adapter**, **quantization**, **VRAM**, **GenAI Ops / LLMOps**, **latency**, **token cost**, **monitoring**.
</content>
</invoke>
