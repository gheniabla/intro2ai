"""Build slides.pptx for Week 10. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 10 — GenAI Frameworks & Vector Storage",
     "subtitle": "CSCI 250 — Introduction to Artificial Intelligence · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "Build embeddings & semantic search FROM SCRATCH (notebook 00 first)",
        "Why keyword search fails; cosine similarity by hand; top-k search",
        "ChromaDB = the scaled-up version of what you built",
        "GenAI frameworks: LangChain building blocks & chains",
        "Document loaders & text splitters; LlamaIndex",
        ("Assignment A8: embeddings + semantic search + a simple LLM app", 1)]},

    {"type": "section", "title": "Embeddings — Build It Before the Database"},
    {"type": "bullets", "title": "Start With the Dumb Baseline", "bullets": [
        "Keyword / substring search matches LETTERS, not meaning",
        "Query \"a young feline resting\" over \"The cat napped...\"",
        ("-> zero hits: none of those words literally appear", 1),
        "A human sees the match instantly — the computer doesn't",
        ("That failure is exactly WHY embeddings exist", 1)]},

    {"type": "code", "title": "Embeddings + Cosine Similarity, by Hand",
     "code": "from sentence_transformers import SentenceTransformer\n"
             "import numpy as np\n\n"
             "model = SentenceTransformer(\"all-MiniLM-L6-v2\")  # 384-dim, local, free\n"
             "emb = model.encode(corpus)            # (n, 384) meaning-vectors\n\n"
             "def cosine(a, b):\n"
             "    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))\n\n"
             "cosine(emb[0], emb[1])   # cat vs kitten -> high\n"
             "cosine(emb[0], emb[5])   # cat vs market -> low",
     "caption": "No library magic: a dot product over two normalized vectors. NO OpenAI"},

    {"type": "code", "title": "Top-k Semantic Search — From Scratch",
     "code": "def semantic_search(query, corpus, emb, k=3):\n"
             "    q = model.encode([query])[0]\n"
             "    scores = [cosine(q, e) for e in emb]   # vs every vector\n"
             "    ranked = sorted(enumerate(scores),\n"
             "                    key=lambda x: x[1], reverse=True)\n"
             "    return ranked[:k]\n\n"
             "semantic_search(\"a young feline resting\", corpus, emb)\n"
             "# -> the cat sentences keyword search MISSED",
     "caption": "This is the whole trick behind a vector database, in 5 lines"},

    {"type": "code", "title": "ChromaDB = The Scaled Version",
     "code": "import chromadb\n"
             "col = chromadb.Client().create_collection(\"notes\")\n"
             "col.add(documents=corpus,\n"
             "        ids=[str(i) for i in range(len(corpus))])\n\n"
             "col.query(query_texts=[\"a young feline resting\"],\n"
             "          n_results=3)\n"
             "# same top results, now fast + indexed + persistent",
     "caption": "col.query() IS your semantic_search() with an index under the hood"},

    {"type": "section", "title": "Why Frameworks?"},
    {"type": "two_col", "title": "LangChain vs LlamaIndex",
     "left_title": "LangChain",
     "left": ["Chaining LLM steps", "Swap models / providers",
              "Tools & agents", "\"Lego bricks for pipelines\""],
     "right_title": "LlamaIndex",
     "right": ["Ingest + index your docs", "Q&A / retrieval focus",
               "Very little code", "\"A librarian for your docs\""]},

    {"type": "section", "title": "LangChain Building Blocks"},
    {"type": "code", "title": "Chains with LCEL (the | pipe)",
     "code": "from langchain_anthropic import ChatAnthropic\n"
             "from langchain_core.prompts import ChatPromptTemplate\n"
             "from langchain_core.output_parsers import StrOutputParser\n\n"
             "claude = ChatAnthropic(model=\"claude-sonnet-4-6\", max_tokens=300)\n"
             "prompt = ChatPromptTemplate.from_messages([\n"
             "    (\"human\", \"Explain {topic} in 2 sentences.\")])\n\n"
             "chain = prompt | claude | StrOutputParser()\n"
             "print(chain.invoke({\"topic\": \"vector stores\"}))",
     "caption": "Swap claude for gemini and the rest of the chain is unchanged"},

    {"type": "code", "title": "Loaders & Splitters",
     "code": "from langchain_community.document_loaders import TextLoader\n"
             "from langchain_text_splitters import RecursiveCharacterTextSplitter\n\n"
             "docs = TextLoader(\"notes.txt\").load()\n"
             "splitter = RecursiveCharacterTextSplitter(\n"
             "    chunk_size=500, chunk_overlap=50)\n"
             "chunks = splitter.split_documents(docs)\n"
             "print(len(chunks), \"chunks\")",
     "caption": "chunk_overlap repeats a little text so cross-boundary ideas survive"},

    {"type": "bullets", "title": "Preview: Ask-Your-Docs (→ RAG)", "bullets": [
        "1. Retrieve relevant chunks (vector search)",
        "2. Stuff them into the prompt as context",
        "3. Generate a grounded answer (Claude or Gemini)",
        ("Next week (Week 11) = full citation-aware RAG pipeline", 1)]},

    {"type": "bullets", "title": "Final Project Ideas (posted this week)", "bullets": [
        "Ask-your-notes / docs chatbot (RAG)",
        "Study-guide / quiz generator with citations",
        "Codebase Q&A — index a small repo",
        "Policy / FAQ assistant that cites sources",
        ("Proposal is Capstone M1 (Week 9); Capstone grows M2–M5", 1)]},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Run 00_embeddings_intuition.ipynb FIRST (build it from scratch)",
        "Run 01_langchain_llamaindex.ipynb",
        "Run 02_embeddings_chromadb.ipynb",
        "Draft one Final Project idea",
        "Submit Assignment A8 by Sunday 11:59 PM PST"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
