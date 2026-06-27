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
           "We keep generation simple and **offline-friendly**: the \"answer\" stitches the "
           "retrieved chunks together. (Swap in `answer_with_claude`/`answer_with_gemini` from "
           "Notebook 1 to evaluate a real generator the same way.)"),
    ("code", "import chromadb\n"
             "from langchain_text_splitters import RecursiveCharacterTextSplitter\n\n"
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
             "        answer = ' '.join(retrieved)   # naive 'generator' for an offline demo\n"
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

print("wrote Week 11 notebooks (01, 02, 03) to", CODE)
