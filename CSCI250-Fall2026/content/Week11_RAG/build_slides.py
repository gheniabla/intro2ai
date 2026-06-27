"""Build slides.pptx for Week 11. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 11 — Retrieval-Augmented Generation (RAG)",
     "subtitle": "CSCI 250 — Introduction to Artificial Intelligence · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "Why RAG: give the LLM an open-book exam",
        "The pipeline: load → chunk → embed → store → retrieve → ground → generate → cite",
        "Chunking trade-offs (size & overlap)",
        "Retrieve from ChromaDB; ground the prompt",
        "Generate with Claude AND Gemini; cite sources",
        "Evaluate with the RAG triad — measure, don't guess",
        ("No graded assignment — build a reusable RAG pipeline", 1)]},

    {"type": "section", "title": "Why RAG?"},
    {"type": "bullets", "title": "A Bare LLM Can't See...", "bullets": [
        "Your private documents (notes, PDFs, wiki)",
        "Anything after its training cutoff",
        "Niche facts it never memorized reliably",
        ("Ask anyway → it may hallucinate (confident + wrong)", 1),
        "RAG = retrieve trusted text, put it in the prompt, answer from THAT",
        ("vs fine-tuning: RAG is editable, cheap to update, and citable", 1)]},

    {"type": "section", "title": "The RAG Pipeline"},
    {"type": "two_col", "title": "Two Phases",
     "left_title": "Indexing (once, ahead)",
     "left": ["load documents", "chunk into passages",
              "embed each chunk", "store in ChromaDB + metadata"],
     "right_title": "Query time (per question)",
     "right": ["embed the question", "retrieve top-k chunks",
               "ground the prompt", "generate + cite (Claude / Gemini)"]},

    {"type": "section", "title": "Chunking"},
    {"type": "code", "title": "Split Documents Sensibly",
     "code": "from langchain_text_splitters import RecursiveCharacterTextSplitter\n\n"
             "splitter = RecursiveCharacterTextSplitter(\n"
             "    chunk_size=500,     # ~chars per chunk\n"
             "    chunk_overlap=80,   # repeat text across boundaries\n"
             ")\n"
             "chunks = splitter.split_text(long_text)",
     "caption": "Too big = noisy retrieval; too small = ideas cut in half; overlap keeps them whole"},

    {"type": "code", "title": "Embed & Store (with metadata)",
     "code": "import chromadb\n"
             "col = chromadb.Client().create_collection('kb')\n"
             "col.add(\n"
             "    documents=chunks,\n"
             "    metadatas=[{'source': 'handbook.txt', 'chunk': i}\n"
             "               for i in range(len(chunks))],\n"
             "    ids=[f'c{i}' for i in range(len(chunks))],\n"
             ")",
     "caption": "Metadata (source, chunk #) is what makes citations possible later"},

    {"type": "section", "title": "Retrieve & Ground"},
    {"type": "code", "title": "Retrieve, then Ground the Prompt",
     "code": "res = col.query(query_texts=[question], n_results=3)\n"
             "retrieved = res['documents'][0]\n"
             "context = '\\n\\n'.join(f'[{i+1}] {c}'\n"
             "                       for i, c in enumerate(retrieved))\n\n"
             "prompt = f'''Answer using ONLY the context below.\n"
             "If it is not in the context, say \"I don't know.\"\n"
             "Cite sources by [number].\n\n"
             "Context:\\n{context}\\n\\nQuestion: {question}'''",
     "caption": "The grounding instruction is the heart of RAG"},

    {"type": "code", "title": "Generate — Claude & Gemini",
     "code": "# Claude\n"
             "import anthropic\n"
             "msg = anthropic.Anthropic().messages.create(\n"
             "    model='claude-sonnet-4-6', max_tokens=400,\n"
             "    messages=[{'role':'user','content':prompt}])\n"
             "print(msg.content[0].text)\n\n"
             "# Gemini\n"
             "import google.generativeai as genai\n"
             "genai.configure(api_key=os.environ['GEMINI_API_KEY'])\n"
             "g = genai.GenerativeModel('gemini-2.5-flash')\n"
             "print(g.generate_content(prompt).text)",
     "caption": "Same retrieved context, two generators — compare faithfulness"},

    {"type": "bullets", "title": "Cite Sources & Know Your Limits", "bullets": [
        "Show WHICH chunks/documents were used",
        "Answer \"I don't know\" when retrieval is empty or weak",
        "Never invent a citation that wasn't retrieved",
        ("Most RAG bugs are in RETRIEVAL, not generation", 1),
        ("Print the retrieved chunks FIRST when debugging", 1)]},

    {"type": "section", "title": "Evaluate RAG — Measure, Don't Guess"},
    {"type": "two_col", "title": "The RAG Triad",
     "left_title": "Three links to check",
     "left": ["Context Relevance: right chunks?",
              "Groundedness: answer supported?",
              "Answer Relevance: on topic?",
              "Each scored 1-5 by an LLM judge"],
     "right_title": "Why it's powerful",
     "right": ["Localizes the failure",
               "Low context -> fix retrieval",
               "Low groundedness -> fix prompt",
               "Low answer rel. -> fix framing"]},

    {"type": "code", "title": "Score It With the Shared Helpers",
     "code": "from eval_utils import llm_judge, scorecard\n\n"
             "rubric = ('Rate 1-5 how RELEVANT the answer is. '\n"
             "          'Return ONLY JSON: {\"score\": <int>, \"reason\": \"\"}.')\n"
             "llm_judge(question, answer, rubric)\n"
             "#   -> {'score': 4, 'reason': '...', 'judge': 'gemini'}\n\n"
             "rows = [{'q': q, **rag_triad(rag(q))} for q in EVAL_QS]\n"
             "scorecard(rows)   # per-question + average triad",
     "caption": "Gemini Flash / Claude Haiku judge; heuristic fallback with no key — never crashes"},

    {"type": "bullets", "title": "Baseline → Change One Thing → Re-measure", "bullets": [
        "Pin a FIXED set of eval questions (a test set)",
        "Score a baseline config; print the scorecard",
        "Change one thing (chunk_size 120 -> 300)",
        ("Re-measure on the SAME questions — compare averages", 1),
        ("Higher triad wins; ties go to the simpler/cheaper config", 1),
        "This is how you improve RAG without fooling yourself"]},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Run 01_rag_pipeline.ipynb (full RAG, Claude + Gemini)",
        "Run 02_rag_experiments.ipynb (tune chunk_size, overlap, k)",
        "Run 03_rag_evaluation.ipynb (RAG triad + re-measure)",
        "Try an out-of-scope question → expect \"I don't know\"",
        "Save the pipeline — reuse it for your Final Project"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
