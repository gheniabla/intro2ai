# Week 15 — Multi-modal LLMs & Generative Media
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of November 30, 2026 · Online / Asynchronous*

---

## Learning objectives
By the end of this week you will be able to:
1. Explain what makes a model **multimodal** and how text + image (and audio) get into the same model.
2. Send an **image plus a prompt** to **Claude** (`claude-sonnet-4-6`) and **Gemini** (`gemini-2.5-flash` / `gemini-2.5-pro`) and read the response.
3. Use vision models for practical tasks: **describe/analyze** an image, **OCR** text, and **read a chart** into structured data (JSON).
4. Understand, conceptually, how **image generation (diffusion)** works and how it differs from understanding.
5. Apply multimodal thinking to your **Capstone** — optionally extend "My Assistant" to **v4 (multimodal)** for the Multimodal track.

> **Time budget:** ~10 hours (lecture + slides + videos + two notebooks + Capstone work). There is **no separate weekly assignment** this week — your graded work continues through the **Capstone milestones**.

---

## 1. What "multimodal" means
A **modality** is a kind of input/output: text, images, audio, video. A **multimodal LLM** can accept more than one modality in a single prompt. This week we focus on **vision-language models (VLMs)** — models that take **images + text** and respond in text.

The key idea: an image is turned into **tokens the model can attend to alongside text tokens.** A vision encoder splits the image into patches and projects them into the same embedding space as words, so the transformer can "read" the picture and your question together. You do not need to manage any of that — you just send the bytes and a prompt.

What VLMs are good at this week:
- **Describing** scenes and objects (captioning, alt-text for accessibility).
- **Reading text in images** (OCR) — receipts, signs, handwriting, screenshots.
- **Interpreting charts and tables** — pulling numbers and trends out of a figure.
- **Visual question answering** — "how many people are wearing hats?"

What they are *not*: pixel-perfect measurement tools. They can **hallucinate** details, miscount, or misread blurry text. Always treat outputs as a draft to verify.

---

## 2. Sending an image to a model
Both SDKs accept an image as **base64-encoded bytes** with a media type, next to your text prompt. The mental model is the same for Claude and Gemini; only the call shape differs.

### 2.1 Claude (Anthropic SDK)
Claude takes a `messages` list where the user `content` is a **list of blocks** — one image block and one text block:
```python
import anthropic, base64
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

img_b64 = base64.standard_b64encode(open("chart.png", "rb").read()).decode()
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    messages=[{"role": "user", "content": [
        {"type": "image", "source": {
            "type": "base64", "media_type": "image/png", "data": img_b64}},
        {"type": "text", "text": "Describe this chart and list the values you can read."},
    ]}],
)
print(msg.content[0].text)
```

### 2.2 Gemini (google-generativeai SDK)
Gemini lets you pass a `PIL.Image` (or raw bytes) directly alongside the prompt string:
```python
import google.generativeai as genai
from PIL import Image
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")
img = Image.open("chart.png")
resp = model.generate_content(
    ["Describe this chart and list the values you can read.", img])
print(resp.text)
```

Same prompt, two providers — comparing their answers is the heart of this week's lab.

---

## 3. Practical task 1 — describe & analyze
The simplest use: hand the model a photo and ask an open question. Good prompts are **specific about the output you want**:
- "In 2 sentences, describe this image for a screen reader." (accessibility alt-text)
- "List every object you see, then guess where this photo was taken."
- "Is there any text in this image? Quote it exactly."

Specificity reduces rambling and makes outputs easier to use downstream.

---

## 4. Practical task 2 — OCR (reading text in images)
Vision models are surprisingly strong at **optical character recognition** without a dedicated OCR library. Ask for the text *and a structure*:
```python
prompt = ("Extract all text from this receipt. Return JSON with keys: "
          "vendor, date, items (list of {name, price}), total. "
          "If a field is unreadable, use null.")
```
Asking for **JSON** turns a vision model into a small extraction pipeline — exactly the spine of the Final Project "Receipt Reader" (Track D). Always **validate** the JSON (`json.loads`) and handle the case where the model adds prose around it.

---

## 5. Practical task 3 — reading charts
Charts are images of data. A VLM can recover **approximate** values and the overall trend:
```python
prompt = ("This is a bar chart. Return a JSON list of {label, value} for each bar, "
          "then state in one sentence which is largest. Values are approximate.")
```
This is powerful for analytics and accessibility, but remember the values are **estimated from pixels** — fine for "which is biggest," not for accounting. We build a chart with Matplotlib and read it back in Notebook 2 so you can check the model's accuracy against ground truth.

---

## 6. A note on audio (briefly)
Gemini also accepts **audio** files (e.g., transcribe or summarize a clip) via the same `generate_content([...])` pattern with an uploaded audio part — the simplest free path for audio. Claude's API is image+text focused; for audio with Claude you would transcribe first and pass the text. To transcribe locally, use the **open-source Whisper model via Hugging Face** (`transformers`) or **faster-whisper** — these are the openly licensed speech-to-text weights you run yourself, **not** the OpenAI hosted product. We mention audio for awareness — the lab stays on images.

---

## 7. Image **generation** — diffusion, conceptually
Everything above is **understanding** (image → text). The other half of multimodal AI is **generation** (text → image), and it uses a different family of models: **diffusion models** (e.g., Imagen, Stable Diffusion).

The intuition:
1. **Training:** take real images and progressively add random **noise** until they are pure static. Train a neural network to **predict and remove** that noise, step by step.
2. **Generation:** start from pure noise and run the network **in reverse**, denoising a little at a time, **steered by your text prompt** (via a text encoder), until a coherent image emerges.

So a diffusion model "sculpts" an image out of noise, guided by your words. This is fundamentally different from the autoregressive next-token prediction that powers text LLMs. Trade-offs to know: generated images can contain artifacts, reflect **training-data biases**, and raise **copyright/consent** concerns — generation is the part of GenAI with the sharpest ethics questions. We treat generation **conceptually** this week (no required generation API), and revisit safety in Week 17.

---

## 8. Choosing & calling a vision model
- **Claude `claude-sonnet-4-6`** — strong reasoning over images, good at structured extraction and "explain this diagram."
- **Gemini `gemini-2.5-flash`** — fast and cheap; great default for description/OCR. Use **`gemini-2.5-pro`** when you need deeper reasoning on a hard image.
- **Local/open VLMs** (e.g., LLaVA via Ollama) exist too — useful when data can't leave your machine, at some quality cost.
- **Always** load keys from Colab Secrets / env vars, never hard-code them. The notebooks **degrade gracefully**: if no key is set, they print a clear message instead of crashing.

---

## 9. Reading & videos
- Anthropic **Vision** docs and Google **Gemini multimodal** docs (linked in Canvas) — required skim.
- *Compact Guide to Large Language Models* (Canvas) — the multimodal section.
- Video: "How diffusion models work" (linked in Canvas) — for §7.
- Optional: a short read on **alt-text & accessibility** to motivate Task 1.

---

## 10. Lab — Capstone work: "My Assistant" v4 (optional multimodal)
There is **no separate weekly assignment** this week. This is **Capstone work** — keep growing "My Assistant" toward **v4 (optional multimodal)**. If you're on the **Multimodal** track, this week's notebooks are the spine of your build; on any other track, adding image understanding is optional polish, not required.

**Do this week:**
1. Run `code/01_multimodal_basics.ipynb` — send a sample image to **Claude** and **Gemini** and compare descriptions/OCR.
2. Run `code/02_charts_and_extraction.ipynb` — generate a chart with Matplotlib, have a vision model read it back as JSON, and **check accuracy** against the true values.
3. **Capstone work:** advance "My Assistant" toward **v4**. Multimodal-track students adapt these notebooks directly into the assistant; other tracks may optionally bolt on a vision feature, or simply keep progressing their core milestones.
4. Post a short **progress update** in the discussion (2–3 sentences + one screenshot). Include a one-line **AI Use** note.

*Graded as part of the **Capstone milestone arc** (see `capstone/` and the rubric); there is no standalone weekly assignment for this week.*

---

## Key terms
**modality**, **multimodal**, **vision-language model (VLM)**, **vision encoder**, **image patch/token**, **base64**, **OCR**, **chart reading**, **structured/JSON output**, **visual question answering**, **diffusion model**, **denoising**, **image generation**, **alt-text**, **hallucination**.
