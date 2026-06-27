# Week 11 — Retrieval-Augmented Generation (RAG)
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of November 2, 2026 · Online / Asynchronous*

> **🎯 Capstone checkpoint —** "My Assistant" v2: **answer from your own documents** (RAG). Chunk, embed, and retrieve over a corpus you choose, then ground the answer in what you retrieved (see `capstone/M2.md`).

---

## Learning objectives
By the end of this week you will be able to:
1. Explain **why RAG exists** — what problem it solves that a bare LLM cannot.
2. Describe the full RAG pipeline: **load → chunk → embed → store → retrieve → ground → generate → cite**.
3. Choose sensible **chunking** parameters and explain the size/overlap trade-off.
4. Retrieve relevant context from a **ChromaDB** vector store using embeddings.
5. **Ground** a prompt in retrieved context and generate an answer with **Claude** *and* **Gemini**.
6. **Cite sources** so users can verify the answer, and recognize when "I don't know" is the right output.
7. **Evaluate** a RAG system with the **RAG triad** (Context Relevance, Groundedness, Answer Relevance) using an **LLM-as-judge**, then change one thing and **re-measure**.

> **Time budget:** ~10 hours this week (lecture + slides + three notebooks + **Capstone Milestone M2**). There is **no standalone weekly assignment** this week — your graded work is **Capstone Milestone M2 (core build)** (see `capstone/M2.md`). The RAG pipeline you build here is the "main engine" of your assistant.

---

## 1. Why RAG?
A pretrained LLM only knows what was in its training data. It cannot see:
- your **private documents** (notes, PDFs, company wiki),
- anything that happened **after its training cutoff**, or
- facts too **niche** to have been memorized reliably.

Ask it anyway and it may **hallucinate** — produce a fluent, confident, wrong answer.

**Retrieval-Augmented Generation (RAG)** fixes this by *retrieving* relevant text from a trusted source at question time and *putting it in the prompt* as context. The model then answers from that context instead of from memory.

> **One sentence:** RAG = "open-book exam for the LLM." It looks up the relevant page, then writes the answer using that page.

**Why not just fine-tune the model on your docs?** Fine-tuning is expensive, slow to update, and bakes facts in opaquely. RAG keeps your knowledge in an external store you can edit instantly, and it lets you **cite** exactly which source produced an answer. (We compare fine-tuning vs RAG vs prompting in Week 16.)

---

## 2. The RAG pipeline at a glance
```
            ┌─────────────── INDEXING (done once, ahead of time) ───────────────┐
  documents ─► load ─► chunk ─► embed ─► vector store (ChromaDB)
            └────────────────────────────────────────────────────────────────────┘

            ┌──────────────── QUERY TIME (per question) ────────────────┐
  question ─► embed ─► retrieve top-k chunks ─► build grounded prompt
                                                       │
                                                       ▼
                                          LLM (Claude / Gemini) ─► answer + citations
            └────────────────────────────────────────────────────────────┘
```
The left half (Weeks 10) you already built. This week adds the right half: **retrieve → ground → generate → cite**.

---

## 3. Chunking — splitting documents the right way
Embeddings work best on focused passages, and LLMs have a finite **context window**, so we split documents into **chunks**.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # ~chars per chunk
    chunk_overlap=80,    # repeat text across boundaries
)
chunks = splitter.split_text(long_text)
```

**Trade-offs:**
- **Too large** → each chunk mixes many topics; retrieval returns noise; you may blow the context window.
- **Too small** → ideas get cut in half; you lose the surrounding context needed to answer.
- **Overlap** → repeating ~10–20% of text between neighbors keeps sentences that straddle a boundary intact.

A good starting point for prose: **chunk_size 300–800, overlap 10–20%**. Tune by inspecting what gets retrieved.

---

## 4. Embed & store
Each chunk is embedded into a vector (we use Hugging Face `all-MiniLM-L6-v2` — free, local, **not OpenAI**) and stored in **ChromaDB** alongside its text and **metadata** (e.g. source filename). Metadata is what makes **citations** possible later.

```python
import chromadb
client = chromadb.Client()
col = client.create_collection("kb")
col.add(
    documents=chunks,
    metadatas=[{"source": "handbook.txt", "chunk": i} for i in range(len(chunks))],
    ids=[f"c{i}" for i in range(len(chunks))],
)
```

---

## 5. Retrieve — find the relevant chunks
At query time we embed the **question** and ask the store for its nearest neighbors.

```python
res = col.query(query_texts=["How many absences are allowed?"], n_results=3)
retrieved = res["documents"][0]
sources   = res["metadatas"][0]    # carries the citation info
```
- **n_results / k** — how many chunks to pull. More context can help, but too much dilutes the signal and costs tokens. Start with **k = 3–5**.
- Optionally apply a **similarity threshold**: if nothing is close enough, return "I don't know" rather than forcing an answer.

---

## 6. Ground the prompt
We build a prompt that (a) gives the retrieved chunks as **context**, (b) instructs the model to answer **only** from that context, and (c) tells it to say so when the answer isn't there.

```python
context = "\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(retrieved))
prompt = f"""Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know based on the provided documents."
Cite the sources you used by their [number].

Context:
{context}

Question: {question}
Answer:"""
```
This **grounding instruction** is the heart of RAG. Without it the model may ignore the context and fall back on (possibly wrong) memory.

---

## 7. Generate — Claude and Gemini variants
The grounded prompt is just text, so any chat model can produce the answer. We show both.

**Claude:**
```python
import anthropic
client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=400,
    messages=[{"role": "user", "content": prompt}],
)
print(msg.content[0].text)
```

**Gemini:**
```python
import google.generativeai as genai
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")
print(model.generate_content(prompt).text)
```
Same retrieved context, two generators — compare their faithfulness and citation behavior.

---

## 8. Cite sources
Because each chunk carries `metadata["source"]`, we can append a **Sources** list so the user can verify the claim. Good RAG systems:
- show **which** documents/chunks were used,
- answer **"I don't know"** when retrieval comes back empty or weak, and
- never invent a citation that wasn't retrieved.

```python
print("\nSources:")
for i, m in enumerate(sources, 1):
    print(f"  [{i}] {m['source']} (chunk {m['chunk']})")
```

> **⚠️ Responsible AI:** RAG **reduces** hallucination but doesn't eliminate it — a model can still misread or over-extrapolate from the retrieved text, so **always show sources** and let users verify. And retrieval **amplifies whatever bias is in your corpus**: if the source documents are skewed or wrong, grounded answers will be confidently skewed or wrong too.

---

## 9. Modern RAG (2026) — beyond plain vector search
Everything above — fixed-size chunks + pure **vector (dense) search** — is the **starting point**, and it's enough for your Capstone. But it has known weak spots: dense search can miss exact keywords (names, error codes, IDs), and the top-k by cosine similarity isn't always the *best* k. The 2026 baseline layers four upgrades on top. They're additive — reach for each one only when the simple pipeline visibly falls short.

**1. Hybrid search (dense + keyword).** Run **dense** embedding similarity *and* a **keyword/BM25** search, then **fuse** the two ranked lists (a common recipe is *Reciprocal Rank Fusion*). Dense catches paraphrases ("how do I drop a class" ↔ "withdrawal policy"); keyword nails exact tokens dense embeddings blur (`CSCI250`, `48-hour`, a product SKU).
*When to use:* your corpus has codes, names, or jargon, and pure vector search keeps missing the obvious chunk.

**2. Reranking (cross-encoder).** Over-retrieve (say top-20), then have a small **cross-encoder** (e.g. `cross-encoder/ms-marco-MiniLM-L-6-v2`) score each *(question, chunk)* pair jointly and **reorder** them; keep the new top-3–5 for the prompt. A cross-encoder reads the question and chunk *together*, so it's far more accurate than the first-pass similarity — at the cost of running per candidate, which is why you only rerank the shortlist.
*When to use:* retrieval pulls roughly the right region but the *best* chunk isn't landing in the top-k.

**3. Contextual Retrieval (Anthropic's technique).** Before embedding, prepend a one-sentence **context blurb** to each chunk ("This chunk is from the Grading section of the CSCI 250 handbook; it explains final-project weighting."). A bare chunk like "It is 30 percent." is ambiguous; the situated version embeds and matches far better. The blurbs are usually generated cheaply by an LLM (e.g. Claude Haiku) at index time and benefit from prompt caching.
*When to use:* chunks lose meaning out of context (lots of pronouns, tables, short fragments).

**4. Agentic RAG.** Instead of always retrieving once, the **model decides** *whether*, *what*, and *how many times* to search — it can reformulate the query, do **multi-step** retrieval (look something up, then look up what it just learned), or skip retrieval entirely for a question it can answer directly. This is RAG meeting the **agent loop** (tool calling) you'll build in Week 13.
*When to use:* questions need multiple lookups or sub-questions; a single retrieval can't gather everything at once. (Cost: more model calls and latency.)

> **Rule of thumb:** start simple (dense + fixed chunks), **measure** with the RAG triad below, and add hybrid → reranking → contextual → agentic **only** where the numbers say the simple pipeline is the bottleneck. Notebook `code/04_hybrid_rerank.ipynb` shows hybrid retrieval + reranking in ~40 lines.

---

## 10. Evaluate RAG — measure, don't guess
You can *feel* that an answer is good, but feelings don't scale and don't catch regressions when you tweak chunking next week. **Measure.** Notebook `code/03_rag_evaluation.ipynb` does this with the **RAG triad** and the course's shared `eval_utils.py`.

### 10.1 The RAG triad
The triad checks the **three links** in a RAG chain, each scored 1–5 by an **LLM-as-judge**:

| Metric | Question it answers | Compares |
|---|---|---|
| **Context Relevance** | Did we retrieve the *right* chunks? | question ↔ context |
| **Groundedness** | Is the answer *supported* by the context (not invented)? | answer ↔ context |
| **Answer Relevance** | Does the answer actually address the question? | answer ↔ question |

The power of the triad is that it **localizes** failure: a low score tells you *which* link broke — retrieval, faithfulness, or focus — instead of just "the answer was bad."

### 10.2 Use the shared eval helpers
Every week in this course scores outputs the same way, via `tools/eval_utils.py`:
```python
from eval_utils import llm_judge, scorecard   # judge with Gemini or Claude; print a report card

rubric = 'Rate 1-5 how RELEVANT the answer is to the question. Return ONLY JSON: {"score": <int>, "reason": "<short>"}.'
result = llm_judge(question, answer, rubric)   # -> {"score": 4, "reason": "...", "judge": "gemini"}
```
`llm_judge` uses **Gemini Flash** or **Claude Haiku** (the cheapest models) and **degrades to a transparent heuristic** with no key, so the notebook always runs.

### 10.3 The discipline: baseline → change one thing → re-measure
1. Pin a **fixed set of evaluation questions** (your test set) so runs are comparable.
2. Score a **baseline** config and print a `scorecard` (average triad score).
3. Change **one** thing (e.g. `chunk_size` 120 → 300).
4. **Re-measure** on the *same* questions and compare the averages. Higher triad wins; ties go to the simpler/cheaper config.

```python
rows = [{'q': q, **rag_triad(rag(q))} for q in EVAL_QUESTIONS]
scorecard(rows)   # per-question scores + an average you can track over time
```
This is how you improve a RAG system **without fooling yourself**.

### 10.4 Quick debugging order (when a score is low)
1. **Low Context Relevance** → the right chunk wasn't retrieved. Print the retrieved text; fix `chunk_size`/`overlap` or `k` — *not* the prompt.
2. **Low Groundedness** → the model is inventing facts. Strengthen the grounding instruction; lower temperature.
3. **Low Answer Relevance** → reframe the question or fix the generator.

We return to formal **LLM evaluation** (eval harnesses, safety, bias) in Week 17 — but you start measuring **now**.

---

## 11. Reading & videos
- Lewis et al., *Retrieval-Augmented Generation* (2020) — skim the abstract & figure 1 (linked in Canvas).
- LangChain docs — *RAG tutorial* (linked in Canvas).
- Anthropic docs — *Long context & grounding tips* (linked in Canvas).
- Chroma docs — *Using metadata & filters* (linked in Canvas).
- Video: "RAG explained in 10 minutes" (linked in Canvas).

---

## 12. Lab — Capstone Milestone M2 (due Sunday 11:59 PM PT)
This week's graded work is **Capstone Milestone M2 — Core Build** (see `capstone/M2.md`): "My Assistant" v2, where your assistant's **central capability works end-to-end**. The notebooks below give you the RAG backbone; use them to build (or feed) your M2 core engine:
1. Run `code/01_rag_pipeline.ipynb` — the full load → chunk → embed → store → retrieve → ground → **generate (Claude + Gemini)** → cite pipeline over a small doc set.
2. Run `code/02_rag_experiments.ipynb` — change `chunk_size`, `chunk_overlap`, and `k`; watch retrieval quality shift; try an out-of-scope question and confirm it answers "I don't know."
3. Run `code/03_rag_evaluation.ipynb` — score the RAG triad with `llm_judge`, change the chunking, and **re-measure** with a `scorecard`. Decide which config you'd ship. *(Note the offline-eval caveat in its banner: without a key the judge and generator are heuristic, so Groundedness looks inflated/flat — use a key for real numbers.)*
4. (Optional, modern) Run `code/04_hybrid_rerank.ipynb` — **hybrid retrieval** (dense + BM25, fused) and a **cross-encoder reranker**, with graceful degradation if packages are missing.
5. **Build your M2 deliverable** per `capstone/M2.md`: get your assistant's core capability running end-to-end with visible output, and keep 5–10 representative inputs for your M3 eval set.

*Submit M2 per `capstone/M2.md`. The pipeline you build here is reusable course infrastructure and the backbone of your Capstone.*

---

## Key terms
**RAG**, **hallucination**, **grounding**, **context window**, **chunk / chunking**, **chunk_overlap**, **embedding**, **vector store**, **ChromaDB**, **retrieval**, **top-k**, **metadata**, **citation / source attribution**, **faithfulness**, **"I don't know" fallback**, **RAG triad**, **context relevance**, **groundedness**, **answer relevance**, **LLM-as-judge**, **scorecard**, **baseline / re-measure**, **hybrid search**, **BM25**, **dense vs keyword retrieval**, **score fusion / reciprocal rank fusion**, **reranking**, **cross-encoder**, **Contextual Retrieval**, **agentic RAG**, **multi-step retrieval**.
