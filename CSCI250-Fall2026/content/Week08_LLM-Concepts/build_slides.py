"""Build slides.pptx for Week 8 — LLM Concepts. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 8 — LLM Concepts, Frameworks & Tools",
     "subtitle": "CSCI 250 — Introduction to Artificial Intelligence · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "How LLMs work: next-token prediction",
        "Tokens & tokenization; the context window",
        "Sampling: temperature, top-p, max_tokens",
        "In-context learning: zero-shot & few-shot",
        "Capabilities & failure modes (hallucination)",
        "From scratch: build a BPE tokenizer + attention in NumPy",
        "Hands-on: Claude + Gemini + a local model"]},

    {"type": "section", "title": "How LLMs Work"},
    {"type": "bullets", "title": "Next-Token Prediction", "bullets": [
        "An LLM is a large Transformer neural network (builds on Week 6)",
        "Trained to predict the next token from the tokens so far",
        "Chat = repeat: predict → append → predict (autoregressive)",
        ("No database lookup — text is generated, not retrieved", 1),
        ("This is why LLMs are fluent AND why they can make things up", 1)]},

    {"type": "bullets", "title": "Tokens & the Context Window", "bullets": [
        "Models see tokens (sub-word IDs), not characters or words",
        "Rule of thumb: 1 token ≈ 4 chars ≈ 0.75 words; rare words split into several",
        "You pay per token; max_tokens caps the response",
        "Context window = max tokens the model can attend to at once",
        ("Prompt + generated reply must both fit inside it", 1),
        ("No memory between API calls — the client replays history", 1),
        ("Long docs need chunking → RAG (Week 11)", 1)]},

    {"type": "code", "title": "Sampling Parameters",
     "code": "msg = client.messages.create(\n"
             "    model=\"claude-sonnet-4-6\",\n"
             "    max_tokens=200,       # caps the RESPONSE length + cost\n"
             "    temperature=0.0,      # 0 = focused; ~1.0 = creative\n"
             "    messages=[{\"role\": \"user\",\n"
             "               \"content\": \"List 3 uses of LLMs.\"}],\n"
             ")\nprint(msg.content[0].text)",
     "caption": "temp=0 for extraction/code; temp~0.7–1.0 for brainstorming. top-p = nucleus sampling."},

    {"type": "code", "title": "In-Context Learning (Few-Shot)",
     "code": "Review: \"Loved every minute.\" -> positive\n"
             "Review: \"A complete waste of time.\" -> negative\n"
             "Review: \"The acting saved a dull script.\" ->",
     "caption": "Examples in the prompt teach the task + output format — no retraining. Foundation for Week 9."},

    {"type": "two_col", "title": "What LLMs Can & Can't Do",
     "left_title": "Strengths",
     "left": ["Summarize, draft, translate", "Classify & extract structure",
              "Write & refactor code", "Flexible reasoning over text"],
     "right_title": "Failure modes",
     "right": ["Hallucination (confident & wrong)", "Knowledge cutoff",
               "Weak exact math / counting", "Prompt sensitivity; bias"]},
    {"type": "bullets", "title": "Mitigating Hallucination", "bullets": [
        "Treat output as a confident DRAFT, not a source of truth",
        "Ground answers in supplied context (RAG, Week 11)",
        "Ask for sources; set temperature=0 for factual tasks",
        "Give the model tools (Week 13); verify anything important"]},

    {"type": "bullets", "title": "Under the Hood: Byte-Pair Encoding, From Scratch", "bullets": [
        "Start from raw bytes (vocab of 256)",
        "Count every adjacent pair of tokens",
        "Merge the most frequent pair into a new token; repeat",
        ("encode = replay merges; decode = bytes back → exact round-trip", 1),
        ("Tradeoff: bigger vocab = shorter sequences (fewer tokens to pay for)", 1),
        ("Why an LLM can't count the r's in 'strawberry': it's one token", 1)]},
    {"type": "code", "title": "The Core of BPE: merge a pair",
     "code": "def merge(ids, pair, new_id):     # replace every (a,b)\n"
             "    a, b = pair; out = []; i = 0\n"
             "    while i < len(ids):\n"
             "        if i < len(ids)-1 and ids[i]==a and ids[i+1]==b:\n"
             "            out.append(new_id); i += 2\n"
             "        else:\n"
             "            out.append(ids[i]); i += 1\n"
             "    return out\n\n"
             "# loop: count pairs -> merge most frequent -> repeat\n"
             "# then encode/decode round-trips your own text exactly",
     "caption": "code/03_build_bpe_tokenizer.ipynb — Karpathy minbpe / CS336 style, pure Python."},

    {"type": "section", "title": "The Idea Behind Transformers: Attention"},
    {"type": "bullets", "title": "Scaled Dot-Product Attention", "bullets": [
        "Each word → Q (query), K (key), V (value) vectors",
        "scores = Q·Kᵀ / √d  — how much each word matches each other word",
        "softmax each row → attention weights that sum to 1",
        "output = weights · V — a context-aware mix of the value vectors",
        ("Heatmap of the weights shows which words attend to which", 1),
        ("Multi-head = run it in parallel; stack layers → a Transformer", 1)]},
    {"type": "code", "title": "Attention in 3 Lines of NumPy",
     "code": "scores  = (Q @ K.T) / np.sqrt(d)   # match strength\n"
             "weights = softmax_rows(scores)     # rows sum to 1\n"
             "output  = weights @ V              # context mix\n\n"
             "# plot 'weights' as a heatmap -> the engine, made visible",
     "caption": "code/04_attention_from_scratch.ipynb — the operation inside every LLM, in pure NumPy."},

    {"type": "two_col", "title": "Three Ways to Run a Model",
     "left_title": "Cloud APIs (need a key)",
     "left": ["Anthropic Claude — messages.create", "Google Gemini + AI Studio"],
     "right_title": "Local (no key, no cost)",
     "right": ["Ollama (Llama, Mistral, Gemma)", "Hugging Face transformers"]},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Read the Compact Guide to LLMs (tokens, context, sampling)",
        "Run 01_llm_concepts.ipynb + 02_claude_gemini_local.ipynb",
        "Build the BPE tokenizer (03) — fill-ins + round-trip on your text",
        "Build attention (04) — fill-ins + paste your heatmap",
        "Do the hallucination hunt + comparison table",
        "Submit Assignment A7 by Sunday 11:59 PM PT"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
