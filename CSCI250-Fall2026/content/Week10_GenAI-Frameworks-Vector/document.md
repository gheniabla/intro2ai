# Week 10 — GenAI Frameworks & Vector Storage
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of October 26, 2026 · Online / Asynchronous*

---

## Learning objectives
By the end of this week you will be able to:
1. Explain why **keyword search fails** for meaning-based questions, and why we need embeddings.
2. Turn text into **embeddings** with Hugging Face `sentence-transformers` (no OpenAI, no key), compute **cosine similarity by hand**, and write **top-k semantic search from scratch**.
3. Explain what a **vector store (ChromaDB)** adds on top of that hand-built search, and query one.
4. Explain what **GenAI frameworks** (LangChain, LlamaIndex) give you on top of a raw model API.
5. Use the core LangChain building blocks: **models**, **prompt templates**, **output parsers**, and **chains** (LCEL); load and split documents with **loaders** and **text splitters**.
6. Connect the pieces into a tiny "ask-your-docs" prototype that previews next week's full **RAG** pipeline.

> **Time budget:** ~10 hours this week (lecture + slides + three notebooks + **Assignment A8**). This week's graded work is **Assignment A8** — embeddings + semantic search + a simple LLM app (see `assignments/A8.md`). Final Project ideas are also posted in the sidebar.

> **Order matters this week.** We build the **embeddings idea from scratch first** (Section 1) so the vector database in Section 2 — and LangChain after it — is never a black box. Start with `code/00_embeddings_intuition.ipynb`.

---

## 1. Embeddings from scratch — build the idea before the database
The most important idea this week is **semantic search**: finding text by *meaning*, not by matching letters. Before reaching for any library, build it yourself in `code/00_embeddings_intuition.ipynb`.

### 1.1 First, watch the dumb baseline fail
Plain **keyword / substring search** matches characters. Ask it for *"a young feline resting"* over a corpus that contains *"The cat napped on the warm windowsill"* and it returns **nothing** — none of those query words literally appear, even though a human sees the match instantly.
```python
def keyword_search(query, corpus):
    q = set(query.lower().split())
    return [i for i, s in enumerate(corpus) if q & set(s.lower().replace('.', '').split())]

keyword_search("a young feline resting", corpus)   # -> [] : misses the cat sentences
```
That failure is *why* embeddings exist.

### 1.2 Embeddings = meaning as a vector
An **embedding** turns each sentence into a fixed-length list of numbers (here 384) that captures meaning. Similar meaning → similar vectors. We use a small, free, **local** Hugging Face model (no key, no OpenAI):
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")   # 384-dim, free, local
embeddings = model.encode(corpus)                 # shape: (n_sentences, 384)
```

### 1.3 Cosine similarity, by hand
We measure closeness with **cosine similarity** — the cosine of the angle between two vectors, from -1 (opposite) to 1 (identical direction):
```python
import numpy as np
def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
```
Compute it for **every pair** and you get a similarity matrix you can draw as a **heatmap**; bright blocks reveal the themes (pets, weather, finance, code) the model found with no labels.

### 1.4 Top-k semantic search, from scratch
The entire trick behind a vector database is just this:
```python
def semantic_search(query, corpus, embeddings, k=3):
    q = model.encode([query])[0]
    scores = [cosine(q, e) for e in embeddings]            # compare to every vector
    return sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:k]
```
Run it on *"a young feline resting"* and it returns the cat sentences keyword search missed. **You just built semantic search.**

---

## 2. Vector stores with ChromaDB — the scaled version of what you built
A **vector store** (vector database) does exactly what your `semantic_search` did — store vectors, cosine-compare a query, sort, return top-k — but fast over millions of items, with persistence and metadata. The mental model is unchanged: `col.query(...)` *is* your hand-written top-k search with an index underneath.

```python
import chromadb
client = chromadb.Client()                       # in-memory; use PersistentClient to save to disk
collection = client.create_collection("notes")
collection.add(
    documents=["LangChain chains LLM steps.", "ChromaDB stores embeddings.",
               "Embeddings capture meaning as vectors."],
    ids=["d1", "d2", "d3"],
)
res = collection.query(query_texts=["What database holds vectors?"], n_results=2)
print(res["documents"])
```
By default Chroma embeds your text with a built-in sentence-transformers model, so this works with **no API key**. You can also pass your own embeddings.

> **Distance vs similarity:** Chroma returns a **distance** (smaller = closer); your hand-built `cosine` was a **similarity** (larger = closer). Same ordering, flipped scale.

### 2.1 Persisting to disk
```python
client = chromadb.PersistentClient(path="./chroma_db")   # survives restarts
```

### 2.2 LangChain's Chroma wrapper
LangChain provides a `Chroma` vector store that plugs straight into chains:
```python
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
store = Chroma.from_documents(chunks, embedding=emb)
hits = store.similarity_search("How does chunking work?", k=3)
```

Notebook `code/02_embeddings_chromadb.ipynb` drills into ChromaDB in depth.

---

## 3. Why frameworks? From raw API calls to building blocks
In Weeks 8–9 you called Claude and Gemini directly and hand-wrote prompts. That works, but real GenAI apps repeat the same plumbing over and over:

- format a **prompt** from variables,
- call a **model**,
- **parse** the reply into something usable,
- pull in **external data** (files, web, databases),
- store and search that data by **meaning**.

**GenAI frameworks** package this plumbing so you compose apps from reusable parts instead of rewriting glue code.

| Framework | Best at | One-line mental model |
|---|---|---|
| **LangChain** | Chaining steps, swapping models, tool/agent orchestration | "Lego bricks for LLM pipelines" |
| **LlamaIndex** | Ingesting + indexing your documents for retrieval/Q&A | "A librarian that indexes your docs for the LLM" |

They overlap a lot and interoperate. This course leans on LangChain for general chains and LlamaIndex for document indexing; both are optional conveniences — you can always drop down to the raw SDK.

> **Stack note:** We use **Claude** and **Gemini** for generation and **Hugging Face sentence-transformers** for embeddings. We do **not** use OpenAI anywhere.

---

## 4. LangChain building blocks

### 4.1 Models (chat models)
LangChain wraps each provider behind a common interface so you can swap them.
```python
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

claude = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=300)
gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

print(claude.invoke("Say hello in one sentence.").content)
```

### 4.2 Prompt templates
A **prompt template** is a reusable, parameterized prompt.
```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise tutor for a CS course."),
    ("human", "Explain {topic} to a {level} student in 2 sentences."),
])
messages = prompt.invoke({"topic": "embeddings", "level": "beginner"})
```

### 4.3 Output parsers
Parsers turn the model's reply object into a plain string (or JSON, lists, etc.).
```python
from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()
```

### 4.4 Chains (LCEL — the `|` pipe)
LangChain Expression Language wires components together with the `|` operator. Data flows left to right.
```python
chain = prompt | claude | parser
answer = chain.invoke({"topic": "vector stores", "level": "beginner"})
print(answer)
```
Swap `claude` for `gemini` and the rest of the chain is unchanged — that is the payoff of the common interface.

---

## 5. Document loaders & text splitters
Before an LLM can answer questions about *your* files, you must (1) **load** them into text and (2) **split** them into chunks small enough to embed and retrieve.

```python
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

docs = TextLoader("notes.txt").load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(len(chunks), "chunks")
```
- **chunk_size** — roughly how many characters per chunk.
- **chunk_overlap** — repeat a little text between chunks so ideas spanning a boundary aren't lost.

We go deeper on chunking strategy in Week 11 (RAG).

> **Why not OpenAI embeddings?** Course policy: no OpenAI. `all-MiniLM-L6-v2` is a strong, free default. For higher quality you could use Gemini's `text-embedding-004` via `GoogleGenerativeAIEmbeddings`.

---

## 6. LlamaIndex — the document-indexing alternative
LlamaIndex specializes in ingesting documents and answering questions over them with very little code.
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("docs").load_data()   # reads a whole folder
index = VectorStoreIndex.from_documents(documents)       # embeds + indexes
query_engine = index.as_query_engine()
print(query_engine.query("What is in these documents?"))
```
LlamaIndex hides the loader → splitter → embed → store steps behind `VectorStoreIndex`. Under the hood it does exactly what Sections 1–2 and 5 spelled out.

---

## 7. Putting it together — a tiny "ask-your-docs" preview
With embeddings + a vector store + a chat model you already have the skeleton of **RAG**:
1. **Retrieve** the most relevant chunks for a question (vector search).
2. **Stuff** them into a prompt as context.
3. **Generate** an answer grounded in that context (Claude or Gemini).

```python
question = "What does ChromaDB do?"
hits = store.similarity_search(question, k=3)
context = "\n".join(d.page_content for d in hits)
prompt = f"Answer using ONLY this context:\n{context}\n\nQuestion: {question}"
print(claude.invoke(prompt).content)
```
Next week (Week 11) we build this out into a real, citation-aware RAG pipeline.

---

## Sidebar — Final Project ideas (posted this week)
Your **Final Project** (due Dec 19) is an applied GenAI app. Start thinking now. Strong ideas from this part of the course:
- **Ask-your-notes / docs chatbot** — RAG over your own PDFs or course notes (builds directly on Weeks 10–11).
- **Study-guide generator** — retrieve from a textbook chapter and produce quizzes with citations.
- **Codebase Q&A** — index a small repo and answer "where is X?" questions.
- **Policy / FAQ assistant** — ground answers in a club, syllabus, or product FAQ and cite sources.
- **Multimodal helper** (preview of Week 15) — describe images plus answer text questions.

Pick something you'd actually use. Your project proposal is **Capstone Milestone M1** (Week 9); the Capstone then grows across milestones M2–M5. This week is for brainstorming and building the retrieval skeleton in A8. Bring an idea to office hours.

---

## 8. Reading & videos
- LangChain docs — *Introduction* and *LCEL* quickstart (linked in Canvas).
- LlamaIndex docs — *Starter Tutorial* (linked in Canvas).
- Chroma docs — *Getting Started* (linked in Canvas).
- Sentence-Transformers docs — *Computing Embeddings* (linked in Canvas).
- Video: "What are embeddings?" (linked in Canvas).

---

## 9. Lab — Assignment A8 (due Sunday 11:59 PM PT)
This week's graded work is **Assignment A8 — Embeddings + Semantic Search + a Simple LLM App** (see `assignments/A8.md`). It builds **semantic search from scratch** — embeddings, cosine similarity by hand, top-k retrieval — and wires it into a tiny "ask-your-docs" LLM app, the retrieval skeleton your Capstone RAG assistant grows from. Work through the notebooks in order:
1. Run `code/00_embeddings_intuition.ipynb` **first** — keyword search fails, then you build embeddings + cosine similarity + top-k semantic search from scratch, and see ChromaDB as the scaled-up version.
2. Run `code/01_langchain_llamaindex.ipynb` — chains with Claude & Gemini, plus a LlamaIndex index.
3. Run `code/02_embeddings_chromadb.ipynb` — embeddings + a ChromaDB vector store you query in depth.
4. Complete the A8 deliverable (semantic search + simple LLM app) per `assignments/A8.md`, and skim the **Final Project ideas** sidebar.

*Submit A8 per the spec; Week 11 also assumes you have run these notebooks.*

---

## Key terms
**framework**, **LangChain**, **LlamaIndex**, **chain (LCEL)**, **prompt template**, **output parser**, **document loader**, **text splitter / chunk**, **embedding**, **vector**, **cosine similarity**, **vector store**, **ChromaDB**, **similarity search**, **index**.
