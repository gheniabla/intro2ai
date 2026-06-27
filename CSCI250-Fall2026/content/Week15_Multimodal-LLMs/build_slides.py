"""Build slides.pptx for Week 15. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 15 — Multi-modal LLMs & Generative Media",
     "subtitle": "CSCI 250 — Introduction to Artificial Intelligence · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "What 'multimodal' means: text + image (+ audio) in one prompt",
        "Send an image to Claude and Gemini vision models",
        "Practical tasks: describe, OCR, read a chart into JSON",
        "Image GENERATION (diffusion) — conceptually",
        "Final Project continues (A7) — Week 15 milestone"]},

    {"type": "section", "title": "What Multimodal Means"},
    {"type": "bullets", "title": "From Pixels to Tokens", "bullets": [
        "Modality = a kind of input/output: text, image, audio, video",
        "Vision-Language Model (VLM): images + text in, text out",
        "A vision encoder splits the image into patches → embeddings",
        "Patches live in the same space as word tokens → model 'reads' both",
        ("You just send the bytes + a prompt — no encoding to manage", 1)]},
    {"type": "two_col", "title": "Good At / Not Good At",
     "left_title": "Good at",
     "left": ["Describing scenes (alt-text)", "OCR: receipts, signs, handwriting",
              "Reading charts & tables", "Visual Q&A"],
     "right_title": "Watch out",
     "right": ["Miscounting objects", "Misreading blurry text",
               "Hallucinated details", "Not pixel-perfect — verify!"]},

    {"type": "section", "title": "Calling Vision Models"},
    {"type": "code", "title": "Image → Claude (Anthropic SDK)",
     "code": "import anthropic, base64\n"
             "client = anthropic.Anthropic()\n"
             "b64 = base64.standard_b64encode(open('chart.png','rb').read()).decode()\n"
             "msg = client.messages.create(\n"
             "    model='claude-sonnet-4-6', max_tokens=500,\n"
             "    messages=[{'role':'user','content':[\n"
             "        {'type':'image','source':{'type':'base64',\n"
             "            'media_type':'image/png','data':b64}},\n"
             "        {'type':'text','text':'Describe this chart.'}]}])\n"
             "print(msg.content[0].text)",
     "caption": "User content is a LIST of blocks: one image + one text"},
    {"type": "code", "title": "Image → Gemini (google-generativeai)",
     "code": "import google.generativeai as genai\n"
             "from PIL import Image\n"
             "genai.configure(api_key=os.environ['GEMINI_API_KEY'])\n"
             "model = genai.GenerativeModel('gemini-2.5-flash')\n"
             "img = Image.open('chart.png')\n"
             "resp = model.generate_content(\n"
             "    ['Describe this chart.', img])\n"
             "print(resp.text)",
     "caption": "Pass a PIL.Image right next to the prompt string"},

    {"type": "section", "title": "Practical Tasks"},
    {"type": "bullets", "title": "Describe · OCR · Charts", "bullets": [
        "Describe: 'In 2 sentences, write screen-reader alt-text.'",
        "OCR: 'Extract the text. Quote it exactly.'",
        "Receipt → JSON: vendor, date, items[], total (null if unreadable)",
        "Chart → JSON: list of {label, value}; values are approximate",
        ("Ask for JSON → validate with json.loads() downstream", 1)]},
    {"type": "code", "title": "Vision as an Extraction Pipeline",
     "code": "prompt = ('Extract all text from this receipt. Return JSON '\n"
             "          'with keys: vendor, date, items (list of '\n"
             "          '{name, price}), total. Null if unreadable.')\n"
             "# ... send prompt + image to Claude or Gemini ...\n"
             "import json\n"
             "data = json.loads(response_text)   # validate!\n"
             "print(data['total'])",
     "caption": "Same spine as the Final Project 'Receipt Reader' (Track D)"},

    {"type": "section", "title": "Image Generation: Diffusion"},
    {"type": "two_col", "title": "Diffusion in Two Steps",
     "left_title": "Training",
     "left": ["Add noise to real images", "...until pure static",
              "Train a net to REMOVE the noise"],
     "right_title": "Generating",
     "right": ["Start from pure noise", "Denoise step by step",
               "Steered by your text prompt", "→ a coherent image emerges"]},
    {"type": "bullets", "title": "Generation & Model Choice", "bullets": [
        "Diffusion differs from text LLMs (next-token) — it 'sculpts' from noise",
        "Models: Imagen, Stable Diffusion (conceptual this week)",
        "Artifacts, bias, copyright/consent — sharpest-ethics GenAI (Wk 17)",
        "Vision: claude-sonnet-4-6 (reasoning) · gemini-2.5-flash (fast OCR)",
        "gemini-2.5-pro for hard images · local LLaVA when data must stay put",
        ("Keys from Colab Secrets / env vars — never hard-code", 1)]},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Read: Claude Vision + Gemini multimodal docs",
        "Run 01_multimodal_basics.ipynb — Claude vs Gemini",
        "Run 02_charts_and_extraction.ipynb — read a chart as JSON",
        "Hit your Week 15 Final-Project milestone (end-to-end)",
        "Post a progress update + screenshot (with AI-Use note)"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
