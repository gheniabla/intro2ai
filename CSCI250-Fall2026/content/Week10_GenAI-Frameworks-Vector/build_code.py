"""Build Week 10 sample-code notebooks. Run: python build_code.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# ---------------------------------------------------------------- notebook 0
# Embeddings intuition — runs BEFORE LangChain/ChromaDB. Build the idea from the
# ground up: keyword search fails -> embed -> cosine by hand -> heatmap ->
# top-k from scratch -> THEN ChromaDB as "the scaled version of what you built."
embeddings_nb = [
    ("md", "## ▶ What you'll see when you run this\n"
           "- Keyword search **misses** a sentence that clearly means the same thing, then "
           "embeddings + cosine similarity **find it** — and a heatmap shows why.\n\n"
           "**Time:** ~10 min · **Cost:** free (local Hugging Face model, no LLM call) "
           "· **Keys:** none"),

    ("md", "# Week 10 · Notebook 0 — Embeddings Intuition (build it before the database)\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Before you trust a vector database, build the idea yourself:\n"
           "1. Watch **keyword search fail** on a meaning-based question (the dumb baseline).\n"
           "2. Turn sentences into **embeddings** with a free local model.\n"
           "3. Compute **cosine similarity by hand** with NumPy and **see it as a heatmap**.\n"
           "4. Write **top-k semantic search from scratch** (it's ~5 lines).\n"
           "5. Only THEN meet **ChromaDB** — the scaled-up version of what you just built.\n\n"
           "> Runs in Google Colab. No API key, no OpenAI — embeddings are local Hugging Face."),

    ("md", "## 0. Install\n"
           "`sentence-transformers` gives us a small, free embedding model; `matplotlib` draws "
           "the heatmap; `chromadb` is only needed for the very last section."),
    ("code", "!pip -q install sentence-transformers matplotlib numpy chromadb"),

    ("md", "## 1. Our tiny corpus\n"
           "Ten short sentences on a few themes (pets, weather, finance, programming). "
           "We'll search them two ways and compare."),
    ("code", "corpus = [\n"
             "    'The cat napped on the warm windowsill.',\n"
             "    'A kitten chased a ball of yarn across the room.',\n"
             "    'My dog loves long walks in the park.',\n"
             "    'It rained heavily all afternoon and the streets flooded.',\n"
             "    'A gentle breeze and clear skies made for a lovely day.',\n"
             "    'The stock market dropped sharply after the report.',\n"
             "    'Investors worried about rising interest rates.',\n"
             "    'Python is a popular language for data science.',\n"
             "    'I debugged the function until all the tests passed.',\n"
             "    'The recipe needs two cups of flour and one egg.',\n"
             "]\n"
             "for i, s in enumerate(corpus):\n"
             "    print(i, s)"),

    ("md", "## 2. The dumbest baseline: keyword / substring search\n"
           "Ask for a **young cat**. A human knows sentence 1 (\"cat\") is a match. But our query "
           "words don't literally appear, so substring search returns **nothing useful**."),
    ("code", "def keyword_search(query, corpus):\n"
             "    q_words = set(query.lower().split())\n"
             "    hits = []\n"
             "    for i, s in enumerate(corpus):\n"
             "        s_words = set(s.lower().replace('.', '').split())\n"
             "        overlap = q_words & s_words\n"
             "        if overlap:\n"
             "            hits.append((i, overlap))\n"
             "    return hits\n\n"
             "query = 'a young feline resting'\n"
             "print('Query:', query)\n"
             "print('Keyword hits:', keyword_search(query, corpus))\n"
             "print('\\n-> None of these words appear literally, so keyword search FINDS NOTHING,')\n"
             "print('   even though sentences 0 and 1 are obviously about cats.')"),

    ("md", "## 3. Embeddings = meaning as a vector\n"
           "A **sentence embedding** turns each sentence into a fixed-length list of numbers "
           "(here 384) that captures *meaning*. Sentences that mean similar things get similar "
           "vectors. We use a small, free, **local** Hugging Face model."),
    ("code", "from sentence_transformers import SentenceTransformer\n"
             "import numpy as np\n\n"
             "model = SentenceTransformer('all-MiniLM-L6-v2')   # 384-dim, free, local\n"
             "embeddings = model.encode(corpus)\n"
             "print('embeddings shape:', embeddings.shape)   # (10 sentences, 384 numbers each)\n"
             "print('first sentence, first 8 numbers:', np.round(embeddings[0][:8], 3))"),

    ("md", "## 4. Cosine similarity, by hand\n"
           "**Cosine similarity** measures the *angle* between two vectors, ignoring length:\n\n"
           "$$\\cos(\\mathbf{a},\\mathbf{b}) = \\frac{\\mathbf{a}\\cdot\\mathbf{b}}"
           "{\\lVert\\mathbf{a}\\rVert\\,\\lVert\\mathbf{b}\\rVert}$$\n\n"
           "It runs from -1 (opposite) to 1 (identical direction). We write it with NumPy — "
           "no library magic."),
    ("code", "def cosine(a, b):\n"
             "    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))\n\n"
             "print('cat (0)    vs kitten (1):', round(cosine(embeddings[0], embeddings[1]), 3))\n"
             "print('cat (0)    vs market (5):', round(cosine(embeddings[0], embeddings[5]), 3))\n"
             "print('market (5) vs rates  (6):', round(cosine(embeddings[5], embeddings[6]), 3))\n"
             "print('\\nSame topic -> high score; different topic -> low score.')"),

    ("md", "## 5. The whole similarity matrix as a heatmap\n"
           "Compare every sentence to every other sentence. Bright blocks along the diagonal "
           "reveal the **themes** the model discovered — pets, weather, finance, programming — "
           "with no labels given to it."),
    ("code", "import matplotlib.pyplot as plt\n\n"
             "# Normalize rows so a single matrix multiply gives all pairwise cosines.\n"
             "norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)\n"
             "sim = norm @ norm.T          # (10, 10) cosine-similarity matrix\n\n"
             "fig, ax = plt.subplots(figsize=(7, 6))\n"
             "im = ax.imshow(sim, cmap='viridis')\n"
             "ax.set_xticks(range(len(corpus)))\n"
             "ax.set_yticks(range(len(corpus)))\n"
             "ax.set_title('Sentence-to-sentence cosine similarity')\n"
             "fig.colorbar(im, label='cosine similarity')\n"
             "plt.tight_layout(); plt.show()\n\n"
             "print('Bright off-diagonal cells = different sentences the model thinks are related.')"),

    ("md", "## 6. Top-k semantic search, from scratch\n"
           "This is the whole trick behind a vector database, in a few lines: **embed the query, "
           "cosine-compare it to every stored vector, sort, take the top k.** Re-run the same "
           "query that keyword search whiffed on."),
    ("code", "def semantic_search(query, corpus, embeddings, k=3):\n"
             "    q = model.encode([query])[0]\n"
             "    scores = [cosine(q, e) for e in embeddings]       # compare to every sentence\n"
             "    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)\n"
             "    return ranked[:k]\n\n"
             "query = 'a young feline resting'\n"
             "print('Query:', query, '\\n')\n"
             "for idx, score in semantic_search(query, corpus, embeddings, k=3):\n"
             "    print(f'  {score:.3f}  [{idx}] {corpus[idx]}')\n"
             "print('\\n-> Embeddings find the cat sentences that keyword search MISSED.')"),

    ("md", "## 7. Check yourself\n"
           "Try a finance query and a programming query. Notice you never typed the matching "
           "words — the model matches on **meaning**."),
    ("code", "for q in ['worries about the economy', 'fixing code with tests']:\n"
             "    print('Query:', q)\n"
             "    for idx, score in semantic_search(q, corpus, embeddings, k=2):\n"
             "        print(f'  {score:.3f}  [{idx}] {corpus[idx]}')\n"
             "    print()"),

    ("md", "## 8. ChromaDB = the scaled version of what you just built\n"
           "You wrote: store vectors → cosine-compare a query → sort → take top-k. "
           "A **vector database** does exactly that, but fast over millions of items, with "
           "persistence and metadata. The mental model is unchanged — `col.query(...)` is your "
           "`semantic_search(...)` with an index under the hood."),
    ("code", "import chromadb\n"
             "client = chromadb.Client()                 # in-memory\n"
             "col = client.create_collection('week10_intuition')\n"
             "col.add(documents=corpus, ids=[str(i) for i in range(len(corpus))])\n\n"
             "res = col.query(query_texts=['a young feline resting'], n_results=3)\n"
             "for doc, dist in zip(res['documents'][0], res['distances'][0]):\n"
             "    print(f'  dist={dist:.3f} | {doc}')\n\n"
             "print('\\nSame top results as your from-scratch search — now backed by an index.')\n"
             "print('(Chroma returns a DISTANCE: smaller = closer. Your cosine was a SIMILARITY:')\n"
             "print(' larger = closer. Same ordering, flipped scale.)')"),

    ("md", "## 9. Recap\n"
           "- **Keyword search** matches letters; it misses meaning.\n"
           "- An **embedding** is meaning as a vector; **cosine similarity** measures closeness.\n"
           "- **Top-k semantic search** = embed query → cosine vs all → sort → take k.\n"
           "- A **vector store (ChromaDB)** is that same idea, scaled and indexed.\n\n"
           "Next: Notebook 1 wires this into **LangChain**, and Notebook 2 goes deeper on "
           "**ChromaDB**. You now know what they're doing underneath."),
]
build_notebook(embeddings_nb, os.path.join(CODE, "00_embeddings_intuition.ipynb"))

# ---------------------------------------------------------------- notebook 1
langchain_nb = [
    ("md", "# Week 10 · Notebook 1 — LangChain & LlamaIndex Building Blocks\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Compose GenAI apps from reusable parts: **models → prompts → parsers → chains**, "
           "plus a quick **LlamaIndex** document index.\n\n"
           "> Runs in Google Colab. Cells **degrade gracefully** if a package or API key is "
           "missing — you'll get a clear message instead of a crash. We use **Claude** and "
           "**Gemini** (never OpenAI)."),

    ("md", "## 0. Install frameworks"),
    ("code", "!pip -q install langchain langchain-core langchain-community \\\n"
             "    langchain-anthropic langchain-google-genai \\\n"
             "    llama-index sentence-transformers"),

    ("md", "## 1. Load API keys safely\n"
           "In Colab use the 🔑 *Secrets* panel; locally use environment variables. "
           "**Never commit keys.**"),
    ("code", "import os\n"
             "try:\n"
             "    from google.colab import userdata\n"
             "    for k in ('ANTHROPIC_API_KEY', 'GEMINI_API_KEY', 'GOOGLE_API_KEY'):\n"
             "        try:\n"
             "            os.environ[k] = userdata.get(k)\n"
             "        except Exception:\n"
             "            pass\n"
             "except Exception:\n"
             "    pass  # not on Colab — set keys in your shell\n"
             "# langchain-google-genai reads GOOGLE_API_KEY\n"
             "if os.environ.get('GEMINI_API_KEY') and not os.environ.get('GOOGLE_API_KEY'):\n"
             "    os.environ['GOOGLE_API_KEY'] = os.environ['GEMINI_API_KEY']\n"
             "print('Anthropic key set:', bool(os.environ.get('ANTHROPIC_API_KEY')))\n"
             "print('Google/Gemini key set:', bool(os.environ.get('GOOGLE_API_KEY')))"),

    ("md", "## 2. Prompt template + output parser\n"
           "A **prompt template** is a reusable, parameterized prompt. An **output parser** "
           "turns the model's reply object into a plain string."),
    ("code", "from langchain_core.prompts import ChatPromptTemplate\n"
             "from langchain_core.output_parsers import StrOutputParser\n\n"
             "prompt = ChatPromptTemplate.from_messages([\n"
             "    ('system', 'You are a concise tutor for a CS course.'),\n"
             "    ('human', 'Explain {topic} to a {level} student in 2 sentences.'),\n"
             "])\n"
             "parser = StrOutputParser()\n"
             "print(prompt.invoke({'topic': 'embeddings', 'level': 'beginner'}))"),

    ("md", "## 3. A chain with Claude (LCEL `|` pipe)\n"
           "`chain = prompt | model | parser` — data flows left to right."),
    ("code", "try:\n"
             "    from langchain_anthropic import ChatAnthropic\n"
             "    claude = ChatAnthropic(model='claude-sonnet-4-6', max_tokens=300)\n"
             "    chain = prompt | claude | parser\n"
             "    print('CLAUDE:\\n', chain.invoke({'topic': 'vector stores',\n"
             "                                      'level': 'beginner'}))\n"
             "except Exception as e:\n"
             "    print('Claude chain skipped:', e)"),

    ("md", "## 4. The same chain with Gemini\n"
           "Only the model changes — prompt and parser are reused. That is the payoff of "
           "the common interface."),
    ("code", "try:\n"
             "    from langchain_google_genai import ChatGoogleGenerativeAI\n"
             "    gemini = ChatGoogleGenerativeAI(model='gemini-2.5-flash')\n"
             "    chain = prompt | gemini | parser\n"
             "    print('GEMINI:\\n', chain.invoke({'topic': 'vector stores',\n"
             "                                      'level': 'beginner'}))\n"
             "except Exception as e:\n"
             "    print('Gemini chain skipped:', e)"),

    ("md", "## 5. Document loaders & text splitters\n"
           "Load text, then split it into overlapping **chunks** small enough to embed."),
    ("code", "sample = (\n"
             "    'LangChain chains LLM steps with the pipe operator. '\n"
             "    'LlamaIndex indexes documents for question answering. '\n"
             "    'ChromaDB is an open-source vector store. '\n"
             "    'Embeddings turn text into vectors that capture meaning. '\n"
             "    'Retrieval-augmented generation grounds answers in your data.'\n"
             ")\n"
             "with open('notes.txt', 'w') as f:\n"
             "    f.write(sample)\n\n"
             "from langchain_community.document_loaders import TextLoader\n"
             "from langchain_text_splitters import RecursiveCharacterTextSplitter\n\n"
             "docs = TextLoader('notes.txt').load()\n"
             "splitter = RecursiveCharacterTextSplitter(chunk_size=120, chunk_overlap=20)\n"
             "chunks = splitter.split_documents(docs)\n"
             "print(len(chunks), 'chunks')\n"
             "for c in chunks:\n"
             "    print('-', c.page_content)"),

    ("md", "## 6. LlamaIndex — index a folder of docs\n"
           "LlamaIndex hides loader → splitter → embed → store behind `VectorStoreIndex`. "
           "We point its embeddings at a **local Hugging Face** model (no OpenAI)."),
    ("code", "import os\n"
             "os.makedirs('docs', exist_ok=True)\n"
             "with open('docs/notes.txt', 'w') as f:\n"
             "    f.write(sample)\n\n"
             "try:\n"
             "    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings\n"
             "    from llama_index.embeddings.huggingface import HuggingFaceEmbedding\n"
             "    Settings.embed_model = HuggingFaceEmbedding(\n"
             "        model_name='sentence-transformers/all-MiniLM-L6-v2')\n"
             "    Settings.llm = None  # retrieval only — no LLM needed for this demo\n"
             "    documents = SimpleDirectoryReader('docs').load_data()\n"
             "    index = VectorStoreIndex.from_documents(documents)\n"
             "    retriever = index.as_retriever(similarity_top_k=2)\n"
             "    hits = retriever.retrieve('What stores vectors?')\n"
             "    for h in hits:\n"
             "        print(round(h.score, 3), '|', h.node.get_content())\n"
             "except Exception as e:\n"
             "    print('LlamaIndex demo skipped (install llama-index-embeddings-huggingface):', e)"),

    ("md", "## 7. Recap\n"
           "- **Models** are swappable behind one interface (Claude ↔ Gemini).\n"
           "- **Prompt templates + parsers + chains** remove glue code.\n"
           "- **Loaders + splitters** prepare your documents.\n"
           "- **LlamaIndex** packages indexing into a few lines.\n\n"
           "Next notebook: embeddings and a **ChromaDB** vector store you can query."),
]
build_notebook(langchain_nb, os.path.join(CODE, "01_langchain_llamaindex.ipynb"))

# ---------------------------------------------------------------- notebook 2
chroma_nb = [
    ("md", "# Week 10 · Notebook 2 — Embeddings & a ChromaDB Vector Store\n"
           "**CSCI 250 · Fall 2026**\n\n"
           "Turn text into vectors with **Hugging Face sentence-transformers**, then build "
           "and query a **ChromaDB** vector store. No API key required for this notebook.\n\n"
           "> Cells degrade gracefully if a package is missing."),

    ("md", "## 0. Install"),
    ("code", "!pip -q install sentence-transformers chromadb langchain-chroma \\\n"
             "    langchain-huggingface numpy"),

    ("md", "## 1. Embeddings = meaning as vectors\n"
           "Texts with similar meaning land close together. We measure closeness with "
           "**cosine similarity** (1.0 = identical direction)."),
    ("code", "from sentence_transformers import SentenceTransformer\n"
             "import numpy as np\n\n"
             "model = SentenceTransformer('all-MiniLM-L6-v2')   # 384-dim, free, local\n"
             "texts = ['a cat on a mat', 'a kitten on a rug', 'the stock market fell']\n"
             "vecs = model.encode(texts)\n"
             "print('shape:', vecs.shape)\n\n"
             "def cos(a, b):\n"
             "    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))\n\n"
             "print('cat vs kitten:', round(cos(vecs[0], vecs[1]), 3))\n"
             "print('cat vs market:', round(cos(vecs[0], vecs[2]), 3))"),

    ("md", "## 2. A ChromaDB vector store (no key)\n"
           "Chroma auto-embeds your text with a built-in sentence-transformers model, "
           "so this runs offline."),
    ("code", "import chromadb\n"
             "client = chromadb.Client()                 # in-memory\n"
             "col = client.create_collection('week10')\n\n"
             "col.add(\n"
             "    documents=[\n"
             "        'LangChain chains LLM steps with the pipe operator.',\n"
             "        'ChromaDB is an open-source vector store for embeddings.',\n"
             "        'Embeddings capture the meaning of text as vectors.',\n"
             "        'LlamaIndex indexes documents for question answering.',\n"
             "        'Cosine similarity measures how close two vectors are.',\n"
             "    ],\n"
             "    ids=['d1', 'd2', 'd3', 'd4', 'd5'],\n"
             ")\n"
             "print('stored', col.count(), 'documents')"),

    ("md", "## 3. Similarity search\n"
           "Query by meaning, not keywords. Note the query word \"database\" never appears "
           "in the stored text, yet the vector-store result is still correct."),
    ("code", "res = col.query(query_texts=['What database holds vectors?'], n_results=2)\n"
             "for doc, dist in zip(res['documents'][0], res['distances'][0]):\n"
             "    print(round(dist, 3), '|', doc)"),

    ("md", "## 4. Persist to disk\n"
           "Swap `Client()` for `PersistentClient(path=...)` so your store survives restarts."),
    ("code", "pclient = chromadb.PersistentClient(path='./chroma_db')\n"
             "pcol = pclient.get_or_create_collection('persisted')\n"
             "pcol.add(documents=['This survives a kernel restart.'], ids=['p1'])\n"
             "print('persisted count:', pcol.count())"),

    ("md", "## 5. LangChain's Chroma wrapper + your own embeddings\n"
           "This plugs straight into LangChain chains and lets you choose the embedding "
           "model explicitly."),
    ("code", "try:\n"
             "    from langchain_chroma import Chroma\n"
             "    from langchain_huggingface import HuggingFaceEmbeddings\n"
             "    from langchain_core.documents import Document\n\n"
             "    emb = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')\n"
             "    docs = [Document(page_content=t) for t in [\n"
             "        'Chunking splits long text into overlapping pieces.',\n"
             "        'Retrieval finds the chunks most relevant to a question.',\n"
             "        'Grounding stuffs retrieved chunks into the prompt.',\n"
             "    ]]\n"
             "    store = Chroma.from_documents(docs, embedding=emb)\n"
             "    for d in store.similarity_search('How do we pick relevant text?', k=2):\n"
             "        print('-', d.page_content)\n"
             "except Exception as e:\n"
             "    print('LangChain Chroma demo skipped:', e)"),

    ("md", "## 6. Optional: Gemini embeddings instead of local\n"
           "If you have a Gemini key and want hosted embeddings (still **not** OpenAI), use "
           "`GoogleGenerativeAIEmbeddings` with model `text-embedding-004`."),
    ("code", "import os\n"
             "try:\n"
             "    if not os.environ.get('GOOGLE_API_KEY') and os.environ.get('GEMINI_API_KEY'):\n"
             "        os.environ['GOOGLE_API_KEY'] = os.environ['GEMINI_API_KEY']\n"
             "    from langchain_google_genai import GoogleGenerativeAIEmbeddings\n"
             "    gemb = GoogleGenerativeAIEmbeddings(model='models/text-embedding-004')\n"
             "    v = gemb.embed_query('embeddings turn text into vectors')\n"
             "    print('Gemini embedding length:', len(v))\n"
             "except Exception as e:\n"
             "    print('Gemini embeddings skipped (no key / package):', e)"),

    ("md", "## 7. Recap\n"
           "You built and queried a real vector store. Next week we add the **generation** "
           "step: retrieve relevant chunks, ground a Claude/Gemini prompt in them, and cite "
           "the sources — that is **RAG**."),
]
build_notebook(chroma_nb, os.path.join(CODE, "02_embeddings_chromadb.ipynb"))

print("wrote Week 10 notebooks (00, 01, 02) to", CODE)
