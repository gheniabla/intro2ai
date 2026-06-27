"""Build Week 11 sample-code notebooks. Run: python build_code.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# Shared tiny "knowledge base" used by both notebooks (built inline so the
# notebooks are self-contained and need no external files).
KB_BUILDER = (
    "COURSE_HANDBOOK = '''\n"
    "Attendance policy: This is an online asynchronous course. Modules open Monday\n"
    "and the weekly lab is due Sunday at 11:59 PM Pacific. You may miss deadlines\n"
    "twice with no penalty using the two automatic 48-hour extensions.\n\n"
    "AI-use policy: Students may use AI assistants such as Claude and Gemini on\n"
    "assignments but must understand and disclose their use with an AI Use note.\n"
    "Exams, including the midterm and final, are AI-restricted.\n\n"
    "Grading: Labs and assignments are 50 percent, the midterm is 20 percent, and\n"
    "the final project is 30 percent. The final project is due December 19.\n\n"
    "Office hours: Tuesday 5 to 6 PM and Saturday 10 to 11 AM Pacific on Zoom.\n"
    "Email the instructor with the subject prefix CSCI250 for a reply within 48 hours.\n"
    "'''\n"
)

# ---------------------------------------------------------------- notebook 1
rag_nb = [
    ("md", "## ▶ What you'll see when you run this\n"
           "- A grounded answer to *\"How is the final project weighted and when is it due?\"* "
           "with **[1]/[2] citations** pointing back to the exact handbook chunks.\n\n"
           "**Time:** ~12 min · **Cost:** free (local HF embeddings; cheapest generator: "
           "Gemini Flash / Claude Haiku) · **Keys:** none for retrieval — add "
           "`ANTHROPIC_API_KEY` or `GEMINI_API_KEY` for the generation cells."),

    ("md", "# Week 11 · Notebook 1 — A Working RAG Pipeline\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Build the full pipeline over a tiny document set:\n"
           "**load → chunk → embed → store (ChromaDB) → retrieve → ground → "
           "generate (Claude + Gemini) → cite.**\n\n"
           "> Runs in Google Colab. Embeddings are **local Hugging Face** (no OpenAI). "
           "Generation cells **degrade gracefully** if a key/package is missing."),

    ("md", "## 0. Install"),
    ("code", "!pip -q install langchain langchain-community langchain-text-splitters \\\n"
             "    chromadb sentence-transformers anthropic google-generativeai"),

    ("md", "## 1. Load API keys safely (optional — retrieval works without them)"),
    ("code", "import os\n"
             "try:\n"
             "    from google.colab import userdata\n"
             "    for k in ('ANTHROPIC_API_KEY', 'GEMINI_API_KEY'):\n"
             "        try:\n"
             "            os.environ[k] = userdata.get(k)\n"
             "        except Exception:\n"
             "            pass\n"
             "except Exception:\n"
             "    pass\n"
             "print('Anthropic key set:', bool(os.environ.get('ANTHROPIC_API_KEY')))\n"
             "print('Gemini key set:', bool(os.environ.get('GEMINI_API_KEY')))"),

    ("md", "## 2. Our document set (a course handbook)"),
    ("code", KB_BUILDER + "print(COURSE_HANDBOOK)"),

    ("md", "## 3. Chunk the document\n"
           "Split into small overlapping passages. Inspect the chunks — retrieval can only "
           "find what chunking produced."),
    ("code", "from langchain_text_splitters import RecursiveCharacterTextSplitter\n"
             "splitter = RecursiveCharacterTextSplitter(chunk_size=240, chunk_overlap=40)\n"
             "chunks = splitter.split_text(COURSE_HANDBOOK)\n"
             "print(len(chunks), 'chunks')\n"
             "for i, c in enumerate(chunks):\n"
             "    print(f'--- [{i}] ---')\n"
             "    print(c.strip())"),

    ("md", "## 4. Embed & store in ChromaDB (with metadata for citations)\n"
           "We attach a `source` and `chunk` number to every chunk — that metadata is what "
           "lets us cite later. Chroma auto-embeds with a local sentence-transformers model."),
    ("code", "import chromadb\n"
             "client = chromadb.Client()\n"
             "try:\n"
             "    client.delete_collection('handbook')\n"
             "except Exception:\n"
             "    pass\n"
             "col = client.create_collection('handbook')\n"
             "col.add(\n"
             "    documents=[c.strip() for c in chunks],\n"
             "    metadatas=[{'source': 'handbook.txt', 'chunk': i} for i in range(len(chunks))],\n"
             "    ids=[f'c{i}' for i in range(len(chunks))],\n"
             ")\n"
             "print('stored', col.count(), 'chunks')"),

    ("md", "## 5. Retrieve the most relevant chunks"),
    ("code", "def retrieve(question, k=3):\n"
             "    res = col.query(query_texts=[question], n_results=k)\n"
             "    return res['documents'][0], res['metadatas'][0]\n\n"
             "QUESTION = 'How is the final project weighted and when is it due?'\n"
             "retrieved, sources = retrieve(QUESTION, k=3)\n"
             "for d, m in zip(retrieved, sources):\n"
             "    print(f\"[{m['chunk']}] {d}\\n\")"),

    ("md", "## 6. Ground the prompt\n"
           "Tell the model to answer ONLY from the retrieved context, to say \"I don't know\" "
           "otherwise, and to cite sources by number."),
    ("code", "def build_prompt(question, retrieved):\n"
             "    context = '\\n\\n'.join(f'[{i+1}] {c}' for i, c in enumerate(retrieved))\n"
             "    return (\n"
             "        'Answer the question using ONLY the context below.\\n'\n"
             "        'If the answer is not in the context, say '\n"
             "        '\"I don\\'t know based on the provided documents.\"\\n'\n"
             "        'Cite the sources you used by their [number].\\n\\n'\n"
             "        f'Context:\\n{context}\\n\\n'\n"
             "        f'Question: {question}\\nAnswer:'\n"
             "    )\n\n"
             "prompt = build_prompt(QUESTION, retrieved)\n"
             "print(prompt)"),

    ("md", "## 7. Generate with Claude"),
    ("code", "def answer_with_claude(prompt):\n"
             "    try:\n"
             "        import anthropic\n"
             "        msg = anthropic.Anthropic().messages.create(\n"
             "            model='claude-sonnet-4-6', max_tokens=400,\n"
             "            messages=[{'role': 'user', 'content': prompt}])\n"
             "        return msg.content[0].text\n"
             "    except Exception as e:\n"
             "        return f'[Claude unavailable: {e}]'\n\n"
             "print('CLAUDE:\\n', answer_with_claude(prompt))"),

    ("md", "## 8. Generate with Gemini (same context)"),
    ("code", "def answer_with_gemini(prompt):\n"
             "    try:\n"
             "        import google.generativeai as genai\n"
             "        genai.configure(api_key=os.environ['GEMINI_API_KEY'])\n"
             "        model = genai.GenerativeModel('gemini-2.5-flash')\n"
             "        return model.generate_content(prompt).text\n"
             "    except Exception as e:\n"
             "        return f'[Gemini unavailable: {e}]'\n\n"
             "print('GEMINI:\\n', answer_with_gemini(prompt))"),

    ("md", "## 9. Cite the sources\n"
           "Because each chunk carried metadata, we can show exactly what the answer was "
           "grounded in."),
    ("code", "print('Sources:')\n"
             "for i, m in enumerate(sources, 1):\n"
             "    print(f\"  [{i}] {m['source']} (chunk {m['chunk']})\")"),

    ("md", "## 10. One function, the whole pipeline\n"
           "Wrap it up so you can ask anything. Reuse this in your Final Project."),
    ("code", "def rag(question, k=3, model='claude'):\n"
             "    retrieved, sources = retrieve(question, k=k)\n"
             "    prompt = build_prompt(question, retrieved)\n"
             "    gen = answer_with_claude if model == 'claude' else answer_with_gemini\n"
             "    answer = gen(prompt)\n"
             "    cites = '\\n'.join(f\"  [{i+1}] {m['source']} (chunk {m['chunk']})\"\n"
             "                       for i, m in enumerate(sources))\n"
             "    return f'{answer}\\n\\nSources:\\n{cites}'\n\n"
             "print(rag('What is the AI-use policy on exams?', model='claude'))"),
]
build_notebook(rag_nb, os.path.join(CODE, "01_rag_pipeline.ipynb"))

# ---------------------------------------------------------------- notebook 2
exp_nb = [
    ("md", "## ▶ What you'll see when you run this\n"
           "- The **same question** retrieved under different chunk sizes/overlap/k, plus an "
           "out-of-scope question correctly flagged **\"I don't know (out of scope)\"**.\n\n"
           "**Time:** ~10 min · **Cost:** free (local HF embeddings, retrieval-only) "
           "· **Keys:** none required."),

    ("md", "# Week 11 · Notebook 2 — RAG Experiments\n"
           "**CSCI 250 · Fall 2026**\n\n"
           "Build intuition: change **chunk_size**, **chunk_overlap**, and **k**, watch "
           "retrieval quality shift, and confirm the system says **\"I don't know\"** for "
           "out-of-scope questions. Retrieval-only — **no API key required**."),

    ("md", "## 0. Install"),
    ("code", "!pip -q install langchain-text-splitters chromadb sentence-transformers"),

    ("md", "## 1. The document set"),
    ("code", KB_BUILDER + "print('handbook length:', len(COURSE_HANDBOOK), 'chars')"),

    ("md", "## 2. A helper: index with given chunk settings, then retrieve\n"
           "We rebuild a fresh Chroma collection for each experiment so settings don't leak."),
    ("code", "import chromadb\n"
             "from langchain_text_splitters import RecursiveCharacterTextSplitter\n\n"
             "client = chromadb.Client()\n"
             "_counter = {'n': 0}\n\n"
             "def index_and_retrieve(question, chunk_size, chunk_overlap, k):\n"
             "    splitter = RecursiveCharacterTextSplitter(\n"
             "        chunk_size=chunk_size, chunk_overlap=chunk_overlap)\n"
             "    chunks = [c.strip() for c in splitter.split_text(COURSE_HANDBOOK)]\n"
             "    _counter['n'] += 1\n"
             "    name = f\"exp_{_counter['n']}\"\n"
             "    col = client.create_collection(name)\n"
             "    col.add(documents=chunks,\n"
             "            ids=[f'{name}_c{i}' for i in range(len(chunks))])\n"
             "    res = col.query(query_texts=[question], n_results=min(k, len(chunks)))\n"
             "    return len(chunks), list(zip(res['documents'][0], res['distances'][0]))"),

    ("md", "## 3. Experiment A — chunk size\n"
           "Same question, three chunk sizes. Small chunks are focused but may cut ideas; "
           "large chunks carry more context but retrieve noisier matches."),
    ("code", "Q = 'How many automatic extensions do I get and how long are they?'\n"
             "for size in (120, 240, 600):\n"
             "    n, hits = index_and_retrieve(Q, chunk_size=size, chunk_overlap=20, k=2)\n"
             "    print(f'\\nchunk_size={size}  -> {n} chunks')\n"
             "    for doc, dist in hits:\n"
             "        print(f'  dist={dist:.3f} | {doc[:80]}...')"),

    ("md", "## 4. Experiment B — overlap\n"
           "Overlap repeats text across boundaries so a sentence that straddles a split "
           "isn't lost. Compare 0 vs 60 characters of overlap."),
    ("code", "for ov in (0, 60):\n"
             "    n, hits = index_and_retrieve(Q, chunk_size=140, chunk_overlap=ov, k=2)\n"
             "    print(f'\\nchunk_overlap={ov}  -> {n} chunks')\n"
             "    for doc, dist in hits:\n"
             "        print(f'  dist={dist:.3f} | {doc[:80]}...')"),

    ("md", "## 5. Experiment C — top-k\n"
           "More chunks give the model more to work with, but too many dilute the signal "
           "and cost tokens. Start with k = 3–5."),
    ("code", "for k in (1, 3, 5):\n"
             "    n, hits = index_and_retrieve(Q, chunk_size=240, chunk_overlap=40, k=k)\n"
             "    print(f'\\nk={k}: retrieved {len(hits)} chunks')\n"
             "    for doc, dist in hits:\n"
             "        print(f'  dist={dist:.3f} | {doc[:70]}...')"),

    ("md", "## 6. Out-of-scope → \"I don't know\"\n"
           "A good RAG system refuses when nothing relevant is retrieved. Distances for an "
           "off-topic question are large; we threshold on them. (Chroma returns squared L2 "
           "distance: smaller = more similar.)"),
    ("code", "def is_answerable(question, threshold=1.2, k=3):\n"
             "    n, hits = index_and_retrieve(question, 240, 40, k)\n"
             "    best = min(d for _, d in hits)\n"
             "    return best <= threshold, best\n\n"
             "for q in ['When is the final project due?',\n"
             "          'What is the airspeed velocity of an unladen swallow?']:\n"
             "    ok, best = is_answerable(q)\n"
             "    verdict = 'ANSWER' if ok else \"I don't know (out of scope)\"\n"
             "    print(f'best_dist={best:.3f} -> {verdict}\\n  Q: {q}\\n')"),

    ("md", "## 7. Takeaways\n"
           "- Most RAG quality comes from **retrieval** — tune chunking and `k` first.\n"
           "- **Overlap** protects ideas that span chunk boundaries.\n"
           "- A **distance threshold** turns \"no good match\" into an honest "
           "\"I don't know\" instead of a hallucination.\n"
           "- Carry these settings (and the pipeline from Notebook 1) into your "
           "**Final Project**."),
]
build_notebook(exp_nb, os.path.join(CODE, "02_rag_experiments.ipynb"))

# ---------------------------------------------------------------- notebook 3
# RAG evaluation — "Measure, don't guess." Uses the shared eval_utils.llm_judge
# / scorecard to score a RAG system on the RAG triad (Context Relevance,
# Groundedness, Answer Relevance), then change chunking and RE-MEASURE.
eval_nb = [
    ("md", "## ▶ What you'll see when you run this\n"
           "- Two RAG configs scored on the **RAG triad** (Context Relevance, Groundedness, "
           "Answer Relevance) and a printed **scorecard** showing which chunking wins.\n\n"
           "> **⚠️ Offline-eval honesty:** with **no API key** this notebook uses a **heuristic "
           "judge** *and* a **join-based generator** (it stitches the retrieved chunks together "
           "instead of calling an LLM). That answer is grounded *by construction*, so offline "
           "**Groundedness scores are inflated and the triad looks flat** — the numbers are for "
           "wiring practice, not real quality. **Add `GEMINI_API_KEY` or `ANTHROPIC_API_KEY` for "
           "real numbers.**\n\n"
           "**Time:** ~12 min · **Cost:** free (cheapest model: Gemini Flash / Claude Haiku) "
           "· **Keys:** none needed (heuristic fallback) — GEMINI_API_KEY or ANTHROPIC_API_KEY "
           "make the judge real"),

    ("md", "# Week 11 · Notebook 3 — Evaluating RAG: Measure, Don't Guess\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "You can *feel* that a RAG answer is good — but feelings don't scale and don't catch "
           "regressions. This notebook **measures** RAG quality with the **RAG triad**, then "
           "changes the chunking and **re-measures** to prove the change helped (or didn't).\n\n"
           "We reuse the course's shared `eval_utils.py` (`llm_judge`, `scorecard`) so every "
           "week scores things the same way. Judging uses **Gemini or Claude**; with no key it "
           "falls back to a transparent heuristic so the notebook still runs."),

    ("md", "## 0. Install"),
    ("code", "!pip -q install langchain-text-splitters chromadb sentence-transformers \\\n"
             "    google-generativeai anthropic"),

    ("md", "## 1. Load API keys (optional)\n"
           "With a key the judge is a real LLM; without one `llm_judge` degrades to a heuristic "
           "so nothing crashes."),
    ("code", "import os\n"
             "try:\n"
             "    from google.colab import userdata\n"
             "    for k in ('ANTHROPIC_API_KEY', 'GEMINI_API_KEY'):\n"
             "        try:\n"
             "            os.environ[k] = userdata.get(k)\n"
             "        except Exception:\n"
             "            pass\n"
             "except Exception:\n"
             "    pass\n"
             "print('Anthropic key set:', bool(os.environ.get('ANTHROPIC_API_KEY')))\n"
             "print('Gemini key set:', bool(os.environ.get('GEMINI_API_KEY')))"),

    ("md", "## 2. Import the shared eval helpers\n"
           "`eval_utils.py` lives in the repo's top-level `tools/` folder. We search upward "
           "from the notebook for it so the import works whether you're local or in Colab. "
           "If it truly can't be found, we define a tiny inline fallback so the lesson still "
           "runs."),
    ("code", "import os, sys\n\n"
             "def _find_tools_dir(start=None, max_up=6):\n"
             "    here = os.path.abspath(start or os.getcwd())\n"
             "    for _ in range(max_up):\n"
             "        cand = os.path.join(here, 'tools', 'eval_utils.py')\n"
             "        if os.path.exists(cand):\n"
             "            return os.path.dirname(cand)\n"
             "        parent = os.path.dirname(here)\n"
             "        if parent == here:\n"
             "            break\n"
             "        here = parent\n"
             "    return None\n\n"
             "tools_dir = _find_tools_dir()\n"
             "if tools_dir:\n"
             "    sys.path.insert(0, tools_dir)\n"
             "    from eval_utils import llm_judge, scorecard\n"
             "    print('Imported eval_utils from:', tools_dir)\n"
             "else:\n"
             "    print('eval_utils.py not found nearby — using a minimal inline fallback.')\n"
             "    import re, json\n"
             "    def llm_judge(question, answer, rubric='', provider='gemini'):\n"
             "        score = 3 if (answer and answer.strip()) else 1\n"
             "        return {'score': score, 'reason': '(inline heuristic fallback)',\n"
             "                'judge': 'fallback'}\n"
             "    def scorecard(rows, score_key='score'):\n"
             "        n = len(rows) or 1\n"
             "        avg = sum(float(r.get(score_key, 0) or 0) for r in rows) / n\n"
             "        print('SCORECARD', len(rows), 'cases  | avg', round(avg, 2))\n"
             "        return {'n': len(rows), 'avg': avg}"),

    ("md", "## 3. A small knowledge base + gold questions\n"
           "Same course handbook as Notebooks 1–2, plus a fixed set of **evaluation questions** "
           "(our test set). Real evals always pin a fixed question set so results are comparable "
           "run to run."),
    ("code", KB_BUILDER +
             "EVAL_QUESTIONS = [\n"
             "    'How is the final project weighted and when is it due?',\n"
             "    'How many automatic extensions do I get and how long are they?',\n"
             "    'What is the AI-use policy on exams?',\n"
             "    'When are office hours?',\n"
             "]\n"
             "print(len(EVAL_QUESTIONS), 'eval questions ready')"),

    ("md", "## 4. A RAG function we can re-configure\n"
           "Index the handbook with a given `chunk_size`/`overlap`, retrieve top-k, and answer. "
           "When a key is present we generate a **real** grounded answer with "
           "`answer_with_claude`/`answer_with_gemini` (same functions as Notebook 1) so the "
           "**Groundedness** metric actually measures the generator. With **no key** we fall back "
           "to stitching the retrieved chunks together so the notebook still runs offline — but "
           "note that fallback is grounded *by construction*, which is exactly why the triad looks "
           "flat without a key."),
    ("code", "import chromadb\n"
             "from langchain_text_splitters import RecursiveCharacterTextSplitter\n\n"
             "HAVE_CLAUDE = bool(os.environ.get('ANTHROPIC_API_KEY'))\n"
             "HAVE_GEMINI = bool(os.environ.get('GEMINI_API_KEY'))\n\n"
             "# Same grounded generators as Notebook 1 — answer ONLY from retrieved context.\n"
             "def _ground_prompt(question, retrieved):\n"
             "    context = '\\n\\n'.join(f'[{i+1}] {c}' for i, c in enumerate(retrieved))\n"
             "    return (\n"
             "        'Answer the question using ONLY the context below.\\n'\n"
             "        'If the answer is not in the context, say '\n"
             "        '\"I don\\'t know based on the provided documents.\"\\n'\n"
             "        'Cite the sources you used by their [number].\\n\\n'\n"
             "        f'Context:\\n{context}\\n\\nQuestion: {question}\\nAnswer:'\n"
             "    )\n\n"
             "def answer_with_claude(prompt):\n"
             "    import anthropic\n"
             "    msg = anthropic.Anthropic().messages.create(\n"
             "        model='claude-haiku-4-5-20251001', max_tokens=400,\n"
             "        messages=[{'role': 'user', 'content': prompt}])\n"
             "    return msg.content[0].text\n\n"
             "def answer_with_gemini(prompt):\n"
             "    import google.generativeai as genai\n"
             "    genai.configure(api_key=os.environ['GEMINI_API_KEY'])\n"
             "    return genai.GenerativeModel('gemini-2.5-flash').generate_content(prompt).text\n\n"
             "def generate(question, retrieved):\n"
             "    \"\"\"Real grounded generation when a key exists; offline join otherwise.\"\"\"\n"
             "    prompt = _ground_prompt(question, retrieved)\n"
             "    try:\n"
             "        if HAVE_CLAUDE:\n"
             "            return answer_with_claude(prompt)\n"
             "        if HAVE_GEMINI:\n"
             "            return answer_with_gemini(prompt)\n"
             "    except Exception as e:\n"
             "        print('[generator fell back to offline join:', e, ']')\n"
             "    return ' '.join(retrieved)   # offline fallback (grounded by construction)\n\n"
             "client = chromadb.Client()\n"
             "_n = {'i': 0}\n\n"
             "def build_rag(chunk_size, chunk_overlap):\n"
             "    splitter = RecursiveCharacterTextSplitter(\n"
             "        chunk_size=chunk_size, chunk_overlap=chunk_overlap)\n"
             "    chunks = [c.strip() for c in splitter.split_text(COURSE_HANDBOOK)]\n"
             "    _n['i'] += 1\n"
             "    col = client.create_collection(f\"eval_{_n['i']}\")\n"
             "    col.add(documents=chunks,\n"
             "            ids=[f'c{j}' for j in range(len(chunks))])\n\n"
             "    def rag(question, k=3):\n"
             "        res = col.query(query_texts=[question],\n"
             "                        n_results=min(k, len(chunks)))\n"
             "        retrieved = res['documents'][0]\n"
             "        answer = generate(question, retrieved)\n"
             "        return {'question': question, 'context': retrieved, 'answer': answer}\n"
             "    return rag"),

    ("md", "## 5. The RAG triad — three judges, three questions\n"
           "The RAG triad (popularized by TruLens) checks the **three links** in a RAG chain:\n\n"
           "| Metric | Question it answers | Compares |\n"
           "|---|---|---|\n"
           "| **Context Relevance** | Did we retrieve the *right* chunks? | question ↔ context |\n"
           "| **Groundedness** | Is the answer *supported* by the context (not made up)? | answer ↔ context |\n"
           "| **Answer Relevance** | Does the answer actually address the question? | answer ↔ question |\n\n"
           "If any link is weak you know *where* RAG broke — retrieval, faithfulness, or "
           "focus. We score each 1–5 with `llm_judge`."),
    ("code", "CONTEXT_RUBRIC = ('Rate 1-5 how RELEVANT the retrieved context is to the question. '\n"
             "                  'Return ONLY JSON: {\"score\": <int 1-5>, \"reason\": \"<short>\"}.')\n"
             "GROUND_RUBRIC  = ('Rate 1-5 how well the ANSWER is GROUNDED in (supported by) the '\n"
             "                  'context — penalize anything not in the context. '\n"
             "                  'Return ONLY JSON: {\"score\": <int 1-5>, \"reason\": \"<short>\"}.')\n"
             "ANSWER_RUBRIC  = ('Rate 1-5 how RELEVANT the answer is to the question. '\n"
             "                  'Return ONLY JSON: {\"score\": <int 1-5>, \"reason\": \"<short>\"}.')\n\n"
             "def rag_triad(item):\n"
             "    ctx = '\\n'.join(item['context'])\n"
             "    cr = llm_judge(item['question'], ctx, CONTEXT_RUBRIC)['score']\n"
             "    gr = llm_judge('Context:\\n' + ctx, item['answer'], GROUND_RUBRIC)['score']\n"
             "    ar = llm_judge(item['question'], item['answer'], ANSWER_RUBRIC)['score']\n"
             "    triad = (cr + gr + ar) / 3\n"
             "    return {'context_relevance': cr, 'groundedness': gr,\n"
             "            'answer_relevance': ar, 'score': round(triad, 2)}"),

    ("md", "## 6. Baseline run — measure config A\n"
           "Evaluate small chunks (`chunk_size=120`). The `scorecard` prints a per-question "
           "report and an average triad score — our **baseline number to beat**."),
    ("code", "def evaluate(rag, label):\n"
             "    rows = []\n"
             "    for q in EVAL_QUESTIONS:\n"
             "        item = rag(q, k=3)\n"
             "        scores = rag_triad(item)\n"
             "        rows.append({'q': q, **scores})\n"
             "    print(f'\\n### {label}')\n"
             "    summary = scorecard(rows)\n"
             "    return rows, summary\n\n"
             "rag_a = build_rag(chunk_size=120, chunk_overlap=10)\n"
             "rows_a, sum_a = evaluate(rag_a, 'Config A — small chunks (120/10)')"),

    ("md", "## 7. Change the chunking, then RE-MEASURE — config B\n"
           "Larger chunks with more overlap (`chunk_size=300`, `overlap=60`) usually retrieve "
           "more complete context. We change **one thing** and re-run the **same** eval set so "
           "the comparison is fair."),
    ("code", "rag_b = build_rag(chunk_size=300, chunk_overlap=60)\n"
             "rows_b, sum_b = evaluate(rag_b, 'Config B — larger chunks (300/60)')"),

    ("md", "## 8. Compare — did the change help?\n"
           "Now we have **numbers**, not vibes. Whichever config has the higher average triad "
           "score wins; if they tie, the simpler/cheaper one wins."),
    ("code", "print('Config A avg triad:', round(sum_a['avg'], 2))\n"
             "print('Config B avg triad:', round(sum_b['avg'], 2))\n"
             "delta = sum_b['avg'] - sum_a['avg']\n"
             "verdict = ('B is better' if delta > 0 else\n"
             "           'A is better' if delta < 0 else 'tie')\n"
             "print(f'Difference (B - A): {delta:+.2f}  ->  {verdict}')\n"
             "print('\\nNote: with NO API key both runs use the heuristic judge, so scores will')\n"
             "print('look flat. Add GEMINI_API_KEY or ANTHROPIC_API_KEY to see the triad separate.')"),

    ("md", "## 9. Takeaways\n"
           "- **Measure, don't guess.** A fixed question set + the **RAG triad** turns "
           "\"feels good\" into a number you can track.\n"
           "- The triad **localizes** failures: low *Context Relevance* → fix retrieval/chunking; "
           "low *Groundedness* → tighten the grounding prompt; low *Answer Relevance* → fix the "
           "question framing or the generator.\n"
           "- **Change one thing, re-measure.** That's how you improve a RAG system without "
           "fooling yourself.\n"
           "- We use the **same** `eval_utils.llm_judge` / `scorecard` here as in Weeks 9, 13, "
           "16, and 17 — evaluation is a course-long throughline, not a final-week topic.\n\n"
           "**Your turn:** plug `answer_with_claude` from Notebook 1 into `build_rag`, re-run the "
           "triad on a real generator, and report which config you'd ship for your Final Project."),
]
build_notebook(eval_nb, os.path.join(CODE, "03_rag_evaluation.ipynb"))

# ---------------------------------------------------------------- notebook 4
# Modern RAG (2026): hybrid retrieval (dense + BM25, fused) + cross-encoder
# reranking. Retrieval-only, no API key. Every external package import is
# guarded so the notebook degrades gracefully if something is missing.
hybrid_nb = [
    ("md", "## ▶ What you'll see when you run this\n"
           "- The **same query** ranked three ways — **dense** (embeddings), **BM25** "
           "(keyword), and a **fused hybrid** list — then a **cross-encoder reranker** "
           "reordering the top candidates, so you can watch each upgrade change the order.\n\n"
           "**Time:** ~8 min · **Cost:** free (all local Hugging Face models, retrieval-only) "
           "· **Keys:** none required. *Every extra package is import-guarded — if one is "
           "missing, that step is skipped with a note instead of crashing.*"),

    ("md", "# Week 11 · Notebook 4 — Modern RAG: Hybrid Retrieval + Reranking\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Plain vector search is the **starting point**. Here we add two of the 2026 "
           "upgrades from the lecture, kept deliberately small:\n"
           "1. **Hybrid search** — combine **dense** (sentence-transformers) similarity with "
           "**BM25** keyword scores and **fuse** them, so we catch both paraphrases *and* exact "
           "terms.\n"
           "2. **Reranking** — let a **cross-encoder** read each *(question, chunk)* pair "
           "together and reorder the shortlist.\n\n"
           "> No OpenAI, no API key: embeddings + reranker are local Hugging Face models. "
           "Imports are guarded so missing packages degrade gracefully."),

    ("md", "## 0. Install (all local, no keys)"),
    ("code", "!pip -q install sentence-transformers rank-bm25"),

    ("md", "## 1. A tiny corpus\n"
           "Same course handbook, pre-split into short passages so we can see the ranking move. "
           "Notice the exact tokens (`CSCI250`, `48-hour`) — those are where keyword search earns "
           "its keep."),
    ("code", "CHUNKS = [\n"
             "    'Modules open Monday and the weekly lab is due Sunday at 11:59 PM Pacific.',\n"
             "    'You may miss deadlines twice using the two automatic 48-hour extensions.',\n"
             "    'Students may use AI assistants such as Claude and Gemini, but must disclose it.',\n"
             "    'Exams, including the midterm and final, are AI-restricted.',\n"
             "    'Labs are 50 percent, the midterm 20 percent, the final project 30 percent.',\n"
             "    'The final project is due December 19.',\n"
             "    'Office hours: Tuesday 5-6 PM and Saturday 10-11 AM Pacific on Zoom.',\n"
             "    'Email the instructor with the subject prefix CSCI250 for a 48-hour reply.',\n"
             "]\n"
             "QUERY = 'How long are the automatic extensions and how do I email the instructor?'\n"
             "print(len(CHUNKS), 'chunks; query =', QUERY)"),

    ("md", "## 2. Dense retrieval (embeddings)\n"
           "Embed the query and every chunk with a local sentence-transformers model and rank by "
           "cosine similarity. Great at paraphrases; can blur exact tokens."),
    ("code", "import numpy as np\n\n"
             "dense_scores = None\n"
             "try:\n"
             "    from sentence_transformers import SentenceTransformer\n"
             "    embedder = SentenceTransformer('all-MiniLM-L6-v2')\n"
             "    emb = embedder.encode([QUERY] + CHUNKS, normalize_embeddings=True)\n"
             "    qv, cv = emb[0], emb[1:]\n"
             "    dense_scores = cv @ qv   # cosine sim (vectors are normalized)\n"
             "    order = np.argsort(-dense_scores)\n"
             "    print('DENSE ranking:')\n"
             "    for r in order:\n"
             "        print(f'  {dense_scores[r]:.3f} | {CHUNKS[r]}')\n"
             "except Exception as e:\n"
             "    print('[sentence-transformers unavailable, skipping dense:', e, ']')"),

    ("md", "## 3. BM25 keyword retrieval\n"
           "BM25 is classic bag-of-words keyword scoring. It nails exact terms (`48-hour`, "
           "`CSCI250`) that dense embeddings smear together."),
    ("code", "bm25_scores = None\n"
             "try:\n"
             "    from rank_bm25 import BM25Okapi\n"
             "    tokenized = [c.lower().split() for c in CHUNKS]\n"
             "    bm25 = BM25Okapi(tokenized)\n"
             "    bm25_scores = np.array(bm25.get_scores(QUERY.lower().split()))\n"
             "    order = np.argsort(-bm25_scores)\n"
             "    print('BM25 ranking:')\n"
             "    for r in order:\n"
             "        print(f'  {bm25_scores[r]:.3f} | {CHUNKS[r]}')\n"
             "except Exception as e:\n"
             "    print('[rank-bm25 unavailable, skipping BM25:', e, ']')"),

    ("md", "## 4. Fuse them → hybrid\n"
           "Two rankers, two score scales — so we **min-max normalize** each to 0–1 and average. "
           "(In production a common alternative is *Reciprocal Rank Fusion*, which fuses by rank "
           "position instead of score.) If only one ranker ran, we fall back to it."),
    ("code", "def _norm(x):\n"
             "    x = np.asarray(x, dtype=float)\n"
             "    lo, hi = x.min(), x.max()\n"
             "    return (x - lo) / (hi - lo) if hi > lo else np.zeros_like(x)\n\n"
             "parts = [s for s in (dense_scores, bm25_scores) if s is not None]\n"
             "if not parts:\n"
             "    raise SystemExit('Neither retriever ran — install the packages above.')\n"
             "hybrid = np.mean([_norm(p) for p in parts], axis=0)\n"
             "hyb_order = list(np.argsort(-hybrid))\n"
             "print(f'HYBRID ranking (fused {len(parts)} retriever(s)):')\n"
             "for r in hyb_order:\n"
             "    print(f'  {hybrid[r]:.3f} | {CHUNKS[r]}')\n\n"
             "TOP_N = 4\n"
             "shortlist = hyb_order[:TOP_N]\n"
             "print('\\nShortlist for reranking:', shortlist)"),

    ("md", "## 5. Rerank the shortlist with a cross-encoder\n"
           "Bi-encoders (steps 2–4) embed the query and chunk **separately**. A **cross-encoder** "
           "reads the *(query, chunk)* pair **together**, so it scores relevance much more "
           "accurately — but it runs once per candidate, which is why we only rerank the "
           "shortlist, not the whole corpus. Guarded so a missing package just keeps the hybrid "
           "order."),
    ("code", "try:\n"
             "    from sentence_transformers import CrossEncoder\n"
             "    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')\n"
             "    pairs = [(QUERY, CHUNKS[i]) for i in shortlist]\n"
             "    ce_scores = reranker.predict(pairs)\n"
             "    reranked = [i for _, i in sorted(zip(ce_scores, shortlist),\n"
             "                                     key=lambda t: -t[0])]\n"
             "    print('RERANKED top results (cross-encoder):')\n"
             "    for s, i in sorted(zip(ce_scores, shortlist), key=lambda t: -t[0]):\n"
             "        print(f'  {s:+.2f} | {CHUNKS[i]}')\n"
             "    final = reranked\n"
             "except Exception as e:\n"
             "    print('[cross-encoder unavailable, keeping hybrid order:', e, ']')\n"
             "    final = shortlist\n\n"
             "print('\\nFinal context order to feed the LLM:', final)"),

    ("md", "## 6. Takeaways\n"
           "- **Hybrid** (dense + BM25) catches both paraphrases and exact tokens — fuse the two "
           "ranked lists.\n"
           "- **Reranking** with a cross-encoder reorders the shortlist far more accurately than "
           "first-pass similarity; only rerank the top-k (it's slower per item).\n"
           "- These are **additive upgrades** to Notebook 1's pipeline — add them only when the "
           "**RAG triad** (Notebook 3) says plain vector search is the bottleneck.\n"
           "- Still 2026 baseline you didn't run here: **Contextual Retrieval** (prepend a context "
           "blurb to each chunk before embedding) and **agentic RAG** (the model decides "
           "when/what to retrieve) — see the lecture notes.\n\n"
           "> **Responsible AI:** even with hybrid + reranking, RAG can still hallucinate — always "
           "cite sources, and remember retrieval **amplifies bias in your corpus**."),
]
build_notebook(hybrid_nb, os.path.join(CODE, "04_hybrid_rerank.ipynb"))

print("wrote Week 11 notebooks (01, 02, 03, 04) to", CODE)
