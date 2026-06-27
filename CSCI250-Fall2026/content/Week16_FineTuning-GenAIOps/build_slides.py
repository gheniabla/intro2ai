"""Build slides.pptx for Week 16. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 16 — Fine-Tuning, GenAI Ops & Deployment",
     "subtitle": "CSCI 250 — Introduction to Artificial Intelligence · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "Decide: prompt vs. RAG vs. fine-tune",
        "How fine-tuning works: data, epochs, overfitting",
        "PEFT / LoRA — fine-tune without melting your GPU",
        "GPUs for LLMs: memory & quantization",
        "GenAI Ops: serve, monitor, control cost & latency",
        ("No graded assignment — keep building your Final Project", 1)]},

    {"type": "section", "title": "Prompt vs. RAG vs. Fine-Tune"},
    {"type": "bullets", "title": "Work Down the Ladder (cheapest first)", "bullets": [
        "1. Prompting — changes behavior & format (try first)",
        "2. RAG — changes knowledge (facts, freshness)",
        "3. Fine-tuning — changes the model (style, narrow task, latency)",
        ("Made-up facts about your domain? → RAG, not fine-tuning", 1),
        ("Want a small, cheap, fast specialist? → fine-tune", 1)]},

    {"type": "section", "title": "How Fine-Tuning Works"},
    {"type": "two_col", "title": "The Dataset Is the Project",
     "left_title": "Data",
     "left": ["input→output pairs (chat turns)",
              "few hundred CLEAN examples beat 1000s noisy",
              "hold out a validation split"],
     "right_title": "Knobs",
     "right": ["epoch = one pass over data",
               "learning rate = step size",
               "val loss climbs → overfitting"]},

    {"type": "section", "title": "PEFT / LoRA"},
    {"type": "bullets", "title": "Fine-Tune Without Full Retraining", "bullets": [
        "Full fine-tune = update ALL billions of weights (costly)",
        "PEFT: freeze base, train a tiny set of new params",
        "LoRA: add small low-rank A·B beside frozen W (rank r ~8-16)",
        "Train <1% of params; save a small adapter (MB, not GB)",
        ("QLoRA: load base in 4-bit + LoRA → fine-tune on one Colab GPU", 1)]},
    {"type": "code", "title": "A LoRA Config (Hugging Face PEFT)",
     "code": "from peft import LoraConfig\n"
             "lora = LoraConfig(\n"
             "    r=8, lora_alpha=16, lora_dropout=0.05,\n"
             "    target_modules=[\"q_proj\", \"v_proj\"],\n"
             "    task_type=\"CAUSAL_LM\",\n"
             ")",
     "caption": "Full runnable demo in 01_lora_finetune_demo.ipynb"},

    {"type": "section", "title": "GPUs & Quantization"},
    {"type": "bullets", "title": "Memory Is the Limit", "bullets": [
        "GPUs do massive parallel matrix math (10-100x CPU)",
        "Loading rule: FP16 ~2 GB / billion params",
        "8-bit ~1 GB/B · 4-bit ~0.5 GB/B",
        "7B model: ~14 GB FP16 → ~4-5 GB in 4-bit",
        ("Quantization (16→8→4 bit) = small accuracy hit, big memory win", 1)]},

    {"type": "section", "title": "GenAI Ops & Deployment"},
    {"type": "code", "title": "Serve a Pipeline as an API",
     "code": "from flask import Flask, request, jsonify\n"
             "import anthropic\n"
             "app = Flask(__name__)\n"
             "client = anthropic.Anthropic()  # ANTHROPIC_API_KEY from env\n\n"
             "@app.post(\"/chat\")\n"
             "def chat():\n"
             "    m = client.messages.create(\n"
             "        model=\"claude-haiku-4-5-20251001\", max_tokens=300,\n"
             "        messages=[{\"role\": \"user\",\n"
             "                   \"content\": request.json[\"message\"]}])\n"
             "    return jsonify({\"reply\": m.content[0].text})",
     "caption": "Hosted API = no GPU to run; self-hosted = privacy + per-token control",
     "code_size": 13},
    {"type": "bullets", "title": "Monitor & Control Cost / Latency", "bullets": [
        "Latency: time-to-first-token + total time",
        "Cost: priced per token — cap max_tokens, track usage",
        "Pick the smallest model that passes eval; route easy → cheap",
        "Cache repeats; shorten context (RAG); quantize self-hosted",
        ("Log prompts/responses → re-score (Week 17 eval harness)", 1)]},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Read the document + skim PEFT/quantization docs",
        "Run 01_lora_finetune_demo.ipynb on a Colab GPU",
        "Skim 02_serving_sketch.ipynb (API + monitoring)",
        "Apply one cost/latency lever to your Final Project",
        "No graded assignment — keep building!"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
