"""Build the CSCI 250 Fall 2026 promotional flyer (PDF + PNG) with matplotlib.
Run: python build_flyer.py   ->  CSCI250-Flyer-Fall2026.pdf / .png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.image as mpimg

HERE = os.path.dirname(os.path.abspath(__file__))
QR = os.path.join(HERE, "..", "..", "assets", "qr-intro2ai.png")

NAVY = "#0B1F3A"; TEAL = "#128C8C"; LIGHT = "#F2F5F8"
INK = "#1A1A1A"; GREY = "#5B6470"; GREEN = "#2E8B57"; CREAM = "#CFE3E3"; MIST = "#9FC6C6"
W, H = 8.5, 11.0  # inches

fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

def band(y, h, color, x=0, w=W):
    ax.add_patch(Rectangle((x, y), w, h, color=color, zorder=0))

def txt(x, y, s, size, color=INK, weight="normal", ha="left", va="baseline", style="normal"):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va,
            style=style, family="DejaVu Sans", zorder=3)

# ---------- Header (navy) ----------
band(H - 1.85, 1.85, NAVY)
txt(0.6, H - 0.62, "PALOMAR COLLEGE  ·  COMPUTER SCIENCE (CSIT)", 11.5, MIST, "bold")
txt(0.6, H - 1.06, "Introduction to Artificial Intelligence", 25, "white", "bold")
txt(0.6, H - 1.55, "CSCI 250   ·   Fall 2026   ·   4 Units   ·   Online", 14.5, CREAM, "bold")

# teal rule
band(H - 1.92, 0.07, TEAL)

# ---------- Tagline (light) ----------
band(H - 2.5, 0.58, LIGHT)
band(H - 2.5, 0.58, TEAL, x=0, w=0.09)
txt(0.62, H - 2.24, "Now with deep, hands-on coverage of Large Language Models,", 13, NAVY, "bold")
txt(0.62, H - 2.46, "Generative AI & AI-assisted coding.", 13, NAVY, "bold")

# ---------- Intro ----------
intro = [
    "Artificial Intelligence is the defining technology of the decade — and generative AI",
    "has put it in everyone's hands. In this project-based, beginner-friendly course you'll go",
    "from the fundamentals of machine learning to building and deploying your own AI",
    "applications using the same tools professionals use today. No expensive textbook and",
    "no costly hardware — everything runs free in your browser.",
]
y = H - 2.95
for line in intro:
    txt(0.6, y, line, 11.3, "#2b2b2b"); y -= 0.26

# ---------- What you'll build & learn ----------
y_h = y - 0.12
txt(0.6, y_h, "What you'll build & learn", 15, NAVY, "bold")
band(0.6, 0.0, LIGHT)  # noop placeholder
ax.add_patch(Rectangle((0.6, y_h - 0.12), W - 1.2, 0.02, color=LIGHT, zorder=1))

left = [
    "ML & neural-network foundations in Python",
    "How LLMs really work — build a tokenizer",
    "    and attention from scratch",
    "Prompt engineering & reasoning",
    "Retrieval-Augmented Generation (RAG)",
    "    over your own data",
]
right = [
    "AI agents & tool use (Model Context",
    "    Protocol)",
    "AI-assisted coding with Claude Code",
    "Multimodal AI, fine-tuning & evaluation",
    "Capstone: build & deploy your own",
    "    AI assistant",
]

def bullets(items, x):
    yy = y_h - 0.4
    for it in items:
        if it.startswith("    "):
            txt(x + 0.28, yy, it.strip(), 11, "#222")
        else:
            txt(x + 0.04, yy, "▸", 11.5, TEAL, "bold")
            txt(x + 0.28, yy, it, 11, "#222")
        yy -= 0.275
    return yy

yl = bullets(left, 0.6)
yr = bullets(right, 4.5)
y_after = min(yl, yr) - 0.05

# ---------- Pills ----------
pills = [("100% Online", TEAL), ("Asynchronous", NAVY), ("$0 Textbook Cost", GREEN),
         ("Hands-on Projects", NAVY), ("Portfolio Capstone", TEAL)]
PSIZE = 10.0
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
px_per_in = fig.dpi
gap = 0.13
widths = []
for label, _ in pills:
    t = ax.text(0, -5, label, fontsize=PSIZE, fontweight="bold", family="DejaVu Sans")
    bb = t.get_window_extent(renderer=renderer)
    widths.append(bb.width / px_per_in + 0.30)  # text width + horizontal padding
    t.remove()
max_w = W - 1.2  # honor 0.6in margins
total = sum(widths) + gap * (len(pills) - 1)
if total > max_w:  # scale-to-fit so nothing clips
    s = max_w / total
    widths = [w * s for w in widths]
    gap *= s
    total = max_w
xstart = (W - total) / 2
yp = y_after - 0.1
for (label, color), wpill in zip(pills, widths):
    ax.add_patch(FancyBboxPatch((xstart, yp - 0.15), wpill, 0.30,
                 boxstyle="round,pad=0.015,rounding_size=0.15", linewidth=0,
                 facecolor=color, zorder=2))
    txt(xstart + wpill / 2, yp, label, PSIZE, "white", "bold", ha="center", va="center")
    xstart += wpill + gap

# ---------- Tools ----------
yt = yp - 0.5
txt(W / 2, yt, "Tools you'll use:  Anthropic Claude  ·  Claude Code  ·  Google Gemini  ·  Hugging Face  ·  Ollama",
    11, GREY, ha="center")

# ---------- Footer (navy) ----------
FH = 1.7
band(0, FH, NAVY)
txt(0.6, FH - 0.4, "Instructor:", 10.5, MIST, "bold")
txt(1.5, FH - 0.4, "Gheni Abla   ·   gabla@palomar.edu", 10.5, "white")
txt(0.6, FH - 0.7, "Prerequisite:", 10.5, MIST, "bold")
txt(1.65, FH - 0.7, "CSCI 114 (grade of “C” or better)", 10.5, "white")
txt(0.6, FH - 1.0, "Format:", 10.5, MIST, "bold")
txt(1.35, FH - 1.0, "Online, fully asynchronous", 10.5, "white")
txt(0.6, FH - 1.36, "Enroll →  palomar.edu/how-to-register", 13, "#7FE3E3", "bold")
txt(0.6, FH - 1.6, "Questions or trouble enrolling?  Email gabla@palomar.edu", 10, CREAM)

# QR on right of footer
if os.path.exists(QR):
    img = mpimg.imread(QR)
    qx, qy, qs = W - 1.85, FH - 1.42, 1.18
    ax.add_patch(Rectangle((qx - 0.06, qy - 0.06), qs + 0.12, qs + 0.12, color="white", zorder=2))
    ax.imshow(img, extent=[qx, qx + qs, qy, qy + qs], zorder=3, aspect="auto")
    txt(qx + qs / 2, qy - 0.16, "Scan for course info & enrollment", 8, MIST, ha="center")

out_pdf = os.path.join(HERE, "CSCI250-Flyer-Fall2026.pdf")
out_png = os.path.join(HERE, "CSCI250-Flyer-Fall2026.png")
fig.savefig(out_pdf)
fig.savefig(out_png, dpi=150)
print("wrote", out_pdf)
print("wrote", out_png)
